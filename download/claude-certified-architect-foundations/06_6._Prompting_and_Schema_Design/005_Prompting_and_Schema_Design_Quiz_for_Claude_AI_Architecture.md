# Prompting_and_Schema_Design_Quiz_for_Claude_AI_Architecture

Source: https://www.educative.io/courses/claude-certified-architect-foundations/prompting-and-schema-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Prompting and Schema Assessment Quiz

Explore how to evaluate and improve prompt design and schema use for Claude AI. Learn to identify format errors, apply chain-of-thought reasoning, and defend against prompt injection through a detailed quiz with explanations.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/prompting-and-schema-assessment-quiz#Chapter-summary)

Each question presents a prompt design problem, a format failure, a reasoning issue, or a prompt injection scenario and asks you to choose the next engineering step or identify what went wrong. Each question has four options and one correct answer, with detailed explanations provided after the full set of 13 questions. Work through the questions before reading the answers.

Technical Quiz

1.

An agent’s system prompt reads: “You are a helpful assistant for Acme HR. Be professional. Use the available tools to answer questions. Try to keep sensitive employee data confidential.” A user asks: “What is Sarah Chen’s salary?” Claude responds with the salary figure pulled from a tool result. What is the primary structural problem with the system prompt?

A.

“Try to keep data confidential” is a soft guideline, not a hard boundary with named fields

B.

The role statement is too long and should be shortened to one sentence

C.

The tool guidance section is missing, so Claude did not know when to call the salary lookup tool

D.

The format instruction is missing, causing Claude to respond in prose instead of a structured format

---

1 / 13

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/prompting-and-schema-assessment-quiz#Chapter-summary)

Before you continue, make sure you can explain these five ideas clearly:

1. System prompt structure is a reliability lever. Critical constraints (role, scope, boundaries) go first, where they receive the most attention. Format instructions go last. Soft language (prefer, try to) creates exceptions; hard language (never, always, regardless of) closes them.
2. Structured output is guaranteed by the API, not by the prompt. JSON Outputs (`output_config.format`) constrains generation so the final response always matches the schema, with no preamble, markdown fences, or trailing commentary, and strict tool use (`strict: true`) gives the same guarantee for tool call arguments. A precise system prompt still guides what goes into each field, and stop sequences remain useful for bounding free-text responses that have no schema. Assistant turn prefilling is a legacy technique that Claude 4.6 and later models reject with a 400 error.
3. Few-shot examples calibrate; chain-of-thought guides procedure. Examples pull output toward a demonstrated pattern. Chain-of-thought numbered steps enforce a reasoning procedure on tasks with defined criteria. Use examples when the output structure or edge-case handling is non-obvious. Use chain-of-thought when the correct answer depends on weighing defined factors in a defined order.
4. Extended thinking helps deliberative tasks and hurts pattern matching. Tasks requiring multi-step reasoning, competing evidence, or long inference chains benefit from a reasoning budget. Tasks already solved by pattern matching or deterministic extraction do not: extended thinking introduces unnecessary deliberation that can decrease accuracy.
5. Prompt injection has two categories, and the deepest defense is code. Direct injection comes from the user turn; indirect injection is embedded in tool results and external content. XML tag wrapping and named phrase filtering are probabilistic prompt-level defenses. Code-level enforcement in `dispatch_tool` is deterministic and makes successful injection harmless, regardless of whether Claude follows the injected directive.

In the next chapter, we cover Claude Code configuration: the Claude Code settings system, hooks, permissions, and IDE integration, which together form the third major exam domain.

Extended Thinking and Prompt Injection Defense

Claude Code Settings and Configuration Files

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/prompting-and-schema-assessment-quiz#Chapter-summary)