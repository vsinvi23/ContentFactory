# Design_Interview_Guide_Low-level_OOD_to_Advanced_System_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design Interview Guide: Low-level OOD to Advanced System Design

Design interviews in the tech industry can be categorized into Low-Level Object-Oriented Design (OOD) and Advanced System Design (ASD). Low-Level OOD focuses on the implementation details of specific components, requiring knowledge of design patterns and object relationships. In contrast, ASD emphasizes the overall architecture of complex systems, demanding a deep understanding of distributed systems and their scalability, performance, and fault tolerance. Preparing for both types is crucial, as the interview style often depends on the role and company, with ASD typically aimed at senior positions. Leveraging past designs and patterns is essential for success in ASD interviews.

We'll cover the following...

- [Low-level OOD vs. ASD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-vs-ASD)
- [Quick differences: ASD vs. Low-level OOD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Quick-differences-ASD-vs-Low-level-OOD)
  - [Advanced System Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design)
  - [Low-level OOD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD)
- [Who needs to know ASD vs. OOD?](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Who-needs-to-know-ASD-vs-OOD)
  - [Advanced System Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-1)
  - [Low-level object-oriented design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-object-oriented-design)
- [Low-level OOD: Leverage design patterns to build components](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-Leverage-design-patterns-to-build-components)
- [Advanced System Design: Build on past designs](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-Build-on-past-designs)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Conclusion)

Let’s begin by visualizing the challenge of designing an intricate distributed relational database system such as Google Cloud Spanner. Now consider doing this while under pressure from an interviewer. What if we were asked to design a specific module or component within that architecture, like a load balancer or cache?

These scenarios are possible during one portion of the modern technical interview loop: the design interview. We can use these interviews to send hireable signals and stand out in a competitive field, but they can be challenging to prepare for if we don’t know the format.

Understanding the different types of design interviews, whether they focus on low-level implementation details or more advanced System Design concepts, can give us the best chance of providing an answer that gets us hired.

Unlike coding interviews, technical design interviews require thinking in broader, systemic terms. For these interviews, we must learn to weigh different tradeoffs between possible solutions and then provide justifications for the solutions we choose.

However, as mentioned earlier, the types of design interviews available can vary, and each will have its own set of expectations and standards for what constitutes an ideal or complete solution. The type of design interview we perform will depend mostly on the size of the company, the role we’re applying for, and our current experience level. Later, we’ll clarify which particular roles and companies are most likely to conduct specific types of interviews.

In this lesson, we’ll discuss two types of design interviews that exist at opposite ends of the spectrum: Low-Level Object-Oriented Design (OOD) and Advanced System Design (ASD). We’ll cover what interviewers are looking for in OOD and ASD interviews and key differences between the types, to help us prepare for the right one.

## Low-level OOD vs. ASD[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-vs-ASD)

System Design interviews have been a part of the technical interviewing process for a relatively shorter period than low-level design interviews. In the software industry, it was always important for engineers to demonstrate the ability to design efficient and effective software at a granular level. System Design only caught on once real-world distributed systems became more commonplace in the 2010s.

The greater complexity of these systems meant we needed highly scalable and reliable architectures and, consequently, people who could design them. Now, System Design is a cornerstone of modern software development.

At the same time, the Low-Level OOD interview remains one of the most common types of design interviews we encounter during tech interviews. Coming into these interviews with a solid grasp of object-oriented design patterns puts us at a massive advantage.

> “All well-structured object-oriented architectures are full of patterns.” — Grady BoochChief Scientist, Rational Software Corporation

Here, the focus is on the implementation details of a specific module or component within a more extensive system. More specifically, it’s focused on the details of individual classes and objects within that software system and their relationships, methods, and properties. Our interviewers are going to determine how well we can design an efficient implementation that satisfies all of the functional requirements.

System Design interviews, on the other hand, take a broader look at the big picture. Here, our concerns are with an entire system’s overall architecture and design. Our interviewers expect us to develop a robust, high-level architecture that meets functional and non-functional requirements alike. We may need to consider properties like scalability, availability, and security in our decision-making process.

