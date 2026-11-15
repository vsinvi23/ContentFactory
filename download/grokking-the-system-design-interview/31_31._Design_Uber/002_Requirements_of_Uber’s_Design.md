# Requirements_of_Uber’s_Design

Source: https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Requirements of Uber’s Design

Explore the critical functional requirements, like real-time location updates and ride requests, necessary for a ride-sharing platform. Define non-functional constraints, including high availability and consistency, and perform resource estimation for servers, storage, and bandwidth.

We'll cover the following...

- [Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Requirements)
  - [Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Functional-requirements)
  - [Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Non-functional-requirements)
- [Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Storage-estimation)
    - [Rider’s metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Riders-metadata)
    - [Driver’s metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Drivers-metadata)
    - [Driver location metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Driver-location-metadata)
    - [Trip metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Trip-metadata)
  - [Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Bandwidth-estimation)
  - [Number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Number-of-servers-estimation)
- [Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Building-blocks-we-will-use)

## Requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Requirements)

Let’s define the requirements for a ride-hailing system like Uber.

### Functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Functional-requirements)

Key functional requirements include:

- **Update driver location:** Automatically track driver coordinates at regular intervals.
- **Find nearby drivers:** Display available drivers in the rider's vicinity.

**Note:** Drivers can be ranked not only by proximity but also by ratings, popularity, or other relevance metrics to optimize matching.

- **Request a ride:** Riders request a ride, and the system notifies the nearest driver.
- **Manage payments:** Handle payment processing at the start and end of the trip.
- **Show driver estimated time of arrival (ETA):** Display pickup and trip ETAs to the rider, and refresh them as traffic and trip conditions change.
- **Confirm pickup:** Drivers confirm when they have picked up the rider.
- **Show trip updates:** Provide real-time status (ETA, location) to both parties during the ride.
- **End the trip:** Drivers mark the trip as complete to become available for the next ride.
- **Notifications:** Push real-time updates (e.g., requests, arrival alerts) to relevant users.

AI Powered

Saved

3 attempts left

Reset

System's Behavior on Multiple Drivers to Accept a Ride Request

What if two drivers are at the same distance from the rider? How will we select the driver to whom we'll send the request?

You have 3 attempts to answer.

### Non-functional requirements[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Non-functional-requirements)

The system must meet the following quality standards:

- **Availability:** High availability is critical; downtime disrupts active trips and prevents users from contacting each other.
- **Scalability:** The system must handle increasing volumes of drivers and riders.
- **Reliability:** Services must be error-free, ensuring smooth ride requests and location updates.
- **Consistency:** The system requires strong consistency so drivers and riders share a unified view of the trip state.
- **Fraud detection:** Identify and prevent fraudulent payment activity.
- **ETA accuracy:** Predicted arrival times must stay accurate across cities and times of day, fit within the routing latency budget, and fall back to a routing-based estimate if the prediction service is unavailable.

## Resource estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Resource-estimation)

We will base our estimates on the following assumptions:

- 500 million total riders (20 million daily active)
- 5 million total drivers (3 million daily active)
- 20 million daily trips
- Active drivers update their location every four seconds

### Storage estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Storage-estimation)

Let’s estimate the storage requirements:

#### Rider’s metadata[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Riders-metadata)

Assuming 1,000 bytes per rider (ID, name, email), storing 500 million riders requires 500 GB:

500×106×1000=500 GB {500 \times 10^6 \times 1000 } = 500\ \text{GB}500×106×1000=500 GB

Daily registration of 500,000 new riders requires an additional 500 MB.

#### Driver’s metadata[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Drivers-metadata)

Assuming 1,000 bytes per driver (ID, name, vehicle type), storing 5 million drivers requires 5 GB:

5×106×1000=5 GB {5 \times 10^6 \times 1000 } = 5\ \text{GB}5×106×1000=5 GB

Daily registration of 100,000 new drivers requires an additional 100 MB.

#### Driver location metadata[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Driver-location-metadata)

Assuming 36 bytes per location update, tracking 3 million active drivers requires 108 MB.

#### Trip metadata[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Trip-metadata)

Assuming 100 bytes per trip (IDs, timestamps), 20 million daily trips generate 2 GB of data.

**Note:** We can also maintain a hash table (DriverLocationHT) to store the most recent driver location, enabling fast updates and reducing load on the map/QuadTree service.

Total daily storage requirements:

#### Storage Capacity Estimation

