# Managing_Browser_State_for_Multimodal_Web_Agents_in_Google_ADK

Source: https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Managing the Browser State

Explore how to manage browser state in a multimodal web agent using Google ADK. Understand maintaining Playwright sessions, tracking element history, and bridging stateless LLM calls with a stateful browser to enable continuous, context-aware web interactions.

We'll cover the following...

- [The entry point: agent.py](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-entry-point-agentpy)
- [The browser runtime: Keeping the session alive](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-browser-runtime-Keeping-the-session-alive)
  - [Defining the state object](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Defining-the-state-object)
  - [Starting and accessing the browser](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Starting-and-accessing-the-browser)
  - [The singleton pattern](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-singleton-pattern)
- [Wrapping up](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Wrapping-up)

In the previous lesson, we observed the web agent seamlessly navigating, clicking, and extracting information. From the user's perspective, it looks like a single continuous session. However, under the hood, we face a fundamental architectural challenge: Large Language Models (LLMs) and their function-calling APIs are inherently stateless. Every time the LLM decides to use a tool (like `click` or `type`), it sends a standalone API request. If we were to start a new browser instance for every tool call, the agent would lose its place, its active tabs, and its login cookies.

To solve this, we must build a bridge between the stateless LLM and a highly stateful browser. In this lesson, we will explore `src/agent.py` to see how the system is launched, and then dive deep into `src/tools/browser_runtime.py` to understand how we keep the browser alive and track the agent's history across the ReAct loop.

## The entry point: `agent.py`[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-entry-point-agentpy)

Before we dive into complex state management, let's look at how the application actually starts. In Google ADK, agents are typically defined in their own modules and imported into a main entry point.

Our entry point is `src/agent.py`. It is intentionally minimal:

Ace Editor

1

2

3

4

5

"""ADK discovery entrypoint for the `src` app."""

from src.adk\_agent.web\_agent import build\_root\_agent

root\_agent = build\_root\_agent()

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The ADK application entry point (src/agent.py)

- **Line 3:** We import the factory function `build_root_agent` from our agent definition file (`src/adk_agent/web_agent.py`).
- **Line 5:** We invoke `build_root_agent()` and assign the result to `root_agent`. This variable name is automatically discovered by the ADK runtime, which binds it to the interactive UI. We will explore the implementation of this factory function in Lesson 4.

## The browser runtime: Keeping the session alive[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-browser-runtime-Keeping-the-session-alive)

When the LLM uses a tool like `capture_observation()`, the browser needs to take a screenshot. When it subsequently calls `action_click(element_id="5")`, the system needs to know which page is currently open and exactly what element "5" refers to based on the *previous* observation.

To handle this, we use the `BrowserRuntime` class.

### Defining the state object[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Defining-the-state-object)

Open `src/tools/browser_runtime.py`. The file begins by defining a dataclass to hold everything related to the current browsing session:

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

from \_\_future\_\_ import annotations

import os

from dataclasses import dataclass

from pathlib import Path

from typing import Optional

from playwright.async\_api import Browser, BrowserContext, Page, async\_playwright

@dataclass

class BrowserRuntime:

browser: Optional[Browser] = None

context: Optional[BrowserContext] = None

page: Optional[Page] = None

pw = None

last\_elements: list[dict] = None # type: ignore[assignment]

capture\_index: int = 0

last\_screenshot\_path: Optional[Path] = None

action\_history: list[str] = None # type: ignore[assignment]

visited\_urls: set[str] = None # type: ignore[assignment]

observation\_streak: int = 0

no\_progress\_streak: int = 0

last\_action\_name: str = ""

# ... Additional tracking fields omitted for brevity ...

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Core state variables in BrowserRuntime (src/tools/browser\_runtime.py)

- **Lines 1–6:** We import required modules.
- **Lines 8–9:** We use the `@dataclass` decorator to define the `BrowserRuntime` class, which stores our Playwright objects and session memory.
- **Lines 10–13:** We declare variables for the Playwright engine (`pw`), the `browser` instance, the `context` (which holds cookies and session data), and the active `page` (the current tab). They are initialized as `None`.
- **Line 14:** `last_elements` is the most important field for multimodal grounding. When the agent observes the page, we inject numeric labels onto candidate UI elements. We store their bounding boxes and selectors here so subsequent click and type commands know exactly where to interact.
- **Lines 15–16:** `capture_index` tracks how many screenshots we've taken, and `last_screenshot_path` stores the disk location of the most recent image for the Vision-Language Model (VLM) to analyze.
- **Lines 17–18:** `action_history` and `visited_urls` keep a running log of where the agent has been and which tools it has used during the session.
- **Lines 20–21:** `observation_streak` and `no_progress_streak` are counters. We use these to detect if the LLM is stuck in an infinite loop (for example, repeatedly clicking a nonresponsive element) so we can intervene.

