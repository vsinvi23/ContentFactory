# Loop_Control_and_Exit_Conditions_in_Eureka-Like_Reward_Systems

Source: https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Loop Control, Exit Conditions, and System Behavior

Explore how to assemble and control an iterative reward learning loop using Google's ADK. Understand how the system orchestrates agents, manages iterations, applies exit strategies, and interprets outputs through logs and leaderboards to refine agent behavior in a Eureka-like reward design setting.

We'll cover the following...

- [Where the full system is assembled](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Where-the-full-system-is-assembled)
- [Entrypoint: agent.py](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Entrypoint-agentpy)
  - [Step A: The orchestration primitive is SequentialAgent](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-A-The-orchestration-primitive-is-SequentialAgent)
  - [Step B: root\_agent is the runnable pipeline that ADK executes](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-B-rootagent-is-the-runnable-pipeline-that-ADK-executes)
- [Loop assembly: reward\_loop.py](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Loop-assembly-rewardlooppy)
- [How to run the system and interpret its outputs](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-run-the-system-and-interpret-its-outputs)
  - [Option A: Run the full system on Google Colab](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-A-Run-the-full-system-on-Google-Colab)
  - [Option B: Inspect a real run using the provided pre-run notebook + rollouts](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-B-Inspect-a-real-run-using-the-provided-pre-run-notebook--rollouts)
