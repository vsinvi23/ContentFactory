# Strategies_for_Handling_Messy_Data_in_Forward_Deployed_Engineering

Source: https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Working with Messy Data

Explore how to profile real inputs before cleaning them, and how normalization differs from inventing missing information. Understand how to prevent join inflation, preserve conflicts, and account for every source row in a disposition ledger, preparing you to deliver totals a customer can trust.

We'll cover the following...

- [Why totals go wrong](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Why-totals-go-wrong)
- [Profiling the source data](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Profiling-the-source-data)
- [Normalizing without inventing data](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Normalizing-without-inventing-data)
- [Preventing join inflation](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Preventing-join-inflation)
- [Accounting for every row](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Accounting-for-every-row)
- [Making reruns repeatable](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Making-reruns-repeatable)
- [Which rules transfer to the stock export?](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Which-rules-transfer-to-the-stock-export)

The command completes without errors and outputs energy totals by region. However, one reading is counted twice, a site is assigned to two regions, and several source rows are excluded during data cleaning without explanation. The report is generated, but its results cannot be fully verified against the source data.

For this separate facilities-export assignment, report accepted energy totals by region and provide an auditable record of every excluded or unresolved source row. Treat this as a separate assignment from the dispatch project.

## Why totals go wrong[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Why-totals-go-wrong)

Start with the actual files. In `sites.csv`, the columns are `site_id,region`, and the four data rows are:

1. `001,North`
2. `002,West`
3. `002,East`
4. `003,South`

In `energy_readings.csv`, the columns are `reading_id,site_id,reading_date,amount,unit`. The eight data rows, in order, are:

1. `R1, 001 ,2026-09-01,1.5,kWh`
2. `R1,001,2026-09-01,1500,Wh`
3. `R2,002,2026-09-01,2,kWh`
4. `R3,009,2026-09-01,300,Wh`
5. `R4,003,03/04/2026,1,kWh`
6. `R5,003,2026-09-01,,Wh`
7. `R6,003,2026-09-01,500,Wh`
8. `R7,001,2026-09-01,250,kW`

In reading row 1, the identifier `001` contains leading and trailing whitespace in the source field. Row 6 contains a blank energy amount. In this example, `source_row` is the one-based index of each data row, excluding the header.

The export contract allows trimming identifier whitespace but requires preserving leading zeros, using ISO-formatted dates, and accepting only nonnegative energy values expressed in Wh or kWh. The contract does not specify which of the two region assignments for site `002` takes precedence.

A cleaned dataset may still be incorrect if processing infers missing dates, replaces blank amounts with zero, or silently removes unmatched rows. These operations alter the source data's meaning rather than simply standardizing its format.

## Profiling the source data[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Profiling-the-source-data)

**Data profiling** involves examining source data to identify its structure, distributions, and quality issues before defining transformation rules. For small datasets, inspect every row alongside summary statistics. A single row cannot establish that an entire column contains valid data.

The dataset profile shows the following:

- **Sites:** Four site records contain three distinct IDs and no missing fields. Site `002` appears twice with conflicting region assignments: West and East.
- **Reading identities:** Eight reading records contain seven distinct reading IDs. Reading `R1` appears in source rows 1 and 2.
- **Amounts:** Source row 6 has a missing energy amount; the remaining seven amounts are numeric and nonnegative.
- **Units:** The dataset contains three `kWh` values, four `Wh` values, and one `kW` value. Source row 8 uses `kW`, which is not an accepted energy unit.
- **Dates:** Seven dates use ISO format. Source row 5 contains `03/04/2026`, which does not meet the required format.
- **Site references:** Source row 1 contains leading and trailing whitespace in its site identifier. After trimming identifier whitespace as permitted by the contract, site references occur as follows: `001` (three), `002` (one), `003` (three), and `009` (one). Site `009` has no matching site record.

Keep identifiers as strings while profiling. Converting `001` to integer `1` loses information. Even trimming whitespace or changing case needs permission from the source contract; another export may use case-sensitive identifiers or significant spaces.

