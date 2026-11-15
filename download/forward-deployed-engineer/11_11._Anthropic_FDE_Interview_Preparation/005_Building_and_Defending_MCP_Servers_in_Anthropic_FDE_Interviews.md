# Building_and_Defending_MCP_Servers_in_Anthropic_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# MCP for the Technical Use Case Screen

Explore how to design and defend an MCP server for Anthropic's Forward Deployed Engineer interviews. Understand server construction using the Python MCP SDK, testing without a model, and safe tool exposure. Learn to connect the server to Claude, handle errors, and respond to common interview probes to demonstrate practical deployment experience.

We'll cover the following...

- [Building an MCP server in Python](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-an-MCP-server-in-Python)
- [Testing the server without Claude](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Testing-the-server-without-Claude)
- [Tool descriptions Claude reads](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Tool-descriptions-Claude-reads)
- [Connecting the server to Claude](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Connecting-the-server-to-Claude)
- [Defending the server in the screen](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Defending-the-server-in-the-screen)
- [Building servers worth defending](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-servers-worth-defending)

Anthropic’s technical use case screen centers on deploying Claude with MCP. Candidates who have only read about the protocol tend to describe it in general terms. Candidates who have built a server can explain where its tools come from, what Claude sees of them, how the server connects, and what happens when it fails. Interviewers look for that second kind of answer.

The **Model Context Protocol (MCP)** is the open standard Anthropic introduced for connecting AI applications to external tools and data. An **MCP server** exposes tools and data through the protocol, and an **MCP client** inside an application, such as an agent, discovers and calls them. MCP servers are also one of the deliverables Anthropic’s FDE posting names directly, so building one is core FDE work.

![](005_Building_and_Defending_MCP_Servers_in_Anthropic_FDE_Interviews_images/img_63758235f3d1.svg)

The examples build an expense policy server for the expense audit scenario, then test it, then connect it to Claude.

## Building an MCP server in Python[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-an-MCP-server-in-Python)

The Python MCP SDK builds a server from ordinary functions. A function decorated with `@mcp.tool()` becomes a **tool**, an action Claude can call. A function decorated with `@mcp.resource()` becomes a **resource**, read-only data an application can load by its address. Each function’s type hints become its input schema, and its docstring becomes the description Claude reads.

The code below is the server file, `expense_policy_server.py`. The test client and the agent later in the lesson both start it by that name.

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

from datetime import date

from mcp.server import MCPServer

from mcp.server.mcpserver.exceptions import ToolError

POLICY\_LIMITS\_USD = {"meals": 75.00, "lodging": 350.00, "airfare": 2500.00}

SUBMISSION\_WINDOW\_DAYS = 30

mcp = MCPServer("expense-policy", log\_level="WARNING")

@mcp.resource("policy://travel-and-expense")

def policy\_summary() -> str:

"""The company's travel and expense policy in brief."""

return "Meals up to $75, lodging up to $350 per night, airfare up to $2,500. Submit receipts within 30 days."

@mcp.tool()

def get\_policy\_limit(category: str) -> dict:

"""Return the per-expense limit in US dollars for one category. Valid categories are meals, lodging, and airfare."""

if category not in POLICY\_LIMITS\_USD:

raise ToolError(f"Unknown category {category}. Use one of: meals, lodging, airfare.")

return {"category": category, "limit\_usd": POLICY\_LIMITS\_USD[category]}

@mcp.tool()

def check\_receipt\_age(receipt\_date: str, submitted\_date: str) -> dict:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Building an expense policy MCP server with one resource and two tools that run over stdio

- **Lines 3–4:** We imported `MCPServer` to build the server and `ToolError` to report failures that Claude should read.
- **Lines 6–7:** We created the policy limits and the 30-day submission window, which stand in for the company’s policy system.
- **Line 9:** We created a server named `expense-policy` that logs only warnings and errors, so routine messages stay out of the output.
- **Lines 12–15:** We exposed a short policy summary as a resource at the address `policy://travel-and-expense`.
- **Lines 18–23:** We defined `get_policy_limit` as a tool. It raises `ToolError` with the valid categories when it receives one it does not know.
- **Lines 26–33:** We defined `check_receipt_age`, which counts the days between a receipt and its submission and checks them against the 30-day window. A badly formatted date raises `ToolError` with an example of the right format.
- **Lines 36–37:** We started the server on the stdio transport, which talks to the client through standard input and output.

The server never mentions Claude. It describes its tools through the protocol, so any MCP client can discover and use them. `ToolError` matters here because it passes a clear message back to the model, while any other exception reaches the client as a generic failure that hides the cause.

A server is only worth connecting to Claude once we know it works, and the fastest way to know is to call it without a model.

## Testing the server without Claude[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Testing-the-server-without-Claude)

An MCP client can start the server, list its tools, and call them directly. This test separates server bugs from model behavior, which is the first thing a debugging interviewer wants to see. If the server fails here, Claude was never the problem.

