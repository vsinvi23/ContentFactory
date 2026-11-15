# Grounding_and_Enterprise_Retrieval_in_Google_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Grounding and Enterprise Retrieval

Explore how grounding connects model answers to current, verifiable sources, using either the public web or private enterprise data. Learn to compare managed enterprise search with custom RAG pipelines and to enforce document permissions during retrieval.

We'll cover the following...

- [What grounding means](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#What-grounding-means)
- [Grounding with Google Search](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-with-Google-Search)
- [Grounding on private enterprise data](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-on-private-enterprise-data)
  - [Managed enterprise search](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Managed-enterprise-search)
  - [Custom RAG pipelines](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Custom-RAG-pipelines)
- [Choice between managed search and custom RAG](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Choice-between-managed-search-and-custom-RAG)
- [Common retrieval mistakes](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Common-retrieval-mistakes)

A Gemini model knows a great deal, but it does not know what happened after its training data was collected, and it has never seen a customer’s internal documents, contracts, product catalog, or policies. When an enterprise agent answers a question without access to the right information, it may produce a confident answer that is outdated or simply wrong. In a customer deployment, one incorrect answer about a refund policy or a contract term can undermine trust in the entire system.

Grounding addresses this problem by connecting the model’s answer to a specific source of information at the time of the request. For an FDE, the core decisions are which source to ground on and how to build the retrieval behind it. Interviewers expect candidates to distinguish public web grounding from private enterprise data, and to explain when a managed search service is enough and when a custom retrieval pipeline is justified.

## What grounding means[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#What-grounding-means)

Grounding is the practice of supplying a model with relevant, verifiable information when it generates an answer, and linking the answer back to that information. A grounded answer has two properties that an ungrounded answer lacks. It is based on current, specific content rather than only on what the model learned during training, and it can be traced to a source, which allows users and reviewers to verify it.

Enterprise grounding usually draws on one of two kinds of sources.

|  |  |  |
| --- | --- | --- |
| Source | What it covers | Typical use |
| Public web | Current, publicly available information | News, regulations, public product information, market data |
| Private enterprise data | The customer’s own documents and records | Policies, contracts, manuals, support tickets, internal knowledge |

Many systems use both. A telecom support agent might ground on the company’s internal plan catalog for pricing questions and on the public web for questions about a newly announced industry regulation. The sources are kept separate so that the system knows which kind of evidence supports each answer.

## Grounding with Google Search[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-with-Google-Search)

Grounding with Google Search lets Gemini run web searches during a request and base its answer on the results. The model decides when a search is needed, generates the search queries, and returns an answer along with metadata that links parts of the answer to specific web sources.

Python 3.14.0

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

13

from google import genai

from google.genai import types

client = genai.Client()

response = client.models.generate\_content(

model=MODEL\_ID,

contents="What changes to EU mobile roaming rules were announced this year?",

config=types.GenerateContentConfig(

tools=[types.Tool(google\_search=types.GoogleSearch())],

),

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

⋯

- **Line 8:** The question depends on recent events, which the model’s training data may not cover.
- **Line 10:** Adding the `GoogleSearch` tool allows the model to search the web during the request. The model decides whether a search is needed.
- **Line 14:** `response.text` contains the answer, written from the search results.
- **Line 16:** `grounding_metadata` holds the details of how the answer was grounded.
- **Line 17:** `web_search_queries` shows the queries the model ran, which is useful for debugging unexpected answers.
- **Lines 18–19:** `grounding_chunks` lists the web sources used. The application can display these as citations so users can verify the answer.

The metadata also includes grounding supports, which map specific segments of the answer to the sources that support them. Applications use this to place inline citations next to the relevant sentences.

Grounding with Google Search has its own usage terms, including requirements for how search suggestions and sources are displayed to end users. These should be reviewed with the customer before the feature appears in a user-facing product.

Public web grounding does not help with a customer’s internal documents. For those, the system needs enterprise retrieval.

## Grounding on private enterprise data[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-on-private-enterprise-data)

Private data is where most enterprise value lies, and also where most of the difficulty lies. Documents are spread across systems such as Google Drive, SharePoint, Cloud Storage, and internal databases. They come in many formats, contain outdated and conflicting versions, and carry access restrictions that must be respected. A support agent that retrieves a confidential HR document for the wrong employee creates a serious incident, even if the answer is technically accurate.

There are two main approaches to retrieval over private data: a managed enterprise search service or a custom retrieval-augmented generation (RAG) pipeline.

### Managed enterprise search[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Managed-enterprise-search)

Google’s managed enterprise search service, Vertex AI Search, handles document ingestion, parsing, chunking, indexing, and ranking as a service. Data is connected through built-in connectors or uploaded to a data store, and Gemini can ground its answers directly on that data store.

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

from google import genai

from google.genai import types

client = genai.Client(vertexai=True, project="PROJECT\_ID", location="global")

DATASTORE = (

"projects/PROJECT\_ID/locations/global/collections/default\_collection/"

"dataStores/hr-policies"

)

response = client.models.generate\_content(

model=MODEL\_ID,

contents="How many days of parental leave do employees in Germany receive?",

config=types.GenerateContentConfig(

tools=[types.Tool(retrieval=types.Retrieval(

vertex\_ai\_search=types.VertexAISearch(datastore=DATASTORE)

))],

),

)

print(response.text)

for chunk in response.candidates[0].grounding\_metadata.grounding\_chunks:

print("Source:", chunk.retrieved\_context.title, chunk.retrieved\_context.uri)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 4:** The client connects through the customer’s Google Cloud project, so the project’s IAM, networking, and data controls apply.
- **Lines 6–9:** `DATASTORE` is the full resource name of the data store that holds the indexed HR policy documents.
- **Line 13:** The question requires private, company-specific information that no public source would contain.
- **Lines 15–17:** The `Retrieval` tool points Gemini at the data store. The service retrieves relevant passages, and the model writes its answer from them.
- **Line 21:** The answer is based on the retrieved policy content rather than on the model’s general knowledge.
- **Lines 22–23:** Each grounding chunk includes a `retrieved_context` with the source document’s title and URI, which the application can show as citations.

The managed approach gets a pilot running quickly and moves maintenance of the retrieval system to Google. It suits document collections in common formats where standard relevance ranking works well.

### Custom RAG pipelines[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Custom-RAG-pipelines)

A custom RAG pipeline gives the FDE team full control over each step of retrieval. It is built from a series of components that the team designs, operates, and tunes.

|  |  |  |
| --- | --- | --- |
| Ingest and parse | Extract text and structure from source documents | Document AI, custom parsers |
| Chunk | Split documents into passages sized for retrieval | Custom logic based on headings, tables, or clauses |
| Embed | Convert passages into vectors that capture meaning | Gemini embedding models |
| Store and retrieve | Index vectors and find the closest matches | AlloyDB with pgvector, BigQuery vector search, Vector Search |
| Rerank | Reorder results by relevance to the question | Ranking API, a model-based reranker |
| Generate | Answer from the retrieved passages, with citations | Gemini with a grounding prompt |

Each step is a place where quality can be improved, and also a place where it can fail. Chunking that splits a table in half, embeddings that miss domain-specific terms, or a retrieval step that returns outdated document versions will all degrade answers, regardless of how capable the generation model is.

## Choice between managed search and custom RAG[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Choice-between-managed-search-and-custom-RAG)

The choice depends on the customer’s data, quality requirements, and operating capacity.

|  |  |  |
| --- | --- | --- |
| Time to first result | Days | Weeks |
| Control over chunking and ranking | Limited | Full |
| Specialized document structures | Standard handling | Custom parsing for contracts, tables, or code |
| Data that lives in databases | Possible with connectors | Direct integration with existing stores |
| Operational burden | Low | High, owned by the customer or FDE team |
| Best fit | Pilots and standard document collections | Specialized content, strict quality targets, existing vector infrastructure |

A practical FDE approach is to start with managed search for the first release, build an evaluation set of real questions with known correct answers, and measure retrieval quality. If the evaluation shows that specific failures, such as poorly parsed tables or missed domain terms, cannot be fixed through configuration, the team moves those parts to a custom pipeline. This path ties the added complexity to measured gaps rather than assumptions.

In interviews, a strong retrieval answer covers access control. Retrieval should respect the source documents’ permissions, so a user only receives passages they are allowed to read. Filtering by the user’s identity at retrieval time is safer than filtering the model’s answer afterward.

## Common retrieval mistakes[#](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Common-retrieval-mistakes)

Several mistakes recur in enterprise deployments. The first is blaming the model for poor answers when the real problem is retrieval: the correct passage was never retrieved, so the model could not use it. The second is indexing every document without cleanup, which mixes outdated and conflicting versions into the results. The third is ignoring document permissions, which can expose restricted content through an otherwise correct answer. The last is evaluating only the final answer. Measuring whether the right passages were retrieved, separately from whether the answer was correct, shows which part of the system needs attention.

Grounding turns a general-purpose model into a system that can answer from current, specific, and verifiable information. Grounding with Google Search handles public, time-sensitive questions, while managed enterprise search and custom RAG pipelines handle the customer’s private data. Strong FDE designs choose the source deliberately, start with the simplest retrieval approach that meets the quality target, enforce document permissions at retrieval time, and measure retrieval quality separately so that each improvement is based on evidence.

A2A and Multi-Agent Design

BigQuery and Text-to-SQL

Ask

[What grounding means](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#What-grounding-means)

[Grounding with Google Search](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-with-Google-Search)

[Grounding on private enterprise data](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Grounding-on-private-enterprise-data)

[Managed enterprise search](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Managed-enterprise-search)

[Custom RAG pipelines](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Custom-RAG-pipelines)

[Choice between managed search and custom RAG](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Choice-between-managed-search-and-custom-RAG)

[Common retrieval mistakes](https://www.educative.io/courses/forward-deployed-engineer/grounding-and-enterprise-retrieval#Common-retrieval-mistakes)