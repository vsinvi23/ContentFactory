# Background_of_Distributed_Cache

Source: https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Background of Distributed Cache

Define the core concepts for designing a high-performance distributed cache. Analyze various writing policies, such as write-through and write-back, alongside common eviction algorithms like LRU. Learn how to apply consistent hashing and sharding to ensure scalability and reliability in distributed System Design.

We'll cover the following...

- [Writing policies](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Writing-policies)
- [Eviction policies](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Eviction-policies)
- [Cache invalidation](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-invalidation)
- [Storage mechanism](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Storage-mechanism)
  - [Hash function](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Hash-function)
  - [Linked list](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Linked-list)
- [Sharding in cache clusters](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Sharding-in-cache-clusters)
  - [Dedicated cache servers](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Dedicated-cache-servers)
  - [Co-located cache](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Co-located-cache)
- [Cache client](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-client)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Conclusion)

This chapter explains the design of a distributed cache. First, it is important to understand core concepts such as data write policies, eviction strategies, and cache invalidation. The following prerequisites are covered:

|  |  |
| --- | --- |
| **Section** | **Motivation** |
| **Writing policies** | Data is written to cache and databases. The order in which data writing happens has performance implications. We’ll discuss various writing policies to help decide which writing policy would be suitable for the distributed cache we want to design. |
| **Eviction policies** | Since the cache is built on limited storage (RAM), we ideally want to keep the most frequently accessed data in the cache. Therefore, we’ll discuss different eviction policies to replace less frequently accessed data with most frequently accessed data. |
| **Cache invalidation** | Certain cached data may get outdated. We’ll discuss different invalidation methods to remove stale or outdated entries from the cache in this section. |
| **Storage mechanism** | A distributed storage has many servers. We’ll discuss important design considerations, such as which cache entry should be stored in which server and what data structure to use for storage. |
| **Cache client** | A cache server stores cache entries, but a cache client calls the cache server to request data. We’ll discuss the details of a cache client library in this section. |

## Writing policies[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Writing-policies)

A cache stores a temporary copy of data that is persistently stored in a database or another datastore. A key design decision is when to write data to the cache versus the database. This choice, known as the write policy, directly affects performance and data consistency.

There are three common writing policies:

- **Write-through:** Data is written to the cache and the database in the same operation. This approach ensures strong consistency between the cache and the database, but increases write latency because the operation is only complete after both writes succeed.
- **Write-back:** Data is written to the cache first, then to the storage. The write to the database happens later, asynchronously. This results in low write latency but introduces the risk of data loss if the cache fails before the data is persisted to the database. It can also lead to temporary inconsistency.
- **Write-around:** Data is written directly to the database, bypassing the cache. Data is loaded into the cache only on a subsequent read miss. This is useful for applications that don’t immediately re-read recently written data, as it avoids filling the cache with potentially unused items.

Quiz

1.

A system wants to write data and promptly read it back. At the same time, we want consistency between the cache and the database. Which writing policy is the optimal choice?

A.

Write-through cache

B.

Write-around cache

C.

Write-back cache

---

1 / 3

## Eviction policies[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Eviction-policies)

Caches are fast because they use high-speed memory, which is expensive and therefore limited in size. When the cache is full, an eviction policy decides which items to remove to make space for new ones.

Common eviction strategies include:

- Least recently used (LRU)
- Most recently used (MRU)
- Least frequently used (LFU)
- Most frequently used (MFU)

Other strategies, like first in, first out (FIFO), also exist. The choice of algorithm depends on the application’s access patterns.

## Cache invalidation[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-invalidation)

Data in the cache can become stale if the original data in the database changes. Invalidating or deleting this stale data is crucial for maintaining consistency.

A common way to handle stale data is to assign a time-to-live (TTL) to each cache entry. Once the TTL expires, the entry is considered invalid.

There are two approaches for handling TTL expiration:

- **Active expiration:** A background process periodically scans the cache and removes expired items.
- **Passive expiration:** An item’s TTL is checked only when it is requested. If it has expired, it is removed, and a cache miss is triggered.

Expired items are removed from the cache upon discovery.

## Storage mechanism[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Storage-mechanism)

In a distributed cache with multiple servers, we must decide where and how to store data. Two key questions are:

- Which server should store a particular piece of data?
- What data structure should be used to store data within each server?

