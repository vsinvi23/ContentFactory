# Introduction_to_the_LeetCode_System

Source: https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Introduction to the LeetCode System

Explore the LeetCode system, its features, and the essential requirements for its design.

We'll cover the following...

- [Introduction](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Introduction)
- [Requirements of LeetCode’s design](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Requirements-of-LeetCodes-design)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Bandwidth-estimation)
  - [Estimating the number of servers](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Estimating-the-number-of-servers)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Building-blocks-we-will-use)

## Introduction[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Introduction)

LeetCode is an online problem-solving platform that focuses on algorithm and data structure challenges, expressed as precise computational problems with well-defined input–output behavior. At a technical level, it can be viewed as a curated set of problem specifications paired with automated evaluation logic. Each problem defines constraints, edge cases, and expected behavior, enabling consistent and deterministic validation of solutions across multiple programming languages.

From a System Design perspective, LeetCode operates as a distributed code execution and grading platform. Its core features include the ability to submit solutions in multiple programming languages, automated evaluation against visible and hidden test cases, and consistent enforcement of correctness, time, and memory constraints. Submissions are executed in isolated environments, and results are aggregated to provide deterministic feedback on correctness and performance. In this way, LeetCode serves as a practical reference for designing scalable, automated code assessment systems, rather than simply a collection of interview-style problems.

The following illustration shows the high-level workflow of a LeetCode-style system from problem selection to evaluation:

![High-level workflow of a LeetCode-style system](001_Introduction_to_the_LeetCode_System_images/img_831936521892.svg "High-level workflow of a LeetCode-style system")

High-level workflow of a LeetCode-style system

In practice, the platform supports browsing and solving coding problems by topic and difficulty, submitting solutions for automated evaluation, participating in time-bound contests with real-time leaderboards, and engaging in discussions about problems and solutions. It also maintains user history and performance metrics and offers premium features such as mock interviews and company-specific problem sets. Together, these capabilities define the functional surface area that the underlying system must support at scale.

In this chapter, we will focus on designing a system similar to LeetCode. Let’s start by identifying the requirements for such a system.

## Requirements of LeetCode’s design[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Requirements-of-LeetCodes-design)

Because LeetCode provides many features, its functional requirements are extensive. To keep this design problem focused, we’ll limit the scope to the following functional and nonfunctional requirements:

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Functional-requirements)

We will consider the following essential functional requirements for designing a LeetCode system:

- **List questions**: The system should allow users to browse practice problems by selecting a difficulty level or searching by topic.
- **Language support:** The system should support submitting and evaluating solutions written in multiple programming languages. Each supported language must have a corresponding execution environment with well-defined compiler or runtime configurations and consistent enforcement of time and memory limits.
- **Contest registration**: Users should be able to register for contests in which they wish to participate.
- **Submit code**: Users practicing or participating in contests should be able to submit one or multiple solutions for evaluation. The system must handle submission requests, evaluate code by running it in the relevant environment, and provide feedback.
- **Leaderboard**: A contest’s results should be displayed on a leaderboard. Participants must be able to fetch the leaderboard and analyze the results. The system should perform real-time evaluations of participants and update the leaderboard accordingly.
- **Interview**: The LeetCode service should allow both users and companies to conduct interviews. The system should handle such requests regardless of the number of users or companies involved.
- **Discussion:** The system should allow users to ask questions, provide answers, and share solutions with the community. The discussion feature should enable users to easily share code files.
- **History**: Users should be able to track their performance metrics, submitted solutions, and contest results. The system should efficiently process and store this data for easy retrieval.

