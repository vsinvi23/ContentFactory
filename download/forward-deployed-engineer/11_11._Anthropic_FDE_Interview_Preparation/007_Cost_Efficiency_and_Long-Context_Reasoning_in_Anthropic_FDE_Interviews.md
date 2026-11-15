# Cost_Efficiency_and_Long-Context_Reasoning_in_Anthropic_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Cost and Long-Context Reasoning on the Spot

Explore how to measure and control AI system costs and ensure reliable long-context reasoning for forward deployed engineering roles. Learn techniques like token counting, prompt caching, batching, and effort tuning that optimize performance and cost in Anthropic FDE interviews.

We'll cover the following...

- [Context windows and their limits](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Context-windows-and-their-limits)
- [Thinking and effort](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Thinking-and-effort)
- [Prompt caching and batching](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Prompt-caching-and-batching)
- [Estimating cost out loud](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Estimating-cost-out-loud)
- [Numbers that hold after launch](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Numbers-that-hold-after-launch)

Two questions come up in both the technical use-case screen and the final panel: “What does this cost at ten times the volume?” and “Will it stay reliable on long documents?” Interviewers want answers built from measured numbers. A candidate who says “it should be cheap” sounds like someone who has never sent a customer an invoice forecast.

The skill behind both answers is knowing which levers move cost and reliability on Claude and being able to measure each one. The examples use the expense-audit scenario with a realistic travel policy of about 5,000 tokens, the kind of long, unchanging document that sits in front of every request.

## Context windows and their limits[#](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Context-windows-and-their-limits)

A **context window** is everything a model can reference while it responds, including its own reply. All current Claude models, including Claude Sonnet 5.5 and Claude Opus 5.5, have a context window of 1 million tokens and can produce up to 128,000 output tokens in one response.

A larger window does not make every token equally useful. As a prompt grows, the model’s recall of details inside it degrades, an effect known as **context rot**. A rule buried in a very long prompt is more likely to be missed than the same rule in a short, focused one. Three habits keep long context reliable.

- **Put long documents first:** Long material goes before the question, so the request ends with what Claude needs to answer.
- **Retrieve instead of stuffing:** When a document set is much larger than any one question needs, retrieving the relevant parts beats sending everything.
- **Test at real size:** Evaluations use documents as long as the customer’s real ones, because short test cases hide context rot.

Each of these decisions starts with knowing how large a request actually is. The policy below is the shared document for every example in this lesson, saved as `travel_policy.py`.

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

10

11

12

13

14

15

16

17

18

19

20

RULES = """TRAVEL AND EXPENSE POLICY, Harbor Manufacturing, effective 2026-01-01

1. Receipts. Every expense over 25 USD needs an itemized receipt.

2. Submission. Employees submit receipts within 30 days of the expense date.

3. Meals. Meals are reimbursed up to the daily meal rate for the city in the schedule below.

4. Lodging. Lodging is reimbursed up to the nightly lodging rate for the city in the schedule below.

5. Airfare. Economy class only, up to 2,500 USD per round trip. Business class needs VP approval.

6. Alcohol. Alcohol is not reimbursed.

7. Exceptions. Any amount above a limit needs written approval from the employee's manager."""

CITIES = ["Boston", "Chicago", "Denver", "Austin", "Seattle", "Atlanta", "Phoenix", "Miami"]

# A long per-city rate schedule makes the policy realistic in size, about 5,000 tokens.

SCHEDULE = [

f"Rate {i + 1}: {CITIES[i % 8]} zone {i // 8 + 1}, meals {40 + (i % 9) \* 5} USD per day, "

f"lodging {150 + (i % 13) \* 15} USD per night"

for i in range(150)

]

POLICY = RULES + "\n\nRATE SCHEDULE\n" + "\n".join(SCHEDULE)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Building a realistic travel and expense policy of about 5,000 tokens for the cost examples

- **Lines 1–8:** We wrote seven policy rules covering receipts, submission, meals, lodging, airfare, alcohol, and exceptions.
- **Lines 13–17:** We generated 150 rate lines, each with a city zone, a daily meal rate, and a nightly lodging rate.
- **Line 19:** We joined the rules and the rate schedule into one `POLICY` string that the other programs import.

The next program measures how many tokens one audit request uses before sending anything to the model.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import anthropic

from travel_policy import POLICY

client = anthropic.Anthropic(api_key="{{ANTHROPIC_API_KEY}}")

