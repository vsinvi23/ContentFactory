# Designing_Real-Time_Voice_Assistants_for_Low_Latency_and_Privacy

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Real-Time Voice Assistant

Design a real-time voice assistant that streams audio continuously, handles turn-taking and interruptions, and recovers from failures while keeping latency low. Size it for peak concurrent sessions, and build it from incremental, modular components that balance responsiveness, accuracy, and privacy.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Storage-estimation)
  - [Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Compute-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Bandwidth-estimation)
- [System design of a real-time voice assistant](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-design-of-a-real-time-voice-assistant)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#High-level-design)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#A-detailed-system-design)
  - [Speech understanding and turn packaging](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-understanding-and-turn-packaging)
  - [Session state and memory](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-state-and-memory)
  - [Speech generation and moderation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-generation-and-moderation)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Workflow-of-the-system)
  - [Session states](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-states)
    - [Listening and endpointing](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Listening-and-endpointing)
    - [Thinking and speaking](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Thinking-and-speaking)
  - [Unhappy paths](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Unhappy-paths)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-nonfunctional-requirements)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Conclusion)

A voice assistant can answer correctly and still feel broken. The failure often happens in the silence after the user stops speaking. If that gap stretches past roughly a second, users start talking over the system, repeat themselves, or assume the call dropped.

This lesson treats that gap as a system design problem. A production voice assistant is not just text chat with audio attached. Capacity is shaped by long-lived concurrent sessions, continuous audio streaming, interruption handling, and strict p95 latency targets. The system must keep listening while it speaks, cancel work mid-response, and recover when audio quality collapses.

We will scope the design around three forces only.

- **Latency** governs every stage on the critical path.
- **Accuracy** must hold under noise, accents, packet loss, and imperfect endpoint detection.
- **Privacy** changes retention, routing, consent, and even whether raw audio is stored at all.

> **Note:** In voice systems, concurrency matters more than requests per second because each session occupies transport, state, and model capacity for minutes.

That framing also sets up the next lesson. Once many real-time models and policies coexist, routing and observability stop being app concerns and become gateway concerns. First, though, we need the voice architecture itself.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-requirements)

Requirements decide the design, so fix them before sizing anything.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Functional-requirements)

- **Turn-taking**: The assistant listens while it speaks, detects end of speech, and yields to real interruptions.
- **Streaming dialogue**: It transcribes, reasons, and speaks incrementally instead of waiting for each stage to finish.
- **Tool use**: It can call tools mid-conversation and speak the result.
- **Consent and retention**: It honors recording consent, retention limits, and deletion requests.
- **Failure recovery**: It survives packet loss, low ASR confidence, and TTS failure without dropping the call.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Nonfunctional-requirements)

- **Latency**: Silence after the user stops speaking stays under about 1 second at p95.
- **Scalability**: The fleet supports 20,000 concurrent sessions at peak.
- **Availability**: Regional media edges and failover keep calls alive.
- **Accuracy**: Speech recognition holds up under noise, accents, and packet loss.
- **Privacy**: Raw audio is encrypted, consent-gated, and kept only as long as policy allows.
- **Cost**: Cancellation-aware serving and warm pools avoid paying for abandoned replies.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Resource-estimation)

Let's size the system from one workload: 20,000 peak concurrent sessions, 4-minute calls, and 50 percent average utilization. Every number below derives from these assumptions.

### Storage estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Storage-estimation)

Let's start with what persists after a call and what must exist during a call. Voice systems keep hot session state in memory, then move artifacts to colder storage. The main buckets are session metadata, transcripts, optional recordings, evaluation labels, and model assets.

With 4-minute calls and 50 percent average utilization, the fleet averages 10,000 concurrent sessions, or about 3.6 million sessions per day, and only 10 percent are retained with consent. Mono compressed audio runs at 24 kbps per direction, so a retained call holds 48 Kbps × 240 s = 11520 KB\text{48 Kbps × 240 s = 11520 KB}48 Kbps × 240 s = 11520 KB, or roughly 1.44 MB before protocol overhead. Across 360,000 retained sessions, that is about 520 GB per day. Transcripts are small by comparison. Each session has 12 turns of about 200 bytes after normalization, so 3.6 million sessions produce about 8.6 GB of transcripts per day.

The system usually separates storage into the following groups.

