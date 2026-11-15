# System_Design_ChatGPT_System

Source: https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# System Design: ChatGPT System

ChatGPT is an advanced AI conversational application developed by OpenAI, capable of understanding natural language and generating human-like text. It excels in dialogue management, natural language understanding, personalization, and feedback integration. Designing a ChatGPT-like system involves defining functional and nonfunctional requirements, estimating resources such as servers, storage, and bandwidth, and identifying essential components like load balancers, databases, and caching systems. The system must ensure scalability, availability, reliability, and data privacy while efficiently handling user interactions and generating responses.

We'll cover the following...

- [What is ChatGPT?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#What-is-ChatGPT)
  - [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Requirements)
    - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Functional-requirements)
    - [Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Non-functional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Resource-estimation)
  - [The number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#The-number-of-servers-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Bandwidth-estimation)
    - [Incoming bandwidth](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Incoming-bandwidth)
    - [Outgoing bandwidth](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Outgoing-bandwidth)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Building-blocks-we-will-use)

## What is ChatGPT?[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#What-is-ChatGPT)

**ChatGPT** is an advanced conversational application built on a sophisticated AI language model developed by OpenAI. It understands natural language and generates human-like text to assist with various communication tasks. ChatGPT helps users by:

- Simplifying technical subjects.
- Proposing innovative ideas.
- Composing clear, well-structured text.

![ChatGPT understands context and provides relevant follow-up responses](001_System_Design_ChatGPT_System_images/img_15ba77118b8e.svg "ChatGPT understands context and provides relevant follow-up responses")

ChatGPT understands context and provides relevant follow-up responses

ChatGPT-like systems are notable for interpreting incomplete or ambiguous inputs to provide relevant, context-aware responses. Instead of relying on predefined answers, these systems use generative AI and large language models to analyze intent and patterns.

In this chapter, we will design a text-to-text generation system. While OpenAI’s specific architecture is proprietary, we will apply general principles and best practices for building similar systems. We begin by defining the core requirements.

### Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Requirements)

The backend design must address the following functional and non-functional requirements:

#### Functional requirements [#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Functional-requirements)

- **Dialogue management:** Interpret user input, maintain context, and generate relevant, human-like responses.
- **Natural language understanding (NLU):** Identify intent and extract key entities from user input.
- **Personalization:** Adapt to user preferences and history to provide tailored interactions.
- **Feedback:** Improve accuracy and performance over time using user feedback.

#### Non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Non-functional-requirements)

- **Scalability:** Handle increasing user traffic and workloads efficiently.
- **Availability:** Ensure consistent uptime for users.
- **Reliability:** Generate stable and predictable responses under varying conditions.
- **Low latency:** Minimize response times through efficient inference and caching.
- **Privacy and security:** Protect user data and ensure compliance with privacy standards.

![Functional and nonfunctional requirements of ChatGPT system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Functional and nonfunctional requirements of ChatGPT system")

Functional and nonfunctional requirements of ChatGPT system

Let’s test your understanding with the help of an AI assessment:

AI Powered

Saved

1 attempt left

Reset

Incomplete user inputs

How does the system differentiate between interpreting incomplete or ambiguous user inputs?

This is your last attempt.

We must estimate the servers, storage, and bandwidth required to operate the system smoothly.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Resource-estimation)

We will use the following assumptions to estimate resources for a large user base:

- **Users:** 1 billion total users, with 150 million daily active users (DAU)
- **Requests:** Each active user sends ~10 requests daily, totaling 1.5 billion requests per day
- **Request size:** Approximately 2 KB (mostly short text prompts)
- **Response size:** Approximately 5 KB (AI-generated replies are typically longer)

### The number of servers estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#The-number-of-servers-estimation)

First, we calculate the average requests per second (RPS) based on the daily volume:

Servers needed at peak load=Number of requests/secondRPS of server\text{ Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of server}} Servers needed at peak load=RPS of serverNumber of requests/second​

Using a standard web server capacity of 64,000 RPS (from the [back-of-the-envelope calculation](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective) section), the web tier requirements are minimal. However, this calculation applies to application servers handling connections, not the GPU servers required for inference.

Servers needed at peak load=150 million64,000≈ 2343 servers\text{Servers\ needed\ at\ peak\ load} = \frac{150 \text{ million}}{64,000} \approx \text{ 2343 servers}Servers needed at peak load=64,000150 million​≈ 2343 servers

