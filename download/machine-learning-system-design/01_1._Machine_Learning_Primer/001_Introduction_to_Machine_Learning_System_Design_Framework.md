# Introduction_to_Machine_Learning_System_Design_Framework

Source: https://www.educative.io/courses/machine-learning-system-design/introduction

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Machine Learning System Design](https://www.educative.io/courses/machine-learning-system-design)

# Introduction

Explore the essential principles of machine learning system design through a structured six-step framework. Understand key aspects like problem formulation, metric selection, training requirements, model evaluation, system architecture, and scalability. This lesson equips you to approach ML system design challenges confidently in technical interviews and real-world applications.

We'll cover the following...

- [What to expect in a machine learning interview](https://www.educative.io/courses/machine-learning-system-design/introduction#What-to-expect-in-a-machine-learning-interview)
  - [Why machine learning system design matters](https://www.educative.io/courses/machine-learning-system-design/introduction#Why-machine-learning-system-design-matters)
  - [How will this course help you?](https://www.educative.io/courses/machine-learning-system-design/introduction#How-will-this-course-help-you)
- [The 6-step framework for machine learning system design](https://www.educative.io/courses/machine-learning-system-design/introduction#The-6-step-framework-for-machine-learning-system-design)
  - [Step 1: Define the problem statement](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-1-Define-the-problem-statement)
    - [Ask clarifying questions](https://www.educative.io/courses/machine-learning-system-design/introduction#Ask-clarifying-questions)
  - [Step 2: Identify the right metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-2-Identify-the-right-metrics)
    - [Offline metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Offline-metrics)
    - [Online metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Online-metrics)
  - [Step 3: Identify system requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-3-Identify-system-requirements)
    - [Training requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Training-requirements)
    - [Inference requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Inference-requirements)
  - [Step 4: Train and evaluate the model](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-4-Train-and-evaluate-the-model)
  - [Step 5: Design the high-level system](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-5-Design-the-high-level-system)
  - [Step 6: Scale the system](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-6-Scale-the-system)

## What to expect in a machine learning interview[#](https://www.educative.io/courses/machine-learning-system-design/introduction#What-to-expect-in-a-machine-learning-interview)

- Most major companies, i.e. Facebook, LinkedIn, Google, Amazon, and Snapchat, expect Machine Learning engineers to have solid engineering foundations and hands-on Machine Learning experiences. This is why interviews for Machine Learning positions share similar components with interviews for traditional software engineering positions. The candidates go through a similar method of problem solving (Leetcode style), system design, knowledge of machine learning and machine learning system design.
- The standard development cycle of machine learning includes data collection, problem formulation, model creation, implementation of models, and enhancement of models. It is in the company’s best interest throughout the interview to gather as much information as possible about the competence of applicants in these fields. There are plenty of resources on how to train machine learning models and how to deploy models with different tools. However, there are no common guidelines for approaching machine learning system design from end to end. This was one major reason for designing this course.

### Why machine learning system design matters[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Why-machine-learning-system-design-matters)

A typical machine learning development cycle includes:

- Data collection
- Problem formulation
- Model training
- Deployment
- Continuous improvement

While there are many resources on training models and deploying them with tools, there is no universally accepted framework for designing an end-to-end machine learning system.

This gap is especially visible in interviews, where candidates are expected to reason about:

- Trade-offs
- Scalability
- Metrics
- Latency
- Reliability

This course was designed to fill that gap.

### How will this course help you?[#](https://www.educative.io/courses/machine-learning-system-design/introduction#How-will-this-course-help-you)

In this course, we will learn how to approach machine learning system design from a top-down view. It’s important for candidates to realize the challenges early on and address them at a structural level. Here is one example of the thinking flow.

## The 6-step framework for machine learning system design[#](https://www.educative.io/courses/machine-learning-system-design/introduction#The-6-step-framework-for-machine-learning-system-design)

We’ll use a 6-step framework throughout the course to design systems such as:

- Feed ranking
- Video recommendation
- Ads click prediction
- Rental search ranking

![The 6 basic steps to approach Machine Learning System Design](001_Introduction_to_Machine_Learning_System_Design_Framework_images/img_a636678446f5.svg "The 6 basic steps to approach Machine Learning System Design")

The 6 basic steps to approach Machine Learning System Design

### Step 1: Define the problem statement[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-1-Define-the-problem-statement)

A strong system design always starts with a clear problem statement.

Candidates must:

- Understand the intent of the system
- Clarify what is being optimized
- Explicitly state assumptions

#### Ask clarifying questions[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Ask-clarifying-questions)

For example, in a **LinkedIn Feed Ranking** interview:

> *“Design the LinkedIn feed ranking system.”*

Before designing anything, a good candidate would ask:

- Is the feed chronological or relevance-based?
- How should sponsored ads be balanced with organic content?
- What user actions matter most (clicks, dwell time, shares)?

Clarifying these early helps align expectations and guides metric selection.

### Step 2: Identify the right metrics[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-2-Identify-the-right-metrics)

Once the problem is clear, we define success metrics.

#### Offline metrics[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Offline-metrics)

Used during development to evaluate models quickly:

- Log loss
- AUC (for classification)
- RMSE or MAPE (for forecasting problems)

#### Online metrics[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Online-metrics)

Used after deployment:

- Click-through rate (CTR)
- Engagement
- Revenue lift

### Step 3: Identify system requirements[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-3-Identify-system-requirements)

Machine learning systems must satisfy both training and inference constraints.

#### Training requirements[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Training-requirements)

Training pipelines often include:

- Data collection
- Feature engineering
- Feature selection
- Loss function design

For example, in a YouTube video recommendation system, most recommended videos are *not* watched, resulting in highly imbalanced data.

Key questions include:

- How do we train models with extreme class imbalance?
- How often should models be retrained?
- How do we prevent models from going stale?

#### Inference requirements[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Inference-requirements)

Once deployed, models must:

- Serve predictions with low latency (often <100 ms)
- Scale to millions of users
- Remain highly available

Designing inference systems requires careful trade-offs between:

- Accuracy
- Speed
- Cost

### Step 4: Train and evaluate the model[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-4-Train-and-evaluate-the-model)

At this stage, we focus on:

- Feature engineering
- Feature selection
- Model choice

Throughout the course, we’ll discuss practical design decisions, such as:

- Whether to use IDs as embeddings
- How to encode geographic features efficiently
- When simpler models outperform complex ones

### Step 5: Design the high-level system[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-5-Design-the-high-level-system)

Here, we design the end-to-end architecture and explain how data flows through the system.

The goal is to create a minimal, viable system design that:

- Solves the problem
- Is easy to explain
- Can be scaled later

For example, a Video Recommendation System typically includes:

- A candidate generation service
- A ranking model service

### Step 6: Scale the system[#](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-6-Scale-the-system)

Finally, we analyze system bottlenecks and scaling strategies.

Key questions include:

- Which components are likely to be overloaded?
- How do we scale them horizontally?
- How do we handle partial failures?

Scaling discussions are often what differentiate strong interview candidates from average ones.

Feature Selection and Feature Engineering

Ask

[What to expect in a machine learning interview](https://www.educative.io/courses/machine-learning-system-design/introduction#What-to-expect-in-a-machine-learning-interview)

[Why machine learning system design matters](https://www.educative.io/courses/machine-learning-system-design/introduction#Why-machine-learning-system-design-matters)

[How will this course help you?](https://www.educative.io/courses/machine-learning-system-design/introduction#How-will-this-course-help-you)

[The 6-step framework for machine learning system design](https://www.educative.io/courses/machine-learning-system-design/introduction#The-6-step-framework-for-machine-learning-system-design)

[Step 1: Define the problem statement](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-1-Define-the-problem-statement)

[Ask clarifying questions](https://www.educative.io/courses/machine-learning-system-design/introduction#Ask-clarifying-questions)

[Step 2: Identify the right metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-2-Identify-the-right-metrics)

[Offline metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Offline-metrics)

[Online metrics](https://www.educative.io/courses/machine-learning-system-design/introduction#Online-metrics)

[Step 3: Identify system requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-3-Identify-system-requirements)

[Training requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Training-requirements)

[Inference requirements](https://www.educative.io/courses/machine-learning-system-design/introduction#Inference-requirements)

[Step 4: Train and evaluate the model](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-4-Train-and-evaluate-the-model)

[Step 5: Design the high-level system](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-5-Design-the-high-level-system)

[Step 6: Scale the system](https://www.educative.io/courses/machine-learning-system-design/introduction#Step-6-Scale-the-system)