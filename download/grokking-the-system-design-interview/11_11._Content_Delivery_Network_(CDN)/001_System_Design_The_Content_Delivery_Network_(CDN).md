# System_Design_The_Content_Delivery_Network_(CDN)

Source: https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# System Design: The Content Delivery Network (CDN)

Define the critical performance and scaling problems of serving global users from a single data center. Analyze how high latency and resource strain necessitate a distributed solution. Justify the fundamental need for a content delivery network (CDN) in modern System Design.

We'll cover the following...

- [Problem statement](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#Problem-statement)
- [How will we design a CDN?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#How-will-we-design-a-CDN)

## Problem statement[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#Problem-statement)

Consider a data-intensive application serving millions of global users from a single data center. This centralized architecture faces several critical challenges:

- **High latency:** Physical distance between clients and servers increases user-perceived latency. Total latency consists of transmission delay (limited by bandwidth), propagation delay (signal travel time), queuing delay (network congestion), and processing delay. Real-time applications such as VoIP typically require end-to-end latency below 150 ms, while video streaming can tolerate higher delays but degrades with multi-second latency.

> **Note:** According to readings from December 2021, the average round-trip latency from US East (N. Virginia) to US West (N. California) was 62.9 ms. Intercontinental latency, for example, from US East to Africa (Cape Town), was 225.63 ms.

![The above map displays the data center entertaining users’ requests across the globe](001_System_Design_The_Content_Delivery_Network_(CDN)_images/img_7d2a636438a8.svg "The above map displays the data center entertaining users’ requests across the globe")

The above map displays the data center entertaining users’ requests across the globe

- **Data-intensive workloads:** Transferring large volumes of data over long distances traverses multiple ISPs and network paths. Throughput often suffers due to variable congestion and smaller Path message transmission unit (MTU) sizes. Additionally, the origin server must transmit the same data individually to every client, resulting in redundant bandwidth usage that scales poorly with user growth.

> **Note:** According to a survey, 78% of United States consumers use streaming services, an increase of 25% over five years.

- **Resource scarcity and failure risks:** A single data center has finite compute, storage, and network capacity. As traffic increases, system resources can become bottlenecks. A centralized deployment also introduces a single point of failure. If the data center goes offline due to an outage or disaster, the service becomes unavailable.

![User growth over the years for Facebook and YouTube applications](001_System_Design_The_Content_Delivery_Network_(CDN)_images/img_342d817072ea.svg "User growth over the years for Facebook and YouTube applications")

User growth over the years for Facebook and YouTube applications

> **Note:** According to one study, YouTube, Netflix, and Amazon Prime collectively generated 80% of Internet traffic in 2020. Circa 2016, the CDN provider Akamai served 15% to 30% of web traffic (about 30 terabits per second). For 90% of Internet users, Akamai was just one hop away. Therefore, we have strong reasons to optimize the delivery and consumption of this data without making the Internet core a bottleneck.

The solution to these problems is a content delivery network (CDN), a system that brings data closer to users around the world.

## How will we design a CDN?[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#How-will-we-design-a-CDN)

We have divided the design of a CDN into six lessons:

1. [**Introduction to a CDN**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-a-cdn)**:** Introduce CDNs and identify their functional and non-functional requirements.
2. [**Design of a CDN**](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-cdn)**:** Design the CDN architecture and outline the API.
3. [**In-depth investigation of CDN (Part 1**](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-1))**:** Explore caching strategies, CDN architecture, and algorithms for finding the nearest proxy server.
4. [**In-depth investigation of CDN (Part 2)**](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2)**:** Discuss content consistency, proxy server deployment, and specialized CDN configurations.
5. [**Evaluation of CDN**](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-cdns-design)**:** Evaluate the proposed design against our requirements.
6. [**Quiz on CDN System Design**](https://www.educative.io/courses/grokking-the-system-design-interview/quiz-on-cdns-design)**:** Reinforce the major concepts of CDN design.

Let’s begin!

Enable Fault Tolerance and Failure Detection

Introduction to a CDN

Ask

[Problem statement](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#Problem-statement)

[How will we design a CDN?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn#How-will-we-design-a-CDN)