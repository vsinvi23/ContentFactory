# System_Design_WhatsApp

Source: https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# System Design: WhatsApp

Explore the architectural challenges of designing WhatsApp, a globally scaled, secure messaging application handling 100 billion messages daily. Outline the structured System Design approach, requirements, high-level design, and detailed design, used to build reliable, low-latency communication services.

We'll cover the following...

- [WhatsApp](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#WhatsApp)
- [Design problem](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#Design-problem)
- [How will we design WhatsApp?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#How-will-we-design-WhatsApp)

## WhatsApp[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#WhatsApp)

**WhatsApp** is the most popular, simple, secure, and reliable messaging system that allows users to send text, voice, and multimedia messages.  
  
WhatsApp is a widely used messaging application used by billions of people worldwide. Many users rely on WhatsApp for daily communication. As of July 2021, the platform had about two billion active users worldwide. The average user spends about 19.4 hours per month on the app. In December 2020, the WhatsApp CEO tweeted that WhatsApp users share more than 100 billion messages per day, an increase of approximately 54% since 2018.

The increase in messages sent globally per day is depicted in the following chart:

The increase in messages communicated per day each year

## Design problem[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#Design-problem)

As system designers, we should be aware of user growth rates. There are many interesting questions about WhatsApp:

- How is this application designed?
- How does it work?
- What are the different types of components involved in it?
- How does WhatsApp enable billions of users to communicate with each other?
- How does WhatsApp keep all that data secure?

In this chapter, we’ll focus on the high-level and detailed design of the WhatsApp application to answer the above questions.

## How will we design WhatsApp?[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#How-will-we-design-WhatsApp)

We’ve divided the design of WhatsApp into the following five lessons:

1. [**Requirements**](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-whatsapps-design): Identify functional and non-functional requirements. We’ll also discuss the resource estimates required for the smooth and efficient operation of the proposed WhatsApp design.
2. [**High-level design**](https://www.educative.io/courses/grokking-the-system-design-interview/high-level-design-of-whatsapp)**:** Focus on the high-level design of our WhatsApp version. We’ll also discuss essential APIs for our WhatsApp design.
3. [**Detailed design**](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-whatsapp)**:** Describe the design of our WhatsApp messenger in detail. Initially, we’ll explain the design of each microservice, including connection with servers, sending and receiving messages and media content, and group messages. In the end, the design of each microservice is combined into the detailed design of WhatsApp.
4. [**Evaluation**](https://www.educative.io/courses/grokking-the-system-design-interview/evaluation-of-whatsapps-design)**:** Explain how our version of WhatsApp meets non-functional requirements. We’ll also evaluate some trade-offs of our design.
5. [**Quiz**](https://www.educative.io/courses/grokking-the-system-design-interview/quiz-on-whatsapps-design)**:** Assess what we’ve learned in this chapter through a quiz.

Let’s start by discussing the requirements of our version of WhatsApp.

System Design: Web Crawler

Requirements of WhatsApp’s Design

Ask

[WhatsApp](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#WhatsApp)

[Design problem](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#Design-problem)

[How will we design WhatsApp?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-whatsapp#How-will-we-design-WhatsApp)