|  |  |  |
| --- | --- | --- |
|  | A | B |
| 1 | Number of drivers (millions) | 3 |
| 2 | Storage required to store a driver's location (Bytes) | 36 |
| 3 | Total storage required to store drivers’ locations (MB per day) | f108 |
| 4 | Number of trips (millions) | 20 |
| 5 | Storage required to store a trip (Bytes) | 100 |
| 6 | Total storage required to store trips (GB per day) | f2 |
| 7 | Storage required for new riders daily (MB per day) | 500 |
| 8 | Storage required for new drivers daily (MB per day) | 100 |
| 9 | Total storage (GB per day) | f2.71 |

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27371%27%20height=%27161%27/%3e)![Total storage required by Uber in a year](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total storage required by Uber in a year")

Total storage required by Uber in a year

> **Note:** We can adjust the values in the table to see how the estimations change.

### Bandwidth estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Bandwidth-estimation)

We focus on driver location updates and trip data. With 20 million daily rides, the system handles approximately 232 trips per second.

20,000,00086,400≈232 trips per second\frac{20,000,000}{86,400} \approx 232\ \text{trips per second}
86,40020,000,000​≈232 trips per second

At 100 bytes per trip, this consumes approximately 23 KB/s of bandwidth.

232×100=23,200 bytes=23 KB×8=185 kbps232 \times 100 = 23,200\ \text{bytes} = 23\ \text{KB} \times 8 = 185\ \text{kbps}
232×100=23,200 bytes=23 KB×8=185 kbps

Active drivers update their location every four seconds. If each update contains a driver ID (3 bytes) and location (16 bytes), the bandwidth usage is:

3M active drivers×(3+16)B=57 MB×8=4564=114 Mbps3M\ \text{active drivers} \times (3 + 16)B = 57\ \text{MB} \times 8 = \frac{456}{4} = 114\ \text{Mbps}
3M active drivers×(3+16)B=57 MB×8=4456​=114 Mbps

**Note:** To optimize bandwidth, the system should push updates only to relevant nearby riders using spatial partitioning, like QuadTree or geohash-based sharding. For trip notifications, while 232 trips/sec is the average, peak loads may require burst handling.

These estimates exclude map data and other heavy assets handled by separate components.

#### Bandwidth Requirements

|  |  |
| --- | --- |
| Trips per second | 232 |
| Bandwidth for each trip (Bytes) | 100 |
| Total bandwidth for trips (kilo bits per second) | f185.6 |
| Active drivers (millions) | 3 |
| Bandwidth for each driver (Bytes) | 19 |
| Bandwidth for drivers (Megabits per second) | f114 |
| Total bandwidth (Megabits per second) | f114.19 |

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27619%27%20height=%27136%27/%3e)![The total bandwidth required by Uber](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The total bandwidth required by Uber")

The total bandwidth required by Uber

> **Note:** We can adjust the values in the table to see how the requirements change.

User-facing bandwidth is minimal compared to map data transmission, which is covered in the [Google Maps](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-google-maps) chapter.

### Number of servers estimation[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Number-of-servers-estimation)

With 23 million total daily active users (20M riders, 3M drivers), we estimate peak load at 23 million requests per second (RPS), using [our DAU-to-RPS proxy assumption](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective). The server count is calculated as:

Servers needed at peak load = Number of requests/secondRPS of server\text{Servers needed at peak load = } \frac{\text{Number of requests/second}}{\text{RPS of server}}
Servers needed at peak load = RPS of serverNumber of requests/second​

Assuming a single server handles 64,000 RPS, the required server count is:

Servers needed at peak load=23 million64,000≈360 servers\text{Servers needed at peak load} = \frac{23\ \text{million}}{64,000} \approx 360\ \text{servers}
Servers needed at peak load=64,00023 million​≈360 servers

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27271%27%20height=%27161%27/%3e)![The number of servers required for Uber service](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The number of servers required for Uber service")

The number of servers required for Uber service

## Building blocks we will use[#](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Building-blocks-we-will-use)

The design utilizes the following core components:

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27497%27%20height=%27141%27/%3e)![Building blocks in the high-level design of Uber](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks in the high-level design of Uber")

Building blocks in the high-level design of Uber

- [**Cache**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-distributed-cache)**:** Stores frequently accessed data for low latency.
- [**Load balancer**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-load-balancers)**:** Distributes requests across services.
- [**CDNs:**](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-the-content-delivery-network-cdn) Deliver static content efficiently, reducing latency and server load.
- [**Databases:**](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases) Store persistent metadata for riders, drivers, and trips.

Additionally, user devices require GPS and sufficient bandwidth for navigation.

> **Note:** The information provided in this chapter is inspired by the engineering blog of Uber.

System Design: Uber

High-level Design of Uber

Ask

[Requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Requirements)

[Functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Functional-requirements)

[Non-functional requirements](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Non-functional-requirements)

[Resource estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Storage-estimation)

[Rider’s metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Riders-metadata)

[Driver’s metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Drivers-metadata)

[Driver location metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Driver-location-metadata)

[Trip metadata](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Trip-metadata)

[Bandwidth estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Bandwidth-estimation)

[Number of servers estimation](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Number-of-servers-estimation)

[Building blocks we will use](https://www.educative.io/courses/grokking-the-system-design-interview/requirements-of-ubers-design#Building-blocks-we-will-use)