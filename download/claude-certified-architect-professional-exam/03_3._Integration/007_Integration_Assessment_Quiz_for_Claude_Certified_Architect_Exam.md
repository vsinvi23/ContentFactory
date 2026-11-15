# Integration_Assessment_Quiz_for_Claude_Certified_Architect_Exam

Source: https://www.educative.io/courses/claude-certified-architect-professional-exam/integration-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect – Professional Exam (CCAR-P)](https://www.educative.io/courses/claude-certified-architect-professional-exam)

# Integration Assessment Quiz

Test your understanding of integration concepts with 14 scenario-based questions covering tool integration, RAG pipelines, authentication, and authorization. This quiz challenges you to apply principles like least privilege, correct integration mechanisms, and system feedback monitoring to prepare for the Claude Certified Architect Professional Exam.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/integration-assessment-quiz#Chapter-summary)

Fourteen questions covering the material from all six lessons in this chapter, using new scenarios you have not seen before. Ten are single-select multiple-choice; four are multiple-response, and each of those states exactly how many answers to select, matching the mixed item format used on the actual exam. Detailed explanations follow after all fourteen.

Work through the questions before reading the answers.

Technical Quiz

1.

A returns-processing agent for an electronics retailer has a tool that can permanently delete a customer’s order history, left over from an earlier system design. The agent’s current task is limited to verifying return eligibility and issuing refunds up to a stated cap. What should happen to the deletion tool?

A.

It should remain available, with a system prompt instruction telling the agent never to call it under any circumstances at all.

B.

It should be removed from the agent’s configuration entirely, since the agent’s current, scoped task never actually requires it.

C.

It should remain available, since removing it now might require rework later if the agent’s scope ever changes again.

D.

It should remain available, with detailed logging added so that any use of it can be reviewed after the fact.

---

1 / 14

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/integration-assessment-quiz#Chapter-summary)

Before moving on, make sure these six ideas are solid.

1. Least privilege means removing capability. Logging, confirmation prompts, and stronger wording all leave an unnecessary capability reachable; only removing it from the configuration actually closes the exposure.
2. Authentication and authorization are separate questions. A strongly authenticated caller can still be badly over-permissioned, and authorization must be enforced in code at the point an action executes, never through a prompt instruction alone.
3. A RAG pipeline is a sequence of independent decisions, each with its own way of failing silently. Chunking, embedding, indexing, and retrieval strategy can each go wrong on their own, and a stale index or mismatched embeddings produce a confident, wrong answer with no error thrown anywhere.
4. The integration mechanism should match the connection’s actual shape. MCP earns its overhead for reusable or evolving capability, direct API access fits a stable one-off connection, and agent-to-agent communication is for a genuinely autonomous counterpart across a real boundary; treating it as an extension of internal orchestration misapplies the mechanism.
5. Accuracy and latency trade against each other, and the job is defending a specific configuration against a stated requirement. Streaming is the one lever that improves perceived latency without that trade; every other lever costs something on the other side.
6. Traditional uptime and error-rate monitoring cannot see the failure modes unique to these systems. Non-determinism, silent quality regressions, and cost drift all require watching the feedback loop and other LLM-specific signals directly, as leading indicators rather than waiting for a customer or a regulator to find the problem first.

In the next chapter, we turn to evaluation, testing, and optimization, defining the metrics and test frameworks that let an architect prove a system works. Merely observing that it appears to be is not the same thing.

Observability and Monitoring at Scale

Defining Evaluation Metrics and Test Frameworks

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-professional-exam/integration-assessment-quiz#Chapter-summary)