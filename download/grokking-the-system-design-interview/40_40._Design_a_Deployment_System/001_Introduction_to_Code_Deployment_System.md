# Introduction_to_Code_Deployment_System

Source: https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Introduction to Code Deployment System

A code deployment system automates the distribution of software code across various environments, ensuring smooth transitions from development to production while minimizing risks. Key stages include version control, continuous integration, automated testing, and deployment to staging and production environments. Various deployment strategies, such as rolling, blue-green, and canary deployments, help manage updates with minimal downtime. Functional requirements encompass building, deploying, and monitoring code, while non-functional requirements emphasize availability, fault tolerance, and security. Resource estimation for storage, bandwidth, and server needs is crucial for efficient operation.

We'll cover the following...

- [What is a code deployment system?](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#What-is-a-code-deployment-system)
  - [Steps involved in the code deployment system](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Steps-involved-in-the-code-deployment-system)
  - [Code deployment strategies](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Code-deployment-strategies)
- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Requirements)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Functional-requirements)
  - [Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Non-functional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Bandwidth-estimation)
  - [The number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#The-number-of-servers-estimation)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Building-blocks-we-will-use)

## What is a code deployment system?[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#What-is-a-code-deployment-system)

A code deployment system, often called a **deployment pipeline** or **continuous deployment system**, automates software distribution across environments like testing, staging, and production. Its primary objective is to release code changes efficiently while minimizing disruption and risk.

This lesson introduces the fundamentals of code deployment. We’ll learn key steps in the deployment process, explore common deployment strategies, and understand how to estimate resources and requirements when designing a deployment system.

### Steps involved in the code deployment system[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Steps-involved-in-the-code-deployment-system)

A typical deployment system follows these key stages to move code from development to production:

1. **Version control:** The process begins when developers commit changes to a [version control system](https://www.educative.io/courses/getting-started-with-git-version-control) (such as Git) to manage and track the codebase.
2. **Continuous integration (CI):** Developers frequently merge changes into a shared repository. Preliminary automated tests run immediately to ensure the codebase remains stable.
3. **Build phase:** The system compiles the code, resolves dependencies, and generates deployable artifacts (binaries).
4. **Automated testing:** The deployment system runs extensive automated tests to detect regressions or defects that changes may inadvertently introduce into existing features. Automated tests are performed in this phase based on the organization’s needs and the nature of the software.

Technical Quiz

1.

How do automated tests in the deployment phase differ from those in CI?

A.

Deployment tests run only on developer machines.

B.

CI tests are optional, but deployment tests are mandatory.

C.

CI tests validate code changes early, while deployment tests validate the full system before release.

D.

CI tests focus on performance and load testing.

---

1 / 1

5. **Staging environment:** Code deploys to a staging environment that mimics production. This allows for final testing and validation before release.
6. **Deployment phase:** The system deploys approved code to the production environment. It downloads artifacts to target machines, often using feature flags or gradual rollouts to minimize risk.
7. **Monitoring and rollback:** The system continuously monitors application performance and rolls back if necessary. If issues arise, it triggers a rollback to the previous stable version.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27451%27%20height=%27391%27/%3e)![Steps involved in the code deployment system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Steps involved in the code deployment system")

Steps involved in the code deployment system

### Code deployment strategies[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Code-deployment-strategies)

Code deployment strategies determine how new code replaces old code in production. They balance downtime, risk, and user impact. Common strategies include:

- **Basic deployment:** We release new code directly to the production environment. While simple, this approach can be risky, as it provides no safety net or rollback mechanism in case issues arise. It’s generally unsuitable for large-scale or critical systems where reliability is essential.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27693%27%20height=%27156%27/%3e)![Releasing code directly to production](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Releasing code directly to production")

Releasing code directly to production

- **Multi-service deployment:** In multi-service deployment, multiple interconnected services are updated simultaneously as part of a coordinated release. This strategy ensures consistency across related services and prevents compatibility issues caused by mismatched versions. While it supports cross-service changes, coordinating the release of multiple services can be complex.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27696%27%20height=%27306%27/%3e)![Releasing multiple dependent services together or in coordination to maintain system compatibility and stability](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Releasing multiple dependent services together or in coordination to maintain system compatibility and stability")

Releasing multiple dependent services together or in coordination to maintain system compatibility and stability

- **Rolling deployment:** Gradually updates a subset of servers while the others continue serving the old version. This minimizes downtime and distributes load, but is slower than other strategies.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27982%27%20height=%27325%27/%3e)![Updating servers in batches to avoid downtime](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Updating servers in batches to avoid downtime")

Updating servers in batches to avoid downtime

- **Blue-green deployment:** Maintains two identical environments (blue and green). One serves live traffic while the other updates. This offers instant rollout and rollback but requires duplicate infrastructure.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27791%27%20height=%27390%27/%3e)![Switching traffic between two identical environments](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Switching traffic between two identical environments")

Switching traffic between two identical environments

- **Canary deployment:** Releases code to a small subset of servers or users before rolling it out to the rest. This allows early bug detection with limited impact but requires complex traffic routing and monitoring.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27585%27%20height=%27416%27/%3e)![Gradually rolling out changes to a small group before full release](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Gradually rolling out changes to a small group before full release")

Gradually rolling out changes to a small group before full release

Let’s test your understanding with the help of an AI assessment:

AI Powered

Saved

1 attempt left

Reset

Deployment strategies

How would you decide which deployment strategy to use for a system that cannot afford any downtime?

This is your last attempt.

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Requirements)

A robust code deployment system must meet the following functional and non-functional requirements.

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Functional-requirements)

