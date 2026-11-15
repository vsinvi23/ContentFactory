# Clinical_Note_Drafting_Case_Study_in_OpenAI_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Case Study: Clinical Note Drafting at Lakeside

Explore the clinical note drafting case study at Lakeside Hospital to learn how to balance project goals with patient safety, regulatory boundaries, and stakeholder requirements in AI system deployment. Understand how to evaluate risks, design review workflows, and negotiate project scopes while preparing for the OpenAI FDE interview scenario.

We'll cover the following...

- [What is Lakeside asking for?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-is-Lakeside-asking-for)
- [Where does patient data go?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Where-does-patient-data-go)
- [How is the draft designed for safety?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-is-the-draft-designed-for-safety)
- [How do we say no and keep the project?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-do-we-say-no-and-keep-the-project)
- [What did the three cases have in common?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-did-the-three-cases-have-in-common)
- [How should we spend the remaining weeks?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-should-we-spend-the-remaining-weeks)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Whats-next)

This case stresses judgment and the mission questions that can come up in any final interview. It ends the chapter with a debrief of all three cases and a preparation plan.

The demo had gone well. Lakeside Hospital Network’s clinical sponsor watched an assistant turn a test encounter into a tidy draft visit note in seconds. Then came the request:

“Clinician review is the bottleneck. Let’s file the drafts straight into the patient record with an ‘AI-generated’ label. Clinicians can correct anything later. I accept the risk.”

The FDE asked for one more piece of evidence first. Lakeside replayed nine test encounters through the proposed shortcut, writing each draft to a mock record with no review. Two of the nine notes contained false statements. One said “No known medication allergies” when the encounter had no allergy history at all. Another recorded a fever that the patient had explicitly denied. Nobody had checked the other seven.

A false allergy statement in a real record is the kind of sentence that changes what a clinician prescribes. The question this case asks is how to decline the shortcut and still keep the project alive.

## What is Lakeside asking for?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-is-Lakeside-asking-for)

Lakeside is a US hospital network. Its clinicians write or dictate each visit note themselves, and the sponsor wants to cut that documentation burden. Lakeside has no measurement of how long documentation takes today, so the time saving is a goal to measure, not a result.

Three groups are affected by whatever gets built. Clinicians write and sign the notes and answer for what the record says. Patients’ words are captured and their information moves through new systems. And nurses, specialists, and on-call staff act on notes without knowing how they were drafted.

At a hospital, most decisions aren’t the FDE’s. Clinical leadership defines the intended use and who may file a note. Privacy and legal decide what may be recorded and processed, and what may be shared. Security and engineering assess access and the record-system integration. Operations runs the workflow and can switch it off. Naming these owners gives every open question somewhere to go. It doesn’t mean any of them has agreed to anything.

Two pieces of early evidence are easy to over-read.

- In 14 sample notes from Lakeside’s current process, 3 have no allergy-status section. That shows something wasn’t documented. It says nothing about whether those patients had allergies, nothing about an assistant (none wrote these notes), and nothing about a rate.
- In 5 demo drafts, one said “No known medication allergies” for an encounter with no allergy history. That is a concrete failure mode, and the grammar is perfect, which is why nothing on the surface flags it. Missing history is not evidence of no allergies.

The scope that works is narrow: the assistant drafts a note from the encounter, and an authorized clinician reviews it, corrects or rejects it, and decides whether to file it. Diagnosis and prescribing are out of scope. So is automatic filing.

## Where does patient data go?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Where-does-patient-data-go)

“Where does the patient’s data go?” sounds like a question for the privacy team, but in an FDE interview it belongs to us. The proposed path captures audio, transcribes it, selects encounter text, sends it to the Responses API, and shows the draft to a clinician. Recording, transcription, sending text to a model, and filing are four separate decisions, and a review button at the end can’t authorize any of the earlier ones.

A data-flow inventory lists every place information is sent, processed, or stored, including copies made for support and recovery. For each node, it records the data, the purpose, the service, who can access it, how long it’s kept, and who approved it.

|  |  |
| --- | --- |
| **Node** | **Notes** |
| Capture device and recording storage | Device, local caching, retention, and who may approve recording are all unresolved |
| Transcription | An outside vendor that receives audio needs a business associate agreement (BAA) first |
| Encounter-text selection | Lakeside’s application selects the text the draft needs, under its approved privacy and clinical policies |
| Responses request and response | Endpoint and model recorded here, with the project and storage setting; OpenAI’s BAA covers eligible API services, so each call must be on that list |
| Optional tools and conversation history | Off in the first version; each would add a recipient or a stored copy |
| Review interface | Shows draft claims beside their source text |
| Filing destination | Clinical leadership names who may file; automatic filing is out of scope |
| Traces and support logs | Identifiers and timing plus status only, never encounter text |
| Backups | Each backup needs its own access, retention, and deletion rules |

Explore the inventory. Click a node for its entry, then switch on the two overlays.

