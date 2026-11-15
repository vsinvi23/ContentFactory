# Setting_up_Agentic_Systems_with_Environment_Grounding

Source: https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# SetupAgent and Environment Grounding

Explore the SetupAgent's role in initializing shared state, loading configurations, and creating environment contexts to support downstream agents. Understand how to prepare system artifacts and generate baseline rollouts that enable reward learning pipelines to function cohesively and reliably.

We'll cover the following...

- [Code walk-through](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Code-walk-through)
  - [Loading configuration files safely](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-configuration-files-safely)
  - [Defining the SetupAgent and its execution entry point](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Defining-the-SetupAgent-and-its-execution-entry-point)
  - [Guarding against repeated setup](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Guarding-against-repeated-setup)
  - [Loading loop and task configuration](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-loop-and-task-configuration)
  - [Enforcing the configuration contract](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Enforcing-the-configuration-contract)
  - [Initializing the run directory and leaderboard](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-the-run-directory-and-leaderboard)
  - [Creating the environment and extracting its source](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Creating-the-environment-and-extracting-its-source)
  - [Persisting run metadata](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Persisting-run-metadata)
  - [Initializing shared session state](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-shared-session-state)
  - [Generating the baseline rollout](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Generating-the-baseline-rollout)
  - [Signaling completion to ADK](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Signaling-completion-to-ADK)
- [Summary](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Summary)

In this EUREKA-like pipeline, the SetupAgent is the first step in the execution flow. It initializes shared state that downstream agents depend on, including loaded configuration, an artifacts directory, and the initial environment context. It also generates a baseline rollout that serves as a visual reference before reward evolution begins. In this lesson, we’ll walk through `agents/setup_agent.py`.

## Code walk-through[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Code-walk-through)

We begin by importing everything the SetupAgent needs to run.

Ace Editor

1

2

3

4

5

6

import yaml

from google.adk.agents import BaseAgent

from google.adk.agents.invocation\_context import InvocationContext

from google.adk.events import Event

from typing import AsyncGenerator

from loguru import logger

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Imports: Declaring what this agent is allowed to do

Let’s unpack this step by step:

- We import `BaseAgent` because every executable unit in an ADK workflow must subclass it. This is what allows ADK to recognize `SetupAgent` as a runnable agent.
- `InvocationContext` is how ADK passes execution state into the agent. This object gives us access to the shared session state that persists across agents.
- `Event` signals completion back to ADK. Even when an agent doesn’t emit meaningful output, it still needs to yield an event to satisfy the execution contract.
- `AsyncGenerator` appears because ADK agents are asynchronous and stream events as they execute.
- `yaml` is used to load configuration files, and `logger` gives us structured logging during setup.

At this point, we’ve declared:

> “This file defines an ADK agent that reads configuration and mutates shared execution state.”

Next, we import the tools that the SetupAgent will rely on.

Ace Editor

1

2

from ..tools.brax\_env import get\_env\_and\_source

from ..tools.artifacts import init\_run\_dir, init\_leaderboard, save\_json

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

These imports are especially important because they show what this agent does not do itself.

- `get_env_and_source(...)` encapsulates environment creation and source extraction. The SetupAgent will call this function, but it does not manage Brax internals directly.
- `init_run_dir(...)` and `init_leaderboard(...)` handle filesystem setup.
- `save_json(...)` persists metadata for later inspection.

This is a deliberate design choice. The SetupAgent handles orchestration, while tools perform execution.

### Loading configuration files safely[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-configuration-files-safely)

Before we define the agent itself, we add a small helper function for reading configuration files.

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

def \_load\_yaml(path):

"""Load YAML file with error handling."""

try:

with open(path, "r") as f:

data = yaml.safe\_load(f)

if data is None:

raise ValueError(f"YAML file {path} is empty or contains no data")

return data

except FileNotFoundError:

raise FileNotFoundError(f"Configuration file not found: {path}")

except yaml.YAMLError as e:

raise ValueError(f"Failed to parse YAML file {path}: {e}")

except Exception as e:

