# Estimating_LLM_Inference_Capacity_and_Fleet_Size

Source: https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Estimating Inference Capacity and Fleet Size

Explore methods to estimate the infrastructure requirements for large language model inference. Understand how to calculate storage needs for model parameters and user data, evaluate GPU fleet sizes based on request rates and batching efficiencies, and estimate network bandwidth for system scalability. This lesson equips you to plan resources effectively for large-scale generative AI deployments using back-of-the-envelope calculations.

We'll cover the following...

- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Resource-estimation)
  - [Storage requirements](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Storage-requirements)
    - [Model storage](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Model-storage)
    - [User data and interaction data](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#User-data-and-interaction-data)
    - [Indexing storage](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Indexing-storage)
  - [Inference server estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Inference-server-estimation)
  - [GPU cost estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#GPU-cost-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Bandwidth-estimation)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Conclusion)

Previously, we devised a formula to estimate model training time and applied it to inference. Building on that foundation, this lesson performs quick BOTECs for the resources required to deploy an LLM at scale. We cover the following:

- Storage estimation:

  - Model storage
  - User profile data
  - User interaction data
  - Indexing storage
- Inference server and fleet estimation
- GPU cost estimation
- Network bandwidth estimation

With these calculations, we aim to estimate the end-to-end resource footprint for deploying LLMs at scale. Let’s start with resource estimation fundamentals.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Resource-estimation)

Resource estimation ensures the infrastructure can handle the expected workload efficiently while remaining cost-effective. It determines the compute, storage, and network requirements for scalability, reliability, and performance. Accurate estimation prevents over-provisioning, which inflates costs, and under-provisioning, which causes failures or poor user experience.

**Note:** These estimates depend on initial assumptions. For this course, we assume **100 million daily active users (DAU)**. These numbers will be refined as the system scales.

### Storage requirements[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Storage-requirements)

Storage covers the model itself, user profile data, and user interaction data. Production systems may also store metadata, context, logs, prompt templates, and configuration files. We focus on the most essential components.

Let’s start with estimating the model’s storage.

#### Model storage[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Model-storage)

The storage for a model depends on its parameter count and the precision used to store each parameter. Data precision can be FP64 (64-bit), FP32 (32-bit), FP16 (16-bit), or quantized (8-bit). This precision shows the size of one parameter.

Model storage=No. of parameters×Data precision\text{Model storage} = \text{No. of parameters} \times \text{Data precision}Model storage=No. of parameters×Data precision

At FP16 (2 bytes per parameter), a 3-billion-parameter model needs:

Model storage=3 B×2 Bytes=6 GB\text{Model storage} = 3 \text{ B} \times 2 \text{ Bytes} = 6 \text{ GB}Model storage=3 B×2 Bytes=6 GB

Higher precision improves accuracy but increases size and can slow inference. Quantization trades some accuracy for a smaller footprint.

#### User data and interaction data[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#User-data-and-interaction-data)

Assume each user’s profile takes 10 KB and each user makes 10 interactions per day, with each interaction stored at 2 KB:

User profile data=100 M×10 KB=1 TB\text{User profile data} = 100 \text{ M} \times 10 \text{ KB} = 1 \text{ TB}User profile data=100 M×10 KB=1 TB

User interaction data=100 M×10×2 KB=2 TB/day\text{User interaction data} = 100 \text{ M} \times 10 \times 2 \text{ KB} = 2 \text{ TB/day}User interaction data=100 M×10×2 KB=2 TB/day

#### Indexing storage[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Indexing-storage)

Fast retrieval of interaction data requires an index. Assuming a 25% overhead:

Indexing storage=2 TB×0.25=0.5 TB\text{Indexing storage} = 2 \text{ TB} \times 0.25 = 0.5 \text{ TB}Indexing storage=2 TB×0.25=0.5 TB

The model and profile data are static, so they are excluded from the daily indexing calculation. The total daily storage is:

Storage required per day=2 TB+0.5 TB=2.5 TB/day\text{Storage required per day} = 2 \text{ TB} + 0.5 \text{ TB} = 2.5 \text{ TB/day}Storage required per day=2 TB+0.5 TB=2.5 TB/day

Over a 30-day month, this is 2.5 TB×30=75 TB/month2.5 \text{ TB} \times 30 = 75 \text{ TB/month}2.5 TB×30=75 TB/month. Production systems typically add redundancy for availability, which multiplies these figures across replicas and regions.

Storage required per day=Users interaction data+Indexing storage=2 TB+0.5 TB=2.5 TB/day\begin{align\*} \text{Storage required per day} &= \text{Users interaction data} + \text{Indexing storage} \\ &= 2 \text{ TB} + 0.5 \text{ TB} \\ &=2.5 \text{ TB/day} \end{align\*}Storage required per day​=Users interaction data+Indexing storage=2 TB+0.5 TB=2.5 TB/day​

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27621%27%20height=%27171%27/%3e)![Total storage consists of the user profile and interaction data, and indexing storage](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total storage consists of the user profile and interaction data, and indexing storage")

Total storage consists of the user profile and interaction data, and indexing storage

The following calculators estimate storage for different types of data. You can change the numbers (cells in yellow) and see the change reflected in the final storage.

#### Model and profile storage

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Model parameters | 3 | Billion |
| 2 | Bytes per parameter (FP64=8, FP32=4, FP16=2, INT8=1) | 2 | Bytes |
| 3 | Model storage | f6 | GB |
| 4 | Number of users | 100 | Million |
| 5 | Profile size per user | 10 | KB |
| 6 | User profile data | f1 | TB |

Model and profile data are stored once and change slowly, so the calculator above sizes them as a one-time footprint. Interaction data accumulates every day, so the following calculator estimates the daily and monthly growth. The user count is entered only in the first calculator and reused in the second.

#### Daily interaction storage

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Number of users | 100 | Million |
| 2 | Interactions per user per day | 10 |  |
| 3 | Size per interaction | 2 | KB |
| 4 | User interaction data per day | f2 | TB |
| 5 | Indexing overhead | 25 | % |
| 6 | Indexing storage per day | f0.5 | TB |
| 7 | Total storage per day | f2.5 | TB |
| 8 | Total storage per month | f75 | TB |

### Inference server estimation[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Inference-server-estimation)

The first step is calculating the total requests per second (TRPS), which describes the average load:

TRPS=No. of users×Requests per day per user86400 seconds\text{TRPS} = \frac{\text{No. of users} \times \text{Requests per day per user}}{86400 \text{ seconds}}TRPS=86400 secondsNo. of users×Requests per day per user​

For 100 M users making 10 requests per day:

TRPS=100 M×1086400≈11,574\text{TRPS} = \frac{100 \text{ M} \times 10}{86400} \approx 11{,}574TRPS=86400100 M×10​≈11,574

This assumes requests are spread uniformly over the day, which is unrealistic. Peak load, where traffic concentrates in a short window, requires a separate estimate and is left as an exercise for the reader.

We use NVIDIA A100 GPUs for inference because they offer strong cost-effectiveness for most inference workloads. Higher-end GPUs such as the H100 are usually reserved for demanding workloads or large-scale training.

Autoregressive decoding generates one token per forward pass, and each pass must read all model weights from GPU memory. Decoding is therefore bounded by memory bandwidth, not by compute. The time per token at batch 1 is approximately:

Ttoken≈Model weight bytesMemory bandwidth\text{T}\_{\text{token}} \approx \frac{\text{Model weight bytes}}{\text{Memory bandwidth}}Ttoken​≈Memory bandwidthModel weight bytes​

For a 3B-parameter model at FP16 (6 GB of weights) on an A100 with about 2 TB/s of memory bandwidth:

Ttoken=6 GB2,000 GB/s=3 ms\text{T}\_{\text{token}} = \frac{6 \text{ GB}}{2{,}000 \text{ GB/s}} = 3 \text{ ms}Ttoken​=2,000 GB/s6 GB​=3 ms

At batch 1, a 500-token response takes about 1.5 seconds, or roughly 0.67 requests per second per GPU. Serving 11,574 requests per second this way would need about 17,000 GPUs, which shows why batching is essential.

Batching changes the math. One weight read serves every sequence in the batch, so the ideal token throughput per GPU is:

Tokens per second (ideal)=Batch size×Memory bandwidthModel weight bytes\text{Tokens per second (ideal)} = \frac{\text{Batch size} \times \text{Memory bandwidth}}{\text{Model weight bytes}}Tokens per second (ideal)=Model weight bytesBatch size×Memory bandwidth​

At batch 32, this gives about 10,667 tokens per second. Real systems do not reach this roofline because of KV-cache reads, attention computation, and kernel overhead. We assume 50% efficiency:

Tokens per second (effective)=Tokens per second (ideal)×50%≈5,333\text{Tokens per second (effective)} = \text{Tokens per second (ideal)} \times 50\% \approx 5{,}333Tokens per second (effective)=Tokens per second (ideal)×50%≈5,333

Dividing token demand by per-GPU throughput gives the fleet size:

Token demand=TRPS×Output tokens per request=11,574×500≈5.8 M tokens/s\text{Token demand} = \text{TRPS} \times \text{Output tokens per request} = 11{,}574 \times 500 \approx 5.8 \text{ M tokens/s}Token demand=TRPS×Output tokens per request=11,574×500≈5.8 M tokens/s

Inference servers required=Token demandTokens per second (effective)=5,787,0005,333≈1,086\text{Inference servers required} = \frac{\text{Token demand}}{\text{Tokens per second (effective)}} = \frac{5{,}787{,}000}{5{,}333} \approx 1{,}086Inference servers required=Tokens per second (effective)Token demand​=5,3335,787,000​≈1,086

**Note:** The 50% efficiency is an assumption, not a measured value. Benchmark the real serving stack, since its efficiency determines the fleet size more than any other input.

### GPU cost estimation[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#GPU-cost-estimation)

Once the fleet size is known, the operational cost follows directly. Cloud GPU pricing is quoted per GPU-hour, so the monthly cost is:

Monthly GPU cost=No. of GPUs×Hourly price per GPU×Hours per month\text{Monthly GPU cost} = \text{No. of GPUs} \times \text{Hourly price per GPU} \times \text{Hours per month}Monthly GPU cost=No. of GPUs×Hourly price per GPU×Hours per month

The price used here is a course assumption of **$2.00 per A100 GPU-hour** on demand. Replace it with your provider’s rate, since reserved or spot pricing can change the result substantially. Using 720 hours per month (30 days × 24 hours) and the 1,086-GPU fleet from the previous section:

Hourly fleet cost=1,086×$2.00=$2,172/hour\text{Hourly fleet cost} = 1{,}086 \times \$2.00 = \$2{,}172/\text{hour}Hourly fleet cost=1,086×$2.00=$2,172/hour

Monthly GPU cost=1,086×$2.00×720≈$1,563,840/month\text{Monthly GPU cost} = 1{,}086 \times \$2.00 \times 720 \approx \$1{,}563{,}840/\text{month}Monthly GPU cost=1,086×$2.00×720≈$1,563,840/month

Annualized, this is about $18.8 million per year. This covers GPU rental only. It excludes CPUs, memory, storage, networking, redundancy, idle capacity for peak load, and engineering overhead, all of which add to the total.

Cost scales linearly with the fleet, so efficiency is the largest lever. At 100% of the memory-bandwidth roofline, the fleet would be about 543 GPUs, or roughly $782,000 per month. Improvements in batching, quantization, and serving software move the bill in the same proportion.

#### GPU Throughput Calculator

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Number of GPUs | 1086 |  |
| 2 | Hourly price per GPU | 2 | $ |
| 3 | Hours per month | 720 | Hours |
| 4 | Hourly fleet cost | f2172 | $ |
| 5 | Monthly GPU cost | f1563840 | $ |
| 6 | Annual GPU cost | f18766080 | $ |

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Bandwidth-estimation)