MODEL = "claude-sonnet-5-5"

INPUT_PRICE_PER_MILLION = 2.00  # Claude Sonnet 5.5 base input price in USD

SYSTEM = "You audit expense reports against this policy.\n\n" + POLICY

REPORT = "Report EXP-4001. Lodging in Denver zone 3, 260 USD for one night, receipt attached."

# Count the tokens a request would use without sending it to the model.

count = client.messages.count_tokens(model=MODEL, system=SYSTEM, messages=[{"role": "user", "content": REPORT}])

print("Input tokens per report:", count.input_tokens)

print(f"Input cost per report: ${count.input_tokens * INPUT_PRICE_PER_MILLION / 1_000_000:.4f}")
```

⋯

Counting the input tokens of one expense audit request with count\_tokens

- **Lines 6–7:** We set the model and the Sonnet 5.5 base input price to $2 per million tokens.
- **Lines 9–10:** We built the system prompt from the policy and wrote one expense report as the user message.
- **Line 13:** We called `count_tokens`, which returns the input size of a request without running the model.
- **Lines 15–16:** We printed the token count and the input cost of one report.

Here is what the count returned.

Ace Editor

1

2

3

Input tokens per report: 5689

Input cost per report: $0.0114

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Almost all of those 5,689 tokens are the policy, and the report itself is only a few dozen. That ratio already points to where the savings are. Before getting to savings, though, cost also depends on how much Claude thinks.

## Thinking and effort[#](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Thinking-and-effort)

Current Claude models reason before they answer. With **adaptive thinking**, the model decides how much to think based on the request, and thinking tokens are billed as output tokens. The main control over that reasoning is effort, set with `output_config={"effort": ...}`. Its levels are `low`, `medium`, `high`, `xhigh`, and `max`. Claude Sonnet 5.5 defaults to `high`, and Claude Opus 5.5 defaults to `medium`.

Higher effort means more thinking, more output tokens, and slower responses. Effort works as a signal rather than a strict budget, so the model still reasons through hard problems at low effort.

In the code below, we ask a multi-step reimbursement question at two effort levels and compare the output tokens.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import anthropic

from travel_policy import POLICY

client = anthropic.Anthropic(api_key="{{ANTHROPIC_API_KEY}}")

SYSTEM = "You audit expense reports against this policy. End with the total reimbursable amount in one line.\n\n" + POLICY

REPORT = (

"Trip report EXP-4100, Denver zone 3, three days. Lodging 260 USD per night for 3 nights. "

"Meals 70, 52, and 61 USD. One dinner of 61 USD includes 18 USD of wine. All receipts attached. "

"How much is reimbursable without manager approval?"

)

for effort in ["low", "high"]:

response = client.messages.create(

model="claude-sonnet-5-5",

max_tokens=4096,

system=SYSTEM,

messages=[{"role": "user", "content": REPORT}],

output_config={"effort": effort},

)

answer = "".join(block.text for block in response.content if block.type == "text")

# Print only the answer's last line, which states the total.

print(f"Effort {effort}: {response.usage.output_tokens} output tokens | {answer.strip().splitlines()[-1]}")
```

⋯

Comparing low and high effort on a multi-step expense reimbursement question

- **Lines 7–12:** We wrote a trip report with lodging over its limit, meals over the daily rate, and wine that policy excludes.
- **Lines 14–21:** We sent the same request twice, once with `low` effort and once with `high`.
- **Lines 22–24:** We printed the output tokens for each run with the last line of the answer, which states the total.

The two runs produced the following.

Ace Editor

1

2

3

Effort low: 626 output tokens | \*\*Total reimbursable without manager approval: 795 USD\*\*

Effort high: 899 output tokens | \*\*Total reimbursable without manager approval: 795 USD\*\*

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Both runs found the correct total of $795, made up of $675 for lodging at the $225 nightly rate and $120 for meals at the $40 daily rate. High effort used about 45 percent more output tokens for the same answer. For this task, low effort is the cheaper choice. A harder task might need the higher level, which is why effort is set with an evaluation set rather than by guesswork.

Effort shapes output cost. The bigger lever for this workload is on the input side.

## Prompt caching and batching[#](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Prompt-caching-and-batching)

**Prompt caching** stores a repeated prefix of a request, such as a long system prompt, so later requests can reuse it at a much lower price. We mark the end of the reusable part with `cache_control`. The first request writes the cache, and requests within the next five minutes read from it and refresh it. A prompt must be at least 286 tokens long to cache on Claude Sonnet 5.5.

