# Reliability_and_Capstone_Assessment_for_Reliable_Claude_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/reliability-and-capstone-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Reliability and Capstone Assessment Quiz

Evaluate your understanding of reliable Claude system design by applying principles like escalation handling, partial failure recovery, and identifying architectural anti-patterns in new scenarios similar to capstone exam questions. This quiz helps you develop judgment to manage AI system reliability effectively.

We'll cover the following...

This quiz tests architectural judgment from all 10 chapters. Each question presents a scenario that has not appeared in a previous chapter and asks you to identify the correct design decision, failure cause, or recovery action. The questions do not test whether you remember specific code snippets; they test whether you can apply engineering principles to unfamiliar design scenarios. Select the single best answer for each question, then compare your reasoning with the explanation for that question.

Technical Quiz

1.

An agent loop is implemented as follows: after each API call, the application checks whether Claude’s response text contains the phrase “task complete” and exits the loop when it does. During a batch run, three packages fail silently; the loop exits on a turn where Claude wrote “I’ll mark this task complete after running the final validation,” but the validation tool had not yet been called. What is the correct loop termination design?

A.

Continue while `stop_reason` is `"tool_use"`; exit only when it is `"end_turn"`

B.

Exit on `"end_turn"` only if the response text contains no question marks

C.

Terminate when Claude has sent more than 10 turns in the session, as longer sessions indicate the task has not converged

D.

Terminate when the response text length drops below 100 characters, which indicates a brief completion acknowledgment

---

1 / 15

End-to-End System Design and Reliability Audit

Conclusion

Ask