These findings establish three different problems: representation differences, invalid values, and unresolved relationships. Each needs its own rule.

## Normalizing without inventing data[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Normalizing-without-inventing-data)

A **canonical schema** gives sources a shared representation while retaining their meaning and provenance. Use these fields for a normalized reading:

- **`reading_id`****and** **`site_id`****:** Nonempty strings, trimmed under this contract, with leading zeros retained.
- **`reading_date`****:** A valid calendar date written exactly as `YYYY-MM-DD`.
- **`energy_wh`****:** A nonnegative `Decimal` quantity expressed in Wh.
- **`source_file`****and** **`source_row`****:** The originating file and data-row index.

The accepted, enriched output adds `region`. Exception evidence also retains the original fields, so a reviewer can inspect the rejected date, blank amount, or unsupported unit.

Normalize `R1` in source row 1 by trimming the surrounding whitespace from its site identifier while preserving `001`. Convert the energy value using `Decimal('1.5') * 1000` to obtain `1500 Wh`. Source row 2 already records `1500 Wh`. Both rows have matching business fields: reading ID, site identifier, date, and normalized energy.

Convert `kWh` to `Wh` by multiplying by 1,000 because **1 kWh = 1,000 Wh**. `kW` measures power, so converting the value in source row 8 to `Wh` requires a duration. Reject source row 8 with the reason code `unsupported_unit`.

Apply the following validation rules to the remaining invalid records:

- **Source row 5:** Reject with `invalid_date`. The value `03/04/2026` is not ISO-formatted and has an ambiguous day-month order.
- **Source row 6:** Reject with `missing_amount`. Do not replace a missing energy value with zero.
- **Invalid amounts:** Reject nonnumeric, nonfinite, or negative energy values with a reason code identifying the validation failure.

Normalization applies defined transformations to source values. It does not justify inferring missing measurements or identifiers.

## Preventing join inflation[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Preventing-join-inflation)

**Join cardinality** describes how many rows on each side can match. A many-to-one enrichment requires each reading to match at most one eligible site row.

Before resolving the lookup, predict what happens to R2 in a raw join and what happens if duplicate site IDs are simply dropped.

What breaks when site-lookup safeguards are bypassed?

↓ Entry

📄Immutable site fixture

↓ Entry

⚡Normalized R2

🔑Unique eligible lookup

📋Conflict hold and evidence

🔗Many-to-one enrichment

📊Accepted-only regional totals

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

Reading `R2` normalizes to `2000 Wh`. Joining `R2` with both records for site `002` duplicates the measurement across West and East, inflating the total from `2000 Wh` to `4000 Wh`. Keeping only the first record for each site ID arbitrarily selects a region and hides the conflicting assignments.

Build a site-to-region lookup that separates valid mappings from conflicting assignments before enriching reading records:

- Map site `001` to North.
- Map site `003` to South.
- Mark site `002` as `conflict-held` and retain both source records for review.

Check that eligible keys are unique. Then R2 remains unresolved with `site_conflict`, while R3 remains unresolved with `site_absent`. R3 has a valid identifier, date, and quantity; syntactic validity cannot supply the missing site relationship. A similar site name would not establish identity either.

Handle repeated reading IDs separately. For equivalent normalized records, this example’s stable duplicate rule retains the lowest source-row index and links later equivalents to it. That choice selects provenance among equivalent values; it does not decide which conflicting measurement is authoritative. Different normalized values under one reading ID would be held as a reading conflict.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27925.09%27%20height=%27498.49%27/%3e)![All eight source readings remain accounted for, while only two accepted business records contribute to the partial-data regional totals](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "All eight source readings remain accounted for, while only two accepted business records contribute to the partial-data regional totals")

All eight source readings remain accounted for, while only two accepted business records contribute to the partial-data regional totals

## Accounting for every row[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Accounting-for-every-row)

A **disposition ledger** records exactly one processing outcome for each source row. Use the total number of source rows, including duplicates, as the denominator rather than the number of resulting business records.

The reading ledger accounts for all eight source rows:

1. `energy_readings.csv:1`, `R1`: **accepted**. Retained as the North reading.
2. `energy_readings.csv:2`, `R1`: **duplicate** (`equivalent_record`). The retained record is `energy_readings.csv:1`.
3. `energy_readings.csv:3`, `R2`: **unresolved** (`site_conflict`). Site `002`.
4. `energy_readings.csv:4`, `R3`: **unresolved** (`site_absent`). Site `009`.
5. `energy_readings.csv:5`, `R4`: **rejected** (`invalid_date`). Raw date: `03/04/2026`.
6. `energy_readings.csv:6`, `R5`: **rejected** (`missing_amount`). Raw amount is empty.
7. `energy_readings.csv:7`, `R6`: **accepted**. Retained as the South reading.
8. `energy_readings.csv:8`, `R7`: **rejected** (`unsupported_unit`). Raw unit: `kW`.

The site ledger separately accounts for all four source rows:

1. `sites.csv:1`, `001 / North`: **eligible**.
2. `sites.csv:2`, `002 / West`: **conflict-held** (`region_conflict`).
3. `sites.csv:3`, `002 / East`: **conflict-held** (`region_conflict`).
4. `sites.csv:4`, `003 / South`: **eligible**.

The canonical accepted dataset contains two records:

- `R1 / 001 / 2026-09-01 / 1500 Wh / North`, from reading row 1.
- `R6 / 003 / 2026-09-01 / 500 Wh / South`, from reading row 7.

Verify reading-row reconciliation: `8 = 2 accepted + 3 rejected + 2 unresolved + 1 duplicate`. Verify site-row reconciliation separately: `4 = 2 eligible + 2 conflict-held`.

The accepted readings total `1500 Wh` for North and `500 Wh` for South, giving an accepted-only total of `2000 Wh`. Mark the summary as `partial_data` and label `2000 Wh` as the total of accepted readings, excluding rejected, unresolved, and duplicate rows.

Do not use the two accepted records to claim complete source coverage. Reconcile coverage against all eight reading rows.

Include data-quality reports alongside the accepted output. Validation checks must identify rejected, unresolved, and duplicate records, even when processing completes successfully.

## Making reruns repeatable[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Making-reruns-repeatable)

Separate extraction, transformation and reconciliation, and loading into named responsibilities. This makes each stage inspectable and keeps output generation separate from decisions about records.

For this bounded local snapshot pipeline:

1. Extract immutable CSV inputs and verify required columns.
2. Profile them, normalize readings, resolve lookup eligibility, and classify every source row in memory.
3. Validate ledger accounting, eligible lookup uniqueness, and unique accepted reading IDs.
4. Write complete derived snapshots inside `energy_output`.

Appending accepted rows on every run would store two rows after the first run and four after the second. Replacing the derived snapshots leaves two. This design gives predictable reruns for a local snapshot; it makes no distributed exactly-once ingestion claim.

Create `energy_pipeline.py`, `sites.csv`, `energy_readings.csv`, `energy_rules.md`, and `test_energy_pipeline.py` in a new directory. Use an existing Python 3 installation; there are no third-party dependencies. In a terminal opened in that directory, run:

`python energy_pipeline.py --sites sites.csv --readings energy_readings.csv --output energy_output`

Use `python3` on macOS or Linux, or `py -3` on Windows, if that is the installed interpreter command.

Inspect the implementation, record your predictions in the blank prompts in `energy_rules.md`, and then optionally run the CLI and focused checks.

Files

energy\_pipeline.py

sites.csv

energy\_readings.csv

energy\_rules.md

test\_energy\_pipeline.py

markdown

