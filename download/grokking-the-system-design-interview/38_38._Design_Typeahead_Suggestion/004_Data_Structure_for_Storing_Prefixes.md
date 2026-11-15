# Data_Structure_for_Storing_Prefixes

Source: https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Data Structure for Storing Prefixes

Define the optimal data structure for storing prefixes in a high-performance typeahead system. Learn how to use the trie to store search frequencies for ranking suggestions. Explore methods for partitioning and updating the Trie offline to achieve massive scalability and maintain low-latency reads in System Design.

We'll cover the following...

- [The trie data structure](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#The-trie-data-structure)
  - [Track the top searches](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Track-the-top-searches)
  - [Trie partitioning](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Trie-partitioning)
    - [Process a query after partitioning](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Process-a-query-after-partitioning)
  - [Update the trie](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Update-the-trie)

## The trie data structure[#](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#The-trie-data-structure)

Use a data structure optimized for prefix lookups. The service must match user input against a large set of strings to return query completions. For example, given the terms “UNITED”, “UNIQUE”, “UNIVERSAL”, and “UNIVERSITY”, typing “UNIV” should return “UNIVERSAL” and “UNIVERSITY” as prefix matches.

To handle high request volumes with minimal latency, we cannot rely on standard database queries. Reading from a database is much slower than reading from RAM. Therefore, we must store the index in memory. However, the data persists in the database for durability.

A trie (pronounced “try”) is commonly used for this purpose. A **trie** is a tree structure where each node stores a character of a string. The example words are stored in the trie as follows:

The trie for UNITED, UNIQUE, UNIVERSAL, and UNIVERSITY

When a user types “UNIV,” the service traverses the trie to the node `V`. It then identifies all terms starting with that prefix, such as `UNIVERSAL` and `UNIVERSITY`.

We can optimize the trie by merging nodes with a single branch. This reduces tree depth and traversal time. The following model illustrates a space- and time-efficient version of the trie:

A reduced Trie for UNITED, UNIQUE, UNIVERSAL, and UNIVERSITY

Let’s test your understanding with the help of an AI assessment:

AI Powered

Saved

1 attempt left

Reset

Trie for Applications

Can a trie be used for approximate matches or spelling corrections? How?

This is your last attempt.

### Track the top searches[#](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Track-the-top-searches)

To return the most relevant suggestions, we track search frequencies. We store the count of how many times a term is searched in its corresponding terminal node. For example, if users search `UNITED` 15 times, `UNIQUE` 20 times, `UNIVERSAL` 21 times, and `UNIVERSITY` 25 times, these counts are stored at the end of each path. The resulting trie looks like this:

A trie showing the search frequency for UNITED, UNIQUE, UNIVERSAL, and UNIVERSITY

If a user types “UNI,” the system traverses to the `UNI` node and identifies all descendants. It ranks suggestions by frequency; `UNIVERSITY` appears at the top because it has the highest count, while `UNITED` appears last. If the user selects `UNIQUE`, the system increments its count to 21.

1.

We reduced the time to traverse the trie by combining nodes with single branches and reducing the number of levels. Is there any other way to minimize the trie traversal time?

Show Answer

Did you find this helpful?

### Trie partitioning[#](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Trie-partitioning)

A single server cannot handle billions of daily queries or store all prefixes in memory. To ensure scalability, availability, and durability, we must split the trie across multiple servers.

The trie can be partitioned by prefix ranges. For example, one server stores prefixes starting with “A” through “M,” while another stores prefixes starting with “N” through “Z.” Each server maintains a replica for durability. However, simple range partitioning can lead to unbalanced load because some prefixes occur far more frequently than others.

We can split the trie into as many parts as necessary to distribute the load and achieve the desired performance.

## Partitioned Trie

|  |  |  |
| --- | --- | --- |
| **Prefixes** | **Primary** | **Secondary** |
| A to M | Server/01 | Server/02 |
| N to Z | Server/03 | Server/04 |

1.

Where will the mapping between the prefixes and their primary and secondary storage be stored? Who will manage and direct the requests to these servers?

Show Answer

Did you find this helpful?

#### Process a query after partitioning[#](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Process-a-query-after-partitioning)

Incoming queries hit a load balancer, which forwards them to an application server. The server routes the request to the appropriate trie shard based on the prefix. For instance, a query starting with “U” is routed to either Server/03 or Server/04, as both host the “N-Z” range.

### Update the trie[#](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Update-the-trie)

Updating the trie in real-time for every query is resource-intensive and slows down read requests. Instead, we update the trie offline. We log queries and their frequencies to a hash table, aggregate the data at regular intervals, and then update the trie. Once updated, we clear the previous entries from the hash table.

## Prefixes and Their Frequencies Updated Periodically

|  |  |  |
| --- | --- | --- |
| **Prefix** | **Time Interval (One Hour)** | **Frequency** |
| UNIVERSITY | 1st hour | 25 |
| UNIVERSITY | 2nd hour | 60 |
| UNIVERSITY | 3rd hour | 100 |

A **MapReduce (MR)** job processes the logs periodically (e.g., every 15 minutes). It calculates phrase frequencies and stores the results in a database such as Cassandra. We then update the trie with this new data. This offline process ensures users receive fast suggestions without waiting for real-time write operations.

1.

If the prefix frequencies keep increasing over time, the corresponding integers storing them can overflow. How can we manage this issue?

Show Answer

Did you find this helpful?

We can update the trie using one of two approaches:

- **Replica replacement:** Create a copy of the trie on each server, update it offline, and then switch traffic to the new version, discarding the old one.
- **Primary-secondary swap:** Maintain a primary copy for traffic and a secondary copy for updates. After updating the secondary, swap roles so it becomes the primary. The previous primary can then be updated.

AI Powered

Saved

3 attempts left

Reset

Storing search frequencies

What are the trade-offs of storing search frequencies in the trie nodes?

You have 3 attempts to answer.

In the next lesson, we’ll discuss the detailed design of the typeahead suggestion system.

High-Level Design of the Typeahead Suggestion System

Detailed Design of the Typeahead Suggestion System

Ask

[The trie data structure](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#The-trie-data-structure)

[Track the top searches](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Track-the-top-searches)

[Trie partitioning](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Trie-partitioning)

[Process a query after partitioning](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Process-a-query-after-partitioning)

[Update the trie](https://www.educative.io/courses/grokking-the-system-design-interview/data-structure-for-storing-prefixes#Update-the-trie)