To calculate ingress and egress network bandwidth for a specific amount of TRPS, we first need to assume the size of a single request. The size of a request depends on various factors such as request metadata, request headers, user input (prompt) length, etc. Generally, the size of a single request is considered to be around 2 KB. This size includes metadata, headers, and the content of the user’s request, such as the input prompt or context data, which is typically compact for most systems. These numbers give the following ingress bandwidth:

Ingress bandwidth=TRPS×Request size=11574×2 KB=23.15 MBps=23.15 MBps×8≈185 Mbps\begin{align\*} \text{Ingress bandwidth} & = \text{TRPS} \times \text{Request size} \\ &= 11574 \times \text{2 KB} \\ &=23.15 \text{ MBps} \\ &=23.15 \text{ MBps} \times 8\approx 185 \text{ Mbps} \end{align\*}Ingress bandwidth​=TRPS×Request size=11574×2 KB=23.15 MBps=23.15 MBps×8≈185 Mbps​

Egress depends on the response size. A 500-token response is about 2,000 characters of English text, which is roughly 2 KB in UTF-8. This matches the output length used in the fleet estimate. Text-to-video responses can be several MB:

Egress bandwidth=TRPS×Response size=11574×2 KB=23.15 MBps=23.15 MBps×8≈ 185 Mbps\begin{align\*} \text{Egress bandwidth} &= \text{TRPS} \times \text{Response size} \\ &= 11574 \times 2 \text{ KB} \\ &= 23.15 \text{ MBps} \\ & =23.15 \text{ MBps}\times 8\approx \ 185 \text{ Mbps} \end{align\*}Egress bandwidth​=TRPS×Response size=11574×2 KB=23.15 MBps=23.15 MBps×8≈ 185 Mbps​

