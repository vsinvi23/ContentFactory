# Security_Alert_Triage_Case_Interview_Questions_for_Anthropic_FDE

Source: https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Interview Questions on the Security Alert Triage Case

Explore how to answer security alert triage case interview questions in Anthropic's Forward Deployed Engineer process. Learn to validate agent performance with metrics, handle design changes, manage failures, and address security policy challenges to confidently defend your system design during interviews.

We'll cover the following...

- [Proving the agent works](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Proving-the-agent-works)
- [Technical follow-up questions](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Technical-follow-up-questions)
  - [Cost at full alert volume](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Cost-at-full-alert-volume)
  - [The SIEM goes down](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#The-SIEM-goes-down)
  - [An alert Claude cannot classify](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#An-alert-Claude-cannot-classify)
  - [Why there is no sub-agent](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Why-there-is-no-sub-agent)
- [Handling a requirement change](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Handling-a-requirement-change)
- [Answering the exploit code request](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Answering-the-exploit-code-request)
- [Defending the case under questioning](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Defending-the-case-under-questioning)

The triage agent now gathers evidence, returns a structured verdict, and routes every risky action through code. Analysts approve isolation, high-severity alerts never close on the model’s word, and log text stays in its place as evidence. Once a candidate presents that design, the interviewer starts testing it.

The questions come in three kinds. The first asks for proof that the agent works. The second probes cost and failure, then changes a requirement to see how the design bends. The last tests values, with a request that sits on the edge of what Anthropic allows. Each section below takes one question and gives an answer a candidate can say out loud.

## Proving the agent works[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Proving-the-agent-works)

The first question is usually the most direct one. “How do you know this works?” A strong answer names the metrics that matter and then measures them. Two metrics fit a triage agent.

**Recall** is the share of real attacks that the agent sends to a person by escalating them or requesting isolation. **Precision** is the share of escalated alerts that turn out to be real attacks. For Harborline, a missed attack costs far more than an extra escalation, so recall matters most. Precision shows how much analyst time the escalations cost.

Suppose the interviewer asks us to measure both on a small labeled set. We already built the triage agent for this case in `triage_agent.py`, with its evidence tools, its structured verdict, and the `route` function that decides what happens next. Now we test that agent without changing it. For this, we create a new file, `eval_triage.py`, which adds four alerts from past nights to the agent’s data, runs all eight alerts through `triage` and `route`, and compares each result with the label analysts gave the case.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Files

eval\_triage.py

triage\_agent.py

eval\_triage.py

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

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

from triage\_agent import ALERTS, LOGINS, PROCESS\_TREES, route, triage

# Four more alerts from past nights, with the evidence the SIEM held for them.

ALERTS.update({

"A-120": {"rule": "encoded\_powershell", "host": "it-ws-05", "user": "svc\_sccm", "severity": "high"},

"A-121": {"rule": "impossible\_travel", "host": "sales-lt-03", "user": "d.moreau", "severity": "medium"},

"A-122": {"rule": "failed\_login\_burst", "host": "srv-file-01", "user": "svc\_backup", "severity": "medium"},

"A-123": {"rule": "scheduled\_task\_created", "host": "hr-ws-12", "user": "a.novak", "severity": "medium"},

})

PROCESS\_TREES.update({

"it-ws-05": ["ccmexec.exe (signed, Microsoft) -> powershell.exe -enc (signed company inventory script) -> connects to sccm.harborline.internal"],

"sales-lt-03": ["outlook.exe (no unusual child processes)"],

"srv-file-01": ["backup\_agent.exe (signed) retrying every 60 seconds with an expired password"],

"hr-ws-12": ["chrome.exe -> download invoice\_viewer.dll to AppData/Local/Temp -> schtasks.exe creates task running rundll32.exe invoice\_viewer.dll every 10 minutes"],

})

LOGINS.update({

"svc\_sccm": ["service account, logins only from sccm.harborline.internal"],

"d.moreau": ["02:40 London office VPN success with MFA", "03:10 session token reused from Lagos, no MFA prompt"],

"svc\_backup": ["password expired yesterday, 40 failed logins from srv-file-01 overnight"],

"a.novak": ["02:48 hr-ws-12 success, usual office IP"],

})

# The right answer for each alert, from the analysts who closed the case.

LABELS = {"A-101": "attack", "A-105": "benign", "A-109": "attack", "A-113": "attack",

"A-120": "benign", "A-121": "attack", "A-122": "benign", "A-123": "attack"}

if \_\_name\_\_ == "\_\_main\_\_":

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Saved

Did you find this helpful?

Measuring recall and precision of the triage agent on eight labeled alerts

- **Line 1:** We imported the agent’s data stores and its `triage` and `route` functions from `triage_agent.py`, the agent built for this case.
- **Lines 4–21:** We added four alerts from past nights and the evidence the SIEM held for each one.
- **Lines 24–25:** We recorded the label analysts gave each alert after closing the case.
- **Lines 31–33:** We triaged each alert, routed the result, and counted it as flagged when it was escalated or sent for isolation.
- **Lines 34–36:** We counted flagged alerts, attacks that were caught, and attacks that were closed.
- **Line 37:** We printed Claude’s recommended action next to the action code actually took.
- **Lines 39–44:** We printed recall, precision, and the number of attacks closed automatically.

Below is the output from one run:

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

13

A-101 attack Claude: request\_isolation routed: request\_isolation

A-105 benign Claude: close routed: close

A-109 attack Claude: request\_isolation routed: request\_isolation

A-113 attack Claude: request\_isolation routed: request\_isolation

A-120 benign Claude: close routed: escalate

A-121 attack Claude: escalate routed: escalate

A-122 benign Claude: close routed: close

A-123 attack Claude: request\_isolation routed: request\_isolation

Real attacks caught: 5/5 (recall 100%)

Escalations that were real: 5/6 (precision 83%)

Attacks closed automatically: 0

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Every real attack reached a person, and no attack was closed automatically. The one false escalation is A-120, and its row explains why. Claude read the evidence correctly and recommended closing a signed inventory script run by IT. The severity rule in `route` overrode it because A-120 is a high-severity alert. That trade-off is deliberate. The rule costs some precision in exchange for a guarantee that a fooled model can never close a high-severity alert.

In the room, we add one sentence of honesty. Eight alerts prove the pipeline runs and the metrics compute. A launch decision needs a few hundred labeled alerts from Harborline’s own history, rerun after every prompt or model change. With the eval answered, the interviewer moves to cost and failure.

## Technical follow-up questions[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Technical-follow-up-questions)

Each follow-up targets one weak point in the design. The strongest answers point to a specific part of the code or a measured number.

### Cost at full alert volume[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Cost-at-full-alert-volume)

The interviewer asks what the agent costs at 4,000 alerts a day.

In testing, each alert used about 2,100 input tokens and 230 output tokens across its tool calls. On Claude Sonnet 5.5 through a Bedrock regional endpoint, that comes to roughly 0.7 cents an alert. The prefilter sent half of a sample night to Claude, so about 2,000 alerts a day cost around 14 dollars. Caching the system prompt and tool definitions brings that lower. The comparison that matters is analyst time saved on every alert Claude closes with evidence.

The answer works because every number comes from a measurement or a stated assumption.

### The SIEM goes down[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#The-SIEM-goes-down)

The interviewer asks what happens when the evidence tools stop answering.

Triage fails closed. Without evidence, Claude can’t support a “close,” so any alert whose triage errors out or times out goes straight to the analyst queue as a raw alert. Analysts lose the time savings during the outage, and they never lose an alert.

### An alert Claude cannot classify[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#An-alert-Claude-cannot-classify)

The interviewer asks about a new rule the agent has never seen.

The prompt tells Claude to escalate when unsure, and the schema gives it a `suspicious` verdict for exactly that case. We track the share of suspicious verdicts per rule. A rising share tells us a rule needs better evidence tools or an analyst-written note in the prompt.

### Why there is no sub-agent[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Why-there-is-no-sub-agent)

The interviewer asks why evidence gathering doesn’t run in a separate sub-agent.

Each alert needs two small lookups, so the context stays short, and a sub-agent would only add tokens and latency. I would add one when evidence gets large, such as reading memory dumps or full packet captures, where isolating that noise keeps the main triage focused.

Questions like these test the current design. The next kind of question changes it.

## Handling a requirement change[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Handling-a-requirement-change)

The interviewer plays Harborline’s operations lead and asks for a change. “Nights are short-staffed. Let the agent isolate hosts automatically after 10 p.m.” This tests whether a candidate protects the system’s guarantees under business pressure. A flat yes breaks the approval rule. A flat no ignores a real staffing problem.

A strong answer agrees to the goal and earns the change with evidence.

I understand the pressure, and I’d start by measuring it. For three months, we log every isolation Claude recommends at night and compare it with what the analyst decided. If agreement is very high for a specific pattern, such as a phishing macro on a workstation, we can automate that pattern only. It would cover workstations and never servers, use a reversible network quarantine, page the on-call analyst immediately, and run only for clients who opt in. Everything else stays in the queue.

The answer turns a broad request into a narrow, measured one. Each condition, from workstations only to an immediate page, maps to a specific risk in the original brief.

The last question in this round leaves engineering behind and tests values.

## Answering the exploit code request[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Answering-the-exploit-code-request)

The interviewer asks a question that sounds like scope creep. “Harborline’s red team wants the agent to write working exploits for vulnerabilities it finds in client networks. Can we add that?” The answer depends on Anthropic’s policy, and a candidate who knows it answers precisely.

Claude’s generally available models carry safeguards that block most offensive cyber work, including exploit development. Anthropic’s Cyber Verification Program can lift some of those blocks for verified organizations. Its Red Team Access tier covers authorized penetration testing and red teaming, limited to systems the organization is authorized to test. Individual researchers are not eligible for that tier. On Amazon Bedrock, the program is available only to customers eligible for Enterprise Frontier Safeguards.

A strong answer uses those facts without hiding behind them.

Not in this agent, and not without the right access. Exploit development is blocked on Claude’s default models, so the path is for Harborline to apply for Red Team Access through Anthropic’s Cyber Verification Program. Because Harborline runs on Bedrock, we’d also confirm its eligibility there first. If approved, the work would run as a separate, access-controlled system scoped to clients who signed a testing agreement, never inside the triage agent. And I wouldn’t try to get around the safeguards by splitting the request into harmless-looking pieces. That would break the customer’s trust in us and Anthropic’s trust in the deployment.

The final sentence matters most. Interviewers listen for whether a candidate treats safety rules as obstacles to route around or as part of the design. Naming the workaround and refusing it shows the second.

## Defending the case under questioning[#](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Defending-the-case-under-questioning)

A case study ends the way a real engagement does, with the customer asking hard questions. The eval proved the agent catches every real attack in the sample and showed exactly what the safety rules cost. The follow-ups were answered with measured numbers and a fail-closed design. The requirement change became a narrow, gated rollout, and the exploit request was answered with Anthropic’s actual policy. A candidate who handles all three kinds of question this way shows an interviewer someone a security customer could trust with its alerts.

Building the Agent for the Security Alert Triage Case

Anthropic Forward Deployed Engineer

Ask

[Proving the agent works](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Proving-the-agent-works)

[Technical follow-up questions](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Technical-follow-up-questions)

[Cost at full alert volume](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Cost-at-full-alert-volume)

[The SIEM goes down](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#The-SIEM-goes-down)

[An alert Claude cannot classify](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#An-alert-Claude-cannot-classify)

[Why there is no sub-agent](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Why-there-is-no-sub-agent)

[Handling a requirement change](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Handling-a-requirement-change)

[Answering the exploit code request](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Answering-the-exploit-code-request)

[Defending the case under questioning](https://www.educative.io/courses/forward-deployed-engineer/interview-questions-on-the-security-alert-triage-case#Defending-the-case-under-questioning)