```
import argparse, csv, json, sys, re

from collections import Counter, defaultdict

from datetime import date

from decimal import Decimal, InvalidOperation, localcontext

from pathlib import Path

SITE = ['site_id', 'region']

READ = ['reading_id', 'site_id', 'reading_date', 'amount', 'unit']

CANON = ['reading_id', 'site_id', 'reading_date', 'energy_wh', 'region', 'source_file', 'source_row']

def require(ok, message):

if not ok: raise ValueError(message)

def extract_csv(path, columns):

path = Path(path)

with path.open(encoding='utf-8', newline='') as f:

reader = csv.reader(f, strict=True)

header = next(reader, [])

require(len(header) == len(set(header)) and set(columns) <= set(header), f'{path}: missing or duplicate columns')

rows = []

for n, values in enumerate(reader, 1):

require(len(values) == len(header), f'{path}: malformed data row {n}')

require(not {'source_file', 'source_row'} & set(header), 'reserved provenance columns')

rows.append(dict(zip(header, values), source_file=path.name, source_row=n))

return rows

def decimal_text(value):

text = format(value, 'f')

return (text.rstrip('0').rstrip('.') if '.' in text else text) if value else '0'

def normalize_reading(raw):

r = {k: raw[k].strip() for k in ['reading_id', 'site_id']}

if not all(r.values()): raise ValueError('missing_id')

d = raw['reading_date']

if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d): raise ValueError('invalid_date')

try: date.fromisoformat(d)

except ValueError: raise ValueError('invalid_date')

if not raw['amount'].strip(): raise ValueError('missing_amount')

try: amount = Decimal(raw['amount'])

except InvalidOperation: raise ValueError('invalid_amount')

if not amount.is_finite(): raise ValueError('nonfinite_amount')

if amount < 0: raise ValueError('negative_amount')

if raw['unit'] not in ('Wh', 'kWh'): raise ValueError('unsupported_unit')

with localcontext() as ctx:

ctx.prec = max(28, len(amount.as_tuple().digits) + 4)

energy = amount * (1000 if raw['unit'] == 'kWh' else 1)

return dict(r, reading_date=d, energy_wh=decimal_text(energy))

def profile_inputs(sites, readings):

result = {}

for name, rows, columns, identity in [('sites', sites, SITE, 'site_id'), ('readings', readings, READ, 'reading_id')]:

result[name] = {'count': len(rows), 'missingness': {k: sum(not r[k].strip() for r in rows) for k in columns}, 'raw_distributions': {k: dict(sorted(Counter(r[k] for r in rows).items())) for k in columns}, 'identifier_multiplicity': dict(sorted(Counter(r[identity].strip() for r in rows).items())), 'rows': rows}

result['normalized_site_references'] = dict(sorted(Counter(r['site_id'].strip() for r in readings).items()))

result['offending_readings'] = []

for r in readings:

try: normalize_reading(r)

except ValueError as e: result['offending_readings'].append({'reason': str(e), 'raw': r})

return result

def reconcile_sites(rows):

groups, lookup, ledger, conflicts = defaultdict(list), {}, [], []

for r in rows: groups[r['site_id'].strip()].append(r)

for key, group in sorted(groups.items()):

conflict = len({r['region'] for r in group}) > 1

valid = bool(key) and all(r['region'] for r in group)

if valid and not conflict: lookup[key] = group[0]['region']

for r in group:

entry = dict(r, normalized_site_id=key, disposition='conflict-held' if conflict else ('eligible' if valid else 'rejected'), reason='region_conflict' if conflict else ('eligible' if valid else 'missing_site_field'))

ledger.append(entry)

if conflict: conflicts.append(entry)

return lookup, sorted(ledger, key=lambda r: r['source_row']), sorted(conflicts, key=lambda r: r['source_row'])

def business(r):

return tuple(r[k] for k in ['site_id', 'reading_date', 'energy_wh'])

def transform_readings(rows, lookup, site_ledger):

ledger, groups, canonical = [], defaultdict(list), []

held = {r['normalized_site_id'] for r in site_ledger if r['disposition'] == 'conflict-held'}

for raw in rows:

entry = {'source_file': raw['source_file'], 'source_row': raw['source_row'], 'raw': raw, 'retained_source_file': '', 'retained_source_row': ''}

ledger.append(entry)

try: entry['normalized'] = normalize_reading(raw)

except ValueError as e: entry.update(disposition='rejected', reason=str(e)); continue

groups[entry['normalized']['reading_id']].append(entry)

for group in groups.values():

group.sort(key=lambda r: r['source_row'])

if len({business(r['normalized']) for r in group}) > 1:

for r in group: r.update(disposition='unresolved', reason='reading_conflict')

continue

first = group[0]

for r in group[1:]: r.update(disposition='duplicate', reason='equivalent_record', retained_source_file=first['source_file'], retained_source_row=first['source_row'])

n = first['normalized']; key = n['site_id']

if key not in lookup: first.update(disposition='unresolved', reason='site_conflict' if key in held else 'site_absent')

else:

first.update(disposition='accepted', reason='accepted')

canonical.append(dict(n, region=lookup[key], source_file=first['source_file'], source_row=first['source_row']))

return sorted(canonical, key=lambda r: r['reading_id']), ledger

def validate_results(readings, sites, canonical, ledger, site_ledger, lookup):

identity = lambda r: (r['source_file'], r['source_row'])

for source, evidence in [(readings, ledger), (sites, site_ledger)]:

require(Counter(map(identity, source)) == Counter(map(identity, evidence)) and len(set(map(identity, evidence))) == len(evidence), 'source coverage is not exhaustive and disjoint')

require(all(r['disposition'] in {'accepted', 'duplicate', 'unresolved', 'rejected'} for r in ledger), 'unknown disposition')

require(all(r['disposition'] in {'eligible', 'conflict-held', 'rejected'} for r in site_ledger), 'unknown site disposition')

eligible = defaultdict(set)

for r in site_ledger:

if r['disposition'] == 'eligible': eligible[r['normalized_site_id']].add(r['region'])

require(all(len(v) == 1 for v in eligible.values()) and lookup == {k: next(iter(v)) for k, v in eligible.items()}, 'lookup not unique')

index = {identity(r): r for r in ledger}

for r in ledger:

if r['disposition'] == 'duplicate':

target = index.get((r['retained_source_file'], r['retained_source_row']))

require(target is not None and target['source_row'] < r['source_row'] and target['disposition'] in {'accepted', 'unresolved'} and target['normalized'] == r['normalized'] and r['reason'] == 'equivalent_record', 'bad duplicate link')

require(len({r['reading_id'] for r in canonical}) == len(canonical), 'duplicate accepted ID')

expected = [dict(r['normalized'], region=lookup[r['normalized']['site_id']], source_file=r['source_file'], source_row=r['source_row']) for r in ledger if r['disposition'] == 'accepted']

require(sorted(expected, key=identity) == sorted(canonical, key=identity), 'canonical correspondence failed')

def summarize(canonical, ledger, site_ledger):

totals = defaultdict(Decimal)

with localcontext() as ctx:

ctx.prec = max([28] + [len(r['energy_wh']) + 10 for r in canonical])

for r in canonical: totals[r['region']] += Decimal(r['energy_wh'])

grand = sum(totals.values(), Decimal(0))

counts = {k: sum(r['disposition'] == k for r in ledger) for k in ['accepted', 'rejected', 'unresolved', 'duplicate']}

site_counts = dict(sorted(Counter(r['disposition'] for r in site_ledger).items()))

return {'status': 'partial_data' if counts['rejected'] or counts['unresolved'] or site_counts.get('conflict-held') else 'complete_data', 'reading_counts': counts, 'site_counts': site_counts, 'accepted_only_regional_wh': {k: decimal_text(v) for k, v in sorted(totals.items())}, 'accepted_only_grand_wh': decimal_text(grand)}

def write_outputs(output, canonical, ledger, site_ledger, conflicts, profile, summary):

output = Path(output); output.mkdir(parents=True, exist_ok=True)

def table(name, rows, fields):

mode = 'w'  # Optional mutation: use 'a' only for canonical_readings.csv.

with (output / name).open(mode, encoding='utf-8', newline='') as f:

writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()

for r in rows: writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, dict) else v for k, v in r.items()})

table('canonical_readings.csv', canonical, CANON)

table('reading_ledger.csv', ledger, ['source_file', 'source_row', 'raw', 'retained_source_file', 'retained_source_row', 'normalized', 'disposition', 'reason'])

fields = SITE + ['source_file', 'source_row', 'normalized_site_id', 'disposition', 'reason']

table('site_ledger.csv', site_ledger, fields)

table('site_conflicts.csv', conflicts, fields)

for name, value in [('profile.json', profile), ('summary.json', summary)]:

(output / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def main(argv=None):

parser = argparse.ArgumentParser()

parser.add_argument('--sites', default='sites.csv'); parser.add_argument('--readings', default='energy_readings.csv'); parser.add_argument('--output', default='energy_output')

args = parser.parse_args(argv)

try:

sites = extract_csv(args.sites, SITE); readings = extract_csv(args.readings, READ)

profile = profile_inputs(sites, readings)

lookup, site_ledger, conflicts = reconcile_sites(sites)

canonical, ledger = transform_readings(readings, lookup, site_ledger)

validate_results(readings, sites, canonical, ledger, site_ledger, lookup)

summary = summarize(canonical, ledger, site_ledger)

write_outputs(args.output, canonical, ledger, site_ledger, conflicts, profile, summary)

except (OSError, UnicodeError, csv.Error, ValueError, ArithmeticError) as e:

print(f'ERROR: {e}. No fresh valid snapshot claimed; any prior output directory is an earlier snapshot (a failed write may leave incomplete files).', file=sys.stderr)

return 1

print('Completed: accepted readings only; ' + json.dumps(summary, sort_keys=True))

return 0

if __name__ == '__main__':

sys.exit(main())
```

