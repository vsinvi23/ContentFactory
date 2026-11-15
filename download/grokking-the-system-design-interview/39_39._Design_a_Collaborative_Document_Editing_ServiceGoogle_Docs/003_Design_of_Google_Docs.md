# Design_of_Google_Docs

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design of Google Docs

Discover the System Design principles behind real-time collaborative services like Google Docs. Architect the system using WebSockets, time series databases, and processing queues to manage concurrency and low-latency updates. Learn to implement robust conflict resolution and document history tracking.

We'll cover the following...

- [Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Design)
  - [Components](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Components)
  - [Workflow](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Workflow)
  - [AI-powered writing assistance](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#AI-powered-writing-assistance)
    - [Using only what the user can read](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Using-only-what-the-user-can-read)
    - [Applying an edit while others are typing](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Applying-an-edit-while-others-are-typing)

## Design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Design)

We will design the system in two steps: first, selecting the components, and second, defining the workflow to meet the functional requirements.

### Components[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Components)

The design utilizes the following components:

- **API gateway:** Intercepts and routes client requests. It handles authentication, rate limiting, and directs edit requests, comments, and notifications to the appropriate services. It can also serve cached responses directly.
- **Application servers:** Execute business logic and compute-intensive tasks. This includes file format conversion (e.g., PDF to Word), import/export functionality, and attribute collection for the recommendation engine.
- **Data stores:** We use specific storage solutions for different data types:

  - **Relational database:** Stores user information and document metadata to enforce privilege restrictions.
  - **NoSQL:** Stores user comments for fast retrieval.
  - **Time series database:** Records the edit history of documents.
  - **Blob storage:** Stores media files like images and videos.
  - **Cache (Redis) and CDN:** Redis stores user sessions, typeahead features, and hot documents. The CDN serves static assets and heavy objects to improve end user performance.

AI Powered

Saved

1 attempt left

Reset

What are the considerations of storing document edit history indefinitely?

Describe the benefits and trade-offs of storing document edit history indefinitely and how these challenges can be mitigated.

This is your last attempt.

- **Operations queue:** Frequent small updates (such as character insertions) are inefficient to write to the database individually. The system uses a queue to batch these changes for periodic processing. WebSockets handle the transport layer to reduce overhead and enable real-time updates.
- **Other components:** Session servers maintain user session data and manage document access privileges. Together with the relational database, they act as the access control service. Additionally, configuration, monitoring, pub-sub, and logging services handle system health, leader election, and asynchronous tasks like notifications.

The illustration below depicts how these components coordinate to provide the service.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271145.7600000000002%27%20height=%27628%27/%3e)![A detailed design of the collaborative document editing service](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A detailed design of the collaborative document editing service")

A detailed design of the collaborative document editing service

The dashed purple group is the AI extension, described in “AI-powered writing assistance” below.

1.

Why should we use WebSockets instead of HTTP methods? Why are WebSockets optimal for this kind of communication?

Show Answer

1 / 3

### Workflow[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Workflow)

The following steps describe how requests are processed after reaching the API gateway:

- **Collaborative editing and conflict resolution:** Requests enter the operations queue, where conflicts between collaborators are resolved. Once resolved, data is batched and stored in the time series database via session servers. Media files are compressed for storage, while character edits are processed immediately.
- **History:** The time-series database supports version recovery. The system uses DIFF operations to compare versions and identify changes, enabling users to revert to older states.
- **Asynchronous operations:** Tasks like notifications, emails, and view counts are handled asynchronously. The API gateway publishes these events to a pub-sub component (e.g., Kafka) for processing.
- **Suggestions:** The typeahead service offers autocomplete suggestions for common words and phrases. It extracts attributes from documents to personalize suggestions. A NoSQL database stores a large volume of word data, while Redis caches frequently used phrases.
- **Import and export documents:** Application servers manage document import/export and format conversion (e.g., `.doc` to `.pdf`). They also handle feature extraction for the typeahead service.

> **Note:** WebSockets enhance performance and facilitate real-time chat between collaborators. Combining WebSockets with a cache like Redis enables an effective chat feature.

1.

We’re implementing view counters through an asynchronous method, which means that the number of views of a document may be outdated. Could we use sharded counters or Redis counters to get effective results?

Show Answer

1 / 2

### AI-powered writing assistance[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#AI-powered-writing-assistance)

Google Docs includes [Gemini](https://support.google.com/docs/answer/14355406), which can write, rewrite, and summarize text, and can draw on other files from the user’s Drive. The design below is a proposed architecture, not a description of Gemini’s internals. It builds on the grounded generation pattern from the [*Ask YouTube lesson*](https://www.educative.io/courses/grokking-the-system-design-interview/ask-youtube-ai-powered-conversational-video-discovery) and adds two concerns that are specific to a shared editor. In the detailed design, an AI assistant service sits behind the API gateway. It calls the access control service for permission checks and an LLM inference service to generate suggestions, and it sends accepted edits to the operations queue.

#### Using only what the user can read[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Using-only-what-the-user-can-read)

Suppose a user selects a paragraph and asks, “Rewrite this using the figures from our Q3 report.” The assistant needs content from another document, and that is where risk appears. If retrieval ignored permissions, the assistant could quote a document the user was never allowed to open.

The design therefore checks permissions at request time, for the user making the request:

- The retrieval step searches only documents the user can currently access, using the same access control service that protects normal file opens.
- A document shared yesterday but unshared this morning is excluded, so the check uses current permissions, not a cached copy.
- Each suggestion lists the source documents it used, so the user can verify them.
- Cached results are keyed by user and permission scope, so one user’s suggestion is never served to another.

#### Applying an edit while others are typing[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Applying-an-edit-while-others-are-typing)

Generating a suggestion takes a few seconds, and collaborators may edit the same paragraph meanwhile. If the suggestion were applied at its original character positions, it could overwrite newer work.

To prevent this, the request records the document revision and the selected range when it starts. When the user accepts the suggestion, the edit enters the same operations queue as typed edits, and the server transforms its position against everything that changed since that revision, using the same conflict resolution (OT or CRDT) covered in the next lesson. If the selected text itself was modified in the meantime, the system does not apply the edit automatically. It shows the suggestion again and asks the user to review it against the current text.

The following diagram shows the path from selection to an accepted edit.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27811%27%20height=%27581%27/%3e)![Generating and safely applying an AI suggestion in a shared document](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Generating and safely applying an AI suggestion in a shared document")

Generating and safely applying an AI suggestion in a shared document

**Note:** Retrieving more context, such as several related files, can improve suggestions, but every extra source needs its own permission check and adds latency and token cost. Keep context focused on what the request needs.

Requirements of Google Docs’ Design

Concurrency in Collaborative Editing

Ask

[Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Design)

[Components](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Components)

[Workflow](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Workflow)

[AI-powered writing assistance](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#AI-powered-writing-assistance)

[Using only what the user can read](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Using-only-what-the-user-can-read)

[Applying an edit while others are typing](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-google-docs#Applying-an-edit-while-others-are-typing)