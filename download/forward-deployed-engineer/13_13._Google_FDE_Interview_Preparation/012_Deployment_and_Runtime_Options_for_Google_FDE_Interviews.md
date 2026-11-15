# Deployment_and_Runtime_Options_for_Google_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Deployment and Runtime

Explore the trade-offs between Agent Runtime, Cloud Run, and GKE for hosting enterprise agents. Learn to choose a runtime based on the customer’s operational capacity, networking, security, and workload needs, and to encode those constraints in deployment configuration.

We'll cover the following...

- [The three runtime options](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-three-runtime-options)
- [The constraints that drive the decision](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-constraints-that-drive-the-decision)
- [Matching runtimes to scenarios](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Matching-runtimes-to-scenarios)
- [Deploying with constraints in mind](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Deploying-with-constraints-in-mind)
- [Common deployment mistakes](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Common-deployment-mistakes)

An agent that works on a developer’s laptop is still a long way from production. In a customer environment, the agent has to run reliably for many users at once, reach private systems inside the customer’s network, meet security and compliance requirements, and fit the skills of the team that will operate it after the FDE engagement ends. The choice of runtime affects all of these, and a choice that seems convenient during a pilot can create serious problems once the system goes live.

Google Cloud offers three main options for running agents: Agent Runtime, Cloud Run, and Google Kubernetes Engine (GKE). Each is a sound choice in the right situation. FDE interviewers rarely ask which option is best in general. They ask which option fits a specific customer, and they listen for whether the answer is driven by the customer’s constraints rather than by the candidate’s personal preference.

## The three runtime options[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-three-runtime-options)

The options differ mainly in how much of the infrastructure Google manages and how much control the customer retains.

**Agent Runtime** is the managed runtime within Gemini Enterprise Agent Platform, previously known as Vertex AI Agent Engine. It is designed specifically for agents. It hosts the agent as a managed service and provides agent-specific capabilities such as Agent Sessions for conversation history, Agent Memory Bank for long-term memory, and Agent Sandbox for safe code execution. It integrates directly with the platform’s identity, governance, evaluation, and observability features. It supports agents built with ADK as well as other popular frameworks.

**Cloud Run** is Google Cloud’s serverless container platform. The agent is packaged as a container, often a web service that exposes the agent through an API, and Cloud Run handles scaling, including scaling to zero when there is no traffic. It offers more control than Agent Runtime over the application, networking, and dependencies, while still requiring no cluster management.

**GKE** is Google Cloud’s managed Kubernetes service. It provides the most control over networking, scaling, scheduling, and hardware, including GPUs for self-hosted models. It also requires the most operational expertise, since the customer’s team is responsible for the cluster configuration and workloads running on it.

|  |  |  |  |
| --- | --- | --- | --- |
| **Aspect** | **Agent Runtime** | **Cloud Run** | **GKE** |
| Management level | Fully managed, agent-specific | Serverless containers | Managed Kubernetes |
| Built-in agent services | Sessions, memory, sandbox, evaluation, observability | None by default; added by the team | None by default; added by the team |
| Control over environment | Lowest | Moderate | Highest |
| Operational effort | Lowest | Low | Highest |
| Scaling | Managed | Automatic, including scale to zero | Configurable, with autoscaling |
| GPU and self-hosted models | Not the primary use | Supported for some workloads | Full support |
| Best fit | Fast path to production for agent-first teams | Teams comfortable with containers that need more control | Customers already running Kubernetes, or with complex networking and hardware needs |

## The constraints that drive the decision[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-constraints-that-drive-the-decision)

The runtime decision is easier when it starts from the customer’s constraints rather than from the options. Several factors usually determine the choice.

|  |  |
| --- | --- |
| **Factor** | **Question to aske** |
| Operational capacity | Who will run the system after handoff? Does the customer have a platform or Kubernetes team? |
| Existing platform | Does the customer already standardize on Cloud Run or GKE for production services? |
| Networking | Does the agent need to reach on-premises systems or private services through a VPC? |
| Security and compliance | Are VPC Service Controls, customer-managed encryption keys, or specific regions required? |
| Workload pattern | Is traffic steady or bursty? Do tasks run for seconds, minutes, or longer? |
| Model hosting | Will the system call Gemini through an API, or host open models on its own hardware? |
| Agent-specific needs | How much does the system depend on managed sessions, memory, and evaluation? |

Operational capacity is often the deciding factor, and it is the one candidates most often overlook. An FDE engagement ends, and the customer’s team inherits the system. A GKE deployment with custom autoscaling and service mesh configuration may be technically excellent, but if the customer has no one who can maintain it, the deployment becomes a liability. The strongest runtime choice is one the customer can operate confidently on their own.

## Matching runtimes to scenarios[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Matching-runtimes-to-scenarios)

