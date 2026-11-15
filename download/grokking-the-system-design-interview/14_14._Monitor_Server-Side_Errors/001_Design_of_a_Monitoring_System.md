# Design_of_a_Monitoring_System

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design of a Monitoring System

Define the scope and requirements for a distributed monitoring system in system design. Identify key signals to track, such as service health, network latency/packet loss, and host-level hardware errors. Outline a high-level architecture with metric collectors, a query API, and a time-series database for storage.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Requirements)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Building-blocks-we-will-use)
- [High-level design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#High-level-design)

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Requirements)

The monitoring system must track the following:

- Critical local process crashes.
- Resource usage anomalies (CPU, memory, disk, network) in specific processes.
- Overall server health, including load averages and resource consumption.
- Hardware faults, such as memory failures or disk degradation.
- Connectivity to critical external services, like network file systems.
- Data center hardware status, including network switches and load balancers.
- Power consumption at the server, rack, and data center levels.
- Power events affecting servers, racks, or the data center.
- Routing information and DNS status.
- Network latency within and across data centers.
- Network status at peering points.
- Global service health across data centers (e.g., CDN performance).

Automated monitoring identifies anomalies and notifies the alert manager or updates a dashboard. Cloud providers offer similar health status pages:

- **AWS:** <https://health.aws.amazon.com/health/status>
- **Azure:** <https://status.azure.com/en-us/status>
- **Google:** <https://status.cloud.google.com/>

AI Powered

Saved

1 attempt left

Reset

Why do you need a dedicated monitoring service?

In a distributed system, why is a dedicated monitoring solution necessary instead of simply relying on individual server logs?

This is your last attempt.

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Building-blocks-we-will-use)

The design uses the following building block:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27454.43000000000006%27%20height=%27276%27/%3e)![Blob storage keeps older metrics cheaply while recent data stays queryable](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Blob storage keeps older metrics cheaply while recent data stays queryable")

Blob storage keeps older metrics cheaply while recent data stays queryable

[**Blob storage**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-a-blob-store)**:** We’ll use blob storage to store our information about metrics.

## High-level design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#High-level-design)

The monitoring service comprises these components:

- **Storage:** A time-series database stores metric data, such as CPU usage or application exceptions.
- **Data collector service:** Fetches relevant data from services and persists it to storage.
- **Querying service:** An API that queries the time-series database to retrieve data.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27750%27%20height=%27371%27/%3e)![High-level design of a monitoring system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "High-level design of a monitoring system")

High-level design of a monitoring system

The next lesson explores these components in detail.

Prerequisites of a Monitoring System

Detailed Design of a Monitoring System

Ask

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Requirements)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#Building-blocks-we-will-use)

[High-level design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-a-monitoring-system#High-level-design)