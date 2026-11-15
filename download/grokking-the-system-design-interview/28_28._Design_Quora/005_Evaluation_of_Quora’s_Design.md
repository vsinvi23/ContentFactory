# Evaluation_of_Quora’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of Quora’s Design

Evaluate the Quora System Design by assessing its compliance with non-functional requirements like scalability and performance. Learn how vertical sharding and varied consistency models address specific data needs. Define essential disaster recovery mechanisms, including remote backups and restoration strategies, to ensure system durability.

We'll cover the following...

- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Requirements-compliance)
- [Disaster recovery](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Disaster-recovery)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Conclusion)

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Requirements-compliance)

We have implemented various techniques to meet functional requirements. Now, let's evaluate how the design fulfills non-functional requirements:

- **Scalability:** The system scales effectively using powerful and homogeneous service hosts. These powerful machines handle in-memory caching, queueing, and routing. Their uniformity simplifies horizontal scaling. For the database, we use vertical sharding to distribute load across MySQL servers. To minimize complex `join` queries, related tables are placed in the same shard.

> **Note:** Vertical sharding has limits. Large tables may eventually cause write bottlenecks, requiring horizontal sharding.

- **Consistency:** The system applies different consistency guarantees based on data criticality. Critical data, such as questions and answers, is written with synchronous replication to ensure strong consistency. Although this increases write latency, the impact is acceptable because the end-to-end user workflow depends on human response time rather than millisecond-level write latency. Non-critical data, such as view counters, is handled using eventual consistency to favor availability and throughput.

> **Note:** Overall, the design prioritizes techniques that reduce user-perceived latency.

- **Availability:** We ensure availability through component isolation, redundancy, CDNs, and load balancers. Configuration services like ZooKeeper help manage state and failover.

While robust, this design currently lacks a disaster recovery plan, which we will address in the next section.

- **Performance:** Performance is improved by selecting technologies based on workload characteristics. This includes adopting specialized datastores and multi-tier distributed caching layers. In addition, Kafka is used to enqueue asynchronous background tasks, decoupling long-running processing from the synchronous API request path.
- **Precision of duplicate suggestions:** Candidate retrieval uses both keyword and vector search, and only pairs that the equivalence classifier scores above a strict threshold are suggested. Merges require confirmation and can be reversed. Posting does not wait on the duplicate-detection service, so a slow or unavailable service only removes suggestions.

## Non-Functional Requirements Compliance

|  |  |
| --- | --- |
| **Requirements** | **Techniques** |
| Scalability | - Is based on AWS, which supports automatic scaling. - Uses the same servers to reduce complexity in horizontal scalability and sharding of the MySQL database. - Employs various data stores for different purposes. - Asynq can enable developers to code quickly by batching cache requests, - Separate compute and feature extraction modules. Therefore, a generic feature extraction facility allows scalability of different recommendation systems. |
| Consistency | - Uses MySQL and synchronous replication within a data center for critical data. - Offers eventual consistency for non-critical data like the view counter. |
| Availability | - Use of different data stores prevents failure of multiple services at once by using database sharding and replicas. - Uses CDN as a backup to serve static/dynamic data in case of failures. - ZooKeeper enables service hosts to get updates about MySQL shards. - Load balancers hide server failures from end users. - AWS supports an availability above 99 percent. - Thrift isolates services and therefore failures. - Posting continues without suggestions if the duplicate-detection service is slow or unavailable. |
| Performance | - MyRocks has a much lower P99 latency. - Uses the right programming language to deliver tasks quickly, such as C++ for the routing library. - Uses `Multiget()`  to retrieve multiple entries from Memcached at once. - Eliminates network round trip time with Asynq. - Kafka improves the performance of service hosts. - Sharding improves QPS of MySQL. - Custom, in-memory caching system reduces the latency of frequently accessed data. - Indexes new and edited questions asynchronously through Kafka, off the posting path. |
| Precision | - Uses two-stage detection: similarity search narrows millions of questions to a few candidates, and an equivalence classifier decides whether they ask the same thing. - Shows only suggestions whose classifier confidence exceeds a strict threshold, favoring precision over coverage. - Merges duplicates only after a user or moderator confirms them. - Records each merge in MySQL with enough history to reverse it. |

## Disaster recovery[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Disaster-recovery)

The proposed design does not yet account for natural disasters. To ensure durability and fault tolerance during catastrophic events, we need a disaster recovery (DR) strategy.

The primary strategy is frequent backups. Given the data size, daily backups of individual datastores and shards are appropriate. These backups must be stored in a remote location to survive facility-level failures.

> **Note:** A DR plan requires more than just backups; it must also ensure timely data restoration.

Key questions for designing a DR plan include:

- Which data and systems are critical for recovery?
- How fast can we restore from the backup facility?
- Can all systems be fully recovered from backups?
- How do we handle data created between the last backup and the disaster?

The following illustration depicts a basic disaster recovery architecture:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27601%27%20height=%27538%27/%3e)![Disaster recovery management](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Disaster recovery management")

Disaster recovery management

This approach backs up data, application servers, and configurations to Amazon S3 in the primary zone. Zonal replication then copies this data to a secondary zone. In the event of a disaster, services are restored using the backups in the secondary zone.

While effective, this strategy has drawbacks:

- **Data loss:** Daily backups leave a gap where data created since the last backup is lost. Synchronous cross-region replication can mitigate this.
- **Downtime:** Restoration can take hours, during which the system cannot serve queries.

> **Note:** Amazon S3 offers high reliability, with 99.999999999% durability and 99.9% availability.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Conclusion)

We have explored how Quora scales to accommodate user growth, highlighting techniques such as MySQL vertical sharding. The design employs various strategies to meet functional and non-functional requirements. Beyond the core architecture, the design adds AI-powered duplicate question detection. It excludes other NLP features, such as spell-checking and typeahead search.

1.

How can using different data stores for different types of data be beneficial in disaster recovery?

Show Answer

Did you find this helpful?

Final Design of Quora

System Design: Google Maps

Ask

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Requirements-compliance)

[Disaster recovery](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Disaster-recovery)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-quoras-design#Conclusion)