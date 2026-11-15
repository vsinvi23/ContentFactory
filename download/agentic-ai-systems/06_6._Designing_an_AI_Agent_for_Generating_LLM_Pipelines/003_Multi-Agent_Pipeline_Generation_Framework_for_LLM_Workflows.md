# Multi-Agent_Pipeline_Generation_Framework_for_LLM_Workflows

Source: https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# The Multi-Agent Pipeline Generation Framework

Explore the architecture and strategy behind ChainBuddy’s multi-agent pipeline generation framework. Understand the planner agent’s role in creating detailed, layer-based blueprints and how specialized worker agents execute tasks to build functional LLM pipelines. Discover principles of decomposition, specialization, and human-in-the-loop safeguards for efficient and scalable AI agent system design.

We'll cover the following...

- [The planner agent: Architect of the workflow](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-planner-agent-Architect-of-the-workflow)
  - [A layer-based design](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#A-layer-based-design)
  - [Variable tracing for connections](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Variable-tracing-for-connections)
  - [The “worker” agents: Building the pipeline components](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-worker-agents-Building-the-pipeline-components)
    - [Task-specific agents: The builders](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Task-specific-agents-The-builders)
    - [Connection agents: The finishers](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Connection-agents-The-finishers)
- [The final output: An executable JSON workflow](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-final-output-An-executable-JSON-workflow)
- [Agentic design takeaway: Decomposition and specialization](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Agentic-design-takeaway-Decomposition-and-specialization)

In our last lesson, we saw how the requirement-gathering agent produces a detailed JSON object, the “work ticket,” from its conversation with us. This ticket is now ready to be sent to the “factory,” that is, the back-end multi-agent system responsible for actually building the pipeline.

But how does a team of agents coordinate to build something complex from a set of instructions? ChainBuddy’s backend uses a specific strategy for this: the plan-and-execute orchestration pattern.

This is a direct application of the [pattern introduced in Chapter 1](https://www.educative.io/editor/collection/page/10370001/4654968800673792/6164855661658112#Plan-and-execute). To understand it, let’s use an analogy: building a house. A construction project doesn’t begin with workers randomly laying bricks.

1. **The plan:** First, an architect creates a detailed blueprint. This plan lays out every room, every connection, and every component *before* any construction begins.
2. **The execution:** Only after the plan is complete do the specialized crews, plumbers, electricians, and carpenters arrive to execute their specific parts of the blueprint.

To see how this translates to a business software environment, imagine an automated customer support system. The Planner agent acts as the architect, reading a frustrated customer email and mapping out a step-by-step blueprint (e.g., Step 1: Query the billing database, Step 2: Check recent shipping logs, Step 3: Draft a refund offer). The specialized crews are individual worker agents designed strictly to execute those specific database queries or draft the email based on that exact plan.

ChainBuddy’s pipeline generation works in exactly the same way. It is inspired by “plan-and-solve” prompting, a specific technique where a detailed plan is generated before execution. While it functions like the general plan-and-execute pattern, this approach emphasizes creating a complete, step-by-step solution plan that task-specific agents can then follow without deviation.

The entire back-end is built using **LangGraph**, a library specifically chosen for its ability to create stateful, multi-agent applications that can handle cycles and ensure persistence. This is essential for building complex and adaptive agentic systems.

In the next section, we’ll meet the “architect” of this system: the planner agent.

## The planner agent: Architect of the workflow[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-planner-agent-Architect-of-the-workflow)

Once the front-end agent hands off its structured “work ticket,” the first back-end agent to act is the planner agent. Continuing our house-building analogy, this agent is the architect. It doesn’t build anything itself; instead, it takes the client’s requirements (the dictionary from the frontend) and creates a detailed, comprehensive blueprint that the other agents will follow.

![Design of the back-end LLM pipeline generation agent: The planner creates a list of tasks, which are then routed to different task-specific ‘worker’ agents (e.g., a TextFields agent, a prompt agent) for execution.](003_Multi-Agent_Pipeline_Generation_Framework_for_LLM_Workflows_images/img_43b823b61a2d.svg "Design of the back-end LLM pipeline generation agent: The planner creates a list of tasks, which are then routed to different task-specific ‘worker’ agents (e.g., a TextFields agent, a prompt agent) for execution.")

Design of the back-end LLM pipeline generation agent: The planner creates a list of tasks, which are then routed to different task-specific ‘worker’ agents (e.g., a TextFields agent, a prompt agent) for execution.

This planning process has two key components, as mentioned below.

### A layer-based design[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#A-layer-based-design)

The planner first organizes the entire workflow into a logical, layer-based design. This ensures that data flows correctly from start to finish, as later steps often depend on the outputs of earlier ones. The structure typically includes the layers mentioned below.

1. **Input layer:** This layer contains the raw, static inputs for the workflow, such as the list of personas or the text of the math question.
2. **Middle layer(s):** These layers are responsible for processing and transforming data. This is where prompt templates are combined with inputs to query the LLMs.
3. **Evaluation layer:** This final layer contains the Evaluator Nodes (like our Python Evaluator) that assess the outputs generated by the models.

By thinking in layers, the planner creates a structured and logical skeleton for the entire pipeline.

### Variable tracing for connections[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Variable-tracing-for-connections)

The planner’s second crucial job is variable tracing. Think of this as the architect carefully labeling all the pipes and wires on the blueprint to show exactly how they connect between rooms.

The planner identifies every variable in the workflow (like `{persona}` and `{math_question}`) and creates a trace that specifies:

- Which node creates the variable (its origin).
- Which node(s) use the variable (who it is consumed by).

This trace is essential because it provides a perfect set of instructions for the connection agents (which we will meet shortly), telling them exactly how to draw the connecting lines between the nodes on the canvas.

With this detailed, layered blueprint and a clear connection map in hand, the system is now ready to start the “construction.”

**Human-in-the-loop safeguard:** At this stage, the user can still review and edit the planner’s blueprint before the workers build it. This ensures that the system stays transparent and flexible, and it prevents over-reliance by keeping the human in control of the final design.

### The “worker” agents: Building the pipeline components[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-worker-agents-Building-the-pipeline-components)

With the detailed blueprint from the planner agent in hand, the system moves into the execution phase. This is where a team of specialized “worker” agents gets to work, each responsible for building a specific part of the final pipeline. Each agent receives a portion of the plan and executes its single, well-defined task.

This team is primarily composed of two types of specialists: task-specific agents and connection agents.

#### Task-specific agents: The builders[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Task-specific-agents-The-builders)

These agents are responsible for creating the actual nodes on the ChainForge canvas. Each type of node has a corresponding specialist agent that knows exactly how to build it. The main builders are mentioned below.

- **The TextFields agent:** This agent receives the plan for any Input nodes and populates them with the correct variables and data. For our example, it would create the Personas node and the Math Question node.
- **The prompt agent:** This agent’s job is to configure the Prompt Node. It takes the prompt template from the plan, sets up the input variables, and populates the list of LLMs to be queried.
- **The evaluator agent:** This is a particularly intelligent agent. It analyzes the user’s requirements from the plan and decides what kind of evaluation is needed. It can choose between creating a Python code evaluator for objective criteria (like checking a math answer) or an LLM scorer for subjective criteria (like rating the “catchiness” of a tagline), and then generates the necessary code or prompt for that evaluator. In a broader industry context, this is exactly how automated marketing systems operate. Specialized evaluator agents are deployed to instantly grade the sentiment, brand alignment, or legal compliance of thousands of generated social media posts before they are ever published

#### Connection agents: The finishers[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Connection-agents-The-finishers)

Once the task-specific agents have created all the individual nodes, the connection agents step in to assemble them into a functional pipeline.

- **The edge agent:** This agent takes the variable traces from the planner’s blueprint and uses them to create all the connections (the “edges”) between the nodes. It ensures that the output of one node flows correctly to the input of the next.
- **The layout agent:** This agent has a simple but important job: it arranges all the nodes on the canvas by setting their x and y coordinates, ensuring the final workflow is clean, organized, and easy for us to read.

Together, this team of specialists works in perfect coordination, following the architect’s blueprint to transform a set of instructions into a complete and functional pipeline.

## The final output: An executable JSON workflow[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-final-output-An-executable-JSON-workflow)

Once the planner has created the blueprint and each “worker” agent has built its assigned component, the system’s final step is to assemble all the pieces.

The individual outputs from the agents are merged into a single, complete JSON file. This file is the final, compiled workflow, and the tangible result of the entire multi-agent process. It’s not just a description of the pipeline; it is an executable file that can be loaded directly into the ChainForge interface. It can render the entire visual pipeline we saw in our first lesson, with all nodes, connections, and settings perfectly in place.

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

{

"layer\_skeleton": {

"justification": "This workflow transforms long paragraphs into catchy tweets.",

"design": [

{

"layer\_id": 1,

"name": "Input Layer",

"description": "Collects long paragraphs for tweet generation."

},

{

"layer\_id": 2,

"name": "Template Layer",

"description": "Generates prompt templates for creating concise tweets."

},

{

"layer\_id": 3,

"name": "Prompt Node Layer",

"description": "Queries LLMs using generated prompts to create tweets."

},

{

"layer\_id": 4,

"name": "Evaluation Layer",

"description": "Evaluates the tweets for adherence to character limits."

}

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A small sample of the final JSON workflow. This machine-readable file contains all the data and settings needed to render the complete pipeline in the user interface.

## Agentic design takeaway: Decomposition and specialization[#](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Agentic-design-takeaway-Decomposition-and-specialization)

The architecture of ChainBuddy’s backend provides us with a powerful design principle that goes far beyond this single case study: the power of decomposition and specialization.

Let’s return to our house-building analogy one last time. You don’t hire a single “general builder” to handle the architecture, plumbing, electrical work, and interior design. Instead, you have an architect (the planner) who designs the blueprint, and then you bring in a team of specialists (the workers), each of whom is an expert at their job.

This is exactly how ChainBuddy’s backend operates. Instead of one massive, monolithic agent trying to handle everything, the system decomposes the complex task of “building a workflow” into smaller, well-defined sub-tasks. Each sub-task is then assigned to a specialized agent that is highly optimized for that single purpose.

This design pattern offers several key advantages.

- **Manageability:** A large, complex problem becomes much easier to solve when broken down into smaller, simpler pieces.
- **Efficiency and accuracy:** Each specialized agent can be an expert at its task. The evaluator agent, for example, contains sophisticated logic for choosing the right kind of evaluation, which is a level of detail that would be hard to manage in a single, generalist agent.
- **Modularity and scalability:** The system is far easier to maintain and extend. To support a new type of node in ChainForge, the developers only need to create a new “worker” agent for it, without having to redesign the entire system.
- **Real-world applicability:** This plan-and-execute pattern is widely used in modern enterprise AI to solve complex, multi-step business problems. For example:

  - **Data engineering:** A planner agent maps out an ETL (Extract, Transform, Load) pipeline, while worker agents write extraction scripts for different databases, and connection agents link the data streams.
  - **Supply chain logistics:** A planner agent evaluates a massive shipping delay and tasks specialized worker agents to simultaneously find alternative routes, calculate new freight costs, and draft update emails to affected vendors.

By orchestrating a team of specialists, ChainBuddy demonstrates a robust and scalable architecture for tackling complex, goal-oriented tasks.

The Requirement-Gathering Chat Assistant

Evaluating ChainBuddy: Performance, Usability, and Design Insight

Ask

[The planner agent: Architect of the workflow](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-planner-agent-Architect-of-the-workflow)

[A layer-based design](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#A-layer-based-design)

[Variable tracing for connections](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Variable-tracing-for-connections)

[The “worker” agents: Building the pipeline components](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-worker-agents-Building-the-pipeline-components)

[Task-specific agents: The builders](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Task-specific-agents-The-builders)

[Connection agents: The finishers](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Connection-agents-The-finishers)

[The final output: An executable JSON workflow](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#The-final-output-An-executable-JSON-workflow)

[Agentic design takeaway: Decomposition and specialization](https://www.educative.io/courses/agentic-ai-systems/the-multi-agent-pipeline-generation-framework#Agentic-design-takeaway-Decomposition-and-specialization)