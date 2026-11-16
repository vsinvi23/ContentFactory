# Running_a_Basic_Web_Server_with_Apache_on_Linux

Source: https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Running a Web Server with Apache

Explore how to install and run an Apache web server on Linux. This lesson helps you understand server startup, serving default web pages, and how IP addressing enables network access. Gain insights into potential security risks hackers exploit using Apache servers.

We'll cover the following...

- [Introduction to the Apache web server](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Introduction-to-the-Apache-web-server)
- [Running a basic web server](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Running-a-basic-web-server)

## Introduction to the Apache web server[#](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Introduction-to-the-Apache-web-server)

Due to its open-source nature, the Apache web server is the most common type of server found in Linux systems, and therefore, familiarity with it is essential for any hacker or system administrator. Most hackers use Apache to set up their own web server to enable them to redirect traffic through the abuse of the Domain Name System (DNS). Some hackers also use Apache servers to perform cross-site scripting for anyone who visits a given site. In this respect, knowledge of what the Apache web server is and how it works is crucial.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzkxIiBoZWlnaHQ9IjIzNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

How a basic Apache web server functions

## Running a basic web server[#](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Running-a-basic-web-server)

The general steps involved in running our own basic web server are as follows:

1. Depending on our Linux setup, we may first need to update our system and install the software package. For Linux, it’s called `apache2`.
2. Initialize the server with `service apache2 start`.
3. Open <http://localhost> in the browser to view the default Apache web page.
4. To change the base contents of our site, we can make changes to `index.html` at `/var/www/html/`.
5. If we want another machine that’s on our network to access our web page, we need to have them type in our IP address in the URL field of their browser, like so: `http://172.17.0.2:80/`. The Apache web server generally runs through port `80`.

The process for hackers also involves getting a hold of a domain name similar to their target’s and pretending to be them. This means that adversaries can also obtain an unprotected server that’s running on Apache and change the information that’s displayed to the public users of the server. They could introduce links to their own malicious sites as well.

You can test the first four steps above using the Chrome browser below.

Running a basic Apache web server

> **Note:** Ignore the warnings from Chrome. We’ll have to open a new terminal by clicking the “**+**” next to the “Terminal” tab to make changes to `index.html`.

HTTP/S Protocol Basics

Web Encoding

Ask

[Introduction to the Apache web server](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Introduction-to-the-Apache-web-server)

[Running a basic web server](https://www.educative.io/courses/web-application-penetration-testing/running-a-web-server-with-apache#Running-a-basic-web-server)