![Functional and nonfunctional requirements for designing a LeetCode system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Functional and nonfunctional requirements for designing a LeetCode system")

Functional and nonfunctional requirements for designing a LeetCode system

### Nonfunctional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Nonfunctional-requirements)

Let’s consider the following nonfunctional requirements:

- **Availability:** LeetCode must ensure high availability to handle the thousands of submissions from contestants.
- **Scalability:** The system should be able to accommodate an increasing number of users.
- **Low latency:** The system should maintain low response times across core functionality, even during peak load, such as contests where many users submit code simultaneously. Code execution, plagiarism checks, and result generation must be optimized to minimize delays.
- **Resource constraints:** The system must enforce execution limits such as maximum runtime and memory usage for submitted code. Submissions that exceed these limits should be terminated and marked accordingly to ensure fair evaluation and protect system resources.
- **Consistency:** The system’s behavior must be reliable and predictable. The same code submitted for the same problem should always produce the same intended result, with evaluation criteria applied fairly to all submissions. Additionally, shared information, such as problem statements or leaderboards, should appear consistently for all users.
- **Security:** The system should prevent unauthorized access to infrastructure, services, and other users’ data. User-submitted code must execute in isolated environments with restricted permissions to ensure it cannot access internal systems, sensitive data, or other users’ execution contexts.

Designing a robust system requires careful consideration of resources, including storage, servers, and bandwidth, to ensure optimal performance and scalability. In the following section, let’s estimate these resources to better understand the system’s needs.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Resource-estimation)

To ensure smooth operation, the system must efficiently handle large volumes of code submissions and associated metadata. Let’s start with the storage estimation:

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Storage-estimation)

Let’s estimate the amount of storage required based on the following assumptions:

- The number of daily active users (DAUs): 10 million10 \ \text{million}10 million
- Average number of metadata records generated per user: 5 records per day5 \ \text{records per day}5 records per day
- Size of a single metadata record: 1 KB
- Size of a single code submission: 30 KB

Additionally, assume that a contest occurs once a day. On average, approximately 50,000 contestants out of 10 million participate. Each contestant submits five code drafts. The system will need to store the code files and metadata related to these submissions.

Since the system processes different kinds of data, such as contest submissions and metadata updates, we calculate total storage as follows:

Storagetotal=Storagecontest+Storagemetadata\text{Storage}\_{\text{total}} = \text{Storage}\_{\text{contest}}+\text{Storage}\_{\text{metadata}}Storagetotal​=Storagecontest​+Storagemetadata​

Each part of the above equation is expanded as follows:

Storage contest=Number of contestants×Submissionsper contestant×Submissionsize=50 K×5×30 KB=7.5 GB\begin{align\*}
\text { Storage }\_{\text{contest}} & = \text{Number of contestants} \times \text{Submissions}\_{\text{per}\ \text{contestant}}\times \text{Submission}\_{\text{size}} \\
& = \text{50 K} \times 5 \times \text{30 KB} \\
&= \text{7.5 GB}
\end{align\*} Storage contest​​=Number of contestants×Submissionsper contestant​×Submissionsize​=50 K×5×30 KB=7.5 GB​

Storage metadata=DAUs×Recordsper user×Recordsize=10 M×5×1 KB=50 GB\begin{align\*}
\text { Storage }\_{\text{metadata}} &= \text{DAUs} \times \text{Records}\_{\text{per}\ \text{user}}\times \text{Record}\_{\text{size}} \\
&=\text{10 M} \times 5 \times \text{1 KB} \\
&= \text{50 GB}
\end{align\*} Storage metadata​​=DAUs×Recordsper user​×Recordsize​=10 M×5×1 KB=50 GB​

Based on the previous calculation, the total storage is:

Storage total=Storagecontest+Storagemetadata=50 GB + 7.5 GB=57.5 GB\begin{align\*}
\text { Storage }\_{\text{total}} &= \text{Storage}\_{\text{contest}}+\text{Storage}\_{\text{metadata}}
\\ &= 50 \ \text{GB} \ + \ 7.5 \ \text{GB} \\ & =57.5\ \text{GB}
\end{align\*}
 Storage total​​=Storagecontest​+Storagemetadata​=50 GB + 7.5 GB=57.5 GB​

The following calculator computes the total amount of storage required per day:

#### Estimating Storage Requirements

