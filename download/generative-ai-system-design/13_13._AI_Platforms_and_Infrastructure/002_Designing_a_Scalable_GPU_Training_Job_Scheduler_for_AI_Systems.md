# Designing_a_Scalable_GPU_Training_Job_Scheduler_for_AI_Systems

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a GPU Training Job Scheduler

Design a multitenant GPU training job scheduler that keeps an 8,000-GPU fleet busy. It uses guaranteed quotas with borrowing of idle capacity, gang scheduling that places each job on well-connected GPUs, and checkpoint-based recovery for preemption and hardware faults, balancing utilization, fairness, and fault tolerance.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Resource-estimation)
- [System design of a GPU training job scheduler](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-design-of-a-GPU-training-job-scheduler)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#High-level-design)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#A-detailed-system-design)
  - [Job queue and quota model](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Job-queue-and-quota-model)
  - [Gang scheduling and placement](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Gang-scheduling-and-placement)
    - [Topology-aware search](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Topology-aware-search)
    - [Why heuristics win](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Why-heuristics-win)
    - [Packing vs. spreading](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Packing-vs-spreading)
  - [Preemption and recovery](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Preemption-and-recovery)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-nonfunctional-requirements)
  - [Utilization and policy tuning](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Utilization-and-policy-tuning)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Conclusion)

Idle GPUs burn cash every minute, but filling them carelessly can make a 512-GPU training run crawl because half its processes communicate across the wrong network boundary. A GPU training scheduler prevents both failures. It acts as the control plane for an accelerator fleet in which jobs last hours or days, request resources in groups, and regularly face hardware faults, preemption, and restarts.

This lesson designs that scheduler from the interview perspective. We cover queueing, placement, preemption, checkpoint recovery, and reporting, with the system framed as a multitenant platform service rather than a single algorithm.

Unlike inference serving, training jobs are usually **gang-scheduled**, meaning the full process set must start together or not at all. They are also topology-sensitive, so placement directly changes training throughput. The scheduler therefore balances four forces at once: utilization, fairness, priority handling, and fault tolerance.

A useful mental model is an airport gate controller. Empty gates waste money, but assigning a large aircraft to the wrong gate disrupts the whole terminal. The next step is to estimate the fleet and workload before choosing policies.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-requirements)

Requirements shape every policy choice, so fix them before sizing the fleet.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Functional-requirements)

- **Job submission**: Teams submit gang jobs with a GPU count, priority class, and checkpoint settings.
- **Quotas and fairness**: Each team gets guaranteed quota, with borrowing of idle capacity and fair-share ordering.
- **Topology-aware placement**: Each gang lands in the best available block of the network.
- **Preemption and recovery**: Urgent jobs can reclaim capacity, and evicted or failed jobs resume from checkpoints.
- **Reporting**: Operators see utilization, wait time, and fairness metrics per team.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Nonfunctional-requirements)

- **Utilization**: Keep GPU utilization above 80 percent without starving large jobs.
- **Scheduling latency**: Decide each placement in under 100 ms.
- **Scalability**: Manage 8,000 GPUs and about 1,900 jobs a day, with a queue of hundreds.
- **Availability**: Replicated scheduler state with failover, and a scheduler outage must not kill running jobs.
- **Fairness**: Delivered GPU-hours track quota and fair-share targets within a tolerance.
- **Recoverability**: A hardware fault loses at most one checkpoint interval of work.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Resource-estimation)

Start with rough numbers before designing components. Assume a fleet of 1,000 nodes, each with 8 GPUs, for 8,000 GPUs total. That scale is large enough that naive scans and brute-force placement become expensive, yet small enough that centralized control with replicated state is still realistic.

Split jobs into broad bands so the scheduler can reason in classes rather than unique cases. Small jobs request 1 to 4 GPUs, medium jobs request 8 to 64 GPUs, and large jobs request 128 to 512 GPUs or more. Durations range from under an hour for experiments to multiple days for foundation-model training.

A typical day brings about 1,900 jobs: roughly 1,500 small, 400 medium, and 12 large jobs of about 256 GPUs running for a day. That consumes about 155,000 of the 192,000 available GPU-hours, or 81 percent utilization, and leaves a queue of roughly 150 to 300 waiting jobs at peak.

Duration estimates are noisy, but they still influence backfill. A bad estimate behaves like a driver saying they will leave a parking spot in five minutes and staying for two hours. Backfill quality drops because the scheduler admits work that runs past the start time planned for a large waiting job.

The scheduling loop runs every 2 seconds and scores at most 500 waiting jobs, so each decision must finish in under 100 ms. Checkpoints set the storage load. A large job's checkpoint with optimizer state is about 2 TB and is written every 30 minutes. Twelve running large jobs average about 13 GB/s, but if their writes align into a 5-minute window, the burst reaches about 80 GB/s, which exceeds a 50 GB/s shared store.

