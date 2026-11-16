# Understanding_API_Response_Structure_for_Claude_AI_Agent_Loops

Source: https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Reading the API Response Shape

Explore how to read and interpret the API response envelope in Claude AI systems, including top-level fields, stop\_reason values, and content block types. Understand how these elements dictate branching decisions in the agent loop so you can manage multi-turn conversations, handle tool calls, and respond to token limits effectively.

We'll cover the following...

- [The full response envelope](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-full-response-envelope)
- [The four stop\_reason values](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-four-stopreason-values)
  - ["end\_turn": Model finished naturally](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#endturn-Model-finished-naturally)
  - ["tool\_use": Model is requesting a tool call](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#tooluse-Model-is-requesting-a-tool-call)
  - ["max\_tokens": The token budget ran out](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#maxtokens-The-token-budget-ran-out)
  - ["stop\_sequence": A custom stop sequence was hit](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#stopsequence-A-custom-stop-sequence-was-hit)
- [Reading the content array](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Reading-the-content-array)
  - [Text block](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Text-block)
  - [Tool use block](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Tool-use-block)
  - [Multiple blocks in one response](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Multiple-blocks-in-one-response)
- [The usage field and context window health](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-usage-field-and-context-window-health)
- [Putting it together: The loop decision](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Putting-it-together-The-loop-decision)
- [Exercise: Read the response](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Exercise-Read-the-response)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Whats-next)

In the last lesson, we traced a full conversation and noted that `stop_reason` drives every branching decision in the agent loop. Now we slow down and read the response envelope carefully: what each top-level field contains, all four `stop_reason` values, what the loop must do for each one, and what the `content` array can hold beyond a simple text reply.

By the end of this lesson, we will be able to read any API response and immediately know what the loop should do next.

## The full response envelope[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-full-response-envelope)

Every call to `client.messages.create()` returns an object with the same top-level shape, regardless of whether the model replied with text, requested a tool, or stopped unexpectedly:

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

{

"id": "msg\_01XYZabc",

"type": "message",

"role": "assistant",

"model": "claude-opus-4-8",

"content": [...],

"stop\_reason": "end\_turn",

"stop\_sequence": None,

"usage": {

"input\_tokens": 120,

"output\_tokens": 44

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The top-level shape of every Claude API response. The stop\_reason and content fields drive all agent loop decisions.

- **Line 2:** `"id"` is a unique identifier for this response object. Log it on every call; it is the only stable reference for correlating a request to its response when debugging multi-turn failures.
- **Line 3:** `"type"` is always `"message"` for the Messages API. It exists to distinguish responses from other future object types that the API may introduce.
- **Line 4:** `"role"` is always `"assistant"`. When we append this response to the messages array, we use this value as the `role` key.
- **Line 5:** `"model"` echoes back the model that actually handled the request. In production systems, this is useful for confirming routing when multiple models are in play.
- **Line 6:** `"content"` is an array of content blocks. We will dissect the full range of block types in the next section.
- **Line 7:** `"stop_reason"` tells the loop why the model stopped generating. This single field drives every branching decision in the agent loop. We will cover all four possible values in detail below.
- **Line 8:** `"stop_sequence"` contains the stop sequence string that triggered the stop if `stop_reason` is `"stop_sequence"`. It is `None` for all other stop reasons.
- **Line 9:** `"usage"` contains the token counts for this round trip. `input_tokens` is the size of the full messages array we sent. `output_tokens` is the size of the model's response. Together, they tell us how quickly the context window is filling up.

## The four stop\_reason values[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-four-stopreason-values)

`stop_reason` can take exactly four values. Each one requires a different response from the agent loop.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27811.5799999999997%27%20height=%27321.30000000000007%27/%3e)![Every agent loop is a single repeated decision on stop_reason](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Every agent loop is a single repeated decision on stop_reason")

Every agent loop is a single repeated decision on stop\_reason

### `"end_turn"`: Model finished naturally[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#endturn-Model-finished-naturally)

This is the most common stop reason. The model generated a complete response and has nothing more to add until we provide new input. Here is what the response looks like:

Ace Editor

1

2

3

4

5

6

{

"stop\_reason": "end\_turn",

"content": [

{"type": "text", "text": "Your refund has been processed."}

]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

stop\_reason: "end\_turn" means the model completed its response. The loop should surface the text to the user or advance to the next pipeline step.

- **Line 2:** `"end_turn"` is the normal completion signal. The model generated a complete response and stopped because it had nothing more to say.
- **Line 3:** When `stop_reason` is `"end_turn"`, the content array holds text blocks (and sometimes tool\_use blocks if the model made a tool call and then completed). The loop reads the text and either returns it to the user or passes it to the next step.

> **Note:** `"end_turn"` does not mean the task is fully complete from the user's perspective. It means the model’s current response is complete. A multi-turn conversation can have many `"end_turn"` responses before the task is done.

### `"tool_use"`: Model is requesting a tool call[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#tooluse-Model-is-requesting-a-tool-call)

When the model needs to run a function before it can continue, it stops and signals the loop with this value. The loop must not surface this response to the user; it runs the tool and sends the result back first. Here is what the response looks like:

Ace Editor

1

2

3

4

5

6

7

8

{

"stop\_reason": "tool\_use",

"content": [

{"type": "text", "text": "I'll look that up now."},

{"type": "tool\_use", "id": "toolu\_01ABC", "name": "get\_order",

"input": {"order\_id": "12345"}}

]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

stop\_reason: "tool\_use" means the model paused mid-response to request a function call. The loop must run the tool and send the result back before the model can continue.

- **Line 2:** `"tool_use"` signals that the loop must not surface this response to the user. The model is mid-task and waiting for a tool result.
- **Line 3:** The content array contains at least one `tool_use` block. It may also contain a `text` block; Model sometimes narrates what it is doing before making the call. The loop must preserve the full content array (both blocks) when appending this turn to the messages array.
- **Line 5:** The `tool_use` block carries an `id` that must be echoed back as `tool_use_id` in the tool result. Without this link, the model cannot match the result to its request.

**Exam tip:** When `stop_reason` is `"tool_use"`, the loop continues. When it is `"end_turn"`, the loop may stop. Checking `stop_reason`, not parsing the model's text, is the correct and tested way to control this branching.

### `"max_tokens"`: The token budget ran out[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#maxtokens-The-token-budget-ran-out)

This stop reason signals an error condition. The model was mid-response when it hit the `max_tokens` limit we set in the request. The content array contains an incomplete output. Here is what it looks like:

Ace Editor

1

2

3

4

5

6

7

{

"stop\_reason": "max\_tokens",

"content": [

{"type": "text", "text": "The investigation shows three contributing factors: first, the deploy"}

],

"usage": {"input\_tokens": 980, "output\_tokens": 1024}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

stop\_reason: "max\_tokens" means the response was cut off at the max\_tokens limit. The text in the content array is incomplete.

- **Line 2:** `"max_tokens"` means the response hit the budget cap set by `max_tokens` in the request before the model finished. The content is truncated.
- **Line 3:** The text block contains whatever the model generated up to the cutoff. It is not a complete sentence or thought. Returning this to the user as-is would be confusing.
- **Line 6:** The `output_tokens` value in `usage` will equal the `max_tokens` value from the request, confirming that the limit was hit.

The loop has three reasonable options when it sees `"max_tokens"`:

1. Increase `max_tokens` and retry the call.
2. Escalate to a human reviewer with a note that the response was truncated.
3. Log the truncation as an error and surface a safe fallback message.

Which option is correct depends on the system design. What is never correct is silently passing a truncated response downstream as if it were complete.

### `"stop_sequence"`: A custom stop sequence was hit[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#stopsequence-A-custom-stop-sequence-was-hit)

If we passed a `stop_sequences` list in the request, the model stops as soon as it generates one of those strings. Unlike `"max_tokens"`, this is intentional, and the content up to the stop string is complete. Here is what the response looks like:

Ace Editor

1

2

3

4

5

6

7

{

"stop\_reason": "stop\_sequence",

"stop\_sequence": "###END###",

"content": [

{"type": "text", "text": "Classification: billing\nConfidence: high"}

]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

stop\_reason: "stop\_sequence" means the model generated a custom stop string we defined. The content up to that point is complete and intentional.

- **Line 2:** `"stop_sequence"` means the model hit one of the stop strings we passed in the requests `stop_sequences` parameter.
- **Line 3:** `"stop_sequence"` also contains the specific string that triggered the stop, in this case `"###END###"`. If we defined multiple stop strings, this field tells us which one fired.
- **Line 4:** Unlike `"max_tokens"`, the content here is intentionally complete. Stop sequences are typically used in structured output pipelines to signal a clean output boundary. The model finishes its structured output, emits the stop string, and the loop extracts the content.

## Reading the content array[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Reading-the-content-array)

The `content` field is always an array, even when the model returns a single sentence. Here are the block types the loop will encounter:

### Text block[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Text-block)

A **text block** carries the model's natural language output. It appears whenever then model writes a sentence, a paragraph, or a full reply. Here’s its structure:

Ace Editor

1

{"type": "text", "text": "Here is the summary you requested."}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A plain text content block. This is model’s natural language output.

- `"type": "text"` identifies a plain-language response. `"text"` contains the string. This is the block we surface to users or pass to downstream steps.

### Tool use block[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Tool-use-block)

A `tool_use` block is the model's request to run a specific function. It always carries an `id`, the tool `name`, and the `input` arguments the model chose. Here is its structure:

Ace Editor

1

2

3

4

5

6

{

"type": "tool\_use",

"id": "toolu\_01XYZabc",

"name": "search\_docs",

"input": {"query": "refund policy", "limit": 5}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A tool call request block. Model is asking the application to run a function and return the result.

- **Line 2:** `"type": "tool_use"` identifies this as a tool call request, not a text response.
- **Line 3:** `"id"` is the unique identifier for this specific call. It must be echoed in the `tool_use_id` field of the tool result.
- **Line 4:** `"name"` is the tool to run. The application looks up this name, runs the corresponding function, and sends back the output.
- **Line 5:** `"input"` contains the arguments the model chose, validated against the `input_schema` we defined in the tools list.

### Multiple blocks in one response[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Multiple-blocks-in-one-response)

The model can return both a `"text"` block and one or more `"tool_use"` blocks in a single `content` array:

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

"content": [

{

"type": "text",

"text": "I found two relevant documents. Let me also check the billing logs."

},

{

"type": "tool\_use",

"id": "toolu\_01DEF",

"name": "get\_billing\_logs",

"input": {"account\_id": "acc\_789", "days": 30}

}

]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A content array with both a text block and a tool\_use block. Both must be preserved when appending this turn to the messages array.

- **Line 2:** The text block is the model’s narration. It is not the final response. The presence of a `tool_use` block in the same array means `stop_reason` is `"tool_use"`, and the loop must continue.
- **Line 6:** The `tool_use` block is the actual action request. The loop runs this function next.

**Key rule:** When building the next API call, append the full content array, including both the `text` block and the `tool_use` block. Stripping either breaks the conversation record that the model relies on to understand the tool result.

## The usage field and context window health[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-usage-field-and-context-window-health)

Ace Editor

1

2

3

4

5

6

"usage": {

"input\_tokens": 4820,

"output\_tokens": 312,

"cache\_creation\_input\_tokens": 0,

"cache\_read\_input\_tokens": 0

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The usage object from a response mid-way through a long agent run. The input token count is approaching the context window limit.

- **Line 2:** `"input_tokens"` is the total size of the messages array we sent, including the system prompt and all conversation history. This number grows with every turn and never shrinks unless we start a fresh context or summarize.
- **Line 3:** `"output_tokens"` is the size of this specific response. High output token counts relative to the task signal that the model is being verbose, which burns context window budget faster.
- **Lines 4–5:** `"cache_creation_input_tokens"` and `"cache_read_input_tokens"` appear when prompt caching is active. Cache reads are cheaper than full reprocessing, so monitoring the ratio tells us how effectively the cache is being used.

**Note:** The model’s context window limit varies by model. When `input_tokens` approaches the limit, earlier context gets dropped. In agent loops, this means early tool results or task instructions can silently disappear. We cover strategies to detect and handle context degradation in Chapter 9.

## Putting it together: The loop decision[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Putting-it-together-The-loop-decision)

Every iteration of an agent loop reduces to one read and one branch:

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

response = client.messages.create(...)

if response.stop\_reason == "tool\_use":

tool\_result = run\_tool(response.content)

messages.append({"role": "assistant", "content": response.content})

messages.append({"role": "user", "content": tool\_result})

# continue the loop

elif response.stop\_reason == "end\_turn":

return extract\_text(response.content)

# loop ends

elif response.stop\_reason == "max\_tokens":

handle\_truncation(response)

# escalate or retry

elif response.stop\_reason == "stop\_sequence":

return extract\_structured\_output(response.content)

# loop ends, extract clean output

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A minimal agent loop skeleton. Every branch is driven by stop\_reason, not by parsing the model’s text.

- **Line 1:** We make the API call and receive the response object.
- **Lines 3–7:** When `stop_reason` is `"tool_use"`, we run the tool, append both turns to the messages array, and continue the loop. The loop does not exit here.
- **Lines 9–11:** When `stop_reason` is `"end_turn"`, we extract the text and return it. The loop exits.
- **Lines 13–15:** When `stop_reason` is `"max_tokens"`, we handle the truncation explicitly. The response is incomplete and must not be passed downstream as if it were finished.
- **Lines 17–19:** When `stop_reason` is `"stop_sequence"`, the output is complete and structured. We extract it and exit the loop.

## Exercise: Read the response[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Exercise-Read-the-response)

Each question below shows a partial API response. Choose the correct action for the agent loop.

Technical Quiz

1.

The loop receives this response:

```
{"stop_reason": "end_turn", "content": [{"type": "text", "text": "I need more information to process this."}]}
```

What should the loop do?

A.

Continue iterating; `end_turn` with a question means the model wants a tool result

B.

Append the response to messages and call the API again without any new input

C.

Retry the API call with a higher `max_tokens` value

D.

Surface the text to the user and wait for their reply

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Whats-next)

We have the full response vocabulary: every top-level field, all four `stop_reason` values, all content block types, and the loop logic that connects them. In the next lesson, we put this vocabulary to work in the chapter assessment quiz, which tests architectural judgment across all the foundations we have built so far.

Agents, Tools, and Context

Foundations Assessment Quiz

Ask

[The full response envelope](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-full-response-envelope)

[The four stop\_reason values](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-four-stopreason-values)

["end\_turn": Model finished naturally](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#endturn-Model-finished-naturally)

["tool\_use": Model is requesting a tool call](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#tooluse-Model-is-requesting-a-tool-call)

["max\_tokens": The token budget ran out](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#maxtokens-The-token-budget-ran-out)

["stop\_sequence": A custom stop sequence was hit](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#stopsequence-A-custom-stop-sequence-was-hit)

[Reading the content array](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Reading-the-content-array)

[Text block](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Text-block)

[Tool use block](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Tool-use-block)

[Multiple blocks in one response](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Multiple-blocks-in-one-response)

[The usage field and context window health](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#The-usage-field-and-context-window-health)

[Putting it together: The loop decision](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Putting-it-together-The-loop-decision)

[Exercise: Read the response](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Exercise-Read-the-response)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/reading-the-api-response-shape#Whats-next)