The client below starts `expense_policy_server.py` as a subprocess, prints what the server exposes, and calls one tool twice.

```
import asyncio

from mcp import Client, StdioServerParameters

# Start the expense policy server as a subprocess and talk to it over stdio.
SERVER = StdioServerParameters(command="python", args=["expense_policy_server.py"])

async def main():
    async with Client(SERVER) as client:
        # These names and descriptions are exactly what Claude reads.
        tools = await client.list_tools()
        for tool in tools.tools:
            print(f"Tool: {tool.name} | {tool.description}")

        policy = await client.read_resource("policy://travel-and-expense")
        print("Resource:", policy.contents[0].text)

        limit = await client.call_tool("get_policy_limit", {"category": "meals"})
        print("Meals limit:", limit.content[0].text)

        missing = await client.call_tool("get_policy_limit", {"category": "parking"})
        print("Unknown category:", missing.is_error, missing.content[0].text)

asyncio.run(main())
```

Testing the expense policy server with an MCP client, with no model involved

- **Line 6:** We told the client to start the server file with `python`.
- **Lines 12–14:** We listed the server’s tools and printed each name with its description.
- **Lines 16–17:** We read the policy resource by its address and printed its text.
- **Lines 19–20:** We called `get_policy_limit` for meals and printed the result.
- **Lines 22–23:** We called it with a category that does not exist and printed the error flag and message.

Here is what the client printed.

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

Tool: get\_policy\_limit | Return the per-expense limit in US dollars for one category. Valid categories are meals, lodging, and airfare.

Tool: check\_receipt\_age | Check whether a receipt was submitted within the 30-day window. Dates use YYYY-MM-DD.

Resource: Meals up to $75, lodging up to $350 per night, airfare up to $2,500. Submit receipts within 30 days.

Meals limit: {

"category": "meals",

"limit\_usd": 75.0

}

Unknown category: True Error executing tool get\_policy\_limit: Unknown category parking. Use one of: meals, lodging, airfare.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The unknown category came back as an error result with the valid choices in the message, which gives Claude what it needs to retry correctly. The first two lines deserve a closer look because they are the only thing Claude knows about these tools.

## Tool descriptions Claude reads[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Tool-descriptions-Claude-reads)

Tool descriptions are prompt text. Claude decides which tool to call, and with which arguments, from the name, the description, and the input schema alone. The two descriptions above came straight from the docstrings, and each one tells Claude both what the tool does and how to call it correctly, with valid categories and the date format.

Three habits keep descriptions useful and safe.

- **Say when to use the tool:** A description that names the situation, such as checking a receipt against the 30-day window, helps Claude pick the right tool on the first try.
- **State valid inputs:** Listing allowed values and formats prevents a round of failed calls.
- **Keep sensitive details out:** Descriptions reach the model in every request, so internal hostnames, credentials, and data the user should not see stay out of them.

This connects to a principle interviewers probe directly. A **least-privilege tool surface** exposes only the tools a workflow needs, with read tools separated from tools that change data. Our server offers two read-only tools, so Claude can look up policy but cannot change a report.

With the server tested and its descriptions in shape, the next step is connecting it to Claude.

## Connecting the server to Claude[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Connecting-the-server-to-Claude)

The Agent SDK starts stdio servers itself. We register the server under a name in `mcp_servers`, with the command that launches it, and approve its tools by their full names.

In the code below, we connect an expense audit agent to the server and ask a question that needs both tools.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

```
import asyncio

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock, query

options = ClaudeAgentOptions(
    model="claude-sonnet-5-5",
    system_prompt="You are an expense audit assistant. Use the expense policy tools to answer policy questions.",
    env={"ANTHROPIC_API_KEY": "{{ANTHROPIC_API_KEY}}"},
    mcp_servers={
        "expense-policy": {"command": "python", "args": ["expense_policy_server.py"]},
    },
    tools=[],
    allowed_tools=["mcp__expense-policy__get_policy_limit", "mcp__expense-policy__check_receipt_age"],
)

PROMPT = (
    "Dana submitted a $68.40 meals receipt dated 2026-09-10 on 2026-10-20. "
    "Is it within the meals limit, and was it submitted on time?"
)

async def main():
    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print("Tool call:", block.name, block.input)
        elif isinstance(message, ResultMessage):
            print("\n" + message.result)

asyncio.run(main())
```

Connecting an expense audit agent to the stdio policy server and answering a two-part policy question

- **Lines 9–11:** We registered the server as `expense-policy` with the command that starts `expense_policy_server.py`.
- **Line 12:** We turned off the built-in tools, so the agent works only through our server.
- **Line 13:** We approved the two tools by their full names, which follow the pattern `mcp__<server>__<tool>`.
- **Lines 16–19:** We wrote a question that needs both the meals limit and the receipt age.
- **Lines 23–29:** We ran the agent, printed each tool call, and printed the final answer.

The agent’s run produced the following.

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

