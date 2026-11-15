# Design_of_Yelp

Source: https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking Modern System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

# Design of Yelp

Define the detailed architecture for a proximity service like Yelp. Explore the necessary API design for search and data entry, and structure the storage schema using relational and key-value databases. Learn how specialized components like quadtree servers and aggregators handle complex geospatial search requests efficiently.

We'll cover the following...

- [API design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#API-design)
  - [Search](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Search)
  - [Add a place](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-place)
  - [Add a review](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-review)
- [Storage schema](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Storage-schema)
- [Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Design)
  - [Components](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Components)
  - [Workflow](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Workflow)

Following the requirements and estimations from the previous lesson, we will now focus on the API design, storage schema, and system building blocks.

## API design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#API-design)

This section outlines the API endpoints for the system.

### Search[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Search)

The `search` function locates places based on categories (e.g., “cafes” ):

Ace Editor

1

search(category, user\_location, radius)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `category` | This is the type of search the user makes, for example, a search for restaurants, cinemas, cafes, and so on. |
| `user_location` | This contains the location of the user who’s searching with Yelp. |
| `radius` | This is the specified radius where the user is trying to find the required category. |

Returns a JSON object listing items in the category within the specified radius. Each entry includes the place name, address, category, rating, and thumbnail.

To search for a specific place by name (e.g., “Burger Hut” ):

Ace Editor

1

search(name\_of\_place, user\_location, radius)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `name_of_place` | This contains the name of the place that the user wants to search for. |

Returns a JSON object containing details of the specified place.

### Add a place[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-place)

To add a new place:

Ace Editor

1

add\_place(name\_of\_place, description\_of\_place, category, latitude, longitude, photo}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `name_of_place` | This contains the name of the place, for example, "Burger Hut". |
| `description_of_place` | This contains a description of the place. For example, "Burger Hut sells the yummiest burgers". |
| `category` | This specifies the category of the place—for example, "cafe". |
| `latitude` | This tells us the latitude of the place. |
| `longitude` | This tells us the longitude of the place. |
| `photo` | This contains photos of the place. There can be a single or multiple photos. |

Returns a confirmation of the addition or an error message.

### Add a review[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-review)

To add a review:

Ace Editor

1

add\_review(place\_ID, user\_ID, review\_description, rating)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `place_ID` | This contains the ID of the place whose review is added. |
| `user_ID` | This contains the ID of the user who adds the review. |
| `review_description` | This contains the review of the place—for example, "the food and ambiance were superb". |
| `rating` | This contains the rating of the place—for example, 4 out of 5. |

Returns a confirmation of the addition or an error message.

## Storage schema[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Storage-schema)

The storage schema requires tables for Places, Photos, Reviews, and Users.

The “Place” table includes:

- **Place\_ID:** Unique 8-byte (64-bit) ID generated by the sequencer.

> **Note:** IDs are generated using the unique ID generator.

- **Name\_of\_Place:** Place name (256 bytes).
- **Description\_of\_Place:** Place description (1,000 bytes).
- **Category:** Type of place (e.g., restaurant, cinema) (8 bytes).
- **Latitude:** Location latitude (8 bytes).
- **Longitude:** Location longitude (8 bytes).
- **Rating:** Star rating (0-5), calculated based on user reviews.

Essential columns are listed above. Additional columns might include menu, address, and operating hours. Based on the essential columns, the row size is:

Ace Editor

1

Size = 8 + 256 + 1000 + 8 + 8 + 8 + 1 = 1289 bytes

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The “Photos” table includes:

- **Photo\_ID**: Unique 8-byte (64-bit) ID.
- **Place\_ID**: Foreign key (8 bytes) linking the photo to a place.
- **Photo\_path**: Path to the photo stored in blob storage (256 bytes).

Ace Editor

1

Size = 8 + 8 + 8 + 256 = 280 bytes

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The “Reviews” table stores reviews, ratings, and photos:

- **Review\_ID:** Unique 8-byte (64-bit) ID.
- **Place\_ID:** Foreign key (8 bytes) linking to the Place table.
- **User\_ID:** Foreign key (8 bytes) linking to the Users table.
- **Review\_description:** Text of the review (512 bytes).
- **Rating:** Star rating (1 byte).

Ace Editor

1

Size = 8 + 8 + 8 + 512 + 1 = 537 bytes

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The “Users” table stores user information:

- **User\_ID:** Unique 8-byte ID.
- **User\_name:** User’s name (256 bytes).

Ace Editor

1

Size = 8 + 256 = 264 bytes

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

> **Note:** The `INT` type in the schema refers to an 8-byte ID generated by the unique ID generator.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27941%27%20height=%27254%27/%3e)![Storage schema](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Storage schema")

Storage schema

## Design[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Design)

This section details the system’s building blocks and their interactions.

### Components[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Components)

- **Segments producer:** Communicates with third-party map services (e.g., Google Maps) to divide the world into smaller regions called segments. This reduces the search scope.
- **Quadtree servers:** Manage trees containing places within segments. They process search requests based on the radius and the user’s location.
- **Aggregators:** Collect results from quadtree servers and return a consolidated list to the user.
- **Read servers:** Handle read requests, directing search queries to quadtree servers. Separating read traffic improves efficiency.
- **Write server:** Handle write requests (e.g., adding places, reviews, ratings) and update storage.
- **Storage:** Two types of storage are used:

  - **SQL database:** Stores relational data (Users, Places, Reviews, Photos). SQL facilitates queries such as retrieving a user’s visit history or a place’s reviews, and it ensures consistency. See the [Database](https://www.educative.io/courses/grokking-the-system-design-interview/introduction-to-databases) building block for more details.
  - **Key-value stores:** Stores the list of places mapped to segment IDs and quadtree data mapped to unique IDs for low-latency access.
- **Load balancer:** Distributes incoming requests uniformly across servers.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271182.7500000000002%27%20height=%27468.3499999999999%27/%3e)![The detail design of Yelp](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The detail design of Yelp")

The detail design of Yelp

### Workflow[#](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Workflow)

When a user initiates a search, the system identifies relevant places within a radius relative to the user’s coordinates.

- **Searching for a place:** Load balancers route requests to read servers, which query quadtree servers for places within the radius. Aggregators refine the results before returning them to the user.
- **Adding a place or feedback:** Load balancers route requests to write servers. These servers update the relational database and store images in blob storage.
- **Making segments:** The segments producer splits the map into segments. Places within each segment are stored in a key-value store. This process repeats periodically (e.g., monthly) to incorporate new places.

We have covered the API design, storage schema, and system architecture. The next lesson focuses on design considerations.

Requirements of Yelp’s Design

Design Considerations of Yelp

Ask

[API design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#API-design)

[Search](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Search)

[Add a place](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-place)

[Add a review](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Add-a-review)

[Storage schema](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Storage-schema)

[Design](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Design)

[Components](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Components)

[Workflow](https://www.educative.io/courses/grokking-the-system-design-interview/design-of-yelp#Workflow)