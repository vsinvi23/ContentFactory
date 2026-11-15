# Building_Multimodal_Web_Agents_with_Google_ADK

Source: https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Assembling the Web Agent with Google ADK

Explore how to build a multimodal web agent leveraging the Google Agent Development Kit. Understand the architecture and orchestration of strict, single-agent, and multi-agent modes while integrating visual grounding and continuous interaction loops. This lesson guides you through assembling the core web agent, managing toolsets, and handling agent workflows for reliable and adaptive web navigation.

We'll cover the following...

- [The agent architecture flow](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-agent-architecture-flow)
  - [Imports and helper functions](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Imports-and-helper-functions)
  - [The factory entry and strict mode](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-factory-entry-and-strict-mode)
    - [Binding the strict agent and loop wrapper](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-the-strict-agent-and-loop-wrapper)
  - [Single agent mode configuration](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Single-agent-mode-configuration)
    - [Binding tools and the loop wrapper](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-tools-and-the-loop-wrapper)
  - [Multi-agent orchestration (delegating tasks)](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Multi-agent-orchestration-delegating-tasks)
  - [Conclusion](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Conclusion)

In the previous lessons, we built a persistent browser session manager and a suite of multimodal web tools. However, tools alone cannot complete a task; they require an intelligent agent to orchestrate them.

In this final lesson, we dissect `src/adk_agent/web_agent.py` chunk by chunk. This file acts as the "brain" of the application. It resolves the LLM model, handles API versioning differences, and uses a factory function to build the root agent based on your environment configuration. Because agentic web systems are complex, `web_agent.py` is designed to support three distinct operational modes:

1. **Strict mode:** A heavily constrained, single-agent loop optimized for precise one-to-seven numeric action commands.
2. **Single-agent mode:** A WebVoyager-style single agent that uses conversational tool calling.
3. **Multi-agent workflow:** A delegated hierarchy in which a Coordinator manages a Planner, a Vision agent, and a Browser agent.

## The agent architecture flow[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-agent-architecture-flow)

Before reading the code, let's visualize the control flow. The factory function checks the environment variables and builds the corresponding agent structure, ultimately wrapping the active agents in a `LoopAgent` so the ReAct loop runs continuously until the task finishes.

![The control flow of the Google ADK web agent. The build_root_agent() factory evaluates environment configurations to launch either a Strict, Single, or Multi-Agent system, ensuring continuous task execution by wrapping the active agents in a LoopAgent](004_Building_Multimodal_Web_Agents_with_Google_ADK_images/img_a86da4c77f44.svg "The control flow of the Google ADK web agent. The build_root_agent() factory evaluates environment configurations to launch either a Strict, Single, or Multi-Agent system, ensuring continuous task execution by wrapping the active agents in a LoopAgent")

The control flow of the Google ADK web agent. The build\_root\_agent() factory evaluates environment configurations to launch either a Strict, Single, or Multi-Agent system, ensuring continuous task execution by wrapping the active agents in a LoopAgent

### Imports and helper functions[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Imports-and-helper-functions)

We begin by importing the tools we built in the previous lesson and defining helper functions that abstract away version differences in the Google ADK library.

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

21

22

23

24

25

26

27

"""Google ADK multi-agent builder for a multimodal web agent."""

from \_\_future\_\_ import annotations

import os

from dotenv import load\_dotenv

from google.adk.agents import Agent, LoopAgent

