# Understanding_Messages_API_and_Tool_Integration_in_Anthropic_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Messages API and Tool Use Under Questioning

Explore how to work with Anthropic's Messages API, manage conversation history, and integrate client-side tools within AI systems. Understand how to handle API responses, stop reasons, and common interview pitfalls to demonstrate fluency in building reliable AI assistants during Forward Deployed Engineer interviews at Anthropic.

We'll cover the following...

- [The request shape interviewers check](https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning#The-request-shape-interviewers-check)
- [Stop reasons as control flow](https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning#Stop-reasons-as-control-flow)
- [The tool loop and its rules](https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning#The-tool-loop-and-its-rules)
- [Mistakes candidates make live](https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning#Mistakes-candidates-make-live)
- [Showing fluency at the base layer](https://www.educative.io/courses/forward-deployed-engineer/messages-api-and-tool-use-under-questioning#Showing-fluency-at-the-base-layer)

Every Claude system an FDE builds rests on one endpoint. Chat assistants, document reviewers, and multi-step agents all send requests to the Messages API and read responses in the same shape.

Anthropic’s interviewers use this layer to separate candidates who have built on Claude from candidates who have only read about it. In the technical use-case screen or the coding round, an interviewer may ask you to wire a tool into Claude live or to explain why a half-working integration fails. Fluency here shows up in small details, such as how you store the conversation, how you branch on a response, and how you return a tool’s result.

The examples follow one scenario: an expense audit assistant that helps a finance team check employee expense reports against company policy.

## The request shape interviewers check

The **Messages API** is Anthropic’s interface for sending a conversation to Claude and receiving Claude’s next turn. Each request carries four core fields.

- `model`**:** The Claude model that answers, such as `claude-sonnet-5-5`.
- `max_tokens`**:** The upper limit on the length of Claude’s reply.
- `system`**:** An optional prompt that sets Claude’s role and rules for the whole conversation.
- `messages`**:** The conversation so far, as a list of user and assistant turns.

Claude’s reply arrives as a list of content blocks. A **content block** is one typed piece of a message, such as a `text` block, a `tool_use` block, or a `thinking` block. Code that checks each block’s `type` keeps working when a reply carries more than text.

The API is **stateless**, which means it keeps no memory between requests. Each request carries the full conversation, and your code owns the history. This detail creates a common interview trap. A candidate who rebuilds the assistant turn from its text alone drops the `tool_use` and `thinking` blocks, and the next request fails or loses context. The safe habit is to append the assistant’s `content` exactly as the API returned it.

Let’s send a first request to the expense assistant, then a follow-up that only makes sense with the history.

Python 3.14.0

```
import anthropic

client = anthropic.Anthropic(api_key="{{ANTHROPIC_API_KEY}}")

MODEL = "claude-sonnet-5-5"

SYSTEM = "You are an expense audit assistant for a finance team. Answer in one short sentence."

# The API keeps no memory between calls, so our code owns the conversation.

messages = [{"role": "user", "content": "What does a finance reviewer check first on a meals expense?"}]

first = client.messages.create(model=MODEL, max_tokens=300, system=SYSTEM, messages=messages)

# The reply is a list of typed content blocks.

print("Block types:", [block.type for block in first.content])

print("Answer:", "".join(block.text for block in first.content if block.type == "text"))

print("Stop reason:", first.stop_reason)

# Append the assistant turn exactly as returned, then ask a follow-up that depends on it.

messages.append({"role": "assistant", "content": first.content})

messages.append({"role": "user", "content": "What is the most common reason it gets flagged?"})

second = client.messages.create(model=MODEL, max_tokens=300, system=SYSTEM, messages=messages)

print("Follow-up answer:", "".join(block.text for block in second.content if block.type == "text"))
```

⋯

Sending a request to the expense assistant and a follow-up that reuses the conversation history

- **Lines 3–5:** We created the client with our API key and set the model and a short system prompt for the expense assistant.
- **Line 8:** We ...