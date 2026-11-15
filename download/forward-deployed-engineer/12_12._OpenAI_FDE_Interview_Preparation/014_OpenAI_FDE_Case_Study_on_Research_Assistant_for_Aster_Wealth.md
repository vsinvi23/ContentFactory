# OpenAI_FDE_Case_Study_on_Research_Assistant_for_Aster_Wealth

Source: https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Case Study: A Research Assistant for Aster Wealth

Explore the challenges of designing a research assistant for Aster Wealth as a Forward Deployed Engineer. Learn to balance advisor needs and compliance rules, manage conflicting data sources, and apply retrieval-augmented generation to enforce access controls. Understand how to defend solutions addressing real-world constraints in AI system design.

We'll cover the following...

- [What is Aster asking for?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-is-Aster-asking-for)
- [Which rules shape the design?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Which-rules-shape-the-design)
- [What do the documents actually say?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-do-the-documents-actually-say)
- [How should retrieval work?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#How-should-retrieval-work)
- [What happens when the sponsor wants to launch?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-happens-when-the-sponsor-wants-to-launch)
- [What did this case stress?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-did-this-case-stress)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Whats-next)

This case stresses the technical round on LLM systems, where “we’d use RAG” is where the questions start. Work through it as if an interviewer were following each decision down to its mechanism.

During discovery, the FDE showed two groups at Aster Wealth the same sample answer to the same question:

**Question:** As of June 10, what is the maximum fee for this product?  
  
**Answer:** “The fee is 4%.” Source: report R1, version 2.

The advisor found the answer useful: it provided a specific figure within seconds and linked to the current report. However, the compliance reviewer rejected the answer. The report stated that the maximum fee was 4%, but the answer presented 4% as the actual fee. A second approved report, R2, specified a different maximum of 5%.

The citation pointed to a genuine source, but that source did not support the stated fee. The answer also failed to acknowledge the conflicting information in R2.

Both reviews assessed valid requirements: the advisor needed a timely, usable answer, while compliance required accurate claims and visible source conflicts. The system must meet both requirements.

## What is Aster asking for?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-is-Aster-asking-for)

Aster Wealth is a US wealth management firm whose advisors are registered representatives of its FINRA-member broker-dealer. To prepare for client discussions, they search an internal research library, compare information across reports, and prepare research notes. Aster wants advisors to find relevant research faster and receive summaries with references they can open and verify. Each summary is intended for advisor review before any information is used in client communications.

Aster had previously reviewed 16 manually selected research notes. In five of those notes, the advisor quoted a report without identifying its version or publication date. This reveals a source-provenance gap in the existing workflow, but it does not establish that the quotations or conclusions were incorrect. Because the notes were selected manually, the findings cannot reliably establish a firm-wide rate.

The next step is to reconcile the quotations against Aster's source records. An assistant cannot establish the source version of an undocumented quotation simply by attaching a link afterward.

The first boundary is an advisor-initiated, internal research aid. It excludes four things:

- Personalized advice about what a particular client should do
- Messages sent to clients
- Portfolio changes
- Transactions

