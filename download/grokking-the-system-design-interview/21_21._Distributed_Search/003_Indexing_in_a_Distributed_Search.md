# Indexing_in_a_Distributed_Search

Source: https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Indexing in a Distributed Search

Discover the role of indexing in distributed search, focusing on the Inverted Index structure for fast information retrieval. Evaluate the design trade-offs and understand why centralized indexing systems cannot scale to handle massive data sets.

We'll cover the following...

- [Indexing](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing)
  - [Build a searchable index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Build-a-searchable-index)
    - [Inverted index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Inverted-index)
    - [Searching from an inverted index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Searching-from-an-inverted-index)
  - [Factors of index design](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Factors-of-index-design)
- [Indexing on a centralized system](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing-on-a-centralized-system)

This lesson explores the mechanics of indexing and the transition from centralized to distributed architectures.

## Indexing[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing)

**Indexing** organizes data to facilitate fast and accurate information retrieval.

### Build a searchable index[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Build-a-searchable-index)

A basic approach assigns a unique ID to each document and stores the text in a database table (a forward index). The first column holds the document ID, and the second contains the text.

## Simple Document Index

|  |  |
| --- | --- |
| **ID** | **Document Content** |
| 1 | Elasticsearch is the distributed and analytics engine that is based on REST APIs. |
| 2 | Elasticsearch is a Lucene library-based search engine. |
| 3 | Elasticsearch is a distributed search and analytics engine built on Apache Lucene. |

In production, documents are significantly larger than single sentences. Storing full text in a table creates a massive dataset. Searching this *document-level index* is slow because the system must scan every document to count occurrences of the search string.

> **Note:** A **fuzzy search** adds complexity. The system must identify unique candidate strings across all documents, determine approximate matches, and locate them, significantly increasing latency.

Search query response time depends on:

- Data organization strategy
- Data volume
- Hardware resources (processing speed and RAM)

Scanning billions of documents in a document-level index is inefficient. To reduce search time, we use an inverted index.

#### Inverted index[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Inverted-index)

An **inverted index** is a HashMap-like structure that maps terms to documents. It parses documents into individual words, creating a **document-term matrix**. It identifies unique words and discards frequent **stop words** (e.g., “the”, “is”) to create a compact **term-level index**.

AI Powered

Saved

3 attempts left

Reset

Trade-off for Removing Stop Words

If stop words are removed to shrink the index for storage and performance improvement, what design tradeoff does that reveal about search behavior?

You have 3 attempts to answer.

For each term, the index stores:

- A list of documents containing the term.
- The frequency of the term in each document.
- The position of the term in each document.

## Inverted Index

|  |  |
| --- | --- |
| **Term** | **Mapping**  **( [doc], [freq], [[loc])** |
| elasticsearch | ( [1, 2, 3], [1, 1, 1], [[1], [1], [1]] ) |
| distributed | ( [1, 3], [1, 1], [[4], [4]] ) |
| restful | ( [1], [1], [[5]] ) |
| search | ( [1, 2, 3], [1, 1, 1], [[6], [4], [5]] ) |
| analytics | ( [1, 3], [1, 1], [[8], [7]] ) |
| engine | ( [1, 2, 3], [1, 1, 1], [[9], [5], [8]] ) |
| heart | ( [1], [1], [[12]] ) |
| elastic | ( [1], [1], [[15]] ) |
| stack | ( [1], [1], [[16]] ) |
| lucene | ( [2, 3], [1, 1], [[9], [12]] ) |
| library | ( [2], [1], [[10]] ) |
| Apache | ( [3], [1], [[11]] ) |

The “Mapping” column in the index contains three lists for each unique term:

- Documents where the term appears.
- Frequency of the term in each document.
- A two-dimensional list pinpointing the term’s position in each document (handling multiple occurrences).

> **Note:** Mappings can also use tuples, such as (`doc`, `freq`, `loc`).

The **inverted index** is the standard for document retrieval. It enables efficient boolean, extended boolean, proximity, and relevance searches.

**Advantages:**

- Facilitates full-text searches.
- Reduces runtime by pre-calculating term occurrences.

**Disadvantages:**

- **Storage overhead** requires maintaining the index alongside actual documents.
- **Maintenance costs** are high. Adding, updating, or deleting documents requires processing terms and updating the index structure.

#### Searching from an inverted index[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Searching-from-an-inverted-index)

Consider a system containing the following mappings for the query search engine:

|  |  |
| --- | --- |
| **Term** | **Mapping** |
| search | ( [1, 2, 3], [1, 1, 1], [[6], [4], [5]] ) |
| engine | ( [1, 2, 3], [1, 1, 1], [[9], [5], [8]] ) |

Both terms appear in documents 1, 2, and 3:

- **search**: Document 1 (pos 6), Document 2 (pos 4), Document 3 (pos 5).
- **engine**: Document 1 (pos 9), Document 2 (pos 5), Document 3 (pos 8).

As a single term can appear in millions of documents, the result list for a query can be extensive.

1.

Would this technique work when too many documents are found against a single term?

Show Answer

Did you find this helpful?

### Factors of index design[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Factors-of-index-design)

Key factors in designing an index include:

- **Storage:** RAM and disk space required to store the index for low-latency access.
- **Search speed:** How quickly a term is located in the inverted index.
- **Maintenance:** Efficiency of updating the index when adding or removing documents.
- **Fault tolerance:** Coping with index corruption, handling invalid data in isolation, dealing with defective hardware, partitioning, and replication are all issues to consider here.
- **Resilience:** Resistance to manipulation, such as Search Engine Optimization (SEO) schemes.

These factors highlight specific challenges when building an index on a centralized system.

## Indexing on a centralized system[#](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing-on-a-centralized-system)

In a **centralized search system**, all components run on a single, high-performance node.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27831%27%20height=%27241%27/%3e)![The architecture of a centralized search system ](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The architecture of a centralized search system ")

The architecture of a centralized search system

- **Indexing process:** This takes documents as input and converts them into an inverted index, which is stored as a binary file.
- **Query process:** It interprets the binary file that contains the inverted index. It also computes the intersection of the inverted lists for a given query to return search results.

Centralized architectures face three primary limitations:

- **Single point of failure (SPOF):** If the central node fails, the entire search service becomes unavailable.
- **Server overload:** High query volume or complex requests can overwhelm the single node’s resources.
- **Index size:** As the document count grows, the index may exceed the storage and RAM capacity of a single server.

> **Note:** Distributed systems allow the use of cost-effective commodity hardware rather than expensive mainframes.

Efficient query processing requires keeping a large portion of the inverted index in memory. With hundreds of billions of web pages and petabytes of data, a single machine cannot store the full index in memory. This requires distributing the index across multiple machines to enable parallel query execution.

> **Note:** Search time increases with data volume. Searching a shelf of one million books takes significantly longer than searching a shelf of one hundred.

Centralized systems are also more vulnerable to attacks and hardware bottlenecks (such as bandwidth or RAM) than distributed alternatives.

This lesson covered the fundamentals of indexing and the limitations of centralized systems. The next lesson introduces distributed indexing solutions.

Requirements of a Distributed Search System's Design

Design of a Distributed Search

Ask

[Indexing](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing)

[Build a searchable index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Build-a-searchable-index)

[Inverted index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Inverted-index)

[Searching from an inverted index](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Searching-from-an-inverted-index)

[Factors of index design](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Factors-of-index-design)

[Indexing on a centralized system](https://www.educative.io/courses/grokking-the-system-design-interview/indexing-in-a-distributed-search#Indexing-on-a-centralized-system)