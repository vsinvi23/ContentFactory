# System_Prompt_Structure_and_Instruction_Hierarchy_for_Claude_Agents

Source: https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# System Prompt Structure and Instruction Hierarchy

Explore how to structure system prompts for Claude agents by ordering instructions effectively, writing clear role and scope boundaries, and balancing inputs from system prompts, user turns, and tool descriptions to maintain predictable, auditable AI behavior.

We'll cover the following...

- [Why order matters](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Why-order-matters)
- [The four-section template](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-four-section-template)
- [The three instruction sources and how Claude weighs them](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-three-instruction-sources-and-how-Claude-weighs-them)
- [Scope boundaries vs. tool-level exclusions](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Scope-boundaries-vs-tool-level-exclusions)
- [Exercise: Diagnose a broken system prompt](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Exercise-Diagnose-a-broken-system-prompt)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Whats-next)

Every agent built in this course has had a system prompt. Until now, we treated it as a single block of text. This lesson examines its internal structure: how instruction order affects what Claude prioritizes, how to write role and scope instructions that shape the entire conversation, and how Claude resolves conflicts when the system prompt, the user turn, and the tool descriptions all contain instructions that point in different directions. By the end of this lesson, we will be able to:

- Explain why instruction order in the system prompt affects Claude’s behavior
- Write a role statement and scope boundary that set the agent’s operating envelope
- Identify the three sources of instructions in an agent and how Claude weighs them
- Apply a four-section system prompt template that produces predictable, auditable behavior

## Why order matters[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Why-order-matters)

Claude reads the system prompt from top to bottom before processing the user’s message. Instructions at the top of the system prompt carry more weight in Claude’s attention than instructions buried near the end. For most content, this difference is small. For critical constraints, it is significant.

A safety boundary, a confidentiality rule, or an irreversible-action gate belongs at the top of the system prompt. A formatting preference or a tone instruction belongs near the bottom. This is not a strict technical rule enforced by the API. It is a reliability principle based on how attention works in large language models. Placing the most consequential constraints where they are read first increases the probability that they hold under adversarial phrasing, long conversations, and complex tool chains.

## The four-section template[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-four-section-template)

A well-structured system prompt for an agent follows four sections in order:

1. **Role and identity:** One or two sentences that give Claude a clear role. This anchors all subsequent behavior. A role statement should name the agent’s domain and its primary responsibility.
2. **Scope and boundaries:** What the agent should do, and what it must never do. Critical business rules, data access limits, and action gates belong here. This is the section that replaces system prompt instructions that should instead be code-enforced (the ones we moved to `dispatch_tool` in the guardrails lesson). Whatever remains as a prompt-level constraint goes here.
3. **Tool and task guidance:** How to use the available tools, in what order, and under what conditions. This overlaps with the tool-description sequencing guidance, but the system prompt can set higher-level priorities: “Prefer cached lookup tools before live API calls” or “If a tool returns an access failure, report the gap rather than substituting an estimate.”
4. **Format and style:** Response format, length, tone, and output structure. These are the lowest-stakes instructions. Claude handles format guidance reliably even when it appears at the end of a long system prompt.

Here is a complete example for an order support agent:

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

You are an order support assistant for Northshore Retail. Your role is to help

customers understand their order status, modify shipping addresses on pre-dispatch

orders, and process returns for eligible items.

BOUNDARIES:

- Do not discuss pricing, promotions, or discounts: direct those questions to the

sales team.

- Do not process refunds: use only the return initiation tools available to you.

- Do not modify any order that has status 'Shipped' or 'Delivered'.

- Never reveal internal order IDs, warehouse codes, or carrier account numbers.

TOOL GUIDANCE:

- Always call get\_order\_status before any modification tool to confirm current status.

- If a tool returns ACCESS\_FAILURE, report the specific gap to the customer and

offer to escalate rather than substituting an estimate.

- Call check\_return\_eligibility before initiate\_return on every return request.

FORMAT:

- Respond in plain English. No bullet lists unless listing multiple order items.

- Keep responses under four sentences for routine status updates.

- For return confirmations, include the return reason and the expected refund timeline.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A four-section system prompt for an order support agent. The boundaries section replaces the highest-stakes constraints that cannot be delegated to the prompt (the ones that stay in code are in dispatch\_tool). Tool guidance reinforces the description-level sequencing from the tool definitions.

