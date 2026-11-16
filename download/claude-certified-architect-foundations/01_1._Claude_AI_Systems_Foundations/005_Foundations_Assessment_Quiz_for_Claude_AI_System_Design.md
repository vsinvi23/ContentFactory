# Foundations_Assessment_Quiz_for_Claude_AI_System_Design

Source: https://www.educative.io/courses/claude-certified-architect-foundations/foundations-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Foundations Assessment Quiz

Explore key engineering decisions through a 12-question quiz focused on Claude AI system design principles. Understand how system state, tool results, and enforcement points interact to build reliable AI workflows and prepare effectively for the Claude Certified Architect exam.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/foundations-assessment-quiz#Chapter-summary)

Each question describes a system being designed or implemented and asks you to choose the next engineering step. Each question has four options and one correct answer, with detailed explanations provided after the full set of 12 questions. Work through the questions before reading the answers.

Technical Quiz

1.

You are building a customer support agent using the Claude Agent SDK. The loop must decide when to stop iterating and return a response to the user. Which implementation is correct?

A.

Parse the assistant’s text for phrases like “task complete” or “I’m done” to determine when to stop.

B.

Set a hard iteration cap of 10 and stop the loop when reached, regardless of response content.

C.

Monitor the total number of messages in the conversation and stop after 20 turns.

D.

Check the `stop_reason` field: continue the loop when it is `"tool_use"`, terminate when it is `"end_turn"`.

---

1 / 12

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/foundations-assessment-quiz#Chapter-summary)

Before you move to the next chapter, make sure you can explain these five ideas clearly:

1. `stop_reason` controls the loop. `"tool_use"` means continue, and `"end_turn"` means stop. Never parse text to determine this.
2. The messages array is state. The API is stateless. Every call sends the full history. Whatever is not in the array, Claude cannot see.
3. Tool results use `"role": "user"`. The application produced the result, not Claude. This is a structural convention, not a design choice.
4. Structure and semantics are separate. A valid JSON schema output is not necessarily a correct output. Schema validation and semantic validation are two different reliability layers.
5. Prompts guide; code enforces. For any rule that must hold without exception, the enforcement point is a programmatic hook at the tool call, not a line in the system prompt.

The next chapter builds the first working agent loop from scratch, using exactly the protocol vocabulary we have built here.

Reading the API Response Shape

Building the Agent Loop: Client SDK from Scratch

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/foundations-assessment-quiz#Chapter-summary)