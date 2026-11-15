# Debugging_and_Verifying_Fixes_in_Palantir_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Re-Engineering Round: Debugging and Verifying Fixes

Establish expected behavior from the service contract, reproduce failures with controlled inputs, and trace data flow to identify their causes. Distinguish history-dependent failures from input-dependent failures by testing with fresh service instances. Manage mutable state carefully, account for state lifetimes, and implement backtracking in graph traversal to preserve valid paths. Investigate common debugging pitfalls and practice identifying, isolating, and resolving bugs efficiently.

We'll cover the following...

- [The contract comes first](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-contract-comes-first)
- [A debugging sequence](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-debugging-sequence)
- [Find the bug without reading everything](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Find-the-bug-without-reading-everything)
- [The first incorrect decision](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-first-incorrect-decision)
- [Reproduce, probe and repair](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reproduce-probe-and-repair)
- [A different bug: Wrong visited-state lifetime](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-different-bug-Wrong-visited-state-lifetime)
- [Practice: find the lost path](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Practice-find-the-lost-path)
  - [Reported re-engineering questions](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reported-re-engineering-questions)

The first tally request returns `red=2, blue=1`. The second returns only `blue=1`, although it should return `red=1, blue=1`.

Before reading the whole repository, ask one question: does the second request succeed on a fresh service instance? That experiment makes request history a testable variable and tells you where to look next.

## The contract comes first[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-contract-comes-first)

The endpoint’s contract is request-local:

- Each distinct event ID contributes once within a request.
- Repeated deliveries of one ID have the same category.
- Separate requests are independent.

Use these two requests, in order, on the same service:

- **Request 1:** `[(E1, red), (E2, blue), (E1, red), (E3, red)]`
- **Request 2:** `[(E1, red), (E4, blue)]`

Before looking at any code, pick a probe that separates a history-dependent failure from an input-dependent one.

Choose the first probe

1.

Request one returns red=2, blue=1; request two on the same service returns only blue=1. Each distinct event ID should contribute once per request, and requests are independent.

Before inspecting the implementation, which first probe and prediction best test whether retained request history causes the failure?

A.

Reverse category sort order and repeat the sequence, predicting that red will reappear if presentation order hides it.

B.

Delete duplicate suppression and repeat the sequence, predicting that allowing every delivery to contribute will restore the missing red.

C.

Add one to the red count in request two, predicting red=1, blue=1 and treating that result as confirmation of the cause.

D.

Run request two alone on a fresh TallyService, without edits. If retained history causes the failure, predict red=1, blue=1.

---

1 / 1

A request-two success on a fresh instance doesn’t mean the service works when reused. It means the failing input is fine, and the problem is state that survives between calls.

## A debugging sequence[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-debugging-sequence)

1. Establish the expected behavior from the contract.
2. Reproduce the symptom with a controlled input sequence.
3. Trace the relevant control and data flow.
4. List competing explanations.
5. Run a probe whose outcomes tell them apart.
6. Make a focused repair.
7. Verify the changed behavior *and* the behavior that must stay the same.

A secondary summary of Palantir’s guidance lists working within existing systems as an engineering competency. One individual account of a software-engineer interview describes short stages of reading code, discussing limits and coding fixes. Reported codebase sizes vary widely between guides, so the sizes don’t predict your interview. Practice reading unfamiliar code quickly instead.

The tally and graph code in this lesson is invented practice, not Palantir code or a known interview question.

## Find the bug without reading everything[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Find-the-bug-without-reading-everything)

Build a narrow map: the request entry point, the tally operation, the formatter and the tests. Follow event E1 through it, asking where its identity is read and where mutable state is stored.

Four explanations fit part of the symptom. Each makes a different prediction:

|  |  |  |
| --- | --- | --- |
| **Hypothesis** | **If true, you would see** | **Probe** |
| Formatter drops red | Raw counts contain red, the output doesn’t | Compare raw counts with formatted output |
| Parser drops E1 | E1 missing before the tally | Print the parsed events |
| Deduplication is disabled | Request 1 returns red=3 | Check request 1 alone |
| Exclusion state is retained | Request 2 works alone, fails after request 1 | Run request 2 on a fresh service |

Use fresh, identically initialized instances for each probe. Calling the tally twice on the same instance changes the very state you’re investigating.

Only the last hypothesis predicts “fresh works, reused fails”. The formatter is a **red herring**: it looks suspicious, but it only sorts labels. The raw tally is already missing red before formatting.

## The first incorrect decision[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-first-incorrect-decision)

Here is the buggy service. The exclusion set `seen` lives on the instance for its whole lifetime, but `counts` is created fresh for each call.

Trace request 2 on the reused service:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Step** | **Event** | **`seen`**  **before** | **Decision** | **Counts** |
| 1 | E1/red | `{E1, E2, E3}` | Skipped. First incorrect exclusion | `{}` |
| 2 | E4/blue | `{E1, E2, E3}` | Accepted | `{blue: 1}` |

The invariant: after each processed prefix, `seen` must hold exactly the IDs accepted **in this request**. The contract requires an empty `seen` at the start of every request, and line 1 of that trace is where the code breaks it.

> **Tempting repairs that don’t work**
>
> - **Delete the duplicate check.** Request 2 now works, but request 1 returns `red=3`, because both copies of E1 count.
> - **Add one to red.** This patches the example, not the cause.
> - **Reset** **`self.seen`** **at the start of** **`tally`****.** This works for one thread, but request-owned data is still stored as shared instance state, so overlapping calls would interfere.

