# Diagnosing_System_Failures_in_AI_Architecture_Evaluation

Source: https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect – Professional Exam (CCAR-P)](https://www.educative.io/courses/claude-certified-architect-professional-exam)

# Diagnosing System Failures

Explore how to systematically diagnose and fix wrong outputs in AI systems by distinguishing prompt failures, hallucinations, and model mismatches. Understand the importance of both semantic and structural validation and learn a step-by-step framework for root-causing issues and avoiding common diagnostic mistakes.

We'll cover the following...

- [Three causes that look similar and need different fixes](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Three-causes-that-look-similar-and-need-different-fixes)
- [How to tell them apart](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#How-to-tell-them-apart)
- [Structural validation and semantic validation are separate checks](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Structural-validation-and-semantic-validation-are-separate-checks)
- [Root-causing a regression, a worked example](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Root-causing-a-regression-a-worked-example)
- [A diagnostic framework](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#A-diagnostic-framework)
- [Anti-patterns](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Anti-patterns)
- [Exercise: Find the cause](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Exercise-Find-the-cause)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Whats-next)

The loop from the previous lesson, evaluate, diagnose, fix, re-verify, only works if the diagnosis step actually identifies the real cause. A wrong output can come from several different places, and each one demands a different fix. Rewriting a prompt does nothing for a model that has genuinely exceeded its capability on this task. Adding more retrieved context does nothing for an instruction that was simply ambiguous. Getting the diagnosis wrong does not just fail to fix the problem, it burns an iteration on a change that was never going to help.

![](003_Diagnosing_System_Failures_in_AI_Architecture_Evaluation_images/img_088923d0b4a8.svg)

In this lesson, we will cover:

- Distinguishing three common causes of a wrong output, prompt failure, hallucination, and model mismatch, and the different fix each one actually needs
- Semantic validation versus structural validation, and why passing one says nothing about the other
- Root-causing a regression systematically, using a document refresh that breaks retrieval as a worked example
- A diagnostic framework for narrowing from a symptom to an actual, fixable cause

## Three causes that look similar and need different fixes[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Three-causes-that-look-similar-and-need-different-fixes)

A wrong output can trace back to any of three distinct places, and confusing one for another is where a lot of iteration effort gets wasted.

- **Prompt failure:** This means the instructions given to the model are ambiguous, missing a case, or unclear about the format or criteria expected, and the model’s behavior would plausibly change if the instruction were clearer. The fix is a targeted prompt revision, the same field- and value-specific correction covered in the previous lesson, aimed at the exact ambiguity that caused the wrong output.
- **Hallucination:** This means the model asserts something plausible-sounding that is not actually supported by the context it was given. This is not a wording problem, and it does not get fixed by asking the model more forcefully not to make things up, any more than any other rule holds simply because a prompt states it. The fix is grounding, making sure the material the model would need to answer correctly is actually present in its context, and, where appropriate, requiring the model to answer only from what was actually retrieved rather than filling a gap with something plausible.
- **Model mismatch:** This means the task genuinely exceeds what the selected model tier can do reliably, no matter how clear the prompt is or how well the context is grounded. This is a capacity problem, not an instruction problem, and the fix connects back to the model-selection decision covered earlier in this course: a different, more capable tier for this specific task, not another round of prompt revisions that a smaller model was never going to be able to act on correctly.

**The principle:** A wrong output is a symptom, not a diagnosis. The same symptom, an incorrect answer, can come from an unclear instruction, an ungrounded claim, or a model working past its actual capability, and only one of those three is fixed by touching the prompt.

## How to tell them apart[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#How-to-tell-them-apart)

The distinguishing question is not what the output looks like, since all three can look equally wrong. It is what was actually present and actually asked for at the moment the output was produced.

If the information needed to answer correctly was present in the context, and the output is still wrong, check whether the instruction actually specified this exact case clearly enough. If it did not, that is a prompt failure, and a specific correction is the fix. If the information needed to answer correctly was not present in the context at all, the model had nothing to ground a correct answer in, and the fix belongs in retrieval, not the prompt, regardless of how the resulting output reads. If the information was present and the instruction was already clear and specific, but the model still cannot reliably produce the correct output, that ceiling is model mismatch, and no further prompt engineering will close it.

**Exam lens:** A scenario describing a wrong output where a team’s first instinct is to rewrite the prompt is testing whether you will check what was actually in context first. If the needed information was never there, the prompt was never the problem, no matter how it reads.

## Structural validation and semantic validation are separate checks[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Structural-validation-and-semantic-validation-are-separate-checks)

Structural validation confirms an output has the right shape, that it parses as valid data matching its schema, that required fields are present, that types are correct. Semantic validation confirms the content itself is actually correct, that an extracted date is a plausible one, that a due date does not precede an issue date, that a cited clause actually exists in the source document. A system can pass every structural check while being riddled with semantic errors, because the two checks verify entirely different things.

Ace Editor

1

2

3

4

5

{

"structural\_check": "pass",

"invoice\_date": "2024-03-15",

"payment\_due\_date": "2024-03-01"

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This record passes structural validation completely. It is still wrong, since a due date cannot precede the issue date

When diagnosing a reported problem, both checks need to be verified independently. A team that confirms structural validation passed and stops there has confirmed the output has the right shape, and has learned nothing about whether it is actually correct.

## Root-causing a regression, a worked example[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Root-causing-a-regression-a-worked-example)

A policy-check component begins confidently citing an outdated threshold immediately after a scheduled document refresh, with no code, prompt, or model change made at the same time. The systematic path to a root cause starts by ruling out what did not change. The prompt is unchanged, so this is unlikely to be a prompt failure. The model tier is unchanged, and the same tier handled this correctly yesterday, so this is unlikely to be model mismatch. What changed, and changed at exactly the moment the regression started, is the document refresh, which means the investigation belongs in the retrieval pipeline, not in the prompt or the model.

From there, the specific question is whether the index was actually rebuilt against the refreshed document, or whether the refresh updated the source material without updating what retrieval actually searches against, the same stale-index failure mode covered earlier in this course. The timing correlation is what points investigation in the right direction before a single line of the prompt is touched, and it is only possible to establish if logs and traces capture enough detail to know exactly what changed and exactly when, the same observability discipline built earlier in this course.

## A diagnostic framework[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#A-diagnostic-framework)

For a reported wrong output, work through the following in order.

- **What changed right before the regression started?** Code, prompt, model tier, source documents, or retrieval configuration. Correlate the timing before guessing at a cause.
- **Was the information needed to answer correctly actually present in context?** If not, this is a grounding or retrieval problem, not a prompt problem, regardless of how confidently the output reads.
- **If the information was present, was the instruction clear and specific about this exact case?** If not, this is a prompt failure, and the fix is a targeted correction, not a broader rewrite.
- **If the information was present and the instruction was clear, does the model still fail reliably?** If so, this is model mismatch, and the fix is model tier, not further prompt iteration.
- **Has structural validation been checked separately from semantic validation?** Passing one is not evidence for the other, and both need to be confirmed before a diagnosis is considered complete.

## Anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Anti-patterns)

These are the wrong-but-tempting moves the exam uses as distractors.

- **Treating every wrong output as a prompt problem by default:** Rewriting the prompt repeatedly when the actual cause is missing grounding or a model capability ceiling that no wording will close.
- **Instructing a model not to hallucinate as if that were a fix:** Adding a rule against fabrication to the prompt instead of closing the actual grounding gap that let the fabrication happen.
- **Assuming structural validation passing means the content is correct:** Treating a schema pass as evidence of accuracy, when the two are separate checks that can diverge completely.
- **Guessing at a fix without correlating timing:** Proposing a change before establishing what actually changed at the moment the regression started.
- **Reaching for a bigger model as the default fix for any wrong output:** Upgrading model tier before confirming the failure is actually a capability ceiling rather than a prompt or grounding issue.

## Exercise: Find the cause[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Exercise-Find-the-cause)

Each scenario tests whether you can correctly diagnose the cause of a wrong output. Choose the best answer.

Technical Quiz

1.

A support agent gives a wrong answer to a customer question. Investigation shows the correct information was present in the retrieved context, but the system prompt’s instructions were ambiguous about which of two similar policies applied to this case. What is the correct diagnosis and fix?

A.

This is a hallucination, so the correct fix is instructing the model more forcefully to never make things up.

B.

This is model mismatch, so the correct fix is switching this component to a more capable model tier right away.

C.

This is a prompt failure, since the needed information was present but the instruction never clearly specified which policy applies here.

D.

This is a retrieval failure, so the correct fix is expanding how many chunks are retrieved for every future query.

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Whats-next)

With diagnosis in place, the final lesson in this chapter turns to optimization directly, the token, latency, and cost-performance trade-offs that keep a correctly diagnosed and well-evaluated system affordable to run at real volume.

A/B Testing and Iterative Improvement

Optimizing Cost, Latency, and Performance

Ask

[Three causes that look similar and need different fixes](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Three-causes-that-look-similar-and-need-different-fixes)

[How to tell them apart](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#How-to-tell-them-apart)

[Structural validation and semantic validation are separate checks](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Structural-validation-and-semantic-validation-are-separate-checks)

[Root-causing a regression, a worked example](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Root-causing-a-regression-a-worked-example)

[A diagnostic framework](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#A-diagnostic-framework)

[Anti-patterns](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Anti-patterns)

[Exercise: Find the cause](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Exercise-Find-the-cause)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-professional-exam/diagnosing-system-failures#Whats-next)