Scheduler Capacity Estimator

Change the fleet and checkpoint assumptions to see when storage becomes the bottleneck.

NodesN

nodes

GPUs per nodeg

GPUs

Jobs per dayJ

jobs

Scheduling loop intervalL

s

Running large jobsm

jobs

Checkpoint size per large jobc

TB

Checkpoint intervalt

min

Burst write windoww

min

Shared storage bandwidthB

GB/s

Total GPUsG

8,000GPUs

GPU-hours available per dayH

192,000GPU-hours

Jobs arriving per houra

79.17jobs/h

Scheduling passes per dayP

43,200passes

Average checkpoint bandwidthBa​

13.33GB/s

Burst bandwidth if writes alignBb​

80GB/s

Burst load on shared storageu

160%

The fleet has **8,000 GPUs** and receives **79.17 jobs per hour**. Checkpoints average **13.33 GB/s** but burst to **80 GB/s** if writes align, which loads shared storage to **160%**.

Do you find this helpful?

The scheduler tracks several live state dimensions.

- **Free GPUs:** These determine immediate allocatable capacity.
- **Node health:** These states filter out drained, flaky, or failed hosts.
- **Rack topology:** These relationships constrain communication-efficient placement.
- **Waiting jobs:** These supply queue scores, aging, and gang size.
- **Running jobs:** These expose reclaimable capacity and fair-share usage.
- **Checkpoint freshness:** These timestamps affect preemption cost and recovery risk.

> **Note:** Rough BOTECs shape everything downstream, including data structures, scoring windows, and how often the scheduling loop can run.

The table below lists the assumptions that drive scheduler policy.

|  |  |  |
| --- | --- | --- |
| **Item** | **Example assumption** | **Why it matters** |
| **Fleet size** | 1000 nodes | Sets the overall cluster scale and scheduling capacity. |
| **GPUs per node** | 8 | Determines node packing efficiency and placement constraints. |
| **Total GPUs** | 8000 | Defines aggregate accelerator capacity available to workloads. |
| **Job size bands** | 1 to 4, 8 to 64, 128 to 512+ | Captures small, medium, and large gang-scheduling demand patterns. |
| **Duration bands** | Under 1 hour, several hours, multi-day | Helps model turnover rate, backfill windows, and reservation planning. |
| **Teams with quotas** | 5 to 10 | Reflects multi-tenant fairness and quota enforcement complexity. |
| **Duration estimate accuracy** | Inaccurate estimates degrade backfill quality | Causes reservation collisions and longer wait times for large gang jobs. |

With fleet scale fixed, the design can move to the high-level architecture.

## System design of a GPU training job scheduler[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-design-of-a-GPU-training-job-scheduler)

Let's start with a high-level design of a GPU training job schedular.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#High-level-design)

The scheduler exposes an API where users submit job specs containing team, GPU count, priority class, duration estimate, placement constraints, and whether the job is preemptible. The request lands in a per-team queue, while the scheduler core reads queue state plus cluster state from a replicated store. A placement engine searches for feasible GPU groups, node agents launch processes, a health monitor updates node liveness, a checkpoint manager tracks recoverability, and a preemption manager handles eviction when policy requires it.

The diagram below shows the control-plane interactions.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271221%27%20height=%27606%27/%3e)![Scheduler control flow](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Scheduler control flow")

Scheduler control flow

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-functional-requirements)

Each functional requirement maps to a component in this architecture.

- **Job submission**: The submission API validates gang specs and places each job in its team's queue.
- **Quotas and fairness**: The scheduler core orders waiting jobs by priority, quota status, fair-share deficit, and age.
- **Topology-aware placement**: The placement engine searches the topology graph in the cluster state store for the best contiguous block.
- **Preemption and recovery**: The preemption manager reclaims borrowed capacity, and the checkpoint manager restores evicted or failed jobs.
- **Reporting**: The metrics pipeline turns job, placement, and health events into utilization and fairness dashboards.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#A-detailed-system-design)

The following sections detail the three core subsystems: the job queue and quota model, gang scheduling and placement, and preemption and recovery.

### Job queue and quota model[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Job-queue-and-quota-model)

The queue model needs both guarantees and opportunism.

- **Guaranteed quota:** Each team receives a minimum long-term share, usually expressed in GPU-hours or target fleet fraction.
- **Over-quota borrowing:** Idle capacity can be used by any team, but that usage is marked as reclaimable.
- **Fair share:** The system compares historical GPU-hours consumed against a team weight over a sliding window and boosts teams that are behind.
- **Aging:** Waiting time increases a job's effective score so that low-priority work does not starve forever.