The smallest repair gives `seen` the same lifetime as `counts`: create both inside `tally`. Deduplicate by ID, not by payload. E7/red and E8/red are two events and both count.

## Reproduce, probe and repair[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reproduce-probe-and-repair)

Run the starter first. It reproduces the symptom: the fresh-instance probe passes, and two reused-instance checks fail. Then move `seen` into `tally`.

C++

```
import json

class TallyService:

def __init__(self):

self.seen = set()  # TODO: this set outlives a single request

def tally(self, events):

counts = {}

for event_id, category in events:

if event_id in self.seen:

continue

self.seen.add(event_id)

counts[category] = counts.get(category, 0) + 1

return counts

def handle_request(events, service):

counts = service.tally(events)

return json.dumps({"counts": dict(sorted(counts.items()))}, separators=(",", ":"))

REQ1 = [("E1", "red"), ("E2", "blue"), ("E1", "red"), ("E3", "red")]

REQ2 = [("E1", "red"), ("E4", "blue")]
```

⋯

Reproduce the bug, then give seen request scope.

- **Lines 5–7:** `seen` is created inside `tally`, next to `counts`. Both now live exactly one request.
- **Lines 9–11:** The duplicate check is unchanged, so a repeated E1 inside one request still counts once.

In the starter, `request 2 after request 1` and `request 1 repeated` fail, and the fresh-instance check passes. That combination points at retained state. A passing run supports these cases only. It doesn’t prove the service is correct for every input.

## A different bug: Wrong visited-state lifetime[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-different-bug-Wrong-visited-state-lifetime)

The same mistake shows up in graph traversal. First settle what the question asks, because each version needs different exclusion state:

|  |  |  |
| --- | --- | --- |
| **Question** | **Exclusion State** | **Result on the Example Graph** |
| Which vertices are reachable? | One visited set for the whole traversal | `{S, A, B, T}` |
| Shortest distance (equal-cost edges)? | First-discovery distance per vertex, using BFS | T is 2 away |
| All simple paths (no repeated vertex)? | The vertices on the current path only | `S–A–T`  and  `S–B–A–T` |

For all simple paths, a traversal-wide visited set is the bug. After exploring `S–A–T`, A stays marked visited. The later branch `S–B–A` finds A excluded and loses a valid path.

The fix is **backtracking**. Add a vertex when entering it, and remove it when leaving, *including after reaching the target*. The cycle `A→S` is still blocked, because S is on the current path.

The traversal-wide visited set is the right tool for reachability, where each vertex needs expanding only once. Using it to enumerate paths is the mistake. The reverse is a different mistake: path enumeration can produce exponentially many results, so it isn’t an `O(V+E)` reachability job.

## Practice: find the lost path[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Practice-find-the-lost-path)

Use this graph (neighbors in the listed order): `P: [Q, R]`, `Q: [U]`, `R: [Q]`, `U: [P, V]`, `V: []`, `Z: []`. The task is to return all simple directed paths from the source to the target, in adjacency order. A source equal to the target returns one zero-edge path.

Before running, predict one missing path from the starter, and name the exact vertex wrongly excluded and why. The answer is in the output.

Running the starter before you change anything is safe. It prints FAIL for two checks, not an error.

C++

```
GRAPH = {"P": ["Q", "R"], "Q": ["U"], "R": ["Q"], "U": ["P", "V"], "V": [], "Z": []}

def simple_paths(graph, source, target):

paths = []

path = []

visited = set()  # TODO: This is never cleared when the DFS backs out of a vertex

def visit(node):

visited.add(node)

path.append(node)

if node == target:

paths.append(path.copy())

else:

for neighbor in graph.get(node, []):

if neighbor not in visited:

visit(neighbor)

path.pop()

# TODO: Undo what you did on entry, so the exclusion is path-local

visit(source)

return paths
```

⋯

Make exclusion path-local so no path is lost.

In the solution:

- **Line 7:** `on_path` holds exactly the vertices of the current path, not every vertex ever seen.
- **Lines 10–11:** On entry, a vertex joins both the path and the set.
- **Line 13:** `path.copy()` saves a snapshot, so later backtracking can’t change a saved answer.
- **Lines 15–17:** Only vertices already on this path are skipped. That blocks the cycle `U→P` and still allows `R→Q` after the first branch has finished.
- **Lines 18–19:** Undo the entry on every exit, including after reaching the target. This is the line that makes Q eligible again for the branch through R.

In the starter, `P to V` returns only one path and `P to Q` returns only `[P, Q]`. The vertex wrongly excluded is Q, on the branch `P→R→Q`, because the first branch left it in `visited`.

### Reported re-engineering questions[#](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reported-re-engineering-questions)

These prompt shapes appear in public candidate reports. Wording varies, and none is guaranteed.

1.

Here is a codebase. Find a limitation against this requirement.

Show Answer

1 / 5

The Learning Round: Reading Docs and Extending Systems

The Coding Round: User Needs and Changing Requirements

Ask

[The contract comes first](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-contract-comes-first)

[A debugging sequence](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-debugging-sequence)

[Find the bug without reading everything](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Find-the-bug-without-reading-everything)

[The first incorrect decision](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#The-first-incorrect-decision)

[Reproduce, probe and repair](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reproduce-probe-and-repair)

[A different bug: Wrong visited-state lifetime](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#A-different-bug-Wrong-visited-state-lifetime)

[Practice: find the lost path](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Practice-find-the-lost-path)

[Reported re-engineering questions](https://www.educative.io/courses/forward-deployed-engineer/the-re-engineering-round-debugging-and-verifying-fixes#Reported-re-engineering-questions)