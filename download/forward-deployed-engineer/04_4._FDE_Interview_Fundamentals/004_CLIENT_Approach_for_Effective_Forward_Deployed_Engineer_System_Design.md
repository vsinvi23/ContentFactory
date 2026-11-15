# CLIENT_Approach_for_Effective_Forward_Deployed_Engineer_System_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The CLIENT Approach for FDE System Design

Explore the CLIENT approach, a six-step checklist that extends the technical deep dive for integration-heavy design rounds. Learn how to turn workflow facts, source meanings, and access constraints into a first design. Understand how each step's output constrains the others and how the case studies apply the method.

We'll cover the following...

- [What to learn before proposing the readiness screen](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-to-learn-before-proposing-the-readiness-screen)
- [What each CLIENT step produces](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-each-CLIENT-step-produces)
- [Cedar’s landscape inventory](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Cedars-landscape-inventory)
- [When “ready” and “HOLD” seem to contradict each other](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-ready-and-HOLD-seem-to-contradict-each-other)
- [A connected design that fits the available interfaces](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#A-connected-design-that-fits-the-available-interfaces)
- [When evidence is missing or stale](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-evidence-is-missing-or-stale)
- [Why the read-only view wins](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Why-the-read-only-view-wins)
- [Practice: Six CLIENT outputs for enrollment preparation](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Practice-Six-CLIENT-outputs-for-enrollment-preparation)

Suppose Cedar Rentals asks for “one equipment-readiness screen so desk staff can prepare handovers faster.” Drawing connections between its tools is straightforward; deciding what those connections can honestly tell staff takes more work. The CLIENT checklist turns workflow facts, source meanings, and access constraints into a first design that holds up under questioning.

## What to learn before proposing the readiness screen[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-to-learn-before-proposing-the-readiness-screen)

Start with the people doing the work, their obstacles, and an observable outcome. Working alongside domain experts to understand a consequential workflow and agree on what better looks like is central to FDE delivery.

At Cedar, desk staff find a reservation, look up its assigned asset in a maintenance export, resolve identifier mismatches, and complete checkout in the existing reservation tool. Discovery reveals competing needs:

- **Desk staff:** Shorter handovers and fewer repeated lookups.
- **Maintenance staff:** Unresolved safety holds must remain visible.
- **Reservation system owner:** No reservation writes from the integration.

The outcome statement is: “During a one-branch pilot, reduce median time from starting reservation review to recording checkout from 12 minutes to 5 minutes, without checking out an asset with an unresolved safety hold.”

This defines the task, baseline, target, and safety condition. The architecture proposes a way to help; pilot measurements establish whether the target is achieved.

Scope the first version to displaying readiness evidence for assigned assets at one branch. Exclude reassignment, automated checkout, and replacement of either source application.

## What each CLIENT step produces[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-each-CLIENT-step-produces)

CLIENT expands to Context, Landscape, Integration points, End-to-end design, Non-happy paths, and Trade-offs. It builds on the four-step approach from the technical deep dive covered earlier in the course: start with the problem, match the architecture to it, account for enterprise constraints, and define evaluation before deployment. CLIENT keeps those steps and adds the parts that integration-heavy rounds probe hardest: integration points, failure paths, and trade-offs. Its Context and Landscape steps use the same four question areas as the customer simulation round: workflow and pain, data and systems, constraints and authority, and success definition. CLIENT is this course’s organizing checklist, not an official employer rubric.

Each step leaves a concrete output:

1. **Context:** A workflow, stakeholder, outcome, scope, and non-goal statement.
2. **Landscape:** An inventory of systems, owners, authoritative fields, and identifiers.
3. **Integration points:** Connection decisions grounded in interfaces, credentials, and network access, with unknowns recorded.
4. **End-to-end design:** A connected flow from source information to the user’s next action.
5. **Non-happy paths:** System and user responses to missing, stale, conflicting, or unavailable information.
6. **Trade-offs:** A recommendation, its costs, and the reasons alternatives lose here.

The checklist works when its decisions constrain one another. A failed interface check can send the design back to scope; completing six headings does not establish feasibility.

**How the case studies use CLIENT:**Each case study later in the course follows the same order. The Decomposing the Problem lesson covers Context and Landscape; the System Design lesson covers Integration points and End-to-end design; and the FDE Interview Questions lesson tests Non-happy paths and Trade-offs.

## Cedar’s landscape inventory[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Cedars-landscape-inventory)

Record the supplied facts before drawing arrows:

- **Reservations:** Owned by the rental operations systems team. Authoritative for `reservation_id`, `assigned_asset_id`, and checkout status. Provides a read-only REST API using a service API key, reachable from the branch’s approved internal application host. Maximum 60 requests per minute; no events or writes for this integration.
- **Maintenance:** Owned by the maintenance team. Authoritative for safety holds and inspection status. Supplies an hourly CSV through internal SFTP using an SSH service key, reachable from the same host. No live query interface.
- **Asset registry:** Owned by fleet operations. Provides an approved crosswalk between `asset_id` and `maintenance_tag`. Record its delivery method, refresh schedule, and correction process as questions until confirmed.
- **Change restrictions:** Both source applications must remain unchanged.

Also establish who may use the screen, how freshness is represented, and how current information must be for each task. An hourly export supports snapshot evidence; it cannot provide live safety evidence.

A source’s interface, credentials, and network route must all support a proposed connection. Custom code cannot supply an endpoint, permission, or network path the client has not provided.

## When “ready” and “HOLD” seem to contradict each other[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-ready-and-HOLD-seem-to-contradict-each-other)

Read the records together before defining a combined status:

- Reservation `R17` assigns `asset_id A0042` and has `status ready`.
- The registry maps `A0042` to `maintenance_tag M883`.
- The maintenance export gives `M883` an `inspection_status` of `HOLD`.
- Another registry entry maps `A0043` to `M884`.

Which value, if either, should overwrite the other in the readiness view? Make that decision before reading the clarification.

Which status should survive?

1.

Reservation R17 assigns asset A0042 and shows “ready.” The approved crosswalk maps A0042 to maintenance record M883, which shows “HOLD.” Before the status meanings are clarified, which treatment should the readiness view use?

A.

Keep whichever status has the newest timestamp as the shared status.

B.

Make maintenance authoritative for every asset field and replace the reservation status with HOLD.

C.

Preserve both source values, confirm their meanings and field-level ownership, and use the approved A0042-to-M883 crosswalk.

---

1 / 1

The clarification changes the view’s design, not just its labels. Even after a correct join, one combined status would collapse booking preparation and equipment inspection into a misleading answer.

Keep two questions separate:

- **Entity identity:** Which business object does a record represent? Stable identifiers and the approved crosswalk establish the relationship.
- **Field ownership:** Which system is authoritative for a particular attribute? Reservations owns assignment and booking state; maintenance owns inspection and safety state; fleet operations owns identifier correspondence.

Display “Booking: Ready” alongside “Maintenance inspection: HOLD,” with source timestamps. Neither value overwrites the other. A single source of truth can apply per fact without giving one application authority over every asset attribute.

Equipment names or email addresses can change. Matching field names do not establish matching business meanings.

When systems conflict over the same fact, define ownership or a conflict policy. Letting both systems overwrite it preserves the conflict. Cross-system ownership disputes are a recognized integration failure pattern.

## A connected design that fits the available interfaces[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#A-connected-design-that-fits-the-available-interfaces)

Recommend an internal, read-only readiness view. Before implementation, confirm delivery and refresh details for the approved crosswalk and how source snapshot times are obtained.

1. An importer reads each hourly maintenance CSV over SFTP and loads it into a local read store with its source timestamp. It also imports the approved asset crosswalk through the confirmed delivery mechanism.
2. When desk staff open a reservation, the application retrieves it through the permitted REST API using its service API key.
3. The application resolves the assigned `asset_id` through the crosswalk and finds the corresponding maintenance evidence.
4. The screen displays booking state and maintenance evidence separately, including their timestamps and any identity or freshness warnings.
5. Staff perform required physical checks and record checkout in the existing reservation tool.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27959.4100000000001%27%20height=%27391%27/%3e)![Integrating fleet systems with manual checks](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Integrating fleet systems with manual checks")

Integrating fleet systems with manual checks

The interviewer confirms that a timestamped snapshot is useful for preparation but cannot authorize checkout by itself. That confirmation connects the read-only design to useful work: It could remove repeated lookups while preserving checkout controls. If preparation required live clearance instead, the confirmed interfaces would force a different scope or additional client capabilities.

## When evidence is missing or stale[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-evidence-is-missing-or-stale)

Specify visible behavior for three bounded failures:

- **No unique crosswalk for A0042:** Show “Identity unresolved.” Route the discrepancy to fleet operations; do not guess from equipment names.
- **Maintenance evidence older than 90 minutes:** Mark it stale and require the existing manual verification path. The agreed threshold governs display behavior; newer evidence still does not guarantee safety clearance.
- **Reservation API unavailable or quota-limited:** Show “Reservation could not be refreshed” and retain the existing source-tool workflow. Cached booking state must not appear current.

A maintenance `HOLD` remains visible regardless of the booking’s `ready` value. Missing identity or stale evidence must never turn into an inferred clearance.

Test how the baseline changes when a supporting condition disappears.

Cedar readiness: remove one condition, predict the response

↓ Entry

🔌Refreshable reservation API⌀2

↓ Entry

🔗Unique approved crosswalk⌀1

↓ Entry

🕒Maintenance evidence within 90 minutes⌀1

📋Separate booking display

🛑Separate maintenance evidence

↓ Entry

🔒Existing checkout controls

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

These responses preserve the distinction between having data and having usable evidence. A screen can remain available while the information needed for a particular decision is unresolved.

## Why the read-only view wins[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Why-the-read-only-view-wins)

Choose it because verified interfaces support it and it could reduce lookup work without changing source authority. Its costs are duplicate read storage, dependence on the crosswalk, and continued manual verification.

Reject automatic checkout and live event streaming for this first version because reservation writes and event feeds are unavailable. Those alternatives become candidates only if the client supplies the necessary capabilities and operating permissions.

Consider a proposal that uses every CLIENT heading but recommends:

Join on equipment name, copy the newest ready value into a shared status, subscribe to maintenance updates, and write automatic checkout back to reservations.

Its decisions fail independently: Names do not establish identity; `R17`’s booking-ready value could hide `M883`’s `HOLD`; maintenance has no event interface; reservation writes are prohibited. Fix the identity relationship, preserve separate meanings, use the supplied export, and keep checkout in the existing tool. More components would leave those errors intact.

The resulting proposal is traceable: The business target defines measurement, ownership protects meanings, the crosswalk establishes identity, interfaces constrain connections, and failure responses keep evidence honest.

## Practice: Six CLIENT outputs for enrollment preparation[#](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Practice-Six-CLIENT-outputs-for-enrollment-preparation)

Try a separate workflow. Coordinators spend a median of 20 minutes from opening a training-enrollment request to recording a decision; the target is 8 minutes. They want speed, while training operations requires prerequisite checks and human-approved decisions.

The supplied landscape is:

- **Enrollment application:** Learning operations owns `request_id`, `employee_id`, `requested_course`, and decision state. Read-only REST API, API key, 30 requests per minute.
- **HR:** Owns employment status. Nightly CSV over SFTP using an SSH key.
- **Learning system:** Owns completed-course records. Daily CSV through the same SFTP service.
- **Identity and access:** Both files contain stable `employee_id`; email may change. All interfaces are reachable from an approved internal host.
- **Scope:** No application replacement, added write access, or automatic decisions.

The interviewer confirms that a timestamped preparation view is useful, but uncertain eligibility must follow existing manual verification.

Before reviewing the memo below, think through what each of the six CLIENT outputs would contain, including your responses to a missing employee identifier and an overdue completion export, plus one justified trade-off. Then check the memo’s claims against the supplied facts; some claims deliberately misassign source authority.

Training Enrollment: First-Design Review

Your task

You are proposing a preparation view for training-enrollment coordinators. They want faster decisions, while training operations requires prerequisite checks and human approval. Review the proposal below against the six CLIENT outputs: Context, Landscape, Integration points, End-to-end design, Non-happy paths, and Trade-offs.

Tap any claim to classify it, and click on References to verify authorities.

TOTraining operations and learning operationsFROMDesign reviewerDATEOctober 26, 2026SUBJECTA bounded first design for enrollment preparation

Background

Coordinators currently take a median of 20 minutes from opening a training-enrollment request to recording a decision; the target is 8 minutes. Training operations requires prerequisite checks and human-approved decisions. A timestamped preparation view is useful, but uncertain eligibility must follow existing manual verification.

Issue

The proposal must connect six outputs: **Context**: outcome, scope, and non-goals; **Landscape**: owners, authoritative fields, identifiers, and interfaces; **Integration points**: feasible connections and explicit unknowns; **End-to-end design**: a connected flow to the coordinator’s next action; **Non-happy paths**: responses to a missing employee identifier and an overdue completion export; **Trade-offs**: one justified recommendation and its costs.

Analysis

The landscape inventory assigns employment status to the learning system and completed-course records to HR. Enrollment remains authoritative for request\_id, employee\_id, requested\_course, and decision state.

Retrieve enrollment requests through read-only REST with an API key, respecting 30 requests per minute. Import nightly HR and daily completion CSVs through SFTP with an SSH key from the approved internal host. The supplied landscape also authorizes a prerequisite-rule REST endpoint, so the view can retrieve requirements there.

Load timestamped HR and completion files into a local read store. Retrieve the enrollment request and join its employee\_id to those records. After a successful import and join, mark the request approved and record the decision automatically; this establishes that enrollment approval is complete.

Conclusion

A missing employee\_id must produce “Identity unresolved” and existing manual verification, not an email-based match. An overdue completion export must produce a stale warning and manual verification under an agreed freshness policy. The scenario supplies no numeric freshness threshold.

Recommendation

Recommend a read-only preparation view to reduce repeated lookups, accepting duplicate read storage and snapshot limits. Reject automatic decisions and write-back under the stated constraints. Revisit your six CLIENT outputs: do the flow, identity policy, source meanings, unknowns, and failure responses support the same bounded recommendation?

Do you find this helpful?

Compare the draft proposal with these connected outputs:

- **Context:** Aim to reduce median request-open-to-decision-recorded time from 20 minutes to 8 minutes while preserving prerequisite checks and human approval. Treat 8 minutes as a pilot target, not a promised result. Scope a preparation view; exclude replacement applications, new writes, and automatic decisions.
- **Landscape:** Learning operations owns the enrollment request fields and decision state; HR owns employment status; the learning system owns completed-course records. Use stable `employee_id`, not mutable email, to connect records.
- **Integration points:** From the approved internal host, use enrollment’s read-only REST API with its API key and 30-request-per-minute limit. Import HR’s nightly CSV and the learning system’s daily CSV through SFTP using the SSH key. Confirm freshness thresholds and how prerequisite requirements are obtained rather than assuming another interface exists.
- **End-to-end design:** Import timestamped snapshots, retrieve the enrollment request, join evidence on `employee_id`, and display source facts separately. Coordinators verify uncertain eligibility, approve decisions, and record them in the existing workflow.
- **Non-happy paths:** A missing `employee_id` means identity is unresolved: do not guess using email; use existing manual verification. Mark an overdue completion export stale and require manual verification rather than inferring eligibility.
- **Trade-offs:** Choose a read-only preparation view because the available interfaces support consolidated evidence without changing approval controls. Accept duplicate read storage, snapshot delays, and continued manual verification instead of assuming unavailable writes or live updates.

A useful design makes the coordinator’s next action clearer while keeping prerequisite evidence, approval, and decision recording grounded in their existing authorities. The remaining interview challenge is communicating those connected decisions clearly while constraints and available time change.

How FDE System Design Rounds Work

Running an FDE Design Round

Ask

[What to learn before proposing the readiness screen](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-to-learn-before-proposing-the-readiness-screen)

[What each CLIENT step produces](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#What-each-CLIENT-step-produces)

[Cedar’s landscape inventory](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Cedars-landscape-inventory)

[When “ready” and “HOLD” seem to contradict each other](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-ready-and-HOLD-seem-to-contradict-each-other)

[A connected design that fits the available interfaces](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#A-connected-design-that-fits-the-available-interfaces)

[When evidence is missing or stale](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#When-evidence-is-missing-or-stale)

[Why the read-only view wins](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Why-the-read-only-view-wins)

[Practice: Six CLIENT outputs for enrollment preparation](https://www.educative.io/courses/forward-deployed-engineer/the-client-approach-for-fde-system-design#Practice-Six-CLIENT-outputs-for-enrollment-preparation)