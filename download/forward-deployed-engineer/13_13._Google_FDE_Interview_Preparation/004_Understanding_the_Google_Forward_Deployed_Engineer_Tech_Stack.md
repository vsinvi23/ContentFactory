# Understanding_the_Google_Forward_Deployed_Engineer_Tech_Stack

Source: https://www.educative.io/courses/forward-deployed-engineer/the-google-fde-tech-stack

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Google FDE Tech Stack

Explore the Google Cloud stack as a set of layers, from Gemini models and the Agent Platform to data, runtime, security, and evaluation. Learn which layers matter most for each FDE track and how to connect product choices to customer constraints in interviews.

We'll cover the following...

- [A layered view of the stack](https://www.educative.io/courses/forward-deployed-engineer/the-google-fde-tech-stack#A-layered-view-of-the-stack)
- [What each layer means in practice](https://www.educative.io/courses/forward-deployed-engineer/the-google-fde-tech-stack#What-each-layer-means-in-practice)
- [Which layers matter most for each track](https://www.educative.io/courses/forward-deployed-engineer/the-google-fde-tech-stack#Which-layers-matter-most-for-each-track)
- [How interviewers use the stack](https://www.educative.io/courses/forward-deployed-engineer/the-google-fde-tech-stack#How-interviewers-use-the-stack)

Google Cloud offers hundreds of products, and an FDE candidate cannot study all of them in depth. Interviewers do not expect that. They expect a clear mental map of how the pieces fit together when an enterprise AI system goes into production, along with deeper knowledge of the layers the role uses most. A candidate who can explain where each product sits and why it was chosen sends a stronger signal than one who can list product names without context.

Google reorganized much of this stack in April 2026 when it introduced Gemini Enterprise Agent Platform, which Google describes as the evolution of Vertex AI. Model access, agent building, runtime, governance, and evaluation now sit under one platform, and new Vertex AI capabilities ship through it. Interviewers and customers may use the older Vertex AI names and the new platform names interchangeably, so a working map needs to account for both.

The sections below present the stack as a set of layers, explain what each layer does in a customer deployment, and then show which layers matter most for each FDE track.

Product names on Google Cloud change often. In interviews, explaining what a layer does and why it fits the customer’s constraints matters more than using the latest product name. When a customer uses an older name, such as Vertex AI, it is fine to use their term.

## A layered view of the stack

A useful way to organize the stack is to follow a single request through a production agent system. A ...

Ask