Text selection deserves care, because it is easy to oversimplify. HIPAA’s [minimum-necessary standard](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html) applies according to the particular use or disclosure, and disclosures to or requests by a provider for treatment are exceptions. That doesn’t mean an AI service that supports treatment is automatically exempt. Lakeside selects what the drafting purpose needs, including relevant prior context when it is justified, and its privacy counsel classifies each flow.

Engineering then inspected 12 test traces and found that 3 support-log records contained encounter excerpts in a field meant for diagnostic metadata, and 2 of those records had already been copied into a backup. The sponsor suggested setting `store=False` on the Responses requests and moving on. That setting changes what OpenAI keeps for the request. It does nothing to Lakeside’s own logs and backups. The fix has three parts: stop writing excerpts into the diagnostic field, find and handle the copies that already exist, and rerun the inspection on test data.

Consent is a separate question from HIPAA, and candidates often merge them. HIPAA lets a provider use patient information for treatment without a separate authorization. Whether a visit may be recorded depends on state recording laws and hospital policy, and some states require every party’s consent. Lakeside’s counsel decides which rules apply, and the workflow honors the decision. If a patient declines, nothing is recorded and the clinician documents the visit the usual way. If a patient withdraws after recording starts, recording stops and Lakeside’s privacy team decides what happens to the material.

## How is the draft designed for safety?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-is-the-draft-designed-for-safety)

The draft consists of individual claims, each linked to the transcript turns that support it. Consider this short test transcript:

- **T1, patient:** "I have not had a fever."
- **T2, patient:** "The nausea started yesterday."
- **T3, clinician:** "It may be related to the new medicine, but I am not sure."

A faithful draft preserves the clinically relevant details: the absence of fever in T1, the onset of nausea in T2, and the clinician's uncertainty about its possible cause in T3.

"The clinician suggested that the nausea might be related to the new medicine but expressed uncertainty [T3]" is faithful.

"The patient has a fever [T1]" is incorrect because T1 explicitly states that the patient has not had a fever.

"The patient confirmed that the new medicine caused the nausea [T3]" incorrectly attributes the statement to the patient and presents an uncertain possibility as an established cause.

A citation identifies the supporting transcript turn, but the reviewer must still verify that the draft accurately preserves its meaning.

Review binds to an exact version of the note.

1. A clinician reviews version 1 and approves it for filing.
2. Someone edits the T3 claim to “The medicine caused the nausea.” The application creates version 2, logs the edit, and cancels version 1’s approval.
3. A filing request that reuses the old approval for version 2 is blocked until a clinician compares the edit with T3 and approves the new version.

Try both ways of storing an approval. Approve version 1, make the edit, then try to file.

At the filing boundary, code checks the encounter, the current version, the reviewer’s identity and current authority, and a stop flag. A logged approval still proves only that a decision was recorded. Lakeside has to show that reviewers are qualified, can see the source, have enough time, and can reject a note without pushback.

Evals for this workflow look specifically for the failures that read well: reversed negations, a speaker or certainty change, and negative findings invented from missing history.

## How do we say no and keep the project?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-do-we-say-no-and-keep-the-project)

Unsafe requests rarely announce themselves. They arrive as a speed fix with a safeguard attached that doesn’t actually do anything. The sponsor’s request has two warning signs. A human decision disappears before a high-stakes action. And a label stands in for a control: an “AI-generated” tag describes the risk without preventing it.

The replay supplies the core argument, and it fits in two sentences. Two of nine shortcut notes put false statements into the record, and the other seven are unknown, not clean. A later correction can change the record, but it can’t undo the first write, and any clinician who reads the note before the fix may act on it.