- **Hot session state:** This keeps turn history, active tool results, consent flags, and transport state in low-latency stores for the life of the conversation.
- **Cold content storage:** This stores archived transcripts, redacted artifacts, and optional recordings in object storage with life cycle policies.
- **Model assets:** These include ASR, TTS, and safety model weights, which stay mostly constant and scale weakly with traffic.

> **Practical tip:** In many domains, retention policy matters more than codec choice because audio dominates storage and deletion workflows dominate operational complexity.

Because recorded voice is more sensitive than plain-text logs, storage design must also carry deletion indexes, residency tags, and redaction lineage. With persistence scoped, we can size the live compute path next.

### Compute estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Compute-estimation)

A voice system is sized by simultaneous conversations, not by request rate. Let's plan for the 20,000 peak concurrent sessions above. At any moment, only a fraction are actively speaking, but every session still holds media transport, state, and interruption monitoring.

We use separate pools for ASR, orchestration, LLM, and TTS because they scale differently. Suppose that each active user produces 1.5 seconds of speech every 8 seconds on average. That means about 18.75 percent of sessions are sending meaningful speech at a time, or roughly 3,750 actively transcribed streams. If streaming ASR handles 100 real-time streams per accelerator with headroom, around 38 accelerator equivalents are needed at p95 plus reserve.

For generation, let's assume each reply averages 60 tokens and users trigger 2.5 replies per minute. Then 20,000 sessions generate about 50,000 replies per minute, or 3 million tokens per minute if every reply runs to completion. In practice, barge-in cancels some replies early, so cancellation-aware serving materially reduces waste. TTS must also stream fast enough for first audio, not just total completion. If the assistant speaks about as often as users do, roughly 18.75 percent of the time, that is about 3,750 concurrent TTS streams. At 200 low-latency streams per worker, about 19 workers are needed plus reserve, not 100.

Warm pools and admission control matter because queueing destroys p95. To hide model latency, the assistant can speak a short filler phrase such as "Let me check that" while the main model works, but only if orchestration can stop the filler cleanly when the real answer is ready.

> **Attention:** A voice assistant that hits target average latency but queues during traffic bursts still fails the interview requirement, because p95 first-audio is the user-facing contract.

Regional sharding usually follows geography and compliance boundaries. Once compute is roughly sized, network throughput becomes the next hard limit.

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Bandwidth-estimation)

Bandwidth comes from continuous duplex audio, not from discrete API payloads. Let's assume each client uploads compressed speech at 24 kbps and receives synthesized speech at 32 kbps. For 20,000 concurrent sessions, nominal aggregate media traffic is about 1.12 Gbps before overhead. With transport headers, jitter buffers, retransmission behavior, telemetry, and control messages added, a planning number closer to 1.4 to 1.6 Gbps is more realistic.

The system must also absorb asymmetry. During a burst of assistant replies, downlink can dominate. During heavy barge-in or noisy environments, uplink processing load rises because more frames need suppression and VAD evaluation. Jitter buffer adds a little latency but prevents choppy speech.

Regional media edges cut one-way delay and reduce backbone traffic by terminating sessions near the user. WebRTC is commonly preferred over request-response APIs because UDP-based delivery tolerates jitter better and avoids head-of-line blocking. Many voice assistants also take calls over phone lines (SIP/PSTN), which carry 8 kHz audio and lower ASR accuracy than wideband WebRTC, so the ASR stack needs a narrowband model.

Voice Assistant Capacity Estimator

Change the workload to see which resource dominates before drawing the architecture.

Peak concurrent sessionsN

sessions

Average utilizationu

%

Average call lengthT

min

Retained sessionsr

%

Sessions speaking at onces

%

Replies per sessionq

per min

Tokens per replyk

tokens

Transport overheado

%

Sessions per dayS

3,600,000sessions

Retained audio per dayA

518.4GB

Transcripts per dayX

8.64GB

Active ASR streamsW

3,750streams

ASR acceleratorsG

37.5units

LLM tokens per minuteK

3,000,000tokens/min

TTS workersV

18.75workers

Nominal bandwidthB

1.12Gbps

Bandwidth with overheadBo​

1.512Gbps

At peak, the system needs about **37.5 ASR accelerators**, **18.75 TTS workers**, and **1.512 Gbps** of media bandwidth. Retained audio adds **518.4 GB** per day.

