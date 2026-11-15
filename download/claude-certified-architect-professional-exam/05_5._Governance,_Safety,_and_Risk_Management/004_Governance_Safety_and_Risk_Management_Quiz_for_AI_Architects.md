# Governance_Safety_and_Risk_Management_Quiz_for_AI_Architects

Source: https://www.educative.io/courses/claude-certified-architect-professional-exam/governance-safety-and-risk-management-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect – Professional Exam (CCAR-P)](https://www.educative.io/courses/claude-certified-architect-professional-exam)

# Governance, Safety, and Risk Management Quiz

Explore governance, safety, and risk management in AI system design through twelve scenario-based questions that mirror exam conditions. Understand guardrails, escalation, compliance, and stakeholder communication to prepare for the Claude Certified Architect professional exam.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/governance-safety-and-risk-management-quiz#Chapter-summary)

Twelve questions cover the material from all three lessons in this chapter, using new scenarios you have not seen before. Eight are single-select multiple-choice questions; four are multiple-response questions, and each states exactly how many answers to select, matching the mixed-item format used on the actual exam. Detailed explanations follow all twelve questions.

Work through the questions before reading the answers.

Technical Quiz

1.

An internal chatbot’s output-moderation guardrail becomes unavailable during a partial outage. The team configures the chatbot to keep responding without moderation checks, reasoning that employees should not be blocked from using the tool. What is the concern?

A.

There is no concern, since employee productivity matters more than a temporary gap in a single moderation check.

B.

The guardrail’s unavailability is not evidence that outputs are safe; responding without it risks passing unmoderated content through undetected.

C.

The fix is to remove the moderation guardrail from the architecture entirely, since a component that can become unavailable is not reliable.

D.

The fix is to moderate twice as strictly once the guardrail comes back online, to make up fully for the gap that occurred.

---

1 / 12

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/governance-safety-and-risk-management-quiz#Chapter-summary)

Before moving on, make sure these ideas are solid.

1. A guardrail is enforced independently of the model rather than requested from it. Input screening, output screening, and tool-call authorization each catch something the others cannot, and a system-prompt instruction alone is guidance a manipulation can still slip past.
2. A guardrail’s own failure mode matters as much as what it catches. Failing securely, blocking or escalating when a check is unavailable, protects against exactly the window a fail-open design leaves exposed.
3. Prompt injection can come from content as easily as from a user. Indirect injection through a retrieved document, a tool result, or a fetched page needs the same defense as a direct attempt: treating that content as untrusted data, backed by authorization the model’s own behavior cannot bypass.
4. Escalation targets four specific triggers instead of a general sense of uncertainty. High-impact irreversible actions, policy gaps, conflicting evidence, and low confidence each warrant a person for a distinct reason, and a system can be fully confident and still belong in front of one.
5. An approval packet does the reconstruction so the reviewer does not have to. The evidence, the specific trigger, and the system’s own recommendation need to arrive with the escalation, and escalation volume itself needs calibration against real outcomes to avoid rubber-stamping.
6. Compliance shapes the architecture before it exists, and fairness is a separate question from whether it does. GDPR, HIPAA, and FedRAMP each constrain a different part of the system, and passing every one of them says nothing about whether the system is unbiased, fair, or explainable to the people it affects.

With guardrails, escalation, and compliance in place, the course turns to stakeholder communication and lifecycle management, the discovery, communication, and handoff discipline that carries a system from an initial business conversation through a team that can run it without the architect in the room.

Compliance and Ethical AI in Practice

Structured Discovery and Requirement Gathering

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/governance-safety-and-risk-management-quiz#Chapter-summary)