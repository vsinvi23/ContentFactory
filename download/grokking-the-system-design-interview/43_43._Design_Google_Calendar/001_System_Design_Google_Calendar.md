# System_Design_Google_Calendar

Source: https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# System Design: Google Calendar

Google Calendar is a complex distributed system that enables users to create, manage, and share calendar events while ensuring consistency across devices and handling high traffic. Key challenges include managing time semantics, collaboration, synchronization, and timely notifications. The system must support functionalities like event lifecycle management, sharing, recurring schedules, and AI-assisted scheduling, all while maintaining low latency, high availability, and data durability. Resource estimations indicate significant storage and bandwidth needs, driven by user interactions and event updates. The architecture involves databases, caching, load balancing, and a distributed task scheduler to efficiently manage operations and user requests.

We'll cover the following...

- [What is Google Calendar?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#What-is-Google-Calendar)
  - [Why calendar systems are challenging](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-calendar-systems-are-challenging)
- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Requirements)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Storage-estimation)
    - [Why sync changes the math](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-sync-changes-the-math)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Bandwidth-estimation)
  - [Number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Number-of-servers-estimation)
  - [Estimating AI-assistant load](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Estimating-AI-assistant-load)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Building-blocks-we-will-use)
  - [Looking ahead](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Looking-ahead)

Millions of people rely on their calendars to show the same meeting details on every device, to share schedules with colleagues, and to send reminders on time, even when a meeting changes minutes before it starts. Meeting those expectations means coordinating event updates, access permissions, and synchronization across distributed services, including during traffic peaks.

## What is Google Calendar?[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#What-is-Google-Calendar)

**Google Calendar** lets users create, manage, and share calendar events. Users can configure event times, locations, attendees, and recurrence rules. Calendar-sharing settings and access permissions determine who can view or edit calendar events.

![](001_System_Design_Google_Calendar_images/img_1a6bd89182a8.svg)

From a System Design perspective, Google Calendar is a distributed scheduling and collaboration system, not a simple CRUD app. Opening a week view means fetching events in that range, expanding recurring series, applying exceptions, and enforcing access controls, while every client stays in sync.

Concurrency makes this harder. One user may update a recurring meeting while another views an older version and a third device is offline. The system must keep one source of truth, sync changes to every client, notify affected attendees, and update their reminders.

### Why calendar systems are challenging[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-calendar-systems-are-challenging)

Calendar systems combine several concerns that are relatively simple individually but become difficult when they interact:

- **Time semantics:** Events can be one-time or recurring, span time zones, and contain exceptions to recurring patterns.
- **Collaboration:** Events can have multiple attendees, shared calendars, and different access permissions.
- **Synchronization:** Updates need to propagate across users and devices while handling concurrent edits and temporarily offline clients.
- **Time-sensitive notifications:** Reminders and invitations must be scheduled for future delivery and remain reliable even when the system is processing large numbers of events.
- **Read-heavy access patterns:** Users frequently browse calendar ranges, while updates must preserve a consistent authoritative state.

In this chapter, we will design a Google Calendar-like system. We begin by defining functional and nonfunctional requirements, followed by estimates of storage, bandwidth, and compute capacity. The next lesson covers the high-level architecture, data model, and workflows for event synchronization, recurrence handling, reminders, and collaboration. We then extend the design with an AI assistant that interprets natural language requests and suggests available meeting times.

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Requirements)

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Functional-requirements)

A reasonable interview scope includes the following capabilities.

- **Event life cycle:** Users can create, edit, and delete events. Accepted changes must be persisted and made available to authorized clients.
- **Sharing and invitations:** Users can invite attendees, share calendars, and configure permissions that control who can view or modify event information.
- **Recurring schedules:** Users can create recurring events using recurrence rules and modify individual occurrences or the entire series.
- **Reminders:** Users can configure email, push, or in-app reminders that are delivered before an event begins.
- **Calendar views:** Users can load day, week, and month views, requiring efficient time-range queries over event data.
- **Device synchronization:** Web, mobile, and desktop clients must receive near-instant incremental updates after changes and catch up correctly after being offline.
- **AI-assisted scheduling:** Users can describe a meeting in natural language, such as “Find 30 minutes with Aisha and Omar next week before my lunch break,” and receive ranked time suggestions that respect attendees’ availability, working hours, and time zones. No event is created until the user confirms a suggestion.

**Note:** Useful event fields may include title, description, start time, end time, time zone, participants, reminder settings, visibility, and recurrence metadata. Full-text event search, task lists, and video-conferencing integration are out of scope for this design.

### Nonfunctional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Nonfunctional-requirements)

These capabilities impose stronger guarantees than a typical CRUD application:

