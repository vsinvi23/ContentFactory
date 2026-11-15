# SQL_Queries_Pagination_and_Aggregation_for_Palantir_FDE_Interview

Source: https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# SQL and API Tasks: Queries, Pagination, and Aggregation

Maintain record identity in SQL queries and paginated API tasks to ensure accurate reporting. Define the grain of each output row, construct queries that prevent double counting, and verify data completeness. Apply correct filters, choose appropriate joins, and handle pagination according to defined contracts. Identify common pitfalls and use practical examples to produce accurate, reliable results across SQL and API workflows.

We'll cover the following...

- [Start with the grain](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Start-with-the-grain)
- [The task: Late-delivery losses by region](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#The-task-Late-delivery-losses-by-region)
- [Fix it in stages](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Fix-it-in-stages)
  - [Pagination: State the contract first](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Pagination-State-the-contract-first)
  - [Practice 1: Fix the query](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-1-Fix-the-query)
  - [Practice 2: Total per category across pages](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-2-Total-per-category-across-pages)
  - [Recap](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Recap)

Order O1 loses 40, but a join gives it two matching rows and the report says 80. Every addition is correct. What went wrong is that the query lost track of *what* should contribute.

SQL reports and paginated API totals fail in the same way. Both need you to keep each record’s identity intact and to show that every qualifying record was included exactly once.

## Start with the grain[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Start-with-the-grain)

**Grain** means what one output row represents: one order, one customer or one region. Before writing a query, work through this:

1. State the output grain and what qualifies a record.
2. Identify the entities that contribute and their keys.
3. Predict which joins will multiply rows.
4. Resolve the *current* record before filtering on current status.
5. Aggregate, then hand-check a tricky example.

For an API, state the paging contract before writing the loop.

One public preparation guide reports an assessment with implementation, SQL and paginated-API tasks, and another mentions a “regional losses from late deliveries” theme. These are reported possibilities, not guaranteed questions. The tasks below are practice contracts built from those themes.

This lesson runs SQL through Python’s built-in `sqlite3` module, so every example runs in the code widget. The SQL used here works the same way in PostgreSQL.

## The task: Late-delivery losses by region[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#The-task-Late-delivery-losses-by-region)

**Contract:**

- Output one row per region in `customers`, including regions with no qualifying orders.
- An order qualifies if it was placed in `[2026-07-01, 2026-10-01)` and its latest delivery event says `late`.
- “Latest” means the greatest `event_time`. When two events share a time, the larger `event_id` wins.
- An order with no events has unknown status, so it doesn’t qualify.
- Report the count of qualifying orders and their total loss. A region with none shows `0, 0`.

The fixture contains four traps:

- **O1** has two events at 11:00 (102 on time and 103 late), so the tie-break decides its status.
- **O3** was late earlier but is on time now (302 at 13:00). Its event with the highest ID (303) is an *older* late event.
- **O5** has no events.
- **C4** (south) has no orders at all.

The plausible query is wrong.

C++

```
import sqlite3

db = sqlite3.connect(":memory:")

db.executescript("""

CREATE TABLE customers (customer_id TEXT PRIMARY KEY, region TEXT);

CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT, placed_at TEXT, loss INTEGER);

CREATE TABLE delivery_events (event_id INTEGER PRIMARY KEY, order_id TEXT, status TEXT, event_time TEXT);

INSERT INTO customers VALUES ('C1','east'), ('C2','west'), ('C3','north'), ('C4','south');

INSERT INTO orders VALUES ('O1','C1','2026-08-01',40), ('O2','C1','2026-08-01',15),

('O3','C2','2026-08-01',25), ('O5','C2','2026-08-01',10), ('O4','C3','2026-08-01',0);

INSERT INTO delivery_events VALUES

(101,'O1','late','2026-08-02 10:00'), (102,'O1','on_time','2026-08-02 11:00'),

(103,'O1','late','2026-08-02 11:00'), (201,'O2','late','2026-08-02 12:00'),

(301,'O3','late','2026-08-02 09:00'), (302,'O3','on_time','2026-08-02 13:00'),

(303,'O3','late','2026-08-02 08:00'), (401,'O4','late','2026-08-02 12:00');

""")

naive = """

SELECT c.region, SUM(o.loss) AS total_loss

FROM customers c

JOIN orders o ON o.customer_id = c.customer_id

JOIN delivery_events e ON e.order_id = o.order_id

WHERE o.placed_at >= '2026-07-01' AND o.placed_at < '2026-10-01'

AND e.status = 'late'

GROUP BY c.region

ORDER BY c.region;

"""

for row in db.execute(naive):

print(row)
```

⋯

Naive join double-counts losses and drops a region.

It prints `('east', 95)`, `('north', 0)` and `('west', 50)`. The correct answer is east 55, north 0, south 0, and west 0.

- **Lines 4–16:** An in-memory database with the fixture. Dates are stored as `YYYY-MM-DD` text, so comparing them as text also compares them in time order.
- **Line 22:** Joining orders to events creates one row per event, not per order. O1 has two late events, so its 40 is added twice (80). With O2’s 15, east becomes 95.
- **Line 24:** `status = 'late'` matches *any* late event in history. O3 is on time now, but its two old late events add 25 + 25 = 50 to west.
- **Line 21:** An inner join drops customers with no orders, so south disappears.

> **Two more join traps**
>
> - `LEFT JOIN orders o ... WHERE o.placed_at >= '2026-07-01'` still drops south. For C4, `o.placed_at` is NULL, the condition isn’t true, and the row is filtered out. Put conditions on the right-side table inside the `ON` clause, or build the qualifying orders first and then left join them.
> - `SUM(DISTINCT o.loss)` doesn’t fix double counting. Two different orders that each lose 40 should add up to 80, not 40. Fix the grain instead of the arithmetic.

## Fix it in stages[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Fix-it-in-stages)

Build the answer one grain at a time: first the latest event per order, then the qualifying orders, then one row per region.

C++

```
import sqlite3

db = sqlite3.connect(":memory:")

db.executescript("""

CREATE TABLE customers (customer_id TEXT PRIMARY KEY, region TEXT);

CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT, placed_at TEXT, loss INTEGER);

CREATE TABLE delivery_events (event_id INTEGER PRIMARY KEY, order_id TEXT, status TEXT, event_time TEXT);

INSERT INTO customers VALUES ('C1','east'), ('C2','west'), ('C3','north'), ('C4','south');

INSERT INTO orders VALUES ('O1','C1','2026-08-01',40), ('O2','C1','2026-08-01',15),

('O3','C2','2026-08-01',25), ('O5','C2','2026-08-01',10), ('O4','C3','2026-08-01',0);

INSERT INTO delivery_events VALUES

(101,'O1','late','2026-08-02 10:00'), (102,'O1','on_time','2026-08-02 11:00'),

(103,'O1','late','2026-08-02 11:00'), (201,'O2','late','2026-08-02 12:00'),

(301,'O3','late','2026-08-02 09:00'), (302,'O3','on_time','2026-08-02 13:00'),

(303,'O3','late','2026-08-02 08:00'), (401,'O4','late','2026-08-02 12:00');

""")

query = """

WITH ranked AS (

SELECT e.*, ROW_NUMBER() OVER (

PARTITION BY order_id ORDER BY event_time DESC, event_id DESC) AS rn

FROM delivery_events e

),

latest AS (SELECT * FROM ranked WHERE rn = 1),

qualifying AS (

SELECT o.order_id, o.customer_id, o.loss

FROM orders o

JOIN latest l ON l.order_id = o.order_id

WHERE o.placed_at >= '2026-07-01' AND o.placed_at < '2026-10-01'

AND l.status = 'late'

)

SELECT c.region,

COUNT(q.order_id) AS late_orders,

COALESCE(SUM(q.loss), 0) AS total_loss

FROM customers c

LEFT JOIN qualifying q ON q.customer_id = c.customer_id

GROUP BY c.region

ORDER BY c.region;

"""

for row in db.execute(query):

print(row)
```

⋯

Staged query: latest event first, then regional totals.

It prints `('east', 2, 55)`, `('north', 1, 0)`, `('south', 0, 0)` and `('west', 0, 0)`.

- **Lines 19–23:** `ROW_NUMBER` numbers each order’s events, newest first, without collapsing the rows the way `GROUP BY` would.
- **Line 21:** `event_id DESC` is the tie-breaker. Without it, O1’s two 11:00 events could rank either way.
- **Line 24:** Keep only the latest event per order: O1 → 103 (late), O2 → 201, O3 → 302 (on time), O4 → 401.
- **Lines 25–31:** Filter on status *after* choosing the latest event. Filtering for late events first would bring back O3’s old event 301. The inner join on line 28 drops O5, which has no events.
- **Lines 33–34:** `COUNT(q.order_id)` counts real orders, not placeholder rows. `COALESCE` turns an empty region’s NULL sum into 0.
- **Line 36:** `LEFT JOIN` from customers keeps every region, including south and west.

East’s 55 is 40 + 15. Each order appears once in `qualifying`, so its loss is added once.

> **NULL, counting and filtering groups**
>
> - `COUNT(*)` counts rows, including a LEFT JOIN placeholder row.
> - `COUNT(column)` skips NULLs, so a placeholder counts as 0.
> - `SUM(column)` ignores NULLs and returns NULL when there is nothing to add. That’s why line 34 uses `COALESCE`.
> - `WHERE` filters rows before grouping. `HAVING` filters groups after. For example, adding `HAVING COALESCE(SUM(q.loss), 0) > 20` after `GROUP BY` keeps only east. `WHERE` can’t do this, because the sum doesn’t exist until rows are grouped.

### Pagination: State the contract first[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Pagination-State-the-contract-first)

Now retrieve East’s losses from a paginated API instead of a database. Here is the contract:

- The first request has no token. Each response has `items` (records with `id` and `loss`) and may include `nextPageToken`.
- Pass `nextPageToken` as the token for the next request.
- The traversal is complete only when `nextPageToken` is absent. A short or empty page doesn’t mean you’re done.
- The same `id` on two pages is one record. The same `id` with a different `loss` is an error.
- The data doesn’t change while you page through it.

This token style is common, and Palantir’s Foundry API uses a similar `pageToken` / `nextPageToken` pattern. The endpoint here is a practice contract, not a real Foundry endpoint.

Decide how far the traversal must go before reading the code.

When is the total complete?

1.

Requests keep region=east and pageSize=2 fixed. All requests succeed, with no retries:

| Requested page | items (id/loss) | nextPageToken |
| --- | --- | --- |
| Start | O1/40 | a |
| a | O1/40 | b |
| b | O2/15 | absent |

Under the specified GET contract, which traversal and final total are correct?

A.

Reject page a because the repeated O1 automatically makes the traversal invalid.

B.

Follow all three pages and count each stable ID once; return 55.

C.

Stop after Start because it has fewer than two items; return 40.

D.

Follow all three pages and sum every returned item; return 95.

---

1 / 1

The code below uses a dictionary in place of the real API, so no network is needed.

C++

```
PAGES = {

None: {"items": [{"id": "O1", "loss": 40}], "nextPageToken": "a"},

"a": {"items": [{"id": "O1", "loss": 40}], "nextPageToken": "b"},

"b": {"items": [{"id": "O2", "loss": 15}]},

}

def total_loss(fetch, max_pages=100):

token = None

seen_tokens = set()

losses = {}

for _ in range(max_pages):

if token in seen_tokens:

raise RuntimeError("repeated page token")

seen_tokens.add(token)

page = fetch(token)

for item in page["items"]:

if item["id"] in losses and losses[item["id"]] != item["loss"]:

raise RuntimeError("conflicting duplicate " + item["id"])

losses[item["id"]] = item["loss"]

if "nextPageToken" not in page:

return sum(losses.values())

token = page["nextPageToken"]

raise RuntimeError("page limit exceeded")

def expect_error(pages, label):

try:

total_loss(lambda token: pages[token])

print("FAIL -", label, "returned a total")

except RuntimeError as error:

print("PASS -", label, "->", error)

print("total:", total_loss(lambda token: PAGES[token]))  # 55

empty_first = {None: {"items": [], "nextPageToken": "z"}, "z": {"items": [{"id": "O9", "loss": 3}]}}

print("empty page, then data:", total_loss(lambda token: empty_first[token]))  # 3

expect_error({None: {"items": [], "nextPageToken": "a"},

"a": {"items": [], "nextPageToken": "a"}}, "token loop")

expect_error({None: {"items": [{"id": "O1", "loss": 40}], "nextPageToken": "a"},

"a": {"items": [{"id": "O1", "loss": 41}]}}, "conflicting O1")
```

⋯

Follow page tokens; count each ID only once

- **Lines 1–5:** The fake API. O1 appears on two pages.
- **Lines 13–15:** If a token repeats, the API is looping, so stop with an error rather than looping forever.
- **Lines 17–20:** Losses are stored by `id`, so O1 counts once even though it appears twice. A different loss for the same `id` is an error, not something to guess about.
- **Lines 21–22:** Return only when `nextPageToken` is absent. That’s the contract’s definition of complete.
- **Line 24:** A safety limit, in case the API never ends.
- **Lines 37–38:** An empty first page still has a token, so the loop continues and finds O9.

**Invariant:** After each page, `losses` holds exactly one entry for each distinct `id` seen so far.

Completeness and counting once are separate checks. A deduplicated total can still be incomplete if you stop early, and a complete traversal can still double-count if you add every item as it arrives.

> **Other pagination styles: Each has its own stop signal**
>
> - **Token or cursor** **(**`nextPageToken`, `cursor`**):** Stop when the token is absent or null.
> - **Page number** **(**`?page=1`, `?page=2`, …**):** Stop at the last page the response reports, such as `total_pages`.
> - **Offset and limit** **(**`?offset=0&limit=10`, then `offset=10`, …**):** Increase the offset by the limit each time. Stop on an empty page, or when you’ve reached a reported `total`.
> - **Flag** **(**`has_more: false`**):** Stop when the flag says there’s nothing more.
>
> Use the stop signal the documentation defines. A short page only means you’re done if the docs say so.

### Practice 1: Fix the query[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-1-Fix-the-query)

The practice fixture has customers U (east) and V (west). Orders P1 (loss 7) and P2 (loss 5) both belong to U and were placed on 2026-08-01. P1 has three events: 1 late at 10:00, 2 on time at 11:00, and 3 late at 11:00. P2 has one late event at 12:00. The rules are the same as above.

Predict the output before writing code. Which event decides P1’s status? Then replace the naive query with a staged one.

C++

```
import sqlite3

db = sqlite3.connect(":memory:")

db.executescript("""

CREATE TABLE customers (customer_id TEXT PRIMARY KEY, region TEXT);

CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT, placed_at TEXT, loss INTEGER);

CREATE TABLE delivery_events (event_id INTEGER PRIMARY KEY, order_id TEXT, status TEXT, event_time TEXT);

INSERT INTO customers VALUES ('U','east'), ('V','west');

INSERT INTO orders VALUES ('P1','U','2026-08-01',7), ('P2','U','2026-08-01',5);

INSERT INTO delivery_events VALUES

(1,'P1','late','2026-08-02 10:00'), (2,'P1','on_time','2026-08-02 11:00'),

(3,'P1','late','2026-08-02 11:00'), (4,'P2','late','2026-08-02 12:00');

""")

# TODO: replace this naive query with a staged query:

#   1. rank each order's events (latest time first, larger event_id wins ties)

#   2. keep orders whose latest event is 'late', placed in [2026-07-01, 2026-10-01)

#   3. LEFT JOIN from customers: region, order count, total loss (0 if none)

query = """

SELECT c.region, SUM(o.loss) AS total_loss

FROM customers c

JOIN orders o ON o.customer_id = c.customer_id

JOIN delivery_events e ON e.order_id = o.order_id

WHERE e.status = 'late'

GROUP BY c.region

ORDER BY c.region;

"""

expected = [('east', 2, 12), ('west', 0, 0)]

got = db.execute(query).fetchall()

print("PASS" if got == expected else "FAIL", "- got:", got, "expected:", expected)
```

⋯

Rewrite the query to use latest order status.

If your result is wrong, check each stage on its own. Run `SELECT * FROM latest` first. If P1 shows event 2, the tie-break is missing.

### Practice 2: Total per category across pages[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-2-Total-per-category-across-pages)

A common API-task variant combines pagination with grouping. The fake API below returns transactions with `id`, `category` and `amount`. Return a sorted list of `(category, total)` pairs, counting each `id` once and following tokens until `nextPageToken` is absent.

Before coding, look at the pages and predict the answer. Note the repeated T2 and the empty page in the middle.

The `break` on the TODO 3 line stops the loop after one page, so it prints FAIL instead of looping. Remove that `break` when you complete TODO 3.

Python 3.14.0

```
PAGES = {

None: {"items": [{"id": "T1", "category": "fuel", "amount": 30},

{"id": "T2", "category": "parts", "amount": 20}], "nextPageToken": "p2"},

"p2": {"items": [{"id": "T2", "category": "parts", "amount": 20}], "nextPageToken": "p3"},

"p3": {"items": [], "nextPageToken": "p4"},

"p4": {"items": [{"id": "T3", "category": "fuel", "amount": 5}]},

}

def totals_by_category(fetch):

token = None

seen_ids = set()

totals = {}

for _ in range(100):  # safety limit

page = fetch(token)

for item in page["items"]:

pass  # TODO 1: skip ids already counted; TODO 2: add amount to totals[category]

# TODO 3: if there is no "nextPageToken", stop; otherwise move to it

break  # remove this line when you finish TODO 3

return sorted(totals.items())
```

⋯

Total per category across pages, counting IDs once.

If you get parts 40, you added T2 twice. If you get only fuel 30 and parts 20, you stopped at the empty page or after the first page.

### Recap[#](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Recap)

Before you submit any data task, you should be able to say three things:

- **What one output row represents:** One region, or one category.
- **When a record contributes:** Once per order, based on its latest event, or once per API `id`.
- **What proves completeness:** The `LEFT JOIN` keeps every region, and paging stops only at the documented stop signal.

You now have the pieces a screen asks for: an implementation task, an algorithm pattern, a SQL query, and a paginated API total. The next lesson puts them together in one timed technical screen, solved step by step, and shows how to keep each of these checks intact when they all share one deadline.

Algorithm Patterns That Show Up in the Screen

Case Study: A Full Technical Screen, Solved Step by Step

Ask

[Start with the grain](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Start-with-the-grain)

[The task: Late-delivery losses by region](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#The-task-Late-delivery-losses-by-region)

[Fix it in stages](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Fix-it-in-stages)

[Pagination: State the contract first](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Pagination-State-the-contract-first)

[Practice 1: Fix the query](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-1-Fix-the-query)

[Practice 2: Total per category across pages](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Practice-2-Total-per-category-across-pages)

[Recap](https://www.educative.io/courses/forward-deployed-engineer/sql-and-api-tasks-queries-pagination-and-aggregation#Recap)