A practical scoring function combines priority, quota status, fair-share deficit, and age into one sortable value. Large jobs should not hold partial resources, because a gang with only half its processes is stuck while the GPUs it holds sit idle. Instead, the scheduler plans a future start time for each large job, leaves those GPUs unreserved until then, and backfills only jobs that will finish before that time. Without that plan, a 1,024-GPU job can wait forever, because small jobs keep filling every gap.

The following illustration shows how submitted jobs flow through per-team queues and scoring, and how backfill fills the gap before a large job's planned start time.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271366%27%20height=%27521%27/%3e)![Job queue and quota model](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Job queue and quota model")

Job queue and quota model

> **Attention:** A fair queue can still produce bad outcomes if topology constraints are ignored during admission.

Once jobs are ordered, the hard problem shifts to deciding where an admitted gang can actually run.

### Gang scheduling and placement[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Gang-scheduling-and-placement)

Placement determines whether a training job runs efficiently or merely runs. A 256-GPU job spread across poor network cuts may satisfy the resource request yet waste days in slower all-reduce steps. The scheduler therefore treats placement as part of admission, not a separate afterthought.

A simple version of **gang scheduling** is all-or-nothing allocation. If a job asks for 64 GPUs, the scheduler reserves the full set atomically or gives it nothing. This avoids deadlocks, partial launches, and orphaned reservations.

Placement comes down to three linked decisions: where the gang can fit, how to search quickly, and whether to pack or spread.

#### Topology-aware search[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Topology-aware-search)

The cluster state store maintains a topology graph. Topology runs from the GPUs inside a node, to the node's NVLink domain, then to the leaf-switch group, the rack, and finally the spine. The placement engine ranks candidate groups by communication quality and fragmentation cost.

The engine first tries same-node placement for very small jobs. It then looks for a single high-bandwidth island, then a same-rack block, and only then accepts broader spread across the fabric.

#### Why heuristics win[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Why-heuristics-win)

Exhaustive search over thousands of GPUs is too slow for a busy fleet. The engine instead uses heuristics that prune impossible regions early, score feasible groups, and prefer contiguous blocks that preserve future options.

#### Packing vs. spreading[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Packing-vs-spreading)

Packing jobs tightly can reduce fragmentation and preserve large free blocks for future gangs. Spreading can isolate noisy neighbors or thermal hot spots but often leaves unusable holes across the fleet. Real schedulers switch between the two based on job size, current fragmentation, and topology pressure.

A good analogy is seating groups in a theater. Filling every other chair keeps people apart, but later a large group cannot sit together even though many seats remain. The scheduler often packs medium jobs precisely to protect future large placements.

> **Practical tip:** Use atomic reservation with an admission timeout so processes do not launch until the full gang and network slice are confirmed.

Once placement is defined, the scheduler must decide what to do when capacity disappears or a higher-priority job arrives.

### Preemption and recovery[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Preemption-and-recovery)

Preemption enters when an urgent job arrives or when the system must correct long-running over-quota usage. The scheduler should first target jobs that are both preemptible and currently consuming borrowed capacity. If that is insufficient, it can consider lower-priority work within quota, but that usually requires stricter policy controls.

Eviction should be cost-aware rather than purely priority-based. The preemption manager scores candidates using reclaimed GPU count, checkpoint recency, estimated remaining runtime, and wasted GPU-hours. A job with a fresh checkpoint and many GPUs is often cheaper to evict than a smaller job that has not checkpointed for hours. Because a gang cannot lose part of its processes, evicting one node kills the whole job, so the cost counts every GPU in the gang. Before evicting, the scheduler signals the job and allows a short grace period to checkpoint, which cuts wasted work.

That policy works only if recovery exists. The checkpoint manager writes periodic snapshots to durable object storage and records the latest consistent version in scheduler metadata. Some training stacks support incremental or differential checkpoints, which reduce write cost during long runs.

Hardware faults follow a similar path. Node agents report liveness, health daemons detect ECC or link errors, and the scheduler drains unhealthy nodes before assigning new work. It then reconciles orphaned processes, marks affected jobs for restart, and requests new placement from the scheduler core.

> **Note:** Frequent checkpoints reduce rework after failure, but they also consume storage bandwidth and can briefly slow training.

A practical policy might checkpoint multiday jobs every 30 minutes, while smaller jobs checkpoint less often, or not at all, if restart is cheaper than snapshotting.

The next section follows a multiteam scheduling sequence through these components.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Workflow-of-the-system)

Consider a fleet with several high-bandwidth topology islands and three active teams. Team A starts a 512-GPU standard job, and the placement engine finds a contiguous block within one island. The node agents launch processes only after the reservation is complete, so the gang begins together.

