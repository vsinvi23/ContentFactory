# Designing_Multi-Agent_Systems_for_Automated_Shipment_Rerouting

Source: https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Decomposing the Problem: Multi-Agent System

Explore how to decompose and design a multi-agent system that automates shipment rerouting within a global logistics company. Learn to integrate multiple data sources, respect operational constraints, and ensure human approval in updating shipment records. Understand the key subproblems and constraints shaping a reliable, auditable solution for disruption management.

We'll cover the following...

- [The case study](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#The-case-study)
- [Clarifying questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Clarifying-questions)
  - [Workflow and process questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Workflow-and-process-questions)
  - [Data and systems questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Data-and-systems-questions)
  - [Risk and authority questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Risk-and-authority-questions)
  - [Success and scope questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Success-and-scope-questions)
- [Problem decomposition](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Problem-decomposition)
- [Constraints that shape the architecture](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Constraints-that-shape-the-architecture)
- [Refined problem statement](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Refined-problem-statement)

This lesson works through a case study from a global freight company. The company manages shipment disruptions through a manual coordination process that spans three separate data sources and ends with a write action to a production system. The request is to automate that process. The real design question is which steps can safely run without human involvement and which require a coordinator to remain in the loop. Answering that question requires working through the case study carefully before any system is designed.

## The case study[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#The-case-study)

The complete case study is given below. Read it once before we begin decomposing it.

> **The case study**
>
> - **The organization:** A global freight and logistics company with operations across North America, Europe, and Southeast Asia. The company manages around 45,000 active shipments at any given time, routed through a network of 200-plus carriers and 30 regional hubs.
> - **The problem:** When a weather event, port closure, or carrier capacity failure occurs, a disruption coordinator manually checks signals from three separate sources, identifies which shipments are affected, evaluates available alternative routes and carrier slots, and executes rerouting decisions by updating records in SAP TM. The process is labor-intensive and requires pulling and reconciling data across systems that were not designed to work together. During peak disruption periods, such as hurricane season or major port strikes, multiple simultaneous disruptions arrive faster than the team can process them one at a time.
> - **The systems:** Shipment records live in SAP TM, where SAP stands for Systems, Applications, and Products in Data Processing and TM stands for Transportation Management. It serves as the company’s system of record for all active loads and exposes a REST API used by other internal tools for read and write operations. Disruption signals come from three sources the operations team monitors today.
>
>   - The first is [Tomorrow.io FleetIQ](https://www.tomorrow.io/solutions/logistics-transportation/), a weather intelligence platform that provides route-level weather risk scores and severe-event alerts via REST API.
>   - The second is the [Portcast Port Congestion API](https://www.portcast.io/blog/portcast-port-congestion-data-now-available-via-api-for-reliable-real-time-insights), a port congestion intelligence service that provides real-time berth wait times, vessel queue data, and terminal-level congestion scores for the ports the company operates through.
>   - The third is [project44](https://developers.project44.com/api-reference/api-docs), a multi-modal supply chain visibility platform the company uses to connect with carriers. project44 aggregates carrier exception signals from EDI (Electronic Data Interchange) feeds, carrier APIs, and telematics into normalized disruption events, and it exposes carrier slot availability and rate quotes through its own API.
>   - All three data sources are already integrated into the company’s AWS-hosted private cloud environment through scheduled polling jobs run by the operations team.
> - **The requirements:** Any write action to SAP TM requires explicit human approval before execution. The company’s IT security and audit policy prohibits fully automated writes to production systems without a human-in-the-loop step. Carrier selection must respect contractual constraints. Hazardous goods, temperature-controlled freight, and oversized loads each have a separate approved-carrier list stored in a relational database the operations team manages. The system must produce a recommendation package in plain language that a non-technical operations coordinator can read and approve without consulting a data analyst.
> - **The ask:** When a disruption is detected across any of the three data sources, the system should identify all affected shipments in SAP TM, generate ranked rerouting options for each using carrier slot data from project44, calculate the cost of rerouting against the cost of the delay, and deliver a ready-to-act recommendation package to the operations coordinator. The coordinator’s role shifts from manually gathering and reconciling data across systems to reviewing a structured recommendation and approving the action. After approval, the system executes the SAP TM update and sends carrier notifications through project44.

With the case study in hand, we can begin decomposing it.

## Clarifying questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Clarifying-questions)

The case study describes a manual workflow spread across three data sources, a hard requirement for human approval for SAP TM writes, and a goal of automating the coordination work. Each of those details leaves open questions that determine what the system can actually do. The four categories below organize the questions by what each reveals.

![](001_Designing_Multi-Agent_Systems_for_Automated_Shipment_Rerouting_images/img_257ddd48a3ba.svg)

### Workflow and process questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Workflow-and-process-questions)

Understanding the current manual workflow step by step is the first priority. Without this, the system risks automating the sequence the operations team follows today rather than the sequence that produces a reliable rerouting decision.

- Who triggers the rerouting analysis, and what does the trigger look like? Does the coordinator monitor all three disruption sources on separate dashboards, or does one source typically surface the alert first and the others confirm it?
- What level of disruption actually warrants a rerouting analysis? Not every weather alert or port congestion signal justifies the cost and complexity of rerouting. The operations team likely has an informal threshold today, and that threshold needs to become an explicit parameter in the system.
- Which disruption type triggers a rerouting analysis most often? Weather events on road routes, port congestion on ocean lanes, and carrier capacity failures each require different data and different response logic.
- Who has authority to approve a rerouting decision? Does the coordinator act alone, or does a manager need to sign off above a certain cost threshold?
- What does the coordinator weigh before selecting an alternative route? Carrier slot availability, rate, delivery time impact, and shipment type constraints are each a separate lookup in the current workflow.

The answers map the current decision process step by step and reveal which steps carry judgment that must be preserved in the system and which are mechanical lookups that can run automatically.

### Data and systems questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Data-and-systems-questions)

The case study names three disruption sources and one system of record. The questions below surface what is actually available in each and whether the data is consistent enough to act on programmatically.

|  |  |
| --- | --- |
| **Source** | **Key Questions** |
| Tomorrow.io  FleetIQ | - Does the company receive route-level weather risk scores or only location-level alerts? - What score or severity level constitutes a disruption worth acting on, versus normal weather variability the operations team monitors but does not respond to? |
| Portcast Port Congestion API | - What congestion level at a contracted port constitutes a disruption that warrants a rerouting analysis? - Does the API response return a congestion score, a predicted wait time, or a binary alert flag? |
| project44 | - Does the integration return carrier slot availability in real time, or does a rate-quote request take several minutes to resolve? - Which carrier exception types currently trigger manual review by the operations team? |
| SAP TM | - What fields identify a shipment’s route, carrier, and transit ports? - Is there a direct field linking each load to its port of transit, or does affected shipment identification require querying across multiple route legs? |
| Approved-carrier database | - How is the approved-carrier list structured and how is it accessed? - How frequently does it change when carrier certifications or contracts are updated? |

One question applies across all three disruption sources. When a [Tomorrow.io](https://www.educative.io/courses/forward-deployed-engineer/Tomorrow.io) severe weather score and a project44 carrier exception point to the same port on the same day, do they represent one disruption or two separate events? How the system deduplicates signals from different sources matters for how many rerouting analyses it triggers.

The answers determine what each agent in the system can call as a tool and what data will be available when a disruption event fires.

### Risk and authority questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Risk-and-authority-questions)

The risk questions surface the cost of a wrong automated decision and the authority structure that shapes how much the system can do without human involvement.

- What does a wrong rerouting decision cost in practice? A penalty from a carrier contract, a missed Service Level Agreement (SLA), or a shipment diverted to a longer route each carries a different financial and reputational consequence.
- Which failure mode is more costly in practice? Triggering an unnecessary reroute from a low-confidence signal, or missing a real disruption because the threshold was set too high?
- Has the company ever had an automated system write to SAP TM before? If this is the first time production shipment records would be updated by a non-human process, the approval workflow needs to be conservative and fully auditable from day one.
- Above what cost threshold does a rerouting decision escalate beyond the coordinator to a manager? The answer sets the boundary between coordinator-level approval and escalation, which shapes how the recommendation package is structured.

The answers define the approval model and determine how conservative the disruption threshold and confidence checks need to be before a recommendation is delivered.

### Success and scope questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Success-and-scope-questions)

The case study describes the outcome as automated disruption response, but leaves open which disruption type to address first and what the system must prove to be considered successful.

- Which disruption type causes the most operational impact per quarter? Building for the most costly disruption type first makes the initial delivery easier to justify and gives the team a clear comparison point against the manual process.
- Which shipment categories are highest priority? Hazardous goods, temperature-controlled freight, and high-volume standard loads each have different carrier constraint complexity and different SLA pressure from customers.
- What does a useful recommendation package look like when several disruptions arrive simultaneously? A coordinator managing multiple events at once needs a view that allows triage and quick action, not a detailed report for each shipment that requires reading in full before any decision can be made.
- What does success look like after the first three months of operation? Whether the team measures it by reduction in manual steps, fewer missed rerouting windows, or coordinator time freed up shapes what the system tracks and what the first evaluation report covers.

The answers set the scope of the initial delivery and clarify what the operations team will use to judge whether the system is working.

## Problem decomposition[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Problem-decomposition)

With the clarifying questions mapped, the problem breaks into six discrete subproblems. Each requires different data inputs, different reasoning, and a different tolerance for error. That combination is what makes this a multi-agent problem rather than a single agent handling everything in sequence.

- **Disruption detection:** Monitor Tomorrow.io FleetIQ, the Portcast Port Congestion API, and project44 on a schedule. Normalize signals from three different schemas into a consistent disruption event format. Apply the disruption threshold from the clarifying questions before triggering any downstream analysis.
- **Affected shipment identification:** Query SAP TM for active shipments on the affected route, port, or carrier. Map each confirmed disruption event to specific load records. Output a structured list of affected shipment IDs with disruption type, severity, and estimated delay impact per shipment.
- **Route and carrier option generation:** For each affected shipment, query project44 for alternative carrier slots. Filter every candidate against the approved carrier list for that shipment type before scoring. Rank alternatives by delivery time impact, carrier availability, and fit against the shipment’s contractual constraints.
- **Cost and feasibility calculation:** Calculate the cost of each candidate alternative route against the estimated cost of leaving the shipment on its delayed path. Flag cases where neither option is clearly better and mark those for escalation with both scenarios presented side by side.
- **Recommendation packaging:** Assemble a structured, plain-language package covering affected shipments, recommended routes, cost comparison, and the reasoning behind each recommendation. The coordinator must be able to read and act on this without querying the raw data from any underlying system.
- **Execution and notification:** After the coordinator approves, write the rerouting decision to SAP TM via its REST API and send carrier notifications through project44. Log every action with a timestamp and the identity of the approving coordinator for the audit record.

![Problem decomposition](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Problem decomposition")

Problem decomposition

Each subproblem has its own engineering complexity. Three constraints from the clarifying questions determine how several of them must be resolved.

## Constraints that shape the architecture[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Constraints-that-shape-the-architecture)

Three constraints directly determine what can and cannot be built.

- **Human approval gates every SAP TM write:** The IT security and audit policy is non-negotiable. The execution step cannot write to SAP TM without a structured approval signal from a coordinator. This means the system holds the recommendation open after delivery and does not proceed until approval arrives. The audit log must record the coordinator’s identity and the timestamp of each approval, not just the outcome of the write.
- **Approved-carrier lists constrain option generation before scoring:** The route and carrier option step cannot propose a carrier that is not on the approved list for that shipment type. Filtering must happen before ranking. A recommendation that includes a non-approved carrier would fail the compliance review and undermine the coordinator's trust in the system from the first use.
- **Concurrent disruption events require parallel execution:** When multiple disruptions arrive simultaneously from different sources, the system must handle each as an independent analysis chain running in parallel. The orchestration layer must isolate those chains so that data from one disruption does not affect the analysis for another, and so a slow or failed chain for one event does not block recommendations for others.

These three constraints define what the refined problem statement must account for.

## Refined problem statement[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Refined-problem-statement)

The original ask described a system that detects disruptions and handles the rerouting workflow. After decomposition, the statement is specific enough to design from. Here is the refined statement:

Design a multi-agent system that monitors Tomorrow.io FleetIQ, the Portcast Port Congestion API, and project44 for disruption signals above the agreed threshold; identifies affected SAP TM shipment records; generates rerouting options constrained by approved-carrier lists per shipment type; calculates the cost comparison against the delay cost; delivers a coordinator-readable recommendation package; and executes the approved SAP TM update and project44 carrier notification with a full audit log.

Structured decomposition makes the system design defensible by providing a clear rationale for each design decision. The six subproblems identify the engineering work. The three constraints determine which design choices are available. The approval boundary establishes the liability model the company’s audit team will require before the system touches SAP TM. The next step is to use that statement to design the system.

Build a RAG Using LangChain with Google Gemini

System Design: Multi-Agent System

Ask

[The case study](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#The-case-study)

[Clarifying questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Clarifying-questions)

[Workflow and process questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Workflow-and-process-questions)

[Data and systems questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Data-and-systems-questions)

[Risk and authority questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Risk-and-authority-questions)

[Success and scope questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Success-and-scope-questions)

[Problem decomposition](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Problem-decomposition)

[Constraints that shape the architecture](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Constraints-that-shape-the-architecture)

[Refined problem statement](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-multi-agent-system#Refined-problem-statement)