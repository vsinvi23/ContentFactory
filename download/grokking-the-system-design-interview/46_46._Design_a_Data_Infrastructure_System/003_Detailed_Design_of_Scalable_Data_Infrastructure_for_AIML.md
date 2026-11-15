# Detailed_Design_of_Scalable_Data_Infrastructure_for_AIML

Source: https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Detailed Design of Scalable Data Infrastructure for AI/ML

The detailed design of a scalable data infrastructure for AI/ML encompasses five key layers: data ingestion, storage, processing, feature store, and model serving. The ingestion layer handles real-time events and batch data, ensuring reliable delivery and schema compatibility. The storage layer utilizes low-cost object storage for raw data and a metadata catalog for organization. The processing layer employs distributed frameworks for ETL, ensuring data quality and lineage. The feature store provides a unified repository for machine learning features, while the model serving layer supports both low-latency online inference and high-throughput batch serving, facilitating efficient model deployment and operation.

We'll cover the following...

- [1. Data ingestion layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#1-Data-ingestion-layer)
- [2. Data storage layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#2-Data-storage-layer)
- [3. Data processing layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#3-Data-processing-layer)
- [4. Feature store layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#4-Feature-store-layer)
- [5. Model serving and access layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#5-Model-serving-and-access-layer)
- [Putting it all together](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Putting-it-all-together)
- [Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Requirements-compliance)
  - [Achieving functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-functional-requirements)
  - [Achieving non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-non-functional-requirements)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Conclusion)

This lesson details the five layers of the data infrastructure: ingestion, storage, processing, feature store, and model serving. We will examine their internal components, technology choices, and design considerations.

## 1. Data ingestion layer[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#1-Data-ingestion-layer)

The data ingestion layer handles two primary data categories using dedicated services:

- **Real-time events:** High-velocity events (e.g., clicks, payments) are published to a distributed message queue like Apache Kafka. A stream processing engine (Apache Flink or Spark Structured Streaming) consumes, validates, and enriches these events before writing them to object storage. This supports real-time features and analytics.
- **Batch data:** Large-volume data (e.g., database snapshots) arrives at scheduled intervals. A workflow orchestrator, such as Apache Airflow, manages the extraction, cleaning, and formatting of this data before loading it into the raw zone of the object storage. This ensures consistent datasets for training.

![Dual ingestion paths for real-time streams (Kafka/Flink) and scheduled batches (orchestrated by Airflow)](003_Detailed_Design_of_Scalable_Data_Infrastructure_for_AIML_images/img_adf9e22c025d.svg "Dual ingestion paths for real-time streams (Kafka/Flink) and scheduled batches (orchestrated by Airflow)")

Dual ingestion paths for real-time streams (Kafka/Flink) and scheduled batches (orchestrated by Airflow)

Both ingestion paths must ensure reliable delivery and schema compatibility. Tools like Confluent Schema Registry or validation libraries in Airflow prevent schema changes from breaking downstream systems.

To support lineage and debugging, all ingested data is tagged with metadata (e.g., timestamps, Kafka offsets, batch IDs). This ensures that both event streams and batch imports provide a dependable foundation for downstream processing.

Once data is reliably ingested, it must be durably stored and cataloged in the data storage layer.

## 2. Data storage layer[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#2-Data-storage-layer)

The data storage layer provides a scalable foundation for all ingested data. Incoming data lands in the raw zone of the data lake, typically hosted on low-cost object storage (e.g., Amazon S3, GCS). This zone preserves data in its original form, supporting schema-on-read flexibility.

Cleaned datasets move to processed zones, which use modern table formats to support [ACID transactions](https://www.educative.io/answers/what-are-acid-properties-in-a-database), time travel, and schema evolution. For fast SQL analytics and BI dashboards, the system leverages a high-performance data warehouse like BigQuery or Redshift.

![The data storage layer, showing the raw/processed zones in the data lake and the central metadata catalog](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The data storage layer, showing the raw/processed zones in the data lake and the central metadata catalog")

The data storage layer, showing the raw/processed zones in the data lake and the central metadata catalog

A central metadata catalog, such as BigQuery Metastore, manages metadata across this multi-layered architecture. It stores schemas, table definitions, and version histories across both the data lake and the warehouse. This provides a unified view of datasets, which simplifies governance and maintains compatibility across pipelines.

With the storage foundation in place, the next step is to transform raw data into useful assets through the data processing layer.

## 3. Data processing layer[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#3-Data-processing-layer)

Once data lands in the raw zone of the storage layer, distributed processing frameworks handle large-scale ETL workloads. Spark processes these workloads by partitioning massive datasets across a cluster of worker nodes, enabling parallel in-memory execution. It automatically manages the complexity of data shuffling for aggregations and joins, while its DAG scheduler optimizes execution plans and ensures fault tolerance by recomputing lost partitions if a node fails.

In parallel, SQL-centric transformations that occur directly within the data warehouse are managed using dbt, which provides modular modeling, version-controlled transformations, and lineage-aware execution. Both Spark and dbt pipelines rely on the workflow orchestrator to manage job scheduling, dependencies, retries, and alerting, ensuring that processing tasks run consistently and reproducibly across different environments.

![The data processing layer, showing Airflow orchestrating both ETL (Spark) and ELT (dbt) workflows](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The data processing layer, showing Airflow orchestrating both ETL (Spark) and ELT (dbt) workflows")

The data processing layer, showing Airflow orchestrating both ETL (Spark) and ELT (dbt) workflows

To guarantee data quality, the infrastructure embeds Great Expectations (GX) within pipelines. Every dataset is validated against explicit rules (e.g., schema checks and uniqueness constraints) before being propagated downstream. Intermediate outputs and quality metrics are stored for auditability.

**Note:** By combining distributed compute (Spark), warehouse-native modeling (dbt), centralized orchestration (Airflow), and continuous quality enforcement (Great Expectations), the system transforms raw inputs into trustworthy, analysis-ready datasets.

After transformation into features, the system requires a specialized layer for storage and serving.

## 4. Feature store layer[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#4-Feature-store-layer)

The feature store layer provides a unified repository for machine learning features, ensuring consistency between training and inference.

The feature registry serves as a central catalog, maintaining metadata such as schemas, owners, and version history. This allows teams to discover and reuse features. Behind the registry, the feature store uses a dual-storage architecture.

The offline store (e.g., BigQuery or Parquet/Delta tables) stores complete historical feature values. This enables point-in-time accurate training data generation and time-travel queries.

![The feature store's dual-store architecture, separating the offline store (for training) from the online store](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The feature store's dual-store architecture, separating the offline store (for training) from the online store")

The feature store's dual-store architecture, separating the offline store (for training) from the online store

The online store is a low-latency key-value database (e.g., Redis, DynamoDB, Cassandra) that provides immediate access to the most recent feature values for real-time inference.

To maintain consistency, a single feature computation pipeline, powered by tools like Feast, writes to both stores using the same logic. This prevents training-serving skew, ensuring features behave identically in both environments.

By combining a central registry, historical offline storage, low-latency online retrieval, and unified feature workflows, the feature store layer enables reliable, reproducible, and scalable feature management across the entire ML life cycle. A critical capability here is preventing data leakage, a common issue where models fail in production because they were inadvertently trained on future data

Finally, the model serving and access layer connects these features to models and data scientists.

## 5. Model serving and access layer[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#5-Model-serving-and-access-layer)

This layer acts as the interface for retrieving data, supporting two distinct access patterns:

- **Online serving** isoptimized for speed. Deployed models fetch the latest feature values from the online store via low-latency APIs (gRPC or REST) to generate real-time predictions. This path supports applications like fraud detection and personalization.

![The two access patterns, low-latency online serving for inference and high-throughput batch serving for training](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The two access patterns, low-latency online serving for inference and high-throughput batch serving for training")

The two access patterns, low-latency online serving for inference and high-throughput batch serving for training

For a deeper understanding of how scalable, production-ready AI applications are designed, [Grokking the Generative AI System Design](https://www.educative.io/courses/generative-ai-system-design) offers a comprehensive perspective.

- **Batch serving** is optimized for high throughput and offline access. Data scientists use this path to export full training datasets or run feature backfills from the offline store. This supports massive reads without impacting real-time inference latency.

Separating these access patterns ensures that real-time systems and offline training pipelines operate efficiently without interference.

AI Powered

Saved

1 attempt left

Reset

Training-serving skew problem

In the detailed design of the scalable data infrastructure, how do the data storage layer and feature store layer work together to address the “training-serving skew” problem?

This is your last attempt.

With the layers defined, we can now examine the complete end-to-end workflow.

## Putting it all together[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Putting-it-all-together)

The following diagram and workflow illustrate how these five layers function as a cohesive system.

![End-to-end workflow of the scalable ML data infrastructure, from ingestion to serving](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "End-to-end workflow of the scalable ML data infrastructure, from ingestion to serving")

End-to-end workflow of the scalable ML data infrastructure, from ingestion to serving

1. **Ingestion:** Real-time data flows into the message queue (Apache Kafka), is processed by the stream processor, utilizing a schema registry for validation, and written to the raw zone of the data lake. Batch data is handled by an ingestion job orchestrated by the orchestrator, which extracts, transforms, and loads it into the raw zone.
2. **Processing and orchestration:** The central orchestrator triggers downstream jobs. It triggers an Apache Spark job to process data from the raw zone. Spark writes clean data to the processed zone and performs ETL to load data into the data warehouse. Raw data may be loaded directly into the data warehouse for ELT processing. The metadata catalog discovers schemas from the processed zone and registers tables from the data warehouse.
3. **Feature computation:** The Spark job feeds into a feature computation pipeline. This pipeline calculates ML features and writes them to both the offline storage (for training) and the online storage (for inference). It also registers feature definitions with the feature registry.
4. **Offline serving (training):** The orchestrator triggers a scheduled retraining job. The model training process uses the batch access API to read historical feature data from the offline store.
5. **Online serving (inference):** A user request travels through a CDN and load balancer to the deployed model (gRPC/REST API). The API fetches the latest feature values from the online storage to generate a real-time prediction.

Now, let’s confirm how this design satisfies our initial requirements.

## Requirements compliance[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Requirements-compliance)

We will review how this detailed design meets the functional and non-functional requirements defined earlier.

### Achieving functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-functional-requirements)

The following section maps our design decisions to the system’s specific functional needs.

|  |  |
| --- | --- |
| **Requirement** | **How It’s Achieved in the Design** |
| **Data collection** | The data ingestion layer, consisting of various services, is responsible for data collection from various sources. |
| **Data processing** | The data processing layer and the associated services process and transform raw data. |
| **Batch and real-time** | Apache Kafka and the stream processors handle the real-time data while the batch ingestion pipeline handles batch data. |
| **Data storage** | The data storage layer uses object storage and columnar formats for efficiency. |
| **Serving data to models** | The feature store provides versioned features for both training and inference. |
| **Data monitoring and lineage** | For monitoring, data validation tools are integrated into the processing layer, while metadata catalogs track lineage. |

### Achieving non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-non-functional-requirements)

A robust data infrastructure must be reliable, scalable, and secure. The table below summarizes how the design addresses these critical non-functional requirements.

|  |  |
| --- | --- |
| **Requirement** | **How It’s Achieved in the Design** |
| **Reliability** | Reliability is guaranteed through acknowledgment mechanisms in ingestion, atomic commit protocols for data lake transactions, and automatic retries with replication for fault tolerance. |
| **Security and privacy** | Data is encrypted at rest and in transit, with access controls enforced at multiple levels. |
| **Scalability** | The architecture relies on horizontally scalable components, including object storage, event streaming platforms, and distributed compute frameworks, allowing the system to grow by adding nodes. |
| **Performance** | High performance is achieved by minimizing I/O through columnar storage, reducing data scanning via partitioning, and parallelizing computations across distributed nodes. |
| **Low latency** | The online feature store (Redis/DynamoDB) and gRPC serving APIs are designed for low-latency serving. |

We have explored the non-functional requirements and the techniques used to achieve them. Let’s test your understanding with a quiz.

Test your knowledge!

1.

A model’s performance drops in production. You find that the `avg_spend_30d` feature is being calculated by two different services: the main Spark (ETL) job and a separate, older Flink (streaming) job. This causes two different values for the same feature. What fundamental component of our design was bypassed or ignored, leading to this training-serving skew?

A.

The metadata catalog

B.

The data validation (Great Expectations) tool

C.

The feature store

D.

The data warehouse

---

1 / 3

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Conclusion)

In this lesson, we detailed the System Design of a scalable ML data infrastructure. By assigning clear responsibilities to the ingestion, storage, processing, feature store, and serving layers, we created an architecture that efficiently handles both batch and real-time workloads. This design addresses challenges, such as training-serving skew and feature reuse, providing a solid foundation for deploying models at scale.

High-Level Design of Scalable Data Infrastructure for AI/ML

System Design: LLM-Powered Customer Support Bot

Ask

[1. Data ingestion layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#1-Data-ingestion-layer)

[2. Data storage layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#2-Data-storage-layer)

[3. Data processing layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#3-Data-processing-layer)

[4. Feature store layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#4-Feature-store-layer)

[5. Model serving and access layer](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#5-Model-serving-and-access-layer)

[Putting it all together](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Putting-it-all-together)

[Requirements compliance](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Requirements-compliance)

[Achieving functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-functional-requirements)

[Achieving non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Achieving-non-functional-requirements)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/detailed-design-of-scalable-data-infrastructure-for-ai-ml#Conclusion)