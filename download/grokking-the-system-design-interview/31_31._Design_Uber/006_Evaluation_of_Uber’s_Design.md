# Evaluation_of_Uber’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Evaluation of Uber’s Design

Evaluate the Uber System Design against critical non-functional requirements like availability, scalability, and consistency. Understand how architectural choices, including synchronous replication and horizontally scalable databases, ensure high reliability.

We'll cover the following...

- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Requirements-compliance)
  - [Availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Availability)
  - [Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Scalability)
  - [Reliability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Reliability)
  - [Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Consistency)
  - [Fraud detection](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Fraud-detection)
  - [ETA accuracy](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#ETA-accuracy)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Conclusion)

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Requirements-compliance)

Let’s evaluate how the design fulfills non-functional requirements.

### Availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Availability)

The system is designed for high availability. WebSocket servers are deployed to maintain persistent client connections. If a connection drops, the client reconnects through the load balancer and is attached to another healthy server instance. The databases use a primary-secondary replication model with multiple replicas. Cassandra is deployed for its distributed architecture, which improves fault tolerance and minimizes single points of failure. CDNs, distributed caches, and load balancers are used to improve resilience and reduce service disruption.

### Scalability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Scalability)

The system is designed for horizontal scalability. The architecture decomposes functionality into independent services that can be scaled horizontally based on demand. Quadtrees partition the map into smaller regions, reducing the search space for location queries. A CDN offloads static and edge-delivered content, increasing capacity to serve concurrent users. Cassandra is deployed as the primary NoSQL datastore due to its horizontal scalability and distributed architecture. Load balancers distribute traffic across multiple instances, improving throughput and resilience.

### Reliability[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Reliability)

Our system is highly reliable. The trip can continue even if the rider’s or driver’s connection is broken. This is achieved by using their phones as local storage. The use of multiple WebSocket servers ensures smooth, nearly real-time operations. If any server fails, the user can reconnect to another server. We also used redundant servers and databases to ensure there’s no single point of failure. Our services are decoupled and isolated, which eventually increases the reliability. Load balancers help distribute requests away from failed servers to healthy ones.

### Consistency[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Consistency)

We used storage like MySQL to keep our data consistent globally. Moreover, our system does synchronous replication to achieve strong consistency. Because there are only a limited number of data writers and viewers for a trip (rider, driver, and some internal services), the use of traditional databases doesn’t become a bottleneck. Also, data sharding is easier in this scenario.

### Fraud detection[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Fraud-detection)

Our system can detect any fraudulent payment activity. We used the RADAR system to detect any suspicious activity. RADAR recognizes the beginning of a fraud attempt and creates a rule to prevent it.

### ETA accuracy[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#ETA-accuracy)

Fresh segment travel times feed the DeepETT traffic forecasts, DeepETA corrects routing estimates, and logged outcomes recalibrate the models. The routing engine's estimate serves as a fallback, so ETAs remain available during prediction outages.

## Non-functional Requirements Compliance

|  |  |
| --- | --- |
| **Requirements** | **Techniques** |
| Availability | - Using server replicas. - Using database replicas with the Cassandra database. - Load balancers hide server failures from end users. |
| Scalability | - Horizontal sharding of the database. - The Cassandra NoSQL database. |
| Reliability | - No single point of failure. - Redundant components. |
| Consistency | - Strong consistency using synchronous replications. |
| Fraud detection | - Using RADAR to recognize and prevent any fraud related to payments. |
| ETA accuracy | • Using DeepETT to forecast segment travel times, so routes reflect upcoming traffic.  • Using DeepETA to correct the routing engine’s estimate.  • Logging predicted ETAs and comparing them with actual arrival times to recalibrate the models.  • Falling back to the routing engine’s estimate when the prediction service is unavailable. |

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Conclusion)

This chapter covered the design of a ride-hailing service like Uber, including discussion and evaluation of functional and non-functional requirements. Key takeaways include:

- Using quadtrees to efficiently locate drivers.
- Calculating ETA with routing algorithms and machine learning.
- Implementing fraud detection to protect business integrity.

Payment Service and Fraud Detection in Uber Design

Quiz on Uber's Design

Ask

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Requirements-compliance)

[Availability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Availability)

[Scalability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Scalability)

[Reliability](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Reliability)

[Consistency](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Consistency)

[Fraud detection](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Fraud-detection)

[ETA accuracy](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#ETA-accuracy)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-ubers-design#Conclusion)