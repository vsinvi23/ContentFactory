# Web_Fingerprinting_Techniques_and_Web_Application_Reconnaissance

Source: https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Web Fingerprinting Infrastructure

Explore how to gather detailed information on users and web applications through web fingerprinting and open-source intelligence methods. Understand browser fingerprinting risks and how penetration testers use tools such as whatweb and whois to analyze technology stacks and domain data during reconnaissance.

We'll cover the following...

- [Introduction to fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Introduction-to-fingerprinting)
- [Browser fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Browser-fingerprinting)
- [Web application fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Web-application-fingerprinting)

## Introduction to fingerprinting[#](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Introduction-to-fingerprinting)

**Fingerprinting** is a technique used by different companies to identify their users through the websites they access. This is sometimes referred to as **browser fingerprinting**. When we browse the internet, the browser gives away a lot of our information simply because the websites request it and we grant permission. Sometimes, they don’t even ask for permission. Furthermore, somewhat like third-party cookies, websites give users unique identities that help in the tracking process. This information includes but is not limited to:

- Browser type
- Browser version
- Language being used
- Time zone
- Specifications of the computer, monitor, and peripherals
- Plug-ins and extensions installed

The information given by the browser doesn’t directly identify users, but with the use of information gathering techniques, like the one learned from the OSINT process, we could uniquely identify the different users on the internet.

## Browser fingerprinting[#](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Browser-fingerprinting)

If we care about privacy, we should be concerned about fingerprinting. There are a number of ways this can be mitigated, but they’re not foolproof. The Tor Browser makes us a more unique target considering its infamy. Mozilla’s Firefox combats browser fingerprinting by blocking all requests made to third-party sites that are known for intrusive fingerprinting, but they only block the ones they’re aware of. Finally, VPNs and proxies and the like can’t block the more determined fingerprinting techniques.

[Am I Unique](https://amiunique.org/) provides developers with data to help them build defense mechanisms against browser fingerprinting. It collects and showcases the same information that websites collect as we surf the internet. The less unique you are, the better.

## Web application fingerprinting[#](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Web-application-fingerprinting)

Pentesters can find the details of web applications with different tools that help in the reconnaissance stage. Some of these tools are Nmap, Netcat, Whatweb, Whois, and Wappalyzer. These tools help pentesters figure out what technologies were used to build a certain web application. As an example, we’ll use both `whatweb` and `whois`.

Click the terminal below to see `whatweb` in action. We’ll also provide the `-v` tag so that we can see detailed information.

Terminal 1

Terminal

Click to Connect...

W

From the output above, we can assume that [example.com](http://example.com) is being hosted on an Amazon EC2 instance (“ECS” is a big giveaway). Due to this, the location should be changing every once in a while. This is a smart move by the owners of the website because the usefulness of tools such as `whatweb` is limited; a website not using Amazon’s services or something like Cloudflare would’ve easily spit out its tech stack along with the software’s specific versions. If we’d tried using something like `whatweb` back around 2010, we’d have found out that the website was hosted somewhere in Marina del Rey or Santa Monica, California.

The `whois` query and response protocol gives a user information for any particular property that’s registered on the internet. For example, when a person registers a domain, their personal information, alongside whatever else is asked of them, becomes a part of the domain. The official `whois` website is by [ICANN](https://lookup.icann.org/en/lookup), the owner of [example.com](http://example.com).

Since it cannot provide information on all generic top-level domains (gTLDs), such as “.com,” duplicates have also popped up over the years. What we’ll test out is the `whois` command, which provides full details with no limitations while also querying the official ICANN servers.

Terminal 1

Terminal

Loading...

The output above shows that ICANN are indeed the owners of the domain. It also provides details about when it was registered, created, and updated, along with many other things.

Gathering Information on a Target

Google Hacking

Ask

[Introduction to fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Introduction-to-fingerprinting)

[Browser fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Browser-fingerprinting)

[Web application fingerprinting](https://www.educative.io/courses/web-application-penetration-testing/web-fingerprinting-infrastructure#Web-application-fingerprinting)