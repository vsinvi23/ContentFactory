# Reward_Generation_and_Evaluation_Loop_in_AI_Agent_Design

Source: https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Reward Generation and Evaluation Loop

Explore the process of implementing a Eureka-like reward learning system for AI agents. Learn to generate multiple reward candidate codes via LLMs, evaluate and validate them safely, and train policies to measure reward effectiveness. By completing this lesson, you will understand how to turn reward ideas into actionable evidence and prepare for iterative improvements in agentic systems.

We'll cover the following...

- [Implementing reward generation](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-reward-generation)
  - [Setting up the OpenAI client and prompt constants](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Setting-up-the-OpenAI-client-and-prompt-constants)
  - [Building the reward generation prompt](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Building-the-reward-generation-prompt)
    - [Prompt mode: Improving an existing best reward](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-Improving-an-existing-best-reward)
    - [Prompt mode: First-iteration exploration](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-First-iteration-exploration)
    - [Enforcing a strict output contract](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Enforcing-a-strict-output-contract)
  - [Implementing the RewardDesigner agent](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-the-RewardDesigner-agent)
    - [Reading iteration context from shared state](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Reading-iteration-context-from-shared-state)
    - [Collecting task spec and environment code](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Collecting-task-spec-and-environment-code)
    - [Including feedback only when available](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Including-feedback-only-when-available)
  - [Calling the LLM reliably (with retries)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Calling-the-LLM-reliably-with-retries)
  - [Storing reward candidates for the evaluator](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Storing-reward-candidates-for-the-evaluator)