raise ValueError(f"Error loading YAML file {path}: {e}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Here’s how to read this as an implementer:

- The SetupAgent is the *first place* where configuration is loaded.
- If the configuration is missing or malformed, it is better to fail here than deep inside the reward loop.
- This helper wraps YAML loading with clear, explicit errors so failures are easy to diagnose.

We define this function outside the agent class because it’s a pure helper function, and it keeps the agent’s execution logic focused. With this in place, the rest of the agent can treat configuration loading as a solved problem.

### Defining the SetupAgent and its execution entry point[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Defining-the-SetupAgent-and-its-execution-entry-point)

Now that the supporting utilities are in place, we define the agent itself.

Ace Editor

1

2

3

4

class SetupAgent(BaseAgent):

async def \_run\_async\_impl(

self, ctx: InvocationContext

) -> AsyncGenerator[Event, None]:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is the *entry point ADK calls* when it executes the SetupAgent.

A few things to note as an implementer:

- We subclass `BaseAgent` so ADK can schedule this class as part of the workflow.
- `_run_async_impl` is the method ADK expects for asynchronous execution.
- `ctx` (`InvocationContext`) is our access point to:

  - Shared session state
  - Configuration injected by the workflow
  - Execution metadata

Everything this agent produces or modifies flows through `ctx`.

### Guarding against repeated setup[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Guarding-against-repeated-setup)

The first thing the agent does is check whether the setup has already been completed.

Ace Editor

1

2

3

if ctx.session.state.get("\_setup\_done", False):

yield Event(author=self.name, content=None)

return

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This guard is important for two reasons:

- ADK workflows can be re-entered or resumed.
- The setup logic must be idempotent. Running it twice would overwrite artifacts and state.

By setting and checking `_setup_done`, we guarantee that setup runs exactly once, and downstream agents always see a stable, initialized state.

### Loading loop and task configuration[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-loop-and-task-configuration)

With execution confirmed, we load the configuration files that define the run.

Ace Editor

1

2

loop\_cfg = \_load\_yaml("configs/loop\_config.yaml")

task\_spec = \_load\_yaml("configs/task\_spec\_halfcheetah.yaml")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

As an implementer, this is where you should pause and ask:

> Which parts of the system depend on configuration?

- `loop_cfg` controls how the system runs (iterations, candidates, training steps, seed, environment).
- `task_spec` controls how performance is evaluated (episodes, horizon, task metadata).

By loading both here, we ensure that every downstream agent reads from the same source of truth.

### Enforcing the configuration contract[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Enforcing-the-configuration-contract)

Next, we validate only the fields that later agents require to function correctly.

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

required\_loop\_keys = [

"env\_name",

"iterations",

"candidates\_per\_iteration",

"train\_steps",

"seed",

]

for key in required\_loop\_keys:

if key not in loop\_cfg:

raise ValueError(f"Missing required config key: {key}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Here, we’re not trying to exhaustively validate every config option.  
We’re enforcing a minimal contract:

- If these keys are missing.
- The reward loop or evaluator will break later.

We follow this with basic type and range checks:

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

if not isinstance(loop\_cfg["iterations"], int) or loop\_cfg["iterations"] < 1:

raise ValueError("iterations must be a positive integer")

if (

not isinstance(loop\_cfg["candidates\_per\_iteration"], int)

or loop\_cfg["candidates\_per\_iteration"] < 1

):

raise ValueError("candidates\_per\_iteration must be a positive integer")

if not isinstance(loop\_cfg["train\_steps"], int) or loop\_cfg["train\_steps"] < 1:

raise ValueError("train\_steps must be a positive integer")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Finally, we validate the evaluation spec:

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

if "evaluation" not in task\_spec:

raise ValueError("task\_spec must contain 'evaluation'")

if (

"episodes" not in task\_spec["evaluation"]

or "horizon" not in task\_spec["evaluation"]

):

raise ValueError(

"task\_spec.evaluation must contain 'episodes' and 'horizon'"

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This ensures that when we reach policy evaluation later, the evaluator can run without defensive checks scattered across the codebase.

### Initializing the run directory and leaderboard[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-the-run-directory-and-leaderboard)

Once the configuration is valid, we prepare the filesystem structure for this run.

Ace Editor

1

2

outdir = init\_run\_dir()

leaderboard\_path = init\_leaderboard(outdir)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This does two things:

- `init_run_dir()` creates a unique output directory for this run.
- `init_leaderboard()` initializes a file where candidate results are accumulated across iterations.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27933%27%20height=%27322%27/%3e)![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

From this point on, every artifact produced by the system has a known destination.

### Creating the environment and extracting its source[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Creating-the-environment-and-extracting-its-source)

Next, we initialize the environment and capture its source code.

Ace Editor

1

env, env\_source = get\_env\_and\_source(loop\_cfg["env\_name"])

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This single line does a lot of work:

- It instantiates the Brax environment.
- It extracts the environment's source code as text.

Why do we do this during setup?

- The environment object is needed by evaluators and rollout generation.
- The environment's source code is later provided to LLM-based agents, so reward generation is grounded in the actual dynamics rather than guesswork.

Note the separation here. The agent determines that this context is required, and the tool is responsible for retrieving it.

### Persisting run metadata[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Persisting-run-metadata)

Before moving on, we save key metadata for inspection and reproducibility.

Ace Editor

1

2

save\_json(loop\_cfg, outdir / "loop\_config.json")

save\_json(task\_spec, outdir / "task\_spec.json")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This allows us to:

- Inspect exactly which configuration produced a given run.
- Rerun or debug experiments later.
- Correlate logs, rollouts, and rewards with their inputs.

### Initializing shared session state[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-shared-session-state)

Now we write everything that downstream agents rely on into the shared state.

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

ctx.session.state.update(

{

"\_setup\_done": True,

"loop\_cfg": loop\_cfg,

"task\_spec": task\_spec,

"env": env,

"env\_source": env\_source,

"outdir": str(outdir),

"leaderboard\_path": str(leaderboard\_path),

"iteration": 0,

}

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This is a critical moment in the implementation.

From here on:

- Reward designers read from this state.
- Evaluators train using this environment.
- Selectors and reflectors rely on the same metadata.

This is how loose coupling between agents is achieved in practice.

### Generating the baseline rollout[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Generating-the-baseline-rollout)

Finally, the SetupAgent generates the baseline rollout.

Ace Editor

1

2

logger.info("Generating baseline rollout...")

rollout\_html = generate\_baseline\_rollout(env, outdir)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This rollout captures behavior before any reward learning occurs.

It is saved as an artifact and serves as a visual reference, a preliminary check, and a comparison point for later iterations.

Once this is complete, the system is ready to learn.

### Signaling completion to ADK[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Signaling-completion-to-ADK)

The last step is to yield an event to ADK and exit.

Ace Editor

1

yield Event(author=self.name, content=None)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

At this point, setup is complete, shared state is initialized, and control returns to the workflow, which then enters the reward evolution loop.

## Summary[#](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Summary)

In this lesson, we have implemented an agent that:

- Runs once.
- Initializes the environment and configuration.
- Prepares output artifacts.
- Generates a baseline rollout.
- Hands a fully grounded state to the rest of the system.

No training happens here, but the rest of the pipeline depends on it.

Agent Design, Code Structure, and Output Demonstration

Reward Generation and Evaluation Loop

Ask

[Code walk-through](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Code-walk-through)

[Loading configuration files safely](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-configuration-files-safely)

[Defining the SetupAgent and its execution entry point](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Defining-the-SetupAgent-and-its-execution-entry-point)

[Guarding against repeated setup](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Guarding-against-repeated-setup)

[Loading loop and task configuration](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Loading-loop-and-task-configuration)

[Enforcing the configuration contract](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Enforcing-the-configuration-contract)

[Initializing the run directory and leaderboard](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-the-run-directory-and-leaderboard)

[Creating the environment and extracting its source](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Creating-the-environment-and-extracting-its-source)

[Persisting run metadata](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Persisting-run-metadata)

[Initializing shared session state](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Initializing-shared-session-state)

[Generating the baseline rollout](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Generating-the-baseline-rollout)

[Signaling completion to ADK](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Signaling-completion-to-ADK)

[Summary](https://www.educative.io/courses/agentic-ai-systems/setupagent-and-environment-grounding#Summary)