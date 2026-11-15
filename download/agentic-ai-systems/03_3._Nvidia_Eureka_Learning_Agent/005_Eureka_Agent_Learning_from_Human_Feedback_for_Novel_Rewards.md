# Eureka_Agent_Learning_from_Human_Feedback_for_Novel_Rewards

Source: https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Eureka from Human Feedback and Novel Reward Discovery

Learn how Eureka, an advanced AI agent, enhances reinforcement learning by using human-initialized rewards and textual feedback to align with subtle human preferences. Understand its capability to discover novel reward functions that surpass human-engineered ones, demonstrating adaptability, creativity, and collaboration in agentic system design.

We'll cover the following...

- [Integrating human intelligence with agent autonomy](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Integrating-human-intelligence-with-agent-autonomy)
  - [Improving existing human rewards (human initialization)](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Improving-existing-human-rewards-human-initialization)
  - [Guiding with textual human feedback (human reward reflection)](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Guiding-with-textual-human-feedback-human-reward-reflection)
- [Novel reward discovery: Going beyond human intuition](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Novel-reward-discovery-Going-beyond-human-intuition)
- [Summary](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Summary)

In previous lessons, we’ve explored Eureka’s impressive ability to autonomously design and refine reward functions for complex reinforcement learning tasks. We saw its power in zero-shot generation, its evolutionary search as a self-improvement loop, and its reward reflection mechanism for targeted code refinement. These capabilities showcase Eureka as a highly goal-oriented, and self-improving agent.

However, in many real-world applications, relying solely on an automated fitness function (F) can have limitations. A numerical score, while objective, might not always capture the subtle, nuanced intent or preferences of a human user. For instance, an agent might learn to run incredibly fast, but a human supervisor might prioritize a “natural” or “stable” gait, even if it’s slightly slower. Also, for truly open-ended tasks, a clear, quantifiable fitness function might not even exist at the outset.

![The alignment gap between an agent’s optimized goal (e.g., fastest movement) and a human’s nuanced preference (e.g., stable gait) illustrates the challenge Eureka addresses with human feedback](005_Eureka_Agent_Learning_from_Human_Feedback_for_Novel_Rewards_images/img_319dabf934fe.svg "The alignment gap between an agent’s optimized goal (e.g., fastest movement) and a human’s nuanced preference (e.g., stable gait) illustrates the challenge Eureka addresses with human feedback")

The alignment gap between an agent’s optimized goal (e.g., fastest movement) and a human’s nuanced preference (e.g., stable gait) illustrates the challenge Eureka addresses with human feedback

This gap between what an autonomous AI system optimizes for, and what humans truly desire is a critical challenge in agent alignment. Eureka offers a sophisticated solution by enabling a new, gradient-free in-context learning approach to reinforcement learning from human feedback (RLHF).

## Integrating human intelligence with agent autonomy[#](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Integrating-human-intelligence-with-agent-autonomy)

While Eureka demonstrates impressive autonomous capabilities, real-world applications often benefit immensely from human input. This section explores how Eureka bridges the gap between AI autonomy, and human values by fluidly incorporating various types of human feedback. This directly connects to our earlier discussions on human oversight (including human-in-the-loop and human-on-the-loop paradigms), and alignment as essential components of trustworthy agentic system design.

Eureka integrates human intelligence in two primary ways:

### Improving existing human rewards (human initialization)[#](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Improving-existing-human-rewards-human-initialization)

It’s very common in practical RL applications that human experts have already tried to create a reward function. While these human-engineered rewards might provide a decent starting point, they are often not perfect or fully optimized. This presents an opportunity: can an AI agent take a human’s best effort and make it even better?

Eureka can be initialized directly with such a human-written reward function. This means the human’s reward code is simply given to Eureka as if it were the output of Eureka’s very first iteration. Crucially, no special code changes or complex re-configurations are needed for Eureka’s core logic. It then proceeds with its regular evolutionary search and reward reflection mechanisms, treating the human-provided reward as its initial “best candidate.”

