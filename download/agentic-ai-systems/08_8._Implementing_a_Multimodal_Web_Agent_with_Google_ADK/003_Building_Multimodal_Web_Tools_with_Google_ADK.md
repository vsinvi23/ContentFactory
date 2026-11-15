# Building_Multimodal_Web_Tools_with_Google_ADK

Source: https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Building Multimodal Web Tools

Explore building a multimodal web agent by managing Playwright sessions, annotating interactive elements with numeric labels, and fusing DOM data with visual language model analysis. Understand fallback mechanisms for element interaction and discover future directions in vision-based and accessibility tree parsing for robust web agents.

We'll cover the following...

- [Annotating the screenshot](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Annotating-the-screenshot)
- [Grounding actions with element IDs](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Grounding-actions-with-element-IDs)
- [Fusing multimodal observations](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Fusing-multimodal-observations)
- [Limitations and improvements](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Limitations-and-improvements)
  - [Conclusion](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Conclusion)

In the previous lesson, we set up `browser_runtime.py` to maintain a persistent Playwright session. However, a browser alone does not make an agent. The agent needs "eyes" to see the page and "hands" to interact with it. In this lesson, we will explore `src/tools/web_tools.py`. This file contains the actual Python functions (tools) exposed to the large language model. We will look at three critical functions:

1. **Annotating the screen:** Injecting numeric labels onto interactive UI elements so the vision-language model (VLM) can reference them.
2. **Executing actions:** Translating a tool call like `click_element("5")` into physical coordinates or CSS-selector clicks.
3. **Multimodal fusion:** Combining raw DOM data with VLM visual analysis into a single observation payload for the LLM.

By the end of this lesson, you should be able to:

- Explain how numeric labels are drawn over web elements using bounding box data.
- Understand the fallback mechanism (selector vs. coordinates) used when clicking an element.
- Describe the structure of a fused multimodal observation.

> **Pause and reflect:** If a web page dynamically changes a button's CSS class every time you reload, why is it safer for an LLM to interact with it using a numeric bounding-box ID rather than generating its own CSS selector?

## Annotating the screenshot[#](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Annotating-the-screenshot)

To give the LLM a WebVoyager-style view of the page, we cannot just send a raw screenshot. We must label candidate elements (links, buttons, and inputs) with IDs like `[0]`, `[1]`, `[2]`.

Under the hood, a function called `_collect_dom_elements` uses JavaScript to find all visible, interactive DOM nodes and calculate their `x`, `y`, `width`, and `height`. We then pass this data to `_annotate_screenshot`.

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

def \_annotate\_screenshot(screenshot\_path: Path, elements: list[dict[str, Any]]) -> str:

annotated\_path = screenshot\_path.parent / f"{screenshot\_path.stem}\_labeled.png"

image = Image.open(screenshot\_path).convert("RGB")

draw = ImageDraw.Draw(image)

image\_w, image\_h = image.size

for item in elements:

x = int(item.get("x", 0))

y = int(item.get("y", 0))

width = max(1, int(item.get("width", 1)))

height = max(1, int(item.get("height", 1)))

label = str(item.get("id", "element"))

x2 = x + width

y2 = y + height

if x2 <= 0 or y2 <= 0 or x >= image\_w or y >= image\_h:

continue

x = max(0, x)

y = max(0, y)

x2 = min(image\_w - 1, x2)

y2 = min(image\_h - 1, y2)

draw.rectangle([(x, y), (x2, y2)], outline=(0, 0, 0), width=2)

draw.rectangle([(x, max(0, y - 16)), (x + 18, y)], fill=(0, 0, 0))

draw.text((x + 4, max(0, y - 15)), label, fill=(255, 255, 255))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Drawing bounding boxes and numeric labels on screenshots (src/tools/web\_tools.py)

