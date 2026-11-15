# Detailed_Design_of_a_Distributed_Cache

Source: https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Detailed Design of a Distributed Cache

Discover how to refine a distributed cache design by eliminating single points of failure and improving availability. Implement a configuration service for server discovery and use primary-replica sharding to ensure data consistency. Learn the internal workings of cache servers, including hash maps and LRU eviction policies.

We'll cover the following...

- [Find and remove limitations](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Find-and-remove-limitations)
  - [Maintain the cache servers list](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Maintain-the-cache-servers-list)
  - [Improve availability](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Improve-availability)
  - [Internals of the cache server](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Internals-of-the-cache-server)
- [Detailed design](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Detailed-design)

This lesson identifies limitations in the high-level design and refines the architecture to address them.

## Find and remove limitations[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Find-and-remove-limitations)

Before we get to the detailed design, we must resolve three specific challenges:

- **Service discovery:** Cache clients have no mechanism to detect when cache servers are added or fail.
- **SPOF and performance:** Using a single server for a dataset creates a Single Point of Failure (SPOF). Additionally, frequently accessed data (hotkeys) can overload a single node, degrading performance.
- **Server internals:** The design lacks details regarding internal data structures and eviction policies.

### Maintain the cache servers list[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Maintain-the-cache-servers-list)

We will address the service discovery problem first. The following slides illustrate three potential strategies:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27622.2%27%20height=%27351.9000000000001%27/%3e)![[Solution 1] Maintaining a configuration file in each server that the cache client can use](https://www.educative.io/api/collection/10370001/4941429335392256/page/4731033765543936/image/5913875813826560?page_type=collection_lesson&get_optimised=true&slide_id=4945533628121088&collection_token=vxC7RH00gFj9nkl254oZpx "[Solution 1] Maintaining a configuration file in each server that the cache client can use")

1 / 3

[Solution 1] Maintaining a configuration file in each server that the cache client can use

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27622.2%27%20height=%27351.9000000000001%27/%3e)![[Solution 2] Maintaining a configuration file on a centralized location](https://www.educative.io/api/collection/10370001/4941429335392256/page/4731033765543936/image/6313687809851392?page_type=collection_lesson&get_optimised=true&slide_id=4945533628121088&collection_token=vxC7RH00gFj9nkl254oZpx "[Solution 2] Maintaining a configuration file on a centralized location")

1 / 3

[Solution 2] Maintaining a configuration file on a centralized location

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27622.2%27%20height=%27351.9000000000001%27/%3e)![[Solution 3] Using a configuration service to monitor cache servers and keep the  cache clients updated](https://www.educative.io/api/collection/10370001/4941429335392256/page/4731033765543936/image/6181724503474176?page_type=collection_lesson&get_optimised=true&slide_id=4945533628121088&collection_token=vxC7RH00gFj9nkl254oZpx "[Solution 3] Using a configuration service to monitor cache servers and keep the  cache clients updated")

1 / 3

[Solution 3] Using a configuration service to monitor cache servers and keep the cache clients updated

- **Solution 1 (local configuration):** A configuration file resides on each service host. This file contains server metadata and health status. Updates require a push service or DevOps tool to deploy changes to every host. The drawback in this approach is that updates are manual and operationally slow.
- **Solution 2 (centralized configuration):** We store the configuration file in a central location accessible to all clients. This simplifies deployment, but still requires manual updates and external health monitoring.
- **Solution 3 (configuration service):** A dedicated service continuously monitors cache server health and automatically notifies clients when nodes are added or removed. This removes the need for human intervention.

> Although the configuration service is the most complex and expensive to operate, it is the most robust solution.

### Improve availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Improve-availability)

To reduce the risk of data unavailability during server failures, the system introduces replica nodes. A typical shard consists of one primary node and two replica nodes. To ensure consistency, writes are performed synchronously across replicas when nodes are located in close proximity. This approach provides two main benefits:

- **High availability:** The system remains operational if a primary node fails.
- **Read scalability:** Hot shards can distribute read traffic across both primary and secondary nodes.

This structure improves both reliability and performance.

### Internals of the cache server[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Internals-of-the-cache-server)

Cache servers use three mechanisms to store and manage data:

- **Hash map:** Stores pointers to cache values in RAM for fast lookup.
- **Doubly linked list:** Orders entries by access frequency. This allows the system to track usage for eviction.
- **Eviction policy:** Determines which data to remove when memory is full. We assume a least recently used (LRU) policy for this design.

The illustration below depicts a sharded cluster and the internal data structures:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27761%27%20height=%27266%27/%3e)![A shard primary and replica, each with the same internal mechanisms](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A shard primary and replica, each with the same internal mechanisms")

A shard primary and replica, each with the same internal mechanisms

> We generally do not expose a `delete` API because eviction (via algorithm) and expiration (via TTL) are handled locally. However, an explicit `delete` API is required to remove cache entries when the corresponding data is deleted from the database to ensure consistency.

AI Powered

Saved

12 attempts left

Reset

Distributed cache

Hi, I’m Ed. In this session, we will focus on some questions related to the distributed cache. Do you want to be mentored or evaluated?

You have 12 attempts to answer.

## Detailed design[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Detailed-design)

With these challenges resolved, we can formalize the detailed design:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27721%27%20height=%27664%27/%3e)![Detailed design of a distributed caching system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a distributed caching system")

Detailed design of a distributed caching system

The proposed design functions as follows:

- The client’s requests reach the service hosts through the load balancers, where the cache clients reside.
- Each cache client uses consistent hashing to determine which cache server to contact. Next, the cache client forwards the request to the cache server that maintains the specific shard.
- Each cache server has primary and replica servers. Internally, every server uses the same mechanisms to store and evict cache entries.
- The configuration service ensures that all clients see an up-to-date, consistent view of the cache servers.
- Monitoring services can also be used to log and report various metrics for the caching service.

> **Note:** An important aspect of the design is that cache entries are stored and retrieved from RAM. We discussed the suitability of RAM for designing a caching system in the previous lesson.

1.

While consistent hashing is a good choice, it may result in unequal distribution of data, and certain servers may get overloaded. How do we resolve this problem?

Show Answer

Did you find this helpful?

High-Level Design of a Distributed Cache

Evaluation of a Distributed Cache's Design

Ask

[Find and remove limitations](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Find-and-remove-limitations)

[Maintain the cache servers list](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Maintain-the-cache-servers-list)

[Improve availability](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Improve-availability)

[Internals of the cache server](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Internals-of-the-cache-server)

[Detailed design](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-a-distributed-cache#Detailed-design)