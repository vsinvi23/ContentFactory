# WebVoyager_Architecture_Explained_with_Multimodal_ReAct_Loop

Source: https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# WebVoyager’s Architecture: A Multimodal ReAct Loop

Understand how WebVoyager uses a multimodal ReAct loop architecture to navigate live websites by observing, reasoning, and acting. Learn the design strategies behind its visual and textual context management, grounded action referencing, and action space, enabling robust AI agent behavior in dynamic web environments.

We'll cover the following...

- [The interaction loop](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-interaction-loop)
  - [Context management](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Context-management)
- [The observation space: Seeing and reading the web](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-observation-space-Seeing-and-reading-the-web)
  - [Screenshots as the primary input](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Screenshots-as-the-primary-input)
  - [Set-of-mark prompting: Making the visuals actionable](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Set-of-mark-prompting-Making-the-visuals-actionable)
  - [Auxiliary textual data](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Auxiliary-textual-data)
- [The action space: How the agent interacts](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-action-space-How-the-agent-interacts)

In our last lesson, we established the core challenge for a multimodal web agent as solving the “grounding problem.” Now, we’ll explore the specific architecture that the WebVoyager agent uses to tackle this challenge.

## The interaction loop[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-interaction-loop)

At its heart, WebVoyager operates in a continuous cycle of observing, thinking, and acting. This design allows it to navigate the dynamic and unpredictable environment of the live web in a flexible, step-by-step manner.

The interaction loop of WebVoyager is inspired by a powerful orchestration pattern we’ve already seen in this course: the ReAct (Reason + Act) pattern.

![The ReAct (Reason + Act) pattern first prompts the agent to generate a natural language ‘Thought’ explaining its plan, before producing the final, executable ‘Action’](002_WebVoyager_Architecture_Explained_with_Multimodal_ReAct_Loop_images/img_4d7e20e4ecb1.svg "The ReAct (Reason + Act) pattern first prompts the agent to generate a natural language ‘Thought’ explaining its plan, before producing the final, executable ‘Action’")

The ReAct (Reason + Act) pattern first prompts the agent to generate a natural language ‘Thought’ explaining its plan, before producing the final, executable ‘Action’

**Why use the ReAct pattern here?** Unlike the structured pipeline generation we saw in the last chapter, web navigation is unpredictable. Websites can change, present unexpected pop-ups, or offer multiple paths to the same goal. A rigid, pre-defined plan (like plan-and-execute) would easily fail. The ReAct pattern is the perfect fit because it allows the agent to observe the current state of the live webpage and react to it step-by-step, making it far more robust in a dynamic environment.

Instead of simply generating an action, the agent is prompted to first generate a natural language “Thought” before producing the executable “Action” code. This two-step process is crucial for its performance.

- **The thought:** This is where the agent’s reasoning is made explicit. It analyzes the current webpage, considers the user’s goal, and explains its plan for the next step.
- **The action:** This is the specific, executable command that the agent will perform, such as `Click [10]` or `Type [17]; Smart Folio for iPad`.

By separating thought from action, the agent’s behavior becomes more transparent and easier to debug. It forces the LMM to “think before it acts,” leading to more deliberate and accurate decision-making.

### Context management[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Context-management)

A key challenge for any agent that operates over multiple steps is managing its memory, or context. As the agent navigates through a website, the history of its actions and observations can become very long. If the entire history is fed back to the LLM at every step, it can become confused by outdated information from previous pages.

To solve this, WebVoyager uses a context clipping strategy:

![To manage its memory, WebVoyager uses a context clipping strategy. It keeps a full history of its thoughts and actions but only focuses on the three most recent observations (screenshots) to avoid getting confused by outdated information.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "To manage its memory, WebVoyager uses a context clipping strategy. It keeps a full history of its thoughts and actions but only focuses on the three most recent observations (screenshots) to avoid getting confused by outdated information.")

To manage its memory, WebVoyager uses a context clipping strategy. It keeps a full history of its thoughts and actions but only focuses on the three most recent observations (screenshots) to avoid getting confused by outdated information.

- It keeps the entire history of its thoughts and actions. This provides a complete record of its reasoning process.
- However, it only includes the three most recent observations (i.e., the last three screenshots) in its context. This ensures the agent is focused on the current state of the webpage, reducing the risk of confusion from old visual data.

To solve this, WebVoyager uses a context clipping strategy that keeps the entire history of thoughts and actions while only including the three most recent observations (i.e., screenshots) in the prompt to the LLM. This balances the need for long-term memory with a focused, uncluttered context for making the next decision.

This strategic approach to memory management is a key design choice that helps the agent stay focused and effective, even during long and complex tasks.

**Design principle: The focus vs. recall trade-off**

- **Large context (high recall):** Giving an agent its entire history provides maximum recall, but it increases costs and the risk of the agent becoming confused by outdated information from previous pages.
- **Small context (high focus):** Giving the agent only recent history keeps it focused on the current task, reduces costs, and lowers the chance of confusion. The trade-off is that it might forget crucial information from much earlier steps.

## The observation space: Seeing and reading the web[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-observation-space-Seeing-and-reading-the-web)

For an agent to act intelligently, it must first have a clear and accurate perception of its environment. For WebVoyager, this “observation space” is a clever combination of both visual and textual information, designed to give the LMM a rich, human-like understanding of the webpage.

### Screenshots as the primary input[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Screenshots-as-the-primary-input)

Similar to how we browse the web, WebVoyager’s primary source of information is the screenshot of the current webpage. This visual-first approach is a key design choice because it allows the agent to perform two functions as mentioned below.

- **Understand layout and design:** It can see the spatial relationships between elements, which is information that is very difficult to extract from raw HTML.
- **Avoid noisy code:** It sidesteps the problem of parsing massive, complex HTML documents, which can be verbose and confusing for an LLM.

