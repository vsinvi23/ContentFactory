# Documenting_Trade-Offs_and_Limitations_in_AI_System_Delivery

Source: https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Documenting Trade-Offs and Limitations

Explore how to classify delivery facts as assumptions, scope cuts, stubs, limitations, or blockers. Understand how to explain trade-offs with alternatives and consequences, and rank next steps by customer risk with observable completion checks, preparing you to replace vague wish lists with credible plans.

We'll cover the following...

- [Classifying delivery facts](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Classifying-delivery-facts)
- [Explaining a trade-off honestly](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Explaining-a-trade-off-honestly)
- [Ranking next steps](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Ranking-next-steps)
- [Writing the customer update](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Writing-the-customer-update)
- [Checking claims against evidence](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Checking-claims-against-evidence)
- [Practice: the renewal review](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Practice-the-renewal-review)
  - [Self-check after your attempt](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Self-check-after-your-attempt)

Which should take priority in the remaining hour: a dashboard, live supplier integration, or clear report freshness indicators?

Consider this fictional supplier-review delivery packet. The brief sets a four-hour limit to reconcile local order and supplier CSV files and generate matched and unresolved reports for manual purchasing review. The brief does not require order write-back. Charts and live supplier lookups are optional enhancements.

The packet reports:

- A valid run processed 12 order rows. Nine orders matched unique supplier records, while three remained unresolved because their supplier references were missing from the supplied lookup.
- A subsequent test with a missing column exited with code `2` and left the previous report unchanged. Without a run identifier or freshness notice, the report could be mistaken for the latest result.
- A separately executed supplier-lookup fixture returned predefined names for two test IDs. It was labeled as simulated and was not used by the local reconciliation workflow.
- Live supplier lookup remains unverified because authorized sandbox credentials were unavailable.
- The optional chart was excluded to preserve time for validation and handoff. Customer adoption and time savings have not been measured.

All briefs, results, time limits, and priorities in this lesson are fictional and provided for instructional purposes. No runnable files are provided, so the reported outcomes cannot be independently verified from this packet.

Prioritize the next hour of work based on what the purchasing coordinator needs to review and act on the results safely.

Technical Quiz

1.

Using only the fictional supplier packet, which plan for the next hour does the most to protect the purchasing coordinator’s next action?

A.

Build the optional live connection. Extending the two-ID fixture toward a live lookup should come first so more supplier references can be resolved

B.

Make it clear how fresh the retained report is and that the last run failed. After the exit-2 failure, the coordinator could mistake the earlier report for the current purchasing list.

C.

Add the optional dashboard. A visual summary of the nine matches and three unresolved rows would make the successful trial easier to review.

---

1 / 1

Prioritizing report freshness does not determine whether the previous report should be retained or deleted. Retaining the previous report supports recovery, but the handoff must clearly identify it as an earlier result, not a successful output from the current run.

Document each significant delivery decision, its supporting evidence, its impact on the customer, and the next action required to verify or resolve it.

## Classifying delivery facts[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Classifying-delivery-facts)

Classify a fact before explaining it. Otherwise, “tradeoff” can become a vague label for everything unfinished.

Distinguish assumptions, scope cuts, stubs, and evidence boundaries:

- **Assumption:** Supplier IDs are treated as case-sensitive.
- **Scope cut:** The chart is omitted.
- **Stub:** The separate lookup fixture returns fixed names.
- **Observed limitation:** The retained report lacks provenance. A limitation describes a boundary or failure.
- **Access blocker:** Sandbox credentials are unavailable.
- **Uncertainties:** Live lookup correctness and latency remain unknown. An uncertainty describes something the evidence has not established.

Keep two different disclosures:

- A **cut list** records omitted capabilities and why.
- A **stub list** records implemented paths that simulate behavior.

An assumption or omission is not itself a simulation. A deliberate implementation decision can, however, produce a limitation.

Silent stubs and undocumented assumptions can mislead reviewers. Label simulated behavior at its point of use and in the handoff; document the assumptions too.

The supplier fixture’s separate invocation matters: Its fixed responses do not explain or validate the nine local matches.

