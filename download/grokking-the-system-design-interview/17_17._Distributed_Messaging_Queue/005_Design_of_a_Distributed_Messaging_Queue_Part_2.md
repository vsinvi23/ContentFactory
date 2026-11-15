# Design_of_a_Distributed_Messaging_Queue_Part_2

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design of a Distributed Messaging Queue: Part 2

Examine how backend services manage message storage and replication in a distributed messaging queue. Compare the primary-secondary model with a cluster of independent brokers. Explain how internal and external cluster managers coordinate queue placement, membership, and failover to maintain high availability.

We'll cover the following...

- [Backend service](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Backend-service)
  - [Primary-secondary model](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Primary-secondary-model)
  - [A cluster of independent hosts](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#A-cluster-of-independent-hosts)

Previously, we discussed frontend servers and metadata services. This lesson focuses on the backend service that stores queues and messages.

## Backend service[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Backend-service)

The **backend service** handles message storage, routing, and replication. When the frontend receives a message, it queries the metadata service to determine which broker is responsible for the queue. The message is forwarded to that broker and replicated to other nodes in the cluster to improve availability and durability. Replication typically follows one of two models:

1. Primary-secondary model
2. A cluster of independent hosts

Before detailing these models, we must distinguish between the two types of cluster managers responsible for queue management: internal and external. The table below outlines their differences.

## Internal vs. External Cluster Managers

|  |  |
| --- | --- |
| **Internal Cluster Manager** | **External Cluster Manager** |
| It manages the assignment of queues within a cluster. | It manages the assignment of queues across clusters. |
| It knows about each and every node within a cluster. | It knows about each cluster. However, it doesn’t have information on every host that’s present inside a cluster. |
| It listens to the heartbeat from each node. | It monitors the health of each independent cluster. |
| It manages host failure, instance addition, and removals from the cluster. | It manages and utilizes clusters. |
| It partitions a queue into several parts and each part gets a primary server. | It may split a queue across several clusters, so that messages for the same queue are equally distributed between several clusters. |

### Primary-secondary model[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Primary-secondary-model)

In the **primary-secondary model**, each node acts as the **primary host** for a specific set of queues. The primary host receives requests for its assigned queues and manages data replication. The frontend consults the metadata service to identify the correct primary host for each request.

For example, assume two queues (101 and 102) are assigned across four hosts (A, B, C, and D). If host B acts as the primary for queue 101, it replicates the queue data to secondary hosts such as A and C. When the frontend receives a request, it queries the metadata service, which is backed by the internal cluster manager, to determine the primary host. The primary host serves the read request and, after receiving an acknowledgment from the consumer, deletes the message and its replicas.

The internal cluster manager maps queues to primary and secondary hosts and assists in primary host selection. This component must be reliable, scalable, and performant.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27651%27%20height=%27544%27/%3e)![Primary-secondary model of distributed queue: A request is received for a queue with ID 101, which is served accordingly](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Primary-secondary model of distributed queue: A request is received for a queue with ID 101, which is served accordingly")

Primary-secondary model of distributed queue: A request is received for a queue with ID 101, which is served accordingly

### A cluster of independent hosts[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#A-cluster-of-independent-hosts)

In the **cluster of independent hosts** model, multiple clusters of independent hosts are distributed across data centers. When the front-end receives a message, it queries the metadata service (backed by the external cluster manager) to identify the correct cluster. The message is forwarded to a random host within that cluster, which then replicates the message to other hosts storing that queue.

1.

How does a host in the cluster replicate messages to queues on other nodes?

Show Answer

Did you find this helpful?

A similar process applies to consumer requests. The randomly selected host handles message delivery and cleans up the message after successful processing.

This model introduces an **external cluster manager** to map queues to specific clusters. It handles queue management and assigns queues to appropriate clusters.

The figure below illustrates this architecture with two clusters, A and B. The external cluster manager maintains a mapping table linking queues to their corresponding clusters. When the frontend receives a request, it routes traffic to the appropriate cluster, where nodes handle storage and delivery.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27851%27%20height=%27510%27/%3e)![A cluster of independent hosts that consist of distributed queues](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A cluster of independent hosts that consist of distributed queues")

A cluster of independent hosts that consist of distributed queues

1.

How is message replication handled in distributed queue systems?

Show Answer

Did you find this helpful?

At this stage, the backend service design covers two organizational models: primary–secondary and clusters of independent hosts. It also defines queue management, message processing, and the distinct roles of internal and external cluster managers. The next lesson evaluates how the proposed architecture satisfies the previously defined functional and non-functional requirements.

AI Powered

Saved

1 attempt left

Reset

Lag in Cluster Manager

If the internal cluster manager suddenly became slower at mapping primaries and secondaries, how might this influence the overall design goals of the back-end service?

This is your last attempt.

Design of a Distributed Messaging Queue: Part 1

Evaluation of a Distributed Messaging Queue’s Design

Ask

[Backend service](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Backend-service)

[Primary-secondary model](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#Primary-secondary-model)

[A cluster of independent hosts](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-distributed-messaging-queue-part-2#A-cluster-of-independent-hosts)