|  |  |  |
| --- | --- | --- |
|  |  |  |
| Number of DAUs | 10 | million |
| Metadata records generated per user | 5 | records/day |
| Size of single record | 1 | KB |
| Amount of storage required for metadata | f50 | GB/day |
| Contestants | 50000 | contestants |
| Submissions per contestant | 5 | submissions/contestant |
| Storage required for a single submission | 30 | KB |
| Amount of storage required (contest) | f7.5 | GB |
| Total storage required (metadata+contest) | f57.5 | GB/day |

Approximately 57.5 GB of storage is required daily to store dynamic data, such as user activity and contest submissions. In addition, a non-dynamic storage allocation of about 10 GB (as an upper limit) is reserved for static data related to user registrations, problem statements, and their metadata.

This 10 GB estimate is based on roughly 10 million registered users, each requiring about 1 KB to store profile and registration information. The platform also maintains approximately 10,000 problems, with each problem’s data and metadata averaging around 10 KB.

**Note:** These figures are approximate and are intended as a starting point. Actual storage requirements may be more complex and could involve different storage technologies to handle diverse data types and future growth.

Now, let’s move on to the bandwidth estimation.

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Bandwidth-estimation)

The bandwidth estimate requires calculating incoming and outgoing data over the network:

- **Incoming traffic**: The incoming traffic bandwidth required per day will be equal to:

Incoming bandwidth= Incoming data sizeTotal seconds/day×8=57.5 GB86400×8≈6 Mbps\text{Incoming }\_{\text{bandwidth}} = \frac{ \text{ Incoming data size} }{\text{Total seconds}\_{/\text{day}}} \times 8 =\frac{57.5 \text{ GB}}{86400} \times 8 ≈ 6 \text{ Mbps}Incoming bandwidth​=Total seconds/day​ Incoming data size​×8=8640057.5 GB​×8≈6 Mbps

> **Note:** Incoming data size is the same as the total storage we calculated earlier, i.e., 57.5 GB.

- **Outgoing traffic:** Assuming each active user generates an average of five data-fetching requests per day (for example, loading problems or leaderboards), with an average response size of 10 KB, the outgoing data size can be computed as follows:

Outgoing data size/day=DAUs×Request/user×Single response size =10 M×5×10 KB=500 GBs\begin{align\*}
\text{Outgoing data size}\_\text{/day} &= \text{DAUs} \times \text{Request}\_{\text{/user}}\times \text{Single response size } \\
&=10 \text{ M} \times5\times10 \ \text{KB} \\
&= 500 \ \text{GBs}
\end{align\*}Outgoing data size/day​​=DAUs×Request/user​×Single response size =10 M×5×10 KB=500 GBs​

The average outgoing bandwidth required per day is therefore:

Outgoing bandwidth=Outgoing data size/dayTotal seconds/day×8=500 GB86400×8≈47 Mbps\text{Outgoing } \_{\text{bandwidth}} = \frac{\text{Outgoing data size}\_{/\text{day}}}{\text{Total seconds}\_{/\text{day}}} \times 8 =\frac{500\ \text{GB}}{86400} \times 8 ≈ 47\ \text{Mbps}Outgoing bandwidth​=Total seconds/day​Outgoing data size/day​​×8=86400500 GB​×8≈47 Mbps

Peak outgoingbandwidth=Concurrent users×Response size×8=10×106×10 KB×8=100 GB/s×8=800 Gbps\begin{align\*}
\text{Peak outgoing}\_{\text{bandwidth}}
&= \text{Concurrent users} \times \text{Response size} \times 8\\
&=10 \times 10^{6} \times 10\ \text{KB} \times 8\\
&=100\ \text{GB/s} \times 8 \\
&=800\ \text{Gbps}
\end{align\*}Peak outgoingbandwidth​​=Concurrent users×Response size×8=10×106×10 KB×8=100 GB/s×8=800 Gbps​

Peak incomingbandwidth=Concurrent users×Request size×8=10×106×1 KB×8=10 GB/s×8=80 Gbps\begin{align\*}
\text{Peak incoming}\_{\text{bandwidth}}
&= \text{Concurrent users} \times \text{Request size} \times 8\\
&=10 \times 10^{6} \times 1\ \text{KB} \times 8\\
&=10\ \text{GB/s} \times 8 \\
&=80\ \text{Gbps}
\end{align\*}
Peak incomingbandwidth​​=Concurrent users×Request size×8=10×106×1 KB×8=10 GB/s×8=80 Gbps​