- **Role section:** Names the domain (Northshore Retail order support) and the three permitted action types. This anchors all subsequent decisions. If a request falls outside these three, Claude knows to decline or redirect.
- **Boundaries section:** Written with an all-caps heading and bullets for visual salience. These are the constraints most likely to face adversarial pressure. Placing them second (immediately after the role) means they are read early and carry high attention weight.
- **Tool guidance section:** Reinforces the description-level instructions (`check_return_eligibility` before `initiate_return`) at the system level. It also adds a cross-cutting instruction that no individual tool description can express: what to do when any tool returns an access failure.
- **Format section:** Lowest stakes, placed last. Even if a long conversation compresses the system prompt’s attention on later sections, losing a format instruction degrades response aesthetics, not correctness.

## The three instruction sources and how Claude weighs them[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-three-instruction-sources-and-how-Claude-weighs-them)

An agent receives instructions from three places:

1. **The system prompt:** Set by the developer, present on every turn, highest authority
2. **The user turn:** Sent by the user, varies per request, lower authority than the system prompt
3. **Tool descriptions:** Embedded in the tool definition, read when Claude selects tools

When these sources conflict, Claude’s general priority is: system prompt first, then user turn, then tool descriptions. But this is not absolute. A user turn that explicitly contradicts a system prompt instruction may succeed if the system prompt phrasing is soft (“prefer to”) rather than hard (“never”).

**The practical lesson is:** Use strong language for constraints that must hold. The difference between these two phrasings is significant:

Ace Editor

1

2

3

4

5

# Soft: guideline, Claude may override with sufficient user context

"Prefer to use the cached data tool before making live API calls."

# Hard: boundary, Claude treats as non-negotiable

"Always call the cached data tool first. Do not call live API tools until the cached tool has returned a result or an explicit cache miss."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

“Prefer” invites reasoning about exceptions. “Always” and “Do not” signal boundaries that Claude applies without weighing user context against them.

## Scope boundaries vs. tool-level exclusions[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Scope-boundaries-vs-tool-level-exclusions)

There are two places to tell Claude what not to do: the system prompt scope section and the individual tool descriptions. Both are useful, and they serve different purposes.

- System prompt scope boundaries set the agent’s operating envelope for the entire conversation. They apply regardless of which tools are available. “Do not discuss competitor pricing” is a system-level scope rule. It applies even if no tool is involved.
- Tool description exclusions constrain which tool to use for a specific task. “Do not use `lookup_customer` for billing questions; use `lookup_account` instead” is a tool-level exclusion. It applies only during tool selection.

A constraint that appears in both locations is more reliable than one that appears in only one. For the highest-stakes boundaries, duplicate them:

Ace Editor

1

2

3

4

5

6

# In the system prompt scope section:

"Do not process refunds. Direct refund requests to the billing team."

# In the refund-adjacent tool description:

"Do not use this tool to initiate or approve a refund. For refund requests,

inform the user that the billing team handles refunds directly."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Duplication here is not redundancy. It is defense in depth. If the system prompt instruction is weakened by a long conversation, the tool description exclusion still fires at the moment of tool selection.

## Exercise: Diagnose a broken system prompt[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Exercise-Diagnose-a-broken-system-prompt)

Read the following system prompt and answer the questions.

Ace Editor

1

2

3

4

5

You are a helpful assistant. Be concise and friendly. Use the tools available

to look up customer information and process requests. Always confirm actions

before executing them. Do not share sensitive information. You work for Meridian

Bank and have access to account lookup, transaction history, and fund transfer

tools.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Technical Quiz

1.

A user asks: “Transfer $50,000 from my savings to my checking account.” Claude calls `transfer_funds` immediately after asking “shall I proceed?” and the user says “yes.” What structural problem in the system prompt allowed this?

A.

The format instruction (“be concise”) caused Claude to skip verification steps

B.

The role statement is too vague: “helpful assistant” gives Claude too much latitude

C.

“Always confirm actions” is a soft instruction with no limits or extra checks for high-value transfers

D.

The tool guidance section is missing, so Claude did not know to call a verification tool first

---

1 / 3

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Whats-next)

In the next lesson, we focus on output format control: how to write system prompt instructions and use the API parameters that ensure Claude returns structured, parseable output on every turn, rather than freeform prose.

Tools and MCP Assessment Quiz

Output Format Control and Structured Outputs

Ask

[Why order matters](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Why-order-matters)

[The four-section template](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-four-section-template)

[The three instruction sources and how Claude weighs them](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#The-three-instruction-sources-and-how-Claude-weighs-them)

[Scope boundaries vs. tool-level exclusions](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Scope-boundaries-vs-tool-level-exclusions)

[Exercise: Diagnose a broken system prompt](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Exercise-Diagnose-a-broken-system-prompt)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/system-prompt-structure-and-instruction-hierarchy#Whats-next)