# Algorithm_Patterns_for_Palantir_FDE_Interview_Screens

Source: https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Algorithm Patterns That Show Up in the Screen

Apply essential algorithm patterns to solve sum and range problems efficiently. Use dictionaries to track counts, two pointers for sorted inputs, sliding windows for contiguous ranges, prefix sums to count exact sums with negative values, heaps to maintain top-k values, and breadth-first search (BFS) to explore graphs and grids. Identify each pattern's underlying invariants and discard rules, and adapt your approach to different problem constraints while optimizing performance.

We'll cover the following...

- [How to choose a pattern](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#How-to-choose-a-pattern)
- [Pattern 1: Dictionary for counts and groups](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-1-Dictionary-for-counts-and-groups)
- [Pattern 2: Two pointers on sorted input](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-2-Two-pointers-on-sorted-input)
  - [Pattern 3: Sliding window](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-3-Sliding-window)
  - [Pattern 4: Prefix sums with counts](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-4-Prefix-sums-with-counts)
  - [Pattern 5: Sort, then scan](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-5-Sort-then-scan)
  - [Pattern 6: Heap for the top k](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-6-Heap-for-the-top-k)
  - [Pattern 7: Graphs and grids with BFS](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-7-Graphs-and-grids-with-BFS)
  - [Practice: Count exact-sum ranges](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Practice-Count-exact-sum-ranges)

Find a pair of values that sums to a target in a sorted list. Count the contiguous ranges that sum to a target in a list with negative numbers. Both prompts are about sums, but they need different algorithms.

What decides the choice is why each algorithm can safely ignore some candidates. If you understand that, you can adapt when a screen question looks like a familiar template but breaks one of its assumptions.

## How to choose a pattern[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#How-to-choose-a-pattern)

Before coding, answer four questions:

1. **What object is requested?** A pair, a contiguous range, a group, a top-k ranking or a path.
2. **Which constraints change correctness?** Sorted input, negative values, duplicates, endpoint rules, edge weights.
3. **What state will you keep, and what does it mean?** That meaning is your invariant.
4. **Why is it safe to discard what you discard?**

A pattern is justified by its invariant and its discard argument, not by a familiar word in the prompt. Public preparation guides mention these patterns in screens, but they are reported possibilities, not an official list.

## Pattern 1: Dictionary for counts and groups[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-1-Dictionary-for-counts-and-groups)

Lesson 4 used a dictionary for keyed totals. The same tool covers counts and groups, as long as the key and value match the contract:

- For `[4, 4, 1]`, counts are `{4: 2, 1: 1}`. A set would lose the repeat.
- When identity is account plus symbol, both belong in the key.
- `'east' in totals` asks whether a key exists. `totals['east'] == 0` asks about its value. They are different questions.

Dictionary lookups take constant time on average, so one pass over `n` items is `O(n)`.

## Pattern 2: Two pointers on sorted input[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-2-Two-pointers-on-sorted-input)

Take ascending values `[1, 2, 4, 7, 11]` and target `10`. Start at both ends:

1. `1 + 11 = 12`, too large: move the right pointer in.
2. `1 + 7 = 8`, too small: move the left pointer in.
3. `2 + 7 = 9`, too small: move left.
4. `4 + 7 = 11`, too large: move right. The pointers meet, so no pair exists.

**Why discarding is safe:** if the sum is too small, the left value paired with any remaining right value is also too small, because those values are no larger. So that left value can never work. If the sum is too large, the same argument rules out the right value. This only works because the list is sorted.

C++

```
def find_pair(values, target):

left, right = 0, len(values) - 1

while left < right:

total = values[left] + values[right]

if total == target:

return (values[left], values[right])

if total < target:

left += 1

else:

right -= 1

return None

print(find_pair([1, 2, 4, 7, 11], 10))  # None

print(find_pair([1, 2, 4, 7, 11], 9))   # (2, 7)

print(find_pair([3, 3], 6))             # (3, 3)
```

⋯

Two pointers find a pair in sorted values.

- **Line 3:** `left < right` keeps the two indices distinct. Two equal values can still pair if they sit at different indices, as in `[3, 3]`.
- **Lines 7–10:** The discard rule: move whichever pointer can no longer be part of an answer.

Cost: `O(n)` time and `O(1)` extra space on sorted input. If the input is unsorted, sorting adds `O(n log n)` and loses the original indices unless you keep them.

### Pattern 3: Sliding window[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-3-Sliding-window)

A sliding window keeps state for one contiguous range, `text[left:right + 1]`. For “longest substring without repeated characters”, keep character counts for the window.

Trace `'abba'`:

- Add `a`: window `'a'`, best 1.
- Add `b`: window `'ab'`, best 2.
- Add the second `b`: there’s a repeat, so remove `a`, then the first `b`. The window is now `'b'`.
- Add the final `a`: window `'ba'`, best stays 2.

**Why discarding is safe:** Any window starting at or before the first `b` would contain both `b`s, so those starts can never be valid again.

C++

```
def longest_unique(text):

counts = {}

left = best = 0

for right, char in enumerate(text):

counts[char] = counts.get(char, 0) + 1

while counts[char] > 1:

counts[text[left]] -= 1

left += 1

best = max(best, right - left + 1)

return best

print(longest_unique("abba"))      # 2

print(longest_unique("abcabcbb"))  # 3

print(longest_unique(""))          # 0
```

⋯

Sliding window finds the longest repeat-free substring.

- **Line 5:** The new character enters the window.
- **Lines 6–8:** Shrink from the left until the repeat is gone.
- **Line 9:** The window is valid again, so measure it.

**Cost:** each pointer moves forward at most `n` times, so the loop is `O(n)` despite the nested `while`.

> **When a sum window breaks:** Find the shortest range with sum at least 3 in `[1, -1, 3]`. The usual window expands to the whole list (sum 3, length 3), then removes `1` and gets sum 2, so it stops. It misses `[3]`, which has length 1. Shrinking assumes that removing a value never increases the sum. Negative values break that, so don’t use a sum window when values can be negative.

### Pattern 4: Prefix sums with counts[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-4-Prefix-sums-with-counts)

To count ranges with an exact sum when values can be negative, use prefix sums. Define `P[0] = 0` and `P[i + 1] = P[i] + values[i]`. Then:

`sum(values[l:r]) = P[r] - P[l]`

For a target `t`, a range ending at `r` matches when `P[l] = P[r] - t`. At each step, count how many earlier prefixes equal `P[r] - t`.

For `[3, -2, 2, -3, 3]` with target `3`, the prefixes are `[0, 3, 1, 3, 0, 3]`. Start with `counts = {0: 1}`, which stands for the empty prefix before the first value.

Predict the last step before reading the full trace.

Predict the final contribution

1.

For [3, -2, 2, -3, 3], target 3, the final value has been added to the prefix but not yet queried:

- Current prefix: 3
- Earlier-prefix frequencies: {0: 2, 3: 2, 1: 1}
- Cumulative answer: 2

The prefixes at boundaries 0 through 5 are [0, 3, 1, 3, 0, 3]. How many matches does this query add, and which earlier boundaries supply them?

A.

Add 3 matches: the current prefix is 3, so it supplies three starts.

B.

Add 1 match: boundaries 0 and 4 share prefix zero, so count them once.

C.

Add 2 matches, from boundaries 0 and 4.

D.

Add 2 matches, from boundaries 1 and 3.

---

1 / 1

The full trace, as `(value, prefix, needed prefix, matches added, running answer)`:

- `(3, 3, 0, 1, 1)`
- `(-2, 1, -2, 0, 1)`
- `(2, 3, 0, 1, 2)`
- `(-3, 0, -3, 0, 2)`
- `(3, 3, 0, 2, 4)`

The last step adds 2 because prefix 0 occurred twice, at boundaries 0 and 4. Counts keep both starting positions, and a set would merge them. The four ranges are `[0:1]`, `[0:3]`, `[0:5]` and `[4:5]`.

**Invariant:** before each lookup, `counts` holds every earlier prefix with how many times it occurred.

C++

```
from itertools import product

def count_target_ranges(values, target):

prefix = 0

answer = 0

counts = {0: 1}          # empty prefix before index 0

for value in values:

prefix += value

answer += counts.get(prefix - target, 0)    # look up first

counts[prefix] = counts.get(prefix, 0) + 1  # then record

return answer

def brute_count(values, target):

answer = 0

for left in range(len(values)):

total = 0

for right in range(left, len(values)):

total += values[right]

if total == target:

answer += 1

return answer

def check(name, got, expected):

ok = got == expected

print("PASS" if ok else "FAIL", "-", name)

if not ok:

print("  got:", got)

print("  expected:", expected)

check("full trace", count_target_ranges([3, -2, 2, -3, 3], 3), 4)

check("single element", count_target_ranges([3], 3), 1)

check("zeros, target zero", count_target_ranges([0, 0], 0), 3)

check("empty input", count_target_ranges([], 0), 0)

mismatches = 0

for size in range(5):

for items in product((-1, 0, 1), repeat=size):

for target in range(-2, 3):

sample = list(items)

if count_target_ranges(sample, target) != brute_count(sample, target):

mismatches += 1

check("matches brute force on small inputs", mismatches, 0)
```

⋯

Prefix counts find every exact-sum range, with checks.

- **Line 7:** `{0: 1}` lets ranges that start at index 0 match. Without it, `[3]` with target 3 returns 0.
- **Lines 10–11:** Look up first, then record. Reversing them lets a boundary match itself, an empty range, so `[0, 0]` with target 0 returns 5 instead of 3.
- **Lines 15–23:** A slow, obviously correct version that tries every range. It’s used only for testing.
- **Lines 39–46:** These compare both versions on every list of length 0 to 4 built from -1, 0, and 1.

Cost: `O(n)` time and `O(n)` space, compared with `O(n²)` for the brute-force version. All five lines should print PASS.

### Pattern 5: Sort, then scan[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-5-Sort-then-scan)

Merge the closed intervals `[(5, 7), (1, 3), (2, 2), (3, 5), (9, 10)]`, where touching endpoints merge. After sorting by start, you only ever need to compare with the last merged interval.

C++

```
def merge_intervals(intervals):

merged = []

for start, end in sorted(intervals):

if merged and start <= merged[-1][1]:

merged[-1] = (merged[-1][0], max(merged[-1][1], end))

else:

merged.append((start, end))

return merged

data = [(5, 7), (1, 3), (2, 2), (3, 5), (9, 10)]

print(merge_intervals(data))  # [(1, 7), (9, 10)]

print(data)                   # unchanged
```

⋯

Sort by start, then merge overlapping intervals.

- **Line 3:** `sorted` returns a new list, so the input stays unchanged. `list.sort()` would modify it.
- **Line 4:** `<=` merges touching intervals. Use `<` if the contract keeps them separate.
- **Line 5:** `max` matters. `(2, 2)` sits inside `(1, 3)`, and taking its end would shrink coverage to 2.

**Why emitting is safe:** Once a gap appears, later intervals start even later, so they can’t reconnect to a finished interval. Cost: `O(n log n)` for the sort.

### Pattern 6: Heap for the top k[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-6-Heap-for-the-top-k)

To keep the largest `k` values from a stream, keep a min-heap of size `k`. Its smallest item, `heap[0]`, is the weakest value you’re keeping. Python’s `heapq` is a min-heap.

For the largest 3 of `[5, 1, 5, 3, 9]`: fill with `5, 1, 5`, where the weakest is 1. Then 3 replaces 1, and 9 replaces 3. The result is `[9, 5, 5]`.

C++

```
import heapq

def largest_k(values, k):

if k <= 0:

return []

heap = []

for value in values:

if len(heap) < k:

heapq.heappush(heap, value)

elif value > heap[0]:

heapq.heapreplace(heap, value)

return sorted(heap, reverse=True)

print(largest_k([5, 1, 5, 3, 9], 3))  # [9, 5, 5]

print(largest_k([2], 5))              # [2]

print(largest_k([4, 1], 0))           # []
```

⋯

Min-heap keeps the largest k values seen.

- **Lines 9–10:** Fill the heap until it holds `k` items.
- **Lines 11–12:** Replace the weakest kept value only when a bigger one arrives.
- **Line 13:** A heap isn’t fully sorted, so sort the final `k` items for output.

Cost: `O(n log k)` time and `O(k)` space. If you need the whole list ranked, just sort it.

**Tie-break tip:** For a job queue, push `(priority, sequence_number, job)`. The unique sequence number breaks ties, so Python never has to compare two job objects.

### Pattern 7: Graphs and grids with BFS[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-7-Graphs-and-grids-with-BFS)

Use an undirected graph with edges `A-B`, `A-C`, `B-D`, `C-D`, plus an isolated vertex `E`.

Breadth-first search (BFS) explores in layers, `{A}` then `{B, C}` then `{D}`, so the first time it reaches a node is by a shortest route when every edge costs the same. Depth-first search (DFS) dives down one branch. It works for “can I reach it?” but doesn’t guarantee shortest paths.

C++

```
from collections import deque

def bfs_distances(graph, start):

distance = {start: 0}

queue = deque([start])

while queue:

node = queue.popleft()

for neighbor in graph[node]:

if neighbor not in distance:

distance[neighbor] = distance[node] + 1

queue.append(neighbor)

return distance

def count_components(graph):

seen = set()

count = 0

for node in graph:

if node not in seen:

count += 1

seen.update(bfs_distances(graph, node))

return count

graph = {

'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D'],

'D': ['B', 'C'], 'E': [],

}

print(bfs_distances(graph, 'A'))  # {'A': 0, 'B': 1, 'C': 1, 'D': 2}

print(count_components(graph))    # 2
```

⋯

BFS gives distances; components counted with repeated BFS.

- **Line 6:** `deque` gives fast removal from the front. `list.pop(0)` is slow.
- **Lines 10–12:** Record the distance before adding to the queue, so cycles can’t add a node twice.
- **Lines 19–22:** Start a new search from every unseen node. Each start is a new component, which is how `E` is counted.

Cost: `O(V + E)` time. With unequal edge costs, BFS no longer gives shortest paths, and you need a different algorithm.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27851.5%27%20height=%27470.55999999999995%27/%3e)![Pathfinding with limited wall entries: two failed steps, six succeed.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Pathfinding with limited wall entries: two failed steps, six succeed.")

Pathfinding with limited wall entries: two failed steps, six succeed.

**Grids are graphs too:** Each cell’s neighbors are the four adjacent cells that are inside the grid and not walls. In the grid `["S..#G", ".#..."]`, the straight route along the top row is blocked at (0, 3). BFS finds the detour through the bottom row: 6 steps.

Python 3.14.0

```
from collections import deque

def shortest_path(grid):

if not grid:

return None

rows, cols = len(grid), len(grid[0])

start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 'S')

queue = deque([(start, 0)])

seen = {start}

while queue:

(r, c), steps = queue.popleft()

if grid[r][c] == 'G':

return steps

for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):

if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in seen:

seen.add((nr, nc))

queue.append(((nr, nc), steps + 1))

return None

print(shortest_path(["S..#G", ".#..."]))  # 6

print(shortest_path(["S#G"]))             # None

print(shortest_path(["SG"]))              # 1
```

⋯

BFS finds the shortest path on a grid.

- **Lines 13–14:** BFS dequeues cells in order of distance, so the first time `G` comes out is the shortest route.
- **Line 15:** The four neighbor positions: up, down, left, and right.
- **Line 16:** Skip positions outside the grid, walls, and cells already seen.

Cost: `O(rows × cols)`, since each cell is visited at most once.

**When a cell isn’t the whole state:** Suppose the prompt says “you may break through one wall”. Two arrivals at the same cell can then differ: one has already used its wall break, and one hasn’t. Store `(row, col, walls_left)` in `seen`, not just `(row, col)`, or BFS may discard the arrival that could still reach the goal. With up to `k` breaks there are at most `rows × cols × (k + 1)` states.

### Practice: Count exact-sum ranges[#](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Practice-Count-exact-sum-ranges)

For `[2, -2, 2, 0]` with target `2`, first write down every matching range on paper. Then answer: why can’t a shrinking sum window solve this? Finally, fill in the two TODOs.

Python 3.14.0

```
def count_target_ranges(values, target):

prefix = 0

answer = 0

counts = {0: 1}  # the empty prefix before index 0

for value in values:

prefix += value

# TODO 1: add to answer how many earlier prefixes equal prefix - target

# TODO 2: record the current prefix in counts

return answer
```

⋯

Fill both TODOs to count exact-sum ranges.

If your prediction and your code disagree, sum each predicted range by hand before changing the code. The mistake may be in the prediction.

Screen Formats, Time Strategy, and the Implementation Problem

SQL and API Tasks: Queries, Pagination, and Aggregation

Ask

[How to choose a pattern](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#How-to-choose-a-pattern)

[Pattern 1: Dictionary for counts and groups](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-1-Dictionary-for-counts-and-groups)

[Pattern 2: Two pointers on sorted input](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-2-Two-pointers-on-sorted-input)

[Pattern 3: Sliding window](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-3-Sliding-window)

[Pattern 4: Prefix sums with counts](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-4-Prefix-sums-with-counts)

[Pattern 5: Sort, then scan](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-5-Sort-then-scan)

[Pattern 6: Heap for the top k](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-6-Heap-for-the-top-k)

[Pattern 7: Graphs and grids with BFS](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Pattern-7-Graphs-and-grids-with-BFS)

[Practice: Count exact-sum ranges](https://www.educative.io/courses/forward-deployed-engineer/algorithm-patterns-that-show-up-in-the-screen#Practice-Count-exact-sum-ranges)