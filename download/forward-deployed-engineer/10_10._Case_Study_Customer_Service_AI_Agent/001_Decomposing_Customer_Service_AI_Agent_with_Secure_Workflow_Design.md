# Decomposing_Customer_Service_AI_Agent_with_Secure_Workflow_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Decomposing the Problem: Customer Service AI Agent

Break down LumenPay's requirements for an AI assistant that handles customer enquiries about payments and refunds. Define the initial scope, identify the authoritative data sources for each response, and determine what information can be disclosed to customers. Identify the design constraints imposed by customer identity verification, PCI DSS requirements, and human oversight of refund decisions.

We'll cover the following...

- [What LumenPay’s first version should resolve](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-LumenPays-first-version-should-resolve)
- [Which systems can establish each answer?](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Which-systems-can-establish-each-answer)
- [Why a login and a payment ID are not enough](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-a-login-and-a-payment-ID-are-not-enough)
- [What the P-730 answer may reveal](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-P-730-answer-may-reveal)
- [Why “No Card Details” doesn’t exclude PCI scope](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-No-Card-Details-doesnt-exclude-PCI-scope)
- [What the human owns for P-730’s refund request](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-human-owns-for-P-730s-refund-request)
- [Practice: Defending scope changes](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Practice-Defending-scope-changes)

LumenPay's support team aims to reduce repetitive payment-status enquiries, operations wants to improve refund request routing, and security requires that card details are never collected through chat. Define the assistant's scope and responsibilities before selecting its architecture. The initial version must define which customer enquiries it can handle, the verified information required for each response, and the teams responsible for unresolved requests.

## What LumenPay’s first version should resolve[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-LumenPays-first-version-should-resolve)

Assume the assistant serves authenticated merchant users, not individual cardholders. Treat the following as proposed discovery decisions, not existing system capabilities.

The CLIENT framework covers Context, Landscape, Integration points, End-to-end design, Non-happy paths, and Trade-offs. Use the CLIENT framework from Chapter 1 to define the workflow, scope, and authorisation requirements before selecting the agent architecture or its components.

Distinguish four types of customer requests:

- **General policy questions:** Answer questions using published, approved support policies.
- **Merchant-specific status questions:** Retrieve payment status information only after verifying the user's current authorisation to access the relevant merchant records.
- **Refund-request intake:** Explain the refund process and route requests containing only the required information to an authorised staff member.
- **Financial execution:** Approve or process refunds and modify payout destinations.

Limit version one to policy questions, authorised payment-status enquiries, and refund-request intake. Exclude financial execution and collection of payment card details. Payment-status assistance provides a clearly defined read-only workflow, while refund intake routes requests without transferring financial decision-making authority to the assistant.

Establish baseline metrics and target outcomes for correctly resolved eligible payment-status enquiries and refund requests successfully routed to the appropriate team. Do not use conversation closure alone as a success metric. It cannot distinguish accurate resolutions from incorrect responses or unresolved requests.

## Which systems can establish each answer?[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Which-systems-can-establish-each-answer)

LumenPay’s stated landscape separates identity, access, payment facts, policy, and support handling. Match each fact to its authority before deciding what the agent may promise.

Match Facts to Their Authority

Requested fact or evidence

Current merchant membership and role

Signed-in user identity

Case assignment and handling history

Published support policy

Payment status, amount, currency, and merchant association

Follow-up: A case note says “payment settled.” What does this establish?

Authority or meaning

Identity service

Approved policy repository

Payment service

Merchant-access directory

Support case system

Handling history, not authoritative current payment status

Match each fact to its authoritative system. Then match the “settled” case note to what it establishes. Submit to check your matches; revise any mismatches.

Do you find this helpful?

Each authoritative system serves a different purpose, and evidence from one cannot replace evidence required from another. Successful connectivity to these systems does not authorise disclosure. The assistant must verify the relevant payment facts and access permissions before returning customer-specific information.

A case note stating "payment settled" reflects a recorded claim, not verified payment status. Confirm the current state through the authoritative payment service. Creating a support case establishes a tracking record and assigned responsibility, not confirmation that a refund has been processed.

For each workflow, document the caller, request type, authoritative data source, required authorisation evidence, permitted response, exclusions, and responsible human owner.

For version one:

- **Policy explanation:** An authenticated merchant user asks about payment or refund procedures. Retrieve applicable guidance from the approved policy repository, respecting publication status and access restrictions. Do not promise approval for individual requests. Escalate missing or conflicting policy guidance to the support-policy owner.
- **Payment status:** An authenticated merchant user requests a payment update. Verify the user's identity, current merchant permissions, and the payment's association with that merchant before retrieving and returning permitted status fields. Do not expose unrelated payment records or perform financial transactions. Support operations handles unresolved status enquiries, while the identity and access team resolves merchant membership disputes.
- **Refund intake:** An authenticated merchant user requests a refund review for a payment they are authorised to access. Use approved refund policies and verified payment details to create a case. Return the case reference and confirmed next steps once the case system records the request. Do not determine refund eligibility or execute refunds. Support operations handles initial triage, while authorised payments operations reviews financial decisions.

Confirm API availability, required permissions, and policy currency during discovery. An existing system does not guarantee that the integration has a supported interface or the permissions required to use it.

## Why a login and a payment ID are not enough[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-a-login-and-a-payment-ID-are-not-enough)

Assume U-17 has the viewer role for merchant M-41, and LumenPay authorises that role to retrieve a defined set of payment status fields. The payment service confirms that P-730 belongs to merchant M-41, has an amount of USD 84.20, and has status `settled`. Payment P-731 belongs to merchant M-88.

Apply the authentication and authorisation principles from Chapter 1. A payment reference entered in chat identifies a record to look up but does not grant access. Before disclosing payment details, verify the caller's current merchant permissions and confirm that the payment belongs to that merchant.

For P-730, verify three conditions:

1. The identity service confirms that the authenticated caller is U-17.
2. The access directory confirms U-17's current membership in M-41 and permission to view the approved payment status fields.
3. The payment service confirms that P-730 is associated with merchant M-41.

Once all three checks pass, return only the payment status fields authorised for the viewer role.

Compare the authorised P-730 lookup with two cases: U-17 requests P-731, which belongs to another merchant, and a request where current merchant membership cannot be verified. For each scenario, decide whether to return the permitted fields, deny disclosure, or hold the request pending verification.

Three payment lookup decisions

1.

Choose one disposition for each of the three cases before submitting for feedback.

U-17 is authenticated. Current checks confirm M-41 membership, a viewer role permitted to read status, and P-730’s association with M-41. What should the assistant disclose?

A.

Return the full payment object because all authorization checks succeeded.

B.

Confirm only that P-730 exists; viewer access cannot support status disclosure.

C.

Withhold all payment facts and route to approved verification despite the successful checks.

D.

Return only payment reference, amount, currency, status, and source observation time.

---

1 / 3

P-731 fails the merchant-association check, so withhold its details and avoid confirming its existence. A safe response is: “I can’t provide payment details for that reference through your current access. Please use the approved verification process.” Email resemblance, a receipt, urgency, and possession of the reference do not establish the required association.

