# Estimating_Training_Compute_and_Cost_for_GenAI_Models

Source: https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Estimating Training Compute and Cost

Learn the essentials of back-of-the-envelope calculations to estimate the training resources required for GenAI applications.

We'll cover the following...

- [Why do BOTECs matter in GenAI?](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Why-do-BOTECs-matter-in-GenAI)
- [Training estimations](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Training-estimations)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Conclusion)

One of the most critical steps when designing and implementing generative AI (GenAI) systems is resource estimation. Whether you're training a new model or deploying an inference system for millions of users, understanding the required resources (computational power, storage, and bandwidth) can save significant time and cost. However, detailed calculations can be time-consuming and require access to precise technical details. This is where back-of-the-envelope calculations (BOTECs) come into play.

**Back-of-the-envelope calculations (BOTECs)** are quick, rough estimations that provide a high-level understanding of what a system might require regarding resources. These calculations aren’t about pinpoint accuracy but getting a reliable ballpark figure to guide decision-making. For instance, we might want to estimate how many GPUs we’ll need before training a large language model or how long the training will take. Similarly, for deployment, we can use BOTECs to predict the number of inference servers required to handle user requests.

![Resource estimation in GenAI systems](images/img_2b66f684bb1f.svg "Resource estimation in GenAI systems")

Resource estimation in GenAI systems

In this lesson, we’ll explore the basics of BOTECs for training and deploying GenAI systems, starting with the training time and resource estimation.

## Why do BOTECs matter in GenAI?[#](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Why-do-BOTECs-matter-in-GenAI)

BOTECs help GenAI engineers make informed resource and performance decisions before detailed measurements or tooling are available. Because GenAI systems operate at large scales, even small estimation errors can lead to significant waste in GPU usage, training time, storage, or serving costs. BOTECs also play an important role in technical interviews, where candidates are expected to break down complex system requirements and reason through estimates such as GPU capacity, training time, and storage needs. Developing this skill helps engineers make practical decisions quickly and communicate their reasoning with confidence.

In this chapter, we will focus on three types of BOTECs:

1. Estimating training compute and cost
2. Estimating training compute and cost
3. Token math and unit economics

Let’s start with the model training estimations to devise some mathematical formulations:

## Training estimations[#](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Training-estimations)

In the training phase of building a generative AI system using a large model like the Llama model, we want to determine how long it would take to train it on a certain amount of data. The Llama 2-70B model took around 1.7 million GPU hours using NVIDIA A100 GPUs. Calculating this beforehand allows us to plan resources accordingly and build systems in a realistic time frame. For example, using one GPU to train Llama 2-70B would take ~195 years, while using a cluster of 10,000 GPUs would take around one week. There is also the cost aspect.

It is reported that Llama 2-70B took around $3.9 M to train. Once we estimate the GPU hours it would take to train a model, we can also predict the cost with some certainty.

As we know, training any model usually means we are passing our data through the model and updating its internal weights. Both these processes require mathematical calculations like multiplying or adding certain values. To estimate the time it takes to train a model, we need the answers to these two questions:

1. How many calculations will be performed?
2. How many calculations can be done in a certain time (e.g., one second)?

The calculations we refer to here are **FLOPS (floating point operations)**. A **floating point** is simply a number with a decimal point. Without diving into the specifics of a model’s architecture, we cannot know how many calculations will be performed during one forward/backward pass, so we need to make some informed guesses.

The BOTEC calculations and equations presented in this course are intended as a foundational blueprint for understanding resource estimation in GenAI systems. While they provide valuable insights and a framework for analysis, they should not be taken as precise references for real-world System Design. The actual resource requirements of GenAI systems can vary significantly depending on numerous factors beyond the scope of these simplified examples. However, the principles and techniques discussed here will be a solid reference for designing and optimizing GenAI systems throughout this course.

Let’s look at an example of how we can estimate these FLOPS:

