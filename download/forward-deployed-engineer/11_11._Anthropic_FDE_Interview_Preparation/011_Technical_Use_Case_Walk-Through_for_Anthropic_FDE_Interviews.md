# Technical_Use_Case_Walk-Through_for_Anthropic_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Technical Use Case Screen Walk-Through

Explore how to approach a technical use case screen in Anthropic's FDE interview by clarifying customer requirements, designing an effective tool layer, defining a safe initial system version, and maintaining reliability on complex tasks. This lesson guides you through using Claude responsibly and demonstrating a deployable AI solution that meets real-world constraints.

We'll cover the following...

- [Clarifying before designing](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Clarifying-before-designing)
- [Designing the tool layer with MCP](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Designing-the-tool-layer-with-MCP)
- [Stating a bounded first version](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Stating-a-bounded-first-version)
- [Keeping long tasks reliable](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Keeping-long-tasks-reliable)
- [Using Claude in the room](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Using-Claude-in-the-room)
- [Walking the customer’s path](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Walking-the-customers-path)

The technical use case screen gives a candidate a customer scenario and asks how they would deploy Claude to solve it. The conversation covers MCP tools, reliability on long documents, and sometimes the candidate’s use of Claude itself during the call. A strong candidate drives the conversation and decides what to ask, what to build first, and what to leave for a later version.

A strong answer follows a recognizable path. It clarifies the problem, designs the tool layer, commits to a bounded first version, explains how the system stays reliable, and uses Claude in the room with care. The walkthrough below works through one realistic prompt along that path, the way a strong candidate would say it out loud.

> A logistics company wants Claude to answer its analysts’ questions about carrier contracts and to draft dispute emails to carriers. The contracts live in a document store, and disputes are tracked in a ticketing system. How would you build this?

## Clarifying before designing[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Clarifying-before-designing)

The prompt does not specify several requirements that would influence the system architecture. Starting with an architecture diagram before clarifying those requirements risks building a solution around unsupported assumptions. Start with five questions that can significantly affect the design, and confirm the answers rather than relying on assumptions.

- **Who will use the system?** Determine whether the users are internal analysts, carriers, or customers. Their workflows affect response-time requirements, review procedures, and the level of validation required before presenting results.
- **What data is available, and who can access it?** Confirm the contract formats, volume, update frequency, and retrieval requirements. Identify which user's or service identity's permissions apply to each data access operation.
- **What actions can the system perform?** Distinguish read-only responses from actions that modify records or communicate externally. Sending a dispute email, for example, may require explicit authorization and human approval.
- **What request volume should the system support?** A few hundred requests per day and several hundred thousand may require different approaches to capacity planning, caching, batching, latency, and cost.
- **How will correctness be evaluated?** Define measurable acceptance criteria before implementation. For example, an answer may need to cite the relevant contract clause and reproduce all numerical values accurately.

During the interview exercise, the interviewer provides answers from the customer's perspective. Record these answers visibly so you can refer to the confirmed requirements when explaining subsequent design decisions.

![](011_Technical_Use_Case_Walk-Through_for_Anthropic_FDE_Interviews_images/img_5240b26b5ef5.svg)

Sometimes the interviewer replies “you decide.” That reply is an invitation to make a reasonable assumption, say it out loud, and move on. A line such as “I’ll assume analysts review every answer, and I’ll come back to this if that changes” keeps the design moving and shows that we know which assumptions carry weight.

Ace Editor

1

2

3

4

5

6

7

8

Scoping notes

- Users: 40 carrier-relations analysts. They read every answer and send every email themselves.

- Data: About 2,000 carrier contracts as PDFs, 60 to 200 pages each. Rate tables and penalty clauses vary by carrier.

- Access: Analysts may read every contract. Each analyst owns a queue of dispute tickets.

- Writes: Dispute emails go to carriers and can trigger credits worth thousands of dollars.

- Volume: About 300 questions a day and 50 disputes a week.

- Correct: The answer cites contract, section, and page, and every amount matches the clause.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

These notes already rule out one tempting design. At 60 to 200 pages per contract, 2,000 contracts hold at least 50 million tokens, far beyond a 1-million-token context window. Claude needs tools that find the right clause, which is where the design starts.

## Designing the tool layer with MCP[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Designing-the-tool-layer-with-MCP)

The tool layer is the set of MCP tools Claude can call, and it carries most of the design’s risk. Four choices shape it.

- **One server per system:** A contracts server and a ticketing server keep each system’s credentials, owners, and failure modes separate. Either server can also be reused by another agent later in the engagement.
- **Read and write tools apart:** Tools that only read sit apart from tools that change data, so the agent’s permissions can grant reading freely and writing narrowly.
- **Descriptions that guide the call:** Each description says when to use the tool and what it returns, such as clause text with its section and page for citation.
- **Approval at the point of consequence:** A person approves the step that leaves the company, which is the email to the carrier.

