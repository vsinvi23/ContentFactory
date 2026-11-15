# MuLan's_Planning_Strategy_for_Progressive_Multi-Object_Generation

Source: https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# MuLan’s Planning and Progressive Generation

Understand how MuLan uses large language models to create a global plan that breaks down complex image prompts into ordered sub-prompts. Learn how progressive generation with conditional diffusion and local LLM planning manages object placement and size. Discover attention guidance and candidate selection techniques to handle overlaps, allowing MuLan to generate detailed multi-object images step-by-step.

We'll cover the following...

- [The LLM as a global planner](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-global-planner)
  - [Creating an ordered sequence of sub-prompts](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Creating-an-ordered-sequence-of-sub-prompts)
- [Conditional single-object diffusion](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Conditional-single-object-diffusion)
  - [The LLM as a local planner](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-local-planner)
  - [Single-object generation with attention guidance](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Single-object-generation-with-attention-guidance)
  - [Handling object overlapping](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Handling-object-overlapping)

In our last lesson, we introduced MuLan’s “divide and conquer” strategy. Instead of tackling a complex image generation task all at once, it breaks the problem down into smaller, more manageable pieces. In this lesson, we’ll explore the first pillar of this architecture in detail: how the agent creates its initial plan.

## The LLM as a global planner[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-global-planner)

Let’s return to our analogy of a human painter. A painter doesn’t just start randomly dabbing paint on a canvas. They first create a mental plan or a light sketch, deciding which objects will form the background and which will be in the foreground, and the general order in which they will be painted.

MuLan’s first step is exactly this: LLM planning. At the very beginning of the process, before any image generation happens, an LLM is used to create a global plan. It takes the user’s single, complex prompt and decomposes it into an ordered sequence of objects to be generated.

### Creating an ordered sequence of sub-prompts[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Creating-an-ordered-sequence-of-sub-prompts)

The first pillar of MuLan’s architecture is the “global plan,” created by an LLM before any image generation begins. The goal is to decompose the user’s single, complex prompt into an ordered sequence of simpler sub-prompts.