### Starting and accessing the browser[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Starting-and-accessing-the-browser)

Because the LLM might call *any* tool first (for example, it might call `search_web` without explicitly calling an initialization tool), we need a safe way to ensure the browser is running before any web action executes.

We achieve this with the `start()` and `ensure_page()` methods:

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

async def start(self) -> None:

if self.page:

return

self.pw = await async\_playwright().start()

headless = os.getenv("BROWSER\_HEADLESS", "false").lower() == "true"

self.browser = await self.pw.chromium.launch(headless=headless)

self.context = await self.browser.new\_context(

viewport={"width": 1440, "height": 900},

locale="en-US",

timezone\_id="America/New\_York",

extra\_http\_headers={"Accept-Language": "en-US,en;q=0.9"},

)

self.page = await self.context.new\_page()

# Initialize tracking variables

if self.action\_history is None:

self.action\_history = []

if self.visited\_urls is None:

self.visited\_urls = set()

# ...

async def ensure\_page(self) -> Page:

if not self.page:

await self.start()

assert self.page is not None

return self.page

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Initializing and accessing the Playwright session (src/tools/browser\_runtime.py)

- **Lines 1–3:** The `start` method first checks whether `self.page` already exists. If it does, the browser is already running, so it returns to prevent launching duplicate browsers.
- **Lines 4–6:** We start the asynchronous Playwright engine (`self.pw`), check environment variables to determine whether we should run in headless mode, and launch a Chromium browser instance.
- **Lines 7–12:** We create a new `BrowserContext`. Notice the strict configuration: `{"width": 1440, "height": 900}`. Consistent viewport sizing is crucial for multimodal agents; it ensures the VLM sees a standard desktop layout and prevents elements from shifting unexpectedly. We also standardize the locale and time zone.
- **Line 13:** We create a new `page` (tab) within our configured context.
- **Lines 14–17:** We initialize our state-tracking arrays and sets if they are currently `None`.
- **Lines 19–23:** The `ensure_page` method is a helper wrapper. Before any tool executes a web action, it calls this method. If the page isn't running, it calls `start()` and then safely returns the active `Page` object.

Notice the viewport configuration: `{"width": 1440, "height": 900}`. Consistent viewport sizing is crucial for multimodal agents so the VLM (Vision-Language Model) sees a standard desktop layout, ensuring that elements do not unexpectedly shift between observation and action.

### The singleton pattern[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-singleton-pattern)

The final, crucial piece of this file is located at the very bottom:

Ace Editor

1

RUNTIME = BrowserRuntime()

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The module-global Singleton (src/tools/browser\_runtime.py)

We instantiate exactly one instance of the `BrowserRuntime` class.

Why do we do this? In Google ADK (and most LLM framework tool implementations), tools are standard Python functions. When the LLM decides to call `click_element(element_id="5")`, ADK invokes that Python function. By importing the global `RUNTIME` object into our tools module, every independent function call can access and modify the same browser instance and `last_elements` list.

## Wrapping up[#](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Wrapping-up)

In this lesson, we established the foundation for our agent's physical interactions with the web. We saw how `agent.py` launches the ADK setup and how `browser_runtime.py` uses a dataclass and the singleton pattern to safely maintain Playwright browser state and element history across asynchronous LLM API calls.

With browser state safely managed, we are ready to give the LLM its hands and eyes. In the next lesson, we will explore `web_tools.py`, where we implement the functions that capture the screen, parse the DOM, and execute clicks.

From Design to a Running Multimodal Web Agent

Building Multimodal Web Tools

Ask

[The entry point: agent.py](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-entry-point-agentpy)

[The browser runtime: Keeping the session alive](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-browser-runtime-Keeping-the-session-alive)

[Defining the state object](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Defining-the-state-object)

[Starting and accessing the browser](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Starting-and-accessing-the-browser)

[The singleton pattern](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#The-singleton-pattern)

[Wrapping up](https://www.educative.io/courses/agentic-ai-systems/managing-the-browser-state#Wrapping-up)