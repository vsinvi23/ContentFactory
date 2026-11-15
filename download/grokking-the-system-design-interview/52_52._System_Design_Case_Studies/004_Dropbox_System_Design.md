# Dropbox_System_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Dropbox System Design

Dropbox is a cloud-based file storage and synchronization service that enables users to store, share, and collaborate on files across devices. It employs a robust architecture that includes a metadata service, chunk service, and synchronization service to manage file uploads, downloads, and real-time updates. Key design considerations include functional requirements like user authentication, version control, and security measures such as AES-256 encryption. The system is designed for scalability, with resource estimations for storage and bandwidth based on projected user activity, ensuring high availability and efficient performance through techniques like data deduplication and adaptive bandwidth control.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Requirements)
- [Resource estimation for Dropbox architecture](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Resource-estimation-for-Dropbox-architecture)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Bandwidth-estimation)
  - [Server estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Server-estimation)
- [High-level design of Dropbox](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#High-level-design-of-Dropbox)
- [Detailed design of Dropbox](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Detailed-design-of-Dropbox)
  - [File upload and download](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-upload-and-download)
  - [File sharing](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-sharing)
  - [User authentication and access control](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#User-authentication-and-access-control)
  - [File synchronization](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-synchronization)
  - [Data storage and replication](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Data-storage-and-replication)
  - [Version control and conflict resolution](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Version-control-and-conflict-resolution)
  - [Security mechanisms](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Security-mechanisms)
- [Putting everything together](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Putting-everything-together)
- [Performance optimization](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Performance-optimization)
- [Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Conclusion)

Dropbox is a cloud-based file storage and synchronization service that allows users to store, share, and collaborate on files across multiple devices.

When a file is added or modified in a Dropbox folder, the system ensures that all connected devices and collaborators have access to the most up-to-date version. This requires efficient storage, synchronization, and metadata management, as well as secure authentication and access control.

Dropbox is one of several cloud storage and collaboration tools available today, alongside:

- Google Drive
- Microsoft OneDrive
- Box
- Jupyter

As of November 2023, Google Drive held the largest market share in cloud storage, with Dropbox in second place. Dropbox’s continued adoption demonstrates its focus on reliable synchronization, simplicity, and scalability, particularly for collaborative workflows.

The market share of top 5 file synchronization and sharing services

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Requirements)

Defining requirements is a crucial first step in designing a system like Dropbox. Requirements are typically categorized as either functional or nonfunctional, providing a clear scope for the design process.

**Functional requirements**

- Upload files
- Download files
- Share files/directory
- Create and delete directories
- Synchronization upon file changes
- Version control for files
- User authentication and access control

**Nonfunctional requirements**

- Durability and reliability
- Availability
- Scalability
- Security
- Low-latency file retrieval

Clarifying requirements is also essential in System Design interviews, as it demonstrates a structured approach to understanding the problem scope. For example, distinguishing between functional and nonfunctional requirements guides both the back-end architecture and the front-end design.

After requirements are established, it is necessary to estimate the system resources required to support expected user activity. This includes determining storage, bandwidth, and server capacity.

## Resource estimation for Dropbox architecture[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Resource-estimation-for-Dropbox-architecture)

Resource estimation involves calculating storage, bandwidth, and server requirements based on projected user activity. For this analysis, assume Dropbox has 50 million paying users.

> **Note:** According to Backlinko, Dropbox had approximately 18.22 million paying users as of Q2 2024. Designing for 50 million users allows planning for future growth.

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Storage-estimation)

If each user is allocated 2 TB of storage, the total storage requirement is calculated as:

Total storage=Number of users×2 TB=50 M×2 TB=100,000 PB\begin{align\*}
\text{Total storage} &= \text{Number of users} \times 2 \text{ TB}
\\
&= 50 \text{ M} \times 2 \text{ TB}
\\
&= \text{100,000 PB}
\end{align\*}Total storage​=Number of users×2 TB=50 M×2 TB=100,000 PB​