- **Line 2:** We define the output path for the new labeled image by appending `_labeled.png` to the original screenshot's name.
- **Lines 3–5:** We open the original screenshot using the `Pillow` library (`Image.open`), convert it to RGB, and initialize an `ImageDraw` context.
- **Lines 7–12:** We iterate through the list of extracted DOM elements, grabbing each element's `x` and `y` coordinates, its dimensions, and its numeric `id`.
- **Lines 14–22:** We calculate the bottom-right coordinates (`x2`, `y2`) and apply clipping logic. This ensures we do not try to draw shapes outside the bounds of the viewport, which would cause errors.
- **Lines 24–26:** We draw the actual visual markers. First, an outlined rectangle around the element. Second, a small filled black square above the top-left corner. Third, we draw the numeric ID in white text inside that black square.
- **Lines 28–29:** Finally, we save the annotated image to disk and return the file path.

## Grounding actions with element IDs[#](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Grounding-actions-with-element-IDs)

Now that the LLM can *see* elements with labels like `[5]`, it will call tools like `click_element(element_id="5")`. Because we saved all the element data in `RUNTIME.last_elements` during the observation phase, we can map this ID back to the physical page.

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

async def click\_element(element\_id: str) -> str:

page = await RUNTIME.ensure\_page()

el = \_lookup\_element(element\_id)

if not el:

return f"click\_element failed: unknown element\_id {element\_id}..."

selector = \_preferred\_selector\_for\_element(el)

if selector and await \_is\_unique\_visible\_locator(page, selector):

try:

target = page.locator(selector).first

await target.wait\_for(state="visible", timeout=4000)

await target.scroll\_into\_view\_if\_needed(timeout=3000)

await target.click(timeout=5000)

return f"Clicked element\_id={element\_id} via selector={selector}..."

except Exception:

pass

x = int(el.get("x", 0)) + int(el.get("width", 1)) // 2

y = int(el.get("y", 0)) + int(el.get("height", 1)) // 2

await page.mouse.click(x, y)

return f"Clicked element\_id={element\_id} (x={x}, y={y})..."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Executing a click using either a CSS selector or physical coordinates (src/tools/web\_ tools.py )

- **Line 2:** We retrieve the active Playwright `page` instance using our `RUNTIME` singleton.
- **Lines 3–5:** We look up the `element_id` in our saved `last_elements` list. If the LLM hallucinates an ID that does not exist, we return an error string that allows the agent to self-correct.
- **Lines 7–8:** We attempt to build a stable CSS selector for the element (for example, using `data-testid` or `aria-label`). We only proceed with the selector if Playwright confirms it resolves to a *unique*, visible element on the page.
- **Lines 9–16:** We attempt a robust DOM-based click. We locate the element, wait for it to be visible, scroll it into view, and click it. If this fails (for example, due to dynamic page shifts), we catch the exception and fall through to the next strategy.
- **Lines 18–20:** This is the robust fallback. We calculate the exact center pixel `(x, y)` of the element using the bounding box we collected during the observation phase. We then instruct the Playwright virtual mouse to click that specific pixel on the screen.

## Fusing multimodal observations[#](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Fusing-multimodal-observations)

At the heart of the ReAct loop is the observation. Instead of just sending the LLM text DOM data or an image, we fuse them. `capture_multimodal_observation` fetches the DOM elements, gets the screenshot, and asks a VLM to provide a high-level visual understanding of the page.

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

async def capture\_multimodal\_observation(

vlm\_prompt: str = "Describe the page goal, key UI regions, and best next actions using visible clues."

) -> str:

if getattr(RUNTIME, "session\_done", False):

return json.dumps({"observation\_type": "multimodal\_fused", "session\_done": True})

RUNTIME.observation\_streak = getattr(RUNTIME, "observation\_streak", 0) + 1

observation = json.loads(await capture\_observation())

vlm\_raw = await analyze\_screenshot\_with\_vlm(vlm\_prompt)

try:

vlm\_data = json.loads(vlm\_raw)

except ValueError:

vlm\_data = {"error": vlm\_raw}