The answers to these questions determine the performance of the cache.

### Hash function[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Hash-function)

Hashing is used in two scenarios:

- To identify which cache server should store or retrieve a piece of data.
- To locate a cache entry inside a specific cache server.

For distributing data across servers, consistent hashing is preferred. With simple hashing (like `server = hash(key) % N`), adding or removing a server (`N`) forces a remapping of almost all keys, causing a massive cache invalidation event. Consistent hashing minimizes remappings, making it ideal for scalable, fault-tolerant systems.

While a hash function maps a key to a server and a location, it doesn’t manage the data itself. For that, we need appropriate data structures to implement policies like LRU eviction.

AI Powered

Saved

1 attempt left

Reset

Why do we prefer consistent hashing?

Explain why consistent hashing is preferred over simple hashing in distributed cache systems and how it improves scalability and fault tolerance.

This is your last attempt.

### Linked list[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Linked-list)

We’ll use a doubly linked list. The main reason is its widespread usage and simplicity. Furthermore, adding and removing data from the doubly linked list, in our case, will be a constant-time operation. This is because we either evict a specific entry from the tail of the linked list or relocate an entry to the head of the doubly linked list. Therefore, no iterations are required.

> **Note:** [Bloom filters](https://www.educative.io/answers/what-is-a-bloom-filter) are an interesting choice for quickly finding if a cache entry doesn’t exist in the cache servers. We can use bloom filters to determine that a cache entry is definitely not present in the cache server, but the possibility of its presence is probabilistic. Bloom filters are quite useful in large caching or database systems.

## Sharding in cache clusters[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Sharding-in-cache-clusters)

To improve scalability and avoid a single point of failure (SPOF), we shard the cache data across multiple servers. There are two primary ways to organize these servers.

### Dedicated cache servers[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Dedicated-cache-servers)

In this model, the cache servers are separated from the application servers.

Advantages of this approach include:

- Flexibility to choose different hardware for application and cache needs.
- Ability to scale the application and cache tiers independently.

This model also enables a “Cache as a Service” architecture, where multiple services can use the shared cache cluster. The system must use key namespacing to prevent data collisions between different applications.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27535%27%20height=%27345%27/%3e)![A depiction of service hosts coordinating with dedicated cache servers](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A depiction of service hosts coordinating with dedicated cache servers")

A depiction of service hosts coordinating with dedicated cache servers

### Co-located cache[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Co-located-cache)

A co-located cache runs on the same servers as the application. This approach can reduce infrastructure costs (CAPEX and OPEX). As the application scales, cache capacity increases automatically. The main drawback is resource contention between the application and the cache process. Additionally, a server failure affects both the application instance and its local cache data.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27525%27%20height=%27340%27/%3e)![Hosting cache and application logic in the same machine](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Hosting cache and application logic in the same machine")

Hosting cache and application logic in the same machine

## Cache client[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-client)

A **cache client** is a library integrated into the application servers. Its primary job is to handle the logic for storing and retrieving data from the correct cache server, which includes performing hash calculations.

All clients must use the same hashing algorithm and server list. This ensures that a PUT operation for a given key is directed to the same server as a GET for that same key. Cache clients may also coordinate with other components, like monitoring and configuration services.

Key characteristics of cache clients include:

- Each client knows the address of all available cache servers.
- Clients use standard network protocols like TCP or UDP to communicate with cache servers.

1.

What is the behavior of cache clients to an access request if one of the cache servers is dead?

Show Answer

Did you find this helpful?

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Conclusion)

This lesson covered the core concepts for designing a distributed cache, including writing policies, eviction strategies, and sharding techniques. Understanding these trade-offs is essential for building high-performance, scalable systems.

System Design: The Distributed Cache

High-Level Design of a Distributed Cache

Ask

[Writing policies](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Writing-policies)

[Eviction policies](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Eviction-policies)

[Cache invalidation](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-invalidation)

[Storage mechanism](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Storage-mechanism)

[Hash function](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Hash-function)

[Linked list](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Linked-list)

[Sharding in cache clusters](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Sharding-in-cache-clusters)

[Dedicated cache servers](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Dedicated-cache-servers)

[Co-located cache](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Co-located-cache)

[Cache client](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Cache-client)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/background-of-distributed-cache#Conclusion)