- **Consistency:** Accepted writes must be durable and reflected correctly across organizer and attendee calendars. The system does not need global serializability, but an acknowledged edit must never disappear, and concurrent edits to the same event must be detected rather than silently overwritten.
- **Low latency:** Calendar views should feel interactive (for example, a week view within a few hundred milliseconds at p95), even though they require recurrence expansion and permission checks.
- **High availability:** Work and personal schedules are operational data, so reads and writes must remain available during server and zone failures.
- **Durability:** Event history is long-lived, so storage must survive node and zone failures and support recovery from backups.
- **Correct time handling:** Timed events store their start time with an IANA time zone, such as America/New\_York, and recurring series are expanded in that zone, so a weekly 9:00 a.m. meeting stays at 9:00 a.m. local time across daylight saving changes. Expanded instances can be indexed as UTC instants for fast range queries. All-day events are stored as dates, not as UTC midnight timestamps.
- **Privacy and access control:** Users see only what their permissions allow. For example, a free/busy viewer sees occupied intervals without titles or descriptions, and revoked access takes effect promptly, including in caches.
- **Timely reminders:** Reminders must fire close to their scheduled time, even during bursts such as thousands of meetings starting at 9:00 a.m.
- **Isolated and bounded AI:** The AI assistant must not degrade core calendar operations. It runs on separate capacity with quotas and timeouts, receives only the data it needs (free/busy rather than event details), and manual event creation keeps working if the model is unavailable.

![Requirements of Google Calendar](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Requirements of Google Calendar")

Requirements of Google Calendar

With the scope and guarantees defined, we can now size the traffic and storage footprint.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Resource-estimation)

We base our resource estimates on the following assumptions:

- 500 million registered users and 50 million daily active users (DAU)
- Each user creates two events per day. A recurring series counts as one event, because we store one recurrence rule plus exceptions, not every instance.
- Average event record size is3 KB3\ KB3 KB(title, description, start/end time, time zone, recurrence rule, visibility, and indexing overhead).
- Each event has five attendees on average. Each attendee gets their own entry (RSVP status, color, personal reminders) of1 KB1\ KB1 KB.
- Each attendee has two reminders per event, and each reminder job is0.2 KB0.2\ KB0.2 KB.
- Each user performs 20 reads per day (calendar views and sync requests).

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Storage-estimation)

With 50 million DAU each creating 2 events, 100 million events are created daily. The storage requirements for one day are:

#### Estimating Storage Requirements

|  |  |  |
| --- | --- | --- |
| Daily active users | 50 | million |
| Events per user | 2 | per day |
| Events created per day | f100 | million |
| Event record size | 3 | KB |
| Attendees per event | 5 | attendees |
| Attendee entry size | 1 | KB |
| Reminders per attendee | 2 | reminders |
| Reminder job size | 0.2 | KB |
| Storage per event | f10 | KB |
| Total daily storage | f1 | TB/day |

**Note:** Adjust the values in the calculator above to observe changes in storage requirements.

![Storage required by the calendar service per day](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Storage required by the calendar service per day")

Storage required by the calendar service per day

#### Why sync changes the math[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-sync-changes-the-math)

A single update fans out. Changing a meeting with ten attendees who each use two devices means 20 device syncs plus reminder updates, so synchronization and notifications carry much of the load:

- **Reads:** Month and week views dominate request count because browsing is frequent.
- **Writes:** Event edits matter more than their raw count suggests because correctness errors are user-visible.
- **Background work:** Reminder scheduling and delivery can exceed CRUD operations in busy periods.

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Bandwidth-estimation)

**Incoming traffic:** With 1 TB of daily writes, the incoming traffic requirement is:

1 TB86400×8=1,000,000,000 KB86400×8=11,574 KB/s×8=92,593 Kbps≈93 Mbps\frac{1\text{ TB}}{86400} \times 8 = \frac{1{,}000{,}000{,}000\text{ KB}}{86400} \times 8 = 11{,}574\text{ KB/s} \times 8 = 92{,}593\text{ Kbps} \approx 93\text{ Mbps}864001 TB​×8=864001,000,000,000 KB​×8=11,574 KB/s×8=92,593 Kbps≈93 Mbps

This is an upper bound. Attendee entries and reminder jobs are generated by the server, so the actual client upload is smaller.

**Outgoing traffic:** Assume each daily active user makes 20 reads per day: 60% are calendar views (about 30 KB per response) and 40% are incremental syncs (about 5 KB per delta). In addition, every new event fans out a 3 KB update to five attendees on two devices each, and each of its 10 reminders produces a notification of about 1 KB. The outgoing traffic is:

#### Bandwidth Requirements

|  |  |  |
| --- | --- | --- |
| Reads per second | 11574 | per second |
| Calendar view response size | 30 | KB |
| Incremental sync response size | 5 | KB |
| Bandwidth for calendar views | f1666.656 | Mbps |
| Bandwidth for incremental sync | f185.184 | Mbps |
| Events created per second | 1157 | per second |
| Fan-out data per event | 30 | KB |
| Bandwidth for attendee fan-out | f277.68 | Mbps |
| Bandwidth for reminder notifications | f92.56 | Mbps |
| Total outgoing bandwidth | f2.22208 | Gbps |