fused = {

"observation\_type": "multimodal\_fused",

"url": observation.get("url"),

"title": observation.get("title"),

"screenshot\_path": observation.get("screenshot\_path"),

"labeled\_screenshot\_path": observation.get("labeled\_screenshot\_path"),

"elements": observation.get("elements", []),

"vlm\_analysis": vlm\_data,

"observation\_streak": RUNTIME.observation\_streak,

"task\_constraints": getattr(RUNTIME, "task\_constraints", None) or {},

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Generating the fused multimodal observation (src/tools/web\_ tools.py )

- **Lines 4–5:** If the task is already marked as complete (`session_done`), we short-circuit and return a terminal payload to stop the agent from looping.
- **Line 7:** We increment the `observation_streak`. If the agent keeps observing without acting, other parts of the system use this streak to suggest an action.
- **Line 9:** We call `capture_observation()`, which handles taking the raw screenshot, extracting DOM rectangles, generating the annotated image, and returning the structured JSON.
- **Line 10:** We call `analyze_screenshot_with_vlm`, passing the screenshot to a vision-language model (like GPT-4o or a Hugging Face model) to get a semantic breakdown of the page.
- **Lines 12–15:** We safely parse the VLM output into a JSON dictionary.
- **Lines 17–27:** We construct the `fused` object. This creates a highly informative context window for the reasoning LLM, offering both structural data (`elements`, `labeled_screenshot_path`) and semantic understanding (`vlm_analysis`).

## Limitations and improvements[#](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Limitations-and-improvements)

The approach we just implemented, using JavaScript to extract the DOM, calculating bounding boxes, and drawing numeric labels on a screenshot, is heavily inspired by early multimodal frameworks like WebVoyager. While it is effective for many tasks, it has distinct limitations.

1. **DOM dependency:** The agent is entirely blind to elements that do not exist cleanly in the standard DOM tree. Interactive elements rendered inside `<canvas>`, WebGL, or complex cross-origin `<iframe>` tags will not generate bounding boxes, which makes them unclickable.
2. **Visual clutter:** On dense pages (like a busy e-commerce site or news portal), extracting hundreds of interactive elements and drawing black boxes over them creates severe visual noise. This can obscure important text or icons, which can confuse the VLM.
3. **Dynamic shift misalignment:** Web pages are highly dynamic. If an animation occurs or an ad loads in the millisecond *between* extracting the DOM coordinates and capturing the screenshot, the drawn bounding boxes will not align with the actual buttons, which can lead to failed clicks.

To overcome these weaknesses, the industry is shifting away from heavy DOM reliance toward pure vision-based models and accessibility-tree integrations:

- **Pure vision parsing (e.g., OmniParser):** Instead of injecting JS into the page, frameworks like OmniParser treat the raw screenshot as the only source of truth. They use specialized OCR and icon-detection models to visually detect buttons, text, and inputs, drawing bounding boxes based strictly on what is rendered on the screen. This solves the `<canvas>` and iframe blindness completely.
- **Coordinate-output models (e.g., Qwen-VL, GPT-4o):** Newer VLMs are trained with intrinsic spatial awareness. Instead of needing us to draw `[0]`, `[1]`, `[2]` on the screen, these models can take a clean, raw screenshot and directly output the `(x, y)` coordinates of the element the user wants to interact with (for example, *"Click the submit button at coordinates 450, 800"*).
- **Accessibility tree (A11y) parsing:** Rather than parsing the raw HTML DOM (which is often cluttered with `<div>` wrappers and styling artifacts), modern agents parse the browser's accessibility tree. The accessibility tree provides a sanitized, highly semantic representation of the UI, exactly as a screen reader would see it, which drastically reduces noise.

### Conclusion[#](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Conclusion)

In this lesson, we examined how `web_tools.py` provides the critical capabilities needed for a multimodal agent. We saw how `_annotate_screenshot` paints numeric IDs onto candidate elements, how `click_element` safely falls back to coordinate-based clicking, and how `capture_multimodal_observation` merges DOM data with VLM insights. We also discussed why moving toward pure vision parsing and coordinate-output models represents the future of web agents.

In our next and final lesson, we will tie all of this together by exploring `web_agent.py`, where we wrap these tools into ADK agents, define their system prompts, and launch the decision loop.

Managing the Browser State

Assembling the Web Agent with Google ADK

Ask

[Annotating the screenshot](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Annotating-the-screenshot)

[Grounding actions with element IDs](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Grounding-actions-with-element-IDs)

[Fusing multimodal observations](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Fusing-multimodal-observations)

[Limitations and improvements](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Limitations-and-improvements)

[Conclusion](https://www.educative.io/courses/agentic-ai-systems/building-multimodal-web-tools#Conclusion)