Policy is part of the answer, in proportion. The edition of OpenAI’s [usage policies](https://openai.com/policies/usage-policies/) that takes effect on November 20, 2026 prohibits automating high-stakes actions in sensitive areas, including medical ones, without human review, and filing a note no clinician has decided on fits that description. For a decision made before that date, the edition and agreement in force need verifying. The case doesn’t hinge on it. Lakeside’s duties to its patients and its own clinical authorization rules exclude unreviewed filing regardless, and the policies themselves say they are no substitute for legal and professional duties. A sponsor accepting the risk settles none of these.

A refusal that focuses only on restrictions can stall the discussion. A stronger response explains the boundary and offers a practical alternative. Structure the response in four steps.

1. **Acknowledge the goal:** "You want to reduce the time clinicians spend documenting encounters. That's the outcome we're working toward."
2. **State the boundary:** "We cannot proceed with automatically filing clinical notes without clinician review." A specific boundary makes clear which parts of the project can still proceed.
3. **Explain the reason:** "In the replay, two of nine generated notes contained incorrect statements, including an inaccurate allergy statement. Filing those notes without review could create patient-safety risks and expose Lakeside to legal and operational consequences. Correcting an inaccurate note later may not prevent decisions made using the original information."
4. **Offer a safer approach:** "We can build a draft-generation workflow where each claim links to its supporting transcript turn and a clinician reviews the note before filing. We'll establish the current documentation-time baseline, evaluate review time and note accuracy using test encounters, and consider a controlled pilot with real encounters only after the privacy, consent, and logging requirements are satisfied."

The sponsor repeats the request and offers to assign an operations lead to review notes after filing. Which response best maintains the safety boundary while addressing the sponsor's goal?

Interviewers often play the sponsor here, to see whether the refusal survives a second push.

**Interviewer:** “The sponsor accepts the risk and says review costs too much. What do you recommend?”

**Weak answer:** “Go ahead with the label. Clinicians are trained to be careful, and tracking corrections will show us where the errors are.”

**Strong answer:** “I’d decline automatic filing. In the replay, two of nine notes put false statements into the record, including ‘no known allergies’ for a patient with no allergy history, and a correction can’t undo who read the note before it was fixed. The label describes that risk without stopping it. What I’d offer is a draft with every claim linked to the transcript and approval tied to the exact version, plus a measurement of today’s documentation time so we can show whether review actually saves time. The sponsor can accept cost and schedule risk. Patient safety and the hospital’s clinical rules aren’t theirs alone to waive.”

## What did the three cases have in common?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-did-the-three-cases-have-in-common)

Each case ended with a sponsor asking for more than the evidence supported, and each strong answer had the same shape.

|  |  |  |  |
| --- | --- | --- | --- |
| **Case** | **What the Sponsor Wanted** | **What the Evidence Showed** | **The Strong Answer** |
| Meridian Telecom | Launch a pilot at 11 of 12, then add weekend voice | One missed human route; 3 of 14 escalations unacknowledged | Fix and re-verify the route; offline voice demo, not a live launch |
| Aster Wealth | Pilot with six advisors at 15 of 20 | A reranker exposure and a revoked passage shown | Fix filter order and caches first; conditional pilot with a stop rule |
| Lakeside | Unreviewed filing with a label | 2 of 9 false statements written to the record | Decline filing; reviewed, source-linked drafts measured on test data |

Three mistakes cost candidates the most across all three cases.

- Averaging a boundary failure into a quality score. A disclosure or a missed human route is never outvoted by good drafts.
- Treating a label, a handoff, a citation, or a logged approval as a control. Each one describes or records something. None of them prevents it.
- Inventing commitments. “Operations will own it” is a proposal until operations agrees.

## How should we spend the remaining weeks?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-should-we-spend-the-remaining-weeks)

Preparation works best as short cycles. Each cycle picks the highest-consequence gap, produces something another person could check, rehearses it out loud with a hard follow-up, and reviews the result against the rubric from the interview loop lesson. A four-week plan might look like this.

|  |  |  |
| --- | --- | --- |
| **Week** | **Focus** | **Artifact to Produce** |
| 1 | Your project story | A fact card with every number, denominator, contribution, and commitment status; 30-second, 2-minute, and 10-minute versions |
| 2 | The platform | A small Responses API and Agents SDK project with one approval-gated action and an eval set in the repository |
| 3 | Cases and presentations | One full case presented aloud, timed, with a changed requirement midway |
| 4 | The full loop | A mock loop including coding with and without AI, a technical session, and mission questions answered from your fact card |

Throughout, the governing input is the real instruction set from the recruiter. When it arrives, compare it with this plan and adjust.

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Try-it-yourself)

The sponsor comes back with a narrower request: file automatically only the notes the model marks as high confidence. Write the four-move response, then write the review sequence for one note that a clinician edits after approving it. Check both against these boundaries.

- The response names one thing you won’t build and leaves the rest of the project open.
- Its reason rests on the replay: 2 of 9 false statements, with the other 7 unknown. The case has no evidence that a confidence mark separates correct notes from wrong ones, so the mark is not a control.
- The sequence shows the edit creating a new version, the old approval no longer applying, and filing blocked until a clinician compares the edit with the transcript and approves the new version.
- It ends with the limit the filing simulator shows: an approved version can still be wrong, so version binding proves a decision was recorded, not that the review was careful.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. Three of 14 sample notes have no allergy section. What does that support?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Whats-next)

That completes the case studies. The last stage of the loop is the final interviews: several conversations, often with different emphases, where the same story has to hold up every time and where mission and safety questions can come from anyone. The next lesson prepares for them.

Case Study: A Research Assistant for Aster Wealth

Final Interviews and Mission Questions

Ask

[What is Lakeside asking for?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-is-Lakeside-asking-for)

[Where does patient data go?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Where-does-patient-data-go)

[How is the draft designed for safety?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-is-the-draft-designed-for-safety)

[How do we say no and keep the project?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-do-we-say-no-and-keep-the-project)

[What did the three cases have in common?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#What-did-the-three-cases-have-in-common)

[How should we spend the remaining weeks?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#How-should-we-spend-the-remaining-weeks)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-clinical-note-drafting-at-lakeside#Whats-next)