# Design_of_a_Key-Value_Store

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design of a Key-Value Store

Define the functional and non-functional requirements essential for designing a highly available key-value store. Analyze how needs like configurable consistency and always-write capability influence System Design decisions. Understand the simple get and put operations that enables complex distributed storage.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Requirements)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Functional-requirements)
  - [Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Non-functional-requirements)
- [Assumptions](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Assumptions)
- [API design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#API-design)
  - [Data type](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Data-type)

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Requirements)

We will design a key-value store that addresses the limitations of traditional databases.

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Functional-requirements)

While standard key-value stores offer `get` and `put` operations, this design focuses on specific characteristics:

- **Configurable service:** Applications often trade strong consistency for higher availability. The system must support configurable consistency models that allow users to balance availability, consistency, cost, and performance.

> **Note:** These configurations are set when instantiating a key-value store instance and cannot be changed dynamically during operation.

- **Ability to always write:** Applications must always be able to write to storage. This prioritizes availability over consistency (choosing “A” over “C” in the CAP theorem).

> **Note:** Whether a requirement is classified as functional or non-functional depends on context. For example, in a shopping cart system, the ability to accept writes at all times (high availability) can be treated as a non-functional requirement. Following the Dynamo design principles, we treat “always write” as a functional requirement in this context.

- **Hardware heterogeneity:** The system must seamlessly integrate new servers with different capacities without upgrading existing ones. Workload distribution should align with server capacity, favoring a peer-to-peer design without distinguished nodes.

### Non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Non-functional-requirements)

The system must meet the following non-functional requirements:

- **Scalability:** The system must support tens of thousands of servers globally. Incremental scalability is essential, allowing servers to be added or removed with minimal service disruption.
- **Fault tolerance:** The system must operate uninterrupted despite server or component failures.

AI Powered

Saved

1 attempt left

Reset

Differences between key-value stores and traditional databases

Now that you understand the functional and non-functional requirements of a key-value store, what do you think are the key differences between key-value stores and traditional databases? In what scenarios are key-value stores particularly advantageous?

This is your last attempt.

## Assumptions[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Assumptions)

We make the following assumptions to simplify the design:

- Data centers hosting the service are trusted (non-hostile).
- Authentication and authorization are handled externally.
- User requests and responses use HTTPS.

## API design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#API-design)

Like hash tables, key-value stores provide two primary operations: `get` and `put`.

**The** **`get`** **function:**

The API call to get a value should look like this:

Ace Editor

1

get(key)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Returns the value associated with `key`. In replicated environments, the system locates the object replica hidden from the user. If configured for weaker consistency (e.g., eventual consistency), the system may return multiple values (versions) for a single key.

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `key` | It’s the `key` against which we want to get `value`. |

**The** **`put`** **function:**

The API call to put the value into the system should look like this:

Ace Editor

1

put(key, value)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Stores the `value` associated with `key`. The system automatically determines data placement and maintains metadata, such as the object version.

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `key` | It's the `key` against which we have to store `value`. |
| `value` | It's the object to be stored against the `key`. |

AI Powered

Saved

1 attempt left

Reset

Best practice for data integrity checks

When performing data integrity checks, we often store hashes of values (and sometimes values along with their associated key) as metadata. Should these hashes be generated before or after data compression or encryption, and why?

This is your last attempt.

### Data type[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Data-type)

The `key` serves as the unique identifier, while the `value` can be any arbitrary binary data.

> **Note:** Dynamo uses MD5 hashes to generate a 128-bit identifier for the key. These identifiers determine which server node is responsible for the specific key.

The next lesson covers the key-value store design, with an emphasis on scalability, replication, and versioning. We start with non-functional requirements, since the chosen scalability strategy shapes how functional requirements are implemented.

> **Note:** This chapter is based on Dynamo, an influential work in the domain of key-value stores.

System Design: The Key-Value Store

Ensure Scalability and Replication

Ask

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Functional-requirements)

[Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Non-functional-requirements)

[Assumptions](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Assumptions)

[API design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#API-design)

[Data type](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-key-value-store#Data-type)