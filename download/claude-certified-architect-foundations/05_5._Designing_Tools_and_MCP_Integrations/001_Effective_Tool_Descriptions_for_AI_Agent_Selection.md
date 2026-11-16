# Effective_Tool_Descriptions_for_AI_Agent_Selection

Source: https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Tool Descriptions That Guide Selection

Explore how to craft tool descriptions that direct Claude's decision-making process for tool selection. Understand the four key components of effective descriptions to ensure correct calls, avoid errors, and enforce behavioral contracts without relying on system prompts.

We'll cover the following...

- [Why the description is the primary signal](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Why-the-description-is-the-primary-signal)
- [The four components of an effective description](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#The-four-components-of-an-effective-description)
- [Sequencing through descriptions](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Sequencing-through-descriptions)
- [Schema-level constraints vs. description-level constraints](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Schema-level-constraints-vs-description-level-constraints)
- [Exercise: Rewrite a weak description](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Exercise-Rewrite-a-weak-description)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Whats-next)

A tool definition has three parts: a name, a description, and an input schema. Most engineers treat the description as documentation for a human reader and the schema as the technical spec. That framing is backward. Claude reads the description to decide whether to call the tool, when to call it, and what to put in the arguments. The description is behavioral instruction, not documentation.

This lesson reframes tool design as the primary mechanism for shaping agent behavior. By the end, we will understand how to write descriptions that produce correct call sequences, avoid ambiguous selections, and enforce boundaries without a system prompt. By the end of this lesson, we will be able to:

- Explain why tool descriptions are Claude’s primary decision signal for tool selection.
- Identify the four components of an effective tool description.
- Write a description that prevents a common selection mistake (over-calling, under-calling, wrong order).
- Distinguish between description-level constraints and schema-level constraints.

## Why the description is the primary signal[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Why-the-description-is-the-primary-signal)

When Claude receives a request and a set of tools, it reads the descriptions to build a model of what each tool is for. The name alone is insufficient. `get_data` and `fetch_record` are names, not behavioral guidance. The input schema tells Claude which fields to populate, but not which tool to pick or when. The description answers three questions Claude needs before calling any tool:

1. **What domain does this tool operate in?** A tool named `lookup` could match dozens of tasks. A description that says “Use this tool to retrieve a customer’s order history from the order management system, not for account or billing lookups” disambiguates immediately.
2. **When should this tool be called?** Descriptions can name preconditions: “Use this after confirming the user wants to proceed” or “Call this first, before any modification tools.”
3. **What should this tool not be used for?** Explicit exclusion prevents Claude from reaching for a tool that looks close but is wrong. “Do not use this tool for refund requests; use `process_refund` instead” prevents a common substitution error.

## The four components of an effective description[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#The-four-components-of-an-effective-description)

A description that produces reliable behavior covers four things:

|  |  |  |
| --- | --- | --- |
| **Component** | **What It Answers** | **Example** |
| Domain | What kind of data or system does this touch? | "Queries the order management database" |
| Trigger condition | When should this tool be called? | "Use when the user asks about order status or shipping" |
| Exclusion | What should this NOT be used for? | "Do not use for billing or payment questions" |
| Sequencing | Does this tool have ordering constraints? | "Call this before any modification tools" |

Not every tool needs all four. A tool with no plausible substitutes needs only a domain and trigger. A tool that is frequently confused with another needs an explicit exclusion. A tool that must run before another needs sequencing guidance. Here is a poorly written description, followed by a well-written one for the same tool:

**Poor:**

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

