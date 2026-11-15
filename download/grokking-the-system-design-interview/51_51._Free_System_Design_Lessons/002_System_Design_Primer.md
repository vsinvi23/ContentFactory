# System_Design_Primer

Source: https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# System Design Primer

Review core OS, networking, and distributed systems concepts behind System Design. Learn to define requirements and weigh trade-offs.

We'll cover the following...

- [Operating systems fundamentals](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Operating-systems-fundamentals)
  - [Concurrency](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency)
  - [Synchronization](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Synchronization)
- [Computer network essentials](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Computer-network-essentials)
  - [Transport layer protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Transport-layer-protocols)
  - [Application layer protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Application-layer-protocols)
  - [Web API architectures](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Web-API-architectures)
  - [Remote procedure call frameworks](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Remote-procedure-call-frameworks)
  - [Comparison of the network protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Comparison-of-the-network-protocols)
  - [Communication models](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Communication-models)
- [Distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Distributed-systems)
  - [Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scalability)
  - [Availability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Availability)
  - [Replication and sharding](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Replication-and-sharding)
  - [Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Consistency)
  - [Latency and performance](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Latency-and-performance)
  - [Concurrency and coordination](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency-and-coordination)
  - [Security and privacy](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Security-and-privacy)
  - [Monitoring and observability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Monitoring-and-observability)
  - [Resilience and error handling](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Resilience-and-error-handling)
- [Defining system requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Defining-system-requirements)
  - [Identifying functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-functional-requirements)
  - [Identifying non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-non-functional-requirements)
  - [Scoping requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scoping-requirements)
  - [Trade-offs](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Trade-offs)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Conclusion)

In this lesson, we will examine operating system concepts, networking fundamentals, and more advanced distributed systems topics. These are the topics that frequently appear in System Design discussions and interviews.

![Other interviews vs. a System Design interview](002_System_Design_Primer_images/img_41d609fca999.svg "Other interviews vs. a System Design interview")

Other interviews vs. a System Design interview

**Disclaimer:** This chapter provides an overview of the basic distributed system concepts. If you are already familiar with these topics, you can proceed to the next chapter. However, we recommend quickly reviewing this chapter to refresh your knowledge.

Of course, there are several terms and concepts in System Design. However, based on our experience, the following topics are considered the highest priority for building a strong understanding.

## Operating systems fundamentals[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Operating-systems-fundamentals)

**Operating systems (OS)** are the backbone of modern computing, but their role extends far beyond simply running applications.

For system designers, a deep understanding of OS internals is crucial. This includes knowledge of process management, memory allocation, concurrency models, and file systems. Understanding OS architectures such as monolithic and microkernel designs, along with their performance trade-offs, helps engineers make better design decisions.

A deep understanding of operating system (OS) concepts is non-negotiable in System Design.

From scheduling and resource allocation to process management and concurrency models, these foundational principles empower us to craft robust, efficient, and scalable systems. Let’s dive into the essential OS knowledge needed to elevate our System Design skills.

### Concurrency[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency)

**Concurrency**, the simultaneous execution of multiple tasks, is a fundamental challenge and opportunity in System Design. While processes and threads are the building blocks, the true mastery lies in understanding how to orchestrate them effectively to achieve optimal performance, reliability, and responsiveness.

> **Educative byte:** *Concurrency is a way to structure a software system by decomposing it into components that can be executed independently—Rob Pike, co-creator of the Go programming language*

Modern systems, especially distributed platforms such as web services and cloud infrastructure, use concurrency to scale throughput and improve performance. However, this concurrency necessitates robust thread synchronization and coordination mechanisms to ensure data consistency, prevent race conditions, and manage resource contention.