- **Building code:** The system must compile code and generate binaries (potentially gigabytes in size) within a designated timeframe (e.g., 20 minutes).
- **Deploying code:** The system must deploy artifacts to thousands of machines across multiple global regions.
- **Version control integration:** It must integrate with version control systems to fetch the latest code from repositories.
- **Environment configuration:** Users must be able to manage environment-specific configurations, such as database connections and API endpoints.
- **Rollback:** The system must support reverting to previous code versions if issues arise.
- **Deployment monitoring:** It must track and report the progress and status of deployments.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27792%27%20height=%27249%27/%3e)![Functional and non-functional requirements of the code deployment system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Functional and non-functional requirements of the code deployment system")

Functional and non-functional requirements of the code deployment system

### Non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Non-functional-requirements)

- **Availability:** The system requires high availability to ensure reliability, utilizing redundancy and failover mechanisms.
- **Fault tolerance:** Failures must be handled gracefully; every build must definitively report `success` or `failure`.
- **Performance:** Deployments must complete within acceptable time limits to maintain development velocity.
- **Scalability:** The system must scale resources vertically or horizontally to handle increased load.
- **Security:** Sensitive data (like credentials) must be encrypted, and all deployment actions must be logged for accountability.

AI Powered

Saved

1 attempt left

Reset

Requirements

Why is managing environment-specific configurations critical for a deployment system?

This is your last attempt.

Now, we’ll estimate the required resources for our system based on the requirements.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Resource-estimation)

Assume engineering teams deploy hundreds of services, with thousands of deployments each day. Each build can take up to 20 minutes and produces large build artifacts.

**Note:** The 20-minute timeframe is a general guideline. Actual build times vary based on codebase size, complexity, and infrastructure (e.g., caching, build farms).

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Storage-estimation)

We estimate storage requirements based on the following assumptions:

- **Number of applications:** 200200 200
- **Frequency of deployments:** 3000 per day3000 \text{ per day}3000 per day
- **Storage required for a single build:** 20 GB20 \text{ GB}20 GB
- **Total daily storage required for binaries:**

Total storage=200×3000×20 GB = 12 PB\text{Total storage}=\text{200}\times\text{3000}\times\text{20 GB = 12 PB}Total storage=200×3000×20 GB = 12 PB

> **Note:** This is a simplistic estimation. Real-world storage needs depend on versioning, redundancy, backups, and compression.

The following calculator computes the total daily storage requirement:

#### Estimating Storage Requirements

|  |  |  |
| --- | --- | --- |
| Number of applications (code updates) | 200 | Applications or code updates |
| Frequency of deployments | 3000 | Per day |
| Storage required for single build | 20 | GB |
| Amount of storage required per day | f12 | PB |

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Bandwidth-estimation)

A build takes 20 minutes, followed by a 5-minute transfer to a regional blob store. With 2,000 machines per region, the system must distribute 20 GB binaries to all machines within that 5-minute window. We estimate the required bandwidth as follows:

Bandwidth = 20 GB5 minutes≈533.3 Mbps\text{Bandwidth = }\frac{\text{20 GB}}{\text{5 minutes}} \approx \text{533.3 Mbps}Bandwidth = 5 minutes20 GB​≈533.3 Mbps

#### Estimating Bandwidth Requirements

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Size of the single build | 20 | GB |
| 2 | Binaries replication time | 5 | minutes |
| 3 | Bandwidth required to copy binaries to each machine in a region | f533.3 | Mbps |

### The number of servers estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#The-number-of-servers-estimation)

We assume 3,000 daily deployments. If a single server handles 50 deployments per day, the total required servers are:

Number of servers=Total deployments (per day)Server’s deployment capacity=300050=60 servers\begin{align\*}
\text{Number of servers} = \frac{\text{Total deployments (per day)}} {\text{Server's deployment capacity}}
= \frac{3000}{50}
= 60 \text{ servers}
\end{align\*}Number of servers=Server’s deployment capacityTotal deployments (per day)​=503000​=60 servers​

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27259.1100000000001%27%20height=%27161%27/%3e)![The number of servers required to perform 3000 deployments per day](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The number of servers required to perform 3000 deployments per day")

The number of servers required to perform 3000 deployments per day

#### Estimating Number of Servers

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Total number of deployments | 3000 | deployments/day |
| 2 | Deployment's capacity of a server | 50 | deployments/day |
| 3 | Total number of servers required | f60 | Servers |

**Note:** These estimates vary based on codebase complexity, infrastructure (e.g., build farms, parallelism), and deployment scale.

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Building-blocks-we-will-use)

The design utilizes the following components:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27578%27%20height=%27151%27/%3e)![Building blocks required to design a code deployment system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks required to design a code deployment system")

Building blocks required to design a code deployment system

- [**Blob storage**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-a-blob-store)**:** Stores code binaries (artifacts) during build and deployment.
- [**Key-value stores**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-key-value-store)**:** Stores configuration information.
- [**Load balancers**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers)**:** Distribute user requests among servers and services.
- [**Pub-sub system**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-pub-sub-abstraction)**:** Queues code build tasks when the service is busy.
- [**Monitoring service**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-distributed-monitoring)**:** Checks the health of machines in the system.

In the next lesson, we will design the code deployment system.

Zoom System Design

Design of a Code Deployment System

Ask

[What is a code deployment system?](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#What-is-a-code-deployment-system)

[Steps involved in the code deployment system](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Steps-involved-in-the-code-deployment-system)

[Code deployment strategies](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Code-deployment-strategies)

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Functional-requirements)

[Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Non-functional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Bandwidth-estimation)

[The number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#The-number-of-servers-estimation)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-code-deployment-system#Building-blocks-we-will-use)