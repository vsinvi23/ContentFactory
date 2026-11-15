# Designing_Multimodal_Web_Agents_to_Navigate_Live_Websites

Source: https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# The Multimodal Web Agent Challenge

Explore the design of multimodal web agents that navigate and interact with real-world websites using both visual screenshots and HTML analysis. Understand the grounding problem where agents must map high-level plans to specific webpage elements, and study the architecture of WebVoyager, a next-generation web agent designed to autonomously complete diverse tasks on live websites by mimicking human-like interactions.

We'll cover the following...

- [What is a web agent?](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#What-is-a-web-agent)
  - [The foundational tool: HTML](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-foundational-tool-HTML)
  - [The limitations of an HTML-only approach](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-limitations-of-an-HTML-only-approach)
  - [The rise of multimodal agents](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-rise-of-multimodal-agents)
- [The core challenge: The grounding problem](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-core-challenge-The-grounding-problem)
- [Design goals for a generalist web agent](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#Design-goals-for-a-generalist-web-agent)
- [High-level architectural overview of WebVoyager](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#High-level-architectural-overview-of-WebVoyager)

> **Problem space:** Multimodal web agents

So far in this course, we’ve seen agents designed for specific, relatively contained environments. Now, we’re going to explore a new and incredibly complex environment for agents to operate in: the live web.

## What is a web agent?[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#What-is-a-web-agent)

A **web agent** is an autonomous system designed to navigate and interact with real-world websites to complete tasks on behalf of a user. Unlike a simple web scraper that just extracts data, a true web agent can perform actions like a human: clicking buttons, typing in forms, and making decisions based on what it sees.

![A web agent must be able to perform actions like a human, such as clicking buttons, to complete its tasks](001_Designing_Multimodal_Web_Agents_to_Navigate_Live_Websites_images/img_4a40417e9064.svg "A web agent must be able to perform actions like a human, such as clicking buttons, to complete its tasks")

A web agent must be able to perform actions like a human, such as clicking buttons, to complete its tasks

Our goal in this chapter is to design an agent that, given a high-level instruction like “Find the cheapest flight from New York to London next Tuesday,” can autonomously browse a website and return a final answer.

### The foundational tool: HTML[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-foundational-tool-HTML)

To perform any action, an agent must first understand the structure of a webpage. The primary source for this understanding is the website’s HTML (Hypertext Markup Language).

HTML is the skeleton of a webpage. For an agent, it’s an incredibly valuable source of signals because it explicitly defines the interactive elements on a page. By parsing the HTML, an agent can perform a number of functions outlined below.

- **Identify elements:** It can see every button, input field, link, and image on the page.
- **Understand element types:** It knows the difference between a clickable `<button>` and a fillable `<input type="text">`.
- **Extract textual content:** It can read the text labels on buttons and links, which is crucial for understanding their function.

For early web agents, HTML was the only way they could perceive their environment. However, as websites grew more complex, it became clear that relying on HTML alone was not enough.

### The limitations of an HTML-only approach[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-limitations-of-an-HTML-only-approach)

While HTML provides the raw structure, it has serious drawbacks when used as the sole source of information for a web agent.

- **It’s verbose and noisy:** Modern HTML is often massive and filled with complex code for styling and scripts, making it difficult for an LLM to find the important signals. A single webpage could contain hundreds of thousands of tokens of code.
- **It lacks visual context:** The way a website looks, its layout, colors, and design, provides a huge amount of information that is completely lost in the raw code. Important context from images is also missing. An agent that only reads HTML is essentially unaware of the final, rendered user experience.

Because of these issues, text-only web agents often struggle to navigate complex, modern websites. This fundamental limitation led to the next major evolution in agent design.

### The rise of multimodal agents[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-rise-of-multimodal-agents)

The recent development of Large Multimodal Models (LMMs) like GPT-4V has opened up a brand new, more human-like approach to web agents.

![A text-only agent is unaware, and perceiving the web as a complex wall of HTML code while a multimodal agent can see the rendered webpage, giving it a richer, more human-like understanding of the environment](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A text-only agent is unaware, and perceiving the web as a complex wall of HTML code while a multimodal agent can see the rendered webpage, giving it a richer, more human-like understanding of the environment")

A text-only agent is unaware, and perceiving the web as a complex wall of HTML code while a multimodal agent can see the rendered webpage, giving it a richer, more human-like understanding of the environment

Instead of just reading the code, these agents can see the webpage by processing a screenshot of how it’s rendered in the browser. This visual understanding is a game-changer because:

- It’s more intuitive and information-dense, much closer to how humans browse.
- It allows the agent to understand visual cues, layout, and the context of images, which are critical for effective navigation.

This multimodal approach is incredibly promising, but it also introduces a new and fundamental challenge.

## The core challenge: The grounding problem[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-core-challenge-The-grounding-problem)

The ability for an agent to “see“ a webpage is a major leap forward. However, it also creates a fundamental challenge that we, as agent designers, must solve, and that is the grounding problem.

Let’s use a new analogy of a busy restaurant kitchen.

Imagine the head chef (our LMM) looks at a new order ticket and creates a high-level plan. The chef says to a line cook, “Sauté the vegetables for table seven's order.” This is a perfect, high-level instruction. The *what* is clear. This is action generation.

Now, the line cook (our agent’s execution system) has to turn that instruction into a physical action. The cook looks at the crowded kitchen counter and sees:

- Three different pans.
- Bowls of prepped vegetables for table five, table six, and table seven.
- Multiple burners on the stove.

The simple instruction “Sauté the vegetables” is not enough. The cook must ground that command in the physical world. This means correctly identifying:

- Which pan to use.
- Which specific bowl of vegetables corresponds to table seven.
- Which burner to turn on.

If the cook grabs the wrong vegetables, the entire plan fails, even though the head chef’s instruction was perfectly correct.

This is precisely the challenge a multimodal web agent faces. Its process for taking any action is split into these two distinct steps.

1. **Action generation (The “what”):** The LMM acts as the “head chef.” It looks at the screenshot, understands the user’s goal, and generates a clear, high-level plan in natural language. For example, it might correctly think, “I need to click the ‘Search’ button to proceed.”
2. **Action grounding (The “which”):** The agent’s execution system must now act as the “line cook.” It looks at the visually complex webpage, a crowded kitchen of similar-looking buttons, links, and forms, and must connect, or ground, the LMM’s textual plan (“click the ‘Search’ button”) to a single, specific, clickable HTML element on the page.

The research in the SeeAct paper found that modern LMMs like GPT-4V are remarkably good at the first step, generating the correct plan. However, they often struggle with the second step. Reliably identifying the exact correct element on a webpage with dozens of interactive components is the primary bottleneck holding back their performance.

Solving this grounding problem is the key to unlocking the full potential of multimodal web agents.

## Design goals for a generalist web agent[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#Design-goals-for-a-generalist-web-agent)

Given the challenges we’ve discussed, the limitations of HTML and the critical “grounding problem,” what should the design goals of a truly capable web agent be? The WebVoyager paper gives us a clear blueprint for what a modern, generalist web agent should aim to achieve.

- **End-to-end task completion:** The agent must be able to handle a user’s instruction from start to finish without needing human intervention. It should autonomously navigate multiple pages and perform a series of actions to complete the goal.
- **Operate on real-world websites:** The agent should not be limited to simplified simulators or static, cached webpages. It must be robust enough to operate on the live, dynamic, and often messy websites that humans use every day.
- **Generalize across diverse tasks:** A true generalist agent should be able to apply its capabilities to a wide variety of websites and tasks without requiring task-specific training or fine-tuning for each one.
- **Mimic human-like interaction:** To overcome the limitations of a text-only approach, the agent’s primary mode of perception should be visual. By processing screenshots, it can interact with web interfaces in a way that is much closer to how a human user does.

## High-level architectural overview of WebVoyager[#](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#High-level-architectural-overview-of-WebVoyager)

To meet these ambitious design goals, WebVoyager is built on a simple yet powerful architectural loop. This design is a direct response to the “grounding problem” we explored earlier.

At its core, the WebVoyager agent operates in a continuous cycle that mirrors the ReAct pattern:

![High-level architecture of WebVoyager: The WebVoyager agent operates in a continuous loop. It observes the webpage with both a screenshot and text, forms a thought about what to do next, and then executes a specific action on the live site](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "High-level architecture of WebVoyager: The WebVoyager agent operates in a continuous loop. It observes the webpage with both a screenshot and text, forms a thought about what to do next, and then executes a specific action on the live site")

High-level architecture of WebVoyager: The WebVoyager agent operates in a continuous loop. It observes the webpage with both a screenshot and text, forms a thought about what to do next, and then executes a specific action on the live site

1. **Observation:** At each step, the agent perceives its environment using two sources of information: a screenshot of the current webpage and a list of text from interactive web elements on that page.
2. **Thought:** This multimodal observation is fed into a Large Multimodal Model (LMM). The LMM analyzes the information and generates a “thought,” a natural language plan for what to do next.
3. **Action:** Based on its thought, the LMM then generates a specific, executable action, such as clicking an element or typing in a form field.

This loop of Observe -> Think -> Act,repeats until the agent determines that it has successfully completed the user’s instruction. This architecture allows the agent to dynamically react to changes on the webpage, making it far more adaptable than the older, and more rigid designs.

In the next lesson, we’ll examine each component of the architecture, exploring how WebVoyager perceives the web, reasons through information, and takes action.

Develop a Multi-Agent Research Assistant Using AutoGen

WebVoyager’s Architecture: A Multimodal ReAct Loop

Ask

[What is a web agent?](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#What-is-a-web-agent)

[The foundational tool: HTML](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-foundational-tool-HTML)

[The limitations of an HTML-only approach](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-limitations-of-an-HTML-only-approach)

[The rise of multimodal agents](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-rise-of-multimodal-agents)

[The core challenge: The grounding problem](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#The-core-challenge-The-grounding-problem)

[Design goals for a generalist web agent](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#Design-goals-for-a-generalist-web-agent)

[High-level architectural overview of WebVoyager](https://www.educative.io/courses/agentic-ai-systems/the-multimodal-web-agent-challenge#High-level-architectural-overview-of-WebVoyager)