- **Locks:** This is the most fundamental synchronization primitive. Various types of locks exist, including mutexes (mutual exclusion locks), read-write locks, and spin locks, each with distinct performance characteristics and use cases.
- **Semaphores:** These are generalized locks that allow a limited number of threads to access a resource concurrently. Semaphores are often used to control access to a pool of resources or to implement producer-consumer scenarios.
- **Condition variables:** These enable threads to wait for a specific condition to become true before proceeding. Condition variables are typically used with locks to create more complex synchronization patterns.
- **Barriers:** These are synchronization points where threads wait until all threads in a group have reached the barrier before continuing. Barriers are useful for coordinating the execution of parallel tasks that must be completed in phases.

However, there is one common issue with concurrency: synchronization.

### Synchronization[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Synchronization)

When two independent processes run in parallel, synchronization is not a problem (they do not share resources).

However, when dealing with dependent processes, synchronizing them is crucial to achieving successful concurrency. **Synchronization** is the cornerstone of concurrent programming. It’s the art and science of coordinating access to shared resources among multiple processes.

Just as traffic lights manage the flow of vehicles, synchronization mechanisms like mutexes (mutual exclusion locks), semaphores, condition variables, and monitors, each with unique strengths and use cases, regulate access to shared data. Choosing the right mechanism ensures correctness and performance in concurrent systems.

