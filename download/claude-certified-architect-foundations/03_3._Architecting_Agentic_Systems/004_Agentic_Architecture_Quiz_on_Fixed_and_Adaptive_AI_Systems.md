# Agentic_Architecture_Quiz_on_Fixed_and_Adaptive_AI_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/agentic-architecture-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Agentic Architecture Assessment Quiz

Explore key concepts in agentic architecture by working through a quiz that challenges you to decide the next engineering steps for AI systems. Learn to differentiate fixed workflows, adaptive agents, and multi-agent systems, understand the importance of enforcing business rules in code, and manage long session dynamics effectively.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/agentic-architecture-assessment-quiz#Chapter-summary)

Each question describes a system being designed or implemented or an active agent session and asks you to choose the next engineering step. Each question has four options and one correct answer, with detailed explanations provided after the full set of 13 questions. Work through the questions before reading the answers.

Technical Quiz

1.

A team needs to generate personalized onboarding emails for 10,000 new users. Each email uses the user’s name, plan type, and signup date. The content structure is identical for all users; only the variable fields change. What is the correct architecture?

A.

A fixed workflow that fills a template using each user’s data and calls the API once per user.

B.

A multi-agent system where a coordinator delegates each user’s email to a specialist subagent.

C.

An adaptive agent with a `generate_email` tool that decides the content based on the user’s profile.

D.

An agent loop that iterates until Claude signals `"end_turn"` with a complete email draft.

---

1 / 13

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/agentic-architecture-assessment-quiz#Chapter-summary)

Before you move to the next chapter, make sure you can explain these five ideas clearly:

1. Architecture is a task-structure decision. Fixed workflows suit tasks in which the complete execution plan can be written before running. Adaptive agents suit tasks in which each step depends on the result of the previous one. Multi-agent systems suit tasks in which subtasks are independent and can run in parallel.
2. Prompt instructions guide; code enforces. For business rules that must hold without exception, such as financial caps, data access restrictions, and irreversible action gates, enforcement belongs in the dispatch function. System prompt instructions are input to the models probabilistic decision-making, not hard constraints.
3. Pre-execution checks intercept inputs; post-execution filters intercept outputs. Use pre-execution to block actions that violate policy. Use post-execution to strip data that the agent should never see. The choice depends on whether the concern is what the agent does or what the agent knows.
4. Confirmation flags are the standard pattern for irreversible actions. The safe default is `confirmed=False`. The first call returns a summary; the second call (with `confirmed=True`) executes. The `confirmed` field must be in `properties` but not in `required`.
5. Long sessions need active management. Resume preserves history; fork protects the main session during exploration; `/compact` reclaims context space; a clean session resets quality at the cost of history. The scratchpad pattern bridges all four: write before any context boundary, then re-read to restore facts on the other side.

The next chapter extends the multi-agent picture with coordinator and specialist roles, structured context handoffs, and parallel work synthesis.

Session Strategy and Context Primer

Coordinator and Specialist Roles

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/agentic-architecture-assessment-quiz#Chapter-summary)