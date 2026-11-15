# Evaluation_of_Google_Docs’_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of Google Docs’ Design

Understand how the collaborative document editing service meets non-functional requirements such as consistency, latency, availability, and scalability through techniques like OT, CRDTs, replication, WebSockets, CDNs, and sharding. Learn how the design maintains reliable conflict resolution, low-latency collaboration, fault tolerance, and horizontal scalability across active documents and distributed components.

We'll cover the following...

- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Requirements-compliance)
  - [Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Consistency)
  - [Latency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Latency)
  - [Availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Availability)
  - [Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Scalability)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Conclusion)

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Requirements-compliance)

This lesson will focus on how our design meets the non-functional requirements.

### Consistency[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Consistency)

We ensure strong consistency for conflict resolution using OTsor CRDTs, with a time-series database preserving the order of operations. Once conflicts are resolved, the final state is persisted, ensuring consistent application of updates.

To keep document state consistent across servers within a data center, updated states are replicated using peer-to-peer protocols such as Gossip. This approach improves both consistency and availability.

AI-powered suggestions keep documents consistent too. Accepted edits go through the same operations queue as typed edits, and if the target text changed in the meantime, the suggestion goes back to the user for review instead of being applied blindly. Permission checks at request time keep suggestions limited to content the user can access.

1.

Why should we use strong consistency instead of eventual consistency for conflict resolution in a collaborative document editing service?

Show Answer

Did you find this helpful?

### Latency[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Latency)

Latency can increase when users are geographically distributed, but each client maintains a local replica of the document. Updates propagate via WebSockets, keeping perceived latency low. Most edits consist of small text payloads, so replication within and across data centers remains efficient. Large, infrequently changing assets such as images and videos can be delivered through CDNs.

In practice, documents have a limited number of active editors. Readers load the document once and can be served from a single data center. For writers, selecting an optimal zone close to collaborators helps minimize latency. For highly popular documents, asynchronous replication improves performance, though it makes strong consistency harder to guarantee.

### Availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Availability)

Availability is achieved through replication and continuous monitoring of primary and replica servers. Core components, such as operation queues and data stores, handle replication internally.

WebSocket servers connect users to session management services that track active collaborators. Running multiple WebSocket servers improves fault tolerance. Caching layers and CDNs further enhance availability during failures.

Disaster recovery is not addressed in the current design.

## Non-Functional Requirements Compliance

|  |  |
| --- | --- |
| **Requirements** | **Techniques** |
| Consistency | - Gossip protocol to replicate operations of a document within the same data center - Concurrency techniques like OT and CRDTs - Usage of time series database for maintaining the order of operations - Replication between data centers |
| Latency | - Employing WebSockets - Asynchronous replication of data - Choosing optimal location for document creation and serving - Using CDNs for serving videos and images - Using Redis to store different data structures including CRDTs - Appropriate NoSQL databases for the required functionality |
| Availability | - Replication of components to avoid SPOFs - Using multiple WebSocket servers for users that may occasionally disconnect - Component isolation improves availability - Implementing disaster recovery protocols like backup, replication to different zones, and global server load balancing - Using monitoring and configuration services |
| Scalability | - Different data stores for different purposes enable scalability - Horizontal sharding of RDBMS - CDNs capable of handling a large number of requests for big files |
| Permission-aware AI | - Permission checks at request time - Caches keyed by user and permission scope - Accepted AI edits go through the operations queue - Edits whose target text changed are sent back for review |

### Scalability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Scalability)

The microservice architecture allows each component to scale independently. If operation queues become a bottleneck, multiple queues can be created, with each queue dedicated to a single document.

All operations for a given document are routed to its assigned queue. The total number of queues scales with the number of active documents, enabling horizontal scalability.

AI Powered

Saved

10 attempts left

Reset

Speed vs. consistency

Hi, I’m Ed. In this session, we will focus on questions about Google Docs. Do you want to be mentored or evaluated?

You have 10 attempts to answer.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Conclusion)

This chapter describes the design of an online collaborative document editing service. The system includes features such as collaborative editing, version history for reverting to previous revisions, suggestions based on frequently used terms and phrases, and document view counts. The design also considers adding a chat feature for users collaborating on the same document. A key aspect of the design is conflict resolution for concurrent editing operations. The system addresses concurrency using operational transformation (OT) and conflict-free replicated data types (CRDTs). The design also adds an AI writing assistant that retrieves only content the user can access and applies accepted suggestions through the same operations queue as typed edits.

Concurrency in Collaborative Editing

Zoom System Design

Ask

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Requirements-compliance)

[Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Consistency)

[Latency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Latency)

[Availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Availability)

[Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Scalability)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-google-docs-design#Conclusion)