# How_Spotify_Wrapped_Scales_for_7M_Users

Source: https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# How Spotify Wrapped Scales for 7M Users

Spotify Wrapped is an annual feature that delivers personalized music summaries to users, leveraging advanced data processing and machine learning to handle massive amounts of user data. The system is designed for scalability, efficiently managing millions of simultaneous requests while ensuring low latency and high performance. Key components include a microservices architecture, data pipelines, and cloud services that facilitate real-time data processing and personalized insights. Spotify continuously enhances the Wrapped experience, integrating new features and AI-driven innovations to engage users and maintain its status as a global phenomenon.

We'll cover the following...

- [Getting to know Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Getting-to-know-Spotify-Wrapped)
  - [Wrapped over the years](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-over-the-years)
  - [Estimating Wrapped users](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Estimating-Wrapped-users)
  - [Wrapped data](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-data)
- [Challenges of scaling Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Challenges-of-scaling-Spotify-Wrapped)
  - [Scalability and resource management](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-and-resource-management)
  - [Data volume and processing](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-volume-and-processing)
  - [Personalization complexity](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Personalization-complexity)
  - [Cost management](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Cost-management)
  - [Data compliance](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-compliance)
- [Scalability techniques for Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-techniques-for-Spotify-Wrapped)
- [Spotify System Design and workflow](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Spotify-System-Design-and-workflow)
  - [Key system components and services](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Key-system-components-and-services)
  - [Distributed databases](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Distributed-databases)
  - [System Design for Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#System-Design-for-Spotify-Wrapped)
    - [Data collection or ingestion (Extract)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-collection-or-ingestion-Extract)
    - [Data processing (Transform)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-processing-Transform)
    - [Data warehousing (Load)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-warehousing-Load)
    - [Wrapped creation and personalization (Reverse ETL)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-creation-and-personalization-Reverse-ETL)
  - [Front-end animations in Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Front-end-animations-in-Spotify-Wrapped)
    - [Visual and interactive features](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Visual-and-interactive-features)
    - [Feature highlights](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Feature-highlights)
- [What we can learn from Spotify](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#What-we-can-learn-from-Spotify)
- [What’s next for Spotify Wrapped?](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Whats-next-for-Spotify-Wrapped)

Every year-end, Spotify delivers its users a gift: a beautifully personalized summary of their listening habits. From your top songs to your most-streamed genres, Spotify Wrapped transforms your music data into an engaging, shareable story.

Spotify Wrapped is also a powerful product offering that users wait for each year.

The numbers speak for themselves:

- 100 million+ shares on social media in 2022[1](https://hightouch.com/blog/how-spotify-wrapped-works)
- 20% increase in Spotify downloads in 2020[2](https://www.moengage.com/blog/spotify-wrapped-2020-app-downloads-engagement/)
- 602 million users engaged across 184 countries (as of 2023)[3](https://investors.spotify.com/financials/default.aspx#quarterly-results)

But Spotify Wrapped is more than just a successful marketing campaign; it’s a time capsule of your year in music, powered by data science, machine learning, and immaculate System Design.

Behind every Wrapped recap is a robust architecture that processes petabytes of data with precision and speed. This means that engineers are working diligently to ensure Wrapped is seamless, scalable, and always ready for millions of users worldwide.

Let’s explore the inner mechanics that make Spotify Wrapped work like clockwork. We’ll cover:

- Challenges for scaling Spotify Wrapped
- System Design of Spotify Wrapped
- 4 engineering lessons we can learn from Spotify

Let’s dive in.

## Getting to know Spotify Wrapped[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Getting-to-know-Spotify-Wrapped)

Spotify’s scalable system design allows the Wrapped campaign to serve millions of users reliably by transforming listening data into personalized year-end summaries.

 By seamlessly scaling to meet huge surges in demand, Spotify ensures that each Wrapped experience is fast, personalized, and ready to share.

### Wrapped over the years[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-over-the-years)

Since its launch in 2016, Spotify Wrapped has added new layers of interactivity and personalization every year:

|  |  |
| --- | --- |
| **Year** | **Spotify Wrapped Features** |
| 2016 | - The first edition of Spotify offered basic stats, such as the top songs, artists, and genres, based on users’ yearly listening habits |
| 2017 | - Expanded stats with more detailed insights, including top 5 artists, songs, genres, and the ability to share these stats on social media |
| 2018 | - Top artists, songs, genres - Added “Your Top Songs” playlist, allowing users to re-listen to their top songs of the year |
| 2019 | - Top artists, songs, genres - Introduced “Tastebreakers” playlist, which recommended new songs outside users’ usual preferences - Added a slideshow for a more engaging experience - Introduced decade-based insights into users’ listening history |
| 2020 | - Top artists, songs, genres - Focused on past listening patterns and added “Missed Hits” playlist - Introduced new stats like the number of new artists discovered, top podcasts, etc. |
| 2021 | - Introduced new interactive features like “Audio Aura.” - The “2021: The Movie,” which matched users’ music to movie scenes - Introduced shareable “Wrapped Cards” for social media |
| 2022 | - Added personalized “Listening Personality” types and improved visuals - Introduced “Audio Day,” offering a peak into evolving tastes based on preferences at different times of the day - Expanded on the slideshow, making it more dynamic and engaging |
| 2023 | - Enhanced “Listening Personality” insights with social sharing - Introduced custom storylines based on listening behavior - Upgraded interactive slideshow - Added “Me in 2023,“ which assigns users a unique listening character - Introduced “Sound Town,” matching listeners to a city that reflects their music tastes - An “AI DJ” that guides users through their Wrapped with commentary on top songs and artists |

### Estimating Wrapped users[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Estimating-Wrapped-users)

![widget](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "widget")

We estimated user counts for 2024 based on past user data from [Spotify](https://investors.spotify.com/financials/default.aspx#quarterly-results)

- 700 million total monthly active users on Spotify

  - Based on average growth of ~23%, 2019 to 2023
- 295 million users accessing Wrapped

  - Based on the average growth of 37.5%, from 2019 to 2022 (2023 data is undisclosed)

While not every user opens and accesses their Wrapped, Spotify creates the personalized Wrapped experience for each user (provided they meet simple eligibility criteria, such as minimum listening time).

### Wrapped data[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-data)

Spotify likely logs user data from January 1 through November 15 or 30.

Here are some insights on the Wrapped data that’s collected:

- Top songs and artists are ranked by play count, not total listening time.
- Songs must be played for over 30 seconds to count in rankings.
- Only the first 10 songs in the top 100 playlists are strictly sorted by play count.

## Challenges of scaling Spotify Wrapped[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Challenges-of-scaling-Spotify-Wrapped)

Processing data and creating Wrapped for 700 million users requires a scalable and robust architecture to process data from the year-long music history of their users. Spotify must support millions of concurrent streams, store and serve petabytes of data, and generate personalized recommendations with low latency.

The engineering team faces several challenges when ensuring a seamless Spotify Wrapped user experience:

### Scalability and resource management[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-and-resource-management)

Scalability is crucial amid Wrapped, as the surge in user engagement and social sharing can overload the system. Maintaining scalable, serverless, and auto-scaling solutions is critical, but these must be optimized without overloading and increasing costs.

### Data volume and processing[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-volume-and-processing)

Spotify handles an enormous amount of data, especially historical data, across hundreds of millions of users.

Processing this data in batch jobs to compile Wrapped insights while simultaneously managing real-time data flows for recommendations requires highly efficient data pipelines and storage solutions, like data lakes and distributed storage.

### Personalization complexity[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Personalization-complexity)

Wrapped’s success hinges on hyper-personalized insights, which require complex machine learning models trained on massive datasets. Scaling these models while avoiding latency issues is challenging, but advanced machine learning models can help optimize this process.

### Cost management[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Cost-management)

Efficiently managing cloud resources during Wrapped’s annual spike is key to balancing performance and costs. One may do this by integrating Wrapped calculations into existing data pipelines used for real-time recommendations.

### Data compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-compliance)

Handling user data requires compliance with regulations like GDPR and CCPA. Spotify can ensure data privacy while maintaining low-latency data delivery through edge computing and real-world distributed systems.

## Scalability techniques for Spotify Wrapped[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-techniques-for-Spotify-Wrapped)

Let’s see how Spotify’s scalability techniques help address these challenges.

|  |  |  |
| --- | --- | --- |
| **Technique** | **Description** | **Challenges Addressed** |
| Multi-tiered storage | Cloud-based tiered storage efficiently stores vast amounts of historical user data and Wrapped results. | Data volume and processing, cost management |
| Horizontal scaling | Adds servers instead of upgrading existing ones, enabling Spotify to handle massive concurrent user demand. | Scalability and resource management, availability |
| Serverless and auto-scaling | Uses serverless architectures and auto-scaling (e.g., AWS Lambda, GCP) to dynamically allocate resources as demand spikes. | Scalability, cost management |
| Data processing using the data lake | Processes user history and engagement data in a data lake or warehouse to manage high-volume batch processing needed for Wrapped. | Data volume, processing, and personalization complexity |
| Real-time processing | Uses tools like Kafka and Spark to continuously process user data, ensuring real-time insights are available. | Data volume, processing, and personalization complexity |
| Edge computing | Caches content closer to users on edge servers, reducing latency and handling regional load effectively during Wrapped access. | Data compliance, scalability & resource management |
| Monitoring and auto-recovery | Implements real-time monitoring tools like Grafana and failover mechanisms to detect and recover from issues quickly. | Scalability and resource management, availability |

## Spotify System Design and workflow[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Spotify-System-Design-and-workflow)

Spotify’s system design ensures seamless streaming, user interactions, and personalized features, such as Wrapped. The architecture is designed for scalability and high availability, efficiently handling millions of simultaneous requests.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27900.2%27%20height=%27373.0999999999999%27/%3e)![An overview of Spotify’s scalable System Design](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "An overview of Spotify’s scalable System Design")

An overview of Spotify’s scalable System Design

### Key system components and services[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Key-system-components-and-services)

Here’s how Spotify processes user requests and ensures scalability:

- **API gateway:** Acts as the entry point, authenticating user requests.
- **Load balancer:** Distributes requests evenly across application servers to handle large volumes of traffic.
- **Messaging queue:** User interactions (e.g., playing songs, creating playlists) are sent to a queue (like Pub/Sub or Kafka). This queue distributes data to various microservices for tasks such as generating recommendations or creating wrapped summaries. This allows the data to be processed asynchronously, improving scalability and availability.

This asynchronous approach enhances scalability and availability, ensuring Spotify’s system can handle traffic spikes and real-time demands.

Spotify’s microservices architecture supports various tasks:

- **User service:** Manages user data, including preferences and subscriptions, with connections to a payment service for subscription verification.
- **Upload service:** Ingests new content from artists.
- **Transcoding service:** Converts uploaded files into streaming-compatible formats, storing them in cloud-based blob storage (and metadata into an SQL database).
- **Streaming service:** Delivers content to users via a content delivery network (CDN), minimizing latency.
- **Search service:** Enables fast lookups using Elasticsearch.
- **Processing service:** Powers recommendations and wrapped summaries using advanced machine learning models.
- **Monitoring service:** Monitors the overall system’s health and alerts in case of errors, failures, etc.

### Distributed databases[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Distributed-databases)

Spotify employs multiple database types:

- **Blob storage:** Stores tracks, podcasts, and audiobooks.
- **SQL databases:** Store user metadata, such as account details.
- **NoSQL databases:** Handle activity data, including listening history, playlists, and preferences.

### System Design for Spotify Wrapped[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#System-Design-for-Spotify-Wrapped)

Let’s explore how data processing services handle such a massive amount of data at scale to create personalized Spotify Wrapped experiences.

Spotify uses the ETL (Extract, Transform, Load) process: **Extract** defines how data is collected, **Transform** covers how data is processed and turned into features, and **Load** specifies where data is stored for efficient retrieval. They also use reverse ETL to create Wrapped from the processed data.

#### Data collection or ingestion (Extract)[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-collection-or-ingestion-Extract)

A **data collection service** collects data from data resources (databases) and passes it to tools like Kafka or Pub/Sub to stream and make it available for immediate processing.

#### Data processing (Transform)[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-processing-Transform)

The data from the ingestion layer is fed to the processing layer, where the batch processor runs on massive data, aggregating users’ year-long listening tasks and generating insights. Spotify utilizes Google Cloud Bigtable to efficiently manage its extensive time-series data and user listening history, optimizing it for rapid data aggregation over specific time frames.

In 2019, Spotify’s use of Bigtable and BigQuery for data processing resulted in processing 5 times the data while reducing the overall cost by 25 percent.

Spotify can quickly compile user-level insights by structuring data storage to minimize shuffling (reducing the need to move data between nodes, which can be time-consuming and resource-intensive) during processing.

> **Note:** The following illustration is an in-depth exploration of how data processing services process data and transform it into a personalized Wrapped.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27916.7500000000002%27%20height=%27625.0999999999999%27/%3e)![A detailed design of data processing for Spotify Wrapped](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A detailed design of data processing for Spotify Wrapped")

A detailed design of data processing for Spotify Wrapped

#### Data warehousing (Load)[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-warehousing-Load)

Apache Spark and other big data frameworks process this data at scale, and the results are stored in data warehouses, such as Google BigQuery.

#### Wrapped creation and personalization (Reverse ETL)[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-creation-and-personalization-Reverse-ETL)

Finally, data visualization tools and services aggregate this processed data, allowing Wrapped summaries to be sent to the user in real time through APIs. Cloud services ensure low latency, high availability, and scalability across Spotify’s global infrastructure.

The Wrapped summaries are sent to users via Email or in-app notifications through the Pub/Sub service.

> **Note:** Spotify Wrapped is all about personalization, done by utilizing advanced machine learning algorithms. The ML engine uses collaborative filtering, content-based filtering, and a hybrid model, mostly the best of both, to generate personalized Wrapped for each user.

For 2019 Wrapped, Spotify processed decade-long user data utilizing Bigtable. A similar data processing pattern for a year-long dataset is shown below:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271201%27%20height=%27384%27/%3e)![The architecture of data pipelines [source: Spotify]](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The architecture of data pipelines [source: Spotify]")

The architecture of data pipelines [source: Spotify]

### Front-end animations in Spotify Wrapped[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Front-end-animations-in-Spotify-Wrapped)

The front-end experience for Spotify Wrapped plays a crucial role in driving user engagement. The design of the Wrapped interface transforms raw data into fun, shareable content.

Spotify Wrapped’s front-end elements include:

#### Visual and interactive features[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Visual-and-interactive-features)

- **Personalized visualizations:** Insights are displayed as animated reels or cards.
- **NLP-powered content:** Uses natural language processing to generate captions and labels for animations.

#### Feature highlights[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Feature-highlights)

- **Audio Aura (2021):** Colors representing listening intensity for different genres.
- **Sound Town (2023):** Mapped users’ tastes to fictional cities, creating playful, shareable visuals.

These interactive features enhance user engagement, turning data into delightful experiences.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27285.98%27%20height=%27510%27/%3e)![2023 Sound Town [Source: Spotify]](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "2023 Sound Town [Source: Spotify]")

2023 Sound Town [Source: Spotify]

## What we can learn from Spotify [#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#What-we-can-learn-from-Spotify)

Here are 4 key takeaways from Spotify’s approach to delivering a seamless Wrapped experience each year:

1. A robust, scalable System Design is the backbone of Wrapped. It handles huge data volumes by separating real-time and batch-processing content, ensuring fast data access and reliable yearly insights.
2. Using solutions like Bigtable and BigQuery, Spotify minimizes data shuffling and enables efficient aggregation, providing users with quick, user-level insights for millions.
3. Advanced machine learning models help Spotify deliver Wrapped’s unique, personalized insights by analyzing patterns in listening data.
4. By employing auto-scaling and load balancing, Spotify can smoothly manage the surge in Wrapped engagement.

## What’s next for Spotify Wrapped?[#](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Whats-next-for-Spotify-Wrapped)

As Spotify Wrapped continues to scale year after year, it offers a glimpse into the complex System Design that powers real-world applications at a massive scale.

Spotify’s developers continually add new features and insights to enhance the user experience, making it challenging to predict what’s coming next. However, we can expect AI to level up the Wrapped experience through features like:

- Interactive, real-time playlists that evolve based on a user’s Wrapped experience.
- AI-driven music DNA visualizations breaking down listening habits into dynamic, shareable formats.
- Leveraging GenAI to create unique soundtracks for users, blending favorite genres, moods, and artists into a custom composition.

Spotify Wrapped highlights the importance of approaches like cloud-based data pipelines, advanced machine learning models, and auto-scaling for cost savings in System Design.

**Disclaimer:** All technical information and design insights provided in this lesson are curated by our System Design experts to the best of their knowledge and based on available resources, including insights from Spotify’s engineering blogs. While we strive for accuracy, some details may vary from Spotify’s actual implementations and are intended for educational purposes only.

System Design Interview PDF

How Amazon Scales for Prime Day

Ask

[Getting to know Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Getting-to-know-Spotify-Wrapped)

[Wrapped over the years](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-over-the-years)

[Estimating Wrapped users](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Estimating-Wrapped-users)

[Wrapped data](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-data)

[Challenges of scaling Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Challenges-of-scaling-Spotify-Wrapped)

[Scalability and resource management](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-and-resource-management)

[Data volume and processing](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-volume-and-processing)

[Personalization complexity](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Personalization-complexity)

[Cost management](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Cost-management)

[Data compliance](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-compliance)

[Scalability techniques for Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Scalability-techniques-for-Spotify-Wrapped)

[Spotify System Design and workflow](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Spotify-System-Design-and-workflow)

[Key system components and services](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Key-system-components-and-services)

[Distributed databases](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Distributed-databases)

[System Design for Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#System-Design-for-Spotify-Wrapped)

[Data collection or ingestion (Extract)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-collection-or-ingestion-Extract)

[Data processing (Transform)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-processing-Transform)

[Data warehousing (Load)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Data-warehousing-Load)

[Wrapped creation and personalization (Reverse ETL)](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Wrapped-creation-and-personalization-Reverse-ETL)

[Front-end animations in Spotify Wrapped](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Front-end-animations-in-Spotify-Wrapped)

[Visual and interactive features](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Visual-and-interactive-features)

[Feature highlights](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Feature-highlights)

[What we can learn from Spotify](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#What-we-can-learn-from-Spotify)

[What’s next for Spotify Wrapped?](https://www.educative.io/courses/grokking-the-system-design-interview/how-spotify-wrapped-scales-for-7m-users#Whats-next-for-Spotify-Wrapped)