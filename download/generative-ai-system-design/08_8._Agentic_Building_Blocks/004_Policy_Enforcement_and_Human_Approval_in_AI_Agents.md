# Policy_Enforcement_and_Human_Approval_in_AI_Agents

Source: https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Policy Enforcement and Human Approval

Explore how AI agents safely execute actions by separating planning from execution through a deterministic policy enforcement layer. Understand the classification of actions by risk, the role of human approval workflows, and the importance of audit trails and override controls to build secure, reliable agentic systems.

We'll cover the following...

- [Why agents need an authorization layer](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Why-agents-need-an-authorization-layer)
- [Policy enforcement architecture](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Policy-enforcement-architecture)
  - [Inputs and verdicts](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Inputs-and-verdicts)
  - [Deployment and failure handling](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Deployment-and-failure-handling)
- [Classifying actions by risk](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Classifying-actions-by-risk)
- [Human approval service design](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Human-approval-service-design)
  - [Queueing and reviewer routing](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Queueing-and-reviewer-routing)
  - [Binding and safe continuation](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Binding-and-safe-continuation)
- [Escape hatches and accountability](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Escape-hatches-and-accountability)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Conclusion)

A support agent correctly identifies a $5,000 refund, but that does not mean it should be allowed to execute it. The model can propose an action, but it cannot grant itself permission to perform it. Production systems therefore place a deterministic policy layer between the agent and side-effecting tools. This layer evaluates identity, permissions, risk, and current state, then decides whether to allow, deny, or require human approval.

This lesson focuses on designing that control boundary and safely handling actions that require human approval.

## Why agents need an authorization layer[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Why-agents-need-an-authorization-layer)

A production agent usually has three distinct paths in a request life cycle. It interprets user intent, plans tool usage, and then tries to invoke systems that change real state. The danger appears at the boundary between planning and execution. A simple way to think about it is this. The model may act like a sharp intern who drafts the correct form, but only the organization decides whether the form is valid to file right now.

The system therefore inserts a **policy enforcement point** between agent intent and tool execution. A policy enforcement point is a deterministic gate that receives a proposed action and returns an execution verdict without consulting model judgment. This gate becomes the only route to side-effecting APIs.

The gate exists because three classes of failure are common.

- **Prompt injection:** Untrusted content can manipulate the planner into proposing privileged actions.

![Example of prompt injection](images/img_1d8197715a27.svg "Example of prompt injection")

Example of prompt injection

- **Hallucinated authority:** The model can confidently assert permissions that do not exist.
- **Stale context:** The model may reason over an outdated state snapshot while the world has already changed.

Once that separation is in place, approvals and denials become durable control-plane events rather than transient chat behavior. That sets up the next layer, where suspended work must resume safely after delays and failures.

## Policy enforcement architecture[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Policy-enforcement-architecture)

The policy engine sits on the critical path between planner and executor. The planner emits a proposed tool call, but the executor refuses to act unless the request carries a valid verdict produced by policy.

### Inputs and verdicts[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Inputs-and-verdicts)

Policy evaluation is deterministic when the request shape is explicit and stable. In practice, the engine consumes a structured action envelope rather than free-form text.

- **Requester identity:** The envelope includes the authenticated user, the acting service, and any delegated authority chain.
- **Tool and action type:** The request specifies which tool is being called and whether it reads, writes, deletes, or performs an external side effect.
- **Parameters and target resource:** The engine inspects exact arguments, target object identifiers, and resource ownership boundaries.
- **Execution context:** The request includes environment, tenant, state version, monetary amount, expected affected count, and any computed blast radius.
- **Control attributes:** The engine records reversibility and whether the action can be compensated for later.

The engine returns one of three verdicts. It can allow immediate execution, deny the request, or require approval. A common implementation uses ABAC.

### Deployment and failure handling[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Deployment-and-failure-handling)

A centralized policy service gives consistency and simpler rule rollout. An embedded library gives lower latency and fewer network hops. Many systems use both, with local enforcement backed by centrally distributed signed rules.

- **Decision records**: Every verdict should be persisted as an idempotent record keyed by action identity. That matters during retries and network ambiguity.
- **Approval contracts:** If policy requires human review, the system creates an approval contract that binds exact parameters, the target state version, and an expiration time. The executor later verifies that contract before acting. Drifted parameters or changed state force re-evaluation.

**Practical tip:** Execution services should accept only signed policy verdicts, never raw model intent. This keeps a bypass bug in the planner from turning into an execution bug.

The architecture below makes that separation visible before we classify actions by risk.

