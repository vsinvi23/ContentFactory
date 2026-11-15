# Understanding_the_Training_Loop_in_Large_Language_Models

Source: https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# How LLMs Learn (The Training Loop)

Understand the core mechanics of how large language models learn over time. This lesson explains the training loop process, including token prediction, loss computation, backpropagation, and parameter updates. Learn how repeated small steps across massive datasets enable models to generate coherent text without human-like reasoning.

We'll cover the following...

- [What does it mean for an LLM to learn?](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#What-does-it-mean-for-an-LLM-to-learn)
- [Self-supervised learning through text](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Self-supervised-learning-through-text)
- [The training loop](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-training-loop)
- [Prediction: Making a guess](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Prediction-Making-a-guess)
- [The loss function: Knowing when the model is wrong](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-loss-function-Knowing-when-the-model-is-wrong)
  - [A simplified numerical intuition](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#A-simplified-numerical-intuition)
- [Backpropagation](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Backpropagation)
- [Weight updates: Where learning actually happens](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Weight-updates-Where-learning-actually-happens)
- [Why scale matters](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Why-scale-matters)
- [Training vs. inference](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Training-vs-inference)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Conclusion)

In this course, we introduced a formula that estimates how long it takes to train a large language model. Depending on the number of parameters, the size of the dataset, and the number of training epochs, this process can span hundreds of days on large-scale hardware. While the formula helps quantify the cost of training, it does not explain *what* is actually happening during that time.

This lesson focuses on the mechanics of learning in large language models. Instead of diving into mathematical derivations, we will take a conceptual view of how an LLM improves over time. The goal is to understand what “learning” means in this context and how the training loop gradually transforms an untrained model into a system capable of generating coherent and useful text.

## What does it mean for an LLM to learn?[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#What-does-it-mean-for-an-LLM-to-learn)

Large language models do not learn concepts, facts, or rules in the way humans do. They do not store explicit knowledge about the world, nor do they reason symbolically about language. Instead, their learning objective is much simpler and more mechanical.

An LLM learns by repeatedly predicting the *next token* in a sequence.

A **token** is a basic unit of text used by the model. Depending on the tokenizer, a token may represent a full word, a word fragment, punctuation, or whitespace. During training, the model is shown a sequence of tokens and asked to predict the next token.

For example, given the sequence:

Ace Editor

1

“The capital of France is”

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The correct next token is:

Ace Editor

1

“Paris”

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The model makes a prediction, compares it with the actual next token from the training data, and adjusts itself if the prediction is incorrect. This process is repeated across massive datasets containing trillions of tokens.

Let’s look at how models learn through these tokens.

## Self-supervised learning through text[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Self-supervised-learning-through-text)

The common training approach is known as **self-supervised learning**. Unlike traditional supervised learning, there is no need for manually labeled data. The structure of the text itself provides supervision.

Every sentence in the training corpus naturally contains both:

- An input (all tokens except one).
- A target (the next token to be predicted).

For instance, if the training data contains the sentence:

Ace Editor

1

“Large language models learn from data.”

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The model can be trained using:

- **Input:** “Large language models learn from”
- **Target:** “data”

Because the correct answer is already present in the data, no external labeling process is required. This enables training models on extremely large, diverse datasets collected from books, articles, code repositories, and other text sources.

It is important to note that the model does not “know” what the sentence means. It only learns that certain token sequences are statistically likely to follow others. Over time, as it is exposed to more data, the model becomes increasingly accurate at making these predictions.

## The training loop[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-training-loop)

The learning process of an LLM is structured as a loop that is repeated continuously during training. Each iteration of this loop slightly improves the model’s parameters. Individually, these improvements are small, but at scale, they accumulate into significant capability.

At a high level, the training loop consists of four steps:

1. The model predicts the next token.
2. The prediction is evaluated using a loss function.
3. The error is propagated backward through the model.
4. The model’s weights are updated to reduce future error.

This loop is executed billions or even trillions of times during training.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271331%27%20height=%27381%27/%3e)![Next-token prediction training flows from input text through tokenization and model prediction to loss feedback](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Next-token prediction training flows from input text through tokenization and model prediction to loss feedback")

Next-token prediction training flows from input text through tokenization and model prediction to loss feedback

In the following sections, we will examine each step of this loop in detail, starting with the model’s prediction.

## Prediction: Making a guess[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Prediction-Making-a-guess)

During training, the model receives a sequence of tokens as input. Using its current set of parameters, it processes this sequence and produces a prediction for the next token. Importantly, the model does not directly output a single token. Instead, it generates a *probability distribution* over all tokens in its vocabulary.

For example, given an input sequence, the model might assign:

- 60% probability to one token.
- 25% to another.
- And smaller probabilities to many others.

The token with the highest probability is considered the model’s prediction. Early in training, these predictions are often close to random. As training progresses, the probability mass increasingly shifts toward correct or plausible tokens.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27881%27%20height=%27391%27/%3e)![Flow through an LLM from raw text to next-token probability predictions](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Flow through an LLM from raw text to next-token probability predictions")

Flow through an LLM from raw text to next-token probability predictions

This prediction step is purely computational. It consists of matrix multiplications, non-linear transformations, and a final normalization step that converts raw scores into probabilities. There is no memory of past predictions and no awareness of meaning—only numerical computation based on the current weights.

## The loss function: Knowing when the model is wrong[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-loss-function-Knowing-when-the-model-is-wrong)

Once the model produces a prediction for the next token, that prediction must be evaluated. The training process needs a way to measure how good or bad the model’s guess was. This is the role of the **loss function**.

A loss function takes two inputs:

- The model’s predicted probability distribution over tokens.
- The correct next token from the training data.

It then produces a single numerical value called the **loss**. This value represents how far the model’s prediction was from the correct answer. A lower loss indicates a better prediction, while a higher loss indicates a worse one.

For example, if the correct next token is `"Paris"` and the model assigns a high probability to `"Paris"`, the loss will be small. If the model assigns most of its probability to an incorrect token, such as `"London"`, the loss will be large, especially if the model was very confident in that incorrect prediction.

This behavior is important. The loss function penalizes confident mistakes more heavily than uncertain ones. As a result, the model is encouraged not only to predict the correct token, but to do so with appropriate confidence.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271071%27%20height=%27411%27/%3e)![How weight updates differ for a confident correct prediction vs. a confident wrong prediction](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "How weight updates differ for a confident correct prediction vs. a confident wrong prediction")