![Eureka’s human reward initialization process, where the agent takes a human-designed reward as a starting point for its own iterative refinement](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Eureka’s human reward initialization process, where the agent takes a human-designed reward as a starting point for its own iterative refinement")

Eureka’s human reward initialization process, where the agent takes a human-designed reward as a starting point for its own iterative refinement

Testing showed that Eureka, when initialized with a human-designed reward, consistently outperforms both the original version of Eureka (which starts from scratch) and the standalone human-engineered reward. This outcome provides a key insight for agentic system design:

Human designers are generally very good at identifying the relevant state variables that should be included in a reward function (this often relies on common sense and domain understanding). However, humans are often less skilled at precisely determining how to mathematically combine and weigh those variables to create an optimal reward function that the RL algorithm can efficiently learn from.

Eureka acts as a powerful “reward assistant” that perfectly complements human knowledge, taking the relevant variables identified by humans and expertly shaping them into effective reward code. This exemplifies a highly effective human-in-the-loop (HITL) pattern for agent bootstrapping and refinement, as human expertise provides the initial starting point for the agent’s iterative optimization.

### Guiding with textual human feedback (human reward reflection)[#](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Guiding-with-textual-human-feedback-human-reward-reflection)

As discussed earlier, sometimes an explicit, quantifiable fitness function (F) simply isn’t available, or it fails to capture subtle human preferences. For example, when training a robot to walk, humans might want a “natural-looking” or “stable” walk, not just the fastest one. These qualities are hard to put into a numerical formula.

To cope with this, a human supervisor steps in to provide direct textual feedback that replaces Eureka’s automated reward reflection. Instead of Eureka’s LLM analyzing training statistics, it receives natural language instructions from a human, describing observed agent behaviors and suggesting desired changes. For instance, a human might tell the agent: “The robot is doing a ‘squat jump’ when it should be ‘running forward,’” or “The torso is too low, encourage upright running.”

This approach allows Eureka to co-pilot reward function designs that precisely capture subtle human preferences and nuances. The humanoid agent example in the paper is a strong case: human textual feedback iteratively helped the agent evolve from an initial “squat jump” into a “forward running” gait, and eventually into a “safer and more stable gait.”

In a user study, the Eureka-HF (human feedback) agent was preferred by a large majority of users (15 out of 20), clearly demonstrating its success in trading speed for stability based on human input. This highlights Eureka’s remarkable adaptability to human values ,and its ability to learn from highly qualitative feedback. This is visualized below, which shows the evolution of learned behaviors after each human feedback.

![Evolution of an agent’s learned behavior over iterations, guided by human textual feedback, demonstrates Eureka’s human-on-the-loop (HOTL) alignment capability](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Evolution of an agent’s learned behavior over iterations, guided by human textual feedback, demonstrates Eureka’s human-on-the-loop (HOTL) alignment capability")

Evolution of an agent’s learned behavior over iterations, guided by human textual feedback, demonstrates Eureka’s human-on-the-loop (HOTL) alignment capability

This process exemplifies a crucial human-on-the-loop (HOTL) pattern for continuous agent refinement and alignment in complex, subjective tasks, as humans provide real-time, iterative guidance.

## Novel reward discovery: Going beyond human intuition[#](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Novel-reward-discovery-Going-beyond-human-intuition)

In the previous sections, we’ve seen how Eureka can be guided by human input, either by building upon existing rewards or by iteratively incorporating textual feedback. But what happens when an agent’s exploration goes beyond merely optimizing human-provided starting points, or aligning with explicit human instructions? This section explores Eureka’s remarkable capacity for novel reward discovery, demonstrating how it can diverge from human intuition entirely to find truly innovative solutions.

This is a powerful feature of an autonomous agent: it can find reward design principles that human experts might not think of, or that even go against established human intuition.

![Eureka’s capacity for novel reward discovery allows it to explore solution spaces beyond conventional human intuition to find optimal, sometimes counter-intuitive, paths](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Eureka’s capacity for novel reward discovery allows it to explore solution spaces beyond conventional human intuition to find optimal, sometimes counter-intuitive, paths")

Eureka’s capacity for novel reward discovery allows it to explore solution spaces beyond conventional human intuition to find optimal, sometimes counter-intuitive, paths

Eureka’s generated reward functions are often “weakly correlated” with, or even negatively correlated with human-engineered rewards. Despite these differences, Eureka’s rewards still consistently outperform the human versions. Many Eureka-generated rewards that led to superior performance had low, or even negative correlation with their human counterparts, indicating truly different strategies.

The Eureka paper suggests that: for “harder tasks,” human rewards are less likely to be optimal, leaving more room for Eureka to discover these unique and effective approaches.

This capability is crucial because it highlights the potential of an autonomous agent to explore a much broader solution space than human experts might consider. Human designers often have inherent biases or stick to conventional approaches. Eureka, unconstrained by such biases, can discover genuinely innovative and sometimes counter-intuitive solutions that lead to breakthroughs in performance. This showcases the agent’s capacity for creativity and finding unforeseen solutions, pushing the boundaries of what’s possible in goal-oriented behavior and complex problem-solving.

## Summary[#](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Summary)

In this lesson, we’ve seen how this powerful learning agent extends its capabilities beyond pure autonomous reward design to effectively incorporate and benefit from invaluable human feedback. Eureka’s ability to seamlessly integrate human reward initialization, and learn from textual human feedback for reward reflection demonstrates its versatility in aligning AI behavior with nuanced human intent. Moreover, its capacity for novel reward discovery highlights the profound potential of AI agents to go beyond human intuition, finding innovative and highly effective solutions in complex design spaces. Eureka stands as a prime example of building adaptive, trustworthy, and high-performing agentic systems that can effectively collaborate with, and even surpass human capabilities in specialized domains. It truly embodies the principles of continuous learning and sophisticated human-AI interaction that we strive for in agentic system design.

We’ve explored Eureka’s sophisticated mechanisms for reward design, self-improvement, and human interaction. But how do we quantitatively assess its overall success, and compare it against other methods? In our next and final lesson for this chapter, we will delve into examining the key metrics, and empirical results that demonstrate its human-level performance.

Eureka's Reward Reflection Mechanism

Evaluating Eureka: Performance and Insights

Ask

[Integrating human intelligence with agent autonomy](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Integrating-human-intelligence-with-agent-autonomy)

[Improving existing human rewards (human initialization)](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Improving-existing-human-rewards-human-initialization)

[Guiding with textual human feedback (human reward reflection)](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Guiding-with-textual-human-feedback-human-reward-reflection)

[Novel reward discovery: Going beyond human intuition](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Novel-reward-discovery-Going-beyond-human-intuition)

[Summary](https://www.educative.io/courses/agentic-ai-systems/eureka-from-human-feedback-and-novel-reward-discovery#Summary)