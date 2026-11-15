# Evaluation_of_a_Distributed_Cache's_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of a Distributed Cache's Design

Evaluate a distributed cache design by assessing its performance, scalability, and availability against defined requirements. Analyze how consistent hashing and eviction algorithms, like LRU, influence effective access time (EAT). Understand the critical trade-offs between strong consistency and high availability in distributed caching.

We'll cover the following...

- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Requirements-compliance)
  - [High performance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-performance)
  - [Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Scalability)
  - [High availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-availability)
  - [Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Consistency)
  - [Affordability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Affordability)
- [Summary](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Summary)

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Requirements-compliance)

Let’s evaluate the design against our requirements.

### High performance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-performance)

The following design choices contribute to high performance:

- Consistent hashing locates keys in O(log N)\text{O(log N)}O(log N) time, where N\text{N}N is the number of cache shards.
- Internal hash tables locate keys in constant time on average.
- LRU eviction accesses and updates doubly linked list entries in constant time.
- TCP and UDP protocols ensure fast client-server communication.
- Replicas distribute traffic, preventing performance degradation from high loads on a single machine.
- Serving data directly from RAM ensures low latency.

> **Note:** The eviction algorithm is critical for performance. A higher cache hit rate directly reduces latency.

To illustrate the impact of the eviction algorithm, consider the following assumptions:

- Cache hit service time (99.9th\text{99.9}^\text{{th}}99.9th percentile): 5 ms
- Cache miss service time (99.9th\text{99.9}^\text{{th}}99.9th percentile): 30 ms (includes database retrieval and cache update)

Assume a 10% miss rate for the Most Frequently Used (MFU) algorithm and a 5% miss rate for LRU. We calculate the Effective Access Time (EAT) as follows:

EAT = Ratiohit×Timehit+Ratiomiss×Timemiss\text{EAT = Ratio}\_{\text{hit}} \times \text{Time}\_{\text{hit}} + \text{Ratio}\_{\text{miss}} \times \text{Time}\_{\text{miss}}
EAT = Ratiohit​×Timehit​+Ratiomiss​×Timemiss​

Where:

EAT:\text{EAT:}EAT: Effective access time.

Ratiohit:\text{Ratio}\_{\text{hit}}:Ratiohit​: The probability of a cache hit.

Ratiomiss:\text{Ratio}\_{\text{miss}}:Ratiomiss​: The probability of a cache miss.

Timehit:\text{Time}\_{\text{hit}}:Timehit​: Time required to serve a cache hit.

Timemiss: \text{Time}\_{\text{miss}}:Timemiss​: Time required to serve a cache miss.

For MFU, we see the following:

Ace Editor

1

EAT = 0.90 x 5 milliseconds + 0.10 x 30 milliseconds = 0.0045 + 0.003 = 0.0075 = 7.5 milliseconds

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

For LRU, we see the following:

Ace Editor

1

EAT = 0.95 x 5 milliseconds + 0.05 x 30 milliseconds = 0.00475 + 0.0015 = 0.00625 = 6.25 milliseconds.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

These figures highlight how the eviction algorithm impacts the cache hit rate. You should conduct empirical studies to determine the best algorithm for your specific workload.

### Scalability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Scalability)

Sharding is used to distribute load as traffic patterns change. Consistent hashing minimizes the amount of data that must be rehashed when new cache servers are added. Replica nodes help distribute read load across hot shards. In rare cases, a single hot key can create contention. This issue can be mitigated by further sharding within the key range or by using client-side techniques such as dynamic replication. However, these approaches are beyond the scope of this lesson.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27501%27%20height=%27351%27/%3e)![Guarantees provided by a distributed cache](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Guarantees provided by a distributed cache")

Guarantees provided by a distributed cache

### High availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-availability)

Redundant cache servers and leader–follower replication improve system reliability and fault tolerance. However, if all replicas reside in a single data center, the system remains vulnerable to a data center failure. Distributing replicas across multiple data centers improves availability but introduces consistency challenges. Synchronous writes across data centers introduce high latency. Therefore, caching systems typically rely on asynchronous replication for cross–data center deployments.

We can achieve strong consistency within a single data center, but we often compromise consistency across data centers to improve availability (see CAP and PACELC theorems).

### Consistency[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Consistency)

Caching systems favor asynchronous writes for performance, which results in eventual consistency. Synchronous writes ensure strong consistency but increase latency.

Inconsistencies also arise during failures. For example, a server recovering after a write operation might hold stale data. To prevent this, a rejoining server should not serve requests until it is fully synchronized.

### Affordability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Affordability)

The design is cost-effective because it utilizes commodity hardware.

1.

What happens if the leader node fails in the leader-follower protocol?

Show Answer

1 / 3

## Summary[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Summary)

This design presents a distributed cache that balances availability, performance, scalability, and cost. Although replicas improve availability, a single–data center deployment remains vulnerable to site-wide failures. The next section examines open-source frameworks such as Memcached and Redis.

Detailed Design of a Distributed Cache

Memcached versus Redis

Ask

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Requirements-compliance)

[High performance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-performance)

[Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Scalability)

[High availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#High-availability)

[Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Consistency)

[Affordability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Affordability)

[Summary](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-a-distributed-caches-design#Summary)