How weight updates differ for a confident correct prediction vs. a confident wrong prediction

### A simplified numerical intuition[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#A-simplified-numerical-intuition)

To build intuition, imagine that tokens are represented as vectors in a low-dimensional space. This is not exactly how loss is computed in practice, but it helps illustrate the idea.

Suppose the correct token `"Tea"` is represented by the vector:

Ace Editor

1

Tea = [1.0, 0.0]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Now consider two confident predictions made by the model:

Ace Editor

1

2

Coffee = [0.8, 0.2]

Pink = [-0.9, 0.1]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Using a simple distance-based loss such as **Euclidean distance**, we can compute how far each prediction is from the correct answer.

- Distance(Tea, Coffee)\text{Distance(Tea, Coffee)}Distance(Tea, Coffee):  
  =(1.0−0.8)2+(0.0−0.2)2)=\sqrt{(1.0 − 0.8)^{2} + (0.0 − 0.2)^{2}})=(1.0−0.8)2+(0.0−0.2)2​)  
  =(0.04+0.04)= \sqrt{(0.04 + 0.04)}=(0.04+0.04)​  
  =0.08= \sqrt{0.08}=0.08​ (small loss)
- Distance(Tea, Pink)\text{Distance(Tea, Pink)}Distance(Tea, Pink):  
  =(1.0+0.9)2+(0.0−0.1)2= \sqrt{(1.0 + 0.9)^{2} + (0.0 − 0.1)^{2}}=(1.0+0.9)2+(0.0−0.1)2​  
  =(3.61+0.01)= \sqrt{(3.61 + 0.01)}=(3.61+0.01)​  
  =3.62= \sqrt {3.62}=3.62​ (large loss)

In this simplified view, `"Coffee"` results in a smaller loss because it is closer to the correct token `"Tea"`, while `"Pink"` produces a much larger loss. The key idea is that “not all mistakes are treated equally.” Confident predictions that are far from the correct answer generate stronger correction signals.

In practice, large language models commonly use a loss function based on cross-entropy. While the mathematical details are beyond the scope of this lesson, the intuition is straightforward: the loss function answers the question, *“How surprised should the model be by the correct answer?”*

## Backpropagation[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Backpropagation)

Once the loss has been computed, the model knows *that* it made a mistake, but not *why* it made that mistake. To improve, it must determine which parts of the model contributed to the error. This is where backpropagation comes in.

**Backpropagation** is the process of propagating the error signal backward through the neural network. Starting from the loss value, the algorithm traces how each layer and each parameter influenced the final prediction. Each weight in the model receives a signal indicating how much it contributed to the error and in which direction it should change to reduce that error in the future.

An intuitive analogy is debugging a complex software system. When a bug appears in the final output, you trace the execution path backward to identify which functions or components caused the problem. Similarly, backpropagation traces the prediction backward through the network to assign responsibility for the mistake.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271071%27%20height=%27321%27/%3e)![How backpropagation affects the different layers in a transformer-based model](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "How backpropagation affects the different layers in a transformer-based model")

How backpropagation affects the different layers in a transformer-based model

