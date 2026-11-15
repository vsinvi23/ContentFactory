# Examples_of_Resource_Estimation

Source: https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Examples of Resource Estimation

Explore practical resource estimation by applying BOTECs to a high-scale service. Quantify server count, storage needs, and bandwidth requirements based on traffic assumptions. Learn to adjust peak load estimates using principles such as the Pareto principle to ensure System Design feasibility and manage costs.

We'll cover the following...

- [Introduction](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Introduction)
- [Number of servers required](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Number-of-servers-required)
  - [Peak capacity](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Peak-capacity)
    - [Improving the RPS of a server](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-the-RPS-of-a-server)
    - [Improving over the peak load assumption](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-over-the-peak-load-assumption)
  - [Cost of servers](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Cost-of-servers)
- [Storage requirements](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Storage-requirements)
- [Bandwidth requirements](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Bandwidth-requirements)

## Introduction[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Introduction)

We’ll now apply these resource estimation techniques to a Twitter-like service. Using baseline assumptions, we’ll estimate the required number of servers, storage capacity, and network bandwidth.

## Number of servers required[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Number-of-servers-required)

We make the following assumptions for a Twitter-like service:

**Assumptions:**

- 500 million (M) daily active users (DAU)
- Average of 20 requests per user per day
- Single server capacity (64 cores): 64,000 requests per second (RPS)

#### Estimating the Number of Servers

|  |  |  |
| --- | --- | --- |
| Daily active users (DAU) | 500 | Million |
| Requests on average / user / day | 20 |  |
| Total requests / day | f10 | Billion |
| Total requests / second | f115 | K |
| Total servers required | f2 |  |

1.

Can you identify a hidden assumption in our calculations above?

Show Answer

Did you find this helpful?

> **Plausibility test:** Always judge if numbers are reasonable. For example, estimating two servers for a service with millions of DAUs is likely incorrect.

### Peak capacity[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Peak-capacity)

Large services must handle flash crowds. To estimate peak capacity, we assume a worst-case scenario where all daily requests arrive simultaneously. More accurate estimates require request and response distributions, which are often available at the prototyping level. Alternatively, we might assume a statistical model like the Poisson distribution.

To simplify, we use DAU as a proxy for peak load in a *specific second*. This treats the total daily active users as the number of requests per second. The number of servers at peak load is calculated as follows:

Servers needed at peak load=Number of requests/secondRPS of server=10 Billion64,000=157K\text{Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of server}} = \frac{10 \ \text{Billion}}{64,000} = 157\text{K}
Servers needed at peak load=RPS of serverNumber of requests/second​=64,00010 Billion​=157K

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27301%27%20height=%27181%27/%3e)![Number of servers required for a Twitter-like service](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Number of servers required for a Twitter-like service")

Number of servers required for a Twitter-like service

If all workloads arrive simultaneously and each server handles 64,000 RPS, we would need approximately 157,000 servers. As this is likely unfeasible, we have two options to address the issue.

#### Improving the RPS of a server[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-the-RPS-of-a-server)

If the peak load assumption holds, we must increase server capacity. For example, if we are limited to 100,000 servers, we must optimize performance:

Number of requests/secondMax servers we can employ=10 Billion100,000=100,000 Requests per second per server\frac{\text{Number of requests/second}}{\text{Max servers we can employ}} = \frac{10 \ \text{Billion}}{100,000} = 100,000 \ \text{Requests per second per server}
Max servers we can employNumber of requests/second​=100,00010 Billion​=100,000 Requests per second per server

Increasing RPS from 64,000 to 100,000 requires significant engineering optimization.

Organizations often rely on extensive engineering to improve server RPS:

**Example 1:** In 2012, WhatsApp managed 2 million concurrent TCP connections per server. By 2017, they used ~700 servers (specific specifications were unclear).

**Example 2:** A research system optimized for IO sorted one trillion records in 172 minutes using only 25% of the resources of the previous record holder. This represented a 3x improvement in RPS.

These examples show that improving RPS is possible but requires focused R&D and financial investment.

#### Improving over the peak load assumption[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-over-the-peak-load-assumption)

Alternatively, we can adjust the peak load assumption. Using the Pareto principle (80/20 rule), we assume 80%80\%80% of traffic occurs within 20%20\%20% of the time. This concentrates 80%80\%80% of the peak traffic into a 4.8-hour window.

Number of requests/secondRPS of server=0.8×10 Billion4.8×60×60 Seconds64,000≈8 servers
\frac{\text{Number of requests/second}}{\text{RPS of server}} = \frac{\frac{0.8 \times 10 \ \text{Billion}}{4.8 \times 60 \times 60 \ \text{Seconds}}}{64,000} \approx 8 \ \text{servers}
RPS of serverNumber of requests/second​=64,0004.8×60×60 Seconds0.8×10 Billion​​≈8 servers

We assume requests are distributed equally within this 4.8-hour window. Concurrent requests versus spread-out requests significantly impact resource needs. Systems built on these assumptions require monitoring to ensure limits are not violated. If load exceeds predictions, we employ techniques like load-shedding, [circuit-breakers,](https://www.educative.io/courses/grokking-the-product-architecture-interview/circuit-breaker-pattern) and [throttling](https://www.educative.io/courses/grokking-the-product-architecture-interview/rate-limiting).

1.

Consider a service that hosts the dynamic, personalized website of a large news organization. Due to unexpected events, such as 9/11, flash crowds are visiting the website to find updates. It might be a situation where all the DAUs come in simultaneously.

Such a situation will clearly break our usual load assumptions. Can you think of some way to gracefully degrade the service to meet such an unexpected load?

Show Answer

Did you find this helpful?

### Cost of servers[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Cost-of-servers)

To estimate costs, we select an AWS EC2 m7i.16xlarge instance (64-core processor, 256 GB RAM, 4th-Gen Intel Xeon). The hourly cost is $3.54816 with a 1-year contract.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271421%27%20height=%27831%27/%3e)![An approximate cost of an AWS instance](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "An approximate cost of an AWS instance")

An approximate cost of an AWS instance

We use an [EC2 instance from AWS](https://aws.amazon.com/savingsplans/compute-pricing/) with the following specifications:

## EC2 Instance Specifications

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Instance Size** | **vCPU** | **Memory (GiB)** | **Instance Storage (GB)** | **Network Bandwidth (Gbps)** | **EBS Bandwidth (Gbps)** |
| m7i.16xlarge | 64 | 256 | EBS-Only | 25 | 20 |

The table below details the cost for two, eight, and 157K servers. Costs escalate quickly in the peak load scenario. In real projects, budget constraints are strict requirements.

## Cost of Servers

|  |  |  |
| --- | --- | --- |
| **Low Bound Server Cost per Hour** | **Cost Under 80–20 Assumptions per Hour** | **Peak Load Cost per Hour** |
| 2\*$3.548 = $7.096 | 8\*$3.548 = $28.38 | 157K\*$3.548 = $557,061 |

## Storage requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Storage-requirements)

We will estimate the annual storage required for new tweets using the following assumptions:

- 500M daily active users
- 3 tweets per user per day
- 10% of tweets contain images; 5% contain video (mutually exclusive)
- Average sizes: Image (200 KB), Video (3 MB)
- Tweet text and metadata: 250 bytes

Daily storage requirements are calculated as follows:

#### Estimating Storage Requirements

|  |  |  |
| --- | --- | --- |
| Daily active users (DAU) | 500 | M |
| Daily tweets | 3 |  |
| Total requests / day | f1500 | M |
| Storage required per tweet | 250 | B |
| Storage required per image | 200 | KB |
| Storage required per video | 3 | MB |
| Storage for tweets | f375 | GB |
| Storage for images | f30 | TB |
| Storage for videos | f225 | TB |
| Total storage | f255 | TB |

> - Total daily storage = 0.375TB + 30 TB + 225 TB≈255 TB0.375 \text{TB + 30 TB + 225 TB} \approx 255\ \text{TB}0.375TB + 30 TB + 225 TB≈255 TB.
> - Total annual storage = 365×255 TB = 93.08 PB365 \times 255\ \text{TB = 93.08\ PB}365×255 TB = 93.08 PB.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27461.3800000000001%27%20height=%27188%27/%3e)![The total storage required by Twitter in a year](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The total storage required by Twitter in a year")

The total storage required by Twitter in a year

## Bandwidth requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Bandwidth-requirements)

To estimate bandwidth requirements:

1. Estimate daily incoming data.
2. Estimate daily outgoing data.
3. Divide by the number of seconds in a day to determine Gbps (Gigabits per second).

**Incoming traffic:** Based on the 255 TB daily storage requirement calculated above, the incoming bandwidth is:

255×101286400×8≈24 Gbps\frac{255 \times 10^{12}}{86400} \times 8 \approx 24 \ \text{Gbps}
86400255×1012​×8≈24 Gbps

> **Note:** We multiply by 8 to convert bytes (B) into bits (b).

**Outgoing traffic:** Assume each user views 50 tweets per day. Using the same content ratios (5% video, 10% image), 50 tweets contain 2.5 videos and 5 images. With 500M DAU:

#### Estimating Bandwidth Requirements

|  |  |  |
| --- | --- | --- |
| Daily active users (DAU) | 500 | M |
| Daily tweets viewed | 50 | per user |
| Tweets viewed / second | f289 | K |
| Bandwidth required for tweets | f0.58 | Gbps |
| Bandwidth required for images | f46.24 | Gbps |
| Bandwidth required for videos | f346.8 | Gbps |
| Total bandwidth | f393.62 | Gbps |

> Twitter requires 24 Gbps24\ \text{Gbps}24 Gbps of incoming traffic and 393.62 Gbps393.62\ \text{Gbps}393.62 Gbps of outgoing traffic (assuming uncompressed uploads). Total bandwidth requirements = 24+393.62=417.62 Gbps24 + 393.62 = 417.62 \ \text{Gbps}24+393.62=417.62 Gbps.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27641%27%20height=%27151%27/%3e)![The total bandwidth required by Twitter](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The total bandwidth required by Twitter")

The total bandwidth required by Twitter

These calculations depend heavily on assumptions regarding traffic mix (text vs. media) and the read/write ratio.

1.

We came up with the number of 93 PB for storage needs per year. Is this number plausible?

Show Answer

1 / 2

This lesson provides a reusable framework for resource estimation throughout the course. Back-of-the-envelope calculations (BOTECs) help validate whether a design is feasible at a high level. In interviews, they demonstrate how you reason under uncertainty and make defensible assumptions. Interviews rely on rough estimates, but production systems use real workload metrics to refine capacity planning.

Put Back-of-the-Envelope Numbers in Perspective

Introduction to Building Blocks for Modern System Design

Ask

[Introduction](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Introduction)

[Number of servers required](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Number-of-servers-required)

[Peak capacity](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Peak-capacity)

[Improving the RPS of a server](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-the-RPS-of-a-server)

[Improving over the peak load assumption](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Improving-over-the-peak-load-assumption)

[Cost of servers](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Cost-of-servers)

[Storage requirements](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Storage-requirements)

[Bandwidth requirements](https://www.educative.io/courses/grokking-the-system-design-interview/examples-of-resource-estimation#Bandwidth-requirements)