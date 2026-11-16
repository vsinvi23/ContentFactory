# Gathering_Information_on_a_Target_Using_OSINT_Techniques

Source: https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Gathering Information on a Target

Explore how to collect vital information on a penetration testing target using Open Source Intelligence. Understand the roles of identifiers and pivoting, and distinguish between active, passive, and semi-passive data gathering methods. Gain foundational knowledge to perform reconnaissance ethically and effectively in cybersecurity.

We'll cover the following...

- [Introduction to OSINT](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Introduction-to-OSINT)
- [Identifiers](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Identifiers)
- [Pivoting](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Pivoting)
- [Information gathering](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Information-gathering)
  - [Active](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Active)
  - [Passive](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Passive)
  - [Semi-passive](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Semi-passive)
- [OSINT lifecycle](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#OSINT-lifecycle)

## Introduction to OSINT[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Introduction-to-OSINT)

Information gathering is critical to penetration testing in the field of cybersecurity. Knowledge is power; therefore, a good pentester should know how to perform reconnaissance activities and be able to glean important information from what is gathered. The most accessible process is known as **Open Source Intelligence (OSINT)**, which involves information gathering from public sources. If you’ve ever received a call from an unknown number and saved that number in order to check the associated WhatsApp account profile, then congratulations, you’ve employed the use of a basic OSINT technique.

The OSINT process is used in many fields of life. A few scenarios are:

- Journalists write news reports using anonymous tips and perform Google reverse image searches on images they’ve been sent.
- Cybercriminals search for people to scam by looking through their Facebook and Instagram post history.
- Students in academia work on their various research projects or theses.
- Employers look for new recruits and perform background checks by accessing public records and social media accounts.
- Law enforcement works on criminal cases. For example, a criminal’s phone may be confiscated, and all the unsaved numbers on it may be passed through phone books and matched against social media accounts.

The sources of data for OSINT are tremendous, covering satellite imagery, public court records, social media posts, videos on anonymous image boards, threads on specialist forums, news articles, data leaks, website history, IP registration data, open directories, and many more.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjYzIiBoZWlnaHQ9IjQ5MyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

The possibilities of sources are almost endless

As well as a great number of sources, the internet is also home to a vast array of tools that can be used to verify both the data and sources and also extrapolate for further clues. For example, we can use Google Maps to identify a location from a photograph. There are even tools to help us ascertain where the photographer was standing when the photograph was taken.

There are two main concepts we use when dealing with the OSINT way of gathering information on a target. These concepts are identifiers and pivoting.

## Identifiers[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Identifiers)

**Identifiers** are keywords that help in describing an entity in the information gathering phase during the OSINT process. The information includes:

- Names
- Emails
- Dates of birth
- IP addresses of home and office networks
- MAC addresses of devices owned or used by the target
- Phone numbers
- Home and work addresses
- Vehicle license plate alphanumeric IDs
- Data on friends or mutuals on social media profiles
- Links to personal sites

This information exists across different datasets scattered through the internet. In some cases, we may even need to implement some field investigative techniques to find further data. But generally, when working with the OSINT process, we start with only one or two identifiers and gradually make up a complete profile of the target.

## Pivoting[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Pivoting)

**Pivoting** is when we correlate or extrapolate identifiers to discover new ones about a target. In the case of web pentesting, a server’s IP address can help give more information about the country of the server’s location. Another example would be that the open ports on a server could indicate the kind of services being run on the server, which could then be exploited.

## Information gathering[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Information-gathering)

There are three ways to gather data or information in OSINT:

- Active
- Passive
- Semi-passive

### Active[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Active)

The **active information gathering** method places the researcher in direct contact with the target. Travelling to the target location may be needed to get the required information. Interviewing people related to the target, doing dumpster diving, or scanning systems for vulnerabilities may also be done to gather information.

The results from the active information gathering methodology have high accuracy; however, there is a higher risk of being detected within the system or even at the premises of the target because of the direct involvement. Beginners may also be trapped by the narrow scope and miss out on the bigger picture. For example, imagine we’re supposed to perform social engineering techniques to gain access to an organization’s network. We choose to investigate certain people from the IT department but fail to realize that a much easier target would be less tech-savvy employees who’re more susceptible to phishing (to be discussed in detail in a later chapter) attempts.

### Passive[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Passive)

**Passive information gathering** focuses more on the quiet observation of data that’s generated by the target. For example, it can involve studying the geolocation of the target, eavesdropping on their conversations, or finding vulnerabilities by fingerprinting a device within the target system.

OSINT largely falls under the category of passive techniques of information gathering since it can be done from our own home. We can also remain anonymous provided we are practicing a good operational security (OPSEC) strategy, such as using virtual machines, VPNs, fake emails and burner phones, and the Tor Browser. The disadvantage of passive information gathering is that it involves detailed analysis and may not provide the same quality of data compared to the active information gathering technique.

## Active vs. Passive Information Gathering

|  |  |
| --- | --- |
| **Active** | **Passive** |
| Make contact with the target. | Never make direct contact with the target. |
| More accurate or up-to-date information | Relies on third-party information |
| Higher risk of being detected | Low risk of being detected unless the target is extra careful |
| Directed scanning with tools such as Nmap and Nikto that can leave records | Passive scanning using tools such as Shodan or Whois |
| May involve deceptive techniques, such as phishing | Tying together public or technical records to show patterns |

### Semi-passive[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Semi-passive)

The **semi-passive technique** involves leveraging a third-party service’s active collection measures to perform passive analysis. For example, we could visit [urlscan.io](http://urlscan.io) in Chrome below and search for [example.com](http://example.com). We’re using this website as a third-party service to scan the target on our behalf and present all relevant details to us, without any of the fluff.

Running Chrome

## OSINT lifecycle[#](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#OSINT-lifecycle)

As established, the lifecycle of the OSINT process involves four stages. Let’s go through each in detail:

1. **Collection:** This stage involves accumulating data from a variety of sources. It sometimes involves signing up for accounts and building up API keys to query services that host the data. For example, a service such as [IntelX](https://intelx.io) scours Pastebin and many other sources, including forums on the dark web, for breached data. This is the kind of data that usually evades search engine indexing. Another example would be querying the target’s email address on [Have I Been Pwned](https://haveibeenpwned.com/) to check whether their account credentials were leaked in any data breaches.
2. **Processing:** This is the process of translating results or normalizing them into a common format for collaboration. For example, working with a diverse team, we may have to translate our findings using Google Translate and then consolidate them in a Google Docs document.
3. **Analysis:** This step involves connecting the dots between the formatted data. It’s sometimes referred to as **data correlation**. This involves identifying information about the identifiers and analyzing the results in a broader context from the target. For example, we could use [Maltego](https://www.maltego.com/) to perform graphical analysis between different identifiers. At this stage, we might also find that some of the sources might be biased or of questionable origin, and therefore authenticating the credibility of the sources becomes vital.
4. **Production:** A final report is drafted, which is then shared with others.

For beginners in cybersecurity, practising OSINT gathering skills is a fantastic way to enter the field. This is because it doesn’t require heavy technical knowledge or programming skills since the process is naturally research oriented, which helps pentesters develop the virtues of persistence and curiosity. These virtues are essential for success in this field.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzc2IiBoZWlnaHQ9IjM3NiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

The OSINT lifecycle

To conclude, we’ve only scratched the surface of OSINT techniques and tools. A cybersecurity enthusiast should always be on the lookout for new sources and be broadening their toolset. They also need to keep evolving; coming up with new tricks is essential because threat actors constantly keep hammering at our defenses.

Quiz Yourself on Network Management and Analysis

Web Fingerprinting Infrastructure

Ask

[Introduction to OSINT](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Introduction-to-OSINT)

[Identifiers](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Identifiers)

[Pivoting](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Pivoting)

[Information gathering](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Information-gathering)

[Active](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Active)

[Passive](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Passive)

[Semi-passive](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#Semi-passive)

[OSINT lifecycle](https://www.educative.io/courses/web-application-penetration-testing/gathering-information-on-a-target#OSINT-lifecycle)