![A simple neural network](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A simple neural network")

A simple neural network

The network is configured with two input nodes, three hidden layer nodes, and one output node.

The total number of parameters in the network are:

Nparams=2×3 + 3×1=9\text{N}\_{\text{params}} = 2 \times 3 \ + \ 3 \times 1 = 9
Nparams​=2×3 + 3×1=9

For one feedforward pass through the network, we will need the following calculations:

H1=(X1×WX1H1)+(X2×WX2H1) +b1\text{H}\_1 = (\text{X}\_1 \times \text{W}\_{\text{X1H1}}) + (\text{X}\_2 \times \text{W}\_{\text{X2H1}})  + \text{b}\_1
H1​=(X1​×WX1H1​)+(X2​×WX2H1​) +b1​

H2=(X1×WX1H2)+(X2×WX2H2)+b1\text{H}\_2 = (\text{X}\_1 \times \text{W}\_{\text{X1H2}}) + (\text{X}\_2 \times \text{W}\_{\text{X2H2}}) + \text{b}\_1
H2​=(X1​×WX1H2​)+(X2​×WX2H2​)+b1​

H3=(X1×WX1H3)+(X2×WX2H3)+b1\text{H}\_3 = (\text{X}\_1 \times \text{W}\_{\text{X1H3}}) + (\text{X}\_2 \times \text{W}\_{\text{X2H3}}) + \text{b}\_1
H3​=(X1​×WX1H3​)+(X2​×WX2H3​)+b1​

Where b1b\_1b1​ is the bias value of the first layer. We can see that the first few calculations require 4+4+44 + 4 + 44+4+4 FLOPS. Next, we have:

O=(H1×WH1O)+(H2×WH2O) +(H3×WH3O)+b2\text{O} = (\text{H}\_1 \times \text{W}\_{\text{H1O}}) + (\text{H}\_2 \times \text{W}\_{\text{H2O}})  + (\text{H}\_3 \times \text{W}\_{\text{H3O}})+ \text{b}\_2
O=(H1​×WH1O​)+(H2​×WH2O​) +(H3​×WH3O​)+b2​

This requires 6 FLOPS. In total, we need 18 FLOPS for the feedforward pass for one set of inputs. This is exactly 2×Nparams2 \times N\_{params}2×Nparams​. Similarly, backward passes usually take at least 4×Nparams4 \times N\_{params}4×Nparams​ FLOPS. So, we can *estimate* the number of FLOPS required for training a neural network on one data input to be 6×Nparams6 \times N\_{params}6×Nparams​.

Once we have these values, calculating the training time is as simple as:

Tsec=Total FLOPSFLOPS per second \text{T}\_{\text{sec}} = \frac{\text{Total FLOPS}}{\text{FLOPS per second}} 
Tsec​=FLOPS per secondTotal FLOPS​

When training on a large dataset of inputs, calculating the total number of FLOPS requires the following variables:

1. The number of parameters (Nparams\text{N}\_{\text{params}} Nparams​)
2. The number of FLOPS needed for processing one data item (NFLOPS\text{N}\_{\text{FLOPS}}NFLOPS​), which we calculate to be 6 for the training
3. The number of epochs (E\text{E}E)
4. The number of data items (D\text{D}D)

**Note:** We assume that each data item’s size does not matter for training time estimation. In reality, retrieving data requires resources, but we will not consider them for our calculations as they depend on many factors, like network bandwidth and data size.

So, the total FLOPS can be calculated as:

Total FLOPS=Nparams×NFLOPS×E×D\text{Total FLOPS} = \text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D}Total FLOPS=Nparams​×NFLOPS​×E×D

We can divide this by the number of FLOPS one GPU can compute per second (rate of operations RopsR\_{ops}Rops​) to get the training time in seconds.

Tsec=Nparams×NFLOPS×E×DRops\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D}}{\text{R}\_{\text{ops}}}Tsec​=Rops​Nparams​×NFLOPS​×E×D​

This will give us the training time for one GPU, but as we'll see later in the lesson on [parallelism in GenAI models](https://www.educative.io/courses/generative-ai-system-design/parallelism-in-genai-models), we use multiple machines to parallelize and speed up the training process. We must divide the time for one GPU by the number of GPUs to reflect that. In other words:

Tsec=Nparams×NFLOPS×E×DRops×NGPUs\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D}}{\text{R}\_{\text{ops}} \times \text{N}\_{\text{GPUs}}} Tsec​=Rops​×NGPUs​Nparams​×NFLOPS​×E×D​

