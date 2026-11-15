# Understanding_Google's_Agent_Platform_and_ADK_Framework

Source: https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Agent Platform and ADK

Explore what Gemini Enterprise Agent Platform provides across building, scaling, governing, and optimizing agents. Learn the core building blocks of the Agent Development Kit, including agents, tools, workflow agents, sessions, and callbacks, and how to enforce business rules in code.

We'll cover the following...

- [What the Agent Platform provides](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#What-the-Agent-Platform-provides)
- [The role of ADK](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#The-role-of-ADK)
- [ADK building blocks at a glance](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#ADK-building-blocks-at-a-glance)
- [Callbacks as guardrails](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#Callbacks-as-guardrails)

When a customer moves from a single Gemini API call to a production agent, the engineering problem changes. The system now needs to manage conversations across many turns, call tools safely, keep memory between sessions, run reliably at scale, and give security and operations teams the controls they expect. Building all of this from scratch for every engagement would slow delivery and introduce risk. Google’s answer is a managed platform for the surrounding infrastructure and an open-source framework for the agent logic itself.

Gemini Enterprise Agent Platform provides the managed infrastructure, and the Agent Development Kit (ADK) provides the framework. FDE interviewers expect candidates to know what each one is responsible for, where the boundary between them sits, and how an ADK agent is structured. The sections below cover the platform’s capabilities first and then the core building blocks of ADK.

## What the Agent Platform provides[#](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#What-the-Agent-Platform-provides)

Google introduced Gemini Enterprise Agent Platform in April 2026 as the evolution of Vertex AI. It brings model access, agent building, runtime, governance, and optimization into one platform. Google groups its capabilities into four areas, and this grouping is a useful way to explain the platform in an interview.

|  |  |  |
| --- | --- | --- |
| **Area** | **Purpose** | **Key capabilities** |
| Build | Create agents and choose models | Agent Development Kit, Agent Studio (low-code), Agent Garden (templates), Model Garden |
| Scale | Run agents reliably in production | Agent Runtime, Agent Sessions, Agent Memory Bank, Agent Sandbox |
| Govern | Control identity, access, and risk | Agent Identity, Agent Registry, Agent Gateway with Model Armor, threat and anomaly detection |
| Optimize | Measure and improve agent quality | Agent Simulation, Agent Evaluation, Agent Observability, Agent Optimizer |

Each area answers a question that enterprise customers ask during a deployment.

- **Build** answers how the agent is created and which model it uses.
- **Scale** answers where the agent runs and how it remembers context. Agent Runtime hosts agents as a managed service, Agent Sessions stores the history of a conversation, and Agent Memory Bank keeps useful information across separate conversations.
- **Govern** answers who the agent acts as and what it is allowed to do. Agent Identity gives each agent an accountable identity, Agent Registry tracks which agents exist in the organization, and Agent Gateway screens traffic for threats such as prompt injection.
- **Optimize** answers whether the agent is working and how to make it better.

Agents built on the platform can be delivered to employees through the Gemini Enterprise app, or exposed through APIs and custom applications. This flexibility matters because some customers want a ready-made interface for a fast pilot, while others need the agent embedded in tools their teams already use.

Customers and documentation may still use earlier names, such as Vertex AI Agent Engine for what is now Agent Runtime. In interviews and customer conversations, describing what the component does is more important than which name is used.

The platform handles the infrastructure. The logic of the agent itself is written with ADK.

## The role of ADK[#](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#The-role-of-ADK)

ADK is an open-source framework for defining agents in code. It is available in Python and other languages, and it is model-agnostic, although it is optimized for Gemini and Google Cloud. An ADK agent can run on a developer’s laptop, in Cloud Run, in GKE, or in Agent Runtime without changes to its core logic.

This portability shapes how FDEs use it. The same agent can be built and tested locally during a proof of concept, then deployed to the runtime that best fits the customer’s constraints. The boundary is clear: ADK defines what the agent does, and the platform or another runtime determines where and how it runs.

ADK is built from a small set of building blocks.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271080%27%20height=%27652%27/%3e)![Gemini Enterprise Agent Platform](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Gemini Enterprise Agent Platform")

Gemini Enterprise Agent Platform

## ADK building blocks at a glance[#](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#ADK-building-blocks-at-a-glance)

Look at the table below to see what components are the building blocks of of ADK.

|  |  |
| --- | --- |
| **Components** | **Functions** |
| Agent | Combines a model, instructions, and tools into a unit that can reason and act |
| Tools | Functions, built-in tools, MCP tools, or other agents that the agent can call |
| Workflow agents | Sequential, parallel, and loop agents that run sub-agents in a fixed pattern |
| Runner | Executes the agent, manages the event loop, and connects it to services |
| Session and state | Stores the conversation history and short-term data for one conversation |
| Memory | Stores information that should persist across separate conversations |
| Callbacks | Hooks that run before or after model and tool calls, used for guardrails and logging |

- The **agent** is the central unit. An LLM-based agent uses a model to decide which tool to call and what to say.
- **Workflow agents** are different: a sequential agent runs sub-agents in order, a parallel agent runs them at the same time, and a loop agent repeats them until a condition is met. Workflow agents make the overall process predictable, while the LLM agents inside them handle the steps that need judgment.
- **Tools** in ADK can be plain Python functions, built-in tools such as Google Search, tools exposed by MCP servers, or other agents wrapped as tools. ADK reads a function’s name, type hints, and docstring to describe it to the model, so well-written docstrings directly improve how reliably the agent uses its tools.
- The **runner** and **session** services handle what the raw API leaves to the application. In the previous Gemini API examples, the application managed the conversation history manually. In ADK, the session service stores events automatically, and session state lets tools and agents share data during a conversation.

The following example defines a simple support agent with two tools.

Please provide values for the following:

GOOGLE\_GEMINI\_API\_KEY

Import Values from JSON

Python 3.14.0

```
from google.adk.agents import Agent

MODEL_ID = "gemini-3.6-flash"

def get_order_status(order_id: str) -> dict:

"""Looks up the shipping status of a customer order.

Args:

order_id: The customer's order number.

"""

return {"order_id": order_id, "status": "shipped", "carrier": "UPS"}

def request_refund(order_id: str, amount: float) -> dict:

"""Submits a refund request for human approval."""

return {"order_id": order_id, "amount": amount, "state": "pending_approval"}

root_agent = Agent(

name="order_support_agent",

model=MODEL_ID,

description="Answers order status questions and submits refund requests.",

instruction=(

"Help customers with their orders. Use get_order_status for shipping questions. "

"Use request_refund only when the customer asks for a refund. "

"Never promise that a refund is approved."

),

tools=[get_order_status, request_refund],

)

import asyncio, os

from google.adk.runners import InMemoryRunner

from google.genai import types

os.environ["GOOGLE_API_KEY"] = "{{GOOGLE_GEMINI_API_KEY}}"

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

async def main():

runner = InMemoryRunner(agent=root_agent, app_name="order_support")

session = await runner.session_service.create_session(app_name="order_support", user_id="learner")

for question in ["Where is order 1042?", "I'd like a refund of $40 for order 1042."]:

print("\nUser:", question)

message = types.Content(role="user", parts=[types.Part(text=question)])

async for event in runner.run_async(user_id="learner", session_id=session.id, new_message=message):

for call in event.get_function_calls():

print("Tool call:", call.name, call.args)

if event.is_final_response() and event.content and event.content.parts:

print("Agent:", event.content.parts[0].text)

asyncio.run(main())
```

⋯

- **Line 1:** We import `Agent`, ADK’s standard LLM-based agent class.
- **Line 3:** We store the model ID in one variable so it can be changed without editing the agent definition.
- **Lines 5–11:** `get_order_status` is a plain Python function used as a tool. ADK reads its name, type hints, and docstring to describe it to the model.
- **Lines 8–9:** The `Args` section of the docstring explains each parameter, which helps the model pass the correct value.
- **Lines 13–15:** `request_refund` returns a `pending_approval` state instead of issuing a refund, keeping a human in the loop for a high-risk action.
- **Line 17:** `root_agent` is the name ADK’s developer tools look for when loading an agent.
- **Line 18:** The `name` identifies the agent in logs, traces, and multi-agent systems.
- **Line 20:** The `description` tells other agents what this agent does, which matters when it becomes a sub-agent.
- **Lines 21–25:** The `instruction` sets the agent’s behavior, including when to use each tool and what not to promise.
- **Line 26:** Passing the functions in `tools` makes them available to the model. ADK handles the function calling loop automatically.
- **Lines 28 onward:** An in-memory runner sends two sample questions to the agent and prints each tool call and the agent’s final reply.

During development, running `adk web` in the project directory opens a local interface for chatting with the agent and inspecting each event, tool call, and state change. This makes it practical to debug agent behavior before deployment.

Instructions guide the agent, but they are not enforcement. Callbacks provide a way to enforce rules in code.

## Callbacks as guardrails[#](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#Callbacks-as-guardrails)

Callbacks run at defined points in the agent’s execution, such as before a model call or before a tool call. A callback can inspect the request, log it, modify it, or block it. This is where FDEs place rules that must hold regardless of what the model decides.

Please provide values for the following:

GOOGLE\_GEMINI\_API\_KEY

Import Values from JSON

Python 3.14.0

```
from google.adk.tools.base_tool import BaseTool

from google.adk.tools.tool_context import ToolContext

from order_tools import Agent, MODEL_ID, get_order_status, request_refund

REFUND_LIMIT = 100.0

def check_refund_limit(tool: BaseTool, args: dict, tool_context: ToolContext):

if tool.name == "request_refund" and args.get("amount", 0) > REFUND_LIMIT:

return {"error": "Refunds above the limit must be handled by a human agent."}

return None

root_agent = Agent(

name="order_support_agent",

model=MODEL_ID,

instruction="Help customers with order status and refund requests.",

tools=[get_order_status, request_refund],

before_tool_callback=check_refund_limit,

)

import asyncio, os

from google.adk.runners import InMemoryRunner

from google.genai import types

os.environ["GOOGLE_API_KEY"] = "{{GOOGLE_GEMINI_API_KEY}}"

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

async def main():

runner = InMemoryRunner(agent=root_agent, app_name="order_support")

session = await runner.session_service.create_session(app_name="order_support", user_id="learner")

for question in ["Please refund $40 for order 1042.", "Please refund $250 for order 1042."]:

print("\nUser:", question)

message = types.Content(role="user", parts=[types.Part(text=question)])

async for event in runner.run_async(user_id="learner", session_id=session.id, new_message=message):

for call in event.get_function_calls():

print("Tool call:", call.name, call.args)

for resp in event.get_function_responses():

print("Tool result:", resp.response)

if event.is_final_response() and event.content and event.content.parts:

print("Agent:", event.content.parts[0].text)

asyncio.run(main())
```

⋯

- **Lines 1–2:** We import `BaseTool` and `ToolContext`, the types ADK passes to a tool callback.
- **Line 3:** We import the agent class, model ID, and the two order tools defined in the previous example.
- **Line 4:** The refund limit is defined once as a business rule, so it can be reviewed and changed without touching the agent.
- **Line 6:** `check_refund_limit` is a callback that runs before every tool call. It receives the tool, the arguments the model chose, and the tool context.
- **Lines 7–8:** If the model tries to call `request_refund` with an amount above the limit, the callback returns an error instead of letting the tool run.
- **Line 9:** Returning `None` lets the tool call proceed normally.
- **Lines 11–17:** We create the agent with the same tools as before.
- **Line 16:** `before_tool_callback` attaches the check, so every tool call passes through it. The model can request a large refund, but the application decides whether it runs.
- **Lines 20–22:** We import `asyncio`, the in-memory runner that executes the agent, and the content types used to send messages.
- **Lines 24–25:** We pass the API key to ADK and tell it to use the Gemini Developer API rather than Google Cloud.
- **Line 28:** `InMemoryRunner` runs the agent locally and keeps session state in memory, which suits testing and demos.
- **Line 29:** We create a session, which holds the conversation history for one user.
- **Line 31:** We send two refund requests, one below the limit and one above it.
- **Line 33:** Each question is wrapped as a user message.
- **Line 34:** `run_async` streams events as the agent works, including tool calls, tool results, and the final reply.
- **Lines 35–36:** We print each tool call the model makes, with the arguments it chose.
- **Lines 37–38:** We print each tool result. For the $250 request, this shows the error returned by the callback rather than a refund.
- **Lines 39–40:** When the agent produces its final response, we print the reply.
- **Line 42:** `asyncio.run` starts the async `main` function.

This pattern reflects a principle interviewers look for: the model can be persuaded or make mistakes, so critical limits belong in code that runs outside the model’s control.

The Agent Platform and ADK divide the work of an enterprise agent into two clear responsibilities. ADK defines the agent’s logic, tools, workflows, and guardrails in portable code, while the platform provides the runtime, memory, identity, governance, and evaluation needed to operate it in production. Being able to explain that boundary, and to show how an ADK agent enforces rules through callbacks rather than instructions alone, gives an FDE a strong foundation for any agentic system design discussion.

The Gemini API

MCP Tool Integration

Ask

[What the Agent Platform provides](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#What-the-Agent-Platform-provides)

[The role of ADK](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#The-role-of-ADK)

[ADK building blocks at a glance](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#ADK-building-blocks-at-a-glance)

[Callbacks as guardrails](https://www.educative.io/courses/forward-deployed-engineer/the-agent-platform-and-adk#Callbacks-as-guardrails)