# Understanding_HTTP_and_HTTPS_Protocol_Basics_for_Web_Security

Source: https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# HTTP/S Protocol Basics

Explore the basics of HTTP and HTTPS protocols essential for web application penetration testing. Understand how data communication occurs between clients and servers, the security risks of unencrypted HTTP, and how HTTPS secures data through encryption and authentication. This lesson equips you with knowledge of web protocols to better assess web application vulnerabilities.

We'll cover the following...

- [Introduction to web protocols](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#Introduction-to-web-protocols)
- [The OSI model](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-OSI-model)
  - [The Hypertext Transfer Protocol (HTTP)](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-HTTP)
- [The Hypertext Transfer Protocol Secure (HTTPS)](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-Secure-HTTPS)

## Introduction to web protocols[#](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#Introduction-to-web-protocols)

**Protocols** are rules that guide communication between different elements in a networking environment. The hardware and software work together to complete tasks—for example, to send data across a network through various computers. As such, the web works with many different protocols that allow communication to take place in many different ways.

This leads us to the Open Systems Interconnection Reference model, which is also known as the OSI model. A web application pentester is expected to have a sound understanding of the OSI model. Knowledge of various protocols and how they work, how communication takes place in and across networks, and how to navigate through the complexities of general web infrastructure is a critical aspect of their job.

## The OSI model[#](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-OSI-model)

The OSI model is a networking structure that has seven layers (tabulated below). We’ll be focusing on the seventh layer, specifically HTTP.

## OSI Model Layers

|  |  |  |
| --- | --- | --- |
| **Layer Number** | **Layer Name** | **Description** |
| 7 | Application layer | This layer focuses on end user processes by allowing users and applications to communicate in and across networks. HTTP, Telnet, and FTP are some of the protocols used in this layer**.** For example, when users are browsing using a browser or Spotify, they are at the application layer. |
| 6 | Presentation layer | This helps in the syntax and reconstruction of the data passed around by the application layer. JPEG, PICT, ASCII, TIFF, GIF, EBCDIC, MPEG, and MIDIare some of the protocols used in this layer. Loading images while browsing or watching a movie are examples of activities at this layer. |
| 5 | Sessional layer | This controls the interactivity between applications in the network. NFS, NetBIOS, RPC, and SQL are some of the protocols used in this layer. SQL has a specific port (typically `1433`) through which it communicates and establishes sessions with remote databases. |
| 4 | Transport layer | This controls what is sent and how much of it gets sent at a particular time within a network. It utilizes protocols such as TCP, UDP, and SPX. |
| 3﻿ | Network layer | This layer helps in facilitating packet forwarding by setting the route in which the packet travels through a network. AppleTalk, TCP/IP, and IPX are some of the protocols used in this layer. |
| 2 | Data link layer | This layer provides node-to-node transfer of data within a network. It's associated with the Media Access Control layer and Logical Link Control layer. The goal of this layer is to ensure that the data being sent is the same as the data being received. |
| 1 | Physical layer | This is the hardware element. It includes switches, routers, Ethernet cables, and many other networking hardware components. |

### The Hypertext Transfer Protocol (HTTP)[#](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-HTTP)

The internet is a massive decentralized network that operates on a client-server information framework. Therefore, for communication to take place, web frameworks, such as websites and servers, must agree on a specific protocol to use as described in the OSI model.

HTTP is the asymmetric protocol for requesting and responding to information in a network between a client and a server. The client sends the request, and the server gives a response back. HTTP is therefore a pull protocol in a networking environment.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTExIiBoZWlnaHQ9IjEzMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

A simplified view of how HTTP works

Whenever a user issues a Uniform Resource Locator (URL), such as [http://www.educative.io](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics), the browser helps in the interpretation of the URL into a piece of request information that is then sent to the HTTP server. The server process the data and then returns the appropriate information, which can be either a resource that was requested or an error message if the resource isn’t available (usually the 404 messages that we see when a website doesn’t load).

However, there’s an age-old security flaw in HTTP: the information it transmits over the network isn’t encrypted. This means that when we submit our username and password to log in to a website, if the website is running with HTTP, then it’s very likely passing the credentials as is. An attacker can easily sniff around for information by capturing our outgoing packets and analyzing them because the data is in plaintext.

## The Hypertext Transfer Protocol Secure (HTTPS)[#](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-Secure-HTTPS)

This is a protocol that combines HTTP and SSL/TLS (Secure Sockets Layer/Transport Layer Security). It helps in the encryption of almost all the information passing through a networked environment between a client and server.

It promotes the CIA triad in a network, which includes:

- **Confidentiality:** This ensures that only authorized users can connect.
- **Integrity:** This ensures that the information sent by connected users and received from the user is not modified or tampered with by third parties.
- **Availability:** This ensures that connected, authorized users can access the website as needed.

There is also one more important feature that we shouldn’t forget. This is authenticity, which ensures that the connected users are indeed who they claim to be.

This is why most websites these days have implemented the use of HTTPS. If you ever encounter a website that hasn’t upgraded to HTTPS, your browser will give you a warning and may also prevent you from accessing it. Browsers also try to automatically upgrade insecure connections to HTTPS when they detect HTTP in the URL field.

Quiz Yourself on Python Basics

Running a Web Server with Apache

Ask

[Introduction to web protocols](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#Introduction-to-web-protocols)

[The OSI model](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-OSI-model)

[The Hypertext Transfer Protocol (HTTP)](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-HTTP)

[The Hypertext Transfer Protocol Secure (HTTPS)](https://www.educative.io/courses/web-application-penetration-testing/http-s-protocol-basics#The-Hypertext-Transfer-Protocol-Secure-HTTPS)