Do you find this helpful?

The estimator above lets us change the workload and see which resource dominates. The next step is deciding how the system speaks back within the latency budget.

## System design of a real-time voice assistant[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-design-of-a-real-time-voice-assistant)

The end-to-end system starts at the client microphone and ends at the speaker, but the critical path is shorter than the full pipeline because stages overlap. That is the first design instinct interviewers want to hear. The assistant should begin speaking shortly after end-of-user-speech, not after every subsystem fully completes.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#High-level-design)

The major subsystems are client and transport, speech understanding, dialogue orchestration, speech generation, and privacy plus evaluation services. The main architectural fork is between a cascaded pipeline and a speech-to-speech model. In interviews, the cascaded design is usually the default answer because it exposes control points for safety, tool use, debugging, and observability. A speech-to-speech model can reduce stage boundaries and sometimes latency, but it hides intermediate state and makes policy checks harder.

A useful mental model is a relay race in which runners start moving before the baton fully settles. Streaming ASR emits partials, the orchestrator forms intent before final punctuation, the LLM begins decoding once enough context is available, and TTS speaks early clauses before the whole reply finishes.

The diagram below shows the happy path and the cancellation path.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271551%27%20height=%27431%27/%3e)![Voice assistant architecture](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Voice assistant architecture")

Voice assistant architecture

At a high level, the system is session oriented and event driven. A session begins after wake-word detection or explicit connect. The client captures audio and may run acoustic echo cancellation, wake-word detection, and lightweight VAD before sending frames upstream.

The regional media edge terminates the real-time connection, handles packetization, jitter buffering, optional noise suppression, and stream authentication. It forwards normalized audio frames to streaming ASR, which emits partial hypotheses with timestamps and confidence. The session orchestrator consumes those events, maintains turn state, tracks context, launches tools, and issues cancellation when the user interrupts. The LLM generates text or semantic actions, and streaming TTS converts early clauses into audio chunks that return through the media edge to the client.

Privacy services run beside the path rather than inside every model call. They enforce consent, encryption, retention policy, and regional residency. Evaluation services collect metrics such as word error rate, endpointing delay, interruption handling, and first-audio latency.

> **Note:** Stateless HTTP thinking leads candidates astray here. Voice sessions behave more like long-lived connections with shared mutable state than isolated prompts.

The next section maps this architecture to the behaviors users notice.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-functional-requirements)

Natural conversation emerges from continuous bidirectional streaming and explicit turn-state management. The system does not wait for fixed phases like "user done, machine starts." It keeps listening throughout the interaction and adjusts state based on incoming evidence.

The design implements the product requirements through the following mechanisms.

- **Turn-taking:** The client and edge keep VAD active, while endpoint detection combines silence duration with transcript signals to decide when a user likely finished.
- **Barge-in:** During assistant playback, the listening path remains live. Echo cancellation on the client removes the assistant's own voice, and a minimum speech length of about 250 ms filters out sounds like "uh-huh". Only sustained user speech triggers an immediate TTS stop and may also cancel LLM decoding to free compute.
- **Multi-turn context:** The orchestrator stores recent transcript history, tool outputs, and domain memory in session state so the next response conditions on current conversation state.
- **Tool usage:** External API calls stay under the orchestrator, which can fetch account data or schedule appointments without embedding those concerns in ASR or TTS.
- **Speech-to-speech variant:** Even if one model handles audio input and output, the system still needs orchestration for tools, safety checks, and telemetry.

That behavior view leads naturally into a deeper subsystem walk-through.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#A-detailed-system-design)

The high-level picture hides an important implementation detail. In a voice assistant, every module on the critical path must process incrementally and support cancellation. A component that only works on complete inputs turns a conversational system into a delayed batch system.

We will walk the design in modular slices. For each slice, focus on three questions. What state does it own, what events does it emit, and which latency or privacy bottleneck does it remove?

That lens keeps the walk-through concrete. It also makes trade-offs easier to explain when two architectures can both meet the requirement.

### Speech understanding and turn packaging[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-understanding-and-turn-packaging)

In a voice design, this stage packages speech understanding for the dialogue manager rather than building classic text embeddings alone. Streaming ASR produces partial transcripts, timestamps, confidence scores, and speaker timing cues. The packaging service normalizes text, extracts entities, applies safety filters, and emits a compact turn representation the orchestrator can consume quickly.

