# Understanding_and_Modifying_Domain_Name_System_Settings

Source: https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Modification of Domain Name System

Explore the Domain Name System (DNS), its role in web applications, and how to analyze DNS records using the dig command. Understand how to modify DNS server addresses in the resolv.conf file on Linux systems to support penetration testing tasks and improve network management skills.

We'll cover the following...

- [Introduction to the DNS](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Introduction-to-the-DNS)
- [Examining the DNS](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Examining-the-DNS)
- [Modification of DNS server address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Modification-of-DNS-server-address)

## Introduction to the DNS[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Introduction-to-the-DNS)

The **DNS (Domain Name System)** provides detailed information about a web server and its interrelated domains. Without the DNS, we’d be required to remember all the IP addresses used by the rapidly growing number of websites on the internet. This makes it a critical component of most websites although it wasn’t primarily introduced with that goal in mind; it was just supposed to translate the underlying IP addresses within the web application for better readability. Basically, it’s just like a phone book, and both pentesters and hackers should be able to use the DNS to gather information about a target website.

## Examining the DNS[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Examining-the-DNS)

To examine the DNS for a given website, we’ll use the `dig` command in the terminal. In order to use `dig`, we need to ensure that we have the dnsutils package installed on our system.

Let’s try checking what information we can gain by testing the tool out with [example.com](http://example.com). In the terminal below, see `dig example.com ns` in action:

Terminal 1

Terminal

Click to Connect...

W

From the output above, we can see that:

- We’re running `dig` on a Debian version of Linux (DiG 9.18.1-1-Debian).
- The IP address of our local DNS server that is used by the `dig` query is 169.254.169.254.
- The DNS servers being queried are [a.iana-servers.net](http://a.iana-servers.net) and [b.iana-servers.net](http://b.iana-servers.net).

If we remove the `ns` argument from the `dig` command, we’ll be returned the IP address of the website itself. We can confirm this above in the terminal.

We can also get the email servers that connect to the IP address of the web server by using the `mx` argument, which is short for “mail exchanger.” If the website is using custom mail servers and they’re poorly set up, an attacker can very easily exploit them.

Since our target website is just a simple landing page for demonstration purposes, it has no mail servers attached to it.

## Modification of DNS server address[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Modification-of-DNS-server-address)

Modification of the DNS takes place in `/etc/resolv.conf` on the system. Let’s check its contents below. As established earlier, the IP address of the local DNS server is 169.254.169.254. In the terminal widget below, let’s try to modify this IP address to Google’s public DNS server, of which the primary address is 8.8.8.8 and the secondary address is 8.8.4.4. We need them both.

As `/etc/resolv.conf` is a read-only file, we’ll have to change its permissions in order to edit it. Another quick trick we can do is to overwrite it with a new file. Launch the terminal below to see how we can do this. We’ll be verifying the change by checking the file’s contents and also retrying our `dig` query from earlier.

Terminal 1

Terminal

Loading...

Modification of Network Information

Wireshark

Ask

[Introduction to the DNS](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Introduction-to-the-DNS)

[Examining the DNS](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Examining-the-DNS)

[Modification of DNS server address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-domain-name-system#Modification-of-DNS-server-address)