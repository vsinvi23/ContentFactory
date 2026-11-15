# Understanding_the_Gemini_API_for_Google_FDE_Interview_Preparation

Source: https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Gemini API

Explore how Gemini requests and responses are structured, including contents, system instructions, finish reasons, and token usage. Learn to use function calling and structured output to build reliable agent components, and choose between Flash and Pro models based on task requirements.

We'll cover the following...

- [The anatomy of a request](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#The-anatomy-of-a-request)
- [Reading the response](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Reading-the-response)
- [Function calling](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Function-calling)
- [Structured output](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Structured-output)
- [Choosing between Flash and Pro](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Choosing-between-Flash-and-Pro)

Almost every Google FDE system design eventually comes down to a call to a Gemini model. An agent built with ADK, a retrieval pipeline, or a ticket classifier all depend on the same basic exchange: the application sends a request with context and instructions, and the model returns a response. Interviewers expect candidates to understand this exchange well enough to explain how an agent decides to call a tool, how its output becomes reliable data, and why one model tier fits a task better than another.

The sections below cover the structure of a Gemini request and response, function calling, structured output, and the trade-offs between the Flash and Pro model tiers. The code examples use the Google Gen AI SDK for Python, which works with both the Gemini Developer API and Google Cloud’s enterprise platform.

## The anatomy of a request[#](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#The-anatomy-of-a-request)

A Gemini request has a small number of parts, and each one controls a different aspect of the model’s behavior.

|  |  |  |
| --- | --- | --- |
| **Part** | **Purpose** | **Example** |
| Model | Selects the model tier and version | A Flash or Pro model ID |
| Contents | The conversation so far, as a list of turns | A user question, previous model replies |
| System instruction | Persistent guidance on role, tone, and rules | “You are a billing support assistant.” |
| Generation config | Controls output behavior | Temperature, maximum output tokens, response format |
| Tools | Functions or services the model may call | An order lookup function |

Contents are organized into turns, and each turn has a role, either `user` or `model`, and one or more parts. A part can be text, an image, a document, a function call, or a function result. This structure is what allows a single API to handle chat, multimodal input, and tool use.

The model is stateless. It does not remember earlier requests, so the application sends the relevant conversation history with each call. In production, this is why session management matters: an agent’s memory is whatever the application chooses to include in the next request.

The following example sends a simple request with a system instruction and generation settings.

Please provide values for the following:

GOOGLE\_GEMINI\_API\_KEY

Import Values from JSON

Python 3.14.0

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

from google import genai

from google.genai import types

client = genai.Client(api\_key="{{GOOGLE\_GEMINI\_API\_KEY}}")

MODEL\_ID = "gemini-3.6-flash"

response = client.models.generate\_content(

model=MODEL\_ID,

contents="My invoice shows two charges for March. What should I do?",

config=types.GenerateContentConfig(

system\_instruction="You are a billing support assistant. Reply in plain text, in two sentences or fewer.",

temperature=0.2,

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

⋯

- **Lines 1–2:** We import the Google Gen AI SDK and its `types` module, which defines configuration and content objects.
- **Line 4:** We create a client that reads the API key from the environment, which keeps credentials out of the code.
- **Line 6:** We store the model ID in one variable so that switching between Flash and Pro takes a single change.
- **Line 8:** `generate_content` sends one request to the model and returns a complete response.
- **Line 10:** `contents` holds the user’s input. A single string is treated as one user turn.
- **Line 12:** The system instruction sets the model’s role and output format for the whole request.
- **Lines 13–14:** A low temperature keeps answers consistent, and `max_output_tokens` caps response length and cost.
- **Line 18:** `response.text` returns the text from the first candidate.
- **Line 19:** The finish reason shows whether the model stopped normally (`STOP`) or was cut off (`MAX_TOKENS`).
- **Lines 20–21:** Usage metadata reports input and output token counts, which are the basis for estimating cost per request.

A low temperature makes the output more consistent, which suits support and data tasks. Creative or brainstorming tasks may use a higher value.

Note: To call Gemini through a Google Cloud project instead of an API key, the client is created with `genai.Client(vertexai=True, project="PROJECT_ID", location="LOCATION")`. The rest of the code stays the same. Enterprise customers almost always use this path, because it applies their project’s IAM, networking, and data controls.

With the request structure in place, the next step is to read what the model sends back.

## Reading the response[#](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Reading-the-response)

A response contains one or more candidates. In most applications, there is a single candidate, and its content holds the model’s parts. The SDK’s `response.text` property is a shortcut for the text parts of the first candidate.

Two other fields matter in production. The **finish reason** explains why generation stopped. A value of `STOP` means the model completed normally, while `MAX_TOKENS` means the output was cut off and may be incomplete. Other values indicate that safety filters or other limits ended the response. Production code should check this field rather than assume every response is complete.

The **usage metadata** reports input and output token counts. Cost and latency both scale with tokens, so these numbers are the basis for estimating cost per request and for spotting prompts that have grown larger than expected. In interviews, referring to token usage when discussing cost shows a practical understanding of how the system is billed.

A text response works well for people. Agents, however, need to take actions, and that requires function calling.

## Function calling[#](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Function-calling)

Function calling allows the model to request that the application run a specific function. The model does not execute anything itself. It returns a structured request containing a function name and arguments, the application runs the function, and the result is sent back to the model so it can continue.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27940.5%27%20height=%27724.68%27/%3e)![function call](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "function call")

function call

This separation is important for enterprise systems. Because the application runs every function, the application controls which functions exist, which arguments are valid, and which user permissions apply. The model can only request an action. It cannot bypass the checks the application enforces.

The example below declares a function, lets the model request it, runs it, and returns the result.

Please provide values for the following:

GOOGLE\_GEMINI\_API\_KEY

Import Values from JSON

Python 3.14.0

```
from google import genai

from google.genai import types

client = genai.Client(api_key="{{GOOGLE_GEMINI_API_KEY}}")

MODEL_ID = "gemini-3.6-flash"

def get_order_status(order_id: str) -> dict:

"""Returns the shipping status for an order."""

# In production, this would query the order system with the user's permissions.

return {"order_id": order_id, "status": "shipped", "carrier": "UPS"}

order_tool = types.Tool(function_declarations=[

types.FunctionDeclaration(

name="get_order_status",

description="Look up the shipping status of a customer order.",

parameters={

"type": "object",

"properties": {"order_id": {"type": "string"}},

"required": ["order_id"],

},

)

])

config = types.GenerateContentConfig(tools=[order_tool])

history = [types.Content(role="user", parts=[types.Part(text="Where is order 1042?")])]

response = client.models.generate_content(model=MODEL_ID, contents=history, config=config)

call = response.function_calls[0]

result = get_order_status(**call.args)

history.append(response.candidates[0].content)

history.append(types.Content(role="user", parts=[

types.Part.from_function_response(name=call.name, response=result)

]))

final = client.models.generate_content(model=MODEL_ID, contents=history, config=config)

print(final.text)
```

⋯

- **Lines 6–9:** `get_order_status` is a regular Python function that the application runs. Here it returns sample data, but in production it would query the order system and enforce the user’s permissions.
- **Lines 11–21:** We describe the function to the model using a `FunctionDeclaration`. The model sees only this description, never the function’s code.
- **Line 14:** The description tells the model when to use the function, so a clear, specific description reduces wrong or unnecessary calls.
- **Lines 15–19:** The parameter schema defines the expected arguments, and `required` ensures the model always supplies an `order_id`.
- **Line 23:** We attach the tool to the request configuration so the model knows it is available.
- **Line 24:** The conversation history starts with the user’s question as a single `user` turn.
- **Line 26:** The first call returns a function call request instead of a text answer.
- **Line 27:** `response.function_calls` contains the function name and arguments the model chose.
- **Line 28:** The application, not the model, runs the function. This is where validation and permission checks belong.
- **Line 30:** We add the model’s function call turn to the history so the model can see what it requested.
- **Lines 31–33:** We send the function result back as a function response part, linked to the original call by name.
- **Line 35:** The second call includes the full history, so the model can use the result to write its final answer.

The function’s name and description strongly influence whether the model calls it correctly. Clear, specific descriptions and tightly defined parameters reduce wrong or unnecessary calls. The SDK can also run this loop automatically when Python functions are passed directly as tools, but writing the loop explicitly shows where validation and permission checks belong, which is exactly what interviewers probe.

Function calling handles actions. When the output needs to feed another system, structured output becomes the next tool.

## Structured output[#](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Structured-output)

Free-form text is difficult for software to consume reliably. Structured output instructs the model to return JSON that matches a defined schema, so downstream code can parse and validate it without fragile text processing.

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

from pydantic import BaseModel

class RefundDecision(BaseModel):

eligible: bool

reason: str

amount: float

response = client.models.generate\_content(

model=MODEL\_ID,

contents="Order 1042 was delivered damaged 3 days ago. Price: $84.50. Policy: refunds within 30 days.",

config=types.GenerateContentConfig(

response\_mime\_type="application/json",

response\_schema=RefundDecision,

),

)

decision = response.parsed # A RefundDecision object

print(decision.eligible, decision.amount)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Lines 3–6:** A Pydantic model defines the exact shape of the output, with a field name and type for each value.
- **Line 12:** Setting the MIME type to `application/json` tells the model to return JSON instead of free text.
- **Line 13:** The response schema constrains the JSON to match `RefundDecision`, so every field is present with the correct type.
- **Line 17:** `response.parsed` converts the JSON into a `RefundDecision` object that downstream code can use directly.
- **Line 18:** The fields are now typed values. They still need business-rule checks, such as refund limits, before any action is taken.

Structured output is useful for classification, extraction, routing decisions, and any step whose result another component consumes. It guarantees the shape of the output, not its correctness. A well-formed `RefundDecision` can still contain the wrong amount, so business rules such as refund limits should be checked in code before any action is taken.

With the core features covered, the remaining decision is which model tier should handle each task.

## Choosing between Flash and Pro[#](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Choosing-between-Flash-and-Pro)

Gemini models come in tiers that trade capability against speed and cost. The Flash tier is optimized for low latency and high volume. The Pro tier provides stronger reasoning for complex, multi-step, or ambiguous tasks. Specific version numbers change frequently, but the trade-off between the tiers stays consistent.

|  |  |  |
| --- | --- | --- |
| **Latency** | **Lower** | **Higher** |
| Cost per token | Lower | Higher |
| Best suited for | Classification, extraction, routing, summarization, high-volume chat | Complex reasoning, multi-step planning, difficult analysis, code generation |
| Typical role in an agent system | Handles most routine requests | Handles hard cases or planning steps |

Many production systems use both. A Flash model handles the high-volume first step, such as classifying a request or extracting fields, and only difficult cases are routed to a Pro model. This pattern keeps average latency and cost low while preserving quality where it matters. Recent Gemini models also offer thinking settings that control how much internal reasoning the model performs before answering, which provides another way to balance quality against latency within a single tier.

In an interview, a strong model choice is tied to the task’s requirements. A statement such as “Flash handles ticket classification because the task is narrow, volume is high, and the support team needs responses in under a second, while Pro handles escalation summaries, where reasoning quality matters more than speed” shows the kind of judgment the interviewer is looking for. The right choice should be confirmed with evaluation on the customer’s own data rather than assumed.

Defaulting to the most capable model for every step is a common design mistake. Starting with Flash and moving specific steps to Pro only when evaluation shows a quality gap leads to cheaper, faster systems and gives a clear, defensible reason for each model choice.

The Gemini API is the foundation that every higher-level Google AI tool builds on. Understanding how requests carry context, how function calling keeps the application in control of actions, how structured output makes results dependable, and how model tiers balance quality against cost makes it much easier to reason about agents, retrieval systems, and production trade-offs in any customer scenario.

The Google FDE Tech Stack

The Agent Platform and ADK

Ask

[The anatomy of a request](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#The-anatomy-of-a-request)

[Reading the response](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Reading-the-response)

[Function calling](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Function-calling)

[Structured output](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Structured-output)

[Choosing between Flash and Pro](https://www.educative.io/courses/forward-deployed-engineer/the-gemini-api#Choosing-between-Flash-and-Pro)