#### Estimating Bandwidth Requirements

|  |  |  |
| --- | --- | --- |
| Incoming data size | 57.5 | GB/day |
| Incoming bandwidth | f6 | Mbps |
| Number of DAUs | 10 | million |
| Data fetching request | 5 | request/day |
| Size of a single response | 10 | KB |
| Total storage (outgoing) | f500 | GB |
| Outgoing bandwidth | f47 | Mbps |
| Peak outgoing bandwidth | f800 | Gbps |
| Peak incoming bandwidth | f80 | Gbps |

> **Note:** Under normal operation, the system requires approximately 6 Mbps of incoming bandwidth and 47 Mbps of outgoing bandwidth to handle typical user traffic. During peak usage periods, bandwidth demands may increase significantly. For planning purposes, we use a conservative estimate of a tenfold surge, which would raise the incoming bandwidth requirement to around 60 Mbps and the outgoing bandwidth to about 470 Mbps. However, actual traffic spikes can be higher or lower depending on user behavior and system conditions. Therefore, the system should be designed with the flexibility to scale accordingly.

### Estimating the number of servers[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Estimating-the-number-of-servers)

To estimate the number of servers, we need to know the number of daily active users on LeetCode. Based on [our assumption](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective) of using daily active users as a proxy for requests per second, we get 10 million requests per second. Then, we use the following formula to calculate the number of servers:

Servers needed at peak load=Number of requests/secondRPS of server\text{Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of server}}Servers needed at peak load=RPS of serverNumber of requests/second​

Using 64,000 as an estimate of the RPS that a server can handle, based on the "[Back-of-the-envelope Calculations](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective)" section, the required number of servers is estimated as follows:

Servers needed at peak load=10 million requests/second64,000≈157 servers\text{Servers needed at peak load} = \frac{10\ \text{million}\_{\text{ requests/second}}}{64,000} ≈ 157 \ \text{servers}Servers needed at peak load=64,00010 million requests/second​​≈157 servers

![The number of servers required for a system like LeetCode](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The number of servers required for a system like LeetCode")

The number of servers required for a system like LeetCode

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Building-blocks-we-will-use)

The design of the LeetCode system incorporates the following building blocks:

![Building blocks required for designing the LeetCode system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks required for designing the LeetCode system")

Building blocks required for designing the LeetCode system

- [**Blob storage**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-a-blob-store) is used for persistent storage of large, unstructured data, such as user-submitted code files, test case data, and other assets essential for the system’s operation.
- [**Load balancers**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers) distribute incoming user requests across multiple active servers to ensure high availability and prevent any single server from becoming a bottleneck, particularly during high-traffic periods like coding contests.
- [**A pub-sub system**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-pub-sub-abstraction) manages asynchronous communication between services using message queues. It decouples service interactions, allowing intensive tasks like code execution and plagiarism checking to be queued and processed efficiently without blocking the main application.
- [**A monitoring service**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-distributed-monitoring) tracks the health and performance of all microservices, particularly the critical code execution and plagiarism-checking services. It continuously checks their operational status and notifies administrators if any issues arise.
- [**Databases**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases) are crucial for storing structured data, such as user profiles, problem metadata, contest results, and leaderboards. Depending on the specific data requirements, a mix of SQL and NoSQL databases may be used.

The LeetCode system may also include key components such as an API gateway, ZooKeeper, caching servers, and message queues to support coordination and performance.

In the next lesson, we will use these building blocks to design a system like LeetCode.

Payment System Design

Design of the LeetCode System

Ask

[Introduction](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Introduction)

[Requirements of LeetCode’s design](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Requirements-of-LeetCodes-design)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Bandwidth-estimation)

[Estimating the number of servers](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Estimating-the-number-of-servers)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-the-leetcode-system#Building-blocks-we-will-use)