Tool call: mcp\_\_expense-policy\_\_get\_policy\_limit {'category': 'meals'}

Tool call: mcp\_\_expense-policy\_\_check\_receipt\_age {'receipt\_date': '2026-09-10', 'submitted\_date': '2026-10-20'}

Dana's receipt is within the meals limit but was submitted late.

- \*\*Meals limit:\*\* The $68.40 receipt is under the $75.00 per-expense limit, with $6.60 to spare.

- \*\*Submission timing:\*\* The receipt is dated 2026-09-10 and was submitted 2026-10-20. That is 40 days, which is 10 days past the 30-day window.

Because it missed the window, the expense is non-compliant. It would need a policy exception or approval to be reimbursed.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Claude found both tools from their descriptions, passed the dates in the format the description asked for, and combined the two results into one answer. We approved each tool by its full name instead of a wildcard, so a tool added to the server later cannot quietly widen what the agent can do.

![One MCP server can serve many Claude clients](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "One MCP server can serve many Claude clients")

One MCP server can serve many Claude clients

A local stdio server suits an agent that runs inside the customer’s environment. Applications built directly on the Messages API have a second option: servers hosted elsewhere.

The **MCP connector** lets a Messages API request use a remote MCP server without any client code. It is in beta and requires the `mcp-client-2025-11-20` beta header. The request lists the server by URL in `mcp_servers` and adds an `mcp_toolset` entry to `tools`. The snippet below shows only those request fields, since the connector needs a server at a public HTTPS address.

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

client.beta.messages.create(

model="claude-sonnet-5-5",

max\_tokens=1024,

messages=[...],

mcp\_servers=[{"type": "url", "url": "https://policy.example.com/mcp", "name": "expense-policy", "authorization\_token": "..."}],

tools=[{"type": "mcp\_toolset", "mcp\_server\_name": "expense-policy"}],

betas=["mcp-client-2025-11-20"],

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The request fields that connect a remote MCP server through the Messages API connector

The connector comes with limits worth knowing before an interview.

- **Tools only:** It supports MCP tool calls, so resources and other MCP features stay out of reach.
- **Public HTTPS:** The server must be reachable over HTTPS with Streamable HTTP or SSE, so local stdio servers cannot connect.
- **Data retention:** It is not eligible for zero data retention, which matters for customers with strict data rules.

The table below sums up the three ways an FDE can give Claude custom tools.

|  |  |  |
| --- | --- | --- |
| **Option** | **How It Connects** | **Fits When** |
| In-process SDK tools | Python functions served inside the agent’s own process | The tools belong to one agent and need no reuse elsewhere |
| Local MCP server through the Agent SDK | The SDK starts the server as a subprocess over stdio | The agent runs inside the customer’s environment, or the server needs resources |
| Remote MCP server through the connector | A Messages API request reaches the server over HTTPS | Several applications share one hosted server and only need its tools |

Knowing how the pieces connect prepares us for the questions that follow every MCP design.

## Defending the server in the screen[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Defending-the-server-in-the-screen)

After a candidate presents an MCP design, interviewers probe the edges of it. Five questions are worth preparing for, and each one has a concrete answer.

- **Authentication:** Credentials go in the server’s own configuration, such as an `env` entry or the connector’s authorization token, so they never appear in prompts or tool descriptions.
- **Which tools write:** Read tools and write tools stay separate. Write tools get approved by full name, and actions with real consequences go through a hook or a human approval step.
- **Failures:** Tools raise `ToolError` with a message that tells Claude how to recover, as `get_policy_limit` does with its list of valid categories.
- **Rate limits and slow systems:** The server handles retries and timeouts toward the customer’s system, and returns a clear error when that system stays unavailable.
- **The server is down:** The agent cannot reach its tools, so the workflow fails closed. Reports go to a person for review instead of receiving a decision the agent could not check.

A candidate who answers these five questions from experience shows the interviewer someone who has deployed a server, beyond simply describing one.

## Building servers worth defending[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-servers-worth-defending)

An MCP server is a small program with a large surface. Its tool descriptions shape what Claude does, its errors decide whether Claude recovers, and its connection method decides where it can run. A strong use case screen answer covers all three. We build the server from plain functions, test it without a model, connect it with the least access the workflow needs, and explain how it behaves when something fails. That sequence is the same one an FDE follows when shipping an MCP server into a customer’s systems.

Defending a Sub-Agent Design

Packaging and Hosting: Agent Skills and Managed Agents

Ask

[Building an MCP server in Python](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-an-MCP-server-in-Python)

[Testing the server without Claude](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Testing-the-server-without-Claude)

[Tool descriptions Claude reads](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Tool-descriptions-Claude-reads)

[Connecting the server to Claude](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Connecting-the-server-to-Claude)

[Defending the server in the screen](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Defending-the-server-in-the-screen)

[Building servers worth defending](https://www.educative.io/courses/forward-deployed-engineer/mcp-for-the-technical-use-case-screen#Building-servers-worth-defending)