# Google_FDE_Interview_Vibe_Coding_and_System_Design_Guide

Source: https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Vibe Coding and System Design

Explore how to approach the vibe-coding session and agentic system design round, where ambiguous briefs test judgment as much as technical skill. Learn to clarify requirements, ship a working slice, adapt to changing direction, and apply a six-step framework to design enterprise agent systems.

We'll cover the following...

- [How the vibe-coding session works](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-vibe-coding-session-works)
- [A framework for the ambiguous build](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-the-ambiguous-build)
  - [Clarify](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Clarify)
  - [Ship a working slice](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Ship-a-working-slice)
  - [Adapt](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Adapt)
- [How the agentic system design round works](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-agentic-system-design-round-works)
- [A framework for agentic system design](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-agentic-system-design)
- [Common mistakes in both rounds](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Common-mistakes-in-both-rounds)

The vibe-coding session and the agentic system design round are the two parts of the Google FDE loop that candidates find most demanding. Neither has a single correct answer, and both begin with a brief that is deliberately incomplete. The interviewer is not checking whether we reach a predetermined solution. The interviewer is watching how we turn an ambiguous request into something that works and holds up under real constraints.

Both rounds reward the same working habit: clarify the problem, scope a first version, build something that works, and adapt as new information arrives. The sections below turn that habit into two practical frameworks, starting with the vibe-coding session.

## How the vibe-coding session works[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-vibe-coding-session-works)

The vibe-coding session is a 60-minute collaborative build. The interviewer presents a short brief and then works through the problem alongside us, much like a pair-programming partner. AI-assisted coding tools are often permitted, and that changes what the round measures. When a tool can generate most of the code, the signal shifts away from typing speed and toward judgment: what we choose to build, how we verify it, and how we respond when the direction changes.

During the session, the interviewer may suggest an approach, ask us to justify a decision, or change a requirement partway through. These interruptions are part of the format. They simulate a customer who learns something new during a working session and asks for a change. Because the setup varies, it is worth confirming with the recruiter whether AI-assisted tools are allowed and which environment the session uses, then practicing in a similar setup beforehand.

With the format clear, the next step is a framework for handling it.

## A framework for the ambiguous build[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-the-ambiguous-build)

A reliable approach is to divide the 60 minutes into three phases: clarify, ship a working slice, and adapt.

|  |  |  |
| --- | --- | --- |
| **Phase** | **Approximate time** | **Goal** |
| Clarify | 5 to 10 min | Understand the users, the input, the output, and what success looks like |
| Ship a working slice | 25 to 30 min | Build the smallest end-to-end version that produces a real result |
| Adapt | Remaining time | Incorporate changes, harden the solution, and explain what comes next |

### Clarify[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Clarify)

The first few minutes decide the direction of the whole session. Before writing code, we ask a small number of targeted questions about the users, the input data, the expected output, and how the customer will judge success. Three or four precise questions, followed by a short restatement of the problem, show the interviewer that we are building for the customer’s real need.

A restatement for a ticket triage brief might sound like this: “So the first version takes a support ticket, classifies it into one of five categories, and flags anything urgent for a human. Accuracy on the urgent flag matters more than the category. Is that right?”

### Ship a working slice[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Ship-a-working-slice)

A working slice is the thinnest version of the system that runs from input to output. It may handle only one case and skip error handling, but it produces a real result. Building end to end first reveals integration problems early and gives the interviewer something concrete to react to.

While building, we narrate decisions and name failure modes as they appear. When an AI coding tool generates code, we read it, explain it, and test it before moving on. Accepting generated code without review is a weak signal, because the same habit in a customer environment leads to untested code in production.

For the ticket triage example, a working slice might be a single function that sends one ticket to Gemini and returns a structured result.

Please provide values for the following:

GOOGLE\_GEMINI\_API\_KEY

Import Values from JSON

Python 3.14.0

```
from google import genai

from google.genai import types

from pydantic import BaseModel

class TicketTriage(BaseModel):

category: str

is_urgent: bool

reason: str

client = genai.Client(api_key="{{GOOGLE_GEMINI_API_KEY}}")

MODEL_ID = "gemini-3.6-flash"

def triage_ticket(ticket_text: str) -> TicketTriage:

response = client.models.generate_content(

model=MODEL_ID,  # A Flash-tier Gemini model

contents=f"Classify this support ticket:\n\n{ticket_text}",

config=types.GenerateContentConfig(

response_mime_type="application/json",

response_schema=TicketTriage,

),

)

return response.parsed

if __name__ == "__main__":

ticket = "My account was charged twice this month and I need a refund ASAP."

result = triage_ticket(ticket)

print("Category: ", result.category)

print("Urgent:   ", result.is_urgent)

print("Reason:   ", result.reason)
```

⋯

This slice is small but complete: a real ticket goes in, and a typed result comes out. Structured output makes the result easy to test and easy to pass to the next step. Exact SDK and model names change over time, so in the interview, correct structure and clear reasoning matter more than recalling a specific model version.

