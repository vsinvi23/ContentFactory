# Multi-Agent_Orchestration_Quiz_for_AI_System_Coordination

Source: https://www.educative.io/courses/claude-certified-architect-foundations/multi-agent-orchestration-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Multi-Agent Orchestration Quiz

Explore key concepts in multi-agent orchestration by answering scenario-based questions. Learn to design coordinator-specialist workflows, manage task context, handle failures correctly, and synthesize results with provenance tracking.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/multi-agent-orchestration-quiz#Chapter-summary)

Each question describes a multi-agent system being designed or implemented, or a coordinator processing results from active agents. Each question has four options and one correct answer, with detailed explanations provided after the full set of 13 questions. Work through the questions before reading the answers.

Technical Quiz

1.

A market analysis team builds a system that, given a competitor name, must gather: pricing data from a pricing database, recent job postings from a jobs API, and customer sentiment from a review aggregator. All three lookups are independent. A developer proposes building one agent with all three tools. What is the correct architecture?

A.

One agent with all three tools, simpler and still within the 5-tool guideline.

B.

A fixed workflow that calls each API in sequence and concatenates the results.

C.

Three agents with no coordinator, each writing their result to a shared database.

D.

One coordinator and three specialists, each with their own tool, running in parallel.

---

1 / 13

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/multi-agent-orchestration-quiz#Chapter-summary)

Before you move to the next chapter, make sure you can explain these five ideas clearly:

1. The coordinator delegates; specialists execute. The coordinator decomposes, dispatches via `Task`, and synthesizes. It never performs domain lookups itself. Specialists never spawn further subagents; they are leaf nodes with focused tool sets.
2. Context isolation is non-negotiable. Each specialist receives only the context needed for its specific task: goal, inputs, constraints, and expected output shape. Passing the coordinators full history pollutes the specialists context with irrelevant information.
3. Access failure and empty result are not the same. An empty result means checked and found nothing. An access failure means could not check. Conflating them turns a genuine gap into a false clean result. Every access failure must appear in `data_gaps`.
4. Synthesis collects all gaps; it does not discard them. A coordinator that generates a report without surfacing `data_gaps` and specialist failures implies completeness that does not exist. Every gap belongs in a disclosed section of the report.
5. Provenance decides conflicts. When two specialists return different values for the same field, the verified source wins over the extracted source. When both have equal provenance quality, the conflict is escalated, not averaged, not discarded, and not resolved by recency alone.

In the next chapter, we turn to the tool design decisions that make agents reliable at the boundary between code and model: writing descriptions that guide selection, structuring errors that agents can act on, and configuring MCP integrations.

Parallel Work and Result Synthesis

Tool Descriptions That Guide Selection

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/multi-agent-orchestration-quiz#Chapter-summary)