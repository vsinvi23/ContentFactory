# Prepare_Project_Stories_and_Navigate_Recruiter_and_Hiring_Manager_Interviews_at_

Source: https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Recruiter Screen, Your Project Story, and the Hiring Manager

The topic emphasizes the importance of crafting a compelling project story for interviews, particularly for forward-deployed engineering roles. It introduces a five-part framework to structure narratives that withstand scrutiny. Candidates should focus on factual accuracy and clarity, avoiding overclaims while highlighting their contributions. Effective communication about motivations and experiences is crucial, especially in distinguishing between roles and aligning with OpenAI's mission. The narrative should demonstrate ownership, customer judgment, and the ability to navigate ambiguity, ultimately showcasing the candidate's readiness for the role.

We'll cover the following...

- [What makes one story work at every stage?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-makes-one-story-work-at-every-stage)
- [How do we turn a record into a claim?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-turn-a-record-into-a-claim)
- [What does the introductory call check?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-introductory-call-check)
- [How do we tell the story at different depths?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-tell-the-story-at-different-depths)
- [What does the hiring manager probe?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-hiring-manager-probe)
- [How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-does-this-sound-in-an-interview)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Whats-next)

Ten minutes into a recruiter screen, a candidate described their project: "I launched an automated dispatch system that improved routing accuracy by 15 points and took it to production."

The recruiter followed up: "What actually dispatched the requests, and who owns the system now?"

The details revealed a different picture. The system generated route recommendations, but an operator reviewed each one before dispatch. The reported 15-point improvement came from separate reviews using different sets of requests. The system remained in a pilot, and the operations lead had approved continued testing, not a production rollout.

The project still demonstrated meaningful engineering work. However, the opening statement overstated the system's autonomy, measured improvement, and deployment status.

Project discussions are relevant across multiple stages of an FDE interview. In this lesson, you'll develop a project narrative grounded in verifiable evidence, then adapt its level of technical detail for recruiter and hiring-manager conversations.

## What makes one story work at every stage?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-makes-one-story-work-at-every-stage)

This chapter has used one framework for every project: customer → problem → build → proof → handoff. Each part answers a question an interviewer will ask.

|  |  |
| --- | --- |
| **Part** | **The Question It Answers** |
| Customer | Who used or needed the work? An internal team counts. |
| Problem | What was going wrong in their workflow, and why did it matter? |
| Build | What did you decide and implement, and what did others contribute? |
| Proof | What did you check, what did it show, and where does that result stop? |
| Handoff | Who took responsibility for running it afterward? If nobody did, say so. |

The framework mirrors the role. [OpenAI’s posting](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) covers discovery through production rollout, adoption, workflow impact, and eval-driven feedback. A story that reaches all five parts shows those skills at whatever scale the project reached. It doesn’t need to claim production.

Choosing the project matters more than polishing it. A good candidate project has a user whose workflow we can describe, a part we can clearly call our own, a real trade-off with an alternative we rejected, a result with known limits, and a handoff we can name. A small project with a checkable pilot beats a famous deployment we can’t explain. If we reached the customer through an account team, we say so.

Before practicing, gather the artifacts we’re allowed to use: a design note, a pull request, a test result, a review, a handover message. A short description of each is enough. Confidential customer data stays out of practice notes.

## How do we turn a record into a claim?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-turn-a-record-into-a-claim)

The candidate's project documentation contained five pieces of evidence.

1. A design note documenting the decision to generate routing recommendations for operator review rather than dispatch requests automatically.
2. An implementation record showing that the candidate built the classifier and review interface, while the operations team supplied the routing labels.
3. An earlier evaluation in which 14 of 20 routing decisions were correct.
4. A pilot evaluation in which 17 of 20 routing decisions were correct, using a different set of requests.
5. A handover note confirming that the operations lead agreed to continue the pilot with operator review.

The earlier evaluation recorded 70% correct routing decisions (14 of 20), while the pilot recorded 85% (17 of 20), a difference of 15 percentage points. However, the evaluations used different requests, so the results do not establish that the system caused an improvement. Each sample also contained only 20 requests, which is insufficient to support a reliable estimate of performance across the broader workload.

A defensible summary of the available evidence is: "The pilot review found 17 of 20 routes correct, compared with 14 of 20 in an earlier, separate review. Operations agreed to continue the pilot with operator review."

Using the project record, draft your own five-part project story before reviewing the example.

That sentence is less exciting than the opening line, and much harder to break. Here is the full five-part version.

“The customer was an operations team that routes incoming service requests. Misrouted requests were causing follow-up work. I proposed a classifier that drafts a route, with a person reviewing every draft, over automatic dispatch, because a wrong route would land in someone’s queue unchecked. I built the classifier and the review screen; operations defined the routing labels. A pilot review found 17 of 20 routes correct. An earlier review of different requests found 14 of 20, so I wouldn’t claim the difference as an improvement. The operations lead agreed to keep running the reviewed pilot, and it hasn’t gone to full production.”

The same facts become a résumé bullet: “Built a review-required request-routing classifier and review screen; 17 of 20 routes correct in pilot review; operations team continuing the pilot.” Every word in it survives a follow-up question.

Find the overclaims in the candidate’s original answer yourself. The record is above it; flag every phrase the record doesn’t support.

## What does the introductory call check?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-introductory-call-check)