### Adapt[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Adapt)

Once the slice works, the interviewer often introduces a change, such as routing tickets to specific queues or handling tickets in another language. We acknowledge the change, explain how it affects the current design, and make the smallest update that handles it. If time remains, we harden the solution with input validation, error handling, or a quick test on a few sample tickets. In the final minutes, we describe what we would build next, such as a labeled evaluation set or a human review step for low-confidence results.

The vibe-coding framework covers building. The system design round asks us to reason about the whole system before building anything.

## How the agentic system design round works[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-agentic-system-design-round-works)

The agentic system design round is a 60-minute session in which the interviewer presents an enterprise scenario and asks us to design an AI system for it. Scenarios often involve a regulated industry, private enterprise data, or actions that affect real customers, such as issuing a refund.

Unlike a traditional system design interview, the focus is not only on scaling servers and databases. The interviewer wants to see how we choose an agent pattern, connect the agent to data and tools safely, control what it is allowed to do, and measure whether it works. A design that names the right components but treats evaluation as an afterthought is a common reason candidates lose ground.

The following framework gives the round a clear structure.

## A framework for agentic system design[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-agentic-system-design)

The framework has six steps. Each one answers a question the interviewer is likely to ask, so working through them in order covers the round’s expectations.

**1. Scope and success:** Enterprise briefs are usually broad, such as “build an AI assistant for our customer service operation.” A strong answer narrows this to one workflow, one user group, and a clear success metric. For example, the first release helps support agents answer billing questions, and success means lower handling time with accuracy above an agreed threshold.

**2. Data and tools:** We identify what the agent needs to know and what it needs to do. Knowledge usually comes from documents or databases, which leads to retrieval or Text-to-SQL. Actions come from tools, such as an API that looks up an account, which often connect through MCP. We also note data quality problems and access restrictions, because they constrain everything that follows.

**3. Agent pattern:** We choose the simplest pattern that meets the scope. A single agent with a few well-defined tools handles most first releases. Multiple agents are worth the added complexity only when parts of the work need separate ownership, different models, or isolated permissions. Explaining why we did not choose a more complex pattern is as valuable as describing the one we chose.

**4. Permissions and guardrails:** Every enterprise customer asks what the agent is allowed to do. A sound design enforces permissions outside the model, based on the user’s session and identity, rather than relying on prompt instructions. Low-risk actions, such as looking up an order, can run automatically. Medium-risk actions, such as drafting a customer reply, need human review. High-risk actions, such as issuing a refund, need explicit approval and logging.

**5. Evaluation and observability:** Interviewers for this track pay close attention to this step. We define what a correct output looks like, how we measure it, and how we catch regressions before they reach the customer. A strong answer includes a golden set of real examples, an automated check before each release, and tracing that records each step the agent takes in production.

**6. Deployment and cost:** We explain where the system runs and what it costs. Deployment choices, such as a managed agent runtime, Cloud Run, or GKE, depend on the customer’s security and operations constraints. Cost depends on model choice, context size, and request volume. Even a rough cost-per-request estimate shows that we think about the system the way the customer’s budget owner will.

Time management matters as much as the steps themselves. Reaching evaluation by roughly the 40-minute mark leaves room for deployment, cost, and follow-up questions. If time runs short, a one-sentence summary of each remaining step is better than skipping it, since a missing evaluation plan is one of the most frequently flagged gaps in this round.

## Common mistakes in both rounds[#](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Common-mistakes-in-both-rounds)

Several mistakes appear in both rounds. The first is skipping clarification, which leads to building or designing for an assumed problem. The second is overbuilding: proposing a multi-agent system or elaborate abstractions when a single agent or a simple function would meet the scope. The third is treating the interviewer as an observer rather than a collaborator. In both rounds, asking a specific question about the interviewer’s preference is a positive signal. The last is leaving evaluation until the end, or leaving it out entirely.

The vibe-coding session and the agentic system design round test the same capability from two directions. One asks us to build under changing requirements, and the other asks us to reason about a full system before building. In both, the strongest candidates clarify before acting, choose the simplest design that meets the scope, and treat evaluation as part of the work rather than a finishing step. That combination is what Google looks for in an engineer who will deliver AI systems inside a customer’s environment.

The Google FDE Interview Loop

Googleyness and Leadership

Ask

[How the vibe-coding session works](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-vibe-coding-session-works)

[A framework for the ambiguous build](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-the-ambiguous-build)

[Clarify](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Clarify)

[Ship a working slice](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Ship-a-working-slice)

[Adapt](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Adapt)

[How the agentic system design round works](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#How-the-agentic-system-design-round-works)

[A framework for agentic system design](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#A-framework-for-agentic-system-design)

[Common mistakes in both rounds](https://www.educative.io/courses/forward-deployed-engineer/vibe-coding-and-system-design#Common-mistakes-in-both-rounds)