The proposed tool surface below turns those choices into a list the interviewer can challenge line by line:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Tool** | **Server** | **Access** | **Approval** | **What It Does** |
| `search_contracts` | Contracts | Read | None | Finds clauses matching a question for one carrier. Returns contract ID, section, page, and text. |
| `get_clause` | Contracts | Read | None | Returns the full text of one section, with its page, for citation. |
| `get_ticket` | Ticketing | Read | None | Returns a dispute ticket with shipment details and the analyst’s notes. |
| `save_dispute_draft` | Ticketing | Write | None | Saves a draft email and its cited clauses to the ticket. Nothing is sent. |
| `send_dispute_email` | Ticketing | Write | Analyst | Not exposed to Claude. The analyst sends from the ticketing system. |

The last line is the strongest design choice on the list. Claude can prepare a dispute, and only a person can send one. `save_dispute_draft` writes, but only into the analyst’s own ticket, where nothing reaches a carrier until the analyst acts.

A tool surface shows what Claude could do. The interviewer also wants to know what we would ship first.

## Stating a bounded first version[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Stating-a-bounded-first-version)

A **bounded first version** is the smallest release that delivers real value while keeping every risky action under human control. Saying it out loud shows the interviewer that we would ship something in weeks and expand it based on evidence. A candidate might state it like this.

Version one answers contract questions with citations, read-only. Analysts check the cited clause before relying on an answer. Once citation accuracy holds on an eval set of real analyst questions, version two adds dispute drafts saved to the ticket. Analysts still send every email. We would only discuss sending on Claude’s behalf after months of drafts that analysts send unchanged.

Each stage earns the next one with a measured result. Citations make version one checkable by any analyst in seconds, and the eval set gives the expansion decision a number instead of a feeling. Two numbers carry most of the weight. Citation accuracy shows whether answers point to the right clause, and the share of drafts that analysts send without edits shows whether drafting saves them time.

Interviewers then push on the hardest technical part of the scenario: the length of the documents.

## Keeping long tasks reliable[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Keeping-long-tasks-reliable)

Dispute work is long. An analyst asks about late-delivery penalties, Claude searches three contracts, reads several clauses, checks the shipment in the ticket, and drafts an email. A design that works on one short question can drift over a task like that. Four controls keep it on track.

- **Retrieval over stuffing:** Claude reads the clauses `search_contracts` returns instead of whole contracts. Smaller, focused context keeps recall high and cost low, even for a 200-page contract.
- **Citations as checkpoints:** Every claim carries a contract, section, and page. An answer without a citation is treated as incomplete, which turns a vague failure into a visible one.
- **Turn and budget limits:** The agent runs with a cap on turns and cost, such as `max_turns` and `max_budget_usd` in the Agent SDK. A task that hits the cap goes back to the analyst with what was found so far.
- **Stop reasons read by code:** A response that ends with `max_tokens` or `model_context_window_exceeded` was cut off, and one that ends with `refusal` was declined. The system flags these instead of saving them as finished drafts.

Each control answers a specific failure. When the interviewer asks what happens on a 200-page contract, we name the control that handles it rather than relying on the large context window alone.

## Using Claude in the room[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Using-Claude-in-the-room)

Some use case screens allow live access to Claude. The interviewer is watching how we use it, so Claude’s output counts only after we have read and checked it. A good pattern has three parts:

- **Ask for a specific draft:** A narrow request, such as the five tool descriptions for the contracts server, gives a draft that can be checked in a minute.
- **Read it out loud and verify it:** We check each description against the scoping notes and say what we are checking, such as whether `search_contracts` returns the page number our citations need.
- **Fix and say why:** When the draft misses something, we correct it and explain the change.

A short narration makes the habit visible.

I asked Claude for the contracts tool descriptions. The search description is good, but it doesn’t say the results include page numbers, and our citations depend on that, so I’m adding it. It also suggested an `update_contract` tool. Analysts never edit contracts, so I’m removing it.

Pasting Claude’s output into the answer unread gives the interviewer the opposite signal. It suggests a candidate who would ship unreviewed output to a customer, which is the habit the screen exists to catch.

## Walking the customer’s path[#](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Walking-the-customers-path)

A use case screen rewards the same habits a real engagement does. We clarify until the design rests on the customer’s facts, build a tool layer that reads freely and writes carefully, ship a first version small enough to verify, and name the controls that keep long tasks honest. Using Claude live is part of that work, done with the same review we would give any draft headed to a customer. A candidate who walks this path out loud shows the interviewer a deployment they could trust in their own systems.

Live Debugging an Almost-Right Pipeline

Multi-Level Coding Round Practice

Ask

[Clarifying before designing](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Clarifying-before-designing)

[Designing the tool layer with MCP](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Designing-the-tool-layer-with-MCP)

[Stating a bounded first version](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Stating-a-bounded-first-version)

[Keeping long tasks reliable](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Keeping-long-tasks-reliable)

[Using Claude in the room](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Using-Claude-in-the-room)

[Walking the customer’s path](https://www.educative.io/courses/forward-deployed-engineer/the-technical-use-case-screen-walk-through#Walking-the-customers-path)