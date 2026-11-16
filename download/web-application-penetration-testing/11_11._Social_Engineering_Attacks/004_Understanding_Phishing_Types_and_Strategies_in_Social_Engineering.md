# Understanding_Phishing_Types_and_Strategies_in_Social_Engineering

Source: https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# A Deeper Look at Phishing

Explore the processes and strategies behind phishing attacks, including mass phishing, spear phishing, whaling, and pharming. Learn how adversaries craft deceptive communications and leverage tools like SET and Metasploit. Understand different phishing vectors and approaches to better identify and mitigate these social engineering attacks.

We'll cover the following...

- [Overview](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Overview)
- [The phishing process](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#The-phishing-process)
- [Phishing strategies](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Phishing-strategies)
  - [Mass phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Mass-phishing)
  - [Spear phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Spear-phishing)
  - [Whaling](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Whaling)
  - [Pharming](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Pharming)
- [Tools used in phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Tools-used-in-phishing)

## Overview[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Overview)

When people mention social engineering, they’re generally thinking of phishing, especially with emails. There are a lot of other vectors that can be used as well. After going through the general process of a phishing attack, we’ll take a deeper look at some common strategies adversaries use when employing it.

## The phishing process[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#The-phishing-process)

Let’s go through how a phishing attack typically works:

1. The adversary creates a fraudulent website, email, or some other communication channel that appears to be both legitimate and trustworthy.
2. The adversary sends the fake or fraudulent channel to the victim either directly, through spam, through a targeted email or messaging campaign, or by pretending to be a service that the target uses frequently.
3. The victim falls for the adversary’s trick and is persuaded to do the ill-intended action, such as clicking on a malicious link or giving personal information in a fake form.
4. The adversary collects the victim’s sensitive information, which can then be used to access their accounts or masquerade as them for other attacks.

## Phishing strategies[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Phishing-strategies)

There are numerous different types of phishing attacks. The aim of some is to lead to other attacks, while others are just for simple credential harvesting. In the real world, a sophisticated adversary is often found using phishing vectors in conjunction with other attacks to truly get to the depths of a target network or system.

Depending on the target, adversaries may employ different strategies for phishing. Let’s take a look at some common ones.

### Mass phishing[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Mass-phishing)

An example of **mass phishing** is where one email with malicious content is sent to several users within a network. The adversary hopes that at least one user will fall for the trap and interact with the malicious content. After this, the adversary can simply and quickly harvest their victim’s information.

The idea here is that the malicious email is supposed to look like it’s come from a trusted source, thereby tricking the victims. A common tactic is to pretend to be from the target’s IT department and aim for less tech-savvy victims.

### Spear phishing[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Spear-phishing)

**Spear phishing** is simply targeted phishing. Instead of employing the use of mass email or messaging campaigns, the adversary conducts detailed research on specific targets and generates an email or message to trick them.

### Whaling[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Whaling)

**Whaling** is simply spear phishing, but the target is way more important, and the stakes are much higher. In the context of this strategy, CEOs, CFOs, and other executives are known as **whales**.

Whales are expected to have extensive training against phishing, so in-depth recon is generally required to successfully trick them. A common tactic is to first spear phish a target close to a whale and then use that target’s data to trick the whale.

### Pharming[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Pharming)

**Pharming** is an attack in which the adversary modifies the DNS server’s mapping of domain names to IP addresses in order to divert users away from trustworthy websites onto malicious ones. Pharming depends less on the victim taking any action, such as hoping they click on malicious links, making them more sophisticated and difficult to spot. However, for basic pharming attacks to work successfully, the adversary already needs to have access to the target’s system.

Assuming that the IP address of the attacker’s malicious website is 172.18.34.21, a brief example of pharming is modifying the `/etc/hosts` file to have [google.com](http://google.com) point to the aforementioned IP address instead.

## Tools used in phishing[#](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Tools-used-in-phishing)

There are many different tools out there that can help attackers carry out phishing attacks. Some tools and services even teach users how to avoid phishing attempts. We’ve demonstrated the use of one such tool, the Social-Engineer Toolkit (SET), and here are a few more:

- **KnowBe4:** [KnowBe4](https://www.knowbe4.com/) offers tools and services that help organizations simulate a variety of social engineering attacks, including phishing. They provide reports on employee susceptibility and offer training to help educate employees on identifying and preventing phishing attacks.
- **Metasploit:** This is a tool that allows users to perform a variety of attacks, including phishing attacks. Security professionals primarily use it to test the security of their organizations, largely because it comes loaded with many scripts, mini-tools, and a database of exploits that can be utilized in a few keypresses.
- **Gophish:** This is an open-source toolkit that allows users to test how secure their organization is from phishing attacks.

> **Note:** No tool is a complete solution for testing for phishing vulnerabilities, and it's essential to combine multiple testing methods, including manual testing and employee education, to ensure an organization's security. It's also important to follow all relevant the laws and regulations when conducting testing for phishing vulnerabilities.

Man-in-the-Middle (MITM) Attacks

Mitigation of Social Engineering

Ask

[Overview](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Overview)

[The phishing process](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#The-phishing-process)

[Phishing strategies](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Phishing-strategies)

[Mass phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Mass-phishing)

[Spear phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Spear-phishing)

[Whaling](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Whaling)

[Pharming](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Pharming)

[Tools used in phishing](https://www.educative.io/courses/web-application-penetration-testing/a-deeper-look-at-phishing#Tools-used-in-phishing)