ASD interviews test our understanding of the principles of System Design through a more rigorous lens. These interviews often hold our solutions to far more exacting standards, as the interviewers will expect us to use more sophisticated techniques and methodologies that are often seen in enterprise-level applications. At this level, our designs must provide elegant, efficient solutions that reflect practical experience with real-world System design and implementation. While non-functional requirements like scalability are important to consider in System Design, they often become essential in ASD, being treated as existing properties of a complex, large-scale system to be optimized and improved.

Returning to Google Cloud Spanner, this system represents the type of case study that could turn up in an Advanced System Design interview. It is a globally distributed relational database that provides strong consistency, high availability, and horizontal scalability, making it a useful example for discussing complex distributed system trade-offs .

At the same time, Spanner could also be used effectively within low-level design interviews to assess our understanding of the underlying architecture of a distributed system and how more specific components like databases and caches might interact.

![](013_Design_Interview_Guide_Low-level_OOD_to_Advanced_System_Design_images/img_f686236e0dd5.svg)

## Quick differences: ASD vs. Low-level OOD[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Quick-differences-ASD-vs-Low-level-OOD)

To review, here are some major differences between the interviews to remember.

### Advanced System Design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design)

- Focuses on the overall architecture of a system.
- Concerned with designing a scalable, performant, and fault-tolerant system.
- Requires a deep understanding of distributed systems and System Design principles.
- Encompasses large-scale, complex systems with many components and stakeholders involved.

### Low-level OOD[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD)

- Focuses on designing individual classes, objects, and their relationships.
- Deals with solving problems related to implementation and programming.
- Requires a deep understanding of object-oriented programming concepts and design principles.
- It is applied to components within larger systems.

Now that we’ve covered the key differences, let’s look at how to determine the style of design interview one should expect.

## Who needs to know ASD vs. OOD?[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Who-needs-to-know-ASD-vs-OOD)

The style of design interview we receive depends on several factors. Here is a quick overview of when we might encounter each type.

### Advanced System Design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-1)

- More frequently used when interviewing for senior software engineering and engineering leadership roles.
- Interviewers expect candidates to be familiar with major examples of both modern and historical distributed systems.
- We are expected to understand how to select and combine the building blocks of a modern system’s architecture.
- Discussions typically focus on system architecture and high-level aspects such as scalability, performance, and fault tolerance.

### Low-level object-oriented design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-object-oriented-design)

- More dependent on the role and company we’re applying for. For example, the mobile application team at Spotify would focus on OOD questions because they want to know how well we can optimize single processes.
- Interview questions focus on creating classes and objects, as well as defining their attributes and behavior at the component level. We can expect to encounter coding exercises and algorithmic questions at this level.

Unless we’re set on a particular role, preparing for both extremes of the design interview is the wisest course of action. Now, let’s look more closely at each type of interview and our best advice for succeeding in them.

## Low-level OOD: Leverage design patterns to build components[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-Leverage-design-patterns-to-build-components)

Now, we will start with the lowest level of the design interview, the Low-Level OOD interview. As defined earlier, OOD involves implementing specific modules or components and their classes within a more extensive system, such as Google’s Chrome browser.

In earlier software engineer interviews, Low-Level OOD interviews were the only type of design interview typically encountered. System Design and scalable systems were not as integral as they are today because large-scale distributed systems were relatively uncommon.

We can think of OOD similarly to building a Formula 1 race car. If the entire car is a distributed system, then the engine’s design would be considered a low-level process within that system.

The OOD interview will primarily measure two things:

- Can we design a component that successfully interacts with other components in the system?
- Can we use design patterns to create this component efficiently?

Understanding the various design patterns of OOD should be a primary focus of our preparation for the low-level design interview.

*“Design Patterns: Elements of Reusable Object-Oriented Software”* (1994) by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, collectively known as the “Gang of Four,” is considered a seminal work in the field of object-oriented design. It was instrumental in popularizing the use of design patterns at a time when object-oriented design was reaching new heights of popularity.

This book highlighted 23 fundamental design patterns of OOD, organized into three categories: creational, structural, and behavioral patterns.

- **Creational patterns** deal with the process of object creation and are used to abstract the process of object creation.
- **Structural patterns** deal with class and object composition. These patterns provide ways to organize or combine classes and objects to form larger structures.
- **Behavioral patterns** focus more on object interaction and how objects communicate with each other. These patterns deal with how responsibilities are delegated across different objects.