If membership or payment association cannot be verified, withhold payment facts and route to approved verification. A broadly privileged connector must not turn U-17’s viewer access into cross-merchant access.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27763%27%20height=%27507%27/%3e)![Controlling data visibility and sensitive propagation](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Controlling data visibility and sensitive propagation")

Controlling data visibility and sensitive propagation

The two lanes require independent decisions: permission to disclose payment facts does not establish permission to receive card data. Denying an unauthorized lookup likewise does not resolve any PAN already received by chat.

## What the P-730 answer may reveal[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-P-730-answer-may-reveal)

Define the approved status fields as payment reference, amount, currency, status, and source observation time. After successful checks, the answer can say:

Payment P-730: USD 84.20, settled. Source observation time: 14:05 UTC.

Here, 14:05 UTC is the assumed time of the payment-service observation. “Settled” carries LumenPay’s documented payment-service meaning; it makes no promise about every downstream bank balance or refund eligibility.

Exclude full card numbers, security codes, unrelated customer information, and internal risk notes. Even masked card fields need a demonstrated workflow need and an approved exposure policy before inclusion.

If the authoritative status is unavailable, say that the current status remains unresolved and assign support operations to investigate. Substituting an old case note would turn handling history into an unsupported financial claim.

## Why “No Card Details” doesn’t exclude PCI scope[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-No-Card-Details-doesnt-exclude-PCI-scope)

Now U-17 sends `[PAN supplied]`. **PAN** means primary account number. This creates a separate data-receipt question even though P-730’s status lookup was authorized.

PCI SSC FAQ 1310 says PCI DSS does not prohibit requesting or receiving cardholder data through end-user messaging technologies. If the technology sends or receives PAN, however, the channel must meet all applicable PCI DSS requirements, and related supporting systems are in scope. The condition concerns actual transmission or receipt, not whether the product is called a support chatbot.

FAQ 1157 says cardholder data received through an unintended channel should either be immediately removed or be secured according to PCI DSS and incorporated into the cardholder data environment. It also calls for preventing further capture and responding without further propagating the data. Customer warnings alone do not establish exclusion from scope.

Trace potential copies before claiming containment:

- Chat intake receives the original message.
- Transcript storage may retain it.
- Model requests may transmit it onward.
- Support tickets may copy the transcript.
- Telemetry and exports may create additional copies.

For this case, require no requested card entry, an approved secure payment channel for legitimate collection, preventive controls before further propagation, and an owned accidental-receipt process. Security and payment-compliance owners must assess affected systems and removal or securing obligations. Excluding card entry from supported workflows is a scope decision, not proof that deployed chat and supporting systems are outside PCI DSS scope.

Consider a tempting proposal:

- Any logged-in merchant can paste a payment ID and receive the complete payment object.
- The merchant can request an automatic refund.
- Chat is outside PCI because a notice prohibits card details and answers mask numbers.

Applied here, this proposal fails in four ways:

- It discloses M-88’s P-731 to U-17.
- It exposes excessive fields.
- It permits an unsupported financial action.
- It can leave PAN in upstream copies despite a clean displayed answer.

Repair the scope and ownership commitments before designing implementation controls.

## What the human owns for P-730’s refund request[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-human-owns-for-P-730s-refund-request)

U-17 next asks to refund P-730. Viewer access supports the approved status read; it grants no refund-execution authority. Version one may explain the published process and create a minimally necessary request for authorized review.

Assign distinct responsibilities:

- Support operations: Triage, assignment, customer communication, and the next update commitment.
- Authorized payments operations: Refund eligibility and approval under LumenPay policy.
- Identity/access owner: Membership and role disputes through approved verification.
- Security/payment-compliance owner: Unintended card receipt and affected copies.

A useful handoff identifies the request, safely shareable verified context, unresolved decision, assigned owner, and next update commitment. Do not forward a PAN-containing transcript as routine context.

As in the previous lesson, distinguish acceptance, durable responsibility, business completion, and user-visible success. Here, creating a refund case establishes neither refund approval nor execution nor completion; tell the customer only what the verified case state supports.

For example, once assignment is confirmed: “Your refund request is recorded for payments-operations review; support will update you by 16:00 UTC.” That statement establishes neither approval nor execution nor completion. Human staff must use their approved permissions and verification process; escalation does not waive customer authorization.

## Practice: Defending scope changes[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Practice-Defending-scope-changes)

Use a fresh LumenPay case. U-28 currently has read-only access to M-52. P-910 belongs to M-52 and is USD 126.50 with status pending; P-911 belongs to M-77. U-28 asks for both statuses, requests a refund of P-910, and supplies `[PAN supplied]`.

The five candidate authority systems are available, but API access is unverified. Transcripts currently flow into support tickets and diagnostic logs. Write a concise discovery-and-scope recommendation before viewing comparison criteria.

Defend the First-Version Scope

LumenPay wants fewer repetitive payment-status contacts, better refund routing, and no card collection in chat. U-28 currently has read-only access to M-52; P-910 belongs to M-52 and is USD 126.50, pending, while P-911 belongs to M-77. U-28 asks for both statuses, requests a P-910 refund, and supplies '[PAN supplied]'; candidate authorities are the identity service, current merchant-access directory, payment service, approved policy repository, and support case system, but API access is unverified and transcripts copy to tickets and diagnostic logs.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

U-28 Discovery-and-Scope Recommendation

1. Original Recommendation

2. Commit OriginalConfigurable

3. Compare After CommitmentConfigurable

4. Separate Revision

5. Revision RecordConfigurable

Do you find this helpful?

The scope is ready to inform architecture when each permitted workflow has required evidence, bounded output, and an accountable fallback. The next design question is how retrieval, live tools, and workflow controls enforce those commitments even when customer text or model output asks for something broader.

FDE Interview Questions: Order-to-Cash Sync

System Design: Customer Service AI Agent

Ask

[What LumenPay’s first version should resolve](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-LumenPays-first-version-should-resolve)

[Which systems can establish each answer?](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Which-systems-can-establish-each-answer)

[Why a login and a payment ID are not enough](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-a-login-and-a-payment-ID-are-not-enough)

[What the P-730 answer may reveal](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-P-730-answer-may-reveal)

[Why “No Card Details” doesn’t exclude PCI scope](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Why-No-Card-Details-doesnt-exclude-PCI-scope)

[What the human owns for P-730’s refund request](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#What-the-human-owns-for-P-730s-refund-request)

[Practice: Defending scope changes](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-customer-service-ai-agent#Practice-Defending-scope-changes)