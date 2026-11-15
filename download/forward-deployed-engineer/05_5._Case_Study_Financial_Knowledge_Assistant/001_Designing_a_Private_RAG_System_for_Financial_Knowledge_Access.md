# Designing_a_Private_RAG_System_for_Financial_Knowledge_Access

Source: https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Decomposing the Problem: The RAG System

Explore the decomposition of a real-world case study involving a mid-size investment bank's need for efficient, permission-sensitive document access. Learn to break down complex enterprise constraints such as private cloud deployment, heterogeneous document sources, and strict access control into distinct engineering subproblems. Understand how to design a retrieval-augmented generation system that respects document-level access controls and self-hosts AI models for embedding and answer generation. This lesson equips you to clarify problem requirements, address engineering challenges, and create a solution architecture that meets diverse user needs in an enterprise AI system.

We'll cover the following...

- [The case study](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#The-case-study)
- [Clarifying questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Clarifying-questions)
  - [User and workflow questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#User-and-workflow-questions)
  - [Document and source questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Document-and-source-questions)
  - [Constraint questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraint-questions)
  - [Success and measurement questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Success-and-measurement-questions)
- [Problem decomposition](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Problem-decomposition)
- [Constraints that shape the architecture](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraints-that-shape-the-architecture)
- [Refined problem statement](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Refined-problem-statement)

This lesson works through a case study from a mid-size investment bank. The case study names a business pain, specifies some constraints, and asks for a solution without defining what that solution looks like. It represents a common class of AI system problem in enterprise settings: a large, heterogeneous document corpus, meaningful access control requirements, and a desire to make it queryable through natural language.

## The case study[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#The-case-study)

Given below is the complete case study of a mid-size investment bank. Read it once before we begin breaking it down.

> **The case study**
>
> - **The organization:** A mid-size investment bank with around 4,000 employees across New York, London, and Hong Kong.
> - **The problem:** Analysts, compliance officers, and senior advisors lose significant time every week searching for information across the bank’s internal document corpus. A typical equity research analyst spends two to three hours before writing a note locating relevant prior research, comparable company filings, and internal memos on the sector. Compliance officers manually scan through policy documents and regulatory guidance to answer questions from the business. Senior advisors assembling a pitch book spend half a day locating relevant deal precedents and internal models from prior transactions.
> - **The documents:** Documents live in three places: SharePoint for internal research notes, compliance policies, and deal memos organized by client; an email archive for Bloomberg Message and Outlook threads going back eight years; and a shared file server for SEC filing PDFs, earnings transcripts, and older documents that predate SharePoint.
> - **The requirements:** All documents and all processing must stay within the bank’s private cloud. No document content, chunk, or query can be sent to any external service. The system must also respect the document permissions that already exist in SharePoint. Different teams and seniority levels have access to different document libraries. If an employee cannot access a document in SharePoint today, they should not be able to receive an answer derived from that document through the AI system. The same access control principle extends to the email archive and file server.
> - **The ask:** Employees should be able to ask questions in plain language and get accurate answers from internal documents.

With the case study in hand, we can begin decomposing it.

## Clarifying questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Clarifying-questions)

The questions below are organized by category. Each category surfaces a different type of information that directly shapes the scope and architecture of what we build.

### User and workflow questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#User-and-workflow-questions)

Understanding who uses the system and how they work today tells us what the system actually needs to do well. The three user groups in the case study have different roles, rely on different document types, and have different tolerances for wrong answers.

![](001_Designing_a_Private_RAG_System_for_Financial_Knowledge_Access_images/img_536544cc5ed5.svg)

- Who are the primary users across the three groups, and do their search patterns differ enough to require different retrieval behavior?
- What does a failed search look like today for each group? Do users give up, ask a colleague, or use a workaround?
- What format do users expect answers in? A brief cited summary, a full document excerpt, or a ranked list of source documents?
- Are there peak usage periods, such as earnings season for analysts or regulatory audit periods for compliance, that affect availability and latency requirements?

The answers determine whether one retrieval approach serves all users or whether the system needs to handle meaningfully different query patterns across groups.

### Document and source questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Document-and-source-questions)

The three document sources in the case study are structurally different. Each requires a separate connector, produces different raw output, and updates on a different schedule. The table below maps the key characteristics of each source.

|  |  |  |  |
| --- | --- | --- | --- |
| **Source** | **Primary Formats** | **How Often It Updates** | **Key Open Question** |
| SharePoint | Word, PDF, Excel | Regular, structured | How is it organized? Does the folder structure reflect access restrictions? |
| Email archive | Message threads, attachments | Continuously | Are all message types stored in one archive, or are they separate systems? How are conversation threads structured? |
| File server | PDFs, scanned documents | Rarely | What proportion are scanned and require OCR processing to extract text? |

Two questions apply across all three sources:

- What is the total document volume across all sources combined?
- Are documents duplicated across sources, for example, a deal memo attached in an email and also stored in SharePoint?

The answers determine how the ingestion pipeline is structured and what preprocessing each source requires before anything is indexed.

### Constraint questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraint-questions)

The two hard requirements in the case study carry significant architectural implications. Both need precise answers before any design decision is made.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

- The first requirement is private deployment. “No document content, chunk, or query can be sent to any external service” raises specific questions:

  - What infrastructure does the bank’s private cloud run on, and does it have GPU capacity for hosting AI models?
  - If GPU capacity does not exist today, what is the provisioning process and expected timeline?
  - Is there a model review process the bank’s IT or security team runs before an open-weight model can be deployed?
- The second requirement is document-level access control. The bank’s SharePoint already has permissions that determine which employees can access which document libraries. The AI system must respect those same permissions at query time.

  - How are SharePoint permissions currently structured? Are they at the folder level, the library level, or the individual document level?
  - Do the email archive and file server have equivalent permission structures, or only SharePoint?
  - How frequently do permissions change, for example, when employees change teams or join or leave the bank?
  - Does SharePoint expose an API that returns the documents a given user is permitted to access?

The answers determine how the retrieval layer reads and enforces permissions at query time.

### Success and measurement questions[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Success-and-measurement-questions)

The case study describes the outcome as accurate answers in plain language. That definition is not specific enough to evaluate against or build toward.

- What accuracy threshold is acceptable for each user type? A compliance officer answering a regulatory question has a lower tolerance for a wrong answer than an analyst doing background research.
- How will accuracy be measured? By user feedback, by an internal evaluation process, or by comparison to answers from subject matter experts?
- What does a wrong answer cost in practice? For a compliance question with regulatory consequences, a missed reference carries material risk.
- What does a successful deployment look like in three to six months?

The answers define the evaluation criteria for the system and the success threshold for the initial delivery.

## Problem decomposition[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Problem-decomposition)

With the clarifying questions mapped, the problem breaks into seven discrete subproblems. Each is a separate engineering challenge with its own inputs, outputs, and design decisions.

- **Document ingestion:** Three separate connectors for SharePoint, the email archive, and the file server. SharePoint exposes a Graph API. The email archive and file server require different access methods, and each connector runs on a schedule matched to how often that source updates.
- **Parsing and preprocessing:** PDFs, Word documents, email threads, and scanned files each require different parsing logic. Email threads require reconstruction and attachment extraction. Scanned documents require OCR (optical character recognition) before any text is available for processing.
- **Embedding and indexing:** Document chunks are embedded using an open-weight embedding model self-hosted on the bank’s private infrastructure. No data leaves the environment at this stage. Embeddings and their associated metadata are stored in a vector index running within the private cloud.
- **Query handling and retrieval:** A user’s natural language question is embedded using the same model and matched against the index to return the most semantically relevant chunks.
- **Access control enforcement:** Each chunk carries the ACL (access control list) of its source document as metadata, stored at ingestion time. At query time, the user's group memberships are resolved and injected as a filter into the vector search, so the search runs only within the permitted subset. A background sync job keeps ACL metadata current as permissions change.
- **Answer generation:** An open-weight language model, also self-hosted, receives the retrieved and filtered chunks and generates a grounded, cited answer.
- **Evaluation:** A process for measuring whether answers are accurate, faithful to the retrieved source documents, and complete enough for each user type.

Each subproblem has its own engineering complexity. Three constraints from the clarifying questions determine how several of them must be resolved.

## Constraints that shape the architecture[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraints-that-shape-the-architecture)

Three constraints from the clarifying questions directly determine what can and cannot be built.

- **Private deployment with self-hosted models:** All models, both embedding and generation, must run on infrastructure the bank controls. Open-weight models make both tasks achievable within a private environment: models such as BGE or E5 handle embedding, and instruction-tuned open-weight LLMs such as Llama handle generation. The bank’s private cloud requires GPU capacity to serve it. If that capacity does not exist, provisioning it is a prerequisite that affects the project timeline.
- **Document-level access control.** Each document source has permissions that define which employees can access which content. When a document is ingested, its ACL is stored as metadata on every chunk in the vector store. At query time, the user’s identity is resolved to their group memberships and used as a filter on the vector search. Permissions change when employees join, leave, or change teams, so a background sync job keeps the ACL metadata in the index current.
- **Heterogeneous document sources:** The three sources share no common access pattern, format, or update schedule. SharePoint has a well-documented API and structured metadata. The email archive requires thread reconstruction and may involve two separate storage systems for Bloomberg Message and Outlook. The file server requires a scheduled crawler and likely includes a substantial volume of scanned documents needing OCR. The ingestion layer carries the most engineering effort of any component because each source requires entirely distinct handling.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

These three constraints define what the refined problem statement must account for.

## Refined problem statement[#](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Refined-problem-statement)

The original case study described the outcome as employees asking questions in plain language and getting accurate answers from internal documents. After decomposition, the statement is considerably more specific. Here is the refined statement:

Design a retrieval and generation system that ingests documents from three heterogeneous sources, embeds and indexes them on self-hosted private infrastructure, scopes each search to only the documents the requesting user is permitted to access, and generates grounded, cited answers using a self-hosted open-weight language model, evaluated against accuracy thresholds defined for each user type.

Arriving at a statement this specific through structured decomposition is what makes a system design possible to reason through correctly. The questions surface what the case study leaves implicit. The subproblems identify the engineering work. The constraints determine which design choices are available. The next step is to use that statement to design the system.

Practice Rounds and Self-Review Rubric

System Design: The RAG System

Ask

[The case study](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#The-case-study)

[Clarifying questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Clarifying-questions)

[User and workflow questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#User-and-workflow-questions)

[Document and source questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Document-and-source-questions)

[Constraint questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraint-questions)

[Success and measurement questions](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Success-and-measurement-questions)

[Problem decomposition](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Problem-decomposition)

[Constraints that shape the architecture](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Constraints-that-shape-the-architecture)

[Refined problem statement](https://www.educative.io/courses/forward-deployed-engineer/decomposing-the-problem-the-rag-system#Refined-problem-statement)