Thus, the system would require approximately 100,000 petabytes of storage to accommodate 50 million users.

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Bandwidth-estimation)

Assuming that each user consumes 1 GB of bandwidth per day, the total bandwidth requirement can be estimated as:

Total bandwidth=50 M×1 GB=50 EBday=50 EB24×60×60=579 GBps=579 GBps8≈72.5 Gbps\begin{align\*}
\text{Total bandwidth} &= \text{50 M} \times 1 \text{ GB} \\ \\
&=\frac{50 \text{ EB}}{\text{day}} \\\\ & = \frac{50 \text{ EB}}{24\times60\times60} \\ \\ &=579 \text{ GBps} \\ \\
&= \frac{579 \text{ GBps}}{8} \\
\\ & \approx 72.5 \text{ Gbps}
\end{align\*}
Total bandwidth​=50 M×1 GB=day50 EB​=24×60×6050 EB​=579 GBps=8579 GBps​≈72.5 Gbps​

This calculation provides a baseline for network infrastructure to support daily user operations.

### Server estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Server-estimation)

To estimate server requirements, first calculate the queries per second (QPS). Assuming each active user sends 5 requests per minute:

QPS=50 M×5 requests60=4.2 M\text{QPS} = \frac{50 \text{ M} \times 5 \text{ requests}}{60} = 4.2 \text{ M}QPS=6050 M×5 requests​=4.2 M