⋯

Inspect first, record predictions in energy\_rules.md, then optionally run the CLI and unittest checks. Reference results are expected, not observed. CSV and Markdown tabs are data/documentation, not Python programs.

In `energy_pipeline.py`:

- **Lines 14–25:** Strict CSV reading separates unusable files from row-level problems; IDs stay strings.
- **Lines 31–47:** Each bad value (date, amount, unit) gets a specific rejection reason instead of a guessed fix.
- **Lines 60–71:** Conflicting site regions never enter the lookup; both rows stay visible as conflicts.
- **Lines 76–126:** Every source row gets exactly one outcome, and totals use accepted rows only, labeled partial\_data.
- **Lines 128–141:** Outputs are overwritten each run, so a second run produces identical files.
- **Lines 143–162:** The command runs each step in order and exits with an error instead of writing a fake result when input is unusable.

**In** **`test_energy_pipeline.py`****:**

- The tests check the exact ledger and totals, that a second run is byte-identical, and that bad input fails visibly without creating output.

In the fixture and rules files:

- **`sites.csv`** **(lines 1–5):** Supply the lookup header and four source records, including both incompatible site-002 regions. Neither region receives authority from its position.
- **`energy_readings.csv`** **(lines 1–9):** Supply the reading header and eight source records. Preserve the whitespace and blank amount to test the actual contract decisions.
- **`energy_rules.md`** **(lines 1–10):** Provide blank prediction prompts. Write your explanations here before optional execution; this is a Markdown document, not a Python program.
- **`energy_rules.md`** **(lines 12–16):** Give CLI and unittest commands and label reference results as expected, not observed.
- **`energy_rules.md`** **(lines 18–36):** Document the contract, rejection reasons, provenance, lookup conflicts, and duplicate precedence. Equivalent duplicates may point to an unresolved representative.
- **`energy_rules.md`** **(lines 38–57):** Record expected canonical rows, both ledgers, accounting, totals, and failure semantics. Failed writes do not promise atomic publication.
- **`energy_rules.md`** **(lines 59–64):** Specify a six-file byte comparison and an optional append mutation. If trying the mutation, predict the failed check before consulting the suggested edit.

The key boundary is between evidence and usable records: normalization can reduce business-record count without reducing the source-row ledger.

Expected behavior, not an execution claim: Unchanged inputs produce the same two canonical rows, eight reading dispositions, four site dispositions, and `2000 Wh` accepted-only total on both runs. The focused rerun check compares file contents, not merely whether both commands exited successfully.

Unreadable input or missing required columns must print a visible error and exit nonzero. Row-level exceptions allow a report to be generated, but its summary must say `partial_data`. These are different outcomes: An unusable input file prevents the run; an invalid measurement remains visible within a completed partial-data run.

## Which rules transfer to the stock export?[#](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Which-rules-transfer-to-the-stock-export)

Consider the following independent stock-reconciliation brief. The product lookup contains `A01 / Tools`, `A01 / Parts`, and `B02 / Supplies`. The two `A01` records have conflicting classifications, and neither takes precedence.

The stock input contains the columns `record_id`, `sku`, `quantity`, and `unit`, with the following five rows:

1. `S1,B02,2,case`
2. `S1,B02,24,each`
3. `S2,A01,3,each`
4. `S3,C03,4,each`
5. `S4,B02,,each`

The contract treats identifiers as case-sensitive strings. For SKU `B02`, one `case` equals 12 `each`. Empty quantities are invalid, and repeated record IDs with equivalent values are duplicates. The contract does not authorize changing identifier case or applying `B02`'s case conversion to other products.

Before reviewing the proposed solution, independently draft a concise reconciliation specification in a separate note. Document the data profile, canonical schema, conversion rules, row-level dispositions and reason codes, accepted output with source provenance, separate lookup-row reconciliation, and safeguards against one-to-many joins. Define a second-run acceptance check that verifies these results and reports source coverage.

Next, review the proposed specification in the memo activity. Identify unsupported assumptions and explain how to correct them before viewing the feedback. Compare the feedback with your independent specification rather than using it to construct your initial answer.

Stock Reconciliation Specification Review

Your task

You are responsible for a stock-reconciliation specification for the independent stock export. The team needs trustworthy accepted stock and visible evidence for every source row, including a repeat-run acceptance check. Review the proposed rules against the supplied fixture and contract.

Tap any claim to classify it, and click on References to verify authorities.

TOStock export teamFROMReconciliation reviewerDATEOctober 19, 2026SUBJECTStock reconciliation rules and acceptance evidence

Background

This specification concerns only the independent stock fixture and its supplied contract. The facilities-export conversion and identifier rules do not automatically apply.

Issue

The specification must profile both inputs, define canonical fields, assign every stock source row a disposition and reason, identify accepted output with provenance, protect lookup cardinality, account for lookup rows separately, and define observable repeat-run evidence and coverage labeling.

Analysis

The facilities example permits identifier normalization. Citing that permission, this stock pipeline should uppercase record IDs and SKUs before checking identity.

An additional product-resolution authority permits the first listed category to win when lookup rows disagree and defines every product case as twelve each. Apply those rules before enrichment.

A repeat run that exits successfully proves complete coverage and repeatability. Appending accepted records to the existing output is therefore sufficient; excluded rows need not appear in a separate artifact.

Conclusion

A trustworthy specification needs explicit source-contract authority and row-level evidence. Accepted business records and source-row coverage are different measures.

Recommendation

Require a complete profile, canonical schema, source-row ledger, accepted output with provenance, eligible-lookup uniqueness validation, separate lookup accounting, and a concrete two-run snapshot comparison before approving implementation.

Do you find this helpful?

String identifiers, provenance, uniqueness checks, row accounting, and snapshot reruns transfer because they protect the data path. Unit conversions and identifier normalization must come from the new contract. For your own submission, make those contract-dependent rules inspectable before trusting its clean-looking output.

Choosing a Stack and Project Structure

Integrating Third-Party APIs

Ask

[Why totals go wrong](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Why-totals-go-wrong)

[Profiling the source data](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Profiling-the-source-data)

[Normalizing without inventing data](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Normalizing-without-inventing-data)

[Preventing join inflation](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Preventing-join-inflation)

[Accounting for every row](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Accounting-for-every-row)

[Making reruns repeatable](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Making-reruns-repeatable)

[Which rules transfer to the stock export?](https://www.educative.io/courses/forward-deployed-engineer/working-with-messy-data#Which-rules-transfer-to-the-stock-export)