![Policy gate architecture](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Policy gate architecture")

Policy gate architecture

With the gate defined, the next step is deciding which actions should flow through each verdict path.

## Classifying actions by risk[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Classifying-actions-by-risk)

The policy layer needs a reproducible taxonomy. In plain terms, the system asks three questions before execution. Does this action change anything, can it be undone, and how much of the world does it touch?

Those questions become deterministic fields rather than model opinions. A draft email and a sent email may look similar in the planner, but one is internal and reversible while the other becomes external history.

Use the following action classes as a starting point.

- **Read or no-state-change:** These actions fetch data, search records, or compute summaries without changing persistent state.
- **Reversible internal write:** These actions update internal tickets, create drafts, or perform soft deletes that can be rolled back.
- **Irreversible external or destructive action:** These actions send emails, issue refunds, hard-delete records, or trigger customer-visible changes.

Thresholds then refine the default class. A ticket update affecting one record in staging may auto-execute, while the same tool touching 5,000 records in production should escalate. Common thresholds include record count, dollar amount, external visibility, tenant sensitivity, and environment.

Do not let the model assign its own risk tier. The classifier must be deterministic so that retries, audits, and postmortems reproduce the same decision.

Low-risk actions often auto-execute with logging. Medium-risk actions may require approval only when thresholds are met. High-risk actions usually require explicit approval, and sometimes two reviewers. This reduces approval fatigue without weakening control.

Once actions can be classified consistently, the system needs a durable way to pause and wait for a human.

## Human approval service design[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Human-approval-service-design)

A human approval step should be designed as workflow infrastructure, not a pop-up attached to the chat UI. The request may wait minutes or hours, reviewers may change, and the downstream world may mutate before execution resumes.

The service usually has three moving parts.

### Queueing and reviewer routing[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Queueing-and-reviewer-routing)

An approval request enters a durable queue with a risk tier, domain label, and required reviewer role. Routing then assigns it to finance reviewers, support managers, security approvers, or other domain owners.

Reviewers need enough context to make a bounded decision instead of reconstructing the entire conversation.

- **Exact action details:** The request shows the precise tool name, arguments, target resource, and a preview or diff of the intended change.
- **Requester context:** The reviewer sees who initiated the action, which agent acted, and what delegated credentials were in scope.
- **Supporting evidence:** The request includes the exact source records, relevant excerpts, or proposed diff needed to verify the action, along with links to the original sources and the policy rule that triggered approval.

### Binding and safe continuation[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Binding-and-safe-continuation)

Approvals must be bound to exact parameters, a resource version, and an expiration time. Optimistic concurrency control is a useful execution-time guard here.

- **Timeout behavior:** If no reviewer responds, the workflow should default to a safe outcome such as deny, expire, or escalate to a secondary queue. Silent auto-approval on timeout breaks the whole control model.
- **Failure modes:** The service must reject stale approvals, replayed approval tokens, and approvals against changed downstream state. Throughput matters too. If medium-risk actions flood reviewers, teams rubber-stamp. That is an operational signal to refine thresholds and reduce needless human gates.

**Note:** An approval is not valid forever. If parameters drift or the target resource version changes, the workflow must return to policy evaluation.

The lifecycle below shows where expiration and revalidation fit before execution resumes.

![Approval lifecycle](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Approval lifecycle")

Approval lifecycle

After approval handling is in place, operators still need direct controls for when the whole system becomes risky or degraded.

## Escape hatches and accountability[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Escape-hatches-and-accountability)

Even with good policy and approvals, operators need deterministic override controls outside the model path. When an incident starts, nobody should ask the agent politely to stop.

Typical escape hatches are straightforward.

- **Tool deny lists:** Operators can block specific tools such as refunds or outbound email across the fleet.
- **Environment kill switches:** The platform can freeze all production writes while leaving read-only behavior available.
- **Scoped autonomy downgrades:** A tenant, workflow type, or agent class can be forced from auto-execute into approval-only mode.
- **Emergency freezes:** Bulk or destructive actions can be halted independently of low-risk internal updates.

Kill switches and deny lists must also block queued requests and approved actions that have not yet executed, with the execution service rechecking the active controls immediately before execution. These controls must remain operable during partial outages, so avoid placing them solely inside the agent service.

The second half of accountability is the audit trail. Every action record should capture requester identity, delegated credentials, policy rule version, approval decision, reviewer identity, exact parameters, resource version, model version, timestamps, execution result, and observed side effects. Store the trail with enough immutability for incident response and compliance review.

**Practical tip:** Log both the proposed action and the executed action. The delta between them reveals parameter drift, approval bugs, and executor-side normalization.

Stronger controls add latency and operational cost, but they reduce blast radius when the planner is wrong. That trade-off is normal in production systems.

AI Powered

Saved

1 attempt left

Reset

Containing blast radius during systemic agent degradation

Following an unexpected model checkpoint update by a third-party provider, an ecommerce customer assistant begins misinterpreting return requests and invoking refund transactions for full order amounts without validating return receipts. How do platform operators contain this failure without shutting down customer support chat entirely?

This is your last attempt.

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Conclusion)

Safe agentic systems separate reasoning from authorization. The model proposes actions, while a deterministic policy engine, risk classifier, approval workflow, kill switches, and audit trail decide whether those actions may execute.

Treat these as core control-plane services, not optional guardrails bolted onto prompts. In the next lesson on durable execution and multi-agent coordination, these decisions must survive pauses, retries, crashes, and agent handoffs without losing correctness.

Planning Loops, Termination, and Budgets

Durable Execution and Multi-Agent Coordination

Ask

[Why agents need an authorization layer](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Why-agents-need-an-authorization-layer)

[Policy enforcement architecture](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Policy-enforcement-architecture)

[Inputs and verdicts](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Inputs-and-verdicts)

[Deployment and failure handling](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Deployment-and-failure-handling)

[Classifying actions by risk](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Classifying-actions-by-risk)

[Human approval service design](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Human-approval-service-design)

[Queueing and reviewer routing](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Queueing-and-reviewer-routing)

[Binding and safe continuation](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Binding-and-safe-continuation)

[Escape hatches and accountability](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Escape-hatches-and-accountability)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/policy-enforcement-and-human-approval#Conclusion)