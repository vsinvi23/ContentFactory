# Practice_Multi-Level_Coding_for_Anthropic_FDE_Interview

Source: https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Multi-Level Coding Round Practice

Explore how to tackle Anthropic's Forward Deployed Engineer coding round by practicing small, practical systems that grow across four levels. Learn to build flexible code incrementally, passing tests at each level while managing complexity like token limits and rolling time windows. Develop strategies to maximize efficiency during a timed assessment and understand the coding patterns favored in this interview format.

We'll cover the following...

- [How the round works](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#How-the-round-works)
- [Problems the round uses](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Problems-the-round-uses)
- [Practicing with a token limiter](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Practicing-with-a-token-limiter)
  - [Tracking token usage per client](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Tracking-token-usage-per-client)
  - [Ranking the heaviest clients](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Ranking-the-heaviest-clients)
  - [Adding a token budget per client](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Adding-a-token-budget-per-client)
  - [Applying budgets to rolling time windows](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Applying-budgets-to-rolling-time-windows)
- [Strategy under the clock](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Strategy-under-the-clock)
- [Code that grows without breaking](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Code-that-grows-without-breaking)

The coding round in Anthropics FDE loop gives a candidate one problem that grows. Each level adds requirements to the code from the level before, and the next level opens only after every test on the current one passes. Algorithm puzzles rarely appear. The problems are small, practical systems, such as a key-value store, a banking ledger, or a rate limiter.

That format rewards one skill above the rest. A candidate whose first version is rigid spends the later levels rewriting it. A candidate whose first version is plain and open spends them adding small methods. The practice problem below builds that habit across four levels.

## How the round works[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#How-the-round-works)

**CodeSignal** is an online platform that companies use to run timed coding assessments in a browser-based editor. Its **Industry Coding Framework** is a format where one project grows across four levels, each adding new methods and requirements. Anthropics round most often runs as a timed CodeSignal assessment in this format. Some teams run a live version instead, in a shared editor with an interviewer watching. The rules below hold for the timed assessment, and the format can vary by team, so the recruiter is the best source for the exact setup.

- **One problem, four levels:** The whole round is a single project, and later levels are harder and worth more points.
- **About 90 minutes:** The clock covers all four levels, and many candidates run out of time on level 4.
- **Tests unlock levels:** Each levels unit tests are visible, and the next level opens only after all of them pass.
- **Earlier methods keep working:** New levels add methods and change rules, and every earlier test still has to pass.
- **Python standard library:** Solutions use plain Python, with no outside packages.
- **Scored from 200 to 600:** A score around 520 or higher usually moves a candidate forward.
- **Code is reviewed:** Submissions are checked for hardcoded outputs and branches written only to pass a specific test.

The rules explain the format. The problems themselves show what the levels actually ask for.

## Problems the round uses[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Problems-the-round-uses)

The domain changes from one problem to the next, and the growth pattern stays similar. Level 1 asks for a small core interface. Middle levels add queries, rankings, or business rules. The final levels add time, history, or persistence, which is where most candidates slow down. The table below shows how several typical problems grow.

|  |  |  |
| --- | --- | --- |
| **Problem** | **Early Levels** | **Later Levels** |
| In-memory key-value store | Set, get, and delete records, then scan by prefix | Records that expire after a time to live, then backup and restore |
| Banking system | Create accounts, deposit, and transfer | Rank top spenders, then scheduled payments and account merges |
| Worker time tracker | Register entry and exit times, then total time worked | Promotions that take effect on the next entry, then salary over a period |
| Least recently used (LRU) cache | Get and put with a size limit | New constraints added at each level |
| Token budget or rate limiter | Track usage per client | Budgets, rankings, and rolling time windows |

Two patterns stand out across these problems. Time appears in almost every one, usually as a timestamp passed into each method call. And the hardest levels change a rule that earlier code depends on, such as how a balance or a budget is counted. Code that keeps each rule in one place absorbs those changes with a small edit.

The practice problem uses the last row, a token limiter, because it sits close to the systems an FDE builds around Claude.

## Practicing with a token limiter[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Practicing-with-a-token-limiter)

The task is a limiter that tracks how many tokens each client sends to a model, and we build it one level at a time.

### Tracking token usage per client[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Tracking-token-usage-per-client)

Suppose level 1 asks us to register clients, record each request a client sends, and report a clients total tokens. Every request arrives with a timestamp. To solve this, we create a `TokenLimiter` class in `token_limiter.py` with three methods. `add_client` registers a client, `record` stores a request along with its timestamp, and `usage` adds up a clients tokens. Nothing uses the timestamp yet, and we keep it anyway because storing it costs one tuple. The code for this first version is given below.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
class TokenLimiter:

"""Tracks how many tokens each client sends to a model."""

def __init__(self):

self.requests = {}  # client ID -> list of (timestamp, tokens)

def add_client(self, client_id):

"""Register a client. Return False if it already exists."""

if client_id in self.requests:

return False

self.requests[client_id] = []

return True

def record(self, timestamp, client_id, tokens):

"""Record one request. Return False for an unknown client or a token count below 1."""

if client_id not in self.requests or tokens < 1:

return False

self.requests[client_id].append((timestamp, tokens))

return True

def usage(self, client_id):

"""Return a client's total tokens, or None for an unknown client."""

if client_id not in self.requests:

return None

return sum(tokens for _, tokens in self.requests[client_id])

def check(name, actual, expected):

print(f"{'PASS' if actual == expected else 'FAIL'}  {name}")

if __name__ == "__main__":

limiter = TokenLimiter()

# Level 1 tests

check("add a client", limiter.add_client("a"), True)

check("reject a duplicate client", limiter.add_client("a"), False)

check("reject an unknown client", limiter.record(1, "z", 50), False)

check("record two requests", [limiter.record(1, "a", 100), limiter.record(2, "a", 200)], [True, True])

check("total usage", limiter.usage("a"), 300)
```

⋯

Building version 1 of the token limiter with client registration, request recording, and total usage

- **Lines 4:** We stored every clients requests in one dictionary, as a list of `(timestamp, tokens)` pairs.
- **Lines 7–12:** We wrote `add_client`, which returns `False` for a client that already exists.
- **Lines 14–19:** We wrote `record`, which rejects an unknown client or a token count below 1, and keeps the timestamp with each request.
- **Lines 21–25:** We wrote `usage`, which adds up a clients tokens and returns `None` for an unknown client.
- **Lines 28–29:** We wrote `check`, which prints PASS or FAIL for each test.
- **Lines 32–39:** We ran the level 1 tests inside `if __name__ == "__main__":`, which runs them only when we run this file directly.

The tests give the following result:

Ace Editor

1

2

3

4

5

6

PASS add a client

PASS reject a duplicate client

PASS reject an unknown client

PASS record two requests

PASS total usage

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

All five tests pass. The design is one dictionary and four short methods, which leaves plenty of room to grow.

### Ranking the heaviest clients[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Ranking-the-heaviest-clients)

Once level 1 passes, level 2 wants the heaviest clients, formatted as `"id(tokens)"`, with ties broken by client ID. Formats and tie rules like this one come up often, and the tests check them character by character. A single new method covers it. We add `top_clients`, which sorts clients by usage and returns the first `n` in the required format. Here’s the updated file:

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
class TokenLimiter:

"""Tracks how many tokens each client sends to a model."""

def __init__(self):

self.requests = {}  # client ID -> list of (timestamp, tokens)

def add_client(self, client_id):

"""Register a client. Return False if it already exists."""

if client_id in self.requests:

return False

self.requests[client_id] = []

return True

def record(self, timestamp, client_id, tokens):

"""Record one request. Return False for an unknown client or a token count below 1."""

if client_id not in self.requests or tokens < 1:

return False

self.requests[client_id].append((timestamp, tokens))

return True

def usage(self, client_id):

"""Return a client's total tokens, or None for an unknown client."""

if client_id not in self.requests:

return None

return sum(tokens for _, tokens in self.requests[client_id])

# Level 2

def top_clients(self, n):

"""Return the n heaviest clients as "id(tokens)", highest first, ties broken by ID."""

ranked = sorted(self.requests, key=lambda client_id: (-self.usage(client_id), client_id))

return [f"{client_id}({self.usage(client_id)})" for client_id in ranked[:n]]

def check(name, actual, expected):

print(f"{'PASS' if actual == expected else 'FAIL'}  {name}")

if __name__ == "__main__":

limiter = TokenLimiter()

# Level 1 tests

check("add a client", limiter.add_client("a"), True)

check("reject a duplicate client", limiter.add_client("a"), False)

check("reject an unknown client", limiter.record(1, "z", 50), False)

check("record two requests", [limiter.record(1, "a", 100), limiter.record(2, "a", 200)], [True, True])

check("total usage", limiter.usage("a"), 300)

# Level 2 tests

limiter.add_client("b")

limiter.add_client("c")

limiter.record(3, "b", 500)

limiter.record(4, "c", 300)

check("top two clients", limiter.top_clients(2), ["b(500)", "a(300)"])

check("tie broken by ID", limiter.top_clients(3), ["b(500)", "a(300)", "c(300)"])
```

⋯

Extending the token limiter with a ranking of the heaviest clients

- **Lines 27–40:** We wrote `top_clients`, which sorts clients by usage from highest to lowest, breaks ties by ID, and formats the first `n`. Sorting by the pair `(-usage, id)` handles both rules in one key.
- **Lines 47–53:** We added two clients and tested the ranking, including a tie.

The end of the output shows the new tests:

Ace Editor

1

2

3

4

PASS total usage

PASS top two clients

PASS tie broken by ID

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The level 1 tests still pass, and no level 1 code changed. The method reuses `usage` instead of recounting tokens, so there is still one place that defines a client’s total.

### Adding a token budget per client[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Adding-a-token-budget-per-client)

Level 3 raises the stakes with a token budget per client. Any request that would push a client over its budget must be rejected and left out of the history. The quick fix is to put the budget math straight into `record`. We take a slightly longer route. A `set_budget` method stores each budget, and a small `used` method returns the tokens that count against it. For now, `used` simply returns total usage. Its job is to give the counting rule a single home, and `record` asks it before storing anything. With that in place, the file looks like this.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
class TokenLimiter:

"""Tracks how many tokens each client sends to a model."""

def __init__(self):

self.requests = {}  # client ID -> list of (timestamp, tokens)

self.budgets = {}  # Level 3: client ID -> maximum tokens

def add_client(self, client_id):

"""Register a client. Return False if it already exists."""

if client_id in self.requests:

return False

self.requests[client_id] = []

return True

def record(self, timestamp, client_id, tokens):

"""Record one request. Return False for an unknown client or a token count below 1."""

if client_id not in self.requests or tokens < 1:

return False

if self.used(timestamp, client_id) + tokens > self.budgets.get(client_id, float("inf")):

return False  # Level 3: the request would go over budget

self.requests[client_id].append((timestamp, tokens))

return True

def usage(self, client_id):

"""Return a client's total tokens, or None for an unknown client."""

if client_id not in self.requests:

return None

return sum(tokens for _, tokens in self.requests[client_id])

# Level 2

def top_clients(self, n):

"""Return the n heaviest clients as "id(tokens)", highest first, ties broken by ID."""

ranked = sorted(self.requests, key=lambda client_id: (-self.usage(client_id), client_id))

return [f"{client_id}({self.usage(client_id)})" for client_id in ranked[:n]]

# Level 3

def set_budget(self, client_id, max_tokens):

"""Set a client's token budget. Return False for an unknown client."""

if client_id not in self.requests:

return False

self.budgets[client_id] = max_tokens

return True

def used(self, timestamp, client_id):

"""Return the tokens that count against a client's budget."""

return self.usage(client_id)

def check(name, actual, expected):

print(f"{'PASS' if actual == expected else 'FAIL'}  {name}")

if __name__ == "__main__":

limiter = TokenLimiter()

# Level 1 tests

check("add a client", limiter.add_client("a"), True)

check("reject a duplicate client", limiter.add_client("a"), False)

check("reject an unknown client", limiter.record(1, "z", 50), False)

check("record two requests", [limiter.record(1, "a", 100), limiter.record(2, "a", 200)], [True, True])

check("total usage", limiter.usage("a"), 300)

# Level 2 tests

limiter.add_client("b")

limiter.add_client("c")

limiter.record(3, "b", 500)

limiter.record(4, "c", 300)

check("top two clients", limiter.top_clients(2), ["b(500)", "a(300)"])

check("tie broken by ID", limiter.top_clients(3), ["b(500)", "a(300)", "c(300)"])

# Level 3 tests

check("set a budget", limiter.set_budget("a", 400), True)

check("allow a request that fits", limiter.record(5, "a", 100), True)

check("reject a request over budget", limiter.record(6, "a", 1), False)

check("rejected request not counted", limiter.usage("a"), 400)
```

⋯

Extending the token limiter with per-client budgets that reject requests over the limit

- **Line 6:** We added a `budgets` dictionary that maps each client to its maximum tokens.
- **Lines 19–20:** We made `record` reject a request when the tokens already used plus the new request exceed the budget. A client with no budget gets infinity, so it is never rejected.
- **Lines 37–42:** We wrote `set_budget`, which returns `False` for an unknown client.
- **Lines 44–46:** We wrote `used`, which returns the tokens that count against the budget. It returns total usage at this level.
- **Lines 70–74:** We set a budget of 400 for client `a`, then tested a request that fits, one that goes over, and that the rejected request was not counted.

Running the file ends with these lines:

Ace Editor

1

2

3

4

5

6

PASS tie broken by ID

PASS set a budget

PASS allow a request that fits

PASS reject a request over budget

PASS rejected request not counted

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The budget works, and every earlier test still passes. The `used` method looks unnecessary for now, and the next level shows why it earns its place.

### Applying budgets to rolling time windows[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Applying-budgets-to-rolling-time-windows)

Finally, level 4 rewrites the budget rule itself. A budget now covers a rolling window, such as 60 seconds, and only requests inside that window count. In rigid code, a change like this means starting over. Our version already keeps a timestamp on every request, and only `used` knows how tokens are counted. So the fix is small. We give the class an optional `window` setting and teach `used` to skip requests older than the window. The code below shows the change.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
class TokenLimiter:

"""Tracks how many tokens each client sends to a model."""

def __init__(self, window=None):

self.window = window  # Level 4: budget window in seconds, or None for no window

self.requests = {}  # client ID -> list of (timestamp, tokens)

self.budgets = {}  # Level 3: client ID -> maximum tokens

def add_client(self, client_id):

"""Register a client. Return False if it already exists."""

if client_id in self.requests:

return False

self.requests[client_id] = []

return True

def record(self, timestamp, client_id, tokens):

"""Record one request. Return False for an unknown client or a token count below 1."""

if client_id not in self.requests or tokens < 1:

return False

if self.used(timestamp, client_id) + tokens > self.budgets.get(client_id, float("inf")):

return False  # Level 3: the request would go over budget

self.requests[client_id].append((timestamp, tokens))

return True

def usage(self, client_id):

"""Return a client's total tokens, or None for an unknown client."""

if client_id not in self.requests:

return None

return sum(tokens for _, tokens in self.requests[client_id])

# Level 2

def top_clients(self, n):

"""Return the n heaviest clients as "id(tokens)", highest first, ties broken by ID."""

ranked = sorted(self.requests, key=lambda client_id: (-self.usage(client_id), client_id))

return [f"{client_id}({self.usage(client_id)})" for client_id in ranked[:n]]

# Level 3

def set_budget(self, client_id, max_tokens):

"""Set a client's token budget. Return False for an unknown client."""

if client_id not in self.requests:

return False

self.budgets[client_id] = max_tokens

return True

def used(self, timestamp, client_id):

"""Return the tokens that count against a client's budget."""

if self.window is None:

return self.usage(client_id)

# Level 4: only requests inside the window count

return sum(tokens for ts, tokens in self.requests[client_id] if ts > timestamp - self.window)

def check(name, actual, expected):

print(f"{'PASS' if actual == expected else 'FAIL'}  {name}")

if __name__ == "__main__":

limiter = TokenLimiter()

# Level 1 tests

check("add a client", limiter.add_client("a"), True)

check("reject a duplicate client", limiter.add_client("a"), False)

check("reject an unknown client", limiter.record(1, "z", 50), False)

check("record two requests", [limiter.record(1, "a", 100), limiter.record(2, "a", 200)], [True, True])

check("total usage", limiter.usage("a"), 300)

# Level 2 tests

limiter.add_client("b")

limiter.add_client("c")

limiter.record(3, "b", 500)

limiter.record(4, "c", 300)

check("top two clients", limiter.top_clients(2), ["b(500)", "a(300)"])

check("tie broken by ID", limiter.top_clients(3), ["b(500)", "a(300)", "c(300)"])

# Level 3 tests

check("set a budget", limiter.set_budget("a", 400), True)

check("allow a request that fits", limiter.record(5, "a", 100), True)

check("reject a request over budget", limiter.record(6, "a", 1), False)

check("rejected request not counted", limiter.usage("a"), 400)

# Level 4 tests

windowed = TokenLimiter(window=60)

windowed.add_client("a")

windowed.set_budget("a", 100)

check("allow within budget", windowed.record(0, "a", 80), True)

check("reject inside the window", windowed.record(30, "a", 30), False)

check("allow once old tokens leave", windowed.record(61, "a", 30), True)

check("earlier levels unchanged", limiter.top_clients(1), ["b(500)"])
```

⋯

Extending the token limiter so budgets apply to a rolling time window

- **Lines 4–5:** We added an optional `window` in seconds. The default of `None` keeps the earlier behavior, so all earlier tests still pass.
- **Lines 47–50:** We changed `used` to count only requests newer than the start of the window when a window is set.
- **Lines 80–83:** We created a limiter with a 60-second window and a budget of 100 tokens.
- **Lines 84–86:** We tested a request that fits, a request rejected inside the window, and a request allowed once the first one left the window.
- **Line 87:** We confirmed the original limiter still ranks clients as before.

The final run ends with the following:

Ace Editor

1

2

3

4

5

6

PASS rejected request not counted

PASS allow within budget

PASS reject inside the window

PASS allow once old tokens leave

PASS earlier levels unchanged

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

All fifteen tests pass. The hardest level took a constructor argument and three lines in `used`, because two small choices made earlier held up. Level 1 stored timestamps before anything needed them, and level 3 gave the counting rule a single home.

The code is only half of a strong round. The other half is how we spend the 90 minutes.

## Strategy under the clock[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Strategy-under-the-clock)

A few habits decide most results in this round.

- **Read every visible test first:** The tests define the exact method names, return values, and output formats, and they often hint at what the next level will need.
- **Spend real time on level 1:** About 10 to 15 minutes on a clean level 1 saves far more time across levels 3 and 4.
- **Run the tests after every change:** A broken earlier level blocks everything after it, so catching it in seconds matters.
- **Keep each rule in one place:** When a later level changes a rule, one method changes instead of five.
- **Write real logic, never test-specific branches:** Hardcoded outputs are flagged in review, and they break at the next level anyway.
- **Talk through choices in the live version:** A sentence such as “I’m storing the timestamp now because time usually shows up later” lets the interviewer see the design reasoning.

When time runs out mid-level, a short comment naming what is unfinished and how it would work shows a plan, which reads better than silent, half-written code.

## Code that grows without breaking[#](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Code-that-grows-without-breaking)

The multi-level round looks like a speed test and works more like a design test. The domain changes every time, and the shape stays the same, with a small core, then new rules, then time. Plain data structures, timestamps kept from the start, and each rule in a single method let every level land as a small addition. A candidate who practices that shape on a few problems walks into the round ready for whichever one appears.

The Technical Use Case Screen Walk-Through

The Final Panel Solution Design Walk-Through

Ask

[How the round works](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#How-the-round-works)

[Problems the round uses](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Problems-the-round-uses)

[Practicing with a token limiter](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Practicing-with-a-token-limiter)

[Tracking token usage per client](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Tracking-token-usage-per-client)

[Ranking the heaviest clients](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Ranking-the-heaviest-clients)

[Adding a token budget per client](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Adding-a-token-budget-per-client)

[Applying budgets to rolling time windows](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Applying-budgets-to-rolling-time-windows)

[Strategy under the clock](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Strategy-under-the-clock)

[Code that grows without breaking](https://www.educative.io/courses/forward-deployed-engineer/multi-level-coding-round-practice#Code-that-grows-without-breaking)