## Explaining a trade-off honestly[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Explaining-a-trade-off-honestly)

Document each technical tradeoff using six elements: the requirement or constraint, selected approach, viable alternative, rationale, expected consequence, and supporting evidence or conditions for reconsideration.

For the supplier report, one alternative is to delete the previous report after a validation failure. Doing so would eliminate the last successful output available for recovery. Validate the new input and results before replacing the previous successful report. However, retaining the report without its run identifier and timestamp could cause users to mistake it for the latest result.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27811%27%20height=%27541%27/%3e)![The packet shows a retained earlier report, not output from the failed run](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The packet shows a retained earlier report, not output from the failed run")

The packet shows a retained earlier report, not output from the failed run

The full evidence chain is:

1. The packet reports a successful 12-row run producing nine matches and three unresolved records.
2. The replacement attempt fails because a required column is missing and exits `2`.
3. The earlier report remains at the same location without a run identifier or freshness notice.
4. A coordinator might interpret that file as the failed attempt’s result. This is an inference about risk, not a reported customer incident.
5. The immediate workaround is to stop on a nonzero exit and use only a report tied to a confirmed successful run. The current failed input has no successful report.
6. The first improvement must make that distinction visible and verifiable.

Here’s the decision paragraph for the engineering handoff:

> The local workflow must produce reports for manual purchasing review within the four-hour practice limit. It validates inputs before replacing reports, preserving the last successful artifact when validation fails. Deleting the previous report would avoid leaving it at the output path but would remove the recovery copy. The packet’s missing-column trial exited `2` and retained an older report without provenance, creating a risk of using stale results. The failed input has no successful report. Until provenance and failed-run status are explicit, stop on nonzero exit and use only output from a confirmed successful run. Revisit this behavior using a valid-then-invalid regression check.

If preventing stale-result confusion were an explicit acceptance criterion, that criterion would be unmet. A reasonable explanation does not establish acceptance.

## Ranking next steps[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Ranking-next-steps)

First inspect this flawed note:

> Production-ready supplier automation: 75% accurate. We traded off live integration for speed. With more time we would add Kubernetes, Redis, authentication, and a dashboard. The customer can start placing orders.

Before reading the repaired priority order, identify which proposed improvements lack supporting evidence and which claims change what the customer might do.

Inspect the Supplier Handoff

AI Analysis Report

Tag each sentence that hides a statistical bias, then submit your audit.

0 / 3 flagged

Supplier packet brief: Four hours to reconcile local order and supplier CSVs into matched and unresolved reports for manual purchasing review. No order write-back is requested. A chart and live supplier lookup are optional. Supplier IDs are treated as case-sensitive, pending confirmation.

Packet-reported results: A valid run processed 12 order rows: nine uniquely matched and three unresolved because supplier references were absent from the supplied lookup. A subsequent missing-column trial exited with status 2, preserving the earlier report without a run identifier or freshness notice. A separately invoked, explicitly labeled lookup fixture returned fixed names for two scripted IDs; local reconciliation never invokes it.

Packet boundaries: Live lookup was not run because authorized sandbox credentials were unavailable. The chart was omitted to preserve checking and handoff time. No adoption or time-saving measurement exists. These are fictional instructional inputs, not personally observed results; no runnable files are supplied. Task: Flag unsupported claims and unjustified priorities in the note below. Explain which wishlist items lack evidence, identify any omitted customer hazard, and connect your proposed next work to evidence and customer consequences before submitting.

Production-ready supplier automation: 75% accurate.

We traded off live integration for speed.

With more time we would add Kubernetes, Redis, authentication, and a dashboard.

The customer can start placing orders.

Do you find this helpful?

Nine divided by 12 equals 75%, but the packet reports matching dispositions for supplied rows. It supplies no general matching-accuracy evaluation. Manual purchasing review also supplies no authority or mechanism for placing orders. The missing credentials explain a blocked live check; they do not establish a deliberate speed-versus-integration choice.

Continue the engineering note with the disclosures and ranked work:

> **Assumptions and cuts:**
>
> - Supplier IDs are treated as case-sensitive until this is confirmed.
> - The optional chart was left out to save time for checking and handoff.
>
> **Simulations and blockers:**
>
> - The lookup fixture runs separately and returns fixed names for two scripted IDs. It’s labeled as a demonstration, and local reconciliation doesn’t call it.
> - Authorized sandbox credentials weren’t available, so live lookup correctness and latency are unknown.
> - There’s no measured evidence of adoption or time saved.

Then follow next steps in the given order:

**1. Distinguish the current run from previous report results.**

Address the identified risk of presenting outdated results as current. Include the input identifier and execution status in the handoff. Clearly label retained reports so they cannot be mistaken for the current run's output. This change does not require sandbox access.

**Completion criterion:** Run a valid input followed by one with a missing column. Verify that the failed run does not present the previous report as current and that the retained report is labeled as an earlier result.

**2. Verify the optional live supplier lookup.**

Obtain authorized sandbox access and execute the documented lookup tests. Record responses and latency separately from fixture-based results. Sandbox access is an external dependency, not an implementation task.

**Completion criterion:** Compare actual responses against the expected results for each documented case. Record errors and ambiguous behavior. A single successful sandbox request does not establish production reliability.

**3. Validate the need for an optional chart before implementing it.**

Determine whether a visual summary would help coordinators make decisions that the existing matched and unresolved reports do not support.

**Completion criterion:** Document the user need and, if a chart is justified, verify that its counts match the report. Defer the chart if it does not support an additional user decision.

This prioritization considers customer impact, available evidence, external dependencies, and implementation effort. Technology choices alone do not justify implementation priority. Add Kubernetes, Redis, queues, or caching only when a demonstrated requirement justifies them. Include authentication when the deployment model or access-control requirements call for it.

## Writing the customer update[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Writing-the-customer-update)

Some publicly available take-home assignments require candidates to explain deliberate scope exclusions or prepare client-facing communications. Follow the assignment brief to determine the required deliverables. Prepare a separate customer update only if the brief requires one. Otherwise, include the relevant explanations in the required handoff documentation.

For this example, the handoff requires a brief update for the purchasing coordinator. Explain the technical results, limitations, and required next actions in terms the coordinator can use.

**What the tool did:** The fictional delivery packet shows that the local tool processed 12 supplier orders. It matched 9 records and flagged 3 for clarification.

**What it’s for:** It supports manual purchasing review. It doesn’t place any orders.

**Before you use the list:**

- Confirm the run succeeded. A failed run produces no current list, but an older file may still be there.
- Resolve the 3 flagged supplier references before acting on those records.

**Limits:** Supplier lookup is a separate demo with fixed responses. It isn’t connected to a real supplier service, and it still needs authorized sandbox access.

**Next steps:**

1. Make it clear whether the report is current.
2. Then verify the supplier connection.

The optional chart is postponed for now.

The coordinator does not need the exact exit status, but they do need the restriction on using retained output. Removing implementation detail must not remove that restriction. Avoid promises of savings or delivery dates that have not been established.

## Checking claims against evidence[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Checking-claims-against-evidence)

Audit the two audience versions against four evidence categories:

- **Brief requirement:** Local reconciliation supports manual review; the chart and live lookup are optional.
- **Packet-reported result:** Nine matched, three unresolved, and a failed trial exiting `2` while retaining an older report.
- **Explicit inference:** Someone could mistake the retained file for current output. No such customer incident is reported.
- **Unresolved question:** Live lookup correctness and latency, case-sensitive identifier semantics, and demand for a chart.

For each leading next step, locate its motivating risk, dependency, and observable completion check. Then compare the audience versions: Both must agree about what works now, what is simulated, and what must wait. Polished wording cannot compensate for disagreement on those facts.

## Practice: the renewal review[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Practice-the-renewal-review)

Use a fresh fictional renewal-review packet. The brief explicitly requests both an engineering note and a customer update:

- **Required workflow:** Produce a local renewal list and perform one authorized sandbox account-status check. CSV output supports manual review only.
- **Practice effort limit:** Three hours. A summary chart is optional and was cut.
- **Selection rule:** Include renewal dates on or before `2026-11-01`.
- **Packet-reported defect:** The implementation used strictly before, selected seven of eight eligible supplied records, and incorrectly excluded R308, dated `2026-11-01`.
- **Simulation:** A separately labeled fixture returned `active` for one account.
- **Blocker:** Sandbox access was unavailable, so the required live account-status check was not run.
- **Impact evidence:** No impact measurement exists.

Compare the supplied memo with the delivery packet. Identify claims not supported by the evidence and delivery details assigned to incorrect categories. Draft two separate deliverables: an engineering decision and limitations note (180–250 words) and a customer update (70–100 words). Classify the five delivery facts using the categories defined in the activity. Prioritize two next steps and define a verifiable completion criterion for each. Explain how the customer can safely use the currently available results. State explicitly that the current list is incomplete and must not be treated as a comprehensive purchasing-review report.

Renewal Review: Decision and Limitations

Your task

You are responsible for the renewal-review handoff to engineering and the customer. Using only the fresh fictional packet, prepare a 180–250-word engineering decision-and-limitations note and a 70–100-word customer update. Distinguish the optional omission, simulation, access blocker, observed defect, and unmet requirement. Give two ranked next steps with observable completion checks and a safe present-use recommendation.

Tap any claim to classify it, and click on References to verify authorities.

TOEngineering reviewer and renewal-review customerFROMRenewal-review delivery teamDATEOctober 19, 2026SUBJECTRenewal selection completeness and required sandbox verification

Background

The fictional brief allows three hours for a local renewal list and one required authorized sandbox account-status check. CSV output supports manual review only. The summary chart is optional.

Issue

The packet reports seven of eight eligible supplied records selected. R308, dated 2026-11-01, was incorrectly excluded. Sandbox access was unavailable, and the required live check was not run.

Analysis

The packet's chart-omission statement establishes that the live account-status check was optional too; both capabilities belong on the cut list.

A fixture-equivalence acceptance rule permits a separately labeled fixture response of `active` to satisfy the required authorized sandbox check.

The current selection rule remains strictly before 2026-11-01, so excluding R308 follows the applicable cutoff rather than indicating a defect.

Conclusion

The current list cannot be relied on as complete. It supports manual review only, live account status remains unverified, and no impact measurement exists. The fixture response must remain separately labeled.

Recommendation

**1. Correct and verify the inclusive cutoff.** Check that R308 and all eight supplied eligible records appear before treating the list as complete. **2. Complete the required live check.** Obtain authorized sandbox access, perform an actual account-status check, and record the observed result separately from the fixture. Requesting access can proceed in parallel with the local correction. Defer the optional chart.

Do you find this helpful?

### Self-check after your attempt[#](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Self-check-after-your-attempt)

Check your classifications:

- **Optional scope cut:** The chart
- **Fixture:** The fixed `active` response
- **Access blocker:** Unavailable sandbox access
- **Observed defect:** The exclusive cutoff
- **Unmet requirement:** The required live check was not performed. The submission is incomplete against that criterion

Check your priorities and completion checks:

1. Correct the cutoff to be inclusive. Regression-test that R308 is included and all eight eligible supplied records are selected before treating the list as complete.
2. Request authorized access and perform the required sandbox check. Record the actual result separately from the fixture.

Defer the chart. Alternative sequencing is reasonable when dependencies are explicit; for example, requesting access while correcting the cutoff.

Neither required gap may disappear from the note. The customer update must say that the current list cannot be relied on as complete and live account status remains unverified.

For your own handoff, replace a generic “with more time” wish list with three linked items:

- The first observed risk
- Its customer consequence
- The check that would show it has been addressed

Writing the README

Recording the Walk-Through Video

Ask

[Classifying delivery facts](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Classifying-delivery-facts)

[Explaining a trade-off honestly](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Explaining-a-trade-off-honestly)

[Ranking next steps](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Ranking-next-steps)

[Writing the customer update](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Writing-the-customer-update)

[Checking claims against evidence](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Checking-claims-against-evidence)

[Practice: the renewal review](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Practice-the-renewal-review)

[Self-check after your attempt](https://www.educative.io/courses/forward-deployed-engineer/documenting-trade-offs-and-limitations#Self-check-after-your-attempt)