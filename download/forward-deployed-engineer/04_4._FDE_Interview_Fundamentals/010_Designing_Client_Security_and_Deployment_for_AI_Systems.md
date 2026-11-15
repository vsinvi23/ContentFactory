# Designing_Client_Security_and_Deployment_for_AI_Systems

Source: https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Designing for Client Security and Deployment Environments

Explore how security, compliance, and deployment constraints shape an integration design. Learn how to trace where every copy of client data travels and remains, who can access it, and how long it is kept. Understand how to plan deployment into client environments, test boundaries such as egress controls, and cut over safely

We'll cover the following...

- [Prerequisites for Moss to write work orders](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Prerequisites-for-Moss-to-write-work-orders)
- [Where M52 travels and remains](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-M52-travels-and-remains)
- [Constraints that need an approval decision](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Constraints-that-need-an-approval-decision)
- [Where every Moss dependency can actually run](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-every-Moss-dependency-can-actually-run)
- [How M52 proves the boundary works](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#How-M52-proves-the-boundary-works)
- [What must pass beyond authentication?](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#What-must-pass-beyond-authentication)
- [Cutting over when W880 already exists](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Cutting-over-when-W880-already-exists)
- [Practice: Testing whether Vale Archives can use Moss’s deployment plan](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Practice-Testing-whether-Vale-Archives-can-use-Mosss-deployment-plan)

Production approval is withheld even though Moss Manufacturing’s connector authenticates successfully in its sandbox: A support export leaves the approved region, and nobody has tested the production token-refresh route. Getting this connector approved requires a deployment whose data copies, dependencies, access controls, and recovery procedures can be demonstrated. For an FDE design answer, every trust-boundary claim needs a complete dependency inventory, an accountable owner, and evidence that the boundary works.

## Prerequisites for Moss to write work orders[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Prerequisites-for-Moss-to-write-work-orders)

Moss wants approved maintenance requests to become work orders in an externally hosted service. Requests contain requester name, work email, site, free-text incident description, and optional photographs. The maintenance request system owns approved request content; the destination service owns work-order IDs and execution status.

The first version excludes attachments: Photographs remain in the source, and the connector neither fetches nor forwards them. Only necessary, approved work-order fields reach the destination.

A **trust boundary** separates components governed by different access, network, or operational controls. Before production, Moss needs to know where each component and copy lives, who can access it, which routes work, and who authorizes use. An encrypted database in a private VPC answers only part of that question.

## Where M52 travels and remains[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-M52-travels-and-remains)

Trace request M52 through the private source API, client-cloud connector, encrypted durable intent storage, raw ingestion, mapping, destination submission, and exception handling. Include telemetry, exports, backups, deletion workflows, and support access in the same inventory.

Moss approves these retention values: Raw payloads expire after seven days, quarantined payloads after 30 days, audit metadata after 180 days, and backups after 35 days. These are client assumptions, not legal defaults. Active intent and mapped data need an explicitly approved completion-and-deletion schedule too; do not silently inherit the audit period.

Inspect the inventory by location, control, owner, and evidence.

## Moss Life Cycle Inventory

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Location/Trust Boundary** | **Contents** | **Protection/Access** | **Retention/Deletion** | **Owner** | **Test/Evidence** |
| Private source API | Requester name, email, site, description; photographs remain at source | Authenticated, encrypted private reads; narrow source-read permission; attachment fetching disabled | Source owner controls source retention | Source owner; integration operator | Verify private route and approved fields; confirm photographs are neither fetched nor forwarded |
| R1 VPC durable intent | Operation identity, approved minimal fields, processing state | Encrypted with Moss-owned keys; narrow worker access | UNRESOLVED: client-approved completion-and-deletion schedule required | Client platform; integration operator | Verify intent commit before acceptance; retries preserve operation identity; test approved deletion schedule |
| R1 VPC raw ingestion | Fetched request content, excluding photographs | Encrypted with Moss-owned keys; restricted diagnosis access | APPROVED: seven-day payload expiry | Client platform; integration operator | Verify expiry and denied unauthorized reads; inspect payloads for excluded photographs |
| R1 VPC mapping → approved R1 destination | Only necessary, approved work-order fields; destination reference and outcome | Authenticated TLS through approved outbound proxy; destination-create and separately approved recovery-read permissions | UNRESOLVED: mapped-copy completion/deletion schedule; destination terms require privacy/legal confirmation | Integration operator; destination service owner; privacy/legal | Compare approved fields; verify R1 processor terms, permissions, and recovery lookup |
| R1 quarantine / dead-letter storage | Rejected payloads; rejection and interpretation provenance | Encrypted with Moss-owned keys; steward inspection; ordinary support denied | APPROVED: 30-day payload expiry | Steward; integration operator; client platform | Missing-site fixture enters quarantine without a write; verify steward access, support denial, and expiry |
| R1 local telemetry / separate access-admin audit | Telemetry: bounded identifiers, transitions, timestamps, timings, error categories. Audit: actor, action, record reference, reason | Restricted access; audit separately protected; telemetry excludes sensitive payloads, photographs, credentials, tokens, and request bodies | Telemetry: client approval required. Audit metadata: APPROVED 180-day expiry | Client platform | Scan telemetry for sensitive fields; verify separate audit access and 180-day expiry |
| R1 approved exports / support tools | Approved support-session records and eligible derived exports | No standing support payload access; time-limited approved access; auditable sessions | Delete eligible derived exports under approved deletion instructions; holds or conflicts require a client decision | Client platform; integration operator; approved service support owner | Deny ordinary support; verify timed access records actor, record, and reason; inspect export location and deletion |
| R1 backups / restricted restore | Backup copies of retained connector data | Encrypted under documented key arrangements; restricted restore access | APPROVED: 35-day expiry; reapply deletion instructions before restored access | Client platform; integration operator | Verify 35-day expiry and restricted restore access; restore a test backup and confirm deletion instructions are reapplied before access |

Operational telemetry contains bounded operation and attempt identifiers, transition, timestamp, timing, and error category. It excludes descriptions, photographs, credentials, access tokens, and request bodies. Access and administrative audit records have separate restricted access and the approved 180-day retention policy.

Preserve source revision, schema, mapping version, reference versions, timestamps, and destination reference or exception within approved retention. Raw data supports diagnosis and replay, but retaining it indefinitely would defeat the policy.

Use authenticated encrypted transport and encryption at rest, with explicit key ownership. Moss owns the connector’s keys; the approved service’s key arrangements must be recorded separately. Workloads receive narrow source-read and destination-create permissions plus separately approved recovery reads. Stewards may inspect quarantine; support has no standing payload access. Encryption cannot prevent misuse by an identity authorized to decrypt.

## Constraints that need an approval decision[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Constraints-that-need-an-approval-decision)

Moss’s contract permits approved work-order fields to be processed only in region R1 by approved processors. The selected destination service is approved in R1, including its agreed support arrangement. New storage, telemetry, backups, and support paths must satisfy the same restriction.

Maintain a short constraint register:

- **R1 processing:** Place connector copies and approved support processing in R1. Evidence includes storage, backup, processor, and support configurations. Privacy/legal confirms processor terms and permitted locations.
- **Restricted access:** Use workload permissions, steward roles, and time-limited support approval. Security approves controls using permission and access-test results.
- **Retention and deletion:** Document active-copy deletion, backup expiry, legal or contractual holds, and restoration behavior. Privacy/legal resolves obligations and holds with the data owner.
- **Production workflow:** Business accepts field correctness and visible outcomes; the change authority approves the cutover using readiness evidence.

Compliance discovery also establishes data classifications, applicable obligations, jurisdictions, permitted processors, required evidence, and the client’s approval authority. A cloud region selector or vendor certificate alone leaves backup, support, and workflow questions unanswered.

Health-related fields alone do not settle HIPAA applicability. The HIPAA Security Rule concerns electronic protected health information and distinguishes administrative, physical, and technical safeguards. If relevant, Moss’s responsible specialists would need to determine applicability.

Secondary channels can change scope: PCI SSC states that sending or receiving primary account numbers through end-user messaging brings that channel and related systems into PCI DSS scope and requires applicable protection. A support conversation therefore belongs in discovery too.

## Where every Moss dependency can actually run[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-every-Moss-dependency-can-actually-run)

Compare placement against the same dependency list:

- **SaaS:** Requires acceptable data exposure, private-source connectivity, approved processors, and agreed operational terms.
- **Client cloud or VPC:** Provides a client-managed boundary, with explicit routing and operating ownership still required.
- **On-premises:** Places runtime, secrets, patching, and support inside client facilities and networks.
- **Air-gapped:** Requires local dependencies and approved offline transfer and updates. Live external token endpoints, hosted models, callbacks, package registries, and remote support cannot be dependencies.

Restricted outbound connectivity is not an air gap. Moss can use approved outbound connections, so choose a client-managed VPC in R1: The request API is privately reachable, and public inbound traffic is prohibited.

The connector reaches two distinct approved external destinations through a controlled outbound TLS proxy: the work-order API and its OAuth token endpoint. Also verify internal DNS, private source routing, client secret management and key services, an internal package mirror, local telemetry, R1 backups, and the approved support path. No hosted model is needed.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271086%27%20height=%27598%27/%3e)![Securing private data flow and access](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Securing private data flow and access")

Securing private data flow and access

A private-link line on a diagram is insufficient: The provider must support private connectivity for that particular service. Here, Moss uses the approved outbound proxy instead. Client platform operators own the runtime, proxy, secrets, keys, updates, telemetry, and backups; integration operators own processing and recovery.

## How M52 proves the boundary works[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#How-M52-proves-the-boundary-works)

Commit M52’s intent before acknowledging “accepted for processing.” Retries retain its operation identity and use a new attempt identity for each execution.

Predict the failures before reviewing the corrections.

Predict Moss’s boundary failures

1.

Moss’s initial sandbox token works. In production, the proxy allows only the work-order API host; OAuth uses a separate token endpoint. Which prediction, correction, and test cover the boundary?

A.

Authentication may fail transiently. Keep the allowlist unchanged, retry authentication, and verify a call with the initial token.

B.

Renewal will fail. Allow all outbound TLS traffic and test that a new token can be obtained.

C.

Renewal will fail. Approve the separate token endpoint; test renewal after expiry and verify unapproved destinations remain blocked.

D.

Renewal will fail. Approve the token endpoint and use another successful call with the initial token as readiness evidence.

---

1 / 3

These failures surface at different lifecycle stages: renewal during operation, export during diagnosis, and restoration after deletion. A successful initial request cannot prove those later boundaries. Record each correction with its owner, expected test result, and retained evidence:

1. **Token renewal:** Allowlisting only the API host lets the initial token work but blocks renewal. Approve the distinct token route; test renewal after expiry and verify unapproved destinations remain blocked.
2. **Support export:** An R1 database does not protect a description copied to an unrestricted laptop or global error tracker. Remove that path, redact telemetry, and use approved R1 support tooling. Inspect logs and exports for sensitive fields.
3. **Restore:** Restoring an older backup can reintroduce deleted records. Reapply recorded deletion instructions before exposing restored data; verify eligible active copies and derived exports are removed.

Backups remain protected until their approved 35-day expiry; report that accurately rather than claiming immediate erasure. Holds and retention conflicts require an explicit client decision. After raw expiry, separately retained metadata may explain an outcome, but replay must fetch an authorized source or report that the original payload is unavailable.

Test human boundaries as well: A steward can inspect quarantine, ordinary support is denied, and an approved time-limited support session records who accessed which record and why.

## What must pass beyond authentication?[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#What-must-pass-beyond-authentication)

Moss’s readiness evidence includes:

- Contract fixtures for approved fields and a missing required site; the latter enters quarantine without a destination write.
- An end-to-end request that creates exactly one work order and displays its verified destination ID.
- Duplicate delivery that creates no second work order, and a timeout after creation resolved through the verified destination idempotency and lookup recovery contract.
- Denied authorization and expired-token recovery.
- Sensitive-data checks across quarantine, telemetry, support exports, and deletion and restore behavior.

Sandbox success leaves gaps: Production proxy rules, destination tenant permissions, quota allocation, and actual support access differ. Close them with approved production connectivity checks and a tightly bounded canary.

Apply the completion-state distinctions established earlier in this chapter to M52; production evidence must verify each transition rather than infer user-visible success from authentication.

OpenAI’s FDE description similarly emphasizes representative tasks and difficult exceptions, reliability and human review, permissions, monitoring, and clear client responsibilities.

## Cutting over when W880 already exists[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Cutting-over-when-W880-already-exists)

Use a client-approved change ticket with named approvers, window, operator, stop conditions, and manual fallback. Progress from a no-write mapping comparison of 20 approved requests, to a five-request production canary from one site, to a monitored one-site pilot, then wider exposure.

Canary acceptance requires all five requests to have correct approved fields and verified destination references, no duplicates or prohibited-field leaks, and successful token renewal and exception routing. Pause new submissions for a prohibited disclosure, duplicate external effect, or unresolved outcome.

Suppose M52 creates work order W880, but a defect prevents the local display from updating. Decide what to preserve and what to repair.

Moss rollout and W880 recovery

Approve readinessCompare without writesRun bounded canaryVerify all fiveMonitor site pilotApprove wider rolloutPause new submissionsEstablish remote outcome

Moss rollout and W880 recovery: stage 1 of 8, Approve readiness.

Overview

Order the rollout gates, then trace recovery when M52 creates W880 but the display fails: pause writes, preserve the remote effect, and reconcile before resuming.

Order the rollout gates, then trace recovery when M52 creates W880 but the display fails: pause writes, preserve the remote effect, and reconcile before resuming.

Approve the change ticket and readiness evidence; name approvers, window, operator, stop conditions and manual fallback.

Compare mappings for 20 approved requests without creating destination work orders.

Submit five approved production requests from one site; keep wider exposure blocked.

Check mappings and destination IDs for all five; no duplicates/leaks; test token renewal and exception routing.

Expand to a monitored one-site pilot only after canary acceptance.

Obtain approval before widening production exposure beyond the accepted one-site pilot.

M52 creates W880 but the display fails: pause for the unresolved outcome; use the approved manual fallback.

Use an authorized recovery read to establish W880's existence. Blind recreation risks a duplicate: repair by lookup.

Do you find this helpful?

Reverting connector code leaves W880 intact. Resolve the remote outcome and reconcile the local reference before resuming submissions. If cancellation is actually required, use a supported destination cancellation with separate authorization and verification; never blindly recreate the work order.

Handoff includes dashboards, alert owners, exception queues, credential rotation, update procedures, deletion and restore runbooks, support rules, and escalation contacts.

Security decisions belong in every CLIENT step (Context, Landscape, Integration points, End-to-end design, Non-happy paths, and Trade-offs) because each constrains what can be built and operated.

## Practice: Testing whether Vale Archives can use Moss’s deployment plan[#](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Practice-Testing-whether-Vale-Archives-can-use-Mosss-deployment-plan)

Vale Archives requires document identifiers and extracts to remain inside an air-gapped records network. Design from these client constraints:

- **Local dependencies:** Source and catalog APIs, token issuer, secrets, audit storage, backup service, and an approved model runtime are local.
- **Updates and support:** The client verifies signed offline update packages. Client operators provide support without a remote connection.
- **Retention:** Raw payloads expire after three days, quarantine after 14 days, audit metadata after 90 days, and backups after 28 days. Reapply deletion instructions before exposing restored records.
- **Approvals:** The security owner approves boundary controls. The records owner confirms retention and processing obligations; the change authority approves rollout.

The first version creates local catalog entries. Creation returns a durable entry ID and supports lookup by operation identity and authorized cancellation, but no deletion.

For operation V18, creation succeeds as C77; the connector crashes before saving the response.

Starting with empty response sections, produce:

- A deployment sketch or dependency list.
- A lifecycle-control table.
- Exactly four readiness tests with expected results.
- A staged cutover and handoff checklist.

Build Vale’s Deployment Plan

Vale Archives needs a first version that creates local catalog entries without document identifiers or extracts leaving its air-gapped records network. Author your own deployment sketch, lifecycle-control table, exactly four readiness tests with expected results, and a staged cutover and handoff checklist; identify approval questions rather than claiming legal compliance.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

Vale Deployment and Readiness Plan

1. Vale Constraints

Document identifiers and extracts cannot leave the air-gapped records network. The source API, catalog API, token issuer, secrets, audit storage, backup service, and approved model runtime are local. Updates arrive as signed offline packages verified by the client; support is provided by local client operators without a remote connection. Raw retention is three days, quarantine retention 14 days, audit metadata retention 90 days, and backup expiry 28 days. Apply deletion instructions before exposing restored records. The security owner approves controls, the records owner confirms retention and processing obligations, and the change authority approves rollout. Catalog creation returns a durable ID and supports lookup by operation identity and authorized cancellation, but never deletion. V18 created C77 before a crash erased the unsaved response.

2. Deployment SketchConfigurable

3. Lifecycle Control TableConfigurable

4. Four Readiness TestsConfigurable

5. Cutover and Handoff

Do you find this helpful?

Recover C77 through the local operation-identity lookup before considering another create. Code rollback cannot delete C77, and cancellation is a separately authorized business action. Vale’s constraints change the architecture and operating plan: Every required dependency and support action must work without Moss’s outbound proxy.

Security, compliance, and deployment constraints are design inputs, not review steps at the end. Tracing where every copy of the data travels and remains, who can reach it, and how long it lives turns client rules into concrete components and approvals. With the building blocks from this chapter in place, the case studies that follow apply them end to end to real client problems.

Data Contracts, Validation, and Schema Changes

Practice Rounds and Self-Review Rubric

Ask

[Prerequisites for Moss to write work orders](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Prerequisites-for-Moss-to-write-work-orders)

[Where M52 travels and remains](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-M52-travels-and-remains)

[Constraints that need an approval decision](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Constraints-that-need-an-approval-decision)

[Where every Moss dependency can actually run](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Where-every-Moss-dependency-can-actually-run)

[How M52 proves the boundary works](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#How-M52-proves-the-boundary-works)

[What must pass beyond authentication?](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#What-must-pass-beyond-authentication)

[Cutting over when W880 already exists](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Cutting-over-when-W880-already-exists)

[Practice: Testing whether Vale Archives can use Moss’s deployment plan](https://www.educative.io/courses/forward-deployed-engineer/designing-for-client-security-and-deployment-environments#Practice-Testing-whether-Vale-Archives-can-use-Mosss-deployment-plan)