The following calculator estimates the ingress and egress bandwidths for different sizes of requests and responses. We can change the numbers (cells in yellow) and see the change reflected in the final outputs.

#### Ingress and Egress Bandwidth Estimation

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | TRPS | 11574 | Requests/second |
| 2 | Request size | 2 | KB |
| 3 | Ingress bandwidth | f185.2 | Mbps |
| 4 | Egress bandwidth | f185.2 | Mbps |

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Conclusion)

This lesson introduced back-of-the-envelope calculations for deploying LLMs. With 100 million DAU, interaction data with indexing comes to about 2.5 TB per day, or 75 TB per month.

Decoding is memory-bandwidth bound. A 3B-parameter FP16 model on an A100 produces about 3 ms per token at batch 1, and batching amortizes each weight read across sequences. At batch 32 and an assumed 50% efficiency, serving 11,574 requests per second with 500-token responses needs about 1,086 A100s. At $2.00 per GPU-hour, that is roughly $1.56 million per month for GPU rental alone. Ingress and egress are each about 185 Mbps.

These are average-load baselines. Batching strategy, measured efficiency, quantization, sharding, redundancy, and peak-load planning will change the final numbers, and the efficiency assumption has the largest effect on the fleet size. Benchmark the actual serving stack before committing to a budget.

