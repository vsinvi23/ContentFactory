# Integrating_MCP_Tools_for_Enterprise_AI_Agents_in_Google_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# MCP Tool Integration

Explore how the Model Context Protocol standardizes connections between agents and enterprise tools and data. Learn when to use managed or custom MCP servers, how to design narrow tools, and why permissions must come from the authenticated session rather than the model.

We'll cover the following...

- [What MCP is](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#What-MCP-is)
- [Managed versus custom MCP servers](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Managed-versus-custom-MCP-servers)
- [Permissions come from the session, not the model](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Permissions-come-from-the-session-not-the-model)
- [Common integration mistakes](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Common-integration-mistakes)

An enterprise agent is useful only when it can reach thesystems where the customer’s work happens: databases, ticketing systems, document stores, and internal APIs. Before a standard existed, each connection between an agent and a system required custom integration code, and that code was rarely reusable across frameworks or projects. For an FDE moving between customers, this meant rebuilding similar connectors repeatedly and reviewing each one separately for security.

The Model Context Protocol (MCP) addresses this problem by defining a common way for AI applications to discover and call external tools. Google Cloud supports MCP across its agent stack, offers managed MCP servers for its own services, and lets ADK agents connect to any MCP server. FDE interviewers expect candidates to explain how MCP works, when to use a managed server versus a custom one, and, most importantly, how permissions are enforced when an agent acts through these tools.

## What MCP is[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#What-MCP-is)

MCP is an open protocol, introduced by Anthropic in late 2024 and now widely adopted, that standardizes how an AI application connects to external capabilities. It follows a client-server model. The MCP client lives inside the AI application or agent framework, such as ADK. The MCP server wraps a system, such as a database or an API, and exposes its capabilities in a standard format.

An MCP server can expose three kinds of capabilities.

|  |  |  |
| --- | --- | --- |
| **Capability** | **What it provides** | **Example** |
| Tools | Actions the agent can invoke | Query a table, create a ticket, send a notification |
| Resources | Read-only data the application can load as context | A file, a database schema, a policy document |
| Prompts | Reusable prompt templates offered by the server | A standard template for summarizing an incident |

Tools are the capability FDEs work with most often. When an agent connects to a server, it asks which tools are available, receives each tool’s name, description, and input schema, and then calls tools as needed. The model sees these descriptions in the same way it sees function declarations in the Gemini API.

Servers communicate with clients through a transport. Local servers often use standard input and output, which suits development and desktop tools. Remote servers use Streamable HTTP, which suits production deployments where the server runs as a separate service with its own authentication, scaling, and monitoring.

The value for enterprise work comes from separation. The team that owns a system can build and maintain one MCP server for it, and any compliant agent can use that server without new integration code. Security reviews also become simpler, since the server is a single, well-defined point of access to the system.

With the protocol defined, the next decision is whether to use a server someone else provides or build one.

## Managed versus custom MCP servers[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Managed-versus-custom-MCP-servers)

Google provides managed, remote MCP servers for several of its own services, including BigQuery and other Google Cloud products. These servers are hosted and maintained by Google, use Google Cloud’s identity and access controls, and can be connected to an agent with configuration rather than code. Many third-party software vendors also publish MCP servers for their products.

Custom servers are needed when a customer’s system has no existing server, such as an internal order management API or a legacy database, or when the customer needs tools shaped around a specific business workflow rather than a generic interface.

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Managed** | **Customer MCP servers** |
| Setup effort | Configuration only | Design, build, and deploy |
| Maintenance | Handled by the provider | Owned by the customer or FDE team |
| Tool design | General-purpose tools | Tools shaped to the customer’s workflow |
| Security model | Provider’s identity and access controls | Must be designed and reviewed |
| Best fit | Standard services such as BigQuery | Internal systems and business-specific actions |

A common FDE pattern combines both. Managed servers handle standard platforms, and a small number of custom servers expose the customer’s internal systems through narrow, task-specific tools. Narrow tools are an important design choice. A tool named `get_open_invoices_for_customer` is safer and easier for the model to use correctly than a general `run_sql_query` tool, because it limits what the agent can do and makes its intent clear in logs.

In a system design interview, starting with managed servers and adding custom servers only for systems that require them shows good judgment. It reduces delivery time and limits the amount of security-sensitive code the customer must maintain.

Choosing the server is only part of the design. The more important question is whose permissions the agent uses when it calls a tool.

## Permissions come from the session, not the model[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Permissions-come-from-the-session-not-the-model)

A model decides which tool to call and what arguments to pass, but it cannot be trusted to decide what the user is allowed to access. Model output can be influenced by prompt injection, misleading documents, or simple mistakes. If a tool accepts a `customer_id` argument from the model and returns that customer’s data, a manipulated prompt could lead the agent to request another customer’s records.

The rule FDEs follow is that **permissions come from the authenticated session, not from the model**. When a user signs in, the application establishes their identity. That identity travels with each tool call, usually as an access token, and the MCP server or the underlying system checks it before returning data or taking action. The model can choose which tool to call, but the server decides what that user is allowed to see.

The following custom MCP server applies this rule. It uses the official MCP Python SDK.

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

from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("billing-tools")

def get\_authenticated\_user(ctx: Context) -> str:

"""Returns the user ID from the verified access token on the request."""

token = ctx.request\_context.request.headers["authorization"]

return verify\_token(token) # Validates the token with the identity provider

@mcp.tool()

def get\_invoices(ctx: Context, limit: int = 5) -> list[dict]:

"""Returns the most recent invoices for the signed-in customer."""

user\_id = get\_authenticated\_user(ctx)

return billing\_db.fetch\_invoices(customer\_id=user\_id, limit=limit)

if \_\_name\_\_ == "\_\_main\_\_":

mcp.run(transport="streamable-http")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** We import `FastMCP`, the MCP SDK’s high-level server class, and `Context`, which gives tools access to the incoming request.
- **Line 3:** We create a server named `billing-tools`. Clients see this name when they connect.
- **Lines 5–8:** `get_authenticated_user` reads the access token from the request header and verifies it with the identity provider. `verify_token` and `billing_db` stand in for the customer’s own identity and data services.
- **Line 10:** The `@mcp.tool()` decorator registers the function as a tool and builds its schema from the type hints and docstring.
- **Line 11:** The tool’s only model-controlled argument is `limit`. There is no `customer_id` parameter for the model to fill in.
- **Line 12:** The docstring becomes the tool’s description, so it states clearly that results are scoped to the signed-in customer.
- **Line 13:** The user’s identity comes from the verified token, not from anything the model generated.
- **Line 14:** The database query is scoped to that user, so a manipulated prompt cannot retrieve another customer’s invoices.
- **Line 17:** The server runs over Streamable HTTP, the transport used for remote production deployments.

On the agent side, ADK connects to the server through an MCP toolset and attaches the user’s token from the session.

Python 3.14.0

```
from google.adk.agents import Agent

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

billing_tools = McpToolset(

connection_params=StreamableHTTPConnectionParams(

url="https://billing-mcp.example.com/mcp",

),

tool_filter=["get_invoices"],

header_provider=lambda ctx: {

"Authorization": f"Bearer {ctx.state['temp:access_token']}"

},

)

root_agent = Agent(

name="billing_agent",

model=MODEL_ID,

instruction="Answer questions about the signed-in customer's invoices.",

tools=[billing_tools],

)
```

⋯

- **Lines 2–3:** We import `McpToolset`, which connects an ADK agent to an MCP server, and the connection settings for a remote server.
- **Lines 6–8:** The connection points to the remote MCP server’s URL over Streamable HTTP.
- **Line 9:** `tool_filter` exposes only the listed tools to the agent, even if the server offers more. This keeps the agent’s capabilities as narrow as the use case.
- **Lines 10–12:** `header_provider` builds request headers for each call. It reads the user’s access token from session state, where the application placed it after sign-in.
- **Line 11:** The `temp:` prefix keeps the token in temporary state for the current invocation, so it is not saved with the session’s stored history.
- **Line 19:** The MCP toolset is passed to the agent like any other tool. ADK discovers the server’s tools and handles each call.

The model never sees or generates the token. It only decides to call `get_invoices`, and the identity attached to that call comes from the session the application created.

## Common integration mistakes[#](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Common-integration-mistakes)

Several mistakes appear often in both interviews and real deployments. The first is exposing broad tools, such as raw SQL execution, when narrow, task-specific tools would meet the need. The second is running every tool call under a single powerful service account, which gives every user the same access and removes the audit trail of who did what. The third is passing user identifiers as model-controlled arguments instead of deriving them from the authenticated session. The last is treating MCP as a security layer in itself. MCP standardizes how tools are described and called, but authentication, authorization, and auditing still have to be designed into the servers and the systems behind them.

MCP gives FDEs a reusable way to connect agents to enterprise systems, and Google’s managed servers reduce the integration work for standard services. The design decisions that matter most are which tools to expose, how narrowly to scope them, and where permissions are enforced. A design in which the model chooses actions while the authenticated session and the server decide access holds up under both prompt injection and a customer’s security review, and that is the standard interviewers expect a strong candidate to meet.

The Agent Platform and ADK

A2A and Multi-Agent Design

Ask

[What MCP is](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#What-MCP-is)

[Managed versus custom MCP servers](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Managed-versus-custom-MCP-servers)

[Permissions come from the session, not the model](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Permissions-come-from-the-session-not-the-model)

[Common integration mistakes](https://www.educative.io/courses/forward-deployed-engineer/mcp-tool-integration#Common-integration-mistakes)