- [How to read the outputs like a system designer](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-read-the-outputs-like-a-system-designer)
  - [1) Start with the run folder](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#1-Start-with-the-run-folder)
  - [2) Look at the leaderboard to see “who won”](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#2-Look-at-the-leaderboard-to-see-who-won)
  - [3) Use rollouts to validate behavior (not just numbers)](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#3-Use-rollouts-to-validate-behavior-not-just-numbers)
  - [4) Use logs to trace execution boundaries](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#4-Use-logs-to-trace-execution-boundaries)
- [Summary](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Summary)

In previous lessons, we implemented each component of the Eureka-like system in isolation:

- Setup and environment initialization
- Reward generation and evaluation
- Selection and reflection
- Feedback and exit control
- Iteration state management

In this lesson, we step back and look at how the components fit together. The goal is not to introduce new agents or tools. Instead, we’ll trace where execution starts, how control flows across agents, how iterations repeat, and how outputs accumulate over time.

## Where the full system is assembled[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Where-the-full-system-is-assembled)

In our implementation, there are two assembly points:

- `agent.py` → the workflow entry point that ADK runs
- `reward_loop.py` → the loop factory that builds the iterative reward evolution loop

Before diving into code, it’s important to read these files with the right mindset. These files answer questions like:

- Which agent runs first?
- Which agents repeat?
- What happens when the exit condition is met?

It does not answer how rewards are generated, how PPO works, or how scoring is computed. All that logic lives elsewhere.

## Entrypoint: `agent.py`[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Entrypoint-agentpy)

When we run the project with ADK, execution begins from the file below:

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

"""ADK entrypoint for `adk run app/eureka\_loop`"""

from google.adk.agents import SequentialAgent

from .agents.setup\_agent import SetupAgent

from .agents.reward\_loop import build\_reward\_loop

root\_agent = SequentialAgent(

name="EurekaRewardEvolutionPipeline",

sub\_agents=[

SetupAgent(name="SetupAgent"),

build\_reward\_loop(),

],

description="Initializes env/task state and runs an Eureka-like reward evolution loop."

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Let’s read this in two steps:

### Step A: The orchestration primitive is `SequentialAgent`[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-A-The-orchestration-primitive-is-SequentialAgent)

Ace Editor

1

from google.adk.agents import SequentialAgent

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

We import `SequentialAgent` because the top-level workflow is strictly ordered. There’s no branching here. The flow is linear: run setup, then enter the loop.

### Step B: `root_agent` is the runnable pipeline that ADK executes[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-B-rootagent-is-the-runnable-pipeline-that-ADK-executes)

Ace Editor

1

2

3

4

5

6

7

8

root\_agent = SequentialAgent(

name="EurekaRewardEvolutionPipeline",

sub\_agents=[

SetupAgent(name="SetupAgent"),

build\_reward\_loop(),

],

...

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This `sub_agents=[ ... ]` list is the entire top-level execution plan:

1. Run `SetupAgent` once.
2. Then, run whatever `build_reward_loop()` returns (the iterative loop).

That’s the key point: the loop is not defined inline here. It’s built in a separate module so we can configure it cleanly.

## Loop assembly: `reward_loop.py`[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Loop-assembly-rewardlooppy)

Now we open the file that constructs the iterative portion of the workflow:

Ace Editor

1

2

3

4

5

6

7

8

import yaml

from google.adk.agents import LoopAgent

from .llm\_agents import RewardDesignerOpenAIAgent, RewardReflectorOpenAIAgent

from .evaluator\_agent import CandidateEvaluatorAgent

from .selector\_agent import SelectorAgent

from .human\_reflection\_agent import HumanReflectionAgent

from .increment\_iteration\_agent import IncrementIterationAgent

from .exit\_checker\_agent import ExitCheckerAgent

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This import list defines the agents involved in the loop. Note what’s missing: `SetupAgent` is not imported here because the setup runs outside the loop.

We load the loop configuration so that the loop is not hard-coded.

Ace Editor

1

2

3

def \_load\_yaml(path):

with open(path, "r") as f:

return yaml.safe\_load(f)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

We keep this helper small on purpose. This file is about assembly, not validation. Validation belongs in `setup_agent.py`, which we implemented earlier.

`build_reward_loop()` is the factory that ADK calls from `agent.py`:

Ace Editor

1

2

3

def build\_reward\_loop():

loop\_cfg = \_load\_yaml("configs/loop\_config.yaml")

model = loop\_cfg.get("openai\_model", "gpt-4o-mini")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Two important implementation details happen here:

- The loop reads `configs/loop_config.yaml`, so the iteration count and settings are configurable.
- The OpenAI model is also config-driven via `openai_model`, with a safe default.

That is why `agent.py` can remain minimal; it delegates loop configuration and construction to this module.

Next, we construct the `LoopAgent` with the iteration body and return the configured agent.

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

return LoopAgent(

name="RewardEvolutionLoop",

sub\_agents=[

RewardDesignerOpenAIAgent(model=model),

CandidateEvaluatorAgent(),

SelectorAgent(name="SelectorAgent"),

RewardReflectorOpenAIAgent(model=model),

HumanReflectionAgent(name="HumanReflectionAgent"), # Human-in-the-loop after LLM reflection

ExitCheckerAgent(name="ExitCheckerAgent"),

IncrementIterationAgent(name="IncrementIterationAgent"),

],

max\_iterations=loop\_cfg["iterations"]

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Read this as the loop’s “execution contract.”

The loop body is defined by `sub_agents=[ ... ]` (in order).

This list is the *exact per-iteration flow*:

1. **RewardDesignerOpenAIAgent** → generates K reward candidates (code).
2. **CandidateEvaluatorAgent** → trains and evaluates policies per candidate.
3. **SelectorAgent** → picks the best candidate by score.
4. **RewardReflectorOpenAIAgent** → analyzes results and writes a reflection.
5. **HumanReflectionAgent** → optional human feedback after reflection.
6. **ExitCheckerAgent** → decides whether to stop early.
7. **IncrementIterationAgent** → advances iteration state for the next cycle.

This ordering *is* the system.

If you ever want to change the loop behavior, this is the single place where that change is expressed.

The loop stops in two ways: a hard cap and an early exit.

Ace Editor

1

max\_iterations=loop\_cfg["iterations"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This gives us a hard upper bound (a safety net).

Separately, the loop can still stop early when `ExitCheckerAgent` triggers the exit tool, which we implemented in the previous lesson.

So termination is both bounded by `max_iterations` and adaptive via early-exit criteria.

## How to run the system and interpret its outputs[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-run-the-system-and-interpret-its-outputs)

In a typical coding lesson, we would run the pipeline live and inspect the outputs together. For this project, there’s one practical constraint: end-to-end runs are GPU-intensive (training multiple PPO policies per iteration) and can take hours, depending on your settings. That makes it impractical to run on our course platform.

So we support two equally valid ways to follow this part:

- **Option A (recommended for hands-on learners):** Run it on Google Colab using a T4 GPU.
- **Option B:** Use our provided pre-run notebook, rollouts, and logs (provided in lesson one of this chapter) to inspect a real execution without spending compute.

We’ll cover both.

### Option A: Run the full system on Google Colab[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-A-Run-the-full-system-on-Google-Colab)

If you want to run the pipeline yourself and experiment, use Google Colab with a GPU runtime.

What you’ll do in Colab:

1. Install dependencies (`requirements.txt`).
2. Set your API key(s) (OpenAI key for reward generation and reflection).
3. Run the ADK workflow.
4. Watch artifacts accumulate across iterations.

You can find the commands in the notebook provided in **lesson one** of this chapter.

Why Colab is the right place:

- You get access to free or low-cost GPUs (T4).
- Your runs can take a long time without blocking a limited course execution environment.
- It’s easy to tweak configs and rerun.

What to experiment with first:

- Reduce compute so you can iterate faster:

  - Fewer iterations
  - Fewer candidates per iteration
  - Fewer training steps
- Then scale up once you’re confident the loop behaves as expected.

### Option B: Inspect a real run using the provided pre-run notebook + rollouts[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-B-Inspect-a-real-run-using-the-provided-pre-run-notebook--rollouts)

If you don’t want to run training yourself, you can still understand the system by inspecting the artifacts we already included:

- The pre-run notebook output (attached earlier) contains the execution logs.
- The rollout visualizations.

This is often the best way to learn the workflow first because you can focus on interpretation rather than waiting for training.

## How to read the outputs like a system designer[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-read-the-outputs-like-a-system-designer)

Whether you run it yourself or use the pre-run artifacts, the outputs tell the same story. Here’s the quickest way to interpret them.

### 1) Start with the run folder[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#1-Start-with-the-run-folder)

Each execution produces a single run directory (timestamped). Inside it, you’ll find:

- Iteration folders
- Per-candidate artifacts
- Summary files (like leaderboards and configs)

```
{
  "avg_return": -91.40534973144531,
  "returns": [
    -91.40534973144531
  ],
  "term_means": {}
}
```

This structure reflects the loop: iteration → candidates → evaluation artifacts.

### 2) Look at the leaderboard to see “who won”[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#2-Look-at-the-leaderboard-to-see-who-won)

The leaderboard is the fastest high-level signal:

- Which candidates scored best?
- How do scores change across iterations?
- How is the system improving or plateauing?

If scores don’t improve, that isn’t a failure. It’s a signal that the reward or evaluation setup needs work.

- Prompts may need tightening.
- Reflections may need to be more specific.
- Reward constraints may be too weak or too strict.

### 3) Use rollouts to validate behavior (not just numbers)[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#3-Use-rollouts-to-validate-behavior-not-just-numbers)

Scores are necessary, but rollouts answer the real question:

- What did the agent actually learn to do?

Rollouts help you detect classic reward pitfalls early:

- Fast movement in the wrong direction
- Unstable gaits that “hack” reward terms
- Behavior that looks good numerically but fails visually

That is exactly why we included rollout HTML artifacts in the project.

### 4) Use logs to trace execution boundaries[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#4-Use-logs-to-trace-execution-boundaries)

The logs are your “flight recorder.”

When skimming, look for:

- Setup completion
- Iteration start markers
- Reward candidate generation
- Evaluation start/end per candidate
- Selection results
- Reflection text
- Exit decisions and iteration increments

If something looks off (missing candidates, repeated results, early termination), logs are the fastest way to locate the stage where it happened.

## Summary[#](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Summary)

In this lesson, we learned how the entire Eureka-like system comes together and runs as a single, executable workflow. We explored:

- Where execution begins in the codebase ([agent.py](https://www.educative.io/courses/agentic-ai-systems/agent.py)).
- How the iterative reward evolution loop is assembled ([reward\_loop.py](https://www.educative.io/courses/agentic-ai-systems/loop.py)).
- How individual agents are orchestrated into a repeatable learning cycle.
- How loop termination is controlled through both configuration and agent-driven exit logic.

We also learned how to work with the system in practice:

- When and why to run it on Google Colab with GPU resources.
- How to inspect a real execution using pre-run notebooks, logs, and rollouts.
- How to interpret leaderboards, visualizations, and logs to understand learning progress.

By the end of this lesson, we should be able to reason about the system as a whole, from entry point to termination, and confidently navigate its outputs to debug, evaluate, and improve reward learning behavior.

This concludes the implementation chapter and sets the stage for further experimentation with custom reward designs, prompts, and agent configurations.

Selection, Reflection, and Human Feedback

Thinking Through Eureka

Ask

[Where the full system is assembled](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Where-the-full-system-is-assembled)

[Entrypoint: agent.py](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Entrypoint-agentpy)

[Step A: The orchestration primitive is SequentialAgent](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-A-The-orchestration-primitive-is-SequentialAgent)

[Step B: root\_agent is the runnable pipeline that ADK executes](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Step-B-rootagent-is-the-runnable-pipeline-that-ADK-executes)

[Loop assembly: reward\_loop.py](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Loop-assembly-rewardlooppy)

[How to run the system and interpret its outputs](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-run-the-system-and-interpret-its-outputs)

[Option A: Run the full system on Google Colab](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-A-Run-the-full-system-on-Google-Colab)

[Option B: Inspect a real run using the provided pre-run notebook + rollouts](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Option-B-Inspect-a-real-run-using-the-provided-pre-run-notebook--rollouts)

[How to read the outputs like a system designer](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#How-to-read-the-outputs-like-a-system-designer)

[1) Start with the run folder](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#1-Start-with-the-run-folder)

[2) Look at the leaderboard to see “who won”](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#2-Look-at-the-leaderboard-to-see-who-won)

[3) Use rollouts to validate behavior (not just numbers)](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#3-Use-rollouts-to-validate-behavior-not-just-numbers)

[4) Use logs to trace execution boundaries](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#4-Use-logs-to-trace-execution-boundaries)

[Summary](https://www.educative.io/courses/agentic-ai-systems/loop-control-exit-conditions-and-system-behavior#Summary)