> **Note:** Adjust the values in the calculator above to observe changes in the bandwidth requirements.

![The total bandwidth required by Google Calendar](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The total bandwidth required by Google Calendar")

The total bandwidth required by Google Calendar

### Number of servers estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Number-of-servers-estimation)

Requests per second follow from the same assumptions. Each daily active user makes about 20 reads and 2 writes per day, which averages to roughly 12,700 requests per second. Following the convention from the back-of-the-envelope chapter, we size for a deliberately pessimistic peak by treating daily active users as peak requests per second, which gives 50 million requests per second. This upper bound leaves ample headroom for bursts, sync fan-out, and retries. We use the following formula to calculate the number of servers:

Servers needed at peak load=Number of requests/secondRPS of server\text{Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of server}}Servers needed at peak load=RPS of serverNumber of requests/second​

Assuming a server handles 64,000 RPS, the required server count is:

Servers needed at peak load=50 million64,000=781.25≈782 servers\text{Servers needed at peak load} = \frac{50\text{ million}}{64{,}000} = 781.25 \approx 782\text{ servers}Servers needed at peak load=64,00050 million​=781.25≈782 servers

![The estimated number of servers required for Google Calendar](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The estimated number of servers required for Google Calendar")

The estimated number of servers required for Google Calendar

**Note:** This count covers the request-serving tier. Reminder scheduling and notification delivery run as separate background workers. In busy periods, such as thousands of meetings starting at 9:00 AM, their load can exceed normal create, read, update, and delete traffic, so they are scaled independently using queues to smooth bursts.

### Estimating AI-assistant load[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Estimating-AI-assistant-load)

Assume 10% of the 50 million daily active users, or 5 million users, make one assistant request per day. With an average of two model calls per request, one to interpret user intent and another to generate suggestions or handle clarification, this results in approximately 10 million model calls per day, averaging 116 model calls per second. Assuming 1,500 input tokens and 200 output tokens per call, daily token usage reaches approximately 17 billion tokens: 15 billion input tokens and 2 billion output tokens.

At approximately 116 model calls per second, AI traffic is much lower than the estimated 11,574 calendar reads per second. However, model inference typically has higher latency and compute costs than a database read, with response times ranging from hundreds of milliseconds to several seconds. Meeting-scheduling requests may also require free/busy lookups across participants' calendars. AI workload capacity is therefore driven primarily by inference throughput, latency, and cost rather than request volume alone. Deploy AI inference on a separate compute tier with per-user quotas and request timeouts to prevent inference workloads from affecting core calendar operations. The lesson on serving models within latency and cost budgets shows how to size such a tier from token demand.

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Building-blocks-we-will-use)

The design uses the following building blocks:

![Building blocks required for Google Calendar](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks required for Google Calendar")

Building blocks required for Google Calendar

- [**Databases**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases)**:** Store calendars, events, recurrence rules, exceptions, attendee RSVP state, and access permissions. Event data is partitioned by calendar ID and per-user attendee views by user ID, so most reads and writes stay on one shard.
- [**Cache**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-cache)**:** Stores frequently viewed day, week, and month ranges and common user metadata. Cached ranges must be invalidated or bypassed after a write, because stale event data is immediately visible to users.
- [**Load balancers**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers)**:** Distribute incoming user traffic across stateless API servers.
- **Pub-sub:** Carries a change event for each committed write, published reliably through a transactional outbox. Sync services, invitation workers, and the notification service subscribe to these changes and process them independently.
- [**Distributed task scheduler**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-task-scheduler)**:** Tracks future reminder times and triggers notifications when they are due. It also smooths bursts, such as thousands of reminders firing at the top of the hour.

**AI extension:** The meeting-suggestion feature uses a hosted large language model (LLM) to turn a natural language request into structured scheduling parameters, such as attendees, duration, and date range. Calendar services then check availability and create the event, so the model never writes data directly. This follows the pattern from the AI building blocks chapter: the model is a component with a narrow output contract, integrated as an external dependency with rate limits, timeouts, and a fallback to manual scheduling.

**Note:** Caching calendar ranges improves speed, but recurring event edits and attendee visibility rules make cache invalidation harder than simple key-value caching.

### Looking ahead[#](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Looking-ahead)

The requirements, estimates, and building blocks set the foundation. In the next lesson, we define the high-level architecture, data model, request flows, synchronization, and failure handling, and then integrate the AI assistant that suggests meeting times from verified availability.

Design of the LeetCode System

Design of Google Calendar

Ask

[What is Google Calendar?](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#What-is-Google-Calendar)

[Why calendar systems are challenging](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-calendar-systems-are-challenging)

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Storage-estimation)

[Why sync changes the math](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Why-sync-changes-the-math)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Bandwidth-estimation)

[Number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Number-of-servers-estimation)

[Estimating AI-assistant load](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Estimating-AI-assistant-load)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Building-blocks-we-will-use)

[Looking ahead](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-calendar#Looking-ahead)