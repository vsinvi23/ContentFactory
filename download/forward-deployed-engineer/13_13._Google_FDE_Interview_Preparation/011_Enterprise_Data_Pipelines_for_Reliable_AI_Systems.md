# Enterprise_Data_Pipelines_for_Reliable_AI_Systems

Source: https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Enterprise Data Pipelines

Explore the common data-readiness problems that stall enterprise AI projects, including fragmented sources, stale content, and unclear ownership. Learn to profile data during discovery, start with a narrow data domain, and build pipelines with built-in quality checks.

We'll cover the following...

- [Common data-readiness problems](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-readiness-problems)
- [Assessing data readiness](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Assessing-data-readiness)
- [Why to start with a narrow data domain](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Why-to-start-with-a-narrow-data-domain)
- [Building the pipeline](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Building-the-pipeline)
- [Common data pipeline mistakes](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-pipeline-mistakes)

Every enterprise AI system depends on data, and in most customer deployments the data is not ready when the project begins. A customer may describe their support knowledge base as “all in one place,” only for the FDE team to discover during discovery that it spans three ticketing systems, a shared drive of outdated PDFs, and a wiki that no one has maintained in two years. The model and agent design may be sound, but if the data feeding them is incomplete, inconsistent, or stale, the system’s answers will be too.

Data readiness is one of the most common reasons AI pilots stall, and it is frequently underestimated in project plans. FDE interviewers raise it often, either directly or as a follow-up in a system design scenario. They want to see whether a candidate identifies data problems early, scopes around them realistically, and designs pipelines that keep data reliable after launch rather than only during a demonstration.

## Common data-readiness problems[#](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-readiness-problems)

Data problems in enterprise environments tend to follow recognizable patterns. Identifying them during discovery, before architecture decisions are made, saves significant rework later.

|  |  |
| --- | --- |
| Problem | What it looks like in practice |
| Fragmented sources | The same information lives in several systems with no single source of truth |
| Poor quality | Duplicate records, missing fields, free-text values where structured data was expected |
| Stale or conflicting content | Old document versions sit alongside current ones, with no clear indication of which is valid |
| Unclear ownership | No team is responsible for keeping a dataset accurate or approving its use |
| Inconsistent definitions | Departments calculate the same metric differently |
| Difficult formats | Scanned PDFs, images of forms, and complex tables that standard parsers handle poorly |
| Access and compliance barriers | Data contains personal or regulated information that requires approvals before use |

Some of these problems are technical, such as parsing scanned documents. Many are organizational, such as unclear ownership and pending access approvals. Organizational problems often take longer to resolve, because they depend on people and processes outside the FDE team’s control. A realistic project plan accounts for both.

## Assessing data readiness[#](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Assessing-data-readiness)

A short, structured assessment during discovery turns vague concerns into specific findings the customer can act on. The FDE team reviews each candidate data source against a consistent set of questions.

|  |  |
| --- | --- |
| **Question** | **Assessment** |
| Where does the data live, and how is it accessed? | Determines integration effort and required permissions |
| Who owns it? | Identifies who approves use and who fixes quality issues |
| How current is it, and how often does it change? | Sets freshness requirements for the pipeline |
| How complete and consistent is it? | Reveals cleanup work before the data is usable |
| Does it contain sensitive or regulated information? | Triggers compliance review and masking requirements |
| Are there conflicting versions? | Determines whether deduplication or version control is needed |

Profiling the data directly is more reliable than relying on descriptions from the customer. The following BigQuery query profiles a support ticket table that a customer plans to use as a knowledge source.

Ace Editor

1

2

3

4

5

6

7

8

9

SELECT

COUNT(\*) AS total\_rows,

COUNT(DISTINCT ticket\_id) AS unique\_tickets,

COUNTIF(resolution\_text IS NULL OR resolution\_text = "") AS missing\_resolutions,

COUNTIF(category IS NULL) AS missing\_categories,

MAX(updated\_at) AS latest\_update,

TIMESTAMP\_DIFF(CURRENT\_TIMESTAMP(), MAX(updated\_at), HOUR) AS hours\_since\_update

FROM `PROJECT\_ID.support.tickets`

WHERE created\_at >= TIMESTAMP\_SUB(CURRENT\_TIMESTAMP(), INTERVAL 90 DAY);

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 2:** `total_rows` gives the overall size of the dataset in the period being assessed.
- **Line 3:** Comparing `unique_tickets` to `total_rows` reveals duplicate records.
- **Line 4:** `missing_resolutions` counts tickets with no resolution text. These tickets cannot teach an agent how a problem was solved.
- **Line 5:** `missing_categories` shows how much of the data lacks the labels needed for routing or filtering.
- **Lines 6–7:** `latest_update` and `hours_since_update` show whether the data is being refreshed as expected.
- **Line 9:** The query limits the assessment to the last 90 days, which keeps it inexpensive and focused on recent, relevant data.

Results like these give the customer concrete facts, such as “12 percent of resolved tickets have no resolution text,” rather than a general warning that the data needs work.

## Why to start with a narrow data domain[#](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Why-to-start-with-a-narrow-data-domain)

Faced with fragmented data, customers often want the first release to cover everything: all products, all regions, and all document sources. This approach almost always delays delivery, because every additional source brings its own access approvals, quality issues, and owners.

A stronger approach is to start with a narrow data domain: one well-defined area where the data is reasonably clean, has a clear owner, and supports a valuable use case. Examples include billing questions for a single product line, HR policies for one country, or support tickets from the last six months for one category.

