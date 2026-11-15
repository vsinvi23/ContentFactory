# Problem_Statement_and_Metrics_for_Personalized_Feed_Ranking

Source: https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Machine Learning System Design](https://www.educative.io/courses/machine-learning-system-design)

# Problem Statement and Metrics

Explore how to formulate the problem statement and design key metrics for personalized feed ranking, focusing on maximizing user engagement. Understand offline and online metrics such as Click Through Rate and Normalized Cross-Entropy. Discover requirements for training, personalization, data freshness, scalability, and latency in large-scale ranking systems.

We'll cover the following...

- [LinkedIn feed ranking](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#LinkedIn-feed-ranking)
- [1. Problem statement](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#1-Problem-statement)
- [2. Metrics design and requirements](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#2-Metrics-design-and-requirements)
  - [Metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Metrics)
    - [Offline metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Offline-metrics)
    - [Online metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Online-metrics)
  - [Requirements](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Requirements)
    - [Training](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Training)
    - [Inference](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Inference)
  - [Summary](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Summary)

## LinkedIn feed ranking[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#LinkedIn-feed-ranking)

## 1. Problem statement[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#1-Problem-statement)

Design a personalized LinkedIn feed to maximize long-term user engagement. One way to measure engagement is user frequency, i.e, measure the number of engagements per user, but it’s very difficult in practice. Another way is to measure the click probability or **Click Through Rate** (CTR).

![LinkedIn feed ranking](001_Problem_Statement_and_Metrics_for_Personalized_Feed_Ranking_images/img_d4f30568fd94.svg "LinkedIn feed ranking")

LinkedIn feed ranking

On the LinkedIn feed, there are five major activity types:

- Connections (A connects with B)
- Informational
- Profile
- Opinion
- Site-specific
- Intuitively different activities have very different CTR. This is important when we decide to build models and generate training data.

| **Category** | **Example** |
| --- | --- |
| Connection | Member connector follows member/company, member joins group |
| Informational | Member or company shares article/picture/message |
| Profile | Member updates profile, i.e., picture, job-change, etc. |
| Opinion | Member likes or comments on articles, pictures, job-changes, etc. |
| Site-Specific | Member endorses member, etc. |

## 2. Metrics design and requirements[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#2-Metrics-design-and-requirements)

### Metrics[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Metrics)

#### Offline metrics[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Offline-metrics)

- The Click Through Rate (CTR) for one specific feed is the number of clicks that feed receives, divided by the number of times the feed is shown.

CTR=number\_of\_clicksnumber\_of\_shown\_timesCTR = \frac{number\\_of\\_clicks}{number\\_of\\_shown\\_times}CTR=number\_of\_shown\_timesnumber\_of\_clicks​

- Maximizing CTR can be formalized as training a supervised binary classification model. For offline metrics, we normalize cross-entropy and AUC.
- Normalizing cross-entropy (NCE) helps the model be less sensitive to background CTR.

NCE=−1N∑i=1n(1+yi2log(pi))+1−yi2log(1−pi))−(p∗log(p)+(1−p)∗log(1−p))NCE = \frac{-\frac{1}{N} \sum\_{i=1}^n (\frac{1+y\_i}{2} log(p\_i)) + \frac{1-y\_i}{2}log(1-p\_i))} {-(p\*log(p) +(1-p)\*log(1-p))}NCE=−(p∗log(p)+(1−p)∗log(1−p))−N1​∑i=1n​(21+yi​​log(pi​))+21−yi​​log(1−pi​))​

#### Online metrics[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Online-metrics)

- For non-stationary data, offline metrics are not usually a good indicator of performance. Online metrics need to reflect the level of engagement from users once the model has deployed, i.e., **Conversion rate** (ratio of clicks with number of feeds).

### Requirements[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Requirements)

#### Training[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Training)

- We need to handle large volumes of data during training. Ideally, the models are trained in distributed settings. In social network settings, it’s common to have online data distribution shift from offline training data distribution. One way to address this issue is to retrain the models (incrementally) multiple times per day.
- Personalization: Support is needed for a high level of personalization since different users have different tastes and styles for consuming their feed.
- Data freshness: Avoid showing repetitive feed on the user’s home feed.

#### Inference[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Inference)

- Scalability: The volume of users’ activities are large and the LinkedIn system needs to handle 300 million users.
- Latency: When a user goes to LinkedIn, there are multiple pipelines and services that will pull data from multiple sources before feeding activities into the ranking model. All of these steps need to be done within 200ms. As a result, the Feed Ranking needs to return within **50ms**.
- Data freshness: Feed Ranking needs to be fully aware of whether or not a user has already seen any particular activity. Otherwise, seeing repetitive activity will compromise the user experience. Therefore, data pipelines need to run really fast.

### Summary[#](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Summary)

| **Type** | **Desired goals** |
| --- | --- |
| Metrics | Reasonable normalized cross-entropy |
| Training | High throughput with the ability to retrain many times per day |
|  | Supports high level of personalization |
| Inference | Latency from 100ms to 200ms |
|  | Provides a high level of data freshness and avoids showing the same feeds multiple times |

Video Recommendation System Design

Feed Ranking Model

Ask

[LinkedIn feed ranking](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#LinkedIn-feed-ranking)

[1. Problem statement](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#1-Problem-statement)

[2. Metrics design and requirements](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#2-Metrics-design-and-requirements)

[Metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Metrics)

[Offline metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Offline-metrics)

[Online metrics](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Online-metrics)

[Requirements](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Requirements)

[Training](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Training)

[Inference](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Inference)

[Summary](https://www.educative.io/courses/machine-learning-system-design/problem-statement-and-metrics-g7DrxM64mxZ#Summary)