- [Implementing candidate evaluation](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-candidate-evaluation)
  - [Imports: Tools that do the heavy lifting](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Imports-Tools-that-do-the-heavy-lifting)
  - [CandidateEvaluatorAgent entry point: Reading iteration context](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#CandidateEvaluatorAgent-entry-point-Reading-iteration-context)
  - [Parsing candidates from LLM output (robustly)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Parsing-candidates-from-LLM-output-robustly)
  - [Fail safely when parsing produces nothing](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Fail-safely-when-parsing-produces-nothing)
  - [Per-candidate evaluation loop: Save code first, then try to execute it](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Per-candidate-evaluation-loop-Save-code-first-then-try-to-execute-it)
  - [Compile and validate the reward code in a sandbox](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Compile-and-validate-the-reward-code-in-a-sandbox)
  - [Train and evaluate (delegated to tools/rl\_runner.py)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Train-and-evaluate-delegated-to-toolsrlrunnerpy)
  - [Save the rollout HTML (noncritical if it fails)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-the-rollout-HTML-noncritical-if-it-fails)
  - [Save metrics, training metadata, and policy params](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-metrics-training-metadata-and-policy-params)
  - [Record results and update the leaderboard](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Record-results-and-update-the-leaderboard)
  - [Handle per-candidate failures without stopping the iteration](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Handle-per-candidate-failures-without-stopping-the-iteration)
  - [Convert results into JSON and store them in shared state](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Convert-results-into-JSON-and-store-them-in-shared-state)
- [Summary](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Summary)

## Implementing reward generation[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-reward-generation)

Start with the first step in each loop iteration: reward generation. In this system, the RewardDesigner has a single job:

- It builds a prompt that includes the task spec, environment code, and feedback from the previous iteration.
- It calls an OpenAI model to generate K reward candidates.
- It stores the raw generated text in the shared state so the evaluator can parse it next.

Everything we do below supports that flow.

### Setting up the OpenAI client and prompt constants[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Setting-up-the-OpenAI-client-and-prompt-constants)

Let's start at the top of `agents/llm_agents.py`. Before defining the agent class, we set up the OpenAI client and a few constants that control output formatting.

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

import os

import json

from openai import OpenAI

from pydantic import PrivateAttr

from loguru import logger

from google.adk.agents import BaseAgent

from google.adk.agents.invocation\_context import InvocationContext

from google.adk.events import Event

from typing import AsyncGenerator

client = OpenAI(api\_key=os.environ.get("OPENAI\_API\_KEY"))

CANDIDATE\_DELIM = "### CANDIDATE ###"

DESIGNER\_SYSTEM = "You are a precise reward-function code generator for JAX/Brax environments."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Here's what we're doing (as implementers):

- We initialize `client` once at import time so the agent can reuse it for every iteration.
- `CANDIDATE_DELIM` is a parsing contract. The evaluator relies on this exact delimiter to split candidates.
- `DESIGNER_SYSTEM` narrows model behavior. We don't want explanations, Markdown, or tips. We want a reward code.

This is the first place where you see an important design pattern:

> We enforce reliability by making the LLM output machine-parseable, not human-friendly.

### Building the reward generation prompt[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Building-the-reward-generation-prompt)

Next, we define `_designer_prompt(...)`. This function is where we program the reward designer's behavior.

Ace Editor

1

2

3

4

5

6

7

def \_designer\_prompt(task\_spec, env\_code, best\_reward\_code, reflection, K, candidate\_results: str | None = None):

"""

Build the prompt for the Reward Designer.

From iteration 2 onward, we include an explicit "Query with Feedback" section

(policy training/eval results + reflection) similar to the Eureka paper diagram.

"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This function supports two modes:

- Iteration 1 (no best reward yet)generates initial candidates.
- Iteration 2+ (we have feedback), improve the best reward so far.

Let's look at how that branching is implemented.

#### Prompt mode: Improving an existing best reward[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-Improving-an-existing-best-reward)

If a best reward exists, we instruct the model to improve it (not start over).

Ace Editor

1

2

3

4

5

6

if best\_reward\_code:

improvement\_instruction = f"""IMPORTANT: You MUST generate {K} IMPROVED versions of the BEST REWARD SO FAR below.

- Each candidate should be a PROGRESSIVE IMPROVEMENT or VARIATION of the best reward

- Build upon the successful aspects identified in the feedback/reflection

- Try different approaches to address issues mentioned in the feedback/reflection

- Do NOT generate completely new rewards from scratch - they must be based on the best reward below"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is a key EUREKA-like design choice in this implementation:

- We treat the best reward as the current parent.
- We ask for variations, not resets.
- We keep improvement grounded in evidence (reflection + results).

Now, we embed the results and reflection as a structured feedback block.

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

feedback\_block = f"""

QUERY WITH FEEDBACK (from the last iteration):

We trained RL policies using reward functions. Here are the results for ALL candidates from the last iteration.

POLICY RESULTS (JSON) - Contains results for ALL candidates:

{candidate\_results if candidate\_results else "(No candidate\_results provided)"}

REFLECTION - Analysis of what worked, what failed, and HOW TO IMPROVE:

{reflection if reflection else "(No reflection available)"}

...

"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This mirrors the logic from the Eureka chapter:

- Candidate results = empirical signal
- Reflection = interpretation + targeted edits

#### Prompt mode: First-iteration exploration[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-First-iteration-exploration)

If there is no best reward yet, we generate initial candidates.

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

else:

improvement\_instruction = f"""Generate {K} initial reward candidates for this task.

- These are the first candidates, so explore different reward shaping approaches

- IMPORTANT: The task requires running fast WHILE staying stable - ensure your rewards balance both:

\* Forward velocity reward (for speed)

\* Stability/balance rewards (for maintaining upright posture, preventing falls)

\* Control smoothness (for energy efficiency)

- Do NOT over-prioritize speed at the expense of stability"""

feedback\_block = ""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is intentionally broad. Iteration one is about proposing different reward hypotheses.

#### Enforcing a strict output contract[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Enforcing-a-strict-output-contract)

Now, the most important part: the returned prompt includes strict format rules.

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

return f"""Return exactly {K} reward candidates.

{improvement\_instruction}

CRITICAL FORMAT RULES:

- Output MUST be plain Python ONLY (no markdown, no backticks, no commentary).

- Each candidate MUST start with: def compute\_reward(

- Separate candidates using EXACT delimiter line:

{CANDIDATE\_DELIM}

- No imports.

- Only use: jnp, jax, math.

- compute\_reward must return: (total\_reward, reward\_terms\_dict)

- reward\_terms\_dict must be a dict[str, jnp.ndarray] for each term.

- CRITICAL: Every compute\_reward function MUST end with: return total\_reward, reward\_terms

- NEVER return None or forget the return statement - this will cause validation to fail.

...

"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is how we shape the output so the evaluator can safely compile it later.

Notice how the rules are written like a validator, not like documentation. That’s intentional: we are designing for execution reliability, not readability.

### Implementing the RewardDesigner agent[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-the-RewardDesigner-agent)

Now we reach the executable agent: `RewardDesignerOpenAIAgent`.

Ace Editor

1

2

3

4

5

6

class RewardDesignerOpenAIAgent(BaseAgent):

\_model: str = PrivateAttr()

def \_\_init\_\_(self, model="gpt-4o-mini", \*\*kwargs):

super().\_\_init\_\_(name="RewardDesignerOpenAIAgent", \*\*kwargs)

self.\_model = model

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

We store the model name as a private attribute so we can configure it at instantiation while keeping the ADK agent interface clean.

#### Reading iteration context from shared state[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Reading-iteration-context-from-shared-state)

Inside `_run_async_impl(...)`, the agent reads the state it needs.

Ace Editor

1

2

3

4

5

async def \_run\_async\_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:

iteration = ctx.session.state.get("iteration", 1)

best\_reward\_code = ctx.session.state.get("best\_reward\_code", "")

reflection = ctx.session.state.get("reflection", "")

K = ctx.session.state["K"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is the minimum set of inputs required to decide:

- Are we exploring (iteration one)?
- Or improving (iteration two and above)?

#### Collecting task spec and environment code[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Collecting-task-spec-and-environment-code)

Now we pull the two most important grounding inputs:

Ace Editor

1

2

task\_spec = ctx.session.state["task\_spec"]

env\_code = ctx.session.state["env\_code"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is what keeps reward generation connected to the actual task and environment dynamics.

#### Including feedback only when available[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Including-feedback-only-when-available)

You’ll notice the system doesn’t always include candidate results:

Ace Editor

1

2

3

4

candidate\_results = None

# Only include "query with feedback" after we have results (i.e., from iteration 2 onward).

if iteration > 1:

candidate\_results = ctx.session.state.get("candidate\_results", None)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This preserves the intended flow:

- **Iteration 1:** No feedback exists, so don’t pretend it does.
- **Iteration 2+:** Feedback exists, so incorporate it.

### Calling the LLM reliably (with retries)[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Calling-the-LLM-reliably-with-retries)

Now we build the prompt and call the model.

Ace Editor

1

2

3

4

5

6

7

8

prompt = \_designer\_prompt(

ctx.session.state["task\_spec"],

ctx.session.state["env\_code"],

best\_reward\_code,

reflection,

K,

candidate\_results=candidate\_results,

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

To make the system more robust, we wrap the API call in retries using `tenacity`.

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

from tenacity import retry, stop\_after\_attempt, wait\_exponential, retry\_if\_exception\_type

@retry(

stop=stop\_after\_attempt(3),

wait=wait\_exponential(multiplier=1, min=2, max=10),

retry=retry\_if\_exception\_type((Exception,)),

reraise=True

)

def call\_llm():

return client.chat.completions.create(

model=self.\_model,

messages=[

{"role": "system", "content": DESIGNER\_SYSTEM},

{"role": "user", "content": prompt},

],

temperature=0.4,

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is one of the practical “production-grade” touches:

- It prevents a transient failure from terminating the entire iteration.
- It provides predictable retry behavior.

### Storing reward candidates for the evaluator[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Storing-reward-candidates-for-the-evaluator)

Once the model responds, we store its output in state:

Ace Editor

1

2

3

resp = call\_llm()

generated\_text = resp.choices[0].message.content

ctx.session.state["reward\_candidates\_text"] = generated\_text

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is the handoff point:

> The RewardDesigner produces raw candidate text; the evaluator parses, compiles, and trains.

We also log how many candidates the model appears to have produced:

Ace Editor

1

2

candidate\_count = generated\_text.count(CANDIDATE\_DELIM) + 1

logger.info(f"[RewardDesignerOpenAIAgent] Generated {candidate\_count} reward candidate(s) (expected {K})")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Finally, we yield control back to ADK:

Ace Editor

1

yield Event(author=self.name, content=None)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Implementing candidate evaluation[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-candidate-evaluation)

The RewardDesigner agent generated reward candidates and stored them in the shared state as raw text. Now we implement the next step: turn those candidates into evidence. The evaluator’s job is straightforward:

1. Parse K reward candidates from the LLM output.
2. Compile and validate each reward safely.
3. Train a policy with PPO for each candidate.
4. Evaluate and score the trained policy.
5. Save artifacts (reward code, metrics, rollout HTML, params).
6. Store a machine-readable summary in `ctx.session.state["candidate_results"]`.

All of that logic lives in `agents/evaluator_agent.py`.

### Imports: Tools that do the heavy lifting[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Imports-Tools-that-do-the-heavy-lifting)

Before we read the agent, notice what the evaluator imports from `tools/`. This tells us what the agent will orchestrate (and what it won’t re-implement).

Ace Editor

1

2

3

4

from ..tools.reward\_sandbox import compile\_reward

from ..tools.rl\_runner import train\_policy, evaluate\_policy, save\_policy\_rollout\_html

from ..tools.scoring import score\_candidate

from ..tools.artifacts import candidate\_dir, save\_text, save\_json, append\_leaderboard, save\_policy\_params

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

As you implement this, keep the agent/tool boundary clear:

- `compile_reward(...)` is the safety gate: it turns generated code into an executable function (or fails fast).
- `train_policy(...)` and `evaluate_policy(...)` do the RL work.
- `score_candidate(...)` converts evaluation metrics into a single comparable score.
- `artifacts.*` makes every run inspectable and reproducible.

### CandidateEvaluatorAgent entry point: Reading iteration context[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#CandidateEvaluatorAgent-entry-point-Reading-iteration-context)

Now we implement the agent and immediately pull what we need from the shared state.

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

class CandidateEvaluatorAgent(BaseAgent):

\_outdir: Path = PrivateAttr()

\_leaderboard\_path: Path = PrivateAttr()

def \_\_init\_\_(self, \*\*kwargs):

super().\_\_init\_\_(name="CandidateEvaluatorAgent", \*\*kwargs)

async def \_run\_async\_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:

iteration = ctx.session.state["iteration"]

env\_name = ctx.session.state["env\_name"]

train\_steps = ctx.session.state["train\_steps"]

seed = ctx.session.state["seed"]

K = ctx.session.state["K"]

self.\_outdir = Path(ctx.session.state["outdir"])

self.\_leaderboard\_path = Path(ctx.session.state["leaderboard\_path"])

text = ctx.session.state["reward\_candidates\_text"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

When you’re implementing this, read this block as the evaluator’s contract:

- It assumes the setup has already written `outdir`, `env_name`, `train_steps`, etc.
- It assumes the reward designer has already written `reward_candidates_text`.
- It will produce per-candidate artifacts under `outdir/iteration_###/candidate_###`.

### Parsing candidates from LLM output (robustly)[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Parsing-candidates-from-LLM-output-robustly)

LLMs sometimes wrap code in markdown fences or add stray backticks. Before we split candidates, we strip those patterns.

Ace Editor

1

2

3

4

5

6

7

# Remove markdown code blocks if present

# Remove ```python ... ``` blocks

text = re.sub(r'```python\s\*\n(.\*?)\n```', r'\1', text, flags=re.DOTALL)

# Remove ``` ... ``` blocks (generic)

text = re.sub(r'```\s\*\n(.\*?)\n```', r'\1', text, flags=re.DOTALL)

# Remove inline code backticks

text = text.replace('`', '')

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Now we split by the delimiter we enforced in the reward designer prompt:

Ace Editor

1

2

# Split by delimiter

parts = text.split("### CANDIDATE ###")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then we extract only valid reward candidates by looking for `def compute_reward` and cutting out extra text.

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

# Extract candidates - look for function definitions

candidates = []

for p in parts:

p = p.strip()

# Look for compute\_reward function definition

if "def compute\_reward" in p:

func\_match = re.search(r'def compute\_reward.\*?(?=\ndef [a-zA-Z\_]|\Z)', p, re.DOTALL)

if func\_match:

candidates.append(func\_match.group(0).strip())

else:

candidates.append(p)

candidates = candidates[:K]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Finally, we log what we found:

Ace Editor

1

logger.info(f"[CandidateEvaluatorAgent] Parsed {len(candidates)} candidates from LLM output (expected {K})")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This parsing strategy matters because it reliably turns “LLM text” into “candidate code units” without requiring perfect output formatting every time.

### Fail safely when parsing produces nothing[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Fail-safely-when-parsing-produces-nothing)

If parsing fails, we don’t fail the pipeline silently. We persist the raw output and write a clear error message to the shared state.

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

if not candidates:

iterdir = self.\_outdir / f"iteration\_{iteration:03d}"

iterdir.mkdir(parents=True, exist\_ok=True)

(iterdir / "raw\_llm\_output.txt").write\_text(text)

ctx.session.state["candidate\_results"] = "[]"

ctx.session.state["llm\_output\_error"] = (

"No valid reward candidates parsed. "

"Expected delimiter '### CANDIDATE ###' and function 'compute\_reward'. "

f"Saved raw output to: {iterdir / 'raw\_llm\_output.txt'}"

)

yield Event(author=self.name, content=None)

return

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

We preserve the exact LLM output so we can fix prompts or parsing later.

### Per-candidate evaluation loop: Save code first, then try to execute it[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Per-candidate-evaluation-loop-Save-code-first-then-try-to-execute-it)

Now we evaluate each candidate. The first thing we do is create a candidate directory and save the raw reward code, even if the evaluation fails.

Ace Editor

1

2

3

4

5

6

results = []

error\_summary = []

for i, code in enumerate(candidates, start=1):

cdir = candidate\_dir(self.\_outdir, iteration, i)

save\_text(cdir / "reward.py", code) # Always save the code, even if it fails

logger.info(f"[CandidateEvaluatorAgent] Evaluating candidate {i}/{len(candidates)}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is a simple but critical implementation choice: it makes every failure inspectable.

### Compile and validate the reward code in a sandbox[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Compile-and-validate-the-reward-code-in-a-sandbox)

This is the gate that turns candidate text into a callable reward function.

Ace Editor

1

2

3

try:

reward\_fn = compile\_reward(code)

logger.debug(f"[CandidateEvaluatorAgent] Candidate {i}: Reward function compiled and validated successfully")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

If compilation fails, we catch it later, write an error file, and move on to the next candidate, so one bad candidate doesn’t stop the iteration.

### Train and evaluate (delegated to `tools/rl_runner.py`)[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Train-and-evaluate-delegated-to-toolsrlrunnerpy)

Before training, we include a defensive cache clear to reduce memory buildup across multiple candidates.

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

# Clear JAX cache before training to prevent memory buildup

try:

import jax

if hasattr(jax, 'clear\_caches'):

jax.clear\_caches()

elif hasattr(jax.extend, 'backend') and hasattr(jax.extend.backend, 'clear\_backends'):

jax.extend.backend.clear\_backends()

except Exception as cache\_error:

logger.debug(f"[CandidateEvaluatorAgent] Could not clear JAX cache (non-critical): {cache\_error}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Now, training:

Ace Editor

1

2

3

4

make\_inf, params, train\_metrics, network\_config = train\_policy(

env\_name, reward\_fn, seed + i, train\_steps,

episode\_length=ctx.session.state["eval\_horizon"]

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

And evaluation:

Ace Editor

1

2

3

4

5

6

eval\_metrics = evaluate\_policy(

env\_name, reward\_fn, make\_inf, params, seed + i,

ctx.session.state["eval\_episodes"],

ctx.session.state["eval\_horizon"]

)

score = score\_candidate(eval\_metrics)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Implementation detail to notice: We deliberately use `seed + i` so that each candidate run is deterministic but distinct.

### Save the rollout HTML (noncritical if it fails)[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-the-rollout-HTML-noncritical-if-it-fails)

Rollouts are valuable, but we don't want them to be a single point of failure. That's why rendering is wrapped in its own `try/except`.

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

video\_horizon = min(400, ctx.session.state["eval\_horizon"])

try:

logger.info(f"[CandidateEvaluatorAgent] Candidate {i}: Rendering interactive HTML viewer...")

save\_policy\_rollout\_html(

out\_dir=cdir,

env\_name=env\_name,

reward\_fn=reward\_fn,

make\_inference\_fn=make\_inf,

params=params,

seed=seed + i,

horizon=video\_horizon,

)

logger.info(f"[CandidateEvaluatorAgent] Candidate {i}: Saved interactive HTML viewer (rollout.html)")

except Exception as render\_err:

logger.warning(f"[CandidateEvaluatorAgent] Candidate {i}: HTML viewer rendering failed (non-critical): {render\_err}. Continuing...")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

### Save metrics, training metadata, and policy params[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-metrics-training-metadata-and-policy-params)

First, the JSON artifacts:

Ace Editor

1

2

3

save\_json(cdir / "train\_metrics.json", train\_metrics)

save\_json(cdir / "eval\_metrics.json", eval\_metrics)

save\_json(cdir / "score.json", {"score": score})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then, metadata needed to regenerate visualizations later (important when you don't want to retrain):

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

save\_json(cdir / "training\_metadata.json", {

"seed": seed + i,

"train\_steps": train\_steps,

"episode\_length": ctx.session.state["eval\_horizon"],

"env\_name": env\_name,

"network\_config": network\_config,

"note": (

"To regenerate visualizations: Use recreate\_inference\_fn() with saved params and network\_config. "

"This avoids retraining and dimension mismatches."

)

})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then we save the policy parameters, guarded so a save failure doesn’t discard a successful evaluation:

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

try:

save\_policy\_params(cdir / "policy\_params.pkl", params)

logger.debug(f"[CandidateEvaluatorAgent] Candidate {i}: Policy parameters saved")

except Exception as save\_error:

logger.warning(

f"[CandidateEvaluatorAgent] Candidate {i}: Failed to save policy parameters: {save\_error}. "

f"Evaluation succeeded but params not saved."

)

save\_text(cdir / "policy\_save\_error.txt", str(save\_error))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

### Record results and update the leaderboard[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Record-results-and-update-the-leaderboard)

Now we append a summary entry to the leaderboard:

Ace Editor

1

append\_leaderboard(self.\_leaderboard\_path, iteration, i, score, eval\_metrics["avg\_return"], str(cdir))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

And we store a structured record in `results` so downstream agents (selector and reflector) don’t need to rescan files.

Ace Editor

1

2

3

4

5

6

7

8

results.append({

"candidate": i,

"score": score,

"eval": eval\_metrics,

"train\_metrics": train\_metrics, # Add behavioral metrics for reflector analysis

"artifact\_dir": str(cdir),

"reward\_code": code

})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is the key implementation outcome of the evaluator: it converts “candidate code” into a structured record of “candidate performance and artifacts.”

### Handle per-candidate failures without stopping the iteration[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Handle-per-candidate-failures-without-stopping-the-iteration)

If anything fails inside the `try` block, we capture it, write an error artifact, and still append a leaderboard entry so the failure is visible in the results.

Ace Editor

1

2

3

4

5

except Exception as e:

error\_msg = str(e)

error\_type = type(e).\_\_name\_\_

error\_summary.append(f"Candidate {i}: {error\_type}: {error\_msg}")

logger.error(f"[CandidateEvaluatorAgent] Candidate {i}: Failed with {error\_type}: {error\_msg}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then you write a detailed error report that includes the reward code and common failure causes:

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

error\_details = f"""Candidate {i} Evaluation Failed

Error Type: {error\_type}

Error Message: {error\_msg}

Reward Code:

{code}

Common Issues:

- Missing return statement: Ensure 'return total\_reward, reward\_terms' at end of function

- None values: Check that all variables are computed before returning

- Wrong return format: Must return (scalar\_jax\_array, dict\_of\_arrays)

- Syntax errors: Check for unclosed parentheses, brackets, or quotes

"""

save\_text(cdir / "error.txt", error\_details)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is exactly the kind of debugging scaffolding that makes an LLM-generated code system usable.

### Convert results into JSON and store them in shared state[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Convert-results-into-JSON-and-store-them-in-shared-state)

At the end, we serialize results so they're safe to pass into the reflector and selector.

Because evaluation metrics often include JAX arrays, convert them to JSON-safe types first:

Ace Editor

1

2

3

4

def convert\_to\_json\_serializable(obj):

"""Recursively convert objects to JSON-serializable format."""

import numpy as np

...

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then store the final JSON string in shared state:

Ace Editor

1

2

3

serializable\_results = convert\_to\_json\_serializable(results)

ctx.session.state["candidate\_results"] = json.dumps(serializable\_results, indent=2)

yield Event(author=self.name, content=None)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This line is the evaluator's output contract:

> Downstream agents read `ctx.session.state["candidate_results"]` and never need to rerun evaluation.

## Summary[#](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Summary)

In this lesson, we implemented the core learning step of the Eureka-like system: turning reward ideas into evidence. We learned how to:

- Reward functions are generated as executable code using an LLM.
- Multiple reward candidates are produced per iteration.
- Candidates are parsed, validated, and compiled safely.
- Policies are trained and evaluated for each candidate.
- Metrics, rollouts, and artifacts are recorded in a structured, inspectable way.

By the end of this lesson, the system is no longer proposing rewards. It is measuring their effects through behavior.

In the next lesson, we will build on this evidence to implement reward selection, automated reflection on what worked and what failed, optional human feedback, and the logic that decides whether the system should continue iterating or stop. This is where iterative improvement becomes deliberate rather than exploratory.

SetupAgent and Environment Grounding

Selection, Reflection, and Human Feedback

Ask

[Implementing reward generation](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-reward-generation)

[Setting up the OpenAI client and prompt constants](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Setting-up-the-OpenAI-client-and-prompt-constants)

[Building the reward generation prompt](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Building-the-reward-generation-prompt)

[Prompt mode: Improving an existing best reward](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-Improving-an-existing-best-reward)

[Prompt mode: First-iteration exploration](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Prompt-mode-First-iteration-exploration)

[Enforcing a strict output contract](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Enforcing-a-strict-output-contract)

[Implementing the RewardDesigner agent](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-the-RewardDesigner-agent)

[Reading iteration context from shared state](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Reading-iteration-context-from-shared-state)

[Collecting task spec and environment code](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Collecting-task-spec-and-environment-code)

[Including feedback only when available](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Including-feedback-only-when-available)

[Calling the LLM reliably (with retries)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Calling-the-LLM-reliably-with-retries)

[Storing reward candidates for the evaluator](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Storing-reward-candidates-for-the-evaluator)

[Implementing candidate evaluation](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Implementing-candidate-evaluation)

[Imports: Tools that do the heavy lifting](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Imports-Tools-that-do-the-heavy-lifting)

[CandidateEvaluatorAgent entry point: Reading iteration context](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#CandidateEvaluatorAgent-entry-point-Reading-iteration-context)

[Parsing candidates from LLM output (robustly)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Parsing-candidates-from-LLM-output-robustly)

[Fail safely when parsing produces nothing](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Fail-safely-when-parsing-produces-nothing)

[Per-candidate evaluation loop: Save code first, then try to execute it](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Per-candidate-evaluation-loop-Save-code-first-then-try-to-execute-it)

[Compile and validate the reward code in a sandbox](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Compile-and-validate-the-reward-code-in-a-sandbox)

[Train and evaluate (delegated to tools/rl\_runner.py)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Train-and-evaluate-delegated-to-toolsrlrunnerpy)

[Save the rollout HTML (noncritical if it fails)](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-the-rollout-HTML-noncritical-if-it-fails)

[Save metrics, training metadata, and policy params](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Save-metrics-training-metadata-and-policy-params)

[Record results and update the leaderboard](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Record-results-and-update-the-leaderboard)

[Handle per-candidate failures without stopping the iteration](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Handle-per-candidate-failures-without-stopping-the-iteration)

[Convert results into JSON and store them in shared state](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Convert-results-into-JSON-and-store-them-in-shared-state)

[Summary](https://www.educative.io/courses/agentic-ai-systems/reward-generation-and-evaluation-loop#Summary)