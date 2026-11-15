# Coding_Round_Strategies_for_User_Needs_and_Changing_Requirements

Source: https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Coding Round: User Needs and Changing Requirements

Build a function that matches users based on shared interests while adapting to changing requirements. Define a clear user result, establish a working baseline, and incorporate updates without breaking existing functionality. Normalize user identities, handle duplicate profiles, and optimize searches using an inverted index where appropriate. Ensure data consistency, query efficiency, and reliable results as the system scales, applying sound system design principles throughout implementation.

We'll cover the following...

- [A method for changing requirements](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#A-method-for-changing-requirements)
- [Agree on the baseline contract](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Agree-on-the-baseline-contract)
- [The baseline: A short scan](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#The-baseline-A-short-scan)
  - [Change 1: Profiles can be replaced](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-1-Profiles-can-be-replaced)
  - [Change 2: Ranking by shared interests](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-2-Ranking-by-shared-interests)
  - [Change 3: Faster repeated searches](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-3-Faster-repeated-searches)
  - [Keeping the index correct](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Keeping-the-index-correct)
  - [Practice: Maintain the index](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Practice-Maintain-the-index)
  - [Common follow-ups](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Common-follow-ups)

“I want to find other people who share my interests.” That request gives the coding task a clear result: someone receives a list of relevant people they can contact.

The coding gets harder when profiles change, relevance gains a ranking rule, or repeated searches need to be faster. A strong answer makes each change explicit, so that improving one behavior doesn’t quietly break another.

## A method for changing requirements[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#A-method-for-changing-requirements)

1. Name the useful result for the user.
2. Settle only the uncertainties that change the implementation.
3. Build and verify a working baseline.
4. For each follow-up, name what changed, keep the remaining promises, and choose the smallest adaptation that works.

Adaptability means changing the code to fit a new contract while showing which promises still hold. Building caches and abstractions in advance for follow-ups that may never come usually delays the first useful result.

Public preparation guides describe coding tasks framed around an end-user system, and recommend a working baseline before caching or pre-computation. One secondary compilation mentions an FDSE prompt about an app connecting people with similar interests. Only that premise comes from the report. The records and follow-ups below are an invented practice exercise.

The deliverable is an in-memory matching function. A UI or social-network architecture would add work without answering the coding request.

## Agree on the baseline contract[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Agree-on-the-baseline-contract)

- **Identity:** Each profile has a unique string ID. Names don’t identify people.
- **Normalization:** Apply `strip()` then `casefold()`, drop blank labels, and count each label once.
- **Duplicates:** A repeated profile ID at construction raises `ValueError`.
- **Output:** `matches(user_id)` returns other IDs that share at least one interest, in ascending ID order, excluding the requester.
- **Boundaries:** A known profile with no interests returns `[]`. An unknown ID raises `KeyError`.
- **Mutation:** The caller’s input is never changed.

Practice records:

Ace Editor

1

2

3

4

5

A: [' Art ', 'HIKING', 'art']

B: ['chess', 'hiking']

C: ['art']

D: ['chess']

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A normalizes to `{art, hiking}`. The repeated `art` adds nothing.

Identity and query boundaries

1.

Keep B, C, and D from the original fixture, but supply A as two initial rows: (‘A’, [‘art’]) and (‘A’, [‘hiking’]). What must the constructor do?

A.

Treat the two A rows as separate people.

B.

Union the interests, leaving A with art and hiking.

C.

Raise ValueError.

D.

Keep the last A row, leaving A with only hiking.

---

1 / 2

Rejecting duplicate IDs at construction stops input order from deciding which version of a profile survives. Keep that rule even after an update method is added later.

## The baseline: A short scan[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#The-baseline-A-short-scan)

C++

```
def normalize(labels):

return {tag for label in labels if (tag := label.strip().casefold())}

class ScanMatches:

def __init__(self, rows):

self.profiles = {}

for user_id, labels in rows:

if user_id in self.profiles:

raise ValueError(f"duplicate user ID: {user_id}")

self.profiles[user_id] = normalize(labels)

def matches(self, user_id):

interests = self.profiles[user_id]

found = []

for other_id, other_interests in self.profiles.items():

if other_id != user_id and interests & other_interests:

found.append(other_id)

return sorted(found)
```

⋯

Baseline scan with checks for every contract rule

- **Line 2:** Builds a fresh set of cleaned, non-blank labels. The caller’s list isn’t touched.
- **Lines 8–11:** Each ID is stored once, and a duplicate is rejected before it can overwrite anything.
- **Line 14:** Looking up an unknown ID raises `KeyError` naturally.
- **Line 17:** Excludes the requester and keeps anyone with a shared interest.
- **Line 19:** Sorting makes the result independent of input order.

For A, B shares `hiking`, C shares `art`, and D shares nothing, so the result is `["B", "C"]`.

### Change 1: Profiles can be replaced[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-1-Profiles-can-be-replaced)

The interviewer adds `upsert(user_id, interests)`. Clarify the rules: it creates a missing profile or **fully replaces** an existing one, it takes effect before the next query, and an empty list clears interests but keeps the identity.

Only mutability changes. The profile map already holds one current set per ID, so the change is one line:

Ace Editor

1

2

def upsert(self, user\_id, labels):

self.profiles[user\_id] = normalize(labels)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

After `upsert("B", ["chess"])`, B no longer has `hiking`, so A matches only C: `["C"]`.

Two tempting versions are wrong:

- Appending a second B row breaks “one current profile per ID”.
- Merging `{chess}` into B’s old set keeps `hiking`, so A still sees B.

### Change 2: Ranking by shared interests[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-2-Ranking-by-shared-interests)

New rules: score each match by the number of **distinct** shared interests, still exclude zero scores, and sort by descending score, then ascending ID.

Now replace C’s interests with `["art", "hiking"]`:

|  |  |  |  |
| --- | --- | --- | --- |
|  | **Shares with A** | **Score** | **Position** |
| C | art, hiking | 2 | 1st |
| B | hiking | 1 | 2nd |

The new answer is `["C", "B"]`. This change retires one old check, “results are in ascending ID order”, and only for the ranked version. Identity, normalization, self-exclusion, unknown-ID behavior and input preservation all stay.

The score is `len(interests & other_interests)`. Counting raw labels is a trap: A’s input lists `art` twice, but after normalization it counts once.

### Change 3: Faster repeated searches[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-3-Faster-repeated-searches)

Before optimizing, ask how many profiles there are, how many interests each has, how often queries and updates happen, and what response time is required. Nothing in the interview setting implies a scale.

For many repeated searches over profiles that rarely change, an **inverted index** maps each interest to the IDs that hold it. A query visits only the posting lists for its own interests. For a small or frequently updated collection, keep the scan: it is simpler, and replacements already work.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27680.5%27%20height=%27271%27/%3e)![Scanning every profile versus an indexed query pipeline compared](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Scanning every profile versus an indexed query pipeline compared")

Scanning every profile versus an indexed query pipeline compared

The two paths cost different amounts:

- **Scan:** visits every profile, keeps eligible IDs, then sorts them. That is about `O(N + M log M)` plus the set-intersection work, for `N` profiles and `M` matches.
- **Indexed query:** for `U` query interests, `P` visited postings and `C` distinct candidates, a query costs about `O(U + P + C log C)`.

If one interest is held by almost everyone, `P` approaches `N` and the index is no faster than the scan. Don’t claim constant-time search.

### Keeping the index correct[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Keeping-the-index-correct)

The index is a second copy of the same facts, so it needs an invariant:

> For every ID `v` and interest `t`: `v` is in `by_interest[t]` if and only if `t` is in `profiles[v]`.

Trace `upsert("B", ["chess"])`:

|  |  |  |  |
| --- | --- | --- | --- |
| **Posting** | **Before** | **After Correct Update** | **After Add-Only Update** |
| art | {A, C} | {A, C} | {A, C} |
| hiking | {A, B} | **{A}** | {A, B} ← stale |
| chess | {B, D} | {B, D} | {B, D} |

With the stale `hiking` entry, the indexed query for A wrongly returns `["B", "C"]`, while the scan correctly returns `["C"]`. Filtering B out of that one result would hide the symptom and leave the index wrong for every other query.

**Correct update:** normalize first, remove `old − new`, add `new − old`, delete empty posting lists, then store the new profile. Repeating the same update changes nothing.

### Practice: Maintain the index[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Practice-Maintain-the-index)

The starter gives you a ranked scan to act as the reference (the **oracle**), and an index with working construction and queries. Only `upsert` is missing. Every step checks Q’s results and the index invariant together.

Records: `Q: [maps, cycling]`, `R: [maps, maps]`, `S: [cycling, maps]`, `T: [music]`.

Predict first: Q’s initial ranked matches are `["S", "R"]`, since S shares two interests and R one. Then predict each step in the checklist before running.

Python 3.14.0

```
from collections import Counter

def normalize(labels):

return {tag for label in labels if (tag := label.strip().casefold())}

class RankedScan:

"""Reference implementation: replacement upsert, ranked by shared interests."""

def __init__(self, rows):

self.profiles = {}

for user_id, labels in rows:

if user_id in self.profiles:

raise ValueError(f"duplicate user ID: {user_id}")

self.profiles[user_id] = normalize(labels)

def upsert(self, user_id, labels):

self.profiles[user_id] = normalize(labels)

def matches(self, user_id):

interests = self.profiles[user_id]

scores = {v: len(interests & s) for v, s in self.profiles.items() if v != user_id}

return sorted((v for v, n in scores.items() if n > 0), key=lambda v: (-scores[v], v))

class IndexedMatches(RankedScan):

def __init__(self, rows):

super().__init__(rows)

self.by_interest = {}

for user_id, interests in self.profiles.items():

for tag in interests:

self.by_interest.setdefault(tag, set()).add(user_id)

def upsert(self, user_id, labels):

pass  # TODO: normalize, remove old - new, add new - old, drop empty lists, store profile

def matches(self, user_id):

scores = Counter()

for tag in self.profiles[user_id]:

for candidate in self.by_interest[tag]:

if candidate != user_id:

scores[candidate] += 1

return sorted(scores, key=lambda v: (-scores[v], v))

def is_consistent(self):

expected = {}

for user_id, interests in self.profiles.items():

for tag in interests:

expected.setdefault(tag, set()).add(user_id)

return self.by_interest == expected

def check(name, got, expected):

ok = got == expected

print("PASS" if ok else "FAIL", "-", name)

if not ok:

print("  got:", got)

print("  expected:", expected)

ROWS = [("Q", ["maps", "cycling"]), ("R", ["maps", "maps"]),

("S", ["cycling", "maps"]), ("T", ["music"])]

scan, indexed = RankedScan(ROWS), IndexedMatches(ROWS)

check("initial index (given)", (indexed.matches("Q"), indexed.is_consistent()), (["S", "R"], True))

for user_id, labels, expected in [

("S", ["cycling"], ["R", "S"]),

("R", [], ["S"]),

("T", ["Maps "], ["S", "T"]),

("T", ["Maps "], ["S", "T"]),

]:

scan.upsert(user_id, labels)

indexed.upsert(user_id, labels)

check(f"upsert {user_id} {labels}", (indexed.matches("Q"), indexed.is_consistent()), (expected, True))
```

⋯

Maintain the index so it always matches profiles.

In the solution:

- **Lines 17–18:** The reference `upsert` replaces the whole set. It never merges.
- **Lines 22–23:** The score is the size of the intersection, so each shared interest counts once. Ties are broken by ID.
- **Lines 34–35:** Normalize the new labels *before* changing anything, and treat a new ID as having no old interests.
- **Lines 37–41:** Remove the ID from interests it no longer has, and delete posting lists that become empty.
- **Lines 42–43:** Add the ID to its new interests, then store the replacement profile.

The last two steps apply the same update twice and expect the same result, which checks that a repeated update is harmless. These checks cover the listed cases. They don’t prove correctness for every sequence or guarantee real latency. This code is single-threaded and assumes callers use its methods rather than editing the dictionaries directly.

### Common follow-ups[#](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Common-follow-ups)

Interviewers often probe a coding answer with follow-ups like these.

1.

Why didn’t you build the index from the start?

Show Answer

1 / 5

Once this feature reads external data or serves many users, the questions grow: what must the surrounding system guarantee so that its answers stay current, reliable, and authorized? That is the territory of system design.

The Re-Engineering Round: Debugging and Verifying Fixes

FDE System Design: Pipelines, Reliability, and Access Control

Ask

[A method for changing requirements](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#A-method-for-changing-requirements)

[Agree on the baseline contract](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Agree-on-the-baseline-contract)

[The baseline: A short scan](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#The-baseline-A-short-scan)

[Change 1: Profiles can be replaced](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-1-Profiles-can-be-replaced)

[Change 2: Ranking by shared interests](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-2-Ranking-by-shared-interests)

[Change 3: Faster repeated searches](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Change-3-Faster-repeated-searches)

[Keeping the index correct](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Keeping-the-index-correct)

[Practice: Maintain the index](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Practice-Maintain-the-index)

[Common follow-ups](https://www.educative.io/courses/forward-deployed-engineer/the-coding-round-user-needs-and-changing-requirements#Common-follow-ups)