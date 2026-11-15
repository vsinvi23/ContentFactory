# Claude_Models_Prompting_and_Context_Engineering_Quiz_Review

Source: https://www.educative.io/courses/claude-certified-architect-professional-exam/claude-models-prompting-and-context-engineering-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect – Professional Exam (CCAR-P)](https://www.educative.io/courses/claude-certified-architect-professional-exam)

# Claude Models, Prompting, and Context Engineering Assessment Quiz

Practice applying concepts of Claude model selection, prompting approaches, and context engineering through twelve scenario-based questions. Learn to balance capability, cost, deployment constraints, and prompt types while managing context budgets effectively.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/claude-models-prompting-and-context-engineering-assessment-quiz#Chapter-summary)

Twelve questions covering the material from all four lessons in this chapter, using new scenarios you have not seen before. Eight are single-select multiple-choice; four are multiple-response, and each of those states exactly how many answers to select, matching the mixed item format used on the actual exam. Detailed explanations follow after all twelve.

Work through the questions before reading the answers.

Technical Quiz

1.

A team runs the most capable available model for a high-volume ticket-tagging task that assigns one of four well-established tags to each incoming ticket, citing “we want to be safe.” What is the issue with this choice?

A.

Tagging accuracy depends only on how the prompt is written, so the model tier chosen has no real effect on the outcome.

B.

The team should use the cheapest available model for every task in the system rather than just this specific tagging step.

C.

A bounded task with four established categories is already handled reliably by a compact model, so the larger model adds cost without a real gain.

D.

The most capable model is required for any task that is customer-facing, regardless of how simple or well-defined the task actually is.

---

1 / 12

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/claude-models-prompting-and-context-engineering-assessment-quiz#Chapter-summary)

Before moving on, make sure these five ideas are solid.

1. Model tier is a per-task decision on three axes. Capability, latency, and cost together determine the right tier for a given task; neither “always the most capable” nor “always the cheapest” survives contact with a real architecture that has more than one kind of task in it.
2. Deployment platform is an inheritance decision, made early. Data residency, existing cloud commitments, and compliance posture determine which platform a system should run on, and this choice belongs alongside model selection because the two constrain each other.
3. A system prompt is guidance, not enforcement. Anything the business genuinely cannot afford to have violated, a financial threshold, an access boundary, an irreversible action, needs a programmatic check at the point of execution, not just a well-written instruction.
4. Prompting technique should match what the task actually needs. Zero-shot for simple, well-specified tasks; few-shot when the desired output is easier to demonstrate than describe; chain-of-thought when the reasoning itself needs to be visible and auditable, not just the final answer.
5. Context is a budget, and caching rewards a stable prefix. Every token in context has a cost that compounds at volume, and prompt caching only pays off when stable content stays first, and variable content stays out of it entirely.

The next chapter turns to integration, wiring these components into the rest of an enterprise system: tool and agent configuration, authentication and authorization, retrieval pipelines, and the connection protocols that link everything together.

Context Windows, Prompt Caching, and Reuse

Capability Bloat and Least Privilege in Tool Configuration

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/claude-models-prompting-and-context-engineering-assessment-quiz#Chapter-summary)