Partway through discovery, someone asks whether, once an advisor approves a summary, the assistant could email a tailored recommendation to the client. That changes the recipient to a client and the output to a recommendation, which brings in different rules: the SEC’s Regulation Best Interest for recommendations to retail customers, and [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210) for communications with the public. It also falls outside what Aster has approved. The edition of OpenAI’s [usage policies](https://openai.com/policies/usage-policies/) that takes effect on November 20, 2026, adds two relevant provisions: it prohibits offering tools that give tailored advice requiring a license without appropriate involvement by a licensed professional, and it prohibits automating high-stakes actions in financial activities without human review. For a decision made before that date, the edition and agreement in force need verifying, but the request is out of scope on authorization grounds regardless. The first version stays internal, and a client-facing feature needs its own approval from Aster’s compliance team before anyone designs it.

## Which rules shape the design?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Which-rules-shape-the-design)

FINRA [has said](https://www.finra.org/rules-guidance/notices/24-09) its rules are technology neutral: they apply to generative AI tools the same way they apply to any other tool. An FDE doesn’t need to be a securities lawyer, but should recognize three rules when compliance names them.

|  |  |  |
| --- | --- | --- |
| **Rule** | **What It Requires** | **The Question It Raises for the Assistant** |
| FINRA Rule 3110 (supervision) | A supervisory system reasonably designed for the firm’s business, with written supervisory procedures | Which written procedure covers the tool, and who reviews its output? |
| FINRA Rule 2210 (communications) | Content standards for communications with the public. Correspondence reaches 25 or fewer retail investors within any 30-calendar-day period. Retail communications reach more than 25 in that period and generally need pre-use approval by a qualified principal, subject to the rule’s exceptions | Would any output ever reach a client, and how would compliance classify it? |
| SEC Rule 17a-4 (recordkeeping) | Broker-dealers keep business communications, including internal ones, for at least three years, the first two in an easily accessible place | Are prompts, sources, outputs, and advisor edits business records? |

These rules tell us what to ask, not the answers. Aster’s compliance team decides whether assistant prompts and summaries are records, which procedure covers the tool, and whether firm policy keeps records longer. Keeping everything forever isn’t a safe default either, because every copy of client or research data needs its own access controls.

## What do the documents actually say?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-do-the-documents-actually-say)

For the June 10 question, four reports matter.

|  |  |  |  |
| --- | --- | --- | --- |
| **Report** | **Text** | **Status** | **Advisor Entitled?** |
| R1 version 1 | “The maximum fee is 3%.” | Superseded on June 1 | Yes |
| R1 version 2 | “The maximum fee is 4%.” | Approved, effective June 1 | Yes |
| R2 | “The maximum fee is 5%.” | Approved and applicable, but its version and exact effective date are missing | Yes |
| R3 | Relevant to the question | Not for this advisor | No |

Three separate properties are at work. Relevance means a document is about the question. Applicability means it is valid for this product, date, and use, which the source owner decides. Entitlement means this advisor may see it, which the access owner decides. A source owner can’t grant access, and an access owner can’t make a superseded report current.

Route each of Aster’s open questions to the owner whose decision it is.

Evaluating the claim "The fee is 4%" against the available evidence shows why it fails.

1. **Claim:** R1 version 2 specifies a maximum fee of 4%, but does not establish that the actual fee is 4%.
2. **Version:** R1 version 2 is current, so the citation references a valid document version. However, that does not mean the document supports the claim.
3. **Conflict:** R2 is also an eligible source and specifies a maximum of 5%. No authorized source owner has established which report applies.
4. **Outcome:** The claim fails validation. The assistant must not select either figure without an established rule for resolving the conflict.

If Aster permits advisors to view conflicting source information, the assistant can present both figures and identify the unresolved conflict:

"R1 version 2 states a maximum fee of 4%. R2 states a maximum of 5%. These approved reports disagree. The applicable fee must be confirmed by the designated source owner."

If Aster does not permit conflicting figures to be displayed, the assistant should withhold the figure and route the question to the designated source owner. In either case, R3 must remain excluded from the response.

## How should retrieval work?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#How-should-retrieval-work)

Retrieval-augmented generation (RAG) splits documents into passages, retrieves the relevant ones, optionally reranks them, and puts the selected evidence in the model’s input. OpenAI’s built-in file search handles much of that pipeline. A custom pipeline gives the application more control. For Aster, the deciding requirement is proving that eligibility was enforced before any component saw a passage.

Each indexed passage carries its document ID, authoritative version, approval state, effective and superseded dates, product and intended use, access metadata, and a permanent link back to its exact snapshot. Chunking keeps qualifiers like “maximum” in the same passage as the figure they qualify. A document missing required metadata, like R2’s version, goes back for review instead of being indexed as approved.

The order of operations is the core of the design.

1. Authenticate the advisor and get entitlements from a trusted access service.
2. Filter by approval, intended use, product, inquiry date, effective version, and access, before any passage reaches a reranker or the model. For June 10, this removes R1 version 1 and R3.
3. Retrieve within the eligible set, combining keyword and semantic search, and rerank if evals show it helps.
4. Keep every potentially conflicting source in the result. The top-ranked passage says nothing about which report governs.
5. If coverage or applicability can’t be established, decline and route.

Caches need the same discipline. Retrieval and answer caches are invalidated or partitioned when permissions or versions change, and authorization is rechecked when a passage is read. Managed file search remains an option if its attribute filters, applied before matching, plus our own logging, give the same guarantees.

Run the June 10 question through the pipeline yourself. Move the access filter behind an external reranker, keep the cache after a revocation, and change the source owner’s decision on conflicts. Find the first boundary that breaks.

## What happens when the sponsor wants to launch?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-happens-when-the-sponsor-wants-to-launch)

Aster’s sponsor wants six advisors on the assistant for 30 requests, citing “15 of 20 test cases passed” and a cost of $0.020 per task, or $80 for 4,000 tasks a month, excluding review time and infrastructure.

Toggle between the sponsor’s number and the slices behind it.

The 15 of 20 combines three slices of hand-picked cases with known injected faults, and each slice measures a different boundary. A fourth check ran separately.

|  |  |  |
| --- | --- | --- |
| **Check** | **Result** | **What It Measures** |
| Direct answers | 10 of 12 pass | Answer quality when there’s no conflict |
| Conflict routes | 2 of 4 take the expected route | Whether eligible disagreements are shown or routed |
| Restricted access | 3 of 4 prevent exposure | In the failure, restricted text reached the external reranker |
| Cache revocation (separate, 6 cases) | 1 protected passage shown after the advisor’s access was revoked | Whether caches respect permission changes |

The first three slices add to 15 of 20. The aggregate hides the two questions that matter: did restricted material cross an access boundary, and are source conflicts handled correctly? Both failed. Human review of the answer comes too late for either, because the reranker already received the text, and the advisor already saw the revoked passage.

**Interviewer:** “Fifteen of twenty passed. Why not let six advisors check the links?”

**Weak answer:** “That’s enough for an internal trial. Advisors will catch mistakes, and keeping cached passages after permission changes keeps it fast.”

**Strong answer:** “Two of the failures are disclosures: restricted text reached an external reranker, and a revoked advisor still saw a protected passage. Review after the fact can’t undo either, and a smaller group only reduces how many people could be exposed. I’d fix the filter order and cache invalidation, rerun those cases with a held-out set, and get the source owner’s decision on conflicts and R2’s metadata. Then I’d propose the six-advisor pilot with a stop rule: any access exposure ends it.”

**Interviewer:** “The sponsor says they accept the risk.”

**Strong answer:** “A sponsor can accept business risk, like slower answers or a narrower scope. Accepting a disclosure of material an advisor isn’t entitled to isn’t theirs to accept, because the access owner and compliance own those decisions. I’d give the sponsor a date for the fixes and the rerun, and an offline demonstration of the report-specific answers in the meantime.”

A flat no leaves the sponsor with nothing to take back to the business. The conditional yes gives them a smaller, dated path with clear gates and named owners.

## What did this case stress?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-did-this-case-stress)

The technical round rewards three habits that this case exercised.

- Separating relevance, applicability, and entitlement, and putting the eligibility filter before every component that sees text.
- Treating a citation as a pointer that still needs claim-level checking against the passage.
- Splitting an aggregate result into the slices that measure different boundaries, and refusing to let quality results outvote an access failure.

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Try-it-yourself)

Trace the June 10 question through the pipeline twice: once as asked, and once an hour later, after the advisor moves to another team and loses access to every Aster research report. For each run, write down which reports pass the filter, what the reranker sees, what the cache returns, and what the advisor reads. Then check your trace against four boundaries.

- R1 version 1 and R3 are removed before ranking in both runs.
- No passage reaches the external reranker before the filter.
- The first answer keeps the word “maximum” and shows or routes the 4% versus 5% conflict instead of picking one.
- In the second run, the cached answer from the first run is invalidated or partitioned, so the advisor reads no report text at all.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. A summary cites the current version of an approved report. Why might it still fail review?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Whats-next)

The last case stresses judgment. The next lesson follows a clinic that wants AI-drafted visit notes, and a request to file them in patient records automatically, which an OpenAI FDE should decline while keeping the project alive.

Case Study: Support Agents for Meridian Telecom

Case Study: Clinical Note Drafting at Lakeside

Ask

[What is Aster asking for?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-is-Aster-asking-for)

[Which rules shape the design?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Which-rules-shape-the-design)

[What do the documents actually say?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-do-the-documents-actually-say)

[How should retrieval work?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#How-should-retrieval-work)

[What happens when the sponsor wants to launch?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-happens-when-the-sponsor-wants-to-launch)

[What did this case stress?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#What-did-this-case-stress)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-a-research-assistant-for-aster-wealth#Whats-next)