### Set-of-mark prompting: Making the visuals actionable[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Set-of-mark-prompting-Making-the-visuals-actionable)

To solve the “grounding problem,” WebVoyager uses a powerful technique that we can generalize into a reusable design pattern.

**Design pattern: Grounded action referencing**

This pattern works by overlaying a visual environment with a set of simple, structured labels (like the numerical tags `[17]`, `[46]`). Instead of trying to describe a target in natural language (“the blue search button near the middle of the page”), the agent can reference a clear, unambiguous label (`Click [17]`). This dramatically simplifies the grounding task and reduces errors.

In WebVoyager, a script automatically draws bounding boxes with numerical labels around most interactive elements. This technique is inspired by Set-of-Mark prompting. Before the screenshot is sent to the LMM, the script automatically draws bounding boxes around all the interactive elements on the page (like buttons, links, and input fields). Each box is then given a unique numerical label.

![To solve the grounding problem, a technique called Set-of-Mark prompting is used. A script automatically overlays the screenshot with bounding boxes and unique numerical labels for every interactive element, creating unambiguous targets for the agent’s actions .](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "To solve the grounding problem, a technique called Set-of-Mark prompting is used. A script automatically overlays the screenshot with bounding boxes and unique numerical labels for every interactive element, creating unambiguous targets for the agent’s actions .")

To solve the grounding problem, a technique called Set-of-Mark prompting is used. A script automatically overlays the screenshot with bounding boxes and unique numerical labels for every interactive element, creating unambiguous targets for the agent’s actions .

This simple but powerful technique makes the visual information actionable. The LMM can now refer to a specific element by its number, creating a clear and unambiguous way to ground its actions. For example, instead of vaguely saying “click the search button,” it can now say, “Click `[46]`.”

### Auxiliary textual data[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Auxiliary-textual-data)

While the visual information is primary, text is still crucial. Along with the marked-up screenshot, the agent also receives a list of auxiliary text. This list includes the text content associated with each numbered element, the element type (e.g., `<input>`, `<button>`), and sometimes contextual clues from aria-label text.

This combination of a marked-up image and a corresponding text list gives the LMM the best of both worlds: it can “see” the layout and design of the page while also “reading” the specific content of each interactive element. This rich, multimodal observation is the foundation for its decision-making process.

**Design pattern: Dual-modality observation**

WebVoyager’s approach of combining a screenshot (vision) with a list of corresponding text (structured metadata) is a powerful and generalizable pattern. By providing the LLM with both modalities, the agent gets the best of both worlds: it understands the visual layout like a human while also having access to the precise, unambiguous text associated with each element. This pattern is highly effective for any task that involves interacting with a graphical user interface, from web browsing to robotics.

## The action space: How the agent interacts[#](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-action-space-How-the-agent-interacts)

Once our agent has a clear, multimodal understanding of the webpage, it needs a set of capabilities to interact with it. This set of capabilities is known as the **action space**.

For WebVoyager, the action space is designed to mirror the most common actions a human user would take while browsing the web. Crucially, by using the numerical labels from the Set-of-Mark prompting technique, the agent can specify its actions in a concise and clear format, which helps solve the “grounding problem.”

The agent has seven core actions it can perform:

![The agent’s action space consists of seven core capabilities that mirror common browsing behaviors, including clicking, typing, and a final ‘Answer’ action to complete the task.](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The agent’s action space consists of seven core capabilities that mirror common browsing behaviors, including clicking, typing, and a final ‘Answer’ action to complete the task.")

The agent’s action space consists of seven core capabilities that mirror common browsing behaviors, including clicking, typing, and a final ‘Answer’ action to complete the task.

1. **Click [**`numerical_label`**]:** This is the most common action. The agent clicks on the element corresponding to the provided numerical label, such as a link or a button.
2. **Input [**`numerical_label`**], [content]:** This is a two-part action. The agent first selects a text box (identified by its numerical label) and then types the specified content into it.
3. **Scroll [**`numerical_label` **or window], [up or down]:** The agent can scroll either the main browser window or a specific scrollable element on the page (identified by its numerical label).
4. **Wait:** This is a simple but important action. The agent can choose to wait for a moment to allow a webpage to finish loading before it proceeds.
5. **Back:** This action allows the agent to return to the previously visited page, just like clicking the “back” button in a browser.
6. **Jump to search engine:** If the agent gets stuck or can’t find the information it needs on the current site, it has a way to recover. This action allows it to navigate to a search engine to start a new search.
7. **Answer [content]:** Once the agent determines that it has successfully completed the user’s task, it uses this final action to provide the answer and terminate the workflow.

This well-defined action space, combined with the agent’s multimodal perception, gives WebVoyager a robust and flexible way to navigate the complexities of the live web.

In our next lesson, we’ll walk through a step-by-step comparison of how this multimodal agent tackles a real-world task that often causes text-only agents to fail.

The Multimodal Web Agent Challenge

Text vs. Multimodal Web Agents in a Real-World Task

Ask

[The interaction loop](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-interaction-loop)

[Context management](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Context-management)

[The observation space: Seeing and reading the web](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-observation-space-Seeing-and-reading-the-web)

[Screenshots as the primary input](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Screenshots-as-the-primary-input)

[Set-of-mark prompting: Making the visuals actionable](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Set-of-mark-prompting-Making-the-visuals-actionable)

[Auxiliary textual data](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#Auxiliary-textual-data)

[The action space: How the agent interacts](https://www.educative.io/courses/agentic-ai-systems/webvoyagers-architecture-a-multimodal-react-loop#The-action-space-How-the-agent-interacts)