Each category represents a set of design patterns meant to solve a specific type of object-oriented design problem. By using these patterns, developers can significantly improve our software’s coherence, modularity, and maintainability.

Of the 23 design patterns, these are the most frequently used in technical design interviews:

- **Singleton:** Restricts the instantiation of a class to a single object.
- **Factory:** Doesn’t require the use of a constructor to create objects (aka, the new keyword).
- **Constructor:** Uses the constructors present in the class to create specific types of objects.
- **Iterator:** Iterates a collection of objects without exposing the underlying form.
- **Facade:** Simplifies a client’s interaction with the system by hiding the underlying complex code.
- **Adaptor:** Allows an object to cooperate with a class that has an incompatible interface.
- **Visitor:** Allows new operations to the objects without changing the structure of the objects themselves.

Ultimately, the best pattern to use depends on the question asked. For example, if a desktop application generates IDs from shared state, the application may need one shared generator instance, especially when multiple threads request IDs concurrently. The Singleton pattern is extremely relevant here as it ensures that each process in the software will have only one instance of our class.

OOD is the oldest among the stages of tech design interviews, but it is not going away anytime soon. System Design can only be effective when individual processes are also optimized. Nobody will use a web app if their web browser software provides a bad user experience. Scalability only matters if customers want to stick around in the first place.

![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)

## Advanced System Design: Build on past designs[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-Build-on-past-designs)

Studying past distributed systems and their design patterns helps engineers identify strategies for building resilient, long-lived systems. It is a practice all engineers should invest time in because many high-level distributed systems, like Amazon’s DynamoDB, are modeled on past systems. In turn, these systems tend to influence the design of future distributed systems.

In this way, we can understand the heart of modern distributed systems by studying the strengths and limitations of older systems. Advanced System Design interview questions require a deep understanding of distributed systems, particularly their history and evolution.

Being advanced in System Design does not mean we are expected to start completely from scratch with every design. It means using existing structures to draft a suitable system design while evaluating their trade-offs against the final requirements. Analyzing successful strategies and designs used in older distributed systems for later use is also known as pattern sharing.

An excellent example of pattern-sharing in the real world can be found in Amazon DynamoDB. In 2004, Amazon published *“*The Dynamo Paper,*”* which documented the creation of its in-house database. This led to the development of DynamoDB a few years later. DynamoDB would go on to significantly influence the overall design of Apache Cassandra.

In 2008, Facebook released Apache Cassandra, a database that aimed to replicate Dynamo’s distributed storage and replication techniques while integrating the ability to handle large analytical and operational workloads like Google’s Bigtable database. In fact, Avinash Lakshman, one of the lead developers on the Cassandra project, was also one of the authors of *“*The Dynamo Paper.*”*

It is reasonable to assume he did not start completely from scratch on Cassandra.

The main lesson is to use prior experience and established design patterns to build better solutions. Lakshman’s experience working on DynamoDB allowed him to incorporate proven techniques to improve and expand an existing design. We need to practice this general approach as we prepare to solve various problems in the System Design interview.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Conclusion)

Low-level OOD and ASD cover different parts of the design interview spectrum, from detailed implementation to high-level architecture. Understanding these differences and preparing for both types ensures a stronger foundation for all design interview challenges.

Does Google Ask System Design Interview Questions for L4?

System Design Interview PDF

Ask

[Low-level OOD vs. ASD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-vs-ASD)

[Quick differences: ASD vs. Low-level OOD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Quick-differences-ASD-vs-Low-level-OOD)

[Advanced System Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design)

[Low-level OOD](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD)

[Who needs to know ASD vs. OOD?](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Who-needs-to-know-ASD-vs-OOD)

[Advanced System Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-1)

[Low-level object-oriented design](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-object-oriented-design)

[Low-level OOD: Leverage design patterns to build components](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Low-level-OOD-Leverage-design-patterns-to-build-components)

[Advanced System Design: Build on past designs](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Advanced-System-Design-Build-on-past-designs)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/design-interview-guide-low-level-ood-to-advanced-system-design#Conclusion)