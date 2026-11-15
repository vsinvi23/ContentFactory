# Designing_a_Scalable_Text-to-Video_Generation_System

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Text-to-Video Generation System

Design a text-to-video system around a diffusion model: train it on large video-text datasets, then serve it through prompt processing, frame generation, rendering, and quality control.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Nonfunctional-requirements)
- [Model selection](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-selection)
- [The training process](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-training-process)
  - [Data acquisition and preparation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-acquisition-and-preparation)
    - [Source of training data](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Source-of-training-data)
      - [Dataset format](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Dataset-format)
    - [Data preprocessing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-preprocessing)
    - [Database selection](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Database-selection)
    - [Time estimation for data processing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Time-estimation-for-data-processing)
  - [Model training and testing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-training-and-testing)
    - [Distributing the training load](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Distributing-the-training-load)
  - [Model evaluation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-evaluation)
    - [Evaluation metrics](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Evaluation-metrics)
- [Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Storage-estimation)
  - [Inference servers estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Inference-servers-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Bandwidth-estimation)
  - [Design considerations](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Design-considerations)
- [System Design of the text-to-video generation system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#System-Design-of-the-text-to-video-generation-system)
  - [The high-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-high-level-design)
    - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Achieving-functional-requirements)
  - [The detailed System Design](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-detailed-System-Design)
    - [Prompt processing and embedding system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Prompt-processing-and-embedding-system)
    - [Model host and frame generation system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-host-and-frame-generation-system)
    - [Rendering system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Rendering-system)
    - [Quality control system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Quality-control-system)
    - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Putting-everything-together)
      - [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Workflow-of-the-system)
- [Fulfilling nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Fulfilling-nonfunctional-requirements)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Conclusion)

Text-to-video models represent the next frontier in generative AI. These models are designed to interpret textual inputs and create videos that adhere to specified prompts in terms of content, style, and motion dynamics. Their applications span diverse fields, including entertainment, education, marketing, and virtual reality, offering a revolutionary toolkit for storytelling, simulation, and content personalization.

The complexity of video generation demands an advanced understanding of both NLP and video synthesis. Unlike text-to-image systems, which output a single image, text-to-video systems must consider spatial and temporal consistency, requiring sophisticated modeling of motion, transitions, and interactions over time. Prominent examples of video generation models include Open-SORA, Mochi 1, and SORA, each excelling in different aspects of video synthesis, such as realism, smooth transitions, and interpretive fidelity.

Let’s explore how to build an advanced and reliable text-to-video system. We’ll focus on creating a system that takes text inputs and generates realistic, high-quality videos.

![A snapshot of a text-to-video system (Source: AI-generated video using Mochi 1)](images/img_73bdecb489b1.svg "A snapshot of a text-to-video system (Source: AI-generated video using Mochi 1)")

A snapshot of a text-to-video system (Source: AI-generated video using Mochi 1)

## Requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Requirements)

Designing a text-to-video system involves addressing functional and nonfunctional requirements to ensure the system performs effectively and reliably. Let’s break these down:

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Functional-requirements)

The core functionalities that our text-to-video system should support include:

- **Natural language understanding:** The system must include a strong natural language understanding component to accurately interpret and extract meaningful information from text inputs.
- **Video generation**:  The system should produce high-quality videos that align with text prompts. These outputs must support specific characteristics, including resolution, frame rate, video length, and smooth transitions between frames.

> **Note:** You may want to design a system with specific output requirements, like a 720p video with 30fps. This is the phase where you can decide the requirements that will later shape the system design and influence the design decisions.

- **Input formats:** The system should handle a variety of input formats, such as JSON and plain text, to allow flexibility in integrating with different applications.
- **Customization:** Users should have fine-grained control over the generated videos, allowing them to specify desired styles, camera angles, emotional tones, or visual themes directly within their text prompts.
- **Output formats:** The system should support multiple video formats (e.g., MP4, AVI, or WebM) to ensure compatibility with various platforms and use cases.

