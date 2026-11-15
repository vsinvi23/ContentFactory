# How_Amazon_Scales_for_Prime_Day

Source: https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# How Amazon Scales for Prime Day

The 2018 Prime Day outage at Amazon serves as a critical case study in system design, illustrating the challenges of scalability and availability during high-demand events. The outage, caused by an unexpected surge in traffic that exceeded capacity, resulted in significant financial losses and highlighted the importance of robust infrastructure. Key strategies for preventing such failures include effective load balancing, autoscaling, redundancy, and thorough monitoring. Additionally, the need for accurate capacity estimation and proactive preparation is emphasized to ensure seamless user experiences during peak traffic periods.

We'll cover the following...

- [Amazon Prime Day outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Amazon-Prime-Day-outage)
  - [Causes of the outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Causes-of-the-outage)
- [Importance of scalability and availability](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Importance-of-scalability-and-availability)
  - [What are the optimal 9s of availability?](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#What-are-the-optimal-9s-of-availability)
  - [Isn’t Amazon Web Services (AWS) good enough?](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Isnt-Amazon-Web-Services-AWS-good-enough)
- [An overview of Amazon’s e-commerce infrastructure](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#An-overview-of-Amazons-e-commerce-infrastructure)
- [Techniques to ensure scalability and availability](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Techniques-to-ensure-scalability-and-availability)
  - [Key takeaways from the Amazon outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Key-takeaways-from-the-Amazon-outage)
  - [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Conclusion)

Imagine this: You’ve been eagerly counting down the days until Amazon Prime Day, waiting to catch that perfect deal. Finally, the moment arrives. You rush to the site... only to face error messages and pages that won’t load. Frustrating, right?

This was the reality for millions of shoppers during Amazon’s 2018 Prime Day outage. Let’s unpack what actually happened from a System Design perspective

## Amazon Prime Day outage[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Amazon-Prime-Day-outage)

Amazon experienced a significant outage during its 2018 Prime Day event. The outage lasted several hours and had a noticeable impact on the shopping experience of millions of customers, and on the business itself.

**Impact:** The main Amazon website and mobile app were affected, with users reporting issues accessing product pages, completing purchases, and loading the home page. According to the [report](https://techcrunch.com/2018/07/18/amazon-prime-day-outage-cost/), Amazon lost over $100 million in sales during the downtime, an estimated $1.2 million per minute.

![Amazon's main page on Prime Day 2018](002_How_Amazon_Scales_for_Prime_Day_images/img_f922cfa028b7.svg "Amazon's main page on Prime Day 2018")

Amazon's main page on Prime Day 2018

### Causes of the outage[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Causes-of-the-outage)

While Amazon has not disclosed all the technical details, we can analyze the causes with industry knowledge and engineering principles based on a CNBC report, which includes the following key factors to failure:

1. The first and most important factor is the higher-than-expected spike in traffic, which exceeded Amazon’s capacity despite the preparation. This observation is evident from Amazon’s steps, which included reverting to a simpler front-end page and blocking international traffic.
2. Although Amazon employed a robust microservices architecture, it may have faced issues where service dependencies led to cascading failures. This issue was also reported for other Amazon services, including Twitch, Alexa, and Prime Now.
3. While Amazon utilizes autoscaling to handle surges in traffic, delays occurred in scaling up resources due to configuration issues with Amazon’s systems and services. This forced Amazon to manually deploy servers to meet the traffic load, which cost time and money.

The CNBC report indicates that the surge in traffic was one of the primary factors Amazon couldn’t handle, as it made the service unavailable. The system received approximately 63.5 million requests per second on its storage and computational service (Sable).

In this blog, I’ll explore the technical intricacies of scaling for traffic during high-demand periods, using Amazon as our case study.

We’ll break down the strategies and approaches that ensure a smooth service, regardless of the number of people searching for products, clicking “add to cart”, or placing orders. Whether you’re a tech enthusiast, an e-commerce entrepreneur, or just someone who wants to understand what happens behind the scenes during these mega-sale events, this journey into Amazon’s world of scalability will be enlightening.

Let’s explore the importance of availability bound to scalable systems.

## Importance of scalability and availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Importance-of-scalability-and-availability)

Scalability is the secret sauce allowing companies like Amazon to handle massive traffic spikes without breaking a sweat.

It’s about having the infrastructure to flexibly expand and contract in response to demand. The 2018 Prime Day outage showed that even mature systems can fail under production load.  But many people don’t realize that ensuring scalability isn’t just about handling spikes in traffic; it’s intrinsically linked to availability.

Let’s look at how Amazon processes a user’s request.

A single API request, such as purchasing an item or performing a search, is routed to multiple back-end services, including inventory, payment, shipping, indexing, and recommendation. Each service must handle part of the request to fulfill it successfully.

When scaling, all these back-end services need to be scaled together to manage increased load effectively, as seen in the purchasing and search examples below:

![A depiction of fanning out requests to multiple subservices ](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A depiction of fanning out requests to multiple subservices ")

A depiction of fanning out requests to multiple subservices

Availability, keeping the services up and running, is the backbone of any online business. A few minutes of downtime can translate into millions of dollars in lost sales, and a spoiled reputation is additional. Availability is important for the success of a service and a seamless user experience. This means that users can access the service and perform the intended operations at any time. In service level agreements (SLAs), availability is defined as a percentage of time, usually represented by 9s, such as 99.999%99.999 \%99.999% uptime of the service.

> **Note:** When we scale a system to handle a surge in demand, it is also crucial to ensure service availability. No matter how much we scale, if we don’t have replicas or failover mechanisms to ensure availability, the service will likely fail, and vice versa.

### What are the optimal 9s of availability?[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#What-are-the-optimal-9s-of-availability)

When deploying services, an uptime of 99.999%99.999 \%99.999% (five 9s) is assumed as the perfect uptime. This allows for only 0.001%0.001 \%0.001% of downtime. Let’s look at some calculations to see what that entails:

24 hours×365 days=8760 hours/year24\ hours \times 365\ days = 8760\ hours/year24 hours×365 days=8760 hours/year

8760 hours×60 minutes=525600 minutes/year8760\ hours \times 60\ minutes = 525600\ minutes/year8760 hours×60 minutes=525600 minutes/year

525600 minutes×0.001100 =5.26 minutes525600\ minutes \times \frac{0.001}{100}\ = 5.26\ minutes 525600 minutes×1000.001​ =5.26 minutes

A downtime of 0.001% equals less than 6 minutes; a service will be down for around 6 minutes in an entire year. Now, 6 minutes in a year doesn’t sound like much, but for services like Amazon, a minute can cost them around a million in sales, especially on events such as *Prime Day.*

Let’s estimate Amazon Prime Day's revenue for 2024 by examining its sales [history](https://capitaloneshopping.com/research/amazon-prime-day-statistics/). Take a look at the graph below:

The expected revenue of Amazon in 2024 (in green).

> **Note:** The expected revenue of Amazon Prime Day 2024 is based on the average annual revenue difference ($1.43 billion) from the above data.

Based on the expected revenue for 2024, Amazon is projected to generate approximately $5 million per minute in sales. Now, let’s see how the 9s of availability affect the downtime and, hence, the loss in revenue of Amazon Prime Day:

## Nines (9s) of availability

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Availability** | **Downtime Per Year** | **Downtime Per Month** | **Downtime Per Day** | **Revenue Loss Per Day** |
| 1 nine––90% | 36.5 days | 72 hours | 2.4 hours | $720 million |
| 2 nines––99.0% | 3.65 days | 7.20 hours | 14.4 minutes | $72 million |
| 3 nines––99.9% | 8.76 hours | 43.8 minutes | 1.46 minutes | $7.3 million |
| 4 nines––99.99% | 52.56 minutes | 4.32 minutes | 8.64 seconds | $0.72 million |
| 5 nines––99.999% | 5.26 minutes | 25.9 seconds | 0.86 seconds | $0.072 million |

The above back-of-the-envelope calculations estimate the loss if Amazon faces downtime on the next Prime Day (2024).

> **Note:** The problem with achieving five or six nines of availability is that it costs a lot of money and effort. The good thing is that you don’t need to have five or six nines of daily availability, except for days like Amazon Prime Day. The cost of achieving five 9s is so high that the returns do not justify the investment.

### Isn’t Amazon Web Services (AWS) good enough?[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Isnt-Amazon-Web-Services-AWS-good-enough)

Amazon Web Services (AWS), Amazon’s cloud platform, offers a powerful suite of services designed to keep modern applications resilient and highly available.

From Amazon EC2 Auto Scaling, which automatically adjusts compute capacity, to Elastic Load Balancing (ELB), which distributes incoming traffic across healthy targets, AWS services enable applications to scale and remain available during high-traffic events such as Amazon Prime Day.

However, even the most advanced cloud infrastructure can experience issues.

In many cases, outages occur not because the tools are insufficient, but because of how they are configured, monitored, and managed. AWS services provide the capabilities, but achieving true reliability requires engineering teams to configure those services correctly, establish clear scaling policies, design for failure, and continuously test their systems.

This serves as an important reminder: AWS offers the building blocks, but availability and scalability ultimately depend on sound architectural decisions. To understand how Amazon achieves this at scale, let’s examine the core principles behind designing systems for high availability and elastic scalability.

## An overview of Amazon’s e-commerce infrastructure[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#An-overview-of-Amazons-e-commerce-infrastructure)

Amazon started as an online bookstore and has since evolved into the world's largest e-commerce platform, offering a vast array of products.

Let’s see how the Amazon e-commerce platform works for selling and purchasing goods. The Amazon system must be highly scalable and available to handle millions of transactions per day, particularly during events like Amazon Prime Day.

Yes, you guessed it right; it should also be performant and consistent, which, for the time being, will be considered secondary metrics. The primary metrics are scalability and availability. Let’s have a walkthrough of the Amazon back-end infrastructure as given in this high-level design:

![A high-level design of Amazon’s e-commerce system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A high-level design of Amazon’s e-commerce system")

A high-level design of Amazon’s e-commerce system

Initially, the users can visit the homepage to search for an item of interest.

The search service utilizes the Elasticsearch system for several key advantages, including performance, scalability, and full-text search features. At the back of the homepage is a recommendation service that provides personalized recommendations to users based on their purchase history or search activity.

If the user is new, they are shown some trending products on the home page.

Once the users select items and add them to the shopping cart, the cart service is triggered at the backend, which keeps the items in the relevant databases. The order service handles incoming orders from users and stores detailed information about the order, including customer and product information, in the databases.

This service is responsible for capturing the delivery address and the relevant information.

When a user submits a purchase, the order service sends the payment request to the payment gateway, which charges the customer’s selected payment method.

 The pub/sub system decouples various services, allowing them to communicate asynchronously.

## Techniques to ensure scalability and availability[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Techniques-to-ensure-scalability-and-availability)

Let’s examine some techniques that can be implemented to ensure the scalability and availability of the system. The most prominent techniques are:

- **Database replication, distributed caches, and backups:** Database replication techniques ensure data availability and significantly enhance scalability. Using the right techniques to store and retrieve data is essential to maintaining seamless service continuity. This includes replicating data across databases and regions, partitioning data based on workload requirements, and using different storage systems for different data types.  Techniques like distributed caching enhance performance by storing frequently accessed data closer to where it is needed, efficiently managing a large volume of incoming requests. Additionally, incorporating regular backups is crucial for disaster recovery. While these strategies require cost and effort, they are essential for maintaining the system’s reliability and readiness for unexpected events.
- **Load balancing and autoscaling groups:** This is a no-brainer. Impleme­nting load balancing involves distributing incoming traffic among targets, such as containers, servers, and data ce­nters. This prevents ove­rwhelming a single serve­r and allows another to step in if nee­ded. Similarly, autoscaling groups enable a system to adjust the number of active instances based on demand, le­ading to enhanced availability, performance, and user experie­nce.
- **Redundancy of services:** By duplicating critical services across multiple zones and regions, a system can ensure that even if a service in one region fails, another can take over seamlessly. This redundancy minimizes downtime and latency, handles large requests efficiently, and maintains the platform’s reliability, ensuring a consistent user experience.
- **Content Delivery Networks (CDNs):** Utilize CDNs to deliver content to users with low latency and high transfer speeds. By caching content at edge locations worldwide, they ensure that users receive data from the nearest server, reducing load times and improving the overall user experience. It also reduces the burden on the origin servers. CDNs are essential for efficiently handling large amounts of traffic and improving overall availability.
- **Monitoring and auto-recovery mechanisms:** Effective monitoring ensures a system’s health and performance. Utilizing tools for real-time monitoring of system metrics (such as response time, resource utilization, access logs, temperature, and security events) and setting up automated alerts helps engineering teams promptly address potential issues. Implementing auto-recovery processes, such as restarting failed instances or triggering automatic failovers, is essential for maintaining service continuity and minimizing downtime. These techniques are vital for proactive system management and ensuring reliable operation under varying conditions.
- **Testing:** Thorough load tests simulating peak traffic conditions are crucial. These tests should account for the worst-case scenarios, ensuring all systems can handle extreme loads.

You might think you can get by without the techniques above, and maybe you can, until that one bad day strikes. Being prepared can make all the difference. Trust me, you’ll be grateful you invested in these strategies when that day comes.

Delivering a reliable user experience during peak traffic requires strong engineering practices and continuous operational improvement. That’s only the first half of the problem. What happens if there is a failure? That’s the second half! You need standby engineering teams on high alert with contingency plan(s) to ensure you recover quickly and successfully.

Let’s see what techniques Amazon uses to ensure scalability and availability in the following table:

|  |  |
| --- | --- |
| **Strategies for Scalability and Availability** | **Amazon’s Techniques and Services** |
| Database replication and backups | - **Amazon RDS** for multi-availability zone deployment - **Amazon DynamoDB** for fully managed multiregion, multi-active data replication - **Amazon Aurora** for synchronous replication for high availability within a region and asynchronous replication for cross-origin data redundancy - **Amazon DocumentDB** for multiprimary replication across multiple availability zones |
| Distributed cache | - **Amazon ElasticCache** is the distributed cache solution used for high performance, scalability, and availability |
| Load balancing and Autoscaling | - **Amazon Elastic** loadbalancing for distributing different types of traffic across various services - **Amazon EC2** autoscaling for automatically adjusting the number of EC2 instances - **Amazon ECS** and **EKS** autoscaling for containerized applications |
| Content Delivery Networks (CDNs) | - **Amazon CloudFront** for placing the content near users |
| Monitoring and autorecovery mechanisms | - **Amazon CloudWatch** for monitoring and observing the services - **Amazon EC2 Auto Recovery** enables automatic recovery of EC2 instances - **AWS Systems Manager** provides a unified user interface for managing AWS resources - **AWS Health** provides personalized alerts and recovery guidance in the event of failure |
| Testing | - **Amazon GameDay** simulates failures to prepare for unforeseen situations |

### Key takeaways from the Amazon outage[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Key-takeaways-from-the-Amazon-outage)

Amazon’s 2018 Prime Day outage highlights several important lessons for managing high-demand periods for engineering teams and tech enthusiasts:

- Building a perfect system is impossible, but there is nothing wrong with striving to achieve a well-designed one. How do you achieve that? Keep your design as simple as possible and evolve it slowly to avoid unnecessary complexities.
- Blame the configuration management or load testing teams; systems inevitably fail, even among tech giants like Amazon, Meta, and Google. Surprisingly, if you visit independent services like Downdetector, you may find your favorite application struggling to provide service in some parts of the world. The key aspect here is preparation for such incidents, including mitigation techniques to employ before they occur, a contingency plan in place after they happen, and the lessons learned from past failures.
- Faulty capacity estimation is a primary reason why systems fail. You design systems and prepare for the traffic you estimate. A faulty estimation leads to a faulty design. Therefore, always base your math on meaningful assumptions and intelligent guessesto make informed design decisions.

### Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Conclusion)

A system like Amazon needs to analyze user behavior and usage patterns and predict traffic spikes.

This can be achieved via advanced analytics, where metrics such as peak viewing times, popular content, and regional user distribution are continuously monitored. Furthermore, traffic patterns can be predicted through big data analytics technology, and the system can be prepared for potential surges.

Simultaneously, monitoring systems can provide valuable insights into current usage and facilitate better resource management.

To handle peak loads effectively, it’s essential to introduce autoscaling systems that adjust the number of servers according to demand. AWS utilizes Auto Scaling groups to automatically add or remove instances based on fluctuations in traffic.

The combination of predictive analytics with reactive scaling and load balancing will enable the system to manage peak loads optimally without sacrificing performance.

How Spotify Wrapped Scales for 7M Users

6 Tips from a System Design Expert: How Twilio Builds for Scale

Ask

[Amazon Prime Day outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Amazon-Prime-Day-outage)

[Causes of the outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Causes-of-the-outage)

[Importance of scalability and availability](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Importance-of-scalability-and-availability)

[What are the optimal 9s of availability?](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#What-are-the-optimal-9s-of-availability)

[Isn’t Amazon Web Services (AWS) good enough?](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Isnt-Amazon-Web-Services-AWS-good-enough)

[An overview of Amazon’s e-commerce infrastructure](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#An-overview-of-Amazons-e-commerce-infrastructure)

[Techniques to ensure scalability and availability](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Techniques-to-ensure-scalability-and-availability)

[Key takeaways from the Amazon outage](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Key-takeaways-from-the-Amazon-outage)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/how-amazon-scales-for-prime-day#Conclusion)