from src.tools.web\_tools import (

action\_answer,

action\_back,

action\_click,

action\_google,

action\_input,

action\_scroll,

action\_wait,

analyze\_screenshot\_with\_vlm,

capture\_observation,

capture\_multimodal\_observation,

click\_element,

close\_browser,

log\_step,

navigate,

go\_back,

go\_google,

reset\_browser\_task\_state,

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

ADK compatibility wrappers, tool imports, and model resolution (web\_ agent.py )

- **Lines 3–34:** We import standard libraries (`os`), environment loaders (`load_dotenv`), ADK base classes (`Agent`, `LoopAgent`), and the exhaustive list of web tools we created previously in `src/tools/web_tools.py`.
- **Lines 37–54:** `_create_agent` packs `name`, `model`, and `instruction` into a `kwargs` dictionary. It conditionally adds `tools` and `sub_agents` only if they are provided, which keeps instantiation clean. It then attempts to instantiate `agent_cls` with these arguments. If a `TypeError` occurs, often due to minor ADK version mismatches around sub-agent initialization, it removes `sub_agents` from the dictionary and tries again as a safe fallback.
- **Lines 57–74:** `_create_workflow_agent` prepares arguments specifically for workflow agents, such as loops. If standard instantiation fails, it iterates through known alternative parameter names (`"agents"`, `"children"`, `"steps"`) to maintain backward and forward compatibility with the ADK framework across versions.
- **Lines 77–88:** `_resolve_llm_model` dynamically assigns the language model. It prioritizes a direct `ADK_MODEL` environment variable, falls back to `ADK_OPENAI_MODEL`, and defaults to `"openai/gpt-5-mini"` if neither is set.

### The factory entry and strict mode[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-factory-entry-and-strict-mode)

The `build_root_agent()` function is the core factory of our application. When it executes, it first checks whether the user wants to run the system in "Strict Mode."

Strict mode removes the standard conversational tool, calling. Instead, it forces the LLM to output rigid, numeric commands, relying entirely on the visual bounding boxes we injected in the previous lesson.

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

21

22

23

24

25

26

27

def build\_root\_agent():

"""Build a Google ADK multi-agent web automation system."""

load\_dotenv()

model\_name = \_resolve\_llm\_model()

strict\_mode = os.getenv("ADK\_STRICT\_MODE", "true").strip().lower() == "true"

if strict\_mode:

strict\_instruction = (

"You are a general multimodal web agent operating in strict mode. "

"Imagine you are a robot browsing the web, just like humans. Now you need to complete a task. "

"In each iteration, you will receive an Observation that includes a screenshot of a webpage and some texts. "

"This screenshot will feature Numerical Labels placed in the TOP LEFT corner of each Web Element. "

"Carefully analyze the visual information to identify the Numerical Label corresponding to the Web Element that requires interaction, "

"then follow the guidelines and choose one of the following actions:\n"

"1. Click a Web Element.\n"

"2. Delete existing content in a textbox and then type content.\n"

"3. Scroll up or down. Multiple scrolls are allowed to browse the webpage. "

"Pay attention: the default scroll is the whole window. If the scroll widget is located in a certain area of the webpage, "

"then you have to specify a Web Element in that area.\n"

"4. Wait. Typically used to wait for unfinished webpage processes, with a duration of 5 seconds.\n"

"5. Go back, returning to the previous webpage.\n"

"6. Google, directly jump to the Google search page. When you can't find information on some websites, try starting over with Google.\n"

"7. Answer. This action should only be chosen when all questions in the task have been solved.\n"

"Correspondingly, Action should STRICTLY follow the format:\n"

"- Click [Numerical\_Label]\n"

"- Type [Numerical\_Label]; [Content]\n"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Checking environment variables and defining the massive Strict Mode Prompt (web\_ agent.py )

- **Lines 3–6:** We load the `.env` configuration, resolve the model string, and check whether `ADK_STRICT_MODE` is enabled. It defaults to `"true"` if the variable is omitted.
- **Lines 8–24:** We define the core operational boundary. The agent is explicitly told to look for "numerical labels placed in the top-left corner of each web element" and is restricted to choosing from exactly seven specific action types (Click, Delete/Type, Scroll, Wait, Go back, Google, Answer).
- **Lines 25–32:** We dictate the strict syntax the model must format its output in (e.g., `- Type [Numerical_Label]; [Content]`).
- **Lines 33–45:** We establish 12 "key guidelines." These rules prevent common LLM pitfalls, such as typing into buttons (Rule 2), repeating actions when stuck (Rule 4), or navigating away via low-signal global links like Learning or Feeds (Rule 12).
- **Lines 46–59:** A "concrete decision policy" (A through H) instructs the agent on goal decomposition, constraint tracking, and recovery rules for dealing with CAPTCHAs, pop-ups, or paywalls.
- **Lines 60–81:** We provide three extensive few-shot examples (E-commerce, Travel, and General Information). Step-by-step patterns help the model sequence its tool calls correctly, such as demonstrating that it must always observe after navigating.
- **Lines 82–85:** The "global completion rule" strictly forbids calling `action_answer` multiple times for a single task, instructing the agent to use `reset_browser_task_state()` if it needs to clear a locked browsing session.
- **Lines 86–91:** A final operational protocol reminds the agent to always start with an observation and forces it to use the ADK tool-calling mechanisms rather than outputting plain-text Markdown.

#### Binding the strict agent and loop wrapper[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-the-strict-agent-and-loop-wrapper)

With the colossal system prompt defined, we now instantiate the agent and wrap it in a continuous loop.

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

21

22

23

24

25

26

27

strict\_agent = \_create\_agent(

Agent,

name="strict\_multimodal\_agent",

model=model\_name,

instruction=strict\_instruction,

tools=[

capture\_multimodal\_observation,

action\_click,

action\_input,

action\_scroll,

action\_wait,

action\_back,

action\_google,

action\_answer,

reset\_browser\_task\_state,

log\_step,

],

)

try:

loop\_max\_iters = int(os.getenv("ADK\_LOOP\_MAX\_ITERS", "15"))

return \_create\_workflow\_agent(

LoopAgent,

name="strict\_multimodal\_root",

sub\_agents=[strict\_agent],

max\_iterations=loop\_max\_iters,

)

except Exception:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Binding the strict agent and wrapping it in a LoopAgent (web\_agent.py)

- **Lines 1–18:** Using our `_create_agent` helper, we instantiate `strict_agent`. Notice that we bind a limited subset of tools (`action_click`, `action_input`, `action_scroll`, etc.) that cleanly map to the seven formatting actions defined in the system prompt above. We also include logging and state reset tools.
- **Lines 19–26:** A standard LLM call fires only once. To create a continuous browsing experience, we wrap `strict_agent` inside an ADK `LoopAgent`. We cap the iterations using `loop_max_iters`, which defaults to 15, to prevent infinite loops and runaway API costs.
- **Lines 27–28:** If constructing the loop fails, for example, due to an ADK framework configuration issue, we catch the exception and safely return the standalone `strict_agent` as a functional fallback.

### Single agent mode configuration[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Single-agent-mode-configuration)

If the application is not running in strict mode, it evaluates the `ADK_SINGLE_AGENT_MODE` variable. This mode configures the system to run as a single, conversational WebVoyager-style agent. This is often the simplest mode for demonstrations because it avoids the complexity of transferring context between multiple sub-agents.

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

21

22

23

24

25

26

# If enabled, run as a single agent with tools (no agent transfer).

# This avoids provider/tool-schema validation issues around transfer\_to\_agent

# and is the most reliable mode for demos.

if os.getenv("ADK\_SINGLE\_AGENT\_MODE", "true").strip().lower() == "true":

single\_instruction = (

"You are a WebVoyager-style multimodal web agent. "

"Follow a strict one-action-per-iteration ReAct loop: Thought -> one Action tool call -> Observation. "

"When user intent is ambiguous or under-specified, ask a concise follow-up question before taking risky actions. "

"If website choice matters and user did not specify one, ask for preference (for example Google Flights, Skyscanner, Trip.com) or proceed with a safe default and state it. "

"Google Search first rule: unless the user provides a website, call search\_web(query) first to find a relevant site. "

"Do not remain on search result pages unless the user asked for SERP analysis; open a relevant result and continue task execution. "

"After every navigation or action, call capture\_multimodal\_observation for fused DOM+vision grounding. "

"Act using element IDs: prefer click\_element/type\_text\_element. "

"IMPORTANT: element\_id values are numeric strings like '0','1','2' taken from the latest observation. "

"Never invent element IDs; if unsure, capture\_observation again and choose from the returned web\_elements\_text list. "

"For date pickers and dropdown widgets: click to open the widget first, capture\_observation again, then choose day/option cells by fresh element IDs. "

"Do not try typing into read-only date fields unless the site clearly supports direct text entry. "

"For flight/travel sites, prefer select\_flight\_dates(departure\_text, return\_text) when date widgets are complex. "

"If a click/type action does not change page state, immediately recapture and try a different element\_id rather than repeating the same action. "

"Use wait(seconds=5) when waiting for dynamic content. Use go\_back() to undo navigation mistakes. Use go\_google() to restart from Google. "

"Only finalize success after calling verify\_task\_completion(...) with task-critical evidence text and getting status='verified'. "

"For transparency, at each step call log\_step(stage, thought, observation, action, values) to log your ReAct loop. "

"Never place final orders or do irreversible actions unless user explicitly asks. "

"Before final answer, you MUST reference at least one concrete insight from vlm\_analysis and map it to element\_id actions. "

"In your final answer, include a short Process Log with labeled\_screenshot\_path values and element\_id actions."

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Checking the environment variable and defining the Single Agent Instruction (web\_ agent.py )

- **Line 4:** We check whether `ADK_SINGLE_AGENT_MODE` is enabled (it defaults to `"true"` if missing). The comments explicitly note that this mode avoids `transfer_to_agent` validation issues.
- **Lines 6–7:** We define the agent's core identity and mandate a strict ReAct loop ("Thought -> one Action tool call -> Observation"). This ensures that the model explicitly reasons about its next move before executing a tool.
- **Lines 8–9:** The agent is instructed to handle ambiguity defensively by asking follow-up questions or stating defaults if the user doesn't specify a target website.
- **Lines 10–11:** The "Google Search first rule" guides initial discovery and explicitly instructs the agent not to stall on search engine results pages (SERPs).
- **Line 12:** The agent is required to call `capture_multimodal_observation` after every action to maintain its visual grounding.
- **Lines 13–15:** These are the critical grounding safety rules. The agent must use numeric `element_id` strings (like `'0'`) and is strictly forbidden from inventing IDs.
- **Lines 16–18:** Specific heuristics are provided for difficult UI elements: how to handle dropdowns and date pickers, avoid read-only fields, and use the specialized `select_flight_dates` tool for complex travel sites.
- **Lines 19–20:** Self-correction instructions tell the agent to recapture the screen if an action fails and explicitly list recovery tools like `wait`, `go_back`, and `go_google`.
- **Lines 21–25:** Finally, we define completion and transparency rules. The agent must verify evidence via `verify_task_completion`, log its steps, map VLM insights to actions, and provide a Process Log in its final answer.

#### Binding tools and the loop wrapper[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-tools-and-the-loop-wrapper)

With the instruction established, we instantiate the single ADK agent, equip it with our extensive toolset, and wrap it in a loop.

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

21

22

23

24

25

26

27

single\_agent = \_create\_agent(

Agent,

name="multimodal\_web\_agent",

model=model\_name,

instruction=single\_instruction,

tools=[

navigate,

search\_web,

capture\_observation,

capture\_multimodal\_observation,

analyze\_screenshot\_with\_vlm,

click\_element,

type\_text\_element,

select\_flight\_dates,

scroll\_by,

wait,

go\_back,

go\_google,

verify\_task\_completion,

log\_step,

close\_browser,

],

)

# Wrap the single agent in a LoopAgent so the system keeps iterating

# even if the model returns STOP after a partial step.

try:

loop\_max\_iters = int(os.getenv("ADK\_LOOP\_MAX\_ITERS", "15"))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Creating the Single Agent and wrapping it in a LoopAgent (web\_ agent.py )

- **Lines 1–23:** Using our helper `_create_agent`, we instantiate `single_agent`, naming it `"multimodal_web_agent"`. We bind the full list of conversational tools imported from `web_tools.py`. Unlike Strict Mode, this agent gets access to complex functions like `search_web`, `analyze_screenshot_with_vlm`, and `verify_task_completion`.
- **Lines 26–33:** We attempt to wrap the agent in a `LoopAgent`. We fetch `ADK_LOOP_MAX_ITERS` (defaulting to 15), then call `_create_workflow_agent`. If successful, this looping root agent is returned to `agent.py`.
- **Lines 34–35:** If the workflow wrapper fails due to framework incompatibility, we catch the exception and return the base `single_agent`.

### Multi-agent orchestration (delegating tasks)[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Multi-agent-orchestration-delegating-tasks)

If both Strict Mode and Single Agent Mode are disabled, the code falls through to the most advanced architecture: a multi-agent hierarchy.

Giving one LLM context window 15 different tools can cause it to get confused. Instead, we create specialized experts: a Planner, a Browser (hands), a Vision agent (eyes), and a Coordinator to manage them.

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

21

22

23

24

25

26

27

planner\_instruction = (

"You are PlannerAgent. The user gives open-ended natural-language web goals. "

"Break each goal into short, safe steps for web execution, including target website selection when unspecified. "

"If the task is vague (missing constraints like site, dates, budget, filters, or output format), ask targeted follow-up questions first. "

"When tradeoffs exist across websites, ask user preference explicitly; if no preference is provided, select a sensible default and mention it. "

"Google Search first rule: Unless the user explicitly provides a target website, begin by navigating to Google Search "

"(`https://www.google.com`), entering the appropriate query, and opening the most relevant safe result. "

"After opening a result, immediately capture a multimodal observation before taking further actions. "

"Ask for an updated observation whenever confidence is low. Keep plans explicit and actionable."

)

browser\_instruction = (

"You are BrowserAgent and you execute actions using tools. "

"Use this strict loop for transparency: navigate -> capture\_multimodal\_observation -> act using element\_id -> capture\_multimodal\_observation -> repeat. "

"Prefer `click\_element(element\_id)` and `type\_text\_element(element\_id, text)` over raw CSS selectors. "

"Only use `click(selector)`/`type\_text(selector, ...)` when an element\_id is not available. "

"For search boxes, prefer `type\_text\_element(element\_id, query, press\_enter=true)` unless the page clearly shows a clickable search/submit button. "

"For calendar/date widgets, first click the date field, then capture a fresh observation and click explicit day cells by element\_id. "

"If date widget interactions are unstable, call `select\_flight\_dates(departure\_text, return\_text)` directly. "

"Use wait(seconds=5), go\_back(), and go\_google() as explicit recovery actions. "

"Before completion, call verify\_task\_completion(...) and require status='verified'. "

"Never perform destructive or irreversible actions unless user explicitly asks. "

)

vision\_instruction = (

"You are VisionAgent. Use capture\_multimodal\_observation() as the primary observation API. "

"Ground every recommendation in element IDs and bounding boxes from the element list. "

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Defining specialized system prompts for the multi-agent team (web\_ agent.py)

- **Lines 1–10:** `planner_instruction` sets up the high-level reasoning agent. It is instructed to handle ambiguity, break goals into safe steps, and enforce the "Google Search first rule."
- **Lines 12–23:** `browser_instruction` sets up the execution agent. Its instructions focus entirely on mechanical interactions, preferring `element_id` tool calls, managing dropdowns, and using recovery actions like `wait` or `go_back`.
- **Lines 25–30:** `vision_instruction` sets up the observation agent. It is tasked with grounding recommendations strictly in element IDs and providing spatial reasoning via the VLM.
- **Lines 32–40:** `coordinator_instruction` sets up the manager. It doesn't browse; it delegates subtasks to the Planner, Vision, and Browser agents, and generates the final Process Log.

Now, we create and nest the agents:

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

21

22

23

24

25

26

27

planner\_agent = \_create\_agent(

Agent,

name="planner\_agent",

model=model\_name,

instruction=planner\_instruction,

tools=[],

)

browser\_agent = \_create\_agent(

Agent,

name="browser\_agent",

model=model\_name,

instruction=browser\_instruction,

tools=[

navigate,

capture\_observation,

capture\_multimodal\_observation,

click\_element,

type\_text\_element,

select\_flight\_dates,

scroll\_by,

wait,

go\_back,

go\_google,

verify\_task\_completion,

close\_browser,

],

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Instantiating the specialized agents and wrapping them in a LoopAgent (web\_ agent.py)

- **Lines 1–7:** The `planner_agent` is instantiated with zero tools (`tools=[]`). It relies purely on its logic.
- **Lines 9–28:** The `browser_agent` is the "hands." It is given only navigational and physical interaction tools (like `Maps`, `click_element`, and `scroll_by`).
- **Lines 30–36:** The `vision_agent` is the "eyes." It is restricted to screenshot tools and the heavy VLM analysis tool (`analyze_screenshot_with_vlm`).
- **Lines 38–45:** The `coordinator_agent` manages the team. It is given the three specialized agents via the `sub_agents` parameter and holds no direct web tools of its own.
- **Lines 48–52:** This block acts as a backward-compatibility patch for certain ADK versions, manually injecting the `sub_agents` array if the constructor dropped them.
- **Lines 54–56:** We check the `ADK_ENABLE_WORKFLOW_AGENT` environment flag. If workflows are disabled, we return the base `coordinator_agent`.
- **Lines 58–70:** Finally, we wrap the entire multi-agent structure inside a `LoopAgent`. As the comments note, we attach the Planner, Vision, and Browser directly as `sub_agents` to the workflow root. This ensures that the built-in `transfer_to_agent` mechanism in ADK correctly validates the agent names.
- **Lines 71–73:** If building the `LoopAgent` fails, it safely falls back to returning the `coordinator_agent`.

### Conclusion[#](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Conclusion)

Congratulations! We traced the implementation of an end-to-end multimodal web agent using Google ADK. In this chapter, we learned how to:

- Trace execution using artifacts (screenshots and JSON logs) to verify the agent's behavior.
- Bridge the gap between stateless LLM APIs and stateful web browsing using a singleton `BrowserRuntime` and Playwright.
- Visually ground the agent by extracting DOM elements, capturing screenshots, and annotating them with numeric IDs for the VLM.
- Orchestrate the LLM by configuring robust system prompts and organizing specialized agents (Planner, Vision, and Browser) into a resilient `LoopAgent` execution cycle.

We now have the foundational knowledge and practical code structure to build, debug, and expand AI systems that can see and interact with the web.

Building Multimodal Web Tools

Introduction to MuLan and the Multi-Object Generation Challenge

Ask

[The agent architecture flow](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-agent-architecture-flow)

[Imports and helper functions](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Imports-and-helper-functions)

[The factory entry and strict mode](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#The-factory-entry-and-strict-mode)

[Binding the strict agent and loop wrapper](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-the-strict-agent-and-loop-wrapper)

[Single agent mode configuration](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Single-agent-mode-configuration)

[Binding tools and the loop wrapper](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Binding-tools-and-the-loop-wrapper)

[Multi-agent orchestration (delegating tasks)](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Multi-agent-orchestration-delegating-tasks)

[Conclusion](https://www.educative.io/courses/agentic-ai-systems/assembling-the-web-agent-with-google-adk#Conclusion)