> **Note:** According to the [back-of-the-envelope estimations](https://www.educative.io/blog/back-of-envelope-estimation-system-design-interview), a 64-core server executes approximately 64000 requests per second.

Considering that a 64-core server can handle approximately 64,000 requests per second, the required number of servers is:

Number of servers=4.2 M64000≈66 servers\text{Number of servers} = \frac{4.2 \text{ M}}{64000} \approx 66 \text{ servers}Number of servers=640004.2 M​≈66 servers

So, to summarize, for 50 M users, the following is the estimation for different resources:

- Estimated storage = 100 EB100 \text{ EB}100 EB
- Estimated bandwidth = 72.5 Gbps72.5 \textrm{ Gbps}72.5 Gbps
- QPS = 4.2 M4.2\text{ M}4.2 M
- The number of servers = 66 servers66 \text{ servers}66 servers

You can estimate these resources for different numbers of users in this calculator:

#### 

|  |  |  |
| --- | --- | --- |
| The number of users | 50 | Million |
| Average storage assigned to each user | 2 | TB |
| Total estimated storage required | f100000 | PB |
| Average daily usage of each user | 1 | GB |
| Total bandwidth | f72.34 | Gb/s |
| Requests a users sends per minute | 5 | Requests |
| QPS | f4.2 | Million |
| The total number of servers | f66 | Servers |

These estimations provide a foundation for designing storage, networking, and server infrastructure to support anticipated user demand.

## High-level design of Dropbox[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#High-level-design-of-Dropbox)

The high-level architecture of Dropbox consists of multiple interacting components and services that manage file storage, metadata, synchronization, and access control. Key components include:

- **Metadata service:** Maintains information about files, directories, and user activity.
- **Chunk service (chunker):** Responsible for splitting files into chunks and handling their storage and retrieval from cloud storage.
- **Metadata database:** Stores metadata, including file paths, versions, ownership, and access permissions.
- **Cloud storage:** Provides scalable, distributed storage for encrypted file chunks.
- **Synchronization service:** Coordinates file updates across multiple devices, ensuring consistency and notifying collaborators of changes.

The overall system ensures that when a user uploads or modifies a file, the metadata service, chunk service, and synchronization service collaborate to update cloud storage and propagate changes to all devices associated with the user's account.

Replication and redundancy mechanisms ensure high availability and durability.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27780%27%20height=%27381%27/%3e)![A high-level design of Dropbox system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A high-level design of Dropbox system")

A high-level design of Dropbox system

This high-level view provides a foundation for the detailed design, where each functional requirement is mapped to specific components and interactions.

## Detailed design of Dropbox[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Detailed-design-of-Dropbox)

Let’s dive into Dropbox’s detailed System Design by starting with each functional requirement. We’ll discuss how to achieve each functionality step by step and the architectural changes necessary to support it.

### File upload and download[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-upload-and-download)

The upload process begins when a user places a file in the client application’s Dropbox folder. The file is divided into smaller chunks, typically 4 MB each. Each chunk is hashed using SHA-256 to produce a unique identifier and encrypted with AES-256 before storage. The encrypted chunks are distributed across multiple servers to ensure high availability.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27551%27%20height=%27301%27/%3e)![The process of dividing a file into chunks and then computing hashes](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The process of dividing a file into chunks and then computing hashes")

The process of dividing a file into chunks and then computing hashes

The client application coordinates with the chunk server, synchronization service, and cloud storage to manage uploads, downloads, and synchronization. During downloads, encrypted chunks are retrieved, decrypted locally, and reassembled. Caching and compression techniques are used to enhance transfer speeds and minimize server load.

The following pseudo-code shows the chunking process and computing their SHA-256:

MySQL

```
IMPORT SHA256 from cryptography library

FUNCTION create_file_chunks_with_hash(file_path, chunk_size):

INITIALIZE empty list called 'chunks'

INITIALIZE empty list called 'hashes'

OPEN file at file_path in binary read mode

SET file_position to 0

WHILE file_position is less than file size:

READ next chunk of chunk_size bytes from file

APPEND the chunk to 'chunks'

COMPUTE hash of the chunk using SHA256

APPEND the hash to 'hashes'

INCREMENT file_position by chunk_size

CLOSE file

RETURN 'chunks', 'hashes'
```

⋯

Pseudo code for creating chunks and computing their hashes using SHA-256

> **Explanation of the above pseudo-code:**
>
> - **Line 1:** Load the SHA256 library.
> - **Lines 3–20:** Define a function that takes two parameters as input: the file path and the chunk size. This function returns a list of chunks and their hashes.
> - **Lines 7–17:** Open a file located at `file_path` for reading in binary mode, and the `file_position` is set to 0 to ensure that the entire file is processed chunk by chunk. Next, the file is read chunk-wise using a loop, and each chunk is appended to a list. Also, the SHA-256 hash is computed for each chunk and appended to the hash list.
> - **Lines 19–20:** Once the file is read, it is closed, and the lists of chunks and hashes are returned.

The chunk server validates each chunk by comparing its hash to existing entries. If a chunk already exists, it is not stored again. During downloads, chunks are retrieved and reassembled before delivery to the client.

### File sharing[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-sharing)

When a user shares a file or folder, the sharing service generates a unique link or sends invitations to designated collaborators. The service enforces permissions such as *read-only* or *can edit* to control the level of access granted to each participant. All associated metadata, including ownership details, access control lists (ACLs), creation and modification timestamps, and permission settings, is stored and managed within the metadata service.

### User authentication and access control[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#User-authentication-and-access-control)

In a system like Dropbox, user authentication and access control are crucial to ensuring that only authorized users can access files and perform specific actions. These tasks are managed through several components, including the authentication server, authorization server, and access control mechanisms.

- **Authentication:** Supports username/password, OAuth 2.0, and multi-factor authentication (MFA). MFA adds a verification layer, such as a one-time password.
- **Authorization:** Manages access based on role-based access control (RBAC), assigning permissions according to user roles (e.g., owner, editor, viewer).

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27567%27%20height=%27268%27/%3e)![Access control in Dropbox](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Access control in Dropbox")

Access control in Dropbox

Additionally, the access control list (ACL) tracks the permissions assigned to each user or group for specific files and folders, ensuring that only authorized users can view, edit, or share content.

### File synchronization[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-synchronization)

File synchronization in the system involves the interaction of different components, including the Dropbox client, metadata service, chunk service, and synchronization service.

The client’s responsibility is to monitor changes in local files for changes and sync them to the cloud, communicating with the aforementioned services. In the file syncing process, the primary actor is the sync engine, a process that runs locally on the user’s device.

It breaks files into chunks, computes hashes, detects changes, and initiates the upload process.

It is necessary to remember the distinction between a sync engine and a synchronization service. The synchronization service sits between the user’s device and backend storage. It ensures that changes made on one device are reflected across all devices linked to the same account and are visible to the file’s collaborators.

For file synchronization, a *block-level sync algorithm* can be used to improve efficiency.

This method divides large files into smaller chunks, which improves upload and download efficiency. When a file is modified, the client computes hashes for each chunk and compares them with the hashes stored on the chunk server. The client uploads only the chunks whose content has changed.

During download, the client retrieves just the updated chunks and then reassembles the file locally.

This approach reduces data transfer and improves performance for large files, such as video assets or database backups, where partial changes would otherwise require reuploading the entire file. The illustration below shows how only the modified chunk is uploaded to cloud storage.

The synchronization service then sends both the update and a corresponding notification to collaborators through the pub/sub (publisher/subscriber) system.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27832%27%20height=%27335%27/%3e)![The modified chunk is uploaded to the cloud storage and sent to other clients via pub/sub system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The modified chunk is uploaded to the cloud storage and sent to other clients via pub/sub system")

The modified chunk is uploaded to the cloud storage and sent to other clients via pub/sub system

When it comes to handling large files and network interruptions, the block-level sync algorithm provides resilience and efficiency.

For large files, the client can upload or download chunks independently, meaning if there’s a network interruption, the sync engine can resume from the last successfully uploaded or downloaded chunk rather than restarting the entire process.

This chunked approach is critical for users on unreliable networks or with bandwidth constraints. Dropbox also uses delta synchronization, ensuring that only modified chunks are synced, further optimizing the process.

> **Note:** Dropbox uses an indexer to manage and search the stored files metadata, enabling quick retrieval and synchronization across devices.

1.

When designing Dropbox’s clients, which protocols or techniques should be used to efficiently monitor changes made by other clients?

Show Answer

Did you find this helpful?

### Data storage and replication[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Data-storage-and-replication)

In Dropbox, data storage involves dividing files into smaller segments, or chunks, which are distributed across multiple storage servers for efficiency and scalability.

Metadata is maintained separately to record the location and identifiers of these chunks, allowing for fast lookup and retrieval. Each chunk is encrypted before storage to ensure data confidentiality. Dropbox replicates data chunks across multiple data centers to provide durability and high availability.

This replication provides redundancy and supports disaster recovery.

If one data center becomes unavailable due to hardware failure or network issues, data can still be retrieved from another without interrupting service. While replication strengthens fault tolerance, it also introduces challenges. The system must provide low-latency access for users worldwide, manage eventual consistency across replicas, and address the operational complexity and costs associated with managing data across geographically distributed servers.

### Version control and conflict resolution[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Version-control-and-conflict-resolution)

Dropbox allows multiple users to edit a document simultaneously, making version control and conflict resolution essential. The metadata server tracks file versions, storing previous copies for rollback if needed.

A simple strategy is last-write-wins, where the most recent upload overwrites earlier changes. To prevent data loss, Dropbox can create conflicted copies for simultaneous edits, appending timestamps or usernames to distinguish versions. For text-based files, merge strategies can automatically combine non-conflicting changes, though complex conflicts may still require manual resolution.

From a user perspective, the system notifies users of conflicts via the pub/sub system, allowing them to view and compare versions. The interface supports intuitive resolution, balancing automated handling with user control to manage conflicts efficiently without confusion.

### Security mechanisms[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Security-mechanisms)

Dropbox implements robust security measures to protect user data both at rest and in transit.

File chunks are encrypted using AES-256, while SSL/TLS ensures secure transmission, preventing interception or eavesdropping. The system also adheres to regulatory standards such as GDPR and HIPAA. GDPR compliance entails providing users with the ability to access, correct, and delete their data, as well as facilitating secure cross-border data transfers.

HIPAA compliance requires encrypting protected health information (PHI) and supporting Business Associate Agreements (BAAs) with healthcare providers.

## Putting everything together[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Putting-everything-together)

The Dropbox system integrates multiple components and services to support efficient file storage, synchronization, and sharing.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27994%27%20height=%27459%27/%3e)![Detailed design of Dropbox system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of Dropbox system")

Detailed design of Dropbox system

**Components overview:**

- **Clients:** User devices with installed applications that interact with backend services to upload, download, and sync files.
- **Load balancer:** Distributes incoming client traffic evenly across servers for efficient resource use.
- **API gateway:** Entry point for client requests, routing them to the appropriate backend services.
- **CDN:** Delivers cached static content close to users to reduce latency.
- **Authentication and authorization service (Authn/Authz):** Verifies user identity and enforces access control.
- **File metadata server:** Maintains metadata (file names, paths, versions) and coordinates access to metadata databases and caches.
- **Metadata database:** Stores file metadata, including locations and access permissions, typically in a NoSQL database.
- **Chunk server:** Handles storage, retrieval, and management of file chunks efficiently.
- **Cloud or block storage:** Provides scalable storage for file chunks across distributed servers.
- **Synchronization server:** Tracks changes and ensures all clients have the latest file versions.
- **Pub/sub system:** Publishes updates to subscribed clients, enabling real-time synchronization and notifications.

> **Note:** User data and structured information, such as accounts or permissions, are stored in relational databases like MySQL.

## Performance optimization[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Performance-optimization)

Dropbox employs several techniques to improve system performance and ensure efficient file transfers.

These methods include using redundant database servers, caching frequently accessed files, compressing file chunks during transfer, and applying data deduplication to avoid storing duplicate content. Network conditions such as bandwidth fluctuations and latency can significantly affect upload and download performance.

To mitigate these issues, Dropbox uses adaptive bandwidth control, multi-threaded transfers, and TCP optimizations that dynamically adjust transfer rates based on network quality.

Storing local copies of frequently accessed files also helps reduce retrieval time and latency. Compression reduces the amount of data transmitted, while deduplication ensures that unique file chunks are uploaded, resulting in faster and more efficient synchronization.

Common compression algorithms include:

- Gzip (DEFLATE) for documents, JPEG for images, MP3 for audio
- LZ77 lossless compression
- On-the-fly algorithms such as LZMA, Snappy, and Brotli

For deduplication, Dropbox can use:

- SHA-256 hashing
- MD5
- Rabin Fingerprinting
- Content-defined chunking (CDC)

These strategies collectively enhance throughput, reduce storage costs, and improve user experience across devices.

## Conclusion[#](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Conclusion)

The Dropbox design strikes a balance between functional efficiency and scalable architecture.

File synchronization, version control, and access management are supported through chunking, hashing, and metadata management, ensuring reliability at scale.  High availability, fault tolerance, and performance optimizations, including real-time updates and deduplication, provide consistent and efficient user experiences across devices.

6 Tips from a System Design Expert: How Twilio Builds for Scale

Ticketmaster System Design

Ask

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Requirements)

[Resource estimation for Dropbox architecture](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Resource-estimation-for-Dropbox-architecture)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Bandwidth-estimation)

[Server estimation](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Server-estimation)

[High-level design of Dropbox](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#High-level-design-of-Dropbox)

[Detailed design of Dropbox](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Detailed-design-of-Dropbox)

[File upload and download](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-upload-and-download)

[File sharing](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-sharing)

[User authentication and access control](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#User-authentication-and-access-control)

[File synchronization](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#File-synchronization)

[Data storage and replication](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Data-storage-and-replication)

[Version control and conflict resolution](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Version-control-and-conflict-resolution)

[Security mechanisms](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Security-mechanisms)

[Putting everything together](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Putting-everything-together)

[Performance optimization](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Performance-optimization)

[Conclusion](https://www.educative.io/courses/grokking-the-system-design-interview/dropbox-system-design#Conclusion)