It also maintains uncertainty. Partial hypotheses can change before finalization, so the representation preserves temporal order and confidence bands instead of pretending the text is settled. A small semantic cache can store the recognized intent for repeated requests such as account balance checks, but never the answer. The answer is always fetched fresh for each user.

That packaged turn then joins session memory and durable user context.

### Session state and memory[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-state-and-memory)

The memory layer splits fast-changing session state from durable user and compliance state. An in-memory session cache holds recent turns, active tool outputs, and interruption markers. Durable stores hold user preferences, consent state, transcript archives, and optional retrieval indexes for domain documents.

Privacy constraints are stricter here than in many text systems. Audio-derived content may reveal health, identity, or location. The storage tier therefore attaches region tags, TTL-based deletion, and redaction lineage to each artifact. Operational metadata stays separate from content data so least-privilege access is easier to enforce.

That separation lets the serving layer move quickly without widening data access.

### Speech generation and moderation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-generation-and-moderation)

The serving tier hosts streaming ASR, LLM, and TTS, or a speech-to-speech alternative. A model router selects the right backend based on region, language, consent, and latency budget. Warm pools reduce cold starts, and autoscaling occurs separately for ASR, generation, and synthesis because their load curves differ.

Moderation checkpoints sit before synthesis, not after playback. Transcript content, tool outputs, and generated text can all be screened before audio leaves the system. Time-to-first-audio becomes the primary serving metric, alongside cancellation latency so interrupted replies release compute quickly.

The next section follows one request through these modules.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Putting-everything-together)

The full path runs as a streaming loop. The client starts a session, the media edge accepts encrypted audio, and ASR emits partials almost immediately. The orchestrator updates turn state and may prefetch likely tools once intent becomes probable. The LLM may start generating from a partial transcript, but if the final transcript differs, the orchestrator cancels that generation and restarts it. TTS starts synthesizing once it receives a stable early clause.

During playback, the client and edge still monitor user speech. If barge-in appears, the orchestrator cancels downstream synthesis and optionally truncates generation. Telemetry stamps every hop so p50 and p95 latency can be attributed to endpointing, ASR finalization, model decode, synthesis startup, or playback buffering.

The diagram below places the three subsystems from the detailed design on this streaming loop, including the barge-in path that cancels generation and synthesis.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271501%27%20height=%27631%27/%3e)![Detailed design of a real-time voice assistant](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a real-time voice assistant")

Detailed design of a real-time voice assistant

The estimator below budgets the first second after the user stops speaking. Adjust each stage to see how overlap and slow stages change time to first audio.

Voice Latency Budget

Adjust each stage to see whether the silence after the user stops speaking stays under one second.

Endpointing delayte​

ms

ASR finalizationta​

ms

Orchestration and toolsto​

ms

LLM time to first tokentl​

ms

TTS first audiots​

ms

Network and playbacktn​

ms

Time to first audioT

950ms

Headroom against 1,000 msH

50ms

The pipeline reaches first audio in **950 ms**, leaving **50 ms** of headroom against the 1,000 ms target.

Do you find this helpful?

With the request path in mind, we can describe the live workflow and the failure states the system must survive.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Workflow-of-the-system)

A production session moves through explicit states rather than hidden flags. Typical states include listening, endpointing, thinking, speaking, interrupted, and recovering. Sticky routing or a dedicated session worker helps because turn state and cancellation need locality.

### Session states[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-states)

The state machine works in small transitions, and each transition changes which downstream work is allowed.

#### Listening and endpointing[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Listening-and-endpointing)

The system accepts audio frames, updates VAD, streams partial ASR, and keeps a short rolling buffer. When endpointing fires, the orchestrator closes the current user turn and triggers generation.

#### Thinking and speaking[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Thinking-and-speaking)

The orchestrator may call tools, the LLM begins decoding, and TTS starts playback on an early stable clause. While speaking, VAD stays active so new user speech can interrupt quickly.

### Unhappy paths[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Unhappy-paths)

Failures should degrade the experience without dead air.

- **Packet loss:** The edge expands buffers slightly, the receiving codec applies packet loss concealment, and the session survives instead of being torn down.
- **ASR confidence collapse:** The orchestrator asks for repetition or confirms a critical entity through speech or text.
- **Tool timeout or TTS failure:** The system falls back to a shorter apology, a simpler voice, or transcript confirmation.

