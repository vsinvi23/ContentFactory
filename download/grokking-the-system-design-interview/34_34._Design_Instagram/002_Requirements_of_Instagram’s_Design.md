# Requirements_of_Instagram’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Requirements of Instagram’s Design

Explore the critical functional and non-functional requirements for designing Instagram, a read-heavy, high-scale service. Calculate resource needs, including petabytes of storage and terabits of bandwidth, using precise back-of-the-envelope methods. Use these constraints to inform the high-level System Design decisions.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Requirements)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Functional-requirements)
  - [Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Non-functional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Bandwidth-estimation)
  - [Server count](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count)
    - [Server count assuming uniform request distribution](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-uniform-request-distribution)
    - [Server count assuming peak load](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-peak-load)
- [Try it yourself](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Try-it-yourself)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Building-blocks-we-will-use)

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Requirements)

We will focus on core features to simplify the design. The system requirements are:

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Functional-requirements)

- **Post photos and videos:** Users can post photos and videos on Instagram.
- **Follow and unfollow users:** Users can follow and unfollow other users on Instagram.
- **Like posts:** Users can like posts and remove their likes.
- **Search photos and videos:** Users can search photos and videos based on captions and location.
- **Generate news feed:** Users can view photos and videos from accounts they follow, ranked by predicted interest, with an optional chronological view. The feed can also include suggested and promoted posts.
- AI-powered Explore recommendations: Users can browse an Explore page featuring photos and videos from accounts they do not follow, selected based on their interests.

### Non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Non-functional-requirements)

- **Scalability:** The system should be scalable to handle millions of users in terms of computational resources and storage.
- **Latency:** The latency to generate a news feed should be low.
- **Availability:** The system should be highly available.
- **Durability:** Any uploaded content (photos and videos) should never get lost.
- **Consistency:** We can compromise a little on consistency. It is acceptable if the content (photos or videos) takes time to show in followers’ feeds located in a distant region.
- **Reliability:** The system must be able to tolerate hardware and software failures.

AI Powered

Saved

5 attempts left

Reset

Functional requirements

Suppose we wanted to implement a time-based expiration feature for the content on Instagram (like Snapchat). What functional requirements would we need to add or remove to reflect this feature?

You have 5 attempts to answer.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Resource-estimation)

The system is read-heavy because users browse feeds far more often than they create posts. Design priorities include storage efficiency and low-latency feed retrieval. Instagram supports roughly 1 billion users who share about 95 million posts per day.

We make the following assumptions:

- **Total users:** 1 billion (500 million daily active users)
- **Daily uploads:** 60 million photos and 35 million videos
- **File sizes:** Max 3 MB per photo, 150 MB per video
- **Traffic:** Average 20 requests per user/day

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Storage-estimation)

We estimate storage, bandwidth, and server count based on these figures.

Daily storage requirements:

60 million photos/day×3 MB=180 TB/day\text{60 million photos/day} \times \text{3 MB} = \text{180 TB/day}60 million photos/day×3 MB=180 TB/day

35 million videos/day×150 MB=5250 TB/day\text{35 million videos/day} \times \text{150 MB} = \text{5250 TB/day}35 million videos/day×150 MB=5250 TB/day

Total daily content size = 180 + 5250 = 5430 TB\text{180 + 5250 = 5430 TB}180 + 5250 = 5430 TB

Annual storage requirement:

5430 TB/day×365 (days a year)=1981950 TB=1981.95 PB\text{5430 TB/day} \times \text{365 (days a year)} = \text{1981950 TB} = \text{1981.95 PB}5430 TB/day×365 (days a year)=1981950 TB=1981.95 PB

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27871%27%20height=%27184%27/%3e)![Total storage required by the Instagram storage system for a year](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total storage required by the Instagram storage system for a year")

Total storage required by the Instagram storage system for a year

For simplicity, we omit metadata (comments, user info) and focus on the 5430 TB/day media requirement.

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Bandwidth-estimation)

Incoming data (5430 TB/day) translates to:

5430 TB24×60×60=5430 TB86400 sec≈62.84 GB/s≈502.8 Gbps\frac{\text{5430 TB}}{\text{24} \times \text{60} \times \text{60}} = \frac{\text{5430 TB}}{\text{86400 sec}} \approx \text{62.84 GB/s} \approx \text{502.8 Gbps}24×60×605430 TB​=86400 sec5430 TB​≈62.84 GB/s≈502.8 Gbps

Assuming a read-to-write ratio of 100:1100:1100:1, outgoing bandwidth is 100x incoming:

Incoming bandwidth ≈ 502.8 Gbps

