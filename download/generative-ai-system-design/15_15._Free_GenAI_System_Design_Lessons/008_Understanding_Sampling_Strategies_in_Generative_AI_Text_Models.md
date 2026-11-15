# Understanding_Sampling_Strategies_in_Generative_AI_Text_Models

Source: https://www.educative.io/courses/generative-ai-system-design/sampling-strategies

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Sampling Strategies

Learn how language models generate text by selecting tokens from probability distributions using different sampling strategies. Understand greedy decoding, beam search, top-k sampling, and nucleus (top-p) sampling. This lesson helps you grasp how these methods balance determinism, diversity, coherence, and creativity in generative AI outputs for various tasks.

We'll cover the following...

- [Greedy decoding](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Greedy-decoding)
  - [Why greedy decoding is not enough](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Why-greedy-decoding-is-not-enough)
- [Controlled randomness](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Controlled-randomness)
- [Beam search](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Beam-search)
  - [The core idea behind beam search](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#The-core-idea-behind-beam-search)
  - [How it works](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#How-it-works)
    - [Next step: Expanding the beam](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Next-step-Expanding-the-beam)
  - [Why beam search feels more “confident”](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Why-beam-search-feels-more-confident)
  - [When to use beam search](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#When-to-use-beam-search)
  - [Limitations of beam search](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Limitations-of-beam-search)
- [Top-k sampling](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Top-k-sampling)
  - [The core idea behind top-k sampling](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#The-core-idea-behind-top-k-sampling)
  - [How it works](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#How-it-works-1)
    - [Case 1: k = 1](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Case-1-k--1)
    - [Case 2: k = 2](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Case-2-k--2)
    - [Case 3: k = 4](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Case-3-k--4)
  - [Why top-k works well for open-ended generation](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Why-top-k-works-well-for-open-ended-generation)
- [Nucleus (Top-p) sampling](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Nucleus-Top-p-sampling)
  - [The core idea behind top-p sampling](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#The-core-idea-behind-top-p-sampling)
  - [How it works](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#How-it-works-2)
  - [Case 1: p = 0.75](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Case-1-p--075)
    - [Case 2: p = 0.90](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Case-2-p--090)
  - [Why top-p is adaptive](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Why-top-p-is-adaptive)
  - [When to use nucleus sampling](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#When-to-use-nucleus-sampling)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/sampling-strategies#Conclusion)

When a language model generates text, it does not directly produce a single next word. Instead, at each step, it outputs a *probability distribution* over all tokens in its vocabulary. This distribution reflects how likely the model believes each token is, given the text generated so far.

For example, consider the prompt:

> “The capital of France is”

After processing this prompt, the model might produce a probability distribution like the following:

Probability distribution of tokens

The model has not committed to a single answer. It has expressed uncertainty by assigning probabilities to multiple possibilities. The question is: *how do we turn this distribution into an actual token choice?*

This decision is handled by the **sampling strategy**.

## Greedy decoding

The most straightforward approach is **greedy decoding**. At each step, the model selects the token with the highest probability.

In the example above, greedy decoding would always select: “Paris.”

Greedy decoding is deterministic. Given the same prompt and model, it will always produce the same output. While this can be useful for debugging or tasks where variability is undesirable, it has important limitations.

### Why greedy decoding is not enough

Greedy decoding works well for short, factual completions, but it often performs poorly for longer or more open-ended generation.

Consider a storytelling prompt:

> “Once upon a time, there was a brave knight who”

At each step, the most probable token is often a common, safe continuation. Over many steps, this leads to outputs that are repetitive, generic, or overly cautious. The model tends to follow high-probability paths that quickly converge on predictable phrasing.

For example, greedy decoding may repeatedly favor tokens like:

- “was”
- “had”
- “the”

This can result in text that feels dull or stuck in loops.

## Controlled randomness

Sampling strategies address this issue by introducing **controlled randomness** into the selection of tokens. Instead of always choosing the most probable token, the model is allowed to sample from the distribution in a structured way.

Returning to the earlier example:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| Paris | 0.72 |
| Lyon | 0.12 |
| Marseille | 0.07 |
| London | 0.03 |

A sampling-based approach might still choose “Paris” most of the time, but it allows lower-probability tokens like “Lyon” or “Marseille” to be selected occasionally. This variability becomes especially important when generating longer sequences, where early choices strongly influence later ones.

All sampling strategies navigate the same fundamental trade-off:

- Determinism vs. diversity
- Coherence vs. creativity
- Safety vs. exploration

Different strategies resolve this trade-off in different ways. Some prioritize the most likely sequences, while others deliberately allow for variation. In the following sections, we will examine three commonly used approaches, beam search, top-k sampling, and nucleus (top-p) sampling, and see how each one makes this decision differently.

## Beam search

Beam search is a decoding strategy that produces more reliable, coherent outputs by simultaneously exploring multiple possible continuations. Instead of committing to a single token choice at each step, beam search keeps track of several promising partial sequences and expands them in parallel.

The key idea is simple: *do not put all your probability mass on a single path too early.*

### The core idea behind beam search

Beam search maintains a fixed number of candidate sequences, called the **beam width**, usually denoted as **BBB**.

At each generation step:

1. Every sequence in the beam is expanded by one token.
2. All expanded sequences are scored using their cumulative probability.
3. Only the top B sequences are kept.
4. The rest are discarded.

This process repeats until a stopping condition is reached.

### How it works

Consider the prompt:

> “The capital of France is”

Assume the model produces the following probabilities for the next token:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| Paris | 0.7 |
| Lyon | 0.2 |
| Marseille | 0.1 |

With `beam width = 2`, we keep the two most likely continuations:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| Paris | 0.7 |
| Lyon | 0.2 |

#### Next step: Expanding the beam

Now each of these partial sequences is expanded. For “Paris”, the next-token probabilities might be:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| . | 0.6 |
| city | 0.3 |
| and | 0.1 |

For “Lyon”, the next-token probabilities might be:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| . | 0.5 |
| is | 0.3 |
| and | 0.2 |

We now compute cumulative probabilities:

- “Paris .”: 0.7×0.6=0.420.7 \times 0.6 = 0.420.7×0.6=0.42
- “Paris city”: 0.7×0.3=0.210.7 \times 0.3 = 0.210.7×0.3=0.21
- “Lyon .”: 0.2×0.5=0.100.2 \times 0.5 = 0.100.2×0.5=0.10
- “Lyon is”:0.2×0.3=0.060.2 \times 0.3 = 0.060.2×0.3=0.06

We keep the top two sequences:

1. “Paris .” (0.42)
2. “Paris city” (0.21)

The “Lyon” path is dropped, even though it initially looked promising.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27701%27%20height=%27574%27/%3e)![The beam search process](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The beam search process")

The beam search process

### Why beam search feels more “confident”

Beam search tends to produce outputs that are:

- Grammatically clean
- Consistent
- Have low-variance across runs

This makes it useful for tasks where correctness and structure matter more than creativity, such as:

- Machine translation
- Summarization
- Structured generation

By evaluating entire sequences instead of individual token choices, beam search avoids some of the early mistakes greedy decoding can make.

### When to use beam search

Beam search is best suited for:

- Deterministic tasks.
- Short to medium-length outputs.
- Cases where correctness is more important than diversity.

For creative or conversational generation, sampling-based methods usually perform better.

### Limitations of beam search

Despite its strengths, beam search has important drawbacks.

First, it often produces overly safe or generic outputs. Because it aggressively favors high-probability paths, it tends to converge on common phrasing.

Second, it is computationally expensive. Expanding and scoring multiple sequences at each step increases both memory usage and latency.

Finally, beam search can amplify repetition. High-probability loops may dominate the beam, leading to repetitive phrases unless additional constraints are applied.

## Top-*k* sampling

Top-k sampling is a decoding strategy that introduces controlled randomness into text generation. Instead of always choosing the most probable token (as in greedy decoding) or tracking multiple full sequences (as in beam search), top-k sampling limits the model’s choices to a small set of likely tokens and then samples from that set.

This allows the model to produce more diverse and natural outputs while still avoiding extremely unlikely tokens.

### The core idea behind top-*k* sampling

At each generation step:

1. The model produces a probability distribution over all tokens.
2. Only the top k tokens with the highest probabilities are kept.
3. All other tokens are discarded.
4. The remaining probabilities are renormalized.
5. One token is sampled at random from this reduced set.

The value of k controls the model’s degree of freedom.

### How it works

Consider the same prompt:

> “The capital of France is”

Assume the model outputs the following probabilities:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| Paris | 0.72 |
| Lyon | 0.12 |
| Marseille | 0.07 |
| London | 0.03 |
| other tokens | 0.06 |

#### Case 1: *k* = 1

Only the top token is kept:

- Paris (1.0)

The output is always “Paris.” There is no randomness.

#### Case 2: *k* = 2

We keep the two most probable tokens:

- Paris (0.72)
- Lyon (0.12)

We sum up their probabilities for normalization: 0.72 + 0.12 = 0.84

After renormalization:

- Paris → 0.720.84≈0.86\frac{0.72}{0.84} \approx 0.860.840.72​≈0.86​
- Lyon → 0.120.84≈0.14\frac{0.12}{0.84} \approx 0.140.840.12​≈0.14

Now:

- “Paris” is chosen most of the time.
- “Lyon” is chosen occasionally.

This introduces diversity without allowing clearly incorrect options.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27701%27%20height=%27531%27/%3e)![The top-k selection process](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The top-k selection process")

The top-k selection process

#### Case 3: *k* = 4

We keep:

- Paris (0.72)
- Lyon (0.12)
- Marseille (0.07)
- London (0.03)

After renormalization, the model can occasionally select less likely tokens, increasing variability but also increasing the risk of incorrect or less relevant outputs.

A Small *k* value means safer outputs, less diversity, and is closer to greedy decoding.  A larger *k* value means more creative outputs and greater variability, but a higher risk of incoherence. Choosing *k* is therefore a tuning decision that depends on the task.

### Why top-*k* works well for open-ended generation

Top-*k* sampling avoids two extremes. It does not collapse into a single deterministic path, like greedy decoding. But it also does not exhaustively explore entire sequences, as beam search does.

Instead, it allows randomness only among plausible options. This makes it a good fit for storytelling, conversational agents, and creative writing, among other tasks.

However, top-*k* has one important limitation: the value of *k* is fixed. A single *k* may be too restrictive for some prompts and too permissive for others. This motivates a more adaptive strategy, which we will examine next.

## Nucleus (Top-*p*) sampling

**Nucleus sampling**, also known as top-*p* sampling, was introduced to address a key limitation of top-*k* sampling: the use of a fixed cutoff. In many cases, the number of reasonable next tokens varies depending on the prompt and the context. A single value of (*k*) cannot adapt to this variation.

Top-*p* sampling solves this by selecting tokens based on cumulative probability mass rather than a fixed count.

### The core idea behind top-*p* sampling

At each generation step:

1. The model outputs a probability distribution over tokens.
2. Tokens are sorted from most to least probable.
3. The smallest set of tokens whose total probability is at least (*p*) is selected.
4. All other tokens are discarded.
5. Probabilities are renormalized.
6. One token is sampled from this dynamic set.

The value of (*p*) controls how much probability mass is considered, rather than how many tokens.

### How it works

Consider the same probability distribution:

|  |  |
| --- | --- |
| **Token** | **Probability** |
| Paris | 0.72 |
| Lyon | 0.12 |
| Marseille | 0.07 |
| London | 0.03 |
| other tokens | 0.06 |

### Case 1: *p* = 0.75

We accumulate probabilities from the top:

- Paris → cumulative = 0.72
- Lyon → cumulative = 0.84

> **Note:** Since 0.72 is less than 0.75, so we continue to add probability of the next token to make it at least 0.75 (or higher).

The smallest set exceeding 0.75 is:

- Paris
- Lyon

Only these two tokens are kept and sampled from.

#### Case 2: *p* = 0.90

Accumulating again:

- Paris → 0.72
- Lyon → 0.84
- Marseille → 0.91

Now the candidate set is:

- Paris
- Lyon
- Marseille

The model has more freedom to explore, but still avoids very unlikely options.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27701%27%20height=%27731%27/%3e)![The top-p selection process](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The top-p selection process")

The top-p selection process

### Why top-*p* is adaptive

Unlike top-*k*, the size of the candidate set in top-*p* sampling is dynamic.

- When the model is confident (one token dominates the distribution), the nucleus is small.
- When the model is uncertain (many tokens have similar probabilities), the nucleus grows.

This adaptivity allows top-*p* sampling to balance coherence and creativity automatically, without manual tuning of a fixed (*k*).

Top-k limits *how many* tokens are considered, while top-*p* limits *how much probability mass* is considered. In practice, top-*p* often produces more natural text because it adjusts to the shape of the probability distribution rather than enforcing a rigid cutoff.

### When to use nucleus sampling

Top-*p* sampling is widely used for:

- Conversational agents
- Creative text generation
- Open-ended responses

It is often the default choice in modern language model deployments because it provides a good balance between determinism and diversity across a wide range of prompts.

## Conclusion

Language models do not generate a single fixed answer. At each step, they produce a probability distribution over possible next tokens. Sampling strategies determine how a token is chosen from this distribution, directly shaping the model’s behavior.

Beam search explores multiple high-probability sequences to produce more deterministic, structured outputs, but often at the expense of diversity. Top-*k* sampling introduces randomness by limiting choices to the *k* most likely tokens, enabling more varied generation while avoiding unlikely options. Nucleus (top-*p*) sampling further improves on this by selecting a dynamic set of tokens based on cumulative probability, adapting automatically to the model’s confidence.

Choosing a sampling strategy is a design decision. It controls the balance between coherence and creativity and should be selected based on the task, whether the goal is reliable generation or open-ended exploration.