![The LLM’s global planning process: The user’s image description (p) is fed into the LLM along with the “Global Planning Prompt” containing specific instructions for the LLM. The LLM then processes these inputs to generate a sequence of conditional sub-prompts that form the overall plan](002_MuLan's_Planning_Strategy_for_Progressive_Multi-Object_Generation_images/img_fdff48d9ffd1.svg "The LLM’s global planning process: The user’s image description (p) is fed into the LLM along with the “Global Planning Prompt” containing specific instructions for the LLM. The LLM then processes these inputs to generate a sequence of conditional sub-prompts that form the overall plan")

The LLM’s global planning process: The user’s image description (p) is fed into the LLM along with the “Global Planning Prompt” containing specific instructions for the LLM. The LLM then processes these inputs to generate a sequence of conditional sub-prompts that form the overall plan

To achieve this, the LLM is assigned the persona of an “adept painter” and given a specific, rule-based task. The prompt template used is as follows.

> **Global planning prompt:** `You are an excellent painter. I will give you some descriptions. Your task is to turn the description into a painting. You only need to list the objects in the description by painting order, from left to right, from down to top. Do not list additional information other than the objects mentioned in the description. Description: {p}.`

This explicit sorting rule transforms a complex spatial reasoning task into a more straightforward sorting problem. Let’s see how it applies given the following image description as an example.

> **Image description:** “A red cube is on top of a wide blue cylinder. To the left of the cylinder stands a small, green pyramid. The entire scene is on a reflective metal floor.”

The LLM applies the rule to create an ordered list of the core objects.

1. **Left-to-right sort:** The “green pyramid” is “to the left of the cylinder,” so it comes first.
2. **Bottom-to-top sort:** The “red cube” is “on top of” the cylinder, so it comes after the cylinder.

This results in the following order of objects: 1. Green pyramid, 2. Blue cylinder, 3. Red cube. This order is then used to generate the final, actionable plan, which is a sequence of conditional sub-prompts. The key here is that each new sub-prompt is conditioned on previously generated objects, which directly includes the necessary spatial relationship.

- **Stage 1 sub-prompt:** `"A green pyramid on a reflective metal floor"`.
- **Stage 2 sub-prompt:** `"A wide blue cylinder to the right of the green pyramid"`.
- **Stage 3 sub-prompt:** `"A red cube on top of the blue cylinder"`.

This global plan provides a foundational roadmap for the entire generation process. Creating this complete, step-by-step plan before any generation begins is a perfect example of the plan-and-execute pattern in action. With this sequence of simple, ordered tasks, the agent is now ready to pick up its “brush,” the diffusion model.

**A training-free system:** It’s crucial to understand that MuLan is a training-free agent. It doesn’t use a specially fine-tuned model. Instead, it cleverly orchestrates a team of pre-existing, general-purpose models (a powerful LLM like GPT-4, a VLM like LLaVA, and a standard stable diffusion model). Its intelligence comes from the system’s architecture, not from custom model training. This is a key advantage, making the system more flexible and easier to adapt.

## Conditional single-object diffusion[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Conditional-single-object-diffusion)

With the global plan and the sequence of sub-prompts ready, the agent moves to the second stage: progressive generation. At each stage of this process, the diffusion model (our “painting” tool) focuses on generating just a single object from the plan, conditioned on the image from the previous stage.

This is where the agentic system design becomes more dynamic. While the global plan from the first module provided the *what* and the *order*, the exact *where* and *how big* for each object is determined in real-time at each step.

![The single-object diffusion process in MuLan. The LLM acts as a local planner, creating a “Rough mask” to define the position and size of the next object. This mask, combined with the sub-prompt, guides the diffusion model to generate the object in the correct location on the canvas, building upon the objects from the previous stage](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The single-object diffusion process in MuLan. The LLM acts as a local planner, creating a “Rough mask” to define the position and size of the next object. This mask, combined with the sub-prompt, guides the diffusion model to generate the object in the correct location on the canvas, building upon the objects from the previous stage")

The single-object diffusion process in MuLan. The LLM acts as a local planner, creating a “Rough mask” to define the position and size of the next object. This mask, combined with the sub-prompt, guides the diffusion model to generate the object in the correct location on the canvas, building upon the objects from the previous stage

### The LLM as a local planner[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-local-planner)

At the beginning of each generation stage, the LLM is called upon again, this time as a local planner. Its job is to determine the rough position and size for the *next* object to be generated, relative to the objects that are already on the canvas.

Given the sub-prompt for the current stage (e.g., “A wide blue cylinder to the right of the green pyramid”), the LLM determines two key things.

1. **Relative position:** It decides where the new object should go in relation to the previous one (e.g., `right`, `top`).
2. **Object count:** It estimates how many non-overlapping objects are in that same region to help determine the new object’s size.

The output of this local planning step is a rough mask, and essentially a bounding box that designates the general area where the new object should be painted.

For the very first object in the sequence, the local planning is simpler. There are only two possible positions (left or bottom), and a simple rule is used to split the canvas and size of this first bounding box.

### Single-object generation with attention guidance[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Single-object-generation-with-attention-guidance)

With this rough mask in place, the system now needs to ensure that the diffusion model actually generates the new object inside that designated area.

To achieve this, MuLan uses a technique called **backward cross-attention guidance**. It is a mechanism in diffusion model that links the words in the text prompt to specific regions of the image being generated. It uses an energy function to calculate a loss based on how much of the object’s attention map is inside the rough mask. During the early timesteps of the diffusion process, it then applies gradients to the latent image to minimize this loss, effectively “pushing” the object to form in the correct place.

MuLan’s attention guidance mechanism effectively forces the model to concentrate the generation of the new object (e.g., the “blue cylinder”) within the boundaries of the rough mask planned by the LLM.

### Handling object overlapping[#](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Handling-object-overlapping)

A key challenge in multi-object scenes is handling overlaps, which is explicitly addressed by MuLan’s design. If the LLM planner determines that a new object should overlap with a previous one, the system generates three candidate images with varying degrees of overlap (e.g., 10%, 30%, 50%). It then uses a CLIP score to automatically select the candidate that best matches the prompt’s description.

**CLIP** stands for Contrastive Language–Image Pre-training. At its core, it’s a model trained to understand how well an image and a text description match. It learns this by training two separate models, one for vision and one for language, and learning to “contrast” correct image-text pairs from incorrect ones.

![The core mechanism of CLIP: It processes both text and images through separate encoders. The outputs are then compared to produce a score (represented by the blue squares on the diagonal), indicating how well a specific image-text pair matches](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The core mechanism of CLIP: It processes both text and images through separate encoders. The outputs are then compared to produce a score (represented by the blue squares on the diagonal), indicating how well a specific image-text pair matches")

The core mechanism of CLIP: It processes both text and images through separate encoders. The outputs are then compared to produce a score (represented by the blue squares on the diagonal), indicating how well a specific image-text pair matches

The CLIP score is the output of this process: a number that measures the quality of the match. A higher score means the image is a better fit for the text prompt.

In the context of MuLan, CLIP functions as a fast and objective judge. Its single job is to judge which of the three candidates best aligns with the prompt’s description, and its verdict determines which image is used for the next stage. The image with the highest score, the best match, is chosen to move forward.

This entire process, local planning, attention guidance, and overlap handling, is repeated for each object in the global plan, progressively building up the complex scene one simple, controlled step at a time.

Introduction to MuLan and the Multi-Object Generation Challenge

VLM-Feedback Control and Human-in-the-Loop Interaction

Ask

[The LLM as a global planner](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-global-planner)

[Creating an ordered sequence of sub-prompts](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Creating-an-ordered-sequence-of-sub-prompts)

[Conditional single-object diffusion](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Conditional-single-object-diffusion)

[The LLM as a local planner](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#The-LLM-as-a-local-planner)

[Single-object generation with attention guidance](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Single-object-generation-with-attention-guidance)

[Handling object overlapping](https://www.educative.io/courses/agentic-ai-systems/mulans-planning-and-progressive-generation#Handling-object-overlapping)