# Introduction_to_Domain_Name_System_(DNS)

Source: https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Introduction to Domain Name System (DNS)

Define the Domain Name System (DNS) as the Internet’s naming service that translates human-friendly domain names into machine-readable IP addresses. Explore the fundamental concepts of DNS infrastructure, including name servers, resource records, and the importance of caching and hierarchy for scalability.

We'll cover the following...

- [The origins of DNS](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#The-origins-of-DNS)
- [What is DNS?](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#What-is-DNS)
- [Important details](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#Important-details)

## The origins of DNS[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#The-origins-of-DNS)

Mobile phones associate a unique number with each user. As contacts grow, we rely on a contact list rather than memory. Similarly, computers are identified by IP addresses (e.g., `104.18.2.119`). Because humans cannot easily remember IP addresses for every website, we need a directory to map domain names (like [educative.io](https://www.educative.io/)) to IP addresses. The Domain Name System (DNS) serves as this phone book for the internet.

![Using a phone book analogy to understand domain name system (DNS)](001_Introduction_to_Domain_Name_System_(DNS)_images/img_a6457ff02d91.svg "Using a phone book analogy to understand domain name system (DNS)")

Using a phone book analogy to understand domain name system (DNS)

## What is DNS?[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#What-is-DNS)

The **Domain Name System (DNS)** is a naming service that maps human-friendly domain names to machine-readable IP addresses. This process is transparent to users. When you enter a domain name, the browser queries the DNS infrastructure to translate it into an IP address, then forwards the request to the destination server.

The following slides illustrate the high-level DNS workflow:

![The user requests to visit a website by entering its URL in the browser](001_Introduction_to_Domain_Name_System_(DNS)_images/img_54c5bf659b2a.svg "The user requests to visit a website by entering its URL in the browser")

1 / 7

The user requests to visit a website by entering its URL in the browser

![The browser requests the ISP to forward the DNS query to resolve the request for the IP address](001_Introduction_to_Domain_Name_System_(DNS)_images/img_259fb69a555d.svg "The browser requests the ISP to forward the DNS query to resolve the request for the IP address")

1 / 7

The browser requests the ISP to forward the DNS query to resolve the request for the IP address

![The ISP forwards the DNS query to the DNS infrastructure](001_Introduction_to_Domain_Name_System_(DNS)_images/img_fb8d33a3e8e4.svg "The ISP forwards the DNS query to the DNS infrastructure")

1 / 7

The ISP forwards the DNS query to the DNS infrastructure

![The DNS infrastructure responds with a list of IP addresses against the domain name](001_Introduction_to_Domain_Name_System_(DNS)_images/img_5ade9b6e2a1e.svg "The DNS infrastructure responds with a list of IP addresses against the domain name")

1 / 7

The DNS infrastructure responds with a list of IP addresses against the domain name

![The IP address(es) reach the browser](001_Introduction_to_Domain_Name_System_(DNS)_images/img_af0f59c203a5.svg "The IP address(es) reach the browser")

1 / 7

The IP address(es) reach the browser

This resolution occurs in milliseconds, minimizing user delay. Browsers also cache frequently used mappings to further improve speed.

AI Powered

Saved

No attempts left

Reset

![Geek Gully](001_Introduction_to_Domain_Name_System_(DNS)_images/img_9b8bf9733526.png)

DNS infrastructure return the associated IP address or addressed to browser and then browser send the request to target server which is identified using IP address

Ahan, you’ve got the core idea right—DNS translates the domain name to an IP address, which the browser uses to reach the server. It’s worth adding that DNS is a distributed system with multiple servers working independently to ensure both users get the correct, current IP address simultaneously. This happens through caching, propagation delays, and authoritative DNS records that keep everything consistent. Keep exploring!

You've used all your attempts

## Important details[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#Important-details)

Key details about DNS infrastructure include:

- **Name servers:** DNS is a distributed infrastructure, not a single server. The servers that respond to queries are called **name servers**.
- **Resource records:** The DNS database stores mappings as resource records (RR). An **RR** is the smallest unit of information requested from name servers. It contains three key fields: type, name, and value.

## Common Types of Resource Records

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Type** | **Description** | **Name** | **Value** | **Example (Type, Name, Value)** |
| A | Provides the hostname to IP address mapping | Hostname | IP address | (A, relay1.main.educative.io,104.18.2.119) |
| NS | Provides the hostname that is the authoritative DNS for a domain name | Domain name | Hostname | (NS, educative.io, dns.educative.io) |
| CNAME | Provides the mapping from alias to canonical hostname | Hostname | Canonical name | (CNAME, educative.io, server1.primary.educative.io) |
| MX | Provides the mapping of mail server from alias to canonical hostname | Hostname | Canonical name | (MX, mail.educative.io, mailserver1.backup.educative.io) |

- **Caching:** DNS employs caching at multiple layers to reduce request latency and alleviate load on the global infrastructure.
- **Hierarchy:** DNS name servers are organized hierarchically. This tree-like structure ensures scalability as the number of domains and query load increases.

We will explore the hierarchical structure and management of the DNS database in the next lesson.

Introduction to Building Blocks for Modern System Design

How the Domain Name System Works

Ask

[The origins of DNS](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#The-origins-of-DNS)

[What is DNS?](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#What-is-DNS)

[Important details](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-domain-name-system-dns#Important-details)