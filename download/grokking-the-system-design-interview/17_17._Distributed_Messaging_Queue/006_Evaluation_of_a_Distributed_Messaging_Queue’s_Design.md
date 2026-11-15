# Evaluation_of_a_Distributed_Messaging_Queue’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of a Distributed Messaging Queue’s Design

Assess a distributed messaging queue design against its core functional and non-functional requirements. Analyze how the design supports the message life cycle, durability guarantees, and horizontal scalability through replication and partitioning. Examine the performance trade-offs between strict message ordering and overall system throughput.

We'll cover the following...

- [Functional requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Functional-requirements-compliance)
- [Non-functional compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Non-functional-compliance)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Conclusion)

With the design complete, we now analyze how the proposed architecture satisfies the functional and non-functional requirements of a distributed messaging queue.

## Functional requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Functional-requirements-compliance)

- **Queue creation and deletion:**

  - **Creation:** When the front-end receives a creation request, it validates the client’s details. The cluster manager assigns servers to the new queue and updates the metadata stores and caches via the metadata service.
  - **Deletion:** When a client requests deletion, the cluster manager deallocates the queue’s storage space and removes the associated data from metadata stores and caches.

1.

How should we handle messages that a consumer fails to consume after the maximum number of retry attempts?

Show Answer

Did you find this helpful?

- **Send and receive messages:** Producers deliver messages to specific queues. At the backend, incoming messages are sorted by timestamps to preserve order and placed in the queue. Consumers then retrieve messages from these queues.

When the frontend receives a message, it identifies the primary host or cluster where the queue resides (depending on the replication model). It forwards the request to the corresponding entity for enqueueing.

- **Message deletion:** There are two primary approaches to deleting messages:

1. **No immediate deletion (Offset tracking):** Messages are not deleted upon consumption. Instead, the system maintains message order, and consumers track their own progress (offsets). A background job deletes messages once expiration conditions are met. Apache Kafka uses this model to allow multiple processes to consume the same message stream.
2. **Visibility time-out:** Messages are not deleted immediately but are made invisible to other consumers for a specific duration (e.g., `visibility_timeout`). The consumer must explicitly delete the message via an API call after processing. If the consumer fails to delete it within the timeout, the message becomes visible again.

In the second approach, the consumer is responsible for the final deletion. This ensures high durability; if a consumer crashes before processing is complete, the message reappears in the queue for another worker to handle.

This mechanism provides at-least-once delivery semantic. If a worker fails, the message eventually becomes visible again, ensuring it is processed at least once.

1.

What happens when the visibility time-out for a specific message expires while the consumer is still processing it?

Show Answer

Did you find this helpful?

## Non-functional compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Non-functional-compliance)

- **Durability:** We replicate queue metadata and message data across different nodes. If a node fails, the system uses replicas to deliver or retrieve messages, ensuring no data is lost.
- **Scalability:** Components like frontend servers, metadata servers, caches, and backend clusters are horizontally scalable. We can adjust capacity based on two dimensions:

  - **Message volume:** If a queue’s message count exceeds a threshold (e.g., 80%), the system expands the queue’s storage. Conversely, it shrinks storage when volume drops.
  - **Queue volume:** As the number of queues increases, the cluster manager adds more servers. We provision nodes to ensure performance isolation, preventing high load on one queue from impacting others.
- **Availability:** We replicate data (metadata and messages) within or across data centers. Load balancers route traffic around failed nodes, ensuring the system remains available during faults.
- **Performance:** Caching, replication, and partitioning reduce read/write latency. We use a “best-effort” ordering strategy to maximize throughput. If strict ordering is required, we use time-window-based sorting, which may affect latency.

AI Powered

Saved

1 attempt left

Reset

How can you use a distributed messaging queue in online games?

Describe how a distributed messaging queue would be used in an online multiplayer game to manage real-time player actions (movement, attacks, etc.). What are the crucial requirements for this scenario?

This is your last attempt.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Conclusion)

Designing a distributed FIFO queue requires balancing strict ordering with throughput and latency. Relaxed ordering improves throughput and reduces latency. Strict ordering requires additional synchronization, such as timestamp-based or causality-based coordination, which increases system overhead. Replication and partitioning enable horizontal scaling of storage and throughput. A simple producer-consumer queue becomes significantly more complex when implemented in a distributed environment.

Design of a Distributed Messaging Queue: Part 2

Quiz on the Distributed Messaging Queue’s Design

Ask

[Functional requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Functional-requirements-compliance)

[Non-functional compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Non-functional-compliance)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-messaging-queues-design#Conclusion)