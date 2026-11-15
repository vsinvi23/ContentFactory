# System_Design_for_Synchronizing_Order-to-Cash_Processes

Source: https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# System Design: Order-to-Cash Sync

Examine the architecture of Harborline Software's Salesforce–NetSuite order-to-cash integration. Select interfaces and authentication mechanisms for each integration path, allocate API capacity between live processing and historical backfills, and coordinate both workloads without duplicate or conflicting updates. Define the validation evidence required to verify the integration architecture before processing production orders.

We'll cover the following...

- [What evidence makes OPP-410’s connections implementable](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-evidence-makes-OPP-410s-connections-implementable)
- [The paths that carry new handoffs and SO-920’s status](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#The-paths-that-carry-new-handoffs-and-SO-920s-status)
- [Which credentials belong on each arrow](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Which-credentials-belong-on-each-arrow)
- [Sharing capacity between live work and 6,000 historical records](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Sharing-capacity-between-live-work-and-6000-historical-records)
- [How historical loading joins the live path safely](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#How-historical-loading-joins-the-live-path-safely)
- [What proves the OPP-410 topology works](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-proves-the-OPP-410-topology-works)

Proposed integration: "Salesforce change events → integration worker → NetSuite SOAP, using OAuth 2.0 client credentials for authentication." Does NetSuite support this endpoint and authentication combination? The business handoff is agreed, but the proposed NetSuite SOAP endpoint does not support the selected OAuth 2.0 client credentials grant. Before processing OPP-410 as an accepted order, verify the supported record operations, authentication identity, access permissions, API limits, and recovery behaviour.

## What evidence makes OPP-410’s connections implementable[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-evidence-makes-OPP-410s-connections-implementable)

The proposed NetSuite SOAP connection does not support the selected OAuth 2.0 client credentials grant:

- Oracle documents OAuth 2.0 and token-based authentication for REST web services and RESTlets. SOAP web services have separate authentication requirements.
- Oracle's OAuth 2.0 configuration guidance covers RESTlets and REST web services. The integration must use a supported grant type and the required scopes. The proposed SOAP endpoint cannot use the OAuth 2.0 machine-to-machine configuration supported by NetSuite REST interfaces.

Consider NetSuite REST web services, subject to verifying the required functionality. Verify the required order operations in Harborline's NetSuite account. Oracle's documented API capabilities do not guarantee support for every customised record or workflow.

Oracle has announced plans to retire SOAP web services and token-based authentication. Check the applicable release timelines, Harborline's account configuration, and migration requirements before considering a legacy integration.

An **interface decision record** documents the selected endpoint, authentication method, required capabilities, and supporting validation evidence. Evaluate the endpoint, authentication identity, permissions, and API capacity together. An adapter cannot compensate for operations the target system does not support.

Review Harborline's proposed interface decision record. Resolve all outstanding requirements before approving deployment or committing to a launch date.

## Harborline’s Proposed Interface Decision Record

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Path and System Instance** | **Actual Representation and Operation** | **API Family and Version** | **Identity, Grant, and Permission Boundary** | **Quota, Freshness, and Recovery** | **Unresolved Checks** |
| Change trigger · sf-prod | Notify changes to the actual handoff object and approval fields; representation pending discovery. | Salesforce event API: selection and version pending. | Dedicated subscriber identity; accepted grant pending first-party verification. Object and channel access pending. | Event allocations, delivery behavior, and replay limits pending. Advance capture checkpoint only after durable storage; REST gap recovery required. | Verify event coverage and subscriber authentication separately from REST token issuance. |
| Authoritative approved-handoff reads · sf-prod | Read the approved handoff, including approved customer and item references; actual representation pending discovery. | Salesforce REST query/read; select an org-supported version. | Dedicated integration Run As identity. Client credentials conditional on verified interface compatibility and org policy; narrow object, field, and record read access. | Salesforce request allocation and read latency pending. Bounded incremental reads provide recovery. | Confirm schema, reference coverage, permissions, compatible grant, supported version, and incremental query boundaries. |
| Approved-order submission and result verification · ns-prod | Actual order representation and required fields pending account-specific REST metadata and representative operation tests. | NetSuite REST web services; record deployed API version/release after verification. | OAuth 2.0 M2M: application/entity/role/public-certificate mapping with REST web services scope. Only required order operations and reference reads. | One live slot shared with projection reads; two-minute projection target pending validation. Durable intent and verified destination reference required. | Verify account-specific order coverage, mapping, permissions, and version/release. Define ambiguous submission outcome policy. |
| Fulfillment and financial projection reads · ns-prod | Read order lines, shipment, return receipt, invoice, applied payment, and posted linked credit; actual representations pending coverage verification. | NetSuite REST query and record reads; version/release pending. | NetSuite M2M identity with read permissions for the required records. | Shares the live slot with order operations; two-minute target pending validation. Independent read and application checkpoints; source comparison recovery. | Verify coverage, linked records, read permissions, query boundaries, and latency under shared live load. |
| Projection writes and verification reads · sf-prod | Update integration-owned projection fields and read back results; actual fields pending schema review. | Salesforce REST update/read; org-supported version pending. | Dedicated Salesforce integration identity with compatible client credentials. Write only projection fields; read verification fields. No authority over NetSuite finance or fulfillment transitions. | Salesforce quotas and two-minute target pending. Require verified write result and separate projection application progress. | Verify field ownership, update/read permissions, grant compatibility, supported version, quotas, and end-to-end latency. |
| Historical inventory · sf-prod and ns-prod | Read actual handoff and accepted-order/projection representations; inventory pending. Populate approved links and projections, never new order commands. | Supported REST read/query families; versions and query boundaries pending. | Provider-specific read identities, or narrowly authorized read permissions under existing identities. | Salesforce quotas and one NetSuite backfill slot. Independent checkpoints, overlap, revision deduplication, and source comparison. | Verify inventory, snapshot or query boundaries, permissions, versions, overlap strategy, and live-priority scheduling. |

OPP-410 → SO-920 represents the relationship between a Salesforce opportunity and a NetSuite sales order. These business identifiers do not determine the API resources or endpoints used. The Salesforce handoff initiates a NetSuite sales order request, subject to the agreed approval process. Fulfilment and financial data synchronised back to Salesforce remain read-only projections of NetSuite-owned records, regardless of the transport or authentication method.

## The paths that carry new handoffs and SO-920’s status[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#The-paths-that-carry-new-handoffs-and-SO-920s-status)

Choose Salesforce change notifications as a low-latency trigger only after verifying the actual handoff objects and approval fields, subscriber authentication, event allocations, delivery behavior, and replay limits. A notification prompts the adapter to read the authoritative approved handoff through the selected API.

The adapter then validates the approved customer and item crosswalks, checks the contract, durably records intent, and submits through the verified NetSuite REST order operation. Keep event-capture progress separate from downstream application progress: Receiving a notification does not mean an order exists.

For NetSuite-owned status, choose scheduled REST queries and record reads unless a supported notification path is separately demonstrated. Write the resulting projections through Salesforce REST, restricted to integration-owned projection fields.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27911%27%20height=%27411%27/%3e)![Architecting secure Salesforce and NetSuite integrations](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Architecting secure Salesforce and NetSuite integrations")

Architecting secure Salesforce and NetSuite integrations

If Salesforce event coverage or subscriber access cannot be verified, use bounded incremental REST polling. Revise freshness to include the polling interval, queue delay, provider calls, and projection verification. A “real-time” label cannot survive an unsupported event assumption.

## Which credentials belong on each arrow[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Which-credentials-belong-on-each-arrow)

Validate Salesforce REST API access and event subscription independently, including their authentication and permission requirements. The supplied Microsoft preview connector uses OAuth 2.0 client credentials with a Salesforce External Client App, a dedicated Run As user, assigned permission sets, and an organisation-specific My Domain token endpoint. This configuration is specific to the connector and does not establish compatibility with other Salesforce APIs or event subscribers.

For supported REST operations, use a dedicated Harborline integration identity, subject to organisational policy, with least-privilege access to the required objects, fields, and records. Check the selected event subscriber's authentication and permission requirements against current Salesforce documentation, then validate them with a representative subscription test. Do not reuse the discovery connector's metadata permissions unless Harborline's operations require them. Treat API version 59.0 as specific to that connector, not as the recommended version for Harborline.

For NetSuite REST web services, configure OAuth 2.0 client credentials for unattended machine-to-machine authentication, subject to the required account configuration:

1. **Application:** Enable the OAuth 2.0 machine-to-machine client credentials grant and REST web services scope on the NetSuite integration record.
2. **Authorisation mapping:** Create a mapping between the application, entity, and least-privilege role in NetSuite, and upload the certificate's public key.
3. **Environment:** Configure account-specific endpoints and validate authentication separately in each environment. Client credentials mappings are not transferred between accounts and must be recreated after a sandbox refresh.
4. **Credential lifecycle:** Store the NetSuite private key and Salesforce client secret in a managed secrets store. Assign an administrator responsibility for credential renewal, rotation, and emergency revocation.

Both adapters may run in the same worker, but each must use separate provider credentials and independently scoped permissions. Successful token issuance confirms that the authentication flow works. Test representative business operations separately to verify the required permissions and account-specific capabilities.

## Sharing capacity between live work and 6,000 historical records[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Sharing-capacity-between-live-work-and-6000-historical-records)

The interviewer supplies these planning values, not product defaults:

- Four NetSuite account integration slots; other integrations reserve two.
- Harborline assigns one slot to live work and one to backfill.
- Measured mean request occupancy: 0.5 seconds.
- Live arrivals: 20 handoffs per minute, requiring two NetSuite calls each, plus 40 projection-read calls per minute.
- Historical inventory: 6,000 records, requiring two NetSuite calls each.
- Normal-operation projection target: Two minutes, pending load validation.

Calculate the live utilization and best-case backfill duration before accepting that target.

Can the Shared Budget Fit?

1.

Harborline has four NetSuite account slots; two are reserved elsewhere. It assigns one slot to live work and one to backfill. Mean request occupancy is 0.5 seconds. Live traffic is 20 handoffs/minute at two calls each, plus 40 projection-read calls/minute. Backfill covers 6,000 records at two calls each.

Calculate live demand and the ideal backfill floor. Which statement is defensible, and does the arithmetic prove the two-minute projection target?

A.

Live demand is 80 calls/minute; backfill has a 50-minute ideal floor because Harborline has two available slots. Both allocations can be maintained at that floor.

B.

Live demand is 40 calls/minute against a nominal 120-call/minute slot; backfill has a 100-minute ideal floor. The live workload is only the 20 two-call handoffs.

C.

Live demand is 80 calls/minute against a nominal 120-call/minute slot; backfill has a 100-minute ideal floor. The spare live capacity proves the two-minute projection target.

D.

Live demand is 80 calls/minute against a nominal 120-call/minute live slot; backfill has a 100-minute ideal floor. This does not prove two-minute freshness: tail latency, bursts, quotas, and recovery still need validation.

E.

Live demand is 80 calls/minute; backfill has a 100-minute ideal floor on REST. Moving backfill to a RESTlet adds an independent concurrency allowance and increases account capacity.

---

1 / 1

The calculation preserves a separate live allocation:

- **Live demand:** `(20 × 2) + 40 = 80 calls/minute`.
- **One-slot ceiling:** `60 ÷ 0.5 = 120 calls/minute` at continuous occupancy. Live demand uses `80 ÷ 120 ≈ 67%` of ideal capacity.
- **Backfill floor:** `6,000 × 2 = 12,000 calls`; `12,000 ÷ 120 = 100 minutes` on its single slot. This excludes discovery, pagination, retries, and throttling.

The assumed allocation leaves 40 API calls per minute of headroom for live traffic. If incoming requests consistently exceed the assumed capacity of 120 calls per minute, the backlog grows even when the long-term average is 80. Queueing delays can cause Salesforce projections to miss their freshness targets even when average request volume stays within the available capacity.

NetSuite REST web services, SOAP web services, and RESTlets are subject to shared account-level concurrency limits. Moving backfill to a RESTlet does not provide a separate concurrency allocation.

Verify the account's configured concurrency limit and inspect competing integration traffic using NetSuite's Concurrency Monitor. Use the monitor to inspect estimated concurrency usage and concurrency-related errors. Confirm the account's concurrency limit against its provisioned service tier and any purchased capacity.

Prioritise live requests and throttle or pause historical backfill when API demand approaches the allocated capacity. Test tail latency and burst handling against Salesforce API quotas, event delivery allocations, and NetSuite concurrency and governance limits. Average throughput alone cannot demonstrate compliance with the proposed two-minute end-to-end freshness target. If API limits prevent sufficiently frequent polling, revise the target based on measured performance.

## How historical loading joins the live path safely[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#How-historical-loading-joins-the-live-path-safely)

Use a read-only historical inventory with independent scheduling and checkpoints, feeding the same mapping and projection machinery as incremental work. Historical accepted orders populate approved links and projections; they do not generate new create-order commands.

Establish the provider-supported snapshot or query boundary before scanning. Where supported, start durable change capture first and retain an overlap covering concurrent changes. Deduplicate observations using scoped entity identity and source revision, and guard application so an older backfill observation cannot replace newer projected state.

If suitable snapshot or ordering guarantees are unavailable, use bounded overlapping scans followed by source comparison. Describe this as convergence work, without claiming a point-in-time snapshot.

Review a memo that skips these feasibility checks, then repair its recommendation.

Harborline Architecture Memo Review

Your task

You are reviewing Harborline’s connection proposal before deployment approval. The agreed contract requests an approved NetSuite order from Salesforce and returns NetSuite-owned facts as read-only Salesforce projections. Assess whether the proposed connections actually support that contract.

Tap any claim to classify it, and click on References to verify authorities.

TOHarborline deployment reviewersFROMIntegration design teamDATEOctober 26, 2026SUBJECTReadiness of the Salesforce-to-NetSuite workflow

Background

The approved handoff requests a NetSuite order. Fulfillment and financial facts return as read-only Salesforce projections.

Analysis

Every Salesforce object emits replayable events, so the approval feed is guaranteed.

One OAuth 2.0 setup authenticates all Salesforce and NetSuite endpoints. We will create NetSuite orders through SOAP with our REST M2M token. Oracle’s OAuth setup instructions establish compatibility for this connection.

Moving historical loading to a RESTlet doubles capacity. The token test passed, so the workflow is deployable.

Conclusion

Deployment approval must establish that the selected connections can carry the agreed handoff and read-only projections.

Recommendation

Provide a replacement deployment recommendation stating the selected paths, outstanding evidence, freshness commitment, and historical-loading controls.

Do you find this helpful?

The repaired design has one shared NetSuite budget and endpoint-specific credentials. It also names what the source can actually expose. Passing a token test cannot repair absent event coverage, and changing adapters cannot prevent backfill from starving live work without scheduling controls.

## What proves the OPP-410 topology works[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-proves-the-OPP-410-topology-works)

Trace one handoff through observable boundaries:

1. **Request acceptance:** Intake receives the approved OPP-410 handoff.
2. **Durable responsibility:** The integration commits recoverable intent, approved references, source revision, and operation identity. Capture progress advances only after recoverable storage.
3. **Business completion:** The selected NetSuite operation is verified to have accepted SO-920. Record the confirmed destination reference and result before advancing order-application progress.
4. **User-visible success:** Write and verify Salesforce’s projection of the accepted order. Track projection application separately from order submission.

Retries retain the operation identity and receive new attempt identities. The trace must distinguish queued intent, confirmed NetSuite acceptance, and verified Salesforce display.

Collect deployment evidence in the intended environment:

- Test representative record operations and least-privilege permissions.
- Exercise restart recovery and a replay gap.
- Check live-plus-backfill load against the shared budget.
- Verify separate projections for six shipped, two returned, and zero remaining on INV-301.

Close the interview recommendation with conditional Salesforce notifications and authoritative REST reads, verified NetSuite REST submission, scheduled NetSuite projection reads, and restricted Salesforce REST writes.

Name the operational costs: durable processing state, polling traffic, credential maintenance, and historical reconciliation. State the polling fallback and outstanding operation, permission, latency, and recovery evidence.

Now make those decisions for a different Harborline configuration. Write and commit an original response covering all five sections before selecting any comparison option. Keep that original separately, then use the revealed criteria to prepare a revision.

Harborline Independent Design

Design an independent Harborline Salesforce–NetSuite handoff: approval lives on a custom Salesforce handoff object whose event coverage is unverified; supported incremental Salesforce REST reads allow 60 requests/minute and up to 100 relevant changes/request, with 30 changes arriving per minute, a five-minute visibility target, confirmed suitable incremental filtering, and no snapshot guarantee. NetSuite REST supports the required record operations; one shared integration slot is available with measured mean occupancy of one second, live work consumes 40 NetSuite calls/minute, 3,000 historical records require two NetSuite calls each, and the proposed configuration pairs NetSuite SOAP with OAuth 2.0 M2M in a just-refreshed sandbox. Start with the five empty sections: write and commit your complete original response before selecting any comparison option, retain that original separately, then use the revealed criteria to prepare a revision.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

Harborline Topology and Interface Decision Record

1. Topology and interface decision recordConfigurable

2. Polling schedule and quota headroom

3. Authentication correction and environment checklistConfigurable

4. Historical capacity and recovery boundary

5. Exactly three verification gatesConfigurable

Do you find this helpful?

An implementable recommendation exposes what must be verified before deployment while still choosing a workable path. Once a create request times out after submission, the next question becomes sharper: How can Harborline establish whether the order exists before another attempt risks a duplicate?

Decomposing the Problem: Order-to-Cash Sync

FDE Interview Questions: Order-to-Cash Sync

Ask

[What evidence makes OPP-410’s connections implementable](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-evidence-makes-OPP-410s-connections-implementable)

[The paths that carry new handoffs and SO-920’s status](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#The-paths-that-carry-new-handoffs-and-SO-920s-status)

[Which credentials belong on each arrow](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Which-credentials-belong-on-each-arrow)

[Sharing capacity between live work and 6,000 historical records](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#Sharing-capacity-between-live-work-and-6000-historical-records)

[How historical loading joins the live path safely](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#How-historical-loading-joins-the-live-path-safely)

[What proves the OPP-410 topology works](https://www.educative.io/courses/forward-deployed-engineer/system-design-order-to-cash-sync#What-proves-the-OPP-410-topology-works)