![Process 1 needs the shared data, so it has acquired a lock on it. This means Process 2 cannot access the data until Process 1 is done using it.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Process 1 needs the shared data, so it has acquired a lock on it. This means Process 2 cannot access the data until Process 1 is done using it.")

Process 1 needs the shared data, so it has acquired a lock on it. This means Process 2 cannot access the data until Process 1 is done using it.

We use interprocess communication (IPC)to synchronize and communicate messages between different processes. This is where the *traffic lights* come in. One process can broadcast a message to the others about using/locking a resource, or about no longer using that resource.

> **Note:** Understanding synchronization is critical. In a System Design interview, being able to discuss why a certain synchronization mechanism was chosen and what trade-offs it implies demonstrates a deeper level of understanding.

Distributed systems introduce additional challenges due to the lack of shared memory and the potential for network delays and failures. Several algorithms have been developed to address these challenges:

- **Distributed locks:** These implement mutual exclusion in a distributed environment. Common approaches include centralized coordinator-based locks, token-based locks, and quorum-based locks.
- **Lamport’s logical clocks:** These provide a way to order events in a distributed system without relying on physical clocks. Logical clocks are used to ensure causal ordering and to detect inconsistencies.
- **Vector clocks:** These are an extension of Lamport’s logical clocks that provide a more accurate representation of causality in distributed systems. Vector clocks are used in applications like conflict resolution in distributed databases and collaborative editing tools.
- **Paxos and Raft:** These are consensus algorithms that enable a group of distributed processes to agree on a single value even in the presence of failures. Paxos and Raft are utilized in distributed databases, file systems, and other systems that require strong consistency guarantees.

While modern operating systems excel at managing concurrent processes on a single machine, their capabilities are inherently confined to that one system. This limitation can be overcome by harnessing the power of computer networks, which enables the distribution of processes across multiple machines and unlocks new levels of parallelism and scalability.

## Computer network essentials[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Computer-network-essentials)

A computer network is a collection of interconnected devices that can share information and resources. It is a way for two independent systems to communicate. They are like IPC, but for separate machines. The machines that need to communicate are usually connected through a LAN, and messages are sent through the LAN infrastructure.

How nodes are interconnected defines the network’s topology, which can significantly impact performance, reliability, and cost. Common topologies include:

- **Bus topology:** A single cable (the bus) connects all nodes linearly. It is simple and inexpensive but vulnerable to single points of failure.
- **Star topology:** Each node connects to a central hub or switch. Offers better fault tolerance than bus topology but requires more cabling.
- **Ring topology:** Nodes are connected in a circular chain, with data flowing in one direction. Offers good fault tolerance and predictable performance, but can be complex to manage and maintain.
- **Mesh topology:** Nodes are interconnected with multiple redundant links. Highly reliable and fault-tolerant, but expensive to implement.

![A group of machines interconnected through a LAN.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A group of machines interconnected through a LAN.")

A group of machines interconnected through a LAN.

When sending messages through the network, we must be very specific in crafting those messages. These messages must pass through several hurdles (routers, switches, etc.), and a message meant for machine X mustn’t arrive at machine Y.

We can see why this would confuse the machines if it were to happen.

> **Note:** Computer networks form the backbone of the internet, the infrastructure for System Design. Knowing the concepts of computer networks allows us to delve deeper into the implementation details.

The OSI model divides network tasks into seven layers. Each layer has a specific job, from the physical wires (Layer 1) to our application (Layer 7). It’s like a layer cake, with each layer depending on the one below it. This completes the model of inter-machine communication for both LANs and cross-network (sometimes referred to as WAN) applications.

Let’s look at an example of how all of this works.

![Sending a message over the internet.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Sending a message over the internet.")

Sending a message over the internet.

To achieve this, the two key protocols for network-based communication are TCP and UDP.

### Transport layer protocols[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Transport-layer-protocols)

If computer networks are like the highways of the digital world, then network communication protocols are the traffic rules of the digital world.

They govern how data travels, ensuring it reaches its destination efficiently and accurately. Think of TCP as the postal service; it ensures our data arrives reliably, in the right order, and with a confirmation. UDP is more like an announcer, quickly sharing information without verifying that everyone has heard it.

TCP is used for tasks such as email and web browsing, where accuracy is crucial.

UDP is used for live video streaming, where speed is more important than perfect delivery. Now, what if we want two devices on separate networks to communicate with each other? Let’s look at application layer protocols.

### Application layer protocols[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Application-layer-protocols)

HTTP is the language our browsers use to communicate with websites. It allows us to request web pages and send data back.

In this scenario, our machine, which is the browser, requests information from another machine located elsewhere. It’s a bit like a conversation, with each request and response forming a step in the dialogue. Whenever we have cross-network communication, we can be certain that HTTP is involved.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

This protocol started the revolution for apps on the internet. Everything from social media and emails to online games uses HTTP.

HTTPS builds on this foundation by providing a secure, encrypted connection, ensuring data privacy and integrity for all internet communications. FTP and SMTP, two other fundamental protocols, also play crucial roles in shaping the internet as we know it today. FTP enables the transfer of files between servers and clients, facilitating the sharing and distribution of digital content.

SMTP, on the other hand, is responsible for delivering emails, enabling users to communicate with each other worldwide.

> **Note:** When designing APIs in a System Design interview, one of the most frequently asked questions is which version of HTTP to use (HTTP/1.1 or HTTP/2.0) and why.

With the advent of the internet, communication between different machines became essential. Everyone started to find better and safer ways to communicate between networks. That’s how we got RPCs and APIs.

### Web API architectures[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Web-API-architectures)

We have likely heard of terms like REST and GraphQL as the essentials for any web application.

**REST** is an architectural style for designing networked applications. It relies on a stateless, client-server communication model and leverages HTTP protocols, making it a highly scalable and flexible approach for building APIs.

This simplicity and wide adoption have made REST a cornerstone of modern web development, facilitating seamless integration between diverse systems.

GraphQL, on the other hand, is a query language for APIs and a runtime for executing those queries by using a type system we define for our data. It offers a more efficient, powerful, and flexible alternative to REST. With GraphQL, clients can request the data they need, reducing over-fetching and under-fetching of data.

These frameworks are so essential for web development that we now have entire system architectures built to support them. While REST is powerful, RPCs can be superior in some applications.

### Remote procedure call frameworks[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Remote-procedure-call-frameworks)

RPCs allow a program on one computer to execute a function or procedure on another computer as if it were running locally. The request message is sent to the remote computer, which executes the requested function and sends back a response message.

![How RPCs work](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "How RPCs work")

How RPCs work

RPCs are used in various applications, from distributed file systems to web services. They simplify the development of distributed systems by abstracting away the details of network communication.

gRPC is a high-performance, open-source RPC framework developed by Google. It leverages modern technologies like Protocol Buffers and HTTP/2.

gRPC offers several advantages over traditional RPC:

- **Performance:** gRPC is designed for high throughput and low latency, making it ideal for modern microservices architectures.
- **Language:** gRPC supports various programming languages, allowing us to build distributed systems using our preferred tools.
- **Streaming:** gRPC supports client-side and server-side streaming, enabling efficient communication for real-time applications.

> **Note:** While gRPC offers numerous advantages, it’s important to consider its learning curve and additional tooling requirements before adopting it.

### Comparison of the network protocols[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Comparison-of-the-network-protocols)

There are numerous network communication protocols, each designed for a specific purpose. The most popular ones are listed below.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Protocol** | **Description** | **Use Cases** | **Strengths** | **Weaknesses** |
| **TCP** | Provides reliable, ordered delivery of data. | Web browsing, email, and file transfer | It is reliable and guarantees data delivery. | It is slower than UDP due to error checking and retransmission overhead. |
| **UDP** | Provides fast, connectionless delivery of data. | Video streaming, online gaming, and DNS lookups | It is fast, with low latency. | It is unreliable and may drop packets, making it unsuitable for applications requiring guaranteed data delivery. |
| **HTTP** | Used for transferring hypertext (web pages). | Web browsing and APIs | It is simple and widely supported. | It is stateless, and each request/response is independent; it can be inefficient for frequent communication. |
| **REST** | Allows stateless communication between devices. | Public APIs, microservices, and web applications | It offers simplicity, ease of use, wide adoption, and scalability. | It presents an over-fetching/under-fetching issue. |
| **GraphQL** | Query language for APIs. | Complex client-server applications (mobile and web) | It offers precise data fetching, flexibility in evolving APIs, and strong typing. | It offers a steep learning curve, harder to implement caching. |
| **RPC** | Enables a program on one computer to execute a procedure on another computer. | Distributed systems, microservices, and remote file systems | It simplifies the development of distributed systems and abstracts network communication details. | If not implemented properly, it can be slower than local procedure calls and potentially create security vulnerabilities. |
| **gRPC** | A high-performance, open-source RPC framework. | Microservices, cloud-native applications, and real-time communication | It is efficient, language-neutral, and supports streaming. | It presents a steeper learning curve than simpler protocols, requiring additional tooling. |
| **WebSocket** | Enables full-duplex communication over a single TCP connection. | Real-time web applications, chat applications, and collaborative editing | It offers real-time communication and efficient use of network resources. | It is more complex to implement than HTTP and may not be supported by all clients/servers. |

Now that we have reviewed the various protocols that govern how data is sent, we can examine the high-level architectural patterns that define who communicates. These protocols serve as the foundation for more comprehensive communication models.

### Communication models[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Communication-models)

In the client-server model, communication is structured with distinct roles for clients and servers.

Clients request services or resources, while servers provide these services or resources to them. This centralized approach is prevalent in various applications, including web services, email, and database management systems.

The client-server model simplifies management and scaling, but it can also create a single point of failure if the server goes down.

Conversely, the P2P model distributes the roles more evenly.

Each peer can act as both a client and a server, sharing resources directly with others. This decentralization enhances redundancy and resilience, making P2P networks ideal for file sharing, blockchain, and collaborative applications.

However, P2P can be more complex to manage.

![Client-server model vs. peer-to-peer model](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Client-server model vs. peer-to-peer model")

Client-server model vs. peer-to-peer model

The client-server model laid the foundation for the Internet and distributed systems, providing architectural styles such as MVC, microkernel, and numerous others. From this, we gained concepts such as load balancing (distributing incoming traffic), failover mechanisms (backups), and monitoring.

Combining parallel computing concepts with computer networks provides the foundation for distributed systems.

## Distributed systems[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Distributed-systems)

In today’s interconnected world, the software we rely on is rarely confined to a single machine. Instead, it spans multiple computers, working together as a unified system. These are distributed systems.

![A distributed system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A distributed system")

A distributed system

Distributed systems have several key characteristics that distinguish them from traditional, single-machine systems. These characteristics present challenges and opportunities for developers and users alike.

### Scalability[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scalability)

One of the primary benefits of distributed systems is their ability to scale.

Adding more computers to the system can increase its capacity to handle a greater number of users, data, or transactions. This scalability allows distributed systems to adapt to growing demands, ensuring a smooth user experience even as the workload increases.

### Availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Availability)

Distributed systems are designed to be highly available, meaning they should be accessible and operational even if some individual computers fail. This is achieved through redundancy and fault tolerance, where data and services are replicated across multiple machines.

### Replication and sharding[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Replication-and-sharding)

To achieve scalability and availability, distributed systems often use **replication** (copying data across multiple machines) and **sharding** (dividing data into smaller pieces and distributing them across machines). These techniques help to distribute the load and ensure data remains accessible even in the face of failures.

### Consistency[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Consistency)

Distributed systems struggle to ensure data consistency across multiple machines.

Strict consistency guarantees that every read sees the most recent write, even if it means sacrificing some availability. Eventual consistency prioritizes availability, allowing for temporary inconsistencies that are eventually resolved.

### Latency and performance[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Latency-and-performance)

In a distributed system, communication between computers takes time, introducing latency. This can impact the system’s overall performance. Therefore, careful design and optimization are necessary to minimize latency and ensure a responsive user experience.

### Concurrency and coordination[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency-and-coordination)

Distributed systems often involve multiple processes or threads running concurrently across different machines. This can lead to complex interactions and race conditions, where the outcome of an operation depends on the timing of events.

Coordination mechanisms are necessary to ensure that the system operates correctly in concurrent situations.

> **Note:** Race conditions are a common problem when creating parallel applications. Knowing their mitigation strategies, such as locks, mutex, semaphores, etc., is imperative.

### Security and privacy[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Security-and-privacy)

Due to their larger attack surface, distributed systems can be more vulnerable to security threats than single-machine systems. Implementing robust security measures, such as authentication, authorization, and encryption, is crucial to protect the system and its data from unauthorized access.

### Monitoring and observability[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Monitoring-and-observability)

Monitoring the health and performance of a distributed system is crucial for identifying and addressing issues before they impact users. Observability tools provide operators with insights into the system’s behavior, helping them understand what’s happening and why.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

### Resilience and error handling[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Resilience-and-error-handling)

Distributed systems are complex, and failures are inevitable. A resilient system is designed to withstand failures and recover gracefully, minimizing downtime and data loss. Effective error-handling mechanisms are essential for ensuring the system’s reliability.

Understanding the diverse challenges and opportunities of distributed systems sets the stage for the crucial next step: defining the system requirements. After all, a well-designed system begins with a clear vision of what it needs to achieve.

## Defining system requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Defining-system-requirements)

Just as an architect needs a detailed blueprint before constructing a building, software developers need a well-defined set of system requirements before building a software system. These requirements outline what the system should do (functional requirements) and how well it should do (non-functional requirements).

### Identifying functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-functional-requirements)

Functional requirements describe the specific features and capabilities that the system must provide. They answer the question, “What should the system do?” Think of them as the user’s wish list. For a social media app, functional requirements might include:

- The ability to create a profile.
- The ability to post messages, photos, and videos.
- The ability to follow other users.
- The ability to like and comment on posts.

> **Educative byte:** Always prioritize user needs and business goals when defining system requirements. A perfectly designed system that doesn’t solve the right problem is ultimately useless.

Identifying these requirements involves close collaboration with stakeholders, including users, product managers, and business analysts. User stories, use cases, and other techniques can help capture and prioritize functional requirements.

### Identifying non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-non-functional-requirements)

Non-functional requirements are often overlooked, but they are just as critical to the success of a system as functional requirements. These requirements define the qualities that make the system usable, reliable, and efficient. Examples of non-functional requirements include:

- **Performance:** How fast the system should respond to requests.
- **Scalability:** How well the system should handle increased workload.
- **Availability:** How often should the system be accessible?
- **Security:** How well the system should protect data and prevent unauthorized access.
- **Usability:** How easy the system should be to use.

Determining non-functional requirements requires a deep understanding of the system’s context, its users, and the environment in which it will operate. It’s also important to be realistic and avoid setting unattainable goals.

### Scoping requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scoping-requirements)

Scoping is the process of defining the boundaries of our project. It involves deciding which requirements are in scope (i.e., will be addressed) and which are out of scope (i.e., will not be addressed). This is a crucial step, as it helps to manage expectations and prevent scope creep, where the project grows uncontrollably.

> **Note:** This is essential for a successful System Design interview. If we can balance the scope of functional and non-functional requirements with the time constraints of the interview, we are on a path to success.

It’s important to strike a balance when scoping functional and non-functional requirements. We don’t want to overload the system with too many features, but we also don’t want to sacrifice essential qualities like performance or security.

### Trade-offs[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Trade-offs)

In an ideal world, we could have a feature-rich, highly performant, scalable, and secure system.

But in reality, trade-offs are often necessary. For example, increasing the level of security might impact performance, or adding more features might make the system harder to use. The key is to prioritize the most important requirements and make informed decisions about acceptable trade-offs.

This requires careful consideration of the system’s goals, users, and available resources.

> **Note:** This is another key aspect that will distinguish a candidate in an interview. A seasoned engineer is expected to be able to weigh the trade-offs between different requirements, develop valid reasoning, and implement the right ones in the design.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

Defining system requirements is a complex but essential task. It requires clear communication, careful analysis, and the ability to make tough decisions. But when done well, it sets the stage for a successful project that delivers real value to its users.

AI Powered

Saved

3 attempts left

Reset

Choosing API architecture

A development team is building a new mobile application that needs to display complex, nested data from multiple sources on a single screen. They are highly concerned about minimizing data usage on slow mobile networks and want to avoid over-fetching. Which API architecture would be most suitable for these specific requirements?

You have 3 attempts to answer.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Conclusion)

System design focuses on understanding user requirements and making informed technical decisions to build scalable and reliable systems. In this lesson, we've covered the foundational pillars that build upon our initial introduction: operating systems, computer networking, the specific challenges of distributed systems, and the process of defining requirements.

In the next lesson, we will learn in detail about System Design trade-offs.

The All-in-One System Design Master Template

Distributed Systems Considerations and Trade-Offs

Ask

[Operating systems fundamentals](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Operating-systems-fundamentals)

[Concurrency](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency)

[Synchronization](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Synchronization)

[Computer network essentials](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Computer-network-essentials)

[Transport layer protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Transport-layer-protocols)

[Application layer protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Application-layer-protocols)

[Web API architectures](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Web-API-architectures)

[Remote procedure call frameworks](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Remote-procedure-call-frameworks)

[Comparison of the network protocols](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Comparison-of-the-network-protocols)

[Communication models](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Communication-models)

[Distributed systems](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Distributed-systems)

[Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scalability)

[Availability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Availability)

[Replication and sharding](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Replication-and-sharding)

[Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Consistency)

[Latency and performance](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Latency-and-performance)

[Concurrency and coordination](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Concurrency-and-coordination)

[Security and privacy](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Security-and-privacy)

[Monitoring and observability](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Monitoring-and-observability)

[Resilience and error handling](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Resilience-and-error-handling)

[Defining system requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Defining-system-requirements)

[Identifying functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-functional-requirements)

[Identifying non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Identifying-non-functional-requirements)

[Scoping requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Scoping-requirements)

[Trade-offs](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Trade-offs)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-primer#Conclusion)