Users may also want to download the generated videos in their specified formats. The lesson [Design of a File API](https://www.educative.io/courses/grokking-the-product-architecture-interview/requirements-of-the-file-api) teaches you how to design a file-handling service.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Nonfunctional-requirements)

The nonfunctional requirements ensure that the video generation model performs reliably, scales effectively, and maintains security:

- **Scalability:** The system should handle varying workloads, from individual users to high-demand scenarios, without degradation in performance.
- **Performance:** Video generation should occur within a reasonable timeframe, maintaining low latency even for longer or high-resolution outputs.
- **Reliability:** The system should consistently generate videos that accurately reflect the input prompts, ensuring predictable and stable behavior.
- **Availability:** The system should prioritize high availability, achieved through a robust infrastructure that includes redundancy and failover mechanisms.
- **Security and privacy:** User inputs and generated outputs should be securely handled, with safeguards against unauthorized access or data leaks, particularly when dealing with sensitive or proprietary prompts. We also want to secure user data to achieve security and privacy.

## Model selection[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-selection)

Text-to-video generation systems require a model combining natural language understanding (interpreting text) and video synthesis (creating dynamic visual content). Common architectures include:

1. **Transformer-based models:** These models, such as those leveraging GPT-style or BERT-style transformers, are adept at handling complex text inputs and aligning them with visual outputs. By pairing transformers with video generation modules, these architectures excel in maintaining temporal consistency across frames.
2. **Generative adversarial networks (GANs):** GANs are effective for video generation due to their ability to create realistic content. Specialized conditional GANs can map textual prompts to video sequences in the text-to-video context. However, they often require additional tuning for temporal coherence.
3. **Diffusion models:** Building on their success in text-to-image generation, diffusion models have begun to extend to video generation. These models iteratively refine frames from noise while maintaining temporal relationships, offering a promising approach for producing high-quality videos.
4. **Hybrid architectures:** Combining elements from different architectures, such as a transformer for text comprehension and a GAN or diffusion model for video synthesis, can offer a balanced approach, taking advantage of the strengths of each model type. Note that hybrid architectures combine any two or more independent architectures, such as GANs, diffusion models, [VAEs](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-image-generation-system#Choosing-the-right-model-architecture), etc.

Let’s compare some of the common state-of-the-art text-to-video models in the table below:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Model** | **Architecture** | **Open Source?** | **Specialization** | **Limitations** |
| **Open-SORA** | Transformer + GAN (Hybrid) | ✅ | General video generation | Higher computational requirements |
| **Mochi 1** | Diffusion + VAE (Hybrid) | ✅ | Stylized videos | Does not support diverse prompts |
| **SORA** | Transformer + Diffusion (Hybrid) | ❌ | Realistic, high-detail videos | A High computational cost for training/inference; not publicly available |
| **VideoGPT** | Transformer | ✅ | Short-form video synthesis | Limited frame resolution and duration |
| **Imagen Video** | Diffusion | ❌ | Realistic, high-detail videos | Not publicly available |
| **Lumiere** | Diffusion | ❌ | Photorealistic videos | Not publicly available |

We will use **Mochi 1**, a diffusion-based model that generates high-quality stylized videos for our text-to-video generation system. Mochi 1 uses ~10 B parameters in the diffusion process and ~300 M for the VAE to ensure detail, temporal consistency, and customization flexibility. We will keep it simple and assume a model with 10 B parameters.

![The Mochi 1 training architecture](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The Mochi 1 training architecture")

The Mochi 1 training architecture

> **Note:** We will not be training the text encoder here (it will be treated as a frozen model). However, due to the size of the encoder used (T5-XXL has ~4.7 B parameters in its encoder), we must consider this when estimating the time it takes to train the model.

The Mochi 1 model starts with two main inputs: a text prompt (processed by the T5-XXL language model) and video input. The text prompt is encoded into text tokens and passed to the text processing stream with a smaller hidden dimension. Simultaneously, the video input is compressed by the video VAE, reducing its size through spatial compression (8x8) and temporal compression (6x) to a compact 12-channel latent space. This output is then processed by the visual processing stream, which has a larger hidden dimension because video data requires more capacity to handle complexity.

The text and video streams come together in the multimodal self-attention module, where the system learns to unify and relate information from both modalities. The model uses an *asymmetric diffusion transformer (AsymmDiT)* with specialized layers like non-square QKV and projection layers to efficiently manage the differences between text and video data. This design ensures efficient memory usage and balances processing power.

After this, the architecture applies full 3D attention to process a large number of video tokens (44,520) within a single context window, enhancing spatial and temporal coherence. It leverages 3D positional embeddings to position each token accurately in space and time. The model then uses techniques like SwiGLU feedforward layers, query-key normalization, and sandwich normalization to stabilize and refine the generation process. Finally, the output is the generated video, which integrates the features from the input text.

This modular design makes Mochi 1 efficient and powerful for video generation while keeping it hackable and open-source for further exploration.

Use the widget below to strengthen your knowledge of the Mochi 1 architecture.

AI Powered

Saved

10 attempts left

Reset

You have 10 attempts to answer.

## The training process[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-training-process)

Next, we’ll discuss acquiring and preparing the datasets needed to train Mochi 1 effectively for text-to-video tasks.

### Data acquisition and preparation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-acquisition-and-preparation)

The dataset’s quality, diversity, and volume are critical for training a text-to-video system. Videos inherently have a higher data complexity than images, as they include spatial and temporal components. The dataset must include various video styles, objects, scenes, and the corresponding textual descriptions.

#### Source of training data[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Source-of-training-data)

Creating a video dataset can be quite a demanding task. We must curate or generate text prompts, record scenes, and store them. This process is infeasible for most people. Another way is scraping videos from online sources and labeling them with appropriate text prompts. This is the same technique used for many public datasets. So, for training, we will look for publicly available data. Some popular public datasets include UCF-101 (13,320 videos), MSR-VTT (10,000 video clips), and Kinetics-700 (650,000 video clips).

While curating data, it is essential to remember that we do not use proprietary or copyrighted data.

We will be sourcing our data from such datasets to equal around ~10 M rows of data around 20 TB (assuming 2 MB per 5s video in one row, along with metadata and text description).

##### Dataset format[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Dataset-format)

For video generation, we require the dataset to be in the following format:

![The required dataset format (Source: AI-generated content using Mochi 1)](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The required dataset format (Source: AI-generated content using Mochi 1)")

The required dataset format (Source: AI-generated content using Mochi 1)

> **Note:** Many off-the-shelf datasets will come in formats that may not be suitable for training immediately. We may need to remove or merge some columns (features) to prepare the dataset for training.

#### Data preprocessing[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-preprocessing)

Before we can move on to training, we need to process the data to ensure consistency. This will involve:

- **Frame standardization:** Rescale videos to a fixed resolution (e.g., 720p or 1080p). Normalize pixel values to improve training stability.
- **Temporal sampling:** Extract a fixed number of frames per second to standardize input sequences.
- **Text preprocessing:** Remove special characters, abbreviations, and unrelated text.

> **Note:** Removing inappropriate or offensive content from a video dataset requires an expert review of each video, using the CLIP model to convert the video frames into text descriptions and then performing sensitive content moderation. Doing that for 10 M rows may be infeasible. However, we may not need to do this if we use a reputable source for our data.

Then, we need to store this data in some data stores.

#### Database selection[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Database-selection)

Like the previous design problem, we can store our data in a simple SQL database and use a blob store for video file storage.

#### Time estimation for data processing[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Time-estimation-for-data-processing)

Let’s use some approximate values for our dataset:

Total data items=10 M\text{Total data items} = \text{10 M}Total data items=10 M

**Assuming:**

Time to preprocess a video file=200 msTime to preprocess a text description=1 msTime to store a row into the database=2 ms\text{Time to preprocess a video file} = \text{200 ms}
\\
\text{Time to preprocess a text description} = \text{1 ms}
\\
\text{Time to store a row into the database} = \text{2 ms}Time to preprocess a video file=200 msTime to preprocess a text description=1 msTime to store a row into the database=2 ms

**We get:**

Total video processing time (Tpv)=Time to preprocess a video×Total data itemsTpv=200 ms×10 M=1,000,000 seconds\text{Total video processing time } (T\_{pv}) = \text{Time to preprocess a video} \times \text{Total data items} \\
T\_{pv} = \text{200 ms} \times \text{10 M} = \text{1,000,000 seconds}Total video processing time (Tpv​)=Time to preprocess a video×Total data itemsTpv​=200 ms×10 M=1,000,000 seconds

Total text processing time (Tpt)=Time to preprocess text×Total data itemsTpt=1 ms×10 M=10,000 seconds\text{Total text processing time } (T\_{pt}) = \text{Time to preprocess text} \times \text{Total data items} \\
T\_{pt} = \text{1 ms} \times \text{10 M} = \text{10,000 seconds}Total text processing time (Tpt​)=Time to preprocess text×Total data itemsTpt​=1 ms×10 M=10,000 seconds

Total storage time (Ts)=Time to store a row×Total data itemsTs=1 ms×10 M=20,000 seconds\text{Total storage time } (T\_s) = \text{Time to store a row} \times \text{Total data items} \\
T\_s = \text{1 ms} \times \text{10 M} = \text{20,000 seconds}Total storage time (Ts​)=Time to store a row×Total data itemsTs​=1 ms×10 M=20,000 seconds

**So the total time taken is:**

Total time=Tpv+Tpt+Ts\text{Total time} = T\_{pv} + T\_{pt} + T\_s Total time=Tpv​+Tpt​+Ts​

Total time=1,000,000+10,000+20,000=1,030,000 seconds\text{Total time} = 1,000,000 + 10,000 + 20,000 = 1,030,000 \ \text{seconds}Total time=1,000,000+10,000+20,000=1,030,000 seconds

Total time≈17,166 minutes≈ 286 hours\text{Total time} \approx 17,166 \ \text{minutes} \approx \ 286 \ \text{hours}Total time≈17,166 minutes≈ 286 hours

![Time taken to process our dataset and store it in data stores](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Time taken to process our dataset and store it in data stores")

Time taken to process our dataset and store it in data stores

So, one machine would take about 286 hours (~12 days) to process all of this data at the speeds we assumed. To speed up this process, we can divide the data into multiple machines in parallel. For example, 8 machines would only take about 1.5 days to process the 10 TB dataset.

### Model training and testing[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-training-and-testing)

To train our model on the dataset selected, we first need to estimate its training time. Let’s say we are using NVIDIA H100 80GB GPUs. These GPUs come with 989 TFLOPS when doing TF32 calculations.

To estimate the time taken for training, we can make use of the following [already-derived equation](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost):

Tsec=Nparams×NFLOPS×E×D×CRops×NGPUs\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D} \times \text{C}}{\text{R}\_{\text{ops}} \times \text{N}\_{\text{GPUs}}}Tsec​=Rops​×NGPUs​Nparams​×NFLOPS​×E×D×C​

Where C\text{C}C becomes equal to the total number of steps required to generate a 5-second video:

C=Nsteps=30 framessecond×5 seconds×100 diffusion steps\text{C} = \text{N}\_{\text{steps}} = 30 \ \frac{\text{frames}}{\text{second}} \times 5 \ \text{seconds} \times 100 \ \text{diffusion steps}C=Nsteps​=30 secondframes​×5 seconds×100 diffusion steps

Nsteps=15,000 steps\text{N}\_{\text{steps}} = 15{,}000 \text{ steps}Nsteps​=15,000 steps

We do need to modify this formula a bit for this application specifically. As we saw before, the Mochi 1 model uses a T5-XXL LLM for its text encoding. This is an 11 B parameter language model, with 4.7 B parameters in its encoder. We need to consider these parameters in our forward pass as well. So, we need to add:

A=Np (endcoder)×2×D×E\text{A} = \text{N}\_{\text{p (endcoder)}} \times 2 \times D \times EA=Np (endcoder)​×2×D×E

So, the formula now becomes:

Tsec=Nparams×NFLOPS×E×D×Nsteps+ARops×NGPUs\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D} \times \text{N}\_{\text{steps}}+\text{A}}{\text{R}\_{\text{ops}} \times \text{N}\_{\text{GPUs}}}Tsec​=Rops​×NGPUs​Nparams​×NFLOPS​×E×D×Nsteps​+A​

Where A\text{A}A is the number of calculations it will take for the input to pass through the encoder. It can be calculated using the original estimation of Params×2\text{Params} \times 2Params×2. Notice that we are not including the backward pass FLOPS (4). This is because we are not training the T5-XXL model. We are simply using it for inference in our training process.

![Training Mochi 1 while keeping the T5-XXL encoder frozen](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Training Mochi 1 while keeping the T5-XXL encoder frozen")

Training Mochi 1 while keeping the T5-XXL encoder frozen

#### Distributing the training load[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Distributing-the-training-load)

We can distribute the training process over multiple machines to reach a realistic time frame using the same peer-to-peer method we used in the [training infrastructure of a text-to-image model](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-image-generation-system#Distributing-the-training-load). The time estimate when training for 1,000 epochs using 5,000 training servers is given below:

> **Note:**The FLOPS required for the T5-XXL encoder in feedforward have already been added to the widget below.

#### 

|  |  |  |  |
| --- | --- | --- | --- |
|  | A | B | C |
| 1 | Number of parameters | 10 | Billion |
| 2 | FLOPS per parameter update | 6 | FLOPS/parameter |
| 3 | Number of Epochs | 1000 | epochs |
| 4 | Size of data | 10 | Million entries |
| 5 | Number of steps | 15000 | Steps |
| 6 | FLOPS for training | f9000000094000 | TFLOPS |
| 7 | Rate of operations | 989 | TFLOPS |
| 8 | Number of GPUs | 5000 | NVIDIA A100 GPUs |
| 9 | Training time (in seconds) | f1820020.24 | Seconds |
| 10 | Training time (in days) | f21.07 | Days |

Try changing the values highlighted in yellow to see the effect on the time.

### Model evaluation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-evaluation)

The evaluation will measure Mochi 1’s capability to generate coherent and visually appealing videos that align with the provided text prompts. The primary loss function is a combination of perceptual and temporal consistency losses.

- The **perceptual loss component** leverages a pretrained CNN to extract high-level features from the generated and ground truth frames. By comparing these feature representations, we assess the model’s ability to capture semantically relevant details and generate visually plausible content that aligns with the text prompts. This can be implemented using a **learned perceptual image patch similarity (LPIPS)** metric or a similar approach that quantifies the difference in perceptual quality between the generated and target images.
- The **temporal consistency loss component** ensures smooth transitions and realistic motion dynamics between consecutive frames. It can be achieved by calculating the difference between optical flow vectors estimated from the generated video and those derived from a ground-truth video.

Minimizing this loss encourages the model to generate perceptually and temporally coherent, realistic videos.

#### Evaluation metrics[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Evaluation-metrics)

- **Mean opinion score (MOS):** MOS evaluates the perceptual quality of generated videos based on human ratings. Evaluators score videos on a scale of 1 to 5, assessing factors like realism, smoothness, and relevance to the prompt.
- **Measuring frame accuracy:** We can measure the alignment between the text prompt and the content of individual video frames. For example, we can derive scores by applying a pretrained image-text model (e.g., CLIP) to compare embeddings of generated frames and text descriptions. Higher scores indicate better prompt adherence.
- **Temporal coherence (TC)****:** This quantifies the smoothness and naturalness of motion across video frames. This is calculated using the optical flow consistency between frames. A higher TC reflects better temporal stability.
- **Fréchet video distance (FVD)****:** This compares the difference between the distribution of generated videos with real video data using pretrained video encoders. Lower FVD indicates that the generated videos are closer to real video distributions regarding quality and motion dynamics.

The illustration below summarizes the complete training process from data acquisition to training. The model weights are saved and synced at each training server.

![The model training architecture and process](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The model training architecture and process")

The model training architecture and process

As with the previous models, we can always fine-tune this model to increase its accuracy or to create a use case-specific model.

1.

How can we adapt our system to take images as input and create an image-to-video model?

Show Answer

Did you find this helpful?

Now, let’s examine how to design the deployment infrastructure for this model to serve users. We estimate various resources, followed by design considerations and a detailed System Design.

Let’s start with the storage estimation:

## Storage estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Storage-estimation)

Storage estimation includes model size, user profile and related data, and indexing storage. Let’s estimate all these resources considering 100 million daily active users:

- **Model size estimation:** We are considering a similar model to Mochi 1, which has approximately 10 billion parameters. For FP16 floating-point precision, the model size becomes:

Model size=10 billion×2 bytes=20 GB\text{Model size} = 10 \text{ billion} \times 2 \text{ bytes} = 20 \text{ GB}Model size=10 billion×2 bytes=20 GB

Mochi 1 uses the T5-XXL encoder for text encoding, which has approximately 4.7 billion parameters. Assuming the same FP16 precision, its size becomes 9.4 GB. So overall, we need 29.4 GB to store both the T5-XXL and Mochi 1 models.

- **User profile data:** Assume that each user’s data takes approximately 10 KB, translating to the following:

User data=100 M×10 KB=1 TB\text{User data} = 100 \text{ M} \times 10 \text{ KB} = 1 \text{ TB}
User data=100 M×10 KB=1 TB

> **Note:** The model and the encoder sizes (29.4 GB) and user profile data (1 TB) will remain constant unless we upgrade the model or the number of users increases. Therefore, we don’t include them in the subsequent storage estimation.

- **User interaction data:** If we store each user interaction data, the storage per interaction will depend on each interaction’s size and the video produced. Assume that the model is set to generate a 5-second video with a resolution of 480p at a frame-rate of 30 frames per second for a single request. A single 480p frame at a standard widescreen aspect ratio of 16:9 translates to around 854×480=409,920 pixels854\times480=409,920 \text{ pixels}854×480=409,920 pixels. This results in a size of 1.25 MB for a single generated video. Suppose that each user interacts 10 times per day with the system, so for 100 million users, the storage required would be:

Users interaction data=100 M×(1.25 MB×10)=1250 TB\text{Users interaction data} = 100 \text{ M} \times (1.25 \text{ MB} \times 10) = 1250 \text{ TB}Users interaction data=100 M×(1.25 MB×10)=1250 TB

- **Indexing storage:** To make the user interactions searchable and efficiently accessible, additional storage for indexing and metadata would be required, adding up to 25% of storage.

Indexing storage=1250 TB×0.25=312.5 TB\text{Indexing storage} = 1250 \text{ TB} \times 0.25 = 312.5 \text{ TB}Indexing storage=1250 TB×0.25=312.5 TB

> **Note:** Other than indexing, redundant storage is required for improved availability, low latency reading, and maybe even to serve videos of varied quality. Real-world systems tend to have much higher storage needs.

So, the total storage requirement per day would be:

Storage per day=Redundant storage+Indexing storage=1250 TB+312.5 TB=1562.5 TB/day\begin{align\*}
\text{Storage per day} &= \text{Redundant storage} + \text{Indexing storage} \\
&=1250 \text{ TB} + 312.5 \text{ TB} \\ &=1562.5 \text{ TB/day}
\end{align\*}
Storage per day​=Redundant storage+Indexing storage=1250 TB+312.5 TB=1562.5 TB/day​

According to the estimates given above, the monthly storage requirement is:

Monthly storage required=1562.5 TB×30≈47 PB\text{Monthly storage required} = 1562.5 \text{ TB} \times 30 \approx 47 \text{ PB}Monthly storage required=1562.5 TB×30≈47 PB

### Inference servers estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Inference-servers-estimation)

At 100 million DAUs, each user generating around 10 videos daily, the estimated Total Requests Per Second (TRPS) is approximately 11574. Using [our proposed inference formula](https://www.educative.io/courses/generative-ai-system-design/estimating-inference-capacity-and-fleet-size#Inference-server-estimation) for generating a 5-second video at 30 frames per second, an average query’s inference time is 0.75 seconds. We assume the model takes 50 iterations per frame, resulting in 1500 iterations (C\text{C}C) for 30 frames per second. This time is estimated using a 14.7 billion parameters model (Mochi-1 and T5-XXL) using the FP16 precision on the NVIDIA A100 GPU.

Inference time for 30 frames per second=14.7×109×2×1500312×1012=0.1413 second\text{Inference time for 30 frames per second} = \frac{14.7\times 10^9 \times 2 \times \text{1500}}{312 \times 10^{12}} = 0.1413 \text{ second}Inference time for 30 frames per second=312×101214.7×109×2×1500​=0.1413 second

Inference time for 5 second video=0.15 second×5≈0.71 second\text{Inference time for 5 second video} = 0.15 \text{ second} \times 5 \approx 0.71 \text{ second}Inference time for 5 second video=0.15 second×5≈0.71 second

According to this estimation, the QPS for NVIDIA server having A100 GPU will be 1.41 QPS, which yields us the following number of GPUs:

Inference servers required=TRPSQPS=115741.41≈8208 GPUs\text{Inference servers required} = \frac{\text{TRPS}}{\text{QPS}}=\frac{11574}{1.41} \approx 8208 \text{ GPUs}Inference servers required=QPSTRPS​=1.4111574​≈8208 GPUs

We need approximately 8208 GPUs to convert 11574 text-to-video requests per second, which is a very large number.

The number of GPUs is calculated based on simplistic assumptions. In reality, this number depends on various factors, such as concurrent operations performed by a GPU, model, and data parallelism, layers complexity in the model, quantization of the model, inference frameworks like TensorRT or ONNX runtime, and the post-processing of the generated frames such as composition and compression.

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Bandwidth-estimation)

To serve 100 million users without interruption, we need to estimate the required ingress and egress bandwidths. The ingress bandwidth depends on the size of the user request. Let’s assume that each request takes approximately 2 KB of size; the ingress bandwidth can be estimated for 11574 requests as follows:

Ingress bandwidth=11574×2 KB=23.15 MBps=23.15 MBps×8≈185 Mbps\begin{align\*}
\text{Ingress bandwidth}
&= 11574 \times 2 \text{ KB} \\
&= 23.15 \text{ MBps} \\ & = 23.15 \text{ MBps} \times 8\approx 185 \text{ Mbps}
\end{align\*}Ingress bandwidth​=11574×2 KB=23.15 MBps=23.15 MBps×8≈185 Mbps​

The egress bandwidth depends on the size of the response. For a 5-second video generated at a rate of 30 frames per second, we have a size of 1.25 MB for a single request. This gives us the following egress bandwidth for a total of 11574 requests:

The system provides a video of 1.25 MB for a single request.

Egress bandwidth=11574×1.25 MB=14467.5 MBps=14467.5 MBps×8≈115740 Mbps≈116 Gbps\begin{align\*}
\text{Egress bandwidth}
&= 11574 \times 1.25 \text{ MB} \\
&= 14467.5 \text{ MBps} \\
&=14467.5 \text{ MBps} \times 8\approx 115740 \text{ Mbps} \\
&\approx 116 \text{ Gbps}
\end{align\*}Egress bandwidth​=11574×1.25 MB=14467.5 MBps=14467.5 MBps×8≈115740 Mbps≈116 Gbps​

So, we have the following number of resource estimations:

- **Storage required per day:** 1562.5 TB1562.5 \text{ TB}1562.5 TB
- **GPUs required to process 11574 TRPS:** 8208 NVIDIA A100 GPUs\text{8208 NVIDIA A100 GPUs}8208 NVIDIA A100 GPUs
- **Ingress bandwidth:** 185 Mbps185\text{ Mbps}185 Mbps
- **Egress bandwidth:**  116 Gbps116 \text{ Gbps}116 Gbps

![Estimated resources for the text-to-video generation system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Estimated resources for the text-to-video generation system")

Estimated resources for the text-to-video generation system

We have estimated the required resources for deploying a text-to-video generation model until now. Before moving toward the System Design, let’s consider some design considerations.

### Design considerations[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Design-considerations)

Some important factors and challenges that need to be carefully considered while designing the system:

- **Prompt understanding:** We should accurately interpret user prompts, considering natural language variations, ambiguous descriptions, and stylistic preferences. If we fail to address these variations, the system could misinterpret user intent, leading to incorrect outputs. We must implement robust text preprocessing and contextual understanding mechanisms to manage this.
- **Scene continuity:** We need to ensure the logical progression of scenes and maintain temporal and narrative coherence across the video. Without careful attention, scenes could become disjointed or unclear. This requires us to effectively integrate the scene planner, temporal sequencing, and storyboard services to guarantee smooth transitions and a cohesive storyline.
- **Asset diversity:** To meet diverse user needs, we must support various characters/objects, environments, and textures. This challenges us to ensure our model host and frame genration system is scalable and efficient enough to handle such diversity without performance issues. We achieve this by leveraging scalable asset databases.
- **Error handling and recovery:** We need to build a robust detection and recovery mechanism to handle failures in the video generation pipeline, such as missing assets or rendering errors. Without this, users could experience disruptions and compromise output reliability. We will address this by designing a system that quickly identifies issues and recovers without causing delays or interruptions.

Let’s move on to the System Design of the text-to-video generation system:

## System Design of the text-to-video generation system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#System-Design-of-the-text-to-video-generation-system)

The text-to-video generation system is composed of interconnected subsystems, each dedicated to specific tasks and domain-specific functions. These subsystems work collaboratively, interacting with one another to support the core model and enable the complete end-to-end video-generation process.

### The high-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-high-level-design)

Our proposed system consists of the following subsystems:

- **Prompt processing and embedding system:** This subsystem analyzes the raw text input, performing language detection, preprocessing, concept extraction, and style analysis to generate meaningful embeddings that capture the context and semantics of the text.
- **Model host and frame generation system:** This subsystem hosts the GenAI model that extracts static assets, such as characters and objects, from the input and brings them to life by generating realistic frames, ensuring dynamic and engaging visuals.
- **Rendering system:** This subsystem combines frames generated by the model host into a cohesive video sequence, applying post-processing effects to enhance visual quality.
- **Quality control system:** This subsystem ensures the generated video meets quality standards and aligns with the user’s intent, performing assessments and validations.

These six subsystems create a comprehensive and efficient text-to-video generation system, as shown in the following illustration:

![The high-level System Design of text-to-video generation system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The high-level System Design of text-to-video generation system")

The high-level System Design of text-to-video generation system

#### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Achieving-functional-requirements)

Let’s discuss how the subsystems integrate to meet the functional requirements that we identified:

- **Natural language understanding:** The prompt processing system achieves this by analyzing the text input, extracting key information, and generating embeddings to understand the user’s intent.
- **Video generation:** This is handled by the model host and rendering systems, which create and assemble the video content according to the processed text.
- **Input formats:** This requirement is handled by the prompt processing system designed to handle various input formats like JSON and plain text.
- **Customization:**The system allows for customization through the prompt processing and embedding system, which enables model host and frame generation to identify style preferences.
- **Output formats:** The rendering system supports multiple output formats to ensure compatibility with different platforms and use cases.

We now understand the system at a high level. Let’s move toward the detailed System Design and discuss each subsystem individually.

### The detailed System Design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-detailed-System-Design)

Let’s describe each component involved in the text-to-video generation system. We follow a modular approach by describing each subsystem individually.

#### Prompt processing and embedding system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Prompt-processing-and-embedding-system)

This backend system serves as the entry for processing user prompts, transforming raw input into enriched vector representation for downstream services. It’s designed to intelligently analyze, clean, and enrich user input, seamlessly bridging the gap between textual descriptions and multimodal representations.

Let’s describe each service in this subsystem:

- **Language analyzer:** This service receives the user’s prompt and detects the language. This ensures consistent language handling across the system, which enables downstream services to process the prompt accurately, regardless of the user’s language.
- **Text preprocessor:** This service cleans and normalizes the prompt by removing textual noise, tokenizing words, and performing lemmatization and parts-of-speech tagging. It also determines key phrases and narrative elements, standardizing and structuring the input text to make extracting meaningful information easier for other services.
- **Concept extractor:**This service extracts the primary and secondary concepts from the text, identifies objects, actions, relationships, and scene elements, and organizes them into a scene composition hierarchy. It transforms abstract text into a structured format of visual elements, laying the groundwork for generating a video scene.
- **Style analyzer:** This service extracts artistic style preferences from the input. It analyzes mood and emotional context and identifies visual aesthetics parameters, color schemes, and lighting. By capturing the user’s stylistic intent, it ensures that the generated video aligns with the desired artistic and emotional tone.

![Prompt preprocessing and embedding system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Prompt preprocessing and embedding system")

Prompt preprocessing and embedding system

- **Embedding and encoding generator:** This service creates a vector representation (embeddings) of text concepts to enable the system to map textual features to a visual feature space.
- **Dynamic contextualizer:** This service refines and balances the relationships between concepts, styles, and embedding to generate coherent and contextually relevant vector representation. It aligns the embeddings with the user’s intent (prompt). It ensures that the final vector representation captures a harmonious balance of user-specified elements, resulting in videos that accurately reflect the intended themes and relationships between objects.
- **Embeddings database:** It is a system of different databases (SQL, NoSQL, and vector databases) that store processed text, generated embeddings, reference mappings, and caches frequently used concepts for fast retrieval and comparison. By enabling efficient reuse and comparison of embeddings, this database speeds up the system’s response time and enhances the quality of generated videos by leveraging prior knowledge.

#### Model host and frame generation system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-host-and-frame-generation-system)

The model host and frame generation system takes contextual embeddings from the prompt processing and embedding system. It hosts the model and generates frames according to the information presented in the input. This subsystem works in the following three main stages:

- **Content planning:** It is the first crucial stage where the model breaks down the input into a structured sequence of actions and scenes. It creates a detailed storyboard, identifying key objects, their attributes, and intended actions. This planning phase helps ensure narrative coherence and temporal consistency throughout the video. The model generates scene descriptions, object relationships, and movement trajectories that will guide the subsequent generation steps.
- **Asset generation:** In the asset generation step, the model creates the individual visual elements needed for each frame. Using a specialized image generation model (similar to Stable Diffusion), it produces consistent visual assets like characters, objects, and backgrounds. The model maintains a “memory bank” of generated assets to ensure consistency across frames - for example, if a character appears in multiple scenes, their appearance remains stable. This stage also involves generating intermediate keyframes that will serve as anchors for the full animation sequence.
- **Motion synthesis and frame generation:** Motion Synthesis is the final and most complex stage, where the model brings everything to life. It uses a motion diffusion model to interpolate between keyframes while maintaining physical plausibility and temporal coherence. The model considers multiple factors like object persistence (ensuring objects don’t disappear randomly), physics constraints (natural movement patterns), and speed consistency. It generates intermediate frames using controlled noise diffusion, where each frame is influenced by both its neighboring frames and the original content plan. The model also employs motion modules that understand common movement patterns between frames, helping it generate smooth and natural-looking frames (animations).

![The content planning, asset generation, and motion synthesis stages of the model host subsystem](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The content planning, asset generation, and motion synthesis stages of the model host subsystem")

The content planning, asset generation, and motion synthesis stages of the model host subsystem

The process for this subsystem is iterative, with feedback loops between stages such as if the motion synthesis reveals issues with asset consistency, it can trigger regeneration of assets, or if movement patterns seem unnatural, it can refine the content plan. The model also uses attention mechanisms to maintain long-range consistency across the entire video sequence, ensuring that the final output tells a coherent visual story that matches the user’s original prompt.

#### Rendering system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Rendering-system)

The rendering system handles the final visual synthesis of the video, combining all the frames into a single video. It contains the following services:

- **Composition service:** This service assembles individual frames generated by the model host into a cohesive video by organizing them in sequence, applying frame rate and resolution settings, and encoding the frames into a compressed video format using advanced codecs and container structures.
- **Post-processing service:** It applies visual enhancements to the rendered frames, ensuring cinematic quality and artistic coherence. This includes color grading, motion blur, depth of field, and visual effects.
- **Rendered assets store:** A key-value store for quickly retrieving preprocessed assets like textures, models, and lighting configurations to optimize rendering speed.
- **Post-processing configuration database:** A document store with presets and parameters for post-processing effects to ensure consistent visual enhancements across projects.

![The rendering system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The rendering system")

The rendering system

#### Quality control system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Quality-control-system)

The quality control system ensures that generated video content meets quality, coherence, and relevance standards before final delivery. It includes the following services:

- **The quality assessment service:** This service analyzes visual quality, motion coherence, and aesthetic appeal, providing quality scores and issue reports.
- **The content validation service:** It checks narrative consistency, ensures compliance with guidelines, and identifies errors like missing elements or style mismatches, producing validation reports.
- **The optimization service:** This service fine-tunes videos for efficient delivery across platforms, using techniques like compression, real-time adjustments, and platform-specific adaptations.
- **Content database:** This database stores and manages generated content (video), including metadata, quality scores, indexed assets, and quality check rules. It also handles repeated requests for the same or similar videos.

![Quality control system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Quality control system")

Quality control system

#### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Putting-everything-together)

Let’s combine all the above subsystems to create a detailed System Design for the text-to-video generation system. As we can see, the system starts with the user’s input, which is directed to the prompt processing system via the load balancer.

##### Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Workflow-of-the-system)

The system’s flow starts with the user submitting a text prompt forwarded to the prompt processing and embedding system, where it undergoes several transformations. For instance, the language analyzer detects the prompt’s language, and the text processor cleans and standardizes the input. The concept extractor identifies the text’s key elements, objects, and actions, working in parallel with a style analyzer that determines artistic and visual parameters. These elements are processed by the embedding and encoding generator, which creates vector representations of the content, while the dynamic contextualizer ensures all elements are properly aligned and contextualized and stores these embeddings in the associated database. The processed and extracted information is then fed to the model host and frames generation system, where the desired animations (frames) are generated in several stages. Next, the rendering system processes everything through its composition and post-processing services, creating the final videos from the generated frames.

![The proposed System Design of the text-to-video generation system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The proposed System Design of the text-to-video generation system")

The proposed System Design of the text-to-video generation system

The quality control system continuously monitors the final output through its quality assessment, content validation, and optimization services to ensure the final video meets quality standards before delivery to the end user. Remember, the workflow maintains consistency and quality while allowing for iterations and improvements at each stage.

In the detailed design outlined above, we intentionally omitted to mention the API gateway, caching system, and feedback control system to keep the explanation concise. However, these components are essential for ensuring efficient, reliable, and seamless operations, and they should be considered integral to the overall architecture.

Let’s see how our proposed design meets the non-functional requirements.

## Fulfilling nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Fulfilling-nonfunctional-requirements)

Let’s dive into the details of how our proposed system achieves the non-functional requirements we described:

- **Scalability:** The system uses a modular architecture with various subsystems having numerous services divided at a granular level that can independently scale based on demand. Systems such as prompt processing and embedding, model host and frame generation, and rendering systems can be scaled horizontally by adding more instances to handle more requests. Also, embedding and asset databases can utilize distributed NoSQL solutions to handle massive data loads efficiently.
- **Performance:** High performance is achieved through optimized algorithms and parallel processing. Caching systems ensure that frequently used data is quickly accessible, reducing response time. The frame generation tasks use GPU-based parallel processing to speed up the final rendering process.
- **Reliability:** Reliability is ensured through fault tolerance and redundant services. Critical services, such as quality control and rendering systems, can be monitored with health checks and auto-restarted or scaled when failures are detected. The quality control system also ensures that content quality checks are always available before final delivery.
- **Availability:** High availability is maintained by deploying services across multiple availability zones or regions. Load balancing between servers ensures that traffic is distributed evenly across available resources, preventing any single point of failure. The model host and rendering systems can operate in a failover configuration to provide continuous operation.
- **Security and privacy:** Security and privacy can be addressed through strong data encryption, access control, and privacy policies. User-generated data, including prompts and videos, is encrypted in transit and at rest. Privacy is safeguarded by ensuring no personally identifiable information (PII) is collected or stored without user consent. Specifically, the quality control system ensures that the generated video does not produce harmful content and avoids resemblance to personal information. It actively monitors the output to prevent the inclusion of sensitive or inappropriate material, ensuring the video adheres to ethical guidelines and privacy standards.

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Conclusion)

This lesson presented a text-to-video generation system integrating multiple subsystems to transform textual prompts into video. We started with the initial resource estimations for approximately 100 million daily active users and gradually moved to the System Design. The system’s modular design allows for scaling of components and reliability. Features like distributed databases, caching, and parallel processing ensure optimal performance. We also discussed strategies to achieve essential nonfunctional requirements.

Design a Text-to-Speech Generation System

Design an Image Captioning System

Ask

[Requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Nonfunctional-requirements)

[Model selection](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-selection)

[The training process](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-training-process)

[Data acquisition and preparation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-acquisition-and-preparation)

[Source of training data](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Source-of-training-data)

[Dataset format](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Dataset-format)

[Data preprocessing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Data-preprocessing)

[Database selection](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Database-selection)

[Time estimation for data processing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Time-estimation-for-data-processing)

[Model training and testing](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-training-and-testing)

[Distributing the training load](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Distributing-the-training-load)

[Model evaluation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-evaluation)

[Evaluation metrics](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Evaluation-metrics)

[Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Storage-estimation)

[Inference servers estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Inference-servers-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Bandwidth-estimation)

[Design considerations](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Design-considerations)

[System Design of the text-to-video generation system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#System-Design-of-the-text-to-video-generation-system)

[The high-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-high-level-design)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Achieving-functional-requirements)

[The detailed System Design](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#The-detailed-System-Design)

[Prompt processing and embedding system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Prompt-processing-and-embedding-system)

[Model host and frame generation system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Model-host-and-frame-generation-system)

[Rendering system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Rendering-system)

[Quality control system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Quality-control-system)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Workflow-of-the-system)

[Fulfilling nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Fulfilling-nonfunctional-requirements)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-text-to-video-generation-system#Conclusion)