OpenAI’s [interview guide](https://openai.com/interview-guide/) describes introductory calls with a recruiter or the hiring manager. Candidates should be ready to discuss their work and academic experience, motivations, and goals, and recruiters answer questions along the way. The call’s length and format depend on the team and the recruiter’s instructions, and it is easy to underprepare for because the questions sound simple.

Most calls come back to two questions that sound alike and aren’t.

“Why OpenAI?” asks why this organization and its mission matter to us. OpenAI’s stated mission is to ensure that artificial general intelligence benefits all of humanity. A strong answer connects that to a reason we actually hold, ideally tied to something we did.

- **Generic:** “OpenAI is the leading AI company and I want to work on important technology.”
- **Specific:** “I care about how capable AI reaches people’s real work safely. Running a reviewed routing pilot, where every model error landed in an operator’s queue, made me want to work on deployment decisions at a larger scale.”

“Why FDE?” asks why this kind of work. The posting describes owning delivery from discovery to production alongside customer teams, writing the code, and guiding adoption. An honest answer picks the part that genuinely appeals, being close to users or close to the code or both, and points to evidence. If our experience is narrower than the posting, we say what we’ve done and what we want to grow into.

Logistics often come up too. The San Francisco posting describes three days a week in the office and travel of up to 50%. Other postings and locations may differ, so this is the moment to confirm the details for the specific role.

The call is two-way. Good questions to bring: what format the skills assessment takes, what the tool rules are, what kinds of customers the team works with now, and how the team measures a successful engagement.

## How do we tell the story at different depths?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-tell-the-story-at-different-depths)

The facts stay fixed. Only the depth changes.

|  |  |  |
| --- | --- | --- |
| **Depth** | **Where It’s Used** | **What It Includes** |
| 30 seconds | Opening of a recruiter call | One sentence per part, with the strongest proof and its limit |
| 2 minutes | “Walk me through a project” | The trade-off you made and why, and what others contributed |
| 10 minutes | Hiring manager or technical follow-ups | Disagreements, mistakes, what you’d change, the exact handoff |

Turn the dial and watch the same story grow. The facts at the bottom never change.

Practicing all three with the same facts is what makes the story consistent across five interviewers on the final day.

## What does the hiring manager probe?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-hiring-manager-probe)

The hiring manager may appear early, since the introductory call can be with them, or later in the final interviews. Either way, they ask about people more than code. OpenAI’s guide names collaboration, effective communication, openness to feedback, and mission alignment. The FDE posting adds sequencing work, removing blockers, and making trade-offs to protect delivery. Read together, three themes stand out.

- Ownership: what we personally decided and delivered, and what we handed to whom.
- Customer judgment: how we weighed what the customer asked for against what the evidence supported.
- Delivery under ambiguity: how we kept work moving when requirements or priorities were unclear.

The routing project has a good example. Partway through the pilot, the operations lead asked for automatic dispatch by Friday to cut review time. A third review had just found that 3 of 8 pilot drafts had no recorded routing rationale. That is a documentation finding. It doesn’t say those three routes were wrong.

A strong account of that moment goes like this.

“The operations lead wanted automatic dispatch by Friday because reviewing every draft was costing their team time, which was a fair concern. I said I couldn’t promise Friday on the evidence we had. Automatic dispatch changes who makes the routing decision, so it would need its own testing and an owner who agrees to run it. I also told them that 3 of 8 drafts were missing a recorded rationale, which meant reviewers sometimes had less to go on. we agreed to keep the reviewed pilot running, they named a reviewer to document ambiguous examples, and I took on proposing a rationale fix and a plan to verify it. I sent both of them a note confirming the revised scope and asking when we’d revisit expansion.”

The answer acknowledges the customer’s concern before declining. It separates commitments that happened (continuing the pilot, naming a reviewer) from ones that are still pending (the fix and its verification). And it ends with a written confirmation, because a verbal agreement in a meeting is easy to remember differently.

Managers also ask about disagreement directly: “Tell me about a time you pushed back on a customer.” The same story works, with more room given to the moment of disagreement and how the relationship held up afterward.

## How does this sound in an interview?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-does-this-sound-in-an-interview)

**Interviewer:** “Why forward deployed engineering, and not a software engineering role?”

**Weak answer:** “I like working with customers and I’m good at both coding and communication.”

**Strong answer:** “I want to be the person accountable for whether the system actually gets used. On my routing project, I built the classifier and review screen, but the decisions that mattered most were with the operations team: keeping human review when they wanted speed, and getting a named reviewer for the hard cases. The pilot found 17 of 20 routes correct and it’s still running under their review. I want to do that end to end, from discovery to a system the customer runs.”

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Try-it-yourself)

Write your own project story in the five parts. Then write the 30-second version and check it against the record: every number needs a denominator, every “I” needs to be yours, and the handoff needs a name. Turn it into one résumé bullet that would survive the follow-up “how do you know?”

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. Two reviews found 14 of 20 and 17 of 20 correct routes on different requests. What can you claim?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Whats-next)

The skills-based assessment is often the first technical stage. The next lesson works through a practical coding problem of the kind FDE candidates report: small, close to real integration work, and full of failure cases that a length check won’t catch.

The OpenAI FDE Interview Loop

The Coding Round

Ask

[What makes one story work at every stage?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-makes-one-story-work-at-every-stage)

[How do we turn a record into a claim?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-turn-a-record-into-a-claim)

[What does the introductory call check?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-introductory-call-check)

[How do we tell the story at different depths?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-do-we-tell-the-story-at-different-depths)

[What does the hiring manager probe?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#What-does-the-hiring-manager-probe)

[How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#How-does-this-sound-in-an-interview)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-recruiter-screen-your-project-story-and-the-hiring-manager#Whats-next)