A 64-GPU urgent job from Team B arrives next. The queue scorer lifts it above standard work, but the scheduler cannot find a contiguous preferred block. It then asks the preemption manager for reclaimable capacity. The manager selects low-priority over-quota jobs with recent checkpoints, drains them, and releases enough GPUs for the urgent gang.

Meanwhile, Team C has a 1,024-GPU job waiting. The scheduler does not hold partial capacity for it. Instead, it plans a future start time for the job and backfills only smaller work that will finish before that time.

Now inject a node failure inside Team A's job. Health monitors detect the fault, mark the node unhealthy, and update cluster state. The scheduler terminates the affected processes, loads the latest checkpoint location, computes a new placement, and relaunches the job on healthy nodes.

> **Attention:** Recovery logic must reconcile orphaned processes. Otherwise, the scheduler may believe GPUs are free while old processes still hold memory and network ports.

The diagram below maps this flow onto the physical fleet.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271511%27%20height=%27935%27/%3e)![Fleet scheduling scenario](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Fleet scheduling scenario")

Fleet scheduling scenario

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-nonfunctional-requirements)

Each nonfunctional requirement maps to a specific mechanism. Utilization stays above 80 percent because over-quota borrowing fills idle GPUs and backfill fills the gaps before a large job's planned start. Scheduling latency stays under 100 ms because each 2-second loop scores at most 500 waiting jobs and the placement engine prunes the topology graph with heuristics instead of searching exhaustively. Scalability to 8,000 GPUs comes from reasoning in job-size bands and topology blocks rather than individual GPUs. Availability comes from replicated scheduler state with failover, and because node agents keep processes running, a scheduler outage pauses new placements without killing running jobs. Fairness comes from guaranteed quotas, fair-share weights, and aging, and recoverability comes from periodic checkpoints whose writes are staggered so bursts stay within shared storage bandwidth.

### Utilization and policy tuning[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Utilization-and-policy-tuning)

A scheduler that cannot be measured cannot be tuned. Operators need a metrics pipeline that joins job metadata, placement outcomes, node health, and restart events into a policy feedback loop.

Track the following signals continuously.

- **GPU utilization:** This captures how much expensive capacity is actually doing work.
- **Queue wait time:** This should be broken down by team, priority, and job-size band.
- **Placement quality:** This records whether jobs landed within preferred topology levels or were forced to spread wider.
- **Preemption rate:** This reveals whether urgent work is destabilizing the fleet.
- **Checkpoint overhead:** This measures storage and training slowdown introduced by snapshots.
- **Job completion time:** This captures end-to-end user impact, not just scheduler efficiency.
- **Restart count:** This highlights hardware instability and poor checkpoint policy.
- **Fairness gap:** This compares actual delivered GPU-hours against quota and fair-share targets.

Those metrics feed policy tuning. Backfill thresholds can be loosened when wait times for small jobs spike, aging can be increased when starvation appears, and checkpoint frequency can be raised for unstable racks. Reporting also needs per-team dashboards and alerts for fragmentation, drained racks, and abnormal preemption bursts.

Industry implementations often resemble Slurm in tightly coupled HPC clusters or Kubernetes with Volcano-like plugins in cloud-native environments. Both patterns surface the same trade-off: perfect fairness with poor utilization is too expensive, while greedy utilization without fairness fails operationally and politically.

A strong answer sounds like a control-plane walk-through instead of a list of features. Test your understanding with the questions below.

Knowledge Check

Q1. A 1,024-GPU job has waited for days because small jobs keep filling every gap. What is the standard fix?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Conclusion)

A GPU training scheduler controls scarce, expensive, failure-prone hardware by combining estimation, queue policy, gang admission, topology-aware placement, preemption, checkpoint recovery, and reporting. In interviews, the best answers explain how jobs move through that control plane and where the hard trade-offs appear, especially fairness vs. utilization and checkpoint cost vs. restart speed.

The good news is that this design pattern repeats across many AI infrastructure problems. Next, we move from governing training capacity to governing model outputs with the design of an AI content moderation system.

Design a GenAI Gateway

Design an AI Content Moderation System

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Resource-estimation)

[System design of a GPU training job scheduler](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#System-design-of-a-GPU-training-job-scheduler)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#High-level-design)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#A-detailed-system-design)

[Job queue and quota model](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Job-queue-and-quota-model)

[Gang scheduling and placement](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Gang-scheduling-and-placement)

[Topology-aware search](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Topology-aware-search)

[Why heuristics win](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Why-heuristics-win)

[Packing vs. spreading](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Packing-vs-spreading)

[Preemption and recovery](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Preemption-and-recovery)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Achieving-nonfunctional-requirements)

[Utilization and policy tuning](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Utilization-and-policy-tuning)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-gpu-training-job-scheduler#Conclusion)