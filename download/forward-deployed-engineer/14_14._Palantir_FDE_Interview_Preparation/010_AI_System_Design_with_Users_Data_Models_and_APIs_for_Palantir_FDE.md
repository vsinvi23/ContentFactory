# AI_System_Design_with_Users_Data_Models_and_APIs_for_Palantir_FDE

Source: https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# From Ideation to Execution: Users, Data Models, and APIs

Define a bounded problem statement that clarifies the required support, then detail execution through user actions, data representation, and appropriate algorithms. Prioritize survey zones based on coverage gaps, keeping provisional labels separate from confirmed ones. Track recorded effort and observations, and use APIs to validate authority and ensure safe data handling. Apply simple rules for zone selection and reserve algorithms for complex scenarios. Model data as separate entities to support accurate tracking and verification, and complete the workflow only when the system reflects the results.

We'll cover the following...

- [Start from the user’s workflow](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Start-from-the-users-workflow)
- [APIs: Operations that match the workflow](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#APIs-Operations-that-match-the-workflow)
- [Where an algorithm fits, and where it doesn’t](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Where-an-algorithm-fits-and-where-it-doesnt)
- [Verify that the decision happened](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Verify-that-the-decision-happened)
- [Common follow-ups](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Common-follow-ups)

A bounded problem statement says *what* to support. Execution answers how: what the user does, what data represents it, which operations change it, and whether any step needs a real algorithm.

The species framing from decomposition carries straight through. The field coordinator must choose tomorrow’s two survey zones before 16:00, prioritizing coverage gaps and keeping provisional labels separate from reviewed ones.

## Start from the user’s workflow[#](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Start-from-the-users-workflow)

Describe the coordinator’s day as steps, before choosing any technology:

1. See each zone’s recorded effort, observations, and access status.
2. Pick two feasible zones and assign the teams.
3. After the survey, see the returned effort and observations.
4. The expert reviewer confirms or corrects provisional labels.

Every later design choice should serve one of these steps. If a component doesn’t, it is out of scope for now.

The confirmation step connects inspection to execution, but the preview cannot reserve the world. Records and permissions can change before submission, so the command must validate them again.

## Data Model: Name the Entities and their Keys

|  |  |  |  |
| --- | --- | --- | --- |
| **Entity** | **Key** | **Key Fields** | **Why It Exists** |
| Zone | zone\_id | name, access status | Assignments and coverage are per zone |
| Assignment | assignment\_id | zone\_id, team, date, planned hours | Records the coordinator’s decision |
| Survey effort | effort\_id | assignment\_id, zone\_id, actual hours, returned\_at | Proves the survey happened |
| Observation | observation\_id | zone\_id, effort\_id, event time, upload time, provisional label | One sighting, linked to the effort that produced it |
| Review | review\_id | observation\_id, reviewer, reviewed label, status | Keeps confirmed labels separate from provisional ones |

Three choices do most of the work:

- **Effort is its own entity.** Coverage is computed from effort, not from observation counts, so “zero sightings” and “never surveyed” stay distinguishable.
- **Assignment and effort are separate.** A planned survey isn’t a completed one. Only returned effort counts toward coverage.
- **Reviews don’t overwrite observations.** The provisional label stays, and the review adds a confirmed one beside it. That preserves history and shows what is still unconfirmed.

## APIs: Operations that match the workflow[#](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#APIs-Operations-that-match-the-workflow)

|  |  |  |  |
| --- | --- | --- | --- |
| **Workflow Step** | **Operation** | **Validates** | **Changes** |
| See coverage | `GET /zones/coverage?date=` | User may view zones | Nothing (read-only) |
| Assign teams | `POST /assignments` | Coordinator role, zone access approved, team capacity | Creates an assignment |
| Return a survey | `POST /effort` | Assignment exists, hours ≥ 0 | Records actual effort |
| Upload sightings | `POST /observations` | Effort exists; duplicate observation\_id is ignored | Adds observations |
| Review a label | `POST /reviews` | Reviewer role | Adds a reviewed label |

Two habits make an API defensible:

- **Validate authority and feasibility where the change happens.** `POST /assignments` rejects a zone without approved access, whatever the dashboard showed.
- **Make retried writes safe.** If an upload is sent twice, reusing the same `observation_id` means it is stored once. This is the same identity rule used for paginated totals.

## Where an algorithm fits, and where it doesn’t[#](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Where-an-algorithm-fits-and-where-it-doesnt)

With four zones and two teams, choosing zones is a short rule, not an optimization problem:

1. Keep only zones with approved access.
2. Put zones with zero recorded effort first.
3. Then sort by lowest recorded effort.
4. Show the result as a recommendation. The coordinator makes the final choice.

That rule is explainable, easy to test, and matches the framing (coverage gaps first). A complex model would add risk without adding information.

|  |  |
| --- | --- |
| **Situation** | Approach |
| 4 zones, 2 teams, one deadline | Simple ranking rule, coordinator decides |
| 200 zones, 10 teams, travel times between zones | Assignment problem: start greedy, consider an optimizer if greedy plans are clearly worse |
| Thousands of photos needing labels | Classifier to suggest labels and triage review. Experts still confirm |
| Labels must be legally certified | No algorithm replaces the expert; software only routes the work |

**Rule of thumb:** Reach for an algorithm when the constraints or scale make a simple rule fail, and say what would make you upgrade. “I’d start with the ranking rule. If we grow to hundreds of zones with travel costs, I’d treat it as an assignment problem.”

## Verify that the decision happened[#](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Verify-that-the-decision-happened)

The workflow is done when the system can show the result, not when the assignment button works:

- **Assigned:** An assignment exists for C tomorrow.
- **Completed:** Returned effort for C is greater than zero.
- **Improved:** Coverage goes from 3 of 4 zones to 4 of 4, computed from effort records.

Each check reads a different entity. That is why the data model kept them separate.

Technical Quiz

1.

Why is survey effort stored as its own entity rather than inferred from observations?

A.

It makes the database faster.

B.

A zone with zero observations could be unsurveyed or surveyed with no sightings, and only effort records tell them apart.

C.

Observations can’t include a zone ID.

D.

Effort is needed only for billing.

---

1 / 2

## Common follow-ups[#](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Common-follow-ups)

Interviewers often probe a design with follow-ups like these. Have a short answer ready for each.

1.

How would this scale to hundreds of zones?

Show Answer

1 / 5

Decomposition: What It Tests and a Repeatable Framework

The Learning Round: Reading Docs and Extending Systems

Ask

[Start from the user’s workflow](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Start-from-the-users-workflow)

[APIs: Operations that match the workflow](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#APIs-Operations-that-match-the-workflow)

[Where an algorithm fits, and where it doesn’t](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Where-an-algorithm-fits-and-where-it-doesnt)

[Verify that the decision happened](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Verify-that-the-decision-happened)

[Common follow-ups](https://www.educative.io/courses/forward-deployed-engineer/from-ideation-to-execution-users-data-models-and-apis#Common-follow-ups)