![Number of servers required for ChatGPT](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Number of servers required for ChatGPT")

Number of servers required for ChatGPT

> **Note:** The estimation above covers application servers. Generative AI relies heavily on GPU servers for inference. For GPU requirements, refer to the [back-of-the-envelope calculations for model training](https://www.educative.io/courses/generative-ai-system-design/back-of-the-envelope-calculations-for-the-model-training).

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Storage-estimation)

Storage requirements depend on the total number of requests and the data size per request. We use the following formula:

Totalstorage=Totaldaily requests×Request size\text{Total}\_{\text{storage}} = \text{Total}\_{\text{daily}\ \text{requests}}× \text{Request size} Totalstorage​=Totaldaily requests​×Request size

Use the calculator below to estimate required resources.

#### Storage Required for Text-Based Requests on ChatGPT

|  |  |  |
| --- | --- | --- |
| Daily Active Users | 150 | million |
| Average Daily Requests per User | 10 | requests/user |
| Total Daily Requests | f1500 | million |
| Request size | 2 | KB |
| Total Storage per day | f3 | TB |

> **Note:** You can modify the highlighted value to see how storage requirements change.

Modern deep learning models are massive, requiring significant storage and compute power. For example, a model with 3 billion parameters in FP16 (16-bit floating point) format occupies around 6 GB. To enable real-time inference, these models are loaded into GPU memory, often distributed across multiple GPUs to balance the load.

![Total storage required by ChatGPT in a year](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total storage required by ChatGPT in a year")

Total storage required by ChatGPT in a year

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Bandwidth-estimation)

We calculate bandwidth separately for incoming and outgoing traffic.

#### Incoming bandwidth[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Incoming-bandwidth)

Incoming bandwidth is determined by the number of incoming requests per second and the size of each request. Since most user requests to ChatGPT are relatively short, we assume an average request size of 2 KB, as mentioned above.

The total incoming bandwidth can be calculated using the formula:

Total incoming bandwidth=Total requests/sec×Total request size\text{Total}\_{\text{ incoming bandwidth}} = \text{Total}\_{\text{ requests/sec}} \times \text{Total}\_{\text{ request size}}Total incoming bandwidth​=Total requests/sec​×Total request size​

#### The Bandwidth Required for Incoming Traffic on ChatGPT

|  |  |  |
| --- | --- | --- |
| Daily active users | 150 | million |
| Daily request per user | 10 | requests |
| Size of each incoming request | 2 | KB |
| Total requests per second (TRPS) | f17361 | TRPS |
| Total incoming bandwidth | f277.8 | Mbps |

> **Note:** Adjust the values in the table to see how incoming bandwidth varies.

#### Outgoing bandwidth[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Outgoing-bandwidth)

Outgoing bandwidth depends on the number of responses per second and the size of each response. As responses are generated dynamically based on user input, response sizes vary. For estimation, assume an average response size of 5 KB per request.

The total outgoing bandwidth can be calculated using the formula:

Total outgoing bandwidth=Total responses/sec×Total response size\text{Total}\_{\text{ outgoing bandwidth}} = \text{Total}\_{\text{ responses/sec}} \times \text{Total}\_{\text{ response size}}Total outgoing bandwidth​=Total responses/sec​×Total response size​

Outgoing bandwidth consumption is significantly higher due to the larger size of generated responses. Use the calculator below to explore these values:

#### The bandwidth required for outgoing traffic on ChatGPT

|  |  |  |
| --- | --- | --- |
| Daily active users | 150 | million |
| Daily request per user | 10 | requests |
| Size of each response | 5 | KB |
| Total responses per second (TRPS) | f17361 | TRPS |
| Total outgoing bandwidth | f694.4 | Mbps |

> **Note:** Adjust the values in the table to observe changes.

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Building-blocks-we-will-use)

Based on our requirements and estimations, we will use the following core components:

![Essential building blocks required to design a ChatGPT system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Essential building blocks required to design a ChatGPT system")

Essential building blocks required to design a ChatGPT system

1. [**Load balancers**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers)**:** Distribute user requests across multiple servers and services.
2. [**Databases**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases)**:** Store metadata and graph-structured data.
3. [**CDNs**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn)**:** Deliver static content to end users, reducing latency and server load.
4. [**Pub-sub system**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-pub-sub-abstraction)**:** Manage real-time messaging and events.
5. [**Cache**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-cache)**:** Store frequently accessed data to improve performance.

Additional components, such as an API gateway and ZooKeeper, are also critical. We will discuss the complete system design in the next lesson.

Design of a Metrics Monitoring and Alerting System

Design of a ChatGPT System

Ask

[What is ChatGPT?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#What-is-ChatGPT)

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Functional-requirements)

[Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Non-functional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Resource-estimation)

[The number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#The-number-of-servers-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Bandwidth-estimation)

[Incoming bandwidth](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Incoming-bandwidth)

[Outgoing bandwidth](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Outgoing-bandwidth)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-chatgpt-system#Building-blocks-we-will-use)