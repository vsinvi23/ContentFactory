# Evaluation_of_WhatsApp’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of WhatsApp’s Design

Evaluate the WhatsApp System Design by verifying how it meets critical non-functional requirements like low latency, consistency, and security. Analyze the key architectural trade-offs, specifically the choice between consistency and availability based on the CAP theorem, and the balance between security and latency.

We'll cover the following...

- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Requirements-compliance)
- [Trade-offs](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Trade-offs)
  - [The trade-off between consistency and availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-consistency-and-availability)
  - [The trade-off between latency and security](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-latency-and-security)
- [Summary](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Summary)

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Requirements-compliance)

We ensure the design meets the following non-functional requirements:

- **Low latency:** We minimize latency through geographically distributed WebSocket servers with local caching, Redis clusters layered over MySQL, and CDNs for media content.
- **Consistency:** A FIFO messaging queue ensures strict ordering. To handle causality, the [Sequencer](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-sequencer) assigns IDs with appropriate inference mechanisms. For offline users, the Mnesia database queues messages for sequential delivery upon reconnection.
- **Availability:** We achieve high availability by provisioning sufficient WebSocket servers and replicating data. If a WebSocket connection fails, a load balancer re-establishes the session on a healthy server. Additionally, the Mnesia cluster uses primary-secondary replication to ensure durability.
- **Security:** End-to-end encryption secures chat data against unauthorized access. AI-powered message summaries preserve this guarantee: the client controls what is sent, Private Processing keeps no message content, and the summary path stays separate from message delivery. Message translation runs entirely on the device.
- **Scalability:** High-performance engineering allows a single server to handle approximately 10 million connections. The architecture remains flexible, allowing horizontal scaling as load fluctuates.

1.

In the event of a network partition, what should the system choose to compromise between consistency and availability?

Show Answer

Did you find this helpful?

## Non-Functional Requirements Compliance

|  |  |
| --- | --- |
| **Non-Functional Requirements** | **Approaches** |
| Minimizing latency | - Geographically distributed cache management systems and servers - CDNs |
| Consistency | - Provide unique IDs to messages using Sequencer or other mechanisms - Use FIFO messaging queue with strict ordering |
| Availability | - Provide multiple WebSocket servers and managers to establish connections between users - Replication of messages and data associated with users and groups on different servers - Follow disaster recovery protocols |
| Security | - Via end-to-end encryption - Run AI features on-device or in a protected environment with no retention |
| Scalability | - Performance tuning of servers - Horizontal scalability of services |

## Trade-offs[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Trade-offs)

Two major trade-offs characterize the proposed WhatsApp design:

- Consistency vs. availability
- Latency vs. security

### The trade-off between consistency and availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-consistency-and-availability)

According to the CAP theorem, a distributed system facing network partitions must choose between consistency and availability. Since message ordering is essential in this design, we prioritize consistency.

### The trade-off between latency and security[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-latency-and-security)

Real-time messaging requires low latency, but transmitting messages without encryption introduces security risks. The system prioritizes security by using end-to-end encryption, despite the additional computational overhead. This overhead is most noticeable when handling multimedia content. Encrypting large files on the sender’s device and decrypting them on the receiver’s device consumes additional CPU resources and increases latency, as illustrated below:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27808%27%20height=%27299%27/%3e)![End-to-end encryption causes a delay in processing, which has an impact on latency](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "End-to-end encryption causes a delay in processing, which has an impact on latency")

End-to-end encryption causes a delay in processing, which has an impact on latency

## Summary[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Summary)

In this chapter, we designed a WhatsApp messenger. We identified requirements, estimated resources, and defined the high-level architecture. We then detailed specific components and evaluated the design against non-functional requirements and trade-offs.

This problem demonstrated how to optimize general-purpose computational resources for specific use cases. Notably, WhatsApp optimized its software stack to handle a massive number of connections on commodity servers.

Detailed Design of WhatsApp

Quiz on WhatsApp’s Design

Ask

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Requirements-compliance)

[Trade-offs](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Trade-offs)

[The trade-off between consistency and availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-consistency-and-availability)

[The trade-off between latency and security](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#The-trade-off-between-latency-and-security)

[Summary](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design#Summary)