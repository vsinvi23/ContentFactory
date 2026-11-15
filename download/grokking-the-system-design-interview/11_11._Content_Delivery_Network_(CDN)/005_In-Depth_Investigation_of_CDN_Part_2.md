# In-Depth_Investigation_of_CDN_Part_2

Source: https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# In-Depth Investigation of CDN: Part 2

Discover how CDNs achieve content consistency using mechanisms like time-to-live and adaptive leases. Analyze optimal proxy server deployment strategies, including ISP placement. Evaluate the strategic decision to use CDN as a service vs. building a specialized private CDN, like Netflix Open Connect.

We'll cover the following...

- [Content consistency in CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Content-consistency-in-CDN)
  - [Periodic polling](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Periodic-polling)
  - [Time-to-live (TTL)](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Time-to-live-TTL)
  - [Leases](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Leases)
- [Deployment](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Deployment)
  - [Placement of CDN proxy servers](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Placement-of-CDN-proxy-servers)
- [CDN as a service](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#CDN-as-a-service)
- [Specialized CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Specialized-CDN)
  - [Why Netflix built its CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Why-Netflix-built-its-CDN)

This lesson explores mechanisms for maintaining content consistency, strategies for deploying proxy servers, and the distinctions between third-party CDN services and specialized, custom-built CDNs.

## Content consistency in CDN[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Content-consistency-in-CDN)

Proxy servers must remain consistent with origin servers to prevent users from accessing stale data. Several mechanisms ensure data consistency depending on whether a Push or Pull model is used.

### Periodic polling[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Periodic-polling)

In the Pull model, proxy servers periodically fetch updated content from the origin. This periodic polling can waste bandwidth when content changes infrequently. The model defines a **time-to-refresh (TTR)** interval that specifies how frequently proxies revalidate or fetch updates.

### Time-to-live (TTL)[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Time-to-live-TTL)

To reduce unnecessary refresh requests from fixed TTR intervals, the **time-to-live (TTL)** mechanism assigns an expiration time to each object. Proxies serve the cached object until the TTL expires. After expiration, the proxy revalidates the object with the origin. If the object has changed, the proxy retrieves the updated version; otherwise, it continues serving the cached copy and resets the TTL.

### Leases[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Leases)

In this technique, the origin server grants a **lease** to the proxy. The lease defines a time interval during which the origin agrees to notify the proxy of any data changes. Once the lease expires, the proxy must request a renewal. This reduces message volume between the proxy and origin. Lease duration can also be dynamically optimized based on proxy load, a technique known as **adaptive leasing**.

The following section discusses the strategic placement of CDN proxy servers to enable efficient data transmission.

## Deployment[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Deployment)

Before installing a CDN facility, we must determine the optimal number of proxy servers and their best locations to maximize utility.

- What are the best locations to install proxy servers?
- How many proxy servers are required?

### Placement of CDN proxy servers[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Placement-of-CDN-proxy-servers)

Proxies should be placed in network locations with high connectivity. Two common strategies are:

- **On-premises:** Placing smaller data centers near major IXPs.
- **Off-premises:** Placing proxies directly inside ISPs networks.

Caching static content, such as movies, at ISP edge locations is feasible. However, services with rapidly growing datasets face challenges in deciding which content to cache near users. One approach is to **split TCP** to optimize long-haul content delivery. Client TCP connections terminate at edge infrastructure located near internet exchange points (IXPs). The edge infrastructure forwards traffic to central data centers over persistent, low-latency connections configured with large TCP window sizes.

This reduces client-perceived latency by avoiding the initial TCP three-way handshake and slow-start phases over long distances to primary data centers. Since the round-trip delay to the local IXP is low, the handshake overhead is negligible. Additionally, **predictive push** strategies help determine which content to proactively move closer to users.

Placement decisions rely on performance measurements. Tools like **ProxyTeller** calculate optimal locations and server counts based on hit ratio, bandwidth, and latency. Other algorithms, such as greedy, random, and hotspot strategies, are also used.

> **Note:** Akamai and Netflix popularized placing proxies inside client ISPs, often putting content just one hop away. Conversely, Google relies more on servers near IXPs, likely due to the scale and volatility of its data.

1.

What benefits could an ISP get by placing the CDN proxy servers inside their network?

Show Answer

Did you find this helpful?

## CDN as a service[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#CDN-as-a-service)

Most companies avoid building their own CDNs, opting instead for providers like Akamai, Cloudflare, or Fastly. Cloud platforms like AWS also offer accessible global CDN facilities.

Companies contract with these providers to distribute content to end users. However, relying on public CDNs introduces specific risks:

- **Outages:** Service failures are outside the content provider's control.
- **Coverage gaps:** If a provider lacks proxies in a specific region, the content provider must contract additional services or deploy private infrastructure.
- **Blocking:** Shared domains or IPs may be blocked in certain regions due to banned content from other customers.

> **Note**: Some companies, such as Netflix, build purpose-built CDNs (e.g., **Open Connect**) instead of relying on third-party providers.

## Specialized CDN[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Specialized-CDN)

While third-party services are common, some companies build specialized CDNs to control costs and performance. A specialized CDN uses Points of Presence **(PoPs)** dedicated solely to the company's content. These PoPs may function as caching servers, reverse proxies, or application delivery controllers. Although initial setup costs are high, long-term operational costs are often lower than commercial services.

Private CDNs scale to serve petabytes of content and often coexist with public CDNs. The public CDN serves as a backup during capacity shortages or failures. Netflix’s **Open Connect Appliance (OCA)** is a prominent example of a specialized video delivery CDN.

Netflix’s OCA servers do not store user data. Their primary tasks include:

- Reporting status (health, routes, and cached content) to the Open Connect control plane in AWS.
- Serving cached content directly to users.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27661%27%20height=%27351%27/%3e)![Netflix's Open Connect Appliances](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Netflix's Open Connect Appliances")

Netflix's Open Connect Appliances

The Open Connect operations team monitors all OCAs, whether situated at IXPs or embedded in ISP networks.

### Why Netflix built its CDN[#](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Why-Netflix-built-its-CDN)

Netflix transitioned to a custom CDN to address several challenges:

- **Scalability:** Commercial providers struggled to scale infrastructure fast enough to match Netflix's rapid growth.
- **Cost:** Rising streaming volumes made third-party services prohibitively expensive.
- **Security:** Custom infrastructure offers better control over data security and leakage risks.
- **Control:** A custom CDN allows end-to-end control over the video player, network path, and servers for optimal delivery.
- **Diagnostics:** Custom HTTP modules and TCP algorithms enable faster detection and troubleshooting of network issues.
- **Retention:** It enables cost-effective long-term retention of popular content, which is expensive with public CDNs.

> **Note**: Netflix achieves a hit ratio close to 95% using OCA.

The next lesson will evaluate the proposed design.

In-Depth Investigation of CDN: Part 1

Evaluation of CDN’s Design

Ask

[Content consistency in CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Content-consistency-in-CDN)

[Periodic polling](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Periodic-polling)

[Time-to-live (TTL)](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Time-to-live-TTL)

[Leases](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Leases)

[Deployment](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Deployment)

[Placement of CDN proxy servers](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Placement-of-CDN-proxy-servers)

[CDN as a service](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#CDN-as-a-service)

[Specialized CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Specialized-CDN)

[Why Netflix built its CDN](https://www.educative.io/courses/grokking-the-system-design-interview/in-depth-investigation-of-cdn-part-2#Why-Netflix-built-its-CDN)