A few typical customer situations show how the constraints lead to a choice.

A mid-sized insurance company with a small cloud team wants an internal claims assistant built with ADK. The team has no Kubernetes experience and wants managed conversation history and evaluation. **Agent Runtime** fits, because it provides the agent-specific services the team would otherwise have to build and maintain.

A retailer already deploys its microservices on Cloud Run and has established practices for CI/CD, monitoring, and secrets. Its agent needs a custom API in front of it and specific Python libraries. **Cloud Run** fits, because it aligns with the customer’s existing practices and gives the team the container-level control it needs.

A telecom operator runs most of its platform on GKE, must reach network management systems through private connectivity, and plans to host an open model for a specific classification task alongside Gemini. **GKE** fits, because the customer already has the operational expertise and needs the networking and hardware control it provides.

These choices are not permanent or exclusive. An ADK agent’s core logic is portable, so a team can start on Agent Runtime for a pilot and move to Cloud Run or GKE later if requirements change. Many production systems also combine runtimes, for example hosting the agent on Agent Runtime, its custom MCP servers on Cloud Run, and a self-hosted model on GKE.

## Deploying with constraints in mind[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Deploying-with-constraints-in-mind)

The deployment configuration is where customer constraints become concrete. The following command deploys an agent service to Cloud Run with settings that reflect common enterprise requirements.

Shell

```
gcloud run deploy support-agent \

--source . \

--region europe-west1 \

--service-account support-agent@PROJECT_ID.iam.gserviceaccount.com \

--no-allow-unauthenticated \

--ingress internal-and-cloud-load-balancing \

--network customer-vpc \

--subnet agents-subnet \

--vpc-egress private-ranges-only \

--set-secrets CRM_API_KEY=crm-api-key:latest \

--min-instances 1 \

--max-instances 20
```

⋯

- **Line 1:** We deploy a Cloud Run service named `support-agent`.
- **Line 2:** `--source .` builds a container from the current directory, so the team does not need to write a Dockerfile for a simple service.
- **Line 3:** The region is set to `europe-west1` to meet a data residency requirement.
- **Line 4:** The service runs as a dedicated service account with only the permissions the agent needs, rather than a broad default account.
- **Line 5:** `--no-allow-unauthenticated` requires every caller to authenticate, so the agent is never publicly accessible.
- **Line 6:** Ingress is limited to internal traffic and the customer’s load balancer, which blocks direct requests from the internet.
- **Lines 7–8:** The service connects to the customer’s VPC network and subnet so it can reach private systems.
- **Line 9:** `private-ranges-only` sends traffic to private IP ranges through the VPC while public API calls, such as calls to Gemini, use the default path.
- **Line 10:** The CRM API key is loaded from Secret Manager at runtime, so it never appears in code or configuration files.
- **Line 11:** Keeping one instance running reduces cold-start latency for the first user request.
- **Line 12:** A maximum instance count caps scaling, which protects downstream systems and controls cost during traffic spikes.

Each flag answers a question a customer’s security or operations team would ask. In an interview, explaining a deployment in these terms, rather than just naming the runtime, shows that the design is ready for a real environment.

ADK includes command-line options to deploy an agent directly to Agent Runtime or Cloud Run, which is useful during development. For production, most customers deploy through their CI/CD pipeline so that every change is reviewed, tested, and traceable.

## Common deployment mistakes[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Common-deployment-mistakes)

Several mistakes recur in agent deployments. The first is choosing a runtime based on what the FDE team is most familiar with rather than what the customer can operate. The second is running the agent under a broadly privileged default service account. The third is allowing unauthenticated access during a pilot and never removing it. The fourth is ignoring private networking requirements until the agent cannot reach the systems it depends on. The last is treating the pilot deployment as production, without CI/CD, monitoring, or a clear plan for who responds when the system fails.

Agent Runtime, Cloud Run, and GKE each offer a valid path to production, and the right choice depends on the customer rather than on the technology. Agent Runtime offers the fastest route with managed agent services, Cloud Run balances control with low operational effort, and GKE provides full control for customers who need it and can support it. FDEs who start from the customer’s operational capacity, networking, security, and workload requirements, and who encode those requirements directly in the deployment configuration, produce systems the customer can run with confidence long after the engagement ends.

Enterprise Data Pipelines

Model and Context Trade-offs

Ask

[The three runtime options](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-three-runtime-options)

[The constraints that drive the decision](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#The-constraints-that-drive-the-decision)

[Matching runtimes to scenarios](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Matching-runtimes-to-scenarios)

[Deploying with constraints in mind](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Deploying-with-constraints-in-mind)

[Common deployment mistakes](https://www.educative.io/courses/forward-deployed-engineer/deployment-and-runtime#Common-deployment-mistakes)