In the coming lessons, we will design systems for text-to-text, text-to-image, text-to-speech, and text-to-video generation. We will refer back to these formulas throughout the course:

> Model storage=No. of parameters×Data precision\text{Model storage} = \text{No. of parameters} \times \text{Data precision}Model storage=No. of parameters×Data precision
>
> User interaction data=Number of users×Daily interactions×Single interaction size\text{User interaction data} = \text{Number of users} \times \text{Daily interactions} \times \text{Single interaction size}User interaction data=Number of users×Daily interactions×Single interaction size
>
> TRPS=No. of users×Requests per day per user86400 seconds\text{TRPS} = \frac{\text{No. of users} \times \text{Requests per day per user}}{86400 \text{ seconds}}TRPS=86400 secondsNo. of users×Requests per day per user​
>
> Ttoken≈Model weight bytesMemory bandwidth\text{T}\_{\text{token}} \approx \frac{\text{Model weight bytes}}{\text{Memory bandwidth}}Ttoken​≈Memory bandwidthModel weight bytes​
>
> Inference servers required=TRPS×Output tokens per requestTokens per second per GPU\text{Inference servers required} = \frac{\text{TRPS} \times \text{Output tokens per request}}{\text{Tokens per second per GPU}}Inference servers required=Tokens per second per GPUTRPS×Output tokens per request​
>
> Monthly GPU cost=No. of GPUs×Hourly price per GPU×Hours per month\text{Monthly GPU cost} = \text{No. of GPUs} \times \text{Hourly price per GPU} \times \text{Hours per month}Monthly GPU cost=No. of GPUs×Hourly price per GPU×Hours per month
>
> Ingress bandwidth=TRPS×Request size\text{Ingress bandwidth} = \text{TRPS} \times \text{Request size}Ingress bandwidth=TRPS×Request size
>
> Egress bandwidth=TRPS×Response size\text{Egress bandwidth} = \text{TRPS} \times \text{Response size}Egress bandwidth=TRPS×Response size

Estimating Training Compute and Cost

Token Math and Unit Economics

Ask

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Resource-estimation)

[Storage requirements](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Storage-requirements)

[Model storage](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Model-storage)

[User data and interaction data](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#User-data-and-interaction-data)

[Indexing storage](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Indexing-storage)

[Inference server estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Inference-server-estimation)

[GPU cost estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#GPU-cost-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Bandwidth-estimation)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Conclusion)