However, as we know, different model architectures require different training and inferencing strategies. For example, a GAN (generative adversarial network) may be able to produce an output in a single time step, while a diffusion model may produce its output in 20-100 time steps. This can significantly affect the training time. We need a variable to reflect the parameters for different model architectures and applications; let’s call it C\text{C}C.

Tsec=Nparams×NFLOPS×E×D×CRops×NGPUs\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D} \times \text{C}}{\text{R}\_{\text{ops}} \times \text{N}\_{\text{GPUs}}}Tsec​=Rops​×NGPUs​Nparams​×NFLOPS​×E×D×C​

This CCC will be different for each GenAI application, for example:

- For text-to-text generation, in the training phase, the model generates the whole sentence in one time step, while in inference, it takes multiple iterations. So, for the training time estimation, we can set C=1\text{C} = 1C=1; for inference, we can set C=Niters\text{C} = \text{N}\_{\text{iters}}C=Niters​.
- For text-to-image generation, using diffusion models (as we do in this course) requires considering the number of iterations or time steps to set C=Nsteps\text{C} = \text{N}\_{\text{steps}}C=Nsteps​.
- For a text-to-speech generation, as it is generally an iterative process, we can set C=Niters\text{C} = \text{N}\_{\text{iters}}C=Niters​.
- Again, diffusion models require time steps for text-to-video generation, so that we can set C=Nsteps\text{C}=\text{N}\_{\text{steps}}C=Nsteps​.

Of course, these are just some parameters we need to consider when designing and building GenAI systems, and they depend on factors like the model architecture. So, you must use your expertise and justify your parameter choice here.

> We can set:
>
> - NFLOPS=2\text{N}\_{\text{FLOPS}} = 2NFLOPS​=2 for feedforward pass
> - E=D=1\text{E} = \text{D} = 1E=D=1 for one input
> - NGPUs=1\text{N}\_{\text{GPUs}} = 1NGPUs​=1
>
> To calculate the time taken for inference for a single input on a single GPU: Tinference=Nparams×2×CRops\text{T}\_{\text{inference}} = \frac{\text{N}\_{\text{params}} \times 2 \times \text{C}}{\text{R}\_{\text{ops}}}Tinference​=Rops​Nparams​×2×C​

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Conclusion)

BOTECs are quick and rough estimations that help you understand the resources needed for a system. They are crucial in GenAI for managing resources, optimizing performance, and making informed decisions early on. They’re also valuable in technical interviews to show your problem-solving skills. We can estimate the training time with the following formula:

Tsec=Nparams×NFLOPS×E×D×CRops×NGPUs\text{T}\_{\text{sec}} = \frac{\text{N}\_{\text{params}} \times \text{N}\_{\text{FLOPS}} \times \text{E} \times \text{D} \times \text{C}}{\text{R}\_{\text{ops}} \times \text{N}\_{\text{GPUs}}}Tsec​=Rops​×NGPUs​Nparams​×NFLOPS​×E×D×C​

And inference time with this one:

Tinference=Nparams×2×CRops \text{T}\_{\text{inference}} = \frac{\text{N}\_{\text{params}} \times 2 \times \text{C}}{\text{R}\_{\text{ops}}}Tinference​=Rops​Nparams​×2×C​

**Test your knowledge!**

Using the formula above, can you estimate the inference time Tinference\text{T}\_\text{{inference}}Tinference​ in seconds for a model with one million trainable parameters, assuming the rate of operations to be one million FLOPS/sec, and the constant C\text{C}C is 1.   
Attempt your solution in the widget below.

AI Powered

Saved

12 attempts left

Reset

Inference Time Calculation

Hi! I’m Ed. I’ll help you practice System Design interview questions from Grokking the Generative AI System Design.

Would you prefer to be mentored with hints and explanations or evaluated on your answers?

You have 12 attempts to answer.

Let’s now look at the estimations for deploying the trained models to build an end-to-end system.

Where the LLM Fits and Where Determinism Wins

Estimating Inference Capacity and Fleet Size

Ask

[Why do BOTECs matter in GenAI?](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Why-do-BOTECs-matter-in-GenAI)

[Training estimations](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Training-estimations)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost#Conclusion)