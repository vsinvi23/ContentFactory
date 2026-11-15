# Key_Concepts_to_Prepare_for_the_System_Design_Interview

Source: https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Key Concepts to Prepare for the System Design Interview

In System Design Interviews, candidates are tasked with designing web-scale applications, such as those for Instagram or YouTube, through open discussions rather than fixed answers. Preparation should focus on fundamental concepts, distributed systems, large-scale web application architecture, and design principles. Key concepts include the PACELC theorem, heartbeat mechanisms, AJAX polling, and the importance of replication and consensus in distributed systems. Understanding these elements is crucial for effectively addressing interview questions and demonstrating the ability to design robust, scalable systems in a cloud-driven environment.

We'll cover the following...

- [Why is it important to prepare strategically?](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Why-is-it-important-to-prepare-strategically)
- [Fundamental concepts in System Design interview](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamental-concepts-in-System-Design-interview)
  - [PACELC theorem](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#PACELC-theorem)
  - [Heartbeat](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Heartbeat)
  - [AJAX polling](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#AJAX-polling)
  - [HTTP long-polling](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-long-polling)
  - [WebSockets](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#WebSockets)
  - [Server-sent events (SSEs)](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Server-sent-events-SSEs)
  - [Fundamentals of distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamentals-of-distributed-systems)
  - [The architecture of large-scale web applications](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#The-architecture-of-large-scale-web-applications)
    - [N-tier applications](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#N-tier-applications)
    - [HTTP and REST](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-and-REST)
    - [DNS and load balancing](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#DNS-and-load-balancing)
    - [Caching](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Caching)
    - [Stream processing](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Stream-processing)
  - [Design of large-scale distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Design-of-large-scale-distributed-systems)
- [Summary](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Summary)

In a System Design Interview, interviewers ask the candidate to design a web-scale application.

For example, they might ask to design platforms like [Instagram](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-instagram), [YouTube](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-youtube), or [Uber's backend](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-uber). Unlike coding interview questions, System Design Interviews are free-form discussions with no right or wrong answers. Instead, the interviewer is trying to evaluate the candidate’s ability to discuss the different aspects of the system and assess the solution based on the requirements that might evolve during the conversation.

The best way to imagine the conversation is that our colleagues and we are asked to design a large-scale system.

We have hashed out the details on the whiteboard, and we understand the requirements, scope, and constraints before proposing a solution. So, how do we design a system in an interview if we have never built one in real life? To crack the System Design interview, we’ll need to prepare in four areas:

1. Fundamental concepts in System Design interview
2. Fundamentals of distributed systems
3. The architecture of large-scale web applications
4. Design of large-scale distributed systems

Each of these dimensions flows into the next.

## Why is it important to prepare strategically?[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Why-is-it-important-to-prepare-strategically)

How we prepare for an interview at Amazon will likely differ from how we prepare for one at Slack.

While many companies share similar interview structures, each also includes unique expectations that require targeted preparation. This is why a strategic approach is essential. When we’re intentional and thorough in creating an interview prep plan, we build long-term confidence.

If we don’t understand the fundamentals, we can’t architect a system.

If we can’t combine those systems effectively, we won’t be able to design a complete solution. But once we’ve practiced designing large-scale systems, we can use those insights to reinforce and expand our foundational knowledge. Preparation becomes a cycle of learning, applying, and refining.

Let’s look at each of these dimensions.

Preparing for the System Design interview

## Fundamental concepts in System Design interview[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamental-concepts-in-System-Design-interview)

In this lesson, we’ll explore some key concepts important for the System Design interview.

### PACELC theorem[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#PACELC-theorem)

The CAP theorem doesn’t answer the question: What choices does a distributed system have when there are no network partitions?. The PACELC theorem answers this question.

The PACELC theorem states the following about a system that replicates data:

- `if statement`**:** A distributed system can trade off between availability and consistency if there’s a partition.
- `else statement`**:** When the system normally runs without partitions, the system can trade off between latency and consistency.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27673%27%20height=%27441%27/%3e)![The flow of the PACELC theorem](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The flow of the PACELC theorem")

The flow of the PACELC theorem

The first three letters of the theorem, PAC, are the same as the CAP theorem.

The ELC is the extension here. The theorem assumes we maintain high availability by replication. When there’s a failure, the CAP theorem prevails. If there isn’t a failure, we still have to consider the tradeoff between consistency and latency of a replicated system.

**Note:** Examples of a PC/EC system include HBase and Google Spanner, which prioritize strong consistency, often at the expense of availability and latency. Bigtable can be configured for strong consistency (by reading from the leader), but its default behavior favors lower latency with eventual consistency, which aligns more with PA/EL. Similarly, PA/EL systems, such as Dynamo and Cassandra, prioritize availability over consistency during partitions and emphasize low-latency operations. MongoDB often behaves like a PA/EC setup, prioritizing availability in partitions while offering configurable consistency guarantees in other scenarios.

### Heartbeat[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Heartbeat)

A **heartbeat message** is a mechanism that helps us detect failures in a distributed system. If there’s a central server, all servers periodically send a heartbeat message to it to show that they’re still alive and functioning. If there’s no central server, all servers randomly select a set of servers and send a heartbeat message to that set every few seconds.

This way, if no heartbeat messages are received for a while, the system can suspect a potential failure or crash.

### AJAX polling[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#AJAX-polling)

Polling is a standard technique used by most AJAX apps. The idea is that the client repeatedly polls a server for data. The client makes a request and waits for the server to respond with data. If no data is available, the server returns an empty response.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27591%27%20height=%27270.9999999999999%27/%3e)![AJAX polling](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "AJAX polling")

AJAX polling

### HTTP long-polling[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-long-polling)

With long-polling, the client requests information from the server, but the server may not respond immediately.

This technique is sometimes referred to as *hanging GET*. If the server doesn’t have any available data for the client, it’ll hold the request and wait until data becomes available, instead of sending an empty response. Once the data becomes available, a full response is sent to the client.

The client immediately re-requests information from the server, ensuring that the server will almost always have an available waiting request to use for delivering data in response to an event.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27591%27%20height=%27271%27/%3e)![HTTP long-polling](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "HTTP long-polling")

HTTP long-polling

### WebSockets[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#WebSockets)

**WebSocket** provides full-duplex communication channels over a single TCP connection.

It provides a persistent connection between a client and a server. Both parties can use this connection to start sending data at any time. The client establishes a connection through a WebSocket handshake. Once the handshake succeeds, the connection stays open, and data can flow in both directions.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27601%27%20height=%27271%27/%3e)![Full-duplex communication using WebSockets](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Full-duplex communication using WebSockets")

Full-duplex communication using WebSockets

### Server-sent events (SSEs)[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Server-sent-events-SSEs)

A client can establish a long-term connection with a server using SSEs. The server uses this connection to send data to a client. If the client wants to send data to the server, it would require the use of another technology or protocol.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27601%27%20height=%27271%27/%3e)![Server-sent events (SSE)](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Server-sent events (SSE)")

Server-sent events (SSE)

### Fundamentals of distributed systems[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamentals-of-distributed-systems)

Like with anything else, it is important to start with the basics.

The fundamentals of distributed systems provide us with a framework for understanding what’s possible and what’s not in a given system. They help us evaluate architectural constraints and the trade-offs involved in optimizing for goals such as consistency or write throughput. At the most basic level, we must start with the strengths, weaknesses, and purposes of distributed systems.

We need to be able to discuss topics like:

**Data durability and consistency:** We must understand the differences and impacts of storage solution failure and corruption rates in read-write processes.

**Replication:** Replication is the key to unlocking data durability and consistency. It deals with backing up data but also with replicating processes at scale.

**Partitioning:** Also called sharding, partitions divide data across different nodes within our system. As replication distributes data across nodes, partitioning distributes processes across nodes, reducing the reliance on pure replication.

**Consensus:** One of our nodes is located in Seattle, another in Beijing, and another in London. There is a system request at 7:05 a.m. Pacific Daylight Time. Given the travel time of data packets, can this be recorded and properly synchronized in the remote nodes, and can it be confirmed?

Consensus is the process by which distributed nodes agree on a shared state or the order of operations, which helps maintain consistency and supports reliable replication across the system.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27491%27%20height=%27376%27/%3e)![Consensus in System Design](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Consensus in System Design")

Consensus in System Design

**Distributed transactions:** Once we’ve achieved consensus, transactions from applications need to be committed across databases, with fault checks performed by each involved resource. Two-way and three-way communication for reading, writing, and committing are shared across participant nodes.

### The architecture of large-scale web applications[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#The-architecture-of-large-scale-web-applications)

We already know that most large-scale applications are web applications. Even if it’s not, major consumer platforms like Netflix, Twitter, and Amazon, as well as enterprises, are moving away from on-premises systems like Exchange to cloud solutions from Microsoft, Google, and AWS. That’s why it’s good to understand the architecture of such systems.

We need to learn about topics such as:

#### N-tier applications[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#N-tier-applications)

Processing happens at various levels in a distributed system.

Some processes are executed on the client, some on the server, and others on another server—all within a single application. These processing layers are called **tiers**, and understanding how those tiers interact with each other and the specific processes they are responsible for is part of System Design for the web.

#### HTTP and REST[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-and-REST)

[HTTP](https://www.educative.io/courses/grokking-the-product-architecture-interview/hypertext-transfer-protocol-http) is a foundational protocol that underlies the entire internet.

It is the system through which we send every email, stream every Netflix movie, and browse every Amazon listing. [REST](https://www.educative.io/courses/grokking-the-product-architecture-interview/representational-state-transfer-rest-web-architecture-style) is a set of design principles that enable direct interaction with the HTTP API, allowing for efficient and scalable systems with components isolated from each other’s assumptions.

Using these principles and an open API makes it easier for others to build on our work or extend our capabilities with extensions to their own apps and services.

#### DNS and load balancing[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#DNS-and-load-balancing)

If 99 users access the system at the same time, DNS-based routing can help distribute traffic across servers A, B, and C instead of sending all traffic to server A.  Routing client requests to the correct server and the appropriate tier where processing occurs helps ensure system stability. We need to know how to do this.

#### Caching[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Caching)

A cache makes our most frequently requested data and applications accessible to most users at high speeds. The questions for our web application are what needs to be stored in the cache, how we direct traffic to the cache, and what happens when we don’t have what we want in the cache.

#### Stream processing[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Stream-processing)

Stream processing applies uniform processes to the data stream. If an application has continuous, consistent data flowing through it, then stream processing enables the efficient use of local resources within the application.

### Design of large-scale distributed systems[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Design-of-large-scale-distributed-systems)

This may seem like a lot, but it actually takes only a few weeks of preparation, less if we have a solid foundation to build on.

Once we have grasped the basics of [distributed systems](https://www.educative.io/courses/distributed-systems-practitioners) and [web architecture](https://www.educative.io/courses/software-architecture-in-applications), it is time to apply this knowledge and design real-world systems. Finding and optimizing potential solutions to these problems will give us the tools to approach the System Design interview with confidence.

Once we are ready to practice our skills, we can tackle some sample problems from real-world interviews, along with tips and approaches to build ten different web services.

## Summary[#](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Summary)

The world is more connected than ever, with almost all devices utilizing System Design and distributed systems.

Technical interviews, especially at large tech companies, are increasingly leaning toward System Design interview questions. We should be well prepared to tackle any questions that come our way. Common system design interview topics include designing a URL shortener, explaining the CAP theorem, comparing SQL and NoSQL databases, choosing the right data model for a use case, and reasoning about latency, scalability, and reliability. Some interviews may also include algorithm and data structure questions.

Consumers and businesses alike are online, and even legacy programs are migrating to the cloud.

Distributed systems are the present and future of the software engineering discipline. As System Design Interview questions make up a bigger part of the developer interview, having a working knowledge of distributed systems will pay dividends in our careers.

Distributed Systems Considerations and Trade-Offs

Scalable Systems 101

Ask

[Why is it important to prepare strategically?](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Why-is-it-important-to-prepare-strategically)

[Fundamental concepts in System Design interview](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamental-concepts-in-System-Design-interview)

[PACELC theorem](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#PACELC-theorem)

[Heartbeat](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Heartbeat)

[AJAX polling](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#AJAX-polling)

[HTTP long-polling](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-long-polling)

[WebSockets](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#WebSockets)

[Server-sent events (SSEs)](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Server-sent-events-SSEs)

[Fundamentals of distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Fundamentals-of-distributed-systems)

[The architecture of large-scale web applications](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#The-architecture-of-large-scale-web-applications)

[N-tier applications](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#N-tier-applications)

[HTTP and REST](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#HTTP-and-REST)

[DNS and load balancing](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#DNS-and-load-balancing)

[Caching](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Caching)

[Stream processing](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Stream-processing)

[Design of large-scale distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Design-of-large-scale-distributed-systems)

[Summary](https://www.educative.io/courses/grokking-the-system-design-interview/key-concepts-to-prepare-for-the-system-design-interview#Summary)