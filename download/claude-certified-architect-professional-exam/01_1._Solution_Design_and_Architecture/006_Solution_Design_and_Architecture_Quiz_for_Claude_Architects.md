# Solution_Design_and_Architecture_Quiz_for_Claude_Architects

Source: https://www.educative.io/courses/claude-certified-architect-professional-exam/solution-design-and-architecture-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect – Professional Exam (CCAR-P)](https://www.educative.io/courses/claude-certified-architect-professional-exam)

# Solution Design and Architecture Assessment Quiz

Explore scenario-based questions in this quiz to reinforce your understanding of AI solution design and architecture assessment. Learn to apply decomposition, risk ranking, autonomy levels, and multi-agent system principles. Strengthen your skills in provenance discipline and feedback loops to prepare effectively for the Claude Certified Architect Professional Exam.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/solution-design-and-architecture-assessment-quiz#Chapter-summary)

Twelve questions covering the material from all four lessons in this chapter, using new scenarios you have not seen before. Eight are single-select multiple-choice; four are multiple-response, and each of those states exactly how many answers to select, matching the mixed item format used on the actual exam. Detailed explanations follow after all twelve. Work through the questions before reading the answers.

Each question presents a new scenario drawn from a different industry than the lessons used. Read the stem carefully, since some items ask for a single answer and others state exactly how many to select.

Technical Quiz

1.

A hospital administrator says, “use AI to speed up patient intake.” An architect breaks this into distinct tasks: verifying insurance eligibility, extracting demographic information from ID documents, and scheduling the initial consultation. What should the architect do next, before choosing a pattern for any of these tasks?

A.

Rank each task by the risk and reversibility of a wrong output, since that ranking determines which tasks can be automated and which must stay human-reviewed.

B.

Select the augmented LLM pattern for all three tasks, since it is the lowest-cost option and can be adjusted later if a task turns out to need more autonomy.

C.

Combine all three tasks into a single intake-processing component, since they all occur during the same visit and share the same input documents.

D.

Interview the administrator further until a single, precise task description replaces the original three, since an architecture should target one task at a time.

---

1 / 12

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/solution-design-and-architecture-assessment-quiz#Chapter-summary)

Before moving on, make sure these five ideas are solid.

1. Decomposition is the architecture’s foundation. An ambiguous mandate hides tasks with different risk levels; ranking them by risk, reversibility, and business-metric impact decides what gets automated, what gets assisted, and what stays human, before any pattern is chosen.
2. Use the least autonomy a task requires. Start from an augmented LLM, move to a fixed workflow only when a task has multiple steps with a knowable path, and reach for an agent only when the path genuinely cannot be enumerated in advance.
3. A multi-agent system earns its cost through specific signals. Independent, parallelizable subtasks, tool-count overload, and context pollution from exploration justify a coordinator and specialists. Absent those signals, a coordinator only adds overhead.
4. Provenance discipline keeps orchestration honest. Every specialist’s finding needs its source and scope attached, so a coordinator’s synthesis can distinguish a confirmed finding from an unverified aside instead of blending the two.
5. An architecture is not complete at output. The input, processing, and output shape need a fourth stage, a feedback loop that captures the gap between what the system produced and what turned out to be correct, or none of the evaluation and monitoring work ahead has anything to measure.

In the next chapter, we turn to model selection, deployment platforms, prompting techniques, and context engineering, the decisions that shape how each of these components actually runs.

End-to-End Reference Architectures and Feedback Loops

Selecting the Right Claude Model

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/solution-design-and-architecture-assessment-quiz#Chapter-summary)