It is important to note that backpropagation does not introduce understanding or reasoning into the model. It is a mathematical procedure that computes gradients—signals that indicate how changing each parameter would affect the loss.

## Weight updates: Where learning actually happens[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Weight-updates-Where-learning-actually-happens)

After backpropagation determines how each weight contributed to the error, the model performs a **weight update**. This is the step where learning actually occurs.

Each weight in the model is adjusted slightly in a direction that reduces the loss. These adjustments are typically very small. A single update does not meaningfully change the model’s behavior. However, when this process is repeated billions of times across massive datasets, the cumulative effect becomes significant.

The size and direction of these updates are controlled by an **optimizer**, such as Adam or stochastic gradient descent. The optimizer determines how aggressively the model updates its weights and helps maintain stable learning across many training steps.

We can see a simple example of a weight update method below:

#### 

|  |  |  |
| --- | --- | --- |
|  | A | B |
| 1 | Original Weight | 0.5 |
| 2 | Gradient | +0.2 |
| 3 | Learning Rate | 0.01 |
| 4 | Weight Delta | f0.002 |
| 5 | New Weight | f0.498 |

Try changing the values in yellow to see how they affect the new weight.

One full cycle of prediction, loss computation, backpropagation, and weight update is often referred to as a **training step**. During large-scale training, models may perform trillions of such steps.

This is what fills those hundreds of days of training time: countless tiny numerical adjustments that gradually shape the model’s behavior.

## Why scale matters[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Why-scale-matters)

The training loop described so far is conceptually simple. What makes large language models powerful is not the complexity of the loop, but the *scale* at which it is executed.

Two forms of scale are particularly important:

- The size of the dataset.
- The number of parameters in the model.

Larger datasets expose the model to a wider range of language patterns, styles, and contexts. This reduces overfitting and allows the model to generalize better to new inputs.

More parameters increase the model’s capacity to store and represent these patterns. A small model quickly reaches a performance ceiling, even with large amounts of data. Larger models can continue improving as both data and training time increase.

As model size increases, performance improves rapidly at first, then slows down. This explains why larger models require disproportionately more data, compute, and training time for smaller gains.

Model size vs. relative performance

This explains why training time grows so rapidly with model size. Increasing the number of parameters and tokens processed per epoch dramatically increases the number of training steps required. The formula introduced in the course captures this growth mathematically, but conceptually it reflects a simple reality: learning at scale is expensive.

## Training vs. inference[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Training-vs-inference)

It is important to distinguish between training and inference, as these two phases are often confused.

**Training** is the phase where learning occurs. During training:

- Predictions are evaluated using a loss function.
- Backpropagation is performed.
- Model weights are updated.

**Inference**, on the other hand, is the phase where the trained model is used to generate outputs. During inference:

- The model makes predictions.
- No loss is computed.
- The weights remain fixed.

This distinction has an important implication: a deployed LLM does not learn from user interactions. When the model generates a response during inference, it is simply applying patterns learned during training. Any improvement to the model requires returning to the training phase and updating the weights offline.

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Training** | **Inference** |
| **Purpose** | Learn patterns from data | Apply learned patterns to new inputs |
| **Weight Updates** | Weights are continuously updated | Weights remain fixed |
| **Loss Computation** | Loss is computed for each prediction | No loss is computed |
| **Backpropagation** | Performed to assign error and update weights | Not performed |
| **Data Requirement** | Large labeled or self-supervised datasets | Single-user prompt |
| **Compute Cost** | Extremely high (GPUs/TPUs over weeks or months) | Relatively low per request |
| **Time Scale** | Days to months | Milliseconds to seconds |
| **Learning** | Model improves over time | No learning occurs |

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Conclusion)

Large language models learn through a simple but highly repeated process. They predict the next token, measure how wrong they were, propagate that error backward, and slightly adjust their parameters. Individually, these steps are small and mechanical. At scale, repeated across massive datasets and large models, they give rise to behavior that appears intelligent.

CPU vs. GPU vs. TPU for AI and Machine Learning

Basics of Variational Autoencoders (VAEs)

Ask

[What does it mean for an LLM to learn?](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#What-does-it-mean-for-an-LLM-to-learn)

[Self-supervised learning through text](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Self-supervised-learning-through-text)

[The training loop](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-training-loop)

[Prediction: Making a guess](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Prediction-Making-a-guess)

[The loss function: Knowing when the model is wrong](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#The-loss-function-Knowing-when-the-model-is-wrong)

[A simplified numerical intuition](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#A-simplified-numerical-intuition)

[Backpropagation](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Backpropagation)

[Weight updates: Where learning actually happens](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Weight-updates-Where-learning-actually-happens)

[Why scale matters](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Why-scale-matters)

[Training vs. inference](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Training-vs-inference)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/how-llms-learn-the-training-loop#Conclusion)