The **Message Batches API** is the second lever. It processes many requests asynchronously at half the standard price, which suits work that can wait, such as an overnight audit of the days reports.

The table below lists the Claude Sonnet 5.5 prices that drive both levers, in US dollars per million tokens.

|  |  |  |
| --- | --- | --- |
| **Price category** | **Standard** | **Batch API** |
| Base input | 2.00 | 1.00 |
| Cache write, 5-minute lifetime | 2.50 | Not applicable |
| Cache write, 1-hour lifetime | 4.00 | Not applicable |
| Cache read | 0.10 | Not applicable |
| Output | 10.00 | 5.00 |

Let’s mark the policy as cacheable and audit two reports in a row:

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import anthropic

from travel_policy import POLICY

client = anthropic.Anthropic(api_key="{{ANTHROPIC_API_KEY}}")

# Mark the long policy, which repeats on every request, as cacheable.

SYSTEM = [

{

"type": "text",

"text": "You audit expense reports against this policy. Answer in one sentence.\n\n" + POLICY,

"cache_control": {"type": "ephemeral"},

}

]

REPORTS = [

"Report EXP-4001. Lodging in Denver zone 3, 260 USD for one night, receipt attached. Within policy?",

"Report EXP-4002. Meals in Boston zone 1, 38 USD for one day, receipt attached. Within policy?",

]

for report in REPORTS:

response = client.messages.create(

model="claude-sonnet-5-5", max_tokens=512, system=SYSTEM, messages=[{"role": "user", "content": report}]

)

usage = response.usage

# Claude Sonnet 5.5 prices per million tokens. Input 2.00, cache write 2.50, cache read 0.10, output 10.00.

cost = (

usage.input_tokens * 2.00

+ usage.cache_creation_input_tokens * 2.50

+ usage.cache_read_input_tokens * 0.10

+ usage.output_tokens * 10.00

) / 1_000_000

print(report.split(".")[0])

print(f"  Cache write: {usage.cache_creation_input_tokens}, cache read: {usage.cache_read_input_tokens}, "

f"uncached input: {usage.input_tokens}, output: {usage.output_tokens}, cost: ${cost:.4f}")
```

⋯

Caching the travel policy and measuring a cache write followed by a cache read

- **Lines 814:** We sent the system prompt as a content block with `cache_control`, which marks the whole policy as reusable.
- **Lines 1619:** We wrote two different reports that share the same policy.
- **Lines 2125:** We sent each report and read its `usage` field.
- **Lines 2732:** We priced each call from the four usage counts, using the Sonnet 5.5 prices.
- **Lines 3335:** We printed the cache write, cache read, uncached input, output, and cost for each report.

The usage numbers below show the cache at work:

Ace Editor

1

2

3

4

5

Report EXP-4001

Cache write: 5655, cache read: 0, uncached input: 48, output: 87, cost: $0.0151

Report EXP-4002

Cache write: 0, cache read: 5655, uncached input: 47, output: 94, cost: $0.0016

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The first report paid to write the policy into the cache. The second read the same 5,655 tokens from the cache and cost about a tenth as much. In production, the cache is rewritten only when it expires, so almost every report pays the cache-read price.

Each lever now has a measured effect. An interviewer wants to hear them combined into one number.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27581.0000000000001%27%20height=%27221%27/%3e)![The four levers that move a Claude system’s cost](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The four levers that move a Claude system’s cost")

The four levers that move a Claude system’s cost

## Estimating cost out loud[#](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Estimating-cost-out-loud)

A cost estimate in an interview follows three steps.

1. **Measure tokens:** Count the input and output of one realistic request, splitting the repeated part from the part that changes.
2. **Apply prices:** Price each part at its rate under each option, such as standard, cached, or batched.
3. **Multiply by volume:** Scale the per-request cost to the customers daily volume.

The program below turns those steps into a forecast for 500 and 5,000 reports a day.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import anthropic

from travel_policy import POLICY

client = anthropic.Anthropic(api_key="{{ANTHROPIC_API_KEY}}")

MODEL = "claude-sonnet-5-5"

SYSTEM = "You audit expense reports against this policy. Answer in one sentence.\n\n" + POLICY

REPORT = "Report EXP-4001. Lodging in Denver zone 3, 260 USD for one night, receipt attached. Within policy?"

# Claude Sonnet 5.5 prices in USD per million tokens.

PRICE = {"input": 2.00, "cache_write": 2.50, "cache_read": 0.10, "output": 10.00, "batch_input": 1.00, "batch_output": 5.00}

# Step 1. Measure real token counts. The policy is counted alone, with a one-character placeholder message.

policy_tokens = client.messages.count_tokens(model=MODEL, system=SYSTEM, messages=[{"role": "user", "content": "x"}]).input_tokens

response = client.messages.create(model=MODEL, max_tokens=512, system=SYSTEM, messages=[{"role": "user", "content": REPORT}])

input_tokens = response.usage.input_tokens

output_tokens = response.usage.output_tokens

report_tokens = input_tokens - policy_tokens

def per_report(policy_price: float, input_price: float, output_price: float) -> float:

"""Cost of one report, given the price paid for the policy tokens, the report tokens, and the output."""

return (policy_tokens * policy_price + report_tokens * input_price + output_tokens * output_price) / 1_000_000

# Step 2. Price one report under each option. Cached requests pay the cache read price for the policy.

options = {

"No caching": per_report(PRICE["input"], PRICE["input"], PRICE["output"]),

"With caching": per_report(PRICE["cache_read"], PRICE["input"], PRICE["output"]),

"Batch API, no caching": per_report(PRICE["batch_input"], PRICE["batch_input"], PRICE["batch_output"]),

}

# Step 3. Multiply by volume.

print(f"Measured tokens per report. Input {input_tokens}, output {output_tokens}")

for name, cost in options.items():

print(f"{name:<22} ${cost:.4f} per report | ${cost * 500:,.2f} per day at 500 | ${cost * 5000:,.2f} per day at 5,000")
```

