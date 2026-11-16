# Designing_Client-Side_Monitoring_Systems_for_Error_Detection

Source: https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[System Design Interview: Fast-Track in 48 Hours](https://www.educative.io/courses/system-design-interview-prep-crash-course)

# Design a Client-Side Monitoring Service

Explore the design of client-side monitoring systems to detect and respond to errors originating from clients in distributed systems. Understand essential concepts like metrics collection, alerting, data persistence, and privacy considerations. By the end, you will know how to build monitoring agents and collectors that improve service reliability and user experience.

We'll cover the following...

- [Monitoring: metrics and alerting](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Monitoring-metrics-and-alerting)
- [Metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Metrics)
  - [Populate the metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Populate-the-metrics)
  - [Persist the data](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Persist-the-data)
  - [Application metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Application-metrics)
- [Alerting](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Alerting)
- [Client-side errors](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Client-side-errors)
- [Failures due to a routing bug](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Failures-due-to-a-routing-bug)
- [Design of a client-side monitoring system](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Design-of-a-client-side-monitoring-system)
  - [Initial design](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Initial-design)
    - [Issues with probers](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Issues-with-probers)
  - [Improve the design](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Improve-the-design)
  - [Activate and deactivate reports](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Activate-and-deactivate-reports)
  - [Reach collectors under faulty conditions](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Reach-collectors-under-faulty-conditions)
  - [Protect user privacy](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Protect-user-privacy)
- [Conclusion](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Conclusion)

The modern economy depends on the continual operation of IT infrastructure. Such infrastructure contains hardware, distributed services, and network resources. These components are interlinked in such infrastructure, making it challenging to keep everything functioning smoothly without application downtime. There are two types of monitoring systems to monitor and capture different errors: client and server-side monitoring systems. In this lesson, we will focus on the client-side monitoring system.

![](007_Designing_Client-Side_Monitoring_Systems_for_Error_Detection_images/img_272098cfaff1.svg)

**Client-side errors** are errors whose root cause is on the client side. Such errors are reported as error 4xx in HTTP response codes. Some client-side errors are invisible to the service when client requests fail to reach the service.

Let’s learn about the metrics and alerting in a monitoring system before designing the system.

## Monitoring: metrics and alerting[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Monitoring-metrics-and-alerting)

A good monitoring system needs to clearly define what to measure and in what units (metrics). The monitoring system also needs to define threshold values of all metrics and the ability to inform appropriate stakeholders (alerts) when values are out of acceptable ranges. Knowing the state of our infrastructure and systems ensures service stability. The support team can respond to issues more quickly and confidently if they have access to information on the health and performance of the deployments. Monitoring systems that collect measurements, show data, and send warnings when something appears wrong are helpful for the support team.

To further understand metrics, alerts, and their connection with monitoring, we’ll review their significance, potential benefits, and the data we might want to keep track of.

1.

What are the conventional approaches to handling failures in IT infrastructure?

Show Answer

Did you find this helpful?

## Metrics[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Metrics)

**Metrics** objectively define what we should measure and what units will be appropriate. Metric values provide an insight into the system at any point in time. For example, a web server’s ability to handle a certain amount of traffic per second or its inclusion in a web server pool are examples of high-level data correlated with a component’s specific purpose or activity. Another example can be measuring network performance in terms of throughput (megabits per second) and latency (round-trip time). We need to collect the values of metrics with a minimal performance penalty. We may measure this penalty using user-perceived latency or the number of computational resources.

Values that track how many physical resources our operating system uses can be a good starting point. If we have a monitoring system in place, we don’t have to do much additional work to get data regarding processor load, CPU statistics like cache hits and misses, RAM usage by OS and processes, page faults, disc space, disc read and write latencies, swap space usage, and so on. Metrics provided by many web servers, database servers, and other software help us determine whether everything is running smoothly or not.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

### Populate the metrics[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Populate-the-metrics)

The metrics should be logically centralized for global monitoring and alerting purposes. Fetching metrics is crucial to the monitoring system. Metrics can either be pushed or pulled into a monitoring system, depending on the user’s preference.

Here, we confront a fundamental design challenge now: Do we utilize push or pull? Should the server proactively send the metrics’ values out, or should it only expose an endpoint and wait reactively for an inquiry?

In the pull strategy, each monitored server merely needs to store the metrics in memory and send them to an exposed endpoint. The exposed endpoint allows the monitoring application to fetch the metrics itself. Servers sending too much data or sending data too frequently can’t overload the monitoring system. The monitoring system will pull data as per its own schedule.

In other situations, pushing may be beneficial, such as when a firewall prevents the monitoring system from accessing the server directly. The monitoring system has the ability to adjust a global configuration about the data to be collected and the interval at which servers and switches should push the data.

Push and pull terminologies might be confusing. We’ll consider the push or pull strategy from the monitoring system’s perspective whenever we discuss it. Either the system will pull the metrics values from the applications, or the metrics will be pushed to the monitoring system. To avoid confusion, we’ll stick to the monitoring system’s viewpoint.

1.

Logging is the act of keeping records of events in a software system. How does it help in monitoring?

Show Answer

Did you find this helpful?

> **Note:** At times, we use the word “metrics” when we should have used “metrics’ values.” However, we can figure out which of them is being referred to through the context they’re being used in.

### Persist the data[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Persist-the-data)

It is crucial to determine the appropriate storage method for the monitored server’s metrics. A centralized in-memory metrics repository may be all that’s needed. However, for a large data center with millions of things to monitor, there will be an enormous amount of data to store, and a time-series database can help in this regard.

**Time-series databases** help maintain durability, which is an important factor. It isn’t very useful without a historical view of events in a monitoring system. Samples having a value of timestamp are stored in chronological sequence. So, a whole metric’s timeline can be shown as a time series.

### Application metrics[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Application-metrics)

We may need to add code or APIs to expose metrics we care about for other components, notably our own applications. We embed logging or monitoring code in our applications, called **code instrumentation,** to collect information of interest.

Looking at metrics as a whole can shed light on how our systems are performing and how healthy they are. Monitoring systems employ these inputs to generate a comprehensive view of our environment, automate responses to changes like commissioning more EC2 instances if the applications’ traffic increases, and warn humans when necessary. Metrics are system measurements that analyze historical trends, correlations, and changes in performance, consumption, or error rates.

## Alerting[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Alerting)

**Alerting** is the part of a monitoring system that responds to changes in metric values and takes action. There are two components to an alert definition: a metrics-based condition or threshold and an action to take when the values fall outside of the permitted range.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

## Client-side errors[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Client-side-errors)

Clients often access the service via an HTTP request in a distributed system. We can monitor our web and application servers’ logs if a request fails to process. If multiple requests fail, we can observe a spike in internal errors (error 500).

Those errors whose root cause is on the client’s side are hard to respond to because the service has little to no insight into the client’s system. We might look for a dip in the load compared to averages, but such a graph is usually hard. It can have false positives and false negatives due to factors such as unexpected variable load or if a small portion of the client population is affected.

Many factors can cause failures that can result in clients being unable to reach the server. These include the following:

- Failure in DNS name resolution.
- Any failure in routing from the client to the service provider.
- Any failures with third-party infrastructure, such as middleboxes and CDNs.

![Server-side errors vs. client-side errors](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Server-side errors vs. client-side errors")

Server-side errors vs. client-side errors

## Failures due to a routing bug[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Failures-due-to-a-routing-bug)

Let’s look at a real-world example of an error that impacted many service customers, but the service wasn’t readily aware of it.

One of Google’s peer ISPs accidentally announced Internet routes that it wasn’t supposed to. As a result, the traffic of many of Google’s customers started routing through unintended ISPs and wasn’t reaching Google because of the BGP leak, one of the examples of the BGP leak is shown in the illustration below. Clients were frustrated because they couldn’t reach Google, while Google might have been unaware of such problems immediately because they didn’t happen on its infrastructure.

![BGP leak](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "BGP leak")

BGP leak

The leak above isn’t unique. Similar issues keep arising. Another such leakage happened on April 16, 2021, when an AS mistakenly announced over 30,000 BGP prefixes. This resulted in a 13 times spike in the inbound traffic to their network. However, an increase in influx was observed, and the problem was solved.

The impacted services’ monitoring systems might not readily catch the events above. Monitoring such situations is crucial so that the application remains available for all its customers. We’ll go through methods that help us monitor the situations mentioned above.

## Design of a client-side monitoring system[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Design-of-a-client-side-monitoring-system)

A service has no visibility of the errors that don’t occur at its infrastructure. Still, such failures are equally frustrating for the customers, and they might have to ask their friends, “Is the service X down for you as well?” or head to sites like Downdetector to see if anyone else is reporting the same issues. They might report the problem via a Tweet or some other communication channel. However, all such cases have a slow feedback loop. As a service provider, we want to detect such problems as quickly as possible to take remedial measures. Let’s design such a system.

### Initial design[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Initial-design)

We’ll act as clients and perform reachability and health checks to ensure that the client’s requests reach the server. We’ll need various vantage points across the globe. We can run a service, let’s call it prober, that periodically sends requests to the service to check availability. This way, we can monitor the reachability to our service from many different places.

![Prober checking the availability of the website](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Prober checking the availability of the website")

Prober checking the availability of the website

#### Issues with probers[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Issues-with-probers)

We can have the following issues with probers:

- **Incomplete coverage:** We might not have good coverage across all autonomous systems. There are 100,000 unique autonomous systems on the Internet as of March 2021. It’s not cost-effective or even possible to put those many probers across the globe. Country or ISP-specific regulations and the need for periodic maintenance are additional hurdles to implementing such a scheme.
- **Lack of user imitation:** Such probers might not represent a typical user behavior to explain how a typical user will use the service.

> **Note:** The initial design is based on active probing.

### Improve the design[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Improve-the-design)

Instead of using a prober on vantage points, we can embed the probers into the actual application instead. We’ll have the following two components:

- **Agent:** This is a prober embedded in the client application that sends the appropriate service reports about any failures.
- **Collector:** This is a report collector independent of the primary service. It’s made independent to avoid situations where client agents want to report an error to the failed service. We summarize error reports from collectors and look for spikes in the errors graph to see client-side issues.

The following illustration shows how an agent reaches an independent collector when the primary service isn’t reachable:

![Evaluating the agent's report to see a spike in errors](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Evaluating the agent's report to see a spike in errors")

Evaluating the agent's report to see a spike in errors

These collectors are a hierarchy of big data processing systems. We can place them near the client network, and over time, we can accumulate these statistics from all such localized sites. We’ll use online stream processing systems to make such a system near real time. If we’re mainly looking for summary statistics, our system can tolerate the loss of some error reports. Some reports will be relative to the overall user population. We might say 1% of service users are “some.” If we don’t want to lose any reports, we’ll need to design a system with more care, which will be more expensive.

Now, we’ll solve the following concerns:

- Can a user activate and deactivate client-side reports?
- How do client-side agents reach collectors under faulty conditions?
- How will we protect user privacy?

### Activate and deactivate reports[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Activate-and-deactivate-reports)

We’ll use a custom HTML header to send appropriate information to the collectors. Though a client accesses the service via a browser, a specific browser should know about this feature to appropriately fill in the header information in the HTTP requests. For organizations that make browsers and provide services (for example, Chromium-based browsers), such features can be incorporated and standardized over time.

Another solution can be to use a client-side application that the service controls, and then we can easily include such headers over HTTP.

The client can fill in the request header if the client has already consented to that. The service can then reply with appropriate values for the policy and collection endpoints.

![Activate and deactivate reports](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Activate and deactivate reports")

Activate and deactivate reports

### Reach collectors under faulty conditions[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Reach-collectors-under-faulty-conditions)

The collectors need to be in a different failure domain from the web service endpoint that we’re trying to monitor. The client side can try various collectors in different failure domains until one works. We can see a similar pattern in the following examples. At times, we refer to such a phenomenon as being outside the blast radius of a fault.

If we want to see the reachability of an IP, we host the service on a different IP. If we monitor the availability of a domain, we host the collector on a different domain. And if we want to detect that an autonomous system route isn’t hijacked, we host the service in a different autonomous system. Though, for last-mile errors, there isn’t much we could do as a service provider. We might accumulate such events at the client side and report them on the next connectivity. A service can influence the remaining component failures.

## Reaching Collectors Under Faulty Conditions

|  |  |
| --- | --- |
| **Faults** | **Mitigation** |
| Can't resolve example.com | Different server IP |
| Can't resolve example.com | Different domain |
| AS 1234 hijacked | Different ASN |
| CDN available | Different/no CDN |
| Last-mile problems | No readily available fallback for the service |

### Protect user privacy[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Protect-user-privacy)

The human user who uses the client-side software should be in full control to precisely know what data is collected and sent with each request. The user should also be able to reactivate the feature any time they wish. If we use our client-side application (and not a browser application), we have a lot of flexibility in what diagnostic could be included in the report. For a browser-based client, we can avoid the following information:

- We can avoid including traceroute hops to see a client to the service path. Users can be susceptible to their geographic location. It might be akin to collecting location information.
- We can avoid including which DNS resolver is being used. Again, details of the DNS can leak some information about the location.
- We can avoid including round-trip-time (RTT) and packet loss information.

> **Note:** As a guiding rule, we should try to collect as little information as possible, and it must only be used for the specific purpose a user gave consent for.

Ideally, for a web-based client, we should only collect the information that’s logged in the weblog when any request has been successful.

We shouldn’t use any active probing except to test the service’s standard functionality and report such probes’ results. So, traceroute and RTT or packet loss information is excluded.

Any intermediary (like ISPs or middleboxes) can’t change, add, or remove the error reporting mechanism due to encryption. Similarly, designated collectors are the only place where such data can go.

Test your knowledge!

Say “Hi” to Ed in the widget below to attempt to solve some client-side monitoring scenarios.

AI Powered

Saved

15 attempts left

Reset

You have 15 attempts to answer.

## Conclusion[#](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Conclusion)

- In a distributed system, detecting and responding to errors on the client side is difficult. So, monitoring such events is necessary to provide a good user experience.
- We can handle errors using an independent agent that sends service reports about any failures to a collector. Such collectors should be independent of the primary service in terms of infrastructure and deployment.

Design a Unique ID Generator

Design a Server-Side Monitoring Service

Ask

[Monitoring: metrics and alerting](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Monitoring-metrics-and-alerting)

[Metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Metrics)

[Populate the metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Populate-the-metrics)

[Persist the data](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Persist-the-data)

[Application metrics](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Application-metrics)

[Alerting](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Alerting)

[Client-side errors](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Client-side-errors)

[Failures due to a routing bug](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Failures-due-to-a-routing-bug)

[Design of a client-side monitoring system](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Design-of-a-client-side-monitoring-system)

[Initial design](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Initial-design)

[Issues with probers](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Issues-with-probers)

[Improve the design](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Improve-the-design)

[Activate and deactivate reports](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Activate-and-deactivate-reports)

[Reach collectors under faulty conditions](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Reach-collectors-under-faulty-conditions)

[Protect user privacy](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Protect-user-privacy)

[Conclusion](https://www.educative.io/courses/system-design-interview-prep-crash-course/design-a-client-side-monitoring-service#Conclusion)