{

"name": "update\_shipping\_address",

"description": "Updates the shipping address for an order.",

"input\_schema": {

"type": "object",

"properties": {

"order\_id": {"type": "string"},

"new\_address": {"type": "string"}

},

"required": ["order\_id", "new\_address"]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

**Better:**

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

{

"name": "update\_shipping\_address",

"description": (

"Update the shipping address for an order that has not yet been dispatched. "

"Use this when the user confirms they want to change the delivery address. "

"Do not use this for orders with status 'Shipped' or 'Delivered': those require "

"a carrier redirect, handled by `request\_carrier\_redirect`. "

"Always call `get\_order\_status` first to confirm the order is still in pre-dispatch state."

),

"input\_schema": {

"type": "object",

"properties": {

"order\_id": {"type": "string"},

"new\_address": {"type": "string", "description": "Full street address including city, state, and postal code."}

},

"required": ["order\_id", "new\_address"]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- The better version covers all four components: domain (pre-dispatch orders), trigger (user confirms), exclusion (not for shipped orders; use the redirect tool instead), and sequencing (call `get_order_status` first).
- The poor version tells Claude what the tool does. The better version tells Claude when to call it, when not to, and what must happen first. This is the behavioral contract.

## Sequencing through descriptions[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Sequencing-through-descriptions)

One of the most powerful uses of a description is encoding call order. When a workflow requires tool A before tool B, the description can state this directly.

Consider an agent that processes returns. The correct sequence is: check eligibility, confirm with the user, then initiate the return. Here are the descriptions that enforce this:

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

TOOLS = [

{

"name": "check\_return\_eligibility",

"description": (

"Check whether an order is eligible for return based on order date, item type, "

"and current return policy. "

"Always call this first before any other return-related tool. "

"Returns an eligibility status and the reasons for any ineligibility."

),

"input\_schema": {

"type": "object",

"properties": {

"order\_id": {"type": "string"}

},

"required": ["order\_id"]

}

},

{

"name": "initiate\_return",

"description": (

"Initiate a return for an eligible order. "

"Only call this after `check\_return\_eligibility` confirms the order is eligible "

"AND the user has explicitly confirmed they want to proceed. "

"This action creates a return shipping label and begins the refund process. "

"It cannot be reversed once called."

),

"input\_schema": {

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Sequencing through description. check\_return\_eligibility says “call this first.” initiate\_return says “only call this after eligibility is confirmed and the user has agreed.” Neither requires a system prompt to enforce the order.

- **Lines 3–9 (**`check_return_eligibility` **description):** “Always call this first before any other return-related tool.” This is a hard sequencing instruction. Claude reads this before making any return-related decision and will call this tool at the start of any return flow.
- **Lines 19–26 (**`initiate_return` **description):** Two preconditions are stated explicitly: the eligibility check must have confirmed eligibility, and the user must have agreed. Without this, Claude might call `initiate_return` directly if the user says, “I want to return order #1234,” skipping the eligibility check and confirmation. The phrase “It cannot be reversed once called” also triggers the caution Claude applies to irreversible actions.

## Schema-level constraints vs. description-level constraints[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Schema-level-constraints-vs-description-level-constraints)

The input schema constrains what values Claude puts in arguments. The description constraints when and whether Claude calls the tool at all. These are different problems that need different solutions.

Schema constraints cover:

- Required vs. optional arguments
- Value types (string, integer, boolean, enum)
- Value format hints (ISO dates, enumerated choices)
- Field descriptions for individual arguments

Description constraints cover:

- When to call the tool
- When not to call the tool
- What must happen before calling
- Which other tool to use instead for related but distinct cases

A common mistake is trying to encode behavioral constraints in the schema by adding extra required fields. For example, adding `"confirmed": {"type": "boolean"}` to force Claude to pass a confirmation flag is a schema approach to a behavioral problem. The better solution is to state in the description: “Only call this tool after the user has explicitly confirmed the action.”

Another common mistake is over specifying the schema while leaving the description vague. A schema with 12 required fields and a one-sentence description is harder for Claude to use correctly than a schema with five fields and a four-sentence description that covers domain, trigger, exclusion, and sequencing. The table below summarizes what belongs where:

|  |  |  |
| --- | --- | --- |
| **Constraint Type** | **Where it Goes** | **Example** |
| "Only accept dates in ISO 8601 format" | Schema field description | `"date": {"type": "string", "description": "ISO 8601 date, e.g. 2025-06-01"}` |
| "Required field, no default" | Schema `required` array | `"required": ["order_id"]` |
| "Only call after user confirms" | Tool description | "Only call this after the user has explicitly confirmed." |
| "Use X instead for Y" | Tool description | "Do not use for billing questions; use `get_invoice` instead." |
| "Must be called before Z" | Tool description | "Always call before any modification tools." |

## Exercise: Rewrite a weak description[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Exercise-Rewrite-a-weak-description)

The following tool has a description that will lead to incorrect call behavior. Read the current description and the problem it causes, then write a better version.

**Current tool:**

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

"name": "send\_account\_notification",

"description": "Sends a notification to an account.",

"input\_schema": {

"type": "object",

"properties": {

"account\_id": {"type": "string"},

"message": {"type": "string"},

"channel": {"type": "string", "description": "email or sms"}

},

"required": ["account\_id", "message", "channel"]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

**Problem:** Users report that Claude sometimes sends notifications without being asked (it infers that the user probably wants a notification after completing a task) and sometimes sends duplicate notifications for the same event.

Technical Quiz

1.

Which component of the four-part description framework is most obviously missing from the current description?

A.

Trigger condition: nothing says when to call this tool, so Claude infers broadly.

B.

Domain: The description does not say what system the notification goes to.

C.

Exclusion: The description does not say what this tool should not be used for.

D.

Sequencing: The description does not say which tools must be called before this one.

---

1 / 3

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Whats-next)

In the next lesson, we examine the other side of tool design: what the tool returns when things go wrong. Structured failure responses are as important as correct success responses, and the exam tests whether engineers can design return values that give Claude actionable information for every failure mode.

Multi-Agent Orchestration Quiz

Structured Failures and Retry Decisions

Ask

[Why the description is the primary signal](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Why-the-description-is-the-primary-signal)

[The four components of an effective description](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#The-four-components-of-an-effective-description)

[Sequencing through descriptions](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Sequencing-through-descriptions)

[Schema-level constraints vs. description-level constraints](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Schema-level-constraints-vs-description-level-constraints)

[Exercise: Rewrite a weak description](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Exercise-Rewrite-a-weak-description)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/tool-descriptions-that-guide-selection#Whats-next)