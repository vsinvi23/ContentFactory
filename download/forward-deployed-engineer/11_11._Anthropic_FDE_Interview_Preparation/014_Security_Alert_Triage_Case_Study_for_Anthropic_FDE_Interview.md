# Security_Alert_Triage_Case_Study_for_Anthropic_FDE_Interview

Source: https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Security Alert Triage Case Study and Scoping

Explore how to scope and design a security alert triage system for a managed security provider using Anthropic's Claude model. Understand customer discovery, policy compliance, workload splitting between code and AI, and deployment considerations to prepare for Forward Deployed Engineer interviews.

We'll cover the following...

- [Questions that change the design](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Questions-that-change-the-design)
- [Checking the request against Anthropic's policy](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Checking-the-request-against-Anthropics-policy)
- [Splitting the work between code and Claude](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Splitting-the-work-between-code-and-Claude)
- [Implementing the alert prefilter](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Implementing-the-alert-prefilter)
- [The scoping brief](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#The-scoping-brief)
- [Scoping as the first deliverable](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Scoping-as-the-first-deliverable)

This case study follows a Claude engagement with a managed security provider, presented the way an interviewer might in a technical round or final panel. The domain is security operations, where the data is noisy, a missed attack is expensive, and the customer's logs contain text written by attackers. Those conditions test every part of a candidate's Claude judgment at once.

The first job is scoping. A candidate who jumps straight to an agent design builds for a problem the customer may not have. A candidate who asks the right questions, checks the request against Anthropic's usage policy, and decides what belongs in code ends up with a design that holds up under every later question.

![rolled-up newspaper](014_Security_Alert_Triage_Case_Study_for_Anthropic_FDE_Interview_images/img_e45a1b9179af.png)

**The case study:**

Harborline Security is a managed security provider that monitors the networks of 120 client companies. Its security information and event management (SIEM) system, the platform that collects logs and raises alerts, produces about 4,000 alerts a day. A team of 14 analysts works them across three shifts, and about 85 percent of alerts turn out to be false positives. At night, a real alert waits a median of 40 minutes before an analyst first looks at it.

Harborline wants Claude to triage incoming alerts, gather evidence from the logs, and recommend a response, such as isolating an infected laptop from the network. Two requirements are fixed. An analyst approves every containment action because isolating the wrong host stops a client's business. Client logs never leave Harborline's own AWS account.

## Questions that change the design[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Questions-that-change-the-design)

The brief leaves out the details that decide the architecture. Six questions shape it the most, and each one has a clear reason behind it.

- **What does an alert contain?**

  - The fields in an alert, such as the rule, the host, the user, and the process command line, decide which evidence tools the agent needs.
- **How do analysts work today?**

  - Knowing which alerts tier 1 analysts close and which they pass to tier 2 shows where triage saves the most time.
- **Which actions change anything?**

  - Closing an alert, escalating it, and isolating a host each carry a different risk, and each needs its own control.
- **What does a miss cost?**

  - A missed attack on a client can cost far more than an analyst's wasted ten minutes, so the system should lean toward escalating.
- **Where may the logs go?**

  - The requirement to keep logs in Harborline's AWS account decides how Claude is reached.
- **How fast must triage be?**

  - The 40-minute night wait sets a target, and a triage result in under a minute changes that number.

In the room, the interviewer answers as Harborline would. Two answers matter most here. Analysts want every escalated alert to arrive with its evidence attached, and they accept extra escalations as long as real attacks are never closed automatically.

The answers settle what to build. Before building it, one more check is specific to Claude.

## Checking the request against Anthropic's policy[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Checking-the-request-against-Anthropics-policy)

Security is a dual-use field. The same skills that defend a network can attack one, so Anthropic's generally available models carry conservative cyber safeguards that block most offensive cyber work. Triage of security alerts is one of the defensive tasks these models still perform by default, so Harborline's request fits without special access.

Anthropic's Cyber Verification Program lets verified organizations lift some of those safeguards for specific work. It has three tiers.

- **Defense access:** Defensive work such as security operations, incident response, malware reverse engineering, and vulnerability validation.
- **Red team access:** Adds authorized penetration testing and red teaming, limited to systems the organization is authorized to test.
- **Specialized access:** The fewest blocks, reserved for a small set of verified organizations testing safety-critical systems.

Checking the policy first protects the engagement. If Harborline later asks the agent to write working exploits for a client's red team, the answer depends on its verification tier. A candidate who knows this can scope the first version to triage with confidence.

The deployment path follows from the brief. Claude in Amazon Bedrock runs on AWS infrastructure where Anthropic personnel have no access to the inference systems, which keeps client logs inside the AWS boundary Harborline requires. One detail affects the program above. On Bedrock, the Cyber Verification Program is open only to customers eligible for Enterprise Frontier Safeguards, so any later red-team request needs to be checked early.

With the policy and the platform settled, the remaining question is which work Claude should do at all.

## Splitting the work between code and Claude[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Splitting-the-work-between-code-and-Claude)

Claude is strongest where judgment meets messy evidence. Exact rules are faster, cheaper, and easier to audit in code. The table below shows the split for this engagement.

|  |  |  |
| --- | --- | --- |
| **Task** | **Owner** | **Reason** |
| Merging duplicate alerts | Code | The same rule firing on the same host is an exact match |
| Closing known routine activity | Code | Analysts already confirmed these patterns, and a lookup is enough |
| Reading process trees and login history | Claude | Connecting events across logs needs judgment |
| Writing the verdict and its evidence | Claude | Analysts need a clear explanation they can check quickly |
| Isolating a host | Analyst | Containment stops a client’s business, so a person decides |

The first two rows run before any model call, which saves cost on every alert that never needs judgment.

![Each stage handles only what the stage before it could not](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Each stage handles only what the stage before it could not")

Each stage handles only what the stage before it could not

## Implementing the alert prefilter[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Implementing-the-alert-prefilter)

Suppose the interviewer asks us to cut alert volume before any model call. The prefilter needs two rules. Alerts with the same rule on the same host within 10 minutes merge into the first one, so analysts still see the count. Low- and medium-severity alerts that match an allowlist of confirmed routine activity close automatically. A high-severity alert always reaches Claude, even when its process is on the allowlist, because an attacker can disguise malware with a trusted process name.

To solve this, we write a `prefilter` function in `prefilter.py` that sorts each alert into one of two lists, with a reason for everything it handles.

Python 3.14.0

```
from datetime import datetime, timedelta

DEDUP_WINDOW = timedelta(minutes=10)

# Rule and process pairs that analysts have confirmed as routine activity.

ALLOWLIST = {

("scheduled_task_created", "backup_agent.exe"),

("new_service_installed", "patch_manager.exe"),

}

# One night of alerts from the SIEM, in time order.

ALERTS = [

{"id": "A-101", "time": "2026-10-29 02:14", "rule": "encoded_powershell", "host": "fin-ws-07", "severity": "high", "process": "powershell.exe"},

{"id": "A-102", "time": "2026-10-29 02:16", "rule": "encoded_powershell", "host": "fin-ws-07", "severity": "high", "process": "powershell.exe"},

{"id": "A-103", "time": "2026-10-29 02:19", "rule": "encoded_powershell", "host": "fin-ws-07", "severity": "high", "process": "powershell.exe"},

{"id": "A-104", "time": "2026-10-29 02:20", "rule": "scheduled_task_created", "host": "srv-db-02", "severity": "low", "process": "backup_agent.exe"},

{"id": "A-105", "time": "2026-10-29 02:31", "rule": "failed_login_burst", "host": "vpn-gw-01", "severity": "medium", "process": "sshd"},

{"id": "A-106", "time": "2026-10-29 02:33", "rule": "failed_login_burst", "host": "vpn-gw-01", "severity": "medium", "process": "sshd"},

{"id": "A-107", "time": "2026-10-29 02:45", "rule": "new_service_installed", "host": "srv-app-04", "severity": "low", "process": "patch_manager.exe"},

{"id": "A-108", "time": "2026-10-29 02:52", "rule": "scheduled_task_created", "host": "hr-ws-12", "severity": "medium", "process": "schtasks.exe"},

{"id": "A-109", "time": "2026-10-29 03:05", "rule": "new_service_installed", "host": "srv-app-05", "severity": "high", "process": "patch_manager.exe"},

{"id": "A-110", "time": "2026-10-29 03:10", "rule": "encoded_powershell", "host": "fin-ws-07", "severity": "high", "process": "powershell.exe"},

{"id": "A-111", "time": "2026-10-29 03:12", "rule": "scheduled_task_created", "host": "srv-db-03", "severity": "low", "process": "backup_agent.exe"},

{"id": "A-112", "time": "2026-10-29 03:40", "rule": "impossible_travel", "host": "sales-lt-03", "severity": "medium", "process": "outlook.exe"},

]

def prefilter(alerts):

"""Split alerts into those Claude should triage and those code can handle, with a reason for each."""

to_claude, handled = [], []

first_seen = {}  # (rule, host) -> (time, ID) of the alert that opened the current group

for alert in alerts:

time = datetime.fromisoformat(alert["time"])

key = (alert["rule"], alert["host"])

if key in first_seen and time - first_seen[key][0] <= DEDUP_WINDOW:

handled.append((alert["id"], f"merged into {first_seen[key][1]}, same rule and host"))

continue

if alert["severity"] != "high" and (alert["rule"], alert["process"]) in ALLOWLIST:

handled.append((alert["id"], "closed, routine activity on the allowlist"))

continue

first_seen[key] = (time, alert["id"])

to_claude.append(alert)

return to_claude, handled

if __name__ == "__main__":

to_claude, handled = prefilter(ALERTS)

for alert_id, reason in handled:

print(f"{alert_id}: {reason}")

print(f"\n{len(ALERTS)} alerts in, {len(to_claude)} sent to Claude: {', '.join(a['id'] for a in to_claude)}")
```

⋯

Merging duplicate alerts and closing routine activity before any alert reaches Claude

- **Line 3:** We set the 10-minute window for merging duplicates.
- **Lines 6–9:** We created `ALLOWLIST`, the rule and process pairs analysts have confirmed as routine.
- **Lines 12–25:** We created one night of 12 alerts in time order, including repeats, routine activity, and one high-severity alert from an allowlisted process.
- **Line 31:** We created `first_seen`, which tracks the first alert of each rule and host group, so later duplicates can point back to it.
- **Lines 35–37:** We merged any alert that repeats a group within the window, and recorded which alert it joined.
- **Lines 38–40:** We closed low and medium alerts that match the allowlist. High-severity alerts skip this check.
- **Lines 41–42:** We started a new group and sent the alert on to Claude.
- **Lines 46–51:** We printed a reason for every handled alert and a one-line summary.

Running the prefilter gives the output below:

Ace Editor

1

2

3

4

5

6

7

8

9

A-102: merged into A-101, same rule and host

A-103: merged into A-101, same rule and host

A-104: closed, routine activity on the allowlist

A-106: merged into A-105, same rule and host

A-107: closed, routine activity on the allowlist

A-111: closed, routine activity on the allowlist

12 alerts in, 6 sent to Claude: A-101, A-105, A-108, A-109, A-110, A-112

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Half of the night's alerts never reach a model, and every one of them has a reason an analyst can audit. A-109 reached Claude even though `patch_manager.exe` is on the allowlist because its severity is high. A-110 also went through since it fired almost an hour after A-101 and may be a new event on the same host. On real traffic, the reduction rate comes from a week of Harborline's own alerts, which gives the interviewer a measured number instead of a guess.

## The scoping brief[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#The-scoping-brief)

Scoping ends with a short brief that every later decision points back to. We write it where the interviewer can see it.

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

Customer: Harborline Security, a managed security provider for 120 client companies.

Problem: 4,000 alerts a day, about 85 percent false positives, 40-minute night wait.

Version 1: Code merges duplicates and closes routine activity. Claude triages the rest,

gathers evidence, and recommends a response with its reasoning.

Controls: An analyst approves every containment action. High-severity alerts are never

closed by code or by the model.

Platform: Claude in Amazon Bedrock inside Harborline's AWS account. Triage needs no

special cyber access.

Success: No real attack closed automatically. Night wait under 5 minutes. Fewer alerts

per analyst shift.

Out: Red-team exploit work, pending a Cyber Verification Program review.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The brief names what version 1 does, what it never does, and how success is measured. Each line answers a question the interviewer is likely to ask later.

## Scoping as the first deliverable[#](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Scoping-as-the-first-deliverable)

A security engagement rewards careful scoping more than most. The discovery questions turned a vague request into concrete limits, and the usage-policy check confirmed that the work fits Claude’s default access. The split between code and Claude kept the rules cheap and auditable, and the prefilter showed that the split worked on real alerts. A candidate who scopes this way gives the interviewer a design that is already safe before a single prompt is written.

The Final Panel Solution Design Walk-Through

Building the Agent for the Security Alert Triage Case

Ask

[Questions that change the design](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Questions-that-change-the-design)

[Checking the request against Anthropic's policy](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Checking-the-request-against-Anthropics-policy)

[Splitting the work between code and Claude](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Splitting-the-work-between-code-and-Claude)

[Implementing the alert prefilter](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Implementing-the-alert-prefilter)

[The scoping brief](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#The-scoping-brief)

[Scoping as the first deliverable](https://www.educative.io/courses/forward-deployed-engineer/security-alert-triage-case-study-and-scoping#Scoping-as-the-first-deliverable)