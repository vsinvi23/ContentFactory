# Decomposing_Order-to-Cash_Sync_to_Define_Integration_Contracts

Source: https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Decomposing the Problem: Order-to-Cash Sync

Break down Harborline Software's requirements for synchronising deals, orders, and invoices between Salesforce and NetSuite. Define system-of-record ownership at the record and field levels, establish how corresponding records are matched across systems, and specify the requirements for data mapping contracts. Identify the integration constraints introduced by partial settlement and conflicting write-back updates.

We'll cover the following...

- [What Harborline must agree on before promising a sync](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-Harborline-must-agree-on-before-promising-a-sync)
- [Who can change each part of OPP-410 and SO-920?](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Who-can-change-each-part-of-OPP-410-and-SO-920)
- [Which records represent the same object](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Which-records-represent-the-same-object)
- [What the QL-1 mapping contract must specify](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-the-QL-1-mapping-contract-must-specify)
- [How SO-920 can be settled so far and still unfinished](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#How-SO-920-can-be-settled-so-far-and-still-unfinished)
- [What breaks when Salesforce writes Complete back](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-breaks-when-Salesforce-writes-Complete-back)
- [Practice: Whether SO-1044 is ready for a design discussion](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Practice-Whether-SO-1044-is-ready-for-a-design-discussion)

Salesforce lists Harborline Software's opportunity OPP-410 as Closed Won for ten units, while NetSuite records six units shipped and an invoice with an outstanding balance. Neither system provides a complete view of the order lifecycle. Connecting these records requires an integration contract that defines system-of-record ownership, field-level authority, and record relationships. The contract provides the basis for automating order creation and giving sales access to authoritative fulfilment and receivables data.

## What Harborline must agree on before promising a sync[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-Harborline-must-agree-on-before-promising-a-sync)

Start by identifying who approves orders, which approved customer and item records each order references, and how order statuses are defined across systems.

Common CRM and ERP integration challenges include conflicting data ownership, inconsistent customer models, duplicate contacts, and order statuses that do not fully represent partial shipments or returns. Selecting an integration protocol or transport mechanism does not resolve conflicting business rules or data ownership.

Use the following working assumptions for Harborline, pending client confirmation:

- Each order handoff references one approved bill-to customer and one accepted order.
- Track fulfilment at the order-line level, including shipped and returned quantities for each item.
- Use USD for all monetary amounts in this scenario, excluding taxes and shipping charges.
- An approved, posted credit reduces the outstanding balance of the invoice to which it is applied.
- Salesforce is the system of record for sales proposals and customer relationship data. Finance approves billing identities and financial decisions managed in NetSuite. The fulfilment owner authorises shipment and return-receipt status changes.

These assumptions apply only to the Harborline scenario and must not be treated as standard product behaviour or accounting rules. The first deliverable is an agreed definition of record ownership, business states, and their relationships.

## Who can change each part of OPP-410 and SO-920?[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Who-can-change-each-part-of-OPP-410-and-SO-920)

Consider a simplified mapping rule: "Synchronise all customer fields bidirectionally and copy the latest `order_status` value." This rule does not establish whether sales users can modify legal billing names or whether a Closed Won opportunity authorises order acceptance.

Data can flow bidirectionally while each field and life cycle transition has a clearly defined authoritative writer. The direction of data flow does not determine which system is authorised to modify a value. A **projection** is a local representation of data owned by another system. Exposing that data in a destination does not grant authority to modify the source record.

Use the following ownership matrix as the proposed data ownership contract for Harborline, pending stakeholder approval. Separate system-of-record ownership from the business role responsible for approving changes.

## Harborline’s Proposed Ownership Matrix

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Entity/Field Group** | **Authoritative System** | **Business Approver** | **Permitted Movement** | **Restriction** |
| Customer relationship / contact fields | Salesforce | Sales owner | Salesforce → approved NetSuite relationship fields | Protect approved legal billing identity |
| Approved customer billing identity | NetSuite | Finance; customer-data owner resolves associations | NetSuite → Salesforce, read-only | Sales proposals require approval |
| Opportunity stage / proposed quantities / proposed terms | Salesforce | Sales owner | Salesforce → NetSuite order request | Closed Won is not order acceptance |
| Accepted sales order quantities / prices / acceptance | NetSuite | Finance / order-approval role | NetSuite → Salesforce projection | Later sales edits require review |
| Item identifiers / accounting attributes | NetSuite | Finance / item-master owner | Approved item correspondence → Salesforce | No description-based substitutions |
| Line fulfillment | NetSuite | Fulfillment owner | NetSuite → Salesforce projection | Preserve line quantities and shipments |
| Invoices | NetSuite | Finance | NetSuite → Salesforce projection | No Salesforce financial overwrite |
| Applied payments / invoice balance | NetSuite | Finance | NetSuite → Salesforce projection | Zero balance ≠ whole-order completion |
| Return receipt | NetSuite | Fulfillment owner | NetSuite → Salesforce projection | Return request ≠ receipt |
| Return-credit decisions / posted credits | NetSuite | Finance | NetSuite → Salesforce projection | Receipt alone ≠ credit or refund |

Marking an opportunity as Closed Won triggers an order handoff request. Once Finance approves the handoff, NetSuite records the accepted commercial commitment. After order acceptance, changes to quantity or price in Salesforce must go through an approved change-request workflow rather than directly updating the accepted order in NetSuite.

Customer data ownership is also defined at the field level. Sales can update contact phone numbers, while Finance retains authority over approved legal billing information.

## Which records represent the same object[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Which-records-represent-the-same-object)

A **crosswalk** records approved correspondences using system instance, object type, and stable record identifier. Keep identity correspondences separate from relationships between different business entities.

For OPP-410, record:

- **Customer correspondence:** `sf-prod/Account/ACC-208` maps to `ns-prod/Customer/CUST-730` for the approved bill-to relationship.
- **Item correspondence:** `sf-prod/Product/PROD-17` maps to `ns-prod/Item/ITEM-42`.
- **Handoff relationship:** `sf-prod/Opportunity/OPP-410` generated `ns-prod/SalesOrder/SO-920`. The opportunity and order remain different entities.
- **Line correspondence:** `sf-prod/OpportunityLine/QL-1` maps to `ns-prod/SalesOrderLine/SOL-1`, with both parent references preserved.
- **Operational and financial relationships:** Within `ns-prod`, `ItemFulfillment/FUL-11` and `Invoice/INV-301` reference `SalesOrder/SO-920` and line SOL-1. `Payment/PAY-20` applies to INV-301. `Return/RET-8` references the returned quantity from FUL-11 and SOL-1. `CreditMemo/CM-8` links to RET-8, INV-301, and the relevant line.

These are conceptual object labels. Exact product representations require interface verification.

Salesforce–NetSuite integration patterns include opportunities flowing to sales orders and NetSuite sales orders flowing to Salesforce orders or opportunities. That correspondence is a design choice; it does not make an opportunity and an order the same entity.

Test the distinction between identity evidence and business relationships.

Identity or relationship?

Harborline references

Matching customer email; matching display order numbers across instances

sf-prod/Opportunity/OPP-410 → ns-prod/SalesOrder/SO-920

sf-prod/Account/ACC-208 ↔ ns-prod/Customer/CUST-730

sf-prod/OpportunityLine/QL-1 ↔ ns-prod/SalesOrderLine/SOL-1, with parents

ns-prod/Return/RET-8 → ns-prod/ItemFulfillment/FUL-11 and ns-prod/SalesOrderLine/SOL-1

sf-prod/Product/PROD-17 ↔ ns-prod/Item/ITEM-42

Classification

Distinct-entity relationship: opportunity-to-order handoff

Distinct-entity relationship: return provenance tied to shipment and line

Insufficient identity evidence: neither shared attribute authorizes merging

Identity correspondence: approved item

Identity correspondence: approved bill-to customer

Line-level relationship: proposal line to accepted order line

Match every reference to its classification, then submit before viewing explanations. Preserve system instance, object type, and stable identifier in every mapping. Classify both matching-attribute cases on the final card together.

Do you find this helpful?

A shared email, customer name, display order number, or item description cannot authorize a merge or substitution. If Harborline needs multiple bill-to entities or split orders, replace the one-to-one assumptions with explicit cardinalities and allocation links.

## What the QL-1 mapping contract must specify[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-the-QL-1-mapping-contract-must-specify)

Matching field names is insufficient. Each mapping needs source meaning, authoritative writer, destination meaning, transformation, and unresolved-value behavior. Treat these as conceptual fields rather than guaranteed API names:

- **Quantity and price:** The sales-approved proposal supplies 10 units at USD 100 each to the order request. Finance acceptance determines SO-920’s accepted quantity and price; proposed and accepted values remain distinguishable.
- **Product:** Resolve PROD-17 through the approved ITEM-42 crosswalk. Descriptions are display data, not lookup authority.
- **Billing:** Keep sales-proposed billing information separate from the approved CUST-730 billing identity. A proposal never overwrites that identity automatically.
- **Receivables:** Project NetSuite’s invoice amount, applied payment amount, posted credit amount, and remaining invoice balance into separately labeled Salesforce fields, retaining invoice references and source-update evidence.

An unknown item creates an approval hold owned by the item-master owner. A disputed customer association goes to the customer-data owner, with finance approving billing identity. Neither condition permits a guessed association.

The contract also preserves acknowledgment boundaries: Request acceptance means intake received the handoff; durable responsibility means its intent is recoverably recorded. Business completion of this handoff means NetSuite has accepted the order. User-visible success requires verification that Salesforce displays that confirmed result. Completing the handoff still leaves fulfillment and financial obligations open.

## How SO-920 can be settled so far and still unfinished[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#How-SO-920-can-be-settled-so-far-and-still-unfinished)

Follow the authoritative records, preserving history as later events occur:

1. **Commercial:** Sales closes OPP-410 as Won and the handoff becomes pending. Finance then approves SO-920/SOL-1 for 10 units at USD 100: An accepted value of 10 × 100 = USD 1,000.
2. **Fulfillment:** The fulfillment owner records FUL-11 shipping 6 units against SOL-1. Unfulfilled quantity is 10 − 6 = 4 units, still committed for shipment.
3. **Invoice:** Finance posts INV-301 for those 6 units: 6 × 100 = USD 600. The invoice links to the fulfilled order line.
4. **Payment:** Finance records PAY-20 applying USD 400 to INV-301. Its remaining balance is initially 600 − 400 = USD 200.
5. **Return receipt:** The fulfillment owner records RET-8 receiving 2 of FUL-11’s shipped units back. Retained quantity is 6 − 2 = 4 units. Gross shipped quantity remains 6; the return does not erase the shipment.
6. **Credit:** Finance posts CM-8 for 2 × 100 = USD 200, linked to RET-8 and INV-301. Under the case assumptions, invoice balance becomes 600 − 400 − 200 = USD 0.

The coordinated ledger therefore has four simultaneous dimensions:

- **Commercial:** 10 accepted units, supported by SO-920/SOL-1 and finance approval.
- **Fulfillment:** 6 shipped, 2 received back, 4 retained, and 4 unfulfilled, supported by SOL-1, FUL-11, and RET-8 under fulfillment authority.
- **Invoice/payment:** USD 600 invoiced, USD 400 payment applied, USD 200 credited, and USD 0 remaining on INV-301, supported by finance-owned INV-301, PAY-20, and CM-8.
- **Return/credit:** Receipt and credit are separately evidenced by RET-8 and CM-8. A return request alone proves neither event. A credit records an adjustment; it supplies no evidence of a cash refund.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27967%27%20height=%27501%27/%3e)![Tracking order fulfillment and financial settlement](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Tracking order fulfillment and financial settlement")

Tracking order fulfillment and financial settlement

Keep FUL-11 and INV-301 linked to the later return and credit. Rewriting the shipment as four units would destroy the explanation for the original six-unit invoice.

## What breaks when Salesforce writes Complete back[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-breaks-when-Salesforce-writes-Complete-back)

A Salesforce automation sees INV-301’s zero balance and proposes writing `Paid/Complete` over NetSuite’s partial-fulfillment state. Decide what that write would claim before accepting it.

Authorize Paid/Complete?

1.

Salesforce proposes writing Paid/Complete into NetSuite for SO-920.

Evidence: INV-301 has USD 600 invoiced, USD 400 payment applied, USD 200 posted credit, and USD 0 remaining. SO-920 has 10 accepted units, 6 shipped, 2 received back, and 4 unfulfilled units still committed.

Which action is supported?

A.

Resolve the conflict by making NetSuite authoritative for every Salesforce field.

B.

Authorize the write if Salesforce’s timestamp is newer than NetSuite’s.

C.

Reject the completion write; display separate finance-owned invoice settlement and fulfillment-owned open quantity projections in Salesforce.

D.

Authorize the write because INV-301 has zero balance.

---

1 / 1

The automation’s evidence is invoice-scoped, but its proposed write is order-scoped. That scope mismatch is the defect: a correct balance calculation cannot authorize a broader lifecycle transition. Closed Won supplies sales intent, not the missing shipment, invoicing, or payment evidence.

Repair the ownership and status model. Salesforce receives read-only financial and fulfillment projections from NetSuite, each traceable to supporting records. Sales relationship edits remain sales-owned; approved billing identity remains finance-owned.

Reject last-write-wins and global source-of-truth rules for the same reason.

## Practice: Whether SO-1044 is ready for a design discussion[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Practice-Whether-SO-1044-is-ready-for-a-design-discussion)

A reviewable decomposition has scoped identifiers for every entity, an authoritative writer for each mapped field, a business approver for each transition, and supporting records for every displayed status. Quantities and balances must reconcile independently.

Apply that standard to a second Harborline order. Its Salesforce display currently says Complete, but the evidence includes an outstanding invoice balance and committed unshipped units. Produce an ownership matrix, identity crosswalk, and current-state ledger from an empty response before opening the worked answer.

SO-1044 Business Contract

Harborline Software needs a reviewable contract for SO-1044 before discussing integration design; its organization size is not specified. Independently draft the three empty sections and commit your response before selecting any worked answer, then compare the evidence-based criteria and revise your draft.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

SO-1044 Ownership, Identity, and Lifecycle Contract

1. Case Evidence

Approved correspondences: sf-prod/Account/ACC-509 maps to ns-prod/Customer/CUST-811; sf-prod/Product/PROD-17 maps to ns-prod/Item/ITEM-42; sf-prod/OpportunityLine/QL-9 maps to ns-prod/SalesOrderLine/SOL-9. Handoff: sf-prod/Opportunity/OPP-612 generated accepted ns-prod/SalesOrder/SO-1044. Five units were accepted at USD 200 each. ns-prod/ItemFulfillment/FUL-44 shipped three; ns-prod/Invoice/INV-88 invoices those three for USD 600; ns-prod/Payment/PAY-88 applied USD 200 to that invoice. ns-prod/Return/RET-44 records one received return from FUL-44. Finance posted linked ns-prod/CreditMemo/CM-44 for USD 200 against INV-88. No refund was issued. Two unshipped units remain committed. Salesforce currently displays Complete.

2. Scope and Instructions

Retain one approved bill-to and one accepted order per handoff, fulfillment-tracked items, USD, no tax or shipping charges, and a posted credit reducing its linked invoice balance. Start with the three empty sections below. Write a compact ownership matrix, scoped identity crosswalk, and current-state ledger covering customers, opportunities, orders, items, invoices, payments, fulfillment, returns, and separate credits. Identify authoritative records and business approvers, permitted directions of movement, and whether Complete is supported. Commit all three drafts before selecting Worked answer. Then review each section against its criteria and revise your original response, explicitly correcting unsupported completion, credit/refund conflation, missing entities, or unsafe overwrite authority. Do not specify endpoints, events, authentication, or recovery machinery.

3. Ownership MatrixConfigurable

4. Scoped Identity CrosswalkConfigurable

5. Current-State Lifecycle LedgerConfigurable

Do you find this helpful?

A useful business contract can explain both the remaining commitment and the financial position without choosing a transport. With those meanings agreed, the next design question becomes concrete: Which available interfaces can carry these approved transitions and projections?

FDE Interview Questions: The Health Data Hub

System Design: Order-to-Cash Sync

Ask

[What Harborline must agree on before promising a sync](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-Harborline-must-agree-on-before-promising-a-sync)

[Who can change each part of OPP-410 and SO-920?](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Who-can-change-each-part-of-OPP-410-and-SO-920)

[Which records represent the same object](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Which-records-represent-the-same-object)

[What the QL-1 mapping contract must specify](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-the-QL-1-mapping-contract-must-specify)

[How SO-920 can be settled so far and still unfinished](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#How-SO-920-can-be-settled-so-far-and-still-unfinished)

[What breaks when Salesforce writes Complete back](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#What-breaks-when-Salesforce-writes-Complete-back)

[Practice: Whether SO-1044 is ready for a design discussion](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-order-to-cash-sync#Practice-Whether-SO-1044-is-ready-for-a-design-discussion)