> **Practical tip:** In interviews, explicitly naming the recovery state often separates a strong answer from a happy-path-only answer.

Those workflow choices now connect directly to nonfunctional requirements.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-nonfunctional-requirements)

Performance starts with geography. Regional media edges reduce one-way delay, and streaming across ASR, LLM, and TTS overlaps work instead of serializing it. Warm pools and bounded queues keep p95 stable under bursty demand.

Scalability comes from separate auto-scaling domains. Media edges scale with sessions and bandwidth. ASR scales with active speakers. LLM scales with reply generation rate and token volume. TTS scales with concurrent assistant speech. Availability uses multi-region failover and graceful downgrades so the system can switch to simpler synthesis or transcript confirmation without repeating speech.

Reliability depends on cancellation correctness, back-pressure, and idempotent tool calls. Security and privacy require encrypted transport, consent-aware recording, redaction, minimization of retained audio, and narrow access control. Accuracy under real conditions comes from noise suppression, robust ASR models, and evaluation on representative audio rather than clean lab clips.

|  |  |  |  |
| --- | --- | --- | --- |
| **Aspect** | **Cascaded Pipeline** | **Speech-to-Speech Model** | **Interview-friendly takeaway** |
| **Latency** | Higher due to separate ASR, NLU/LLM, and TTS stages | Lower with more direct end-to-end generation | Speech-to-speech often wins on speed; cascaded trades latency for control |
| **Debuggability** | Strong, since each stage can be inspected independently | Weaker, because errors are harder to localize inside one model | Cascaded is easier to troubleshoot in production |
| **Tool calling** | Easier to insert structured tool use between stages | Possible, but often less explicit and less controllable | Cascaded fits tool-heavy agent workflows better |
| **Privacy control** | Finer control over where transcription, reasoning, and synthesis happen | Less granular if a single model handles the full flow | Cascaded gives more deployment and data-governance flexibility |
| **Observability** | Better metrics at each component boundary | More limited unless the model exposes rich internal signals | Cascaded offers clearer monitoring and SLA tracking |
| **Vendor lock-in** | Lower, since components can be swapped independently | Higher if the end-to-end stack depends on one provider | Cascaded reduces dependence on a single vendor |
| **Cost efficiency** | Can be optimized per stage, but may add orchestration overhead | Can be cheaper operationally if one model replaces multiple services | Best choice depends on scale: cascaded for optimization, end-to-end for simplicity |
| **Suitability for noisy domain workflows** | Better when domain-specific ASR tuning, validation, and fallback logic are needed | Strong for fluid interaction, but may struggle where strict handling is required | Cascaded is usually safer for noisy, high-precision enterprise use cases |

Let's test our understanding of turn-taking and the latency budget with the questions below.

Knowledge Check

Q1. The assistant stops mid-sentence whenever the user says "uh-huh" or the assistant's own voice leaks into the microphone. What is the best fix?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Conclusion)

Real-time voice assistants are distributed, stateful, and unforgiving about latency. A solid interview answer estimates by concurrent sessions, streams every stage, makes barge-in explicit, and treats privacy as part of the data path rather than an afterthought.

The trade-off to articulate clearly is modularity vs. latency, especially when comparing a cascaded streaming design with a speech-to-speech alternative. In the next lesson, we zoom out from one assistant to the platform layer that routes, governs, and observes these model interactions through a GenAI gateway.

Design a Unified Query Engine Across Data Sources

DALL·E

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Storage-estimation)

[Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Compute-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Bandwidth-estimation)

[System design of a real-time voice assistant](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#System-design-of-a-real-time-voice-assistant)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#High-level-design)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#A-detailed-system-design)

[Speech understanding and turn packaging](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-understanding-and-turn-packaging)

[Session state and memory](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-state-and-memory)

[Speech generation and moderation](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Speech-generation-and-moderation)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Workflow-of-the-system)

[Session states](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Session-states)

[Listening and endpointing](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Listening-and-endpointing)

[Thinking and speaking](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Thinking-and-speaking)

[Unhappy paths](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Unhappy-paths)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Achieving-nonfunctional-requirements)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-real-time-voice-assistant#Conclusion)