⋯

Estimating the daily cost of the expense audit agent with and without caching and batching

- **Line 11:** We stored the Sonnet 5.5 prices, including the batch rates.
- **Lines 13–18:** We counted the policy alone, ran one real request, and split its input into policy tokens and report tokens.
- **Lines 21–23:** We wrote `per_report`, which prices the policy, the report, and the output separately.
- **Lines 27–31:** We priced one report three ways. The cached option pays the cache read price for the policy, and the batch option pays half price for everything.
- **Lines 34–36:** We printed the measured tokens and the per-report and daily cost of each option.

Running the estimate gives the forecast below.

Ace Editor

1

2

3

4

5

Measured tokens per report. Input 5703, output 85

No caching $0.0123 per report | $6.13 per day at 500 | $61.28 per day at 5,000

With caching $0.0015 per report | $0.75 per day at 500 | $7.49 per day at 5,000

Batch API, no caching $0.0061 per report | $3.06 per day at 500 | $30.64 per day at 5,000

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The cached figures leave out the occasional cache write, which happens each time the cache expires and adds little at steady volume. With those numbers, the spoken answer is short and specific.

Each report sends about 5,700 input tokens, and almost all of them are the policy. Without caching, that is about 61 dollars a day at 5,000 reports. Caching the policy cuts it to about 7.50 a day because cache reads cost a twentieth of base input. If the audit can run overnight, the Batch API halves the uncached price instead. If the customer requires US-only inference, Id add 10 percent, since `inference_geo` set to `"us"` costs 1.1 times the standard rate.

The answer names the measurement, the dominant cost, the lever that moves it, and the condition that changes it.

## Numbers that hold after launch[#](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Numbers-that-hold-after-launch)

Cost surprises in production usually trace back to an estimate made on short test prompts. A strong candidate measures tokens at real document sizes, caches the content that repeats, sets effort with evidence, and keeps context focused. Those same habits protect reliability because a focused context is both cheaper to send and easier for the model to use well. In an interview, a forecast built this way shows the customer-facing judgment the FDE role depends on.

Packaging and Hosting: Agent Skills and Managed Agents

Building Eval Sets That Prove a Claude System Works

Ask

[Context windows and their limits](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Context-windows-and-their-limits)

[Thinking and effort](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Thinking-and-effort)

[Prompt caching and batching](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Prompt-caching-and-batching)

[Estimating cost out loud](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Estimating-cost-out-loud)

[Numbers that hold after launch](https://www.educative.io/courses/forward-deployed-engineer/cost-and-long-context-reasoning-on-the-spot#Numbers-that-hold-after-launch)