Required outgoing bandwidth ≈ 100×502.8 Gbps≈50.28 Tbps\text{100} \times \text{502.8 Gbps} \approx \text{50.28 Tbps}100×502.8 Gbps≈50.28 Tbps

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27601%27%20height=%27141.67999999999995%27/%3e)![Total bandwidth required](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total bandwidth required")

Total bandwidth required

Outbound bandwidth usage is high due to frequent media delivery. Media compression can reduce file sizes before delivery. Content is cached near users through CDNs and edge caches located at IXPs and ISP networks to reduce latency during content delivery.

### Server count[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count)

Server capacity is estimated using two scenarios: a uniform request distribution (best case) and peak load conditions (worst case). These scenarios establish the lower and upper bounds for required server capacity. These bounds can be refined by adjusting traffic assumptions, for example, assuming 20% of daily requests occur during peak concurrency.

#### Server count assuming uniform request distribution[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-uniform-request-distribution)

Assume 500 million DAUs and a server capacity of 64,000 requests per second (RPS).

- Requests per user/day = 202020
- Total requests/day = 500 million×20\text{500 million} \times \text{20}500 million×20
- Requests/second = 500 million×2024×60×60≈116 K\frac{\text{500 million} \times \text{20}}{\text{24} \times \text{60} \times \text{60}} \approx \text{116 K}24×60×60500 million×20​≈116 K

Server calculation:

Servers needed for uniform requests=Number of requests/secondRPS of server\text{Servers needed for uniform requests} = \frac{\text{Number of requests/second}}{\text{RPS of server}}
Servers needed for uniform requests=RPS of serverNumber of requests/second​

Servers needed for uniform requests=116 K64,000≈2 servers\text{Servers needed for uniform requests} = \frac{\text{116 K}}{\text{64,000}} \approx \text{2 servers}
Servers needed for uniform requests=64,000116 K​≈2 servers

Under uniform distribution, approximately 2 servers are required.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27221%27%20height=%27141%27/%3e)![Number of servers required for the Instagram system under a uniform request distribution assumption](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Number of servers required for the Instagram system under a uniform request distribution assumption")

Number of servers required for the Instagram system under a uniform request distribution assumption

#### Server count assuming peak load[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-peak-load)

Using [our assumption](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective) of Daily Active Users as a proxy for peak concurrent requests (worst-case), we assume 500 million requests per second. The server count is calculated as:

Servers needed at peak load=Number of requests/secondRPS of server\text{Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of server}}
Servers needed at peak load=RPS of serverNumber of requests/second​

Servers needed at peak load=500 million64,000=7812.5≈8K servers\text{Servers needed at peak load} = \frac{\text{500 million}}{\text{64,000}} = \text{7812.5} \approx \text{8K servers}
Servers needed at peak load=64,000500 million​=7812.5≈8K servers

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27251%27%20height=%27141%27/%3e)![Number of servers required for the Instagram system under peak load assumption](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Number of servers required for the Instagram system under peak load assumption")

Number of servers required for the Instagram system under peak load assumption

> **Note:** Concurrent requests drive server needs more than average load. Refer to [Back-of-the-envelope Calculations](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective) for details on refining peak load assumptions.

## Try it yourself[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Try-it-yourself)

Let’s analyze how the number of photos per day affects the storage and bandwidth requirements. For this purpose, could you try to change the values in the following table to compute the estimates? We have set 20 requests for each user per day in the following calculation:

#### 

|  |  |
| --- | --- |
| Requirements | Calculations |
| Number of photos per day (in millions) | 60 |
| Size of each photo (in MB) | 3 |
| Number of videos per day (in millions) | 35 |
| Size of each video (in MB) | 150 |
| Number of daily active users (in millions) | 500 |
| Number of requests a server can handle per day | 691200000 |
| Storage estimation per day (in TB) | f5430 |
| Incoming bandwidth (Gb/s) | f502.8 |
| Number of servers needed | f15 |

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Building-blocks-we-will-use)

In the next lesson, we’ll focus on the high-level design of Instagram. The design will utilize many building blocks that have been discussed in the initial chapters also. We’ll use the following building blocks in our design:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27589%27%20height=%27132%27/%3e)![Building blocks used in Instagram design](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks used in Instagram design")

Building blocks used in Instagram design

- [**Load balancer**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers)**:** Distributes requests across available servers.
- [**Database:**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases) Stores user metadata and relationships.
- [**Blob storage**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-a-blob-store)**:** Stores media content like photos and videos.
- [**Task scheduler**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-task-scheduler)**:** Manages asynchronous tasks, such as cleaning up expired content.
- [**Cache:**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-cache) Stores frequently accessed content.
- [**CDN**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn)**:** Delivers content to end-users, reducing latency and server load.

In the next lesson, we’ll discuss the high-level design of the Instagram system.

System Design: Instagram

Design of Instagram

Ask

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Functional-requirements)

[Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Non-functional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Bandwidth-estimation)

[Server count](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count)

[Server count assuming uniform request distribution](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-uniform-request-distribution)

[Server count assuming peak load](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Server-count-assuming-peak-load)

[Try it yourself](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Try-it-yourself)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-instagrams-design#Building-blocks-we-will-use)