A narrow domain offers several advantages. It reduces the number of approvals and owners involved, so the team can reach production sooner. It makes data cleanup manageable, since the team fixes a small, specific set of problems rather than every problem at once. It makes evaluation practical, because a focused set of test questions can cover the domain thoroughly. It also builds trust: a system that answers billing questions accurately earns support for expanding to other domains, while a system that answers everything poorly can end the project.

In an interview, choosing the first domain based on data readiness as well as business value is a strong signal. A high-value domain with unusable data is often a worse first choice than a moderately valuable domain with clean, well-owned data.

## Building the pipeline[#](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Building-the-pipeline)

Once the domain is chosen, the pipeline moves data from its sources into a form the AI system can use, and keeps it current. Google Cloud provides services for each stage.

|  |  |  |
| --- | --- | --- |
| **Service** | **Function** | **Services** |
| Ingest | Bring data in from source systems | Data stream for change data capture, Pub/Sub, BigQuery Data Transfer Service, Storage Transfer Service |
| Process | Clean, deduplicate, and transform data | Dataflow, BigQuery SQL, Dataform |
| Parse unstructured content | Extract text, tables, and fields from documents | Document AI |
| Protect | Find and mask sensitive information | Sensitive Data Protection |
| Govern | Catalog data, track lineage, and monitor quality | Dataplex |
| Serve | Store data in the form the AI system consumes | BigQuery, AlloyDB, search indexes, vector stores |

Freshness requirements shape the ingestion design. A product catalog that changes weekly can be loaded in a scheduled batch, while account balances or network outage status may need near-real-time updates through change data capture or streaming. Matching the pipeline to the actual freshness need avoids both stale answers and unnecessary complexity.

A pipeline should also check data quality before updating what the AI system uses. If a source system fails and sends incomplete data, the pipeline should stop rather than replace good data with bad. The following function applies quality thresholds to the profile query results.

Python 3.14.0

```
from google.cloud import bigquery

THRESHOLDS = {

"max_duplicate_rate": 0.01,

"max_missing_resolution_rate": 0.05,

"max_hours_since_update": 24,

}

def check_ticket_readiness(client: bigquery.Client) -> list[str]:

row = list(client.query(PROFILE_SQL).result())[0]

if row.total_rows == 0:

return ["No tickets found in the last 90 days."]

issues = []

duplicate_rate = 1 - row.unique_tickets / row.total_rows

if duplicate_rate > THRESHOLDS["max_duplicate_rate"]:

issues.append(f"Duplicate rate {duplicate_rate:.1%} exceeds the limit.")

missing_rate = row.missing_resolutions / row.total_rows

if missing_rate > THRESHOLDS["max_missing_resolution_rate"]:

issues.append(f"Missing resolutions at {missing_rate:.1%} exceed the limit.")

if row.hours_since_update > THRESHOLDS["max_hours_since_update"]:

issues.append(f"Data is {row.hours_since_update} hours old.")

return issues

from types import SimpleNamespace

PROFILE_SQL = "SELECT ..."

class SampleClient:

def query(self, sql):

row = SimpleNamespace(

total_rows=10_000,

unique_tickets=9_700,

missing_resolutions=1_200,

hours_since_update=36,

)

return SimpleNamespace(result=lambda: [row])

issues = check_ticket_readiness(SampleClient())

print("\n".join(issues) if issues else "Data is ready.")
```

⋯

- **Lines 3–7:** The thresholds are defined together as agreed quality standards, which makes them easy to review with the data owner.
- **Line 10:** We run the profile query from the previous section, stored here in `PROFILE_SQL`, and read its single result row.
- **Lines 11–12:** An empty dataset usually signals a broken source, so the check fails immediately instead of dividing by zero.
- **Lines 15–17:** The duplicate rate compares unique tickets with total rows and flags the data if duplicates exceed 1 percent.
- **Lines 19–21:** The missing resolution rate flags the data if too many tickets lack the text the agent depends on.
- **Lines 23–24:** The freshness check flags the data if it has not been updated within the last 24 hours.
- **Line 26:** The function returns a list of issues. An empty list means the data passed, and the pipeline can update the index. A non-empty list stops the update and alerts the data owner.

Checks like this turn data quality from a one-time cleanup into an ongoing property of the system, which is what keeps answers reliable months after launch.

## Common data pipeline mistakes[#](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-pipeline-mistakes)

Several mistakes recur in enterprise AI projects. The first is assuming data is ready because the customer says it is, without profiling it. The second is scoping the first release around every available source, which multiplies approvals and quality problems. The third is building a one-time data load for the pilot with no plan for keeping data current. The fourth is skipping sensitive data checks until a security review blocks the launch. The last is leaving data ownership undefined, so that when quality drops, no one on the customer side is responsible for fixing it.

Data readiness often determines whether an enterprise AI system reaches production, more than model choice or agent design. FDEs who profile data early, choose a narrow first domain based on both value and readiness, and build pipelines with built-in quality checks give the system a reliable foundation. Expanding one domain at a time then becomes a repeatable process rather than a new risk with each addition.

BigQuery and Text-to-SQL

Deployment and Runtime

Ask

[Common data-readiness problems](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-readiness-problems)

[Assessing data readiness](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Assessing-data-readiness)

[Why to start with a narrow data domain](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Why-to-start-with-a-narrow-data-domain)

[Building the pipeline](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Building-the-pipeline)

[Common data pipeline mistakes](https://www.educative.io/courses/forward-deployed-engineer/enterprise-data-pipelines#Common-data-pipeline-mistakes)