# Understanding_Social_Engineering_Attacks_and_Defense_Strategies

Source: https://www.educative.io/courses/web-application-penetration-testing/social-engineering

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Social Engineering

Explore common social engineering attacks including phishing, pretexting, smishing, and baiting, and understand their methods and impacts. Learn how attackers exploit human behavior to access sensitive information and systems. Gain knowledge of mitigation techniques and tools used to test and strengthen defenses against these attacks to better protect organizational security.

We'll cover the following...

- [Introduction to social engineering](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Introduction-to-social-engineering)
- [Types of social engineering attacks](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Types-of-social-engineering-attacks)
  - [Phishing](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Phishing)
  - [Pretexting](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Pretexting)
  - [Smishing](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Smishing)
  - [Physical breaches](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Physical-breaches)
  - [Baiting](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Baiting)
  - [Honeytrap](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Honeytrap)
  - [Quid pro quo](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Quid-pro-quo)
  - [Water hole attacks](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Water-hole-attacks)
- [Testing for social engineering](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Testing-for-social-engineering)

## Introduction to social engineering[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Introduction-to-social-engineering)

The aim of hacking is to compromise systems and applications. Social engineering attackers attempt to exploit the users of these systems by pretending to be employees, vendors, or even support personnel to try to trick the workers of those organizations. Unaware and unprepared employees are the ones who’re most vulnerable to social engineering attacks. Attackers may appeal to these people’s willingness to help others or take advantage of their lack of knowledge to try and get them to reveal information that would compromise the system.

Traditional protection from viruses and malware, i.e., antiviruses, cannot protect organizations from social engineering attacks. Rigid training sessions and drills need to be conducted regularly to ensure employees don’t fall for the attackers’ tricks. Some employees may also not care either way, so there should be failsafe mechanisms in place to ensure that attackers don’t take advantage of these willing employees. These mechanisms also should protect the system in case of a breach.

Let’s see what the general flow of a social engineering attack looks like:

1. The attacker gathers information on their target before establishing contact.
2. The attacker initiates contact with their target and gradually gains their trust—for example, by pretending to be from the IT team.
3. The target breaks security protocol and hands over confidential information to the attacker without even verifying their identity first.
4. The confidential information includes the target user’s credentials, which the attacker then uses to compromise the target’s system.

![The general flow of a social engineering attack](001_Understanding_Social_Engineering_Attacks_and_Defense_Strategies_images/img_578447102f59.svg "The general flow of a social engineering attack")

The general flow of a social engineering attack

## Types of social engineering attacks[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Types-of-social-engineering-attacks)

There are many different types of social engineering attacks, and the number will keep increasing as technology evolves. Let’s look into some of the most common ones.

### Phishing[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Phishing)

People are the most prone to falling for a **phishing** email. This is where an attacker sends an email to a predetermined target employee at an organization and hopes that they’ll open the email. The actions after the opening of the email vary. Most phishing emails are gateways to XSS attacks, like the links received to confirm lottery winnings are just disguised malicious sites. Some phishing emails may ask us for credentials or certain information. The rule of thumb should be that if we’re not expecting the email and if the domain of the sender’s account is strange or misspelled, then it’s a phishing attempt.

### Pretexting[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Pretexting)

This is the scam call approach. Attackers make up a scenario to obtain sensitive information through phone calls. This process first needs trust between the adversary and the target. The attacker, therefore, must compose some plausible scenario that’ll move the victim to reveal the sensitive information to the attacker. A common attack that involves this technique is calling a bank’s support line and claiming that we’ve changed numbers and have forgotten our credit card’s PIN code. Some support technicians may break protocol and hear our plea out, then ask simple questions to verify our identity before telling us your PIN code. This is why most companies don’t let support employees have access to such information anymore.

### Smishing[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Smishing)

This is the same as phishing but involves SMS. Smishing attacks are often accompanied by pretexting attempts so that users are less suspicious of the harmful messages.

### Physical breaches[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Physical-breaches)

This is where the attacker physically tries to gain entry into secure locations, such as server rooms. These include techniques such as:

- **Tailgating:** Passing through a locked door right after an actual employee has authorized entry for themselves.
- **Identification through obscurity:** Large organizations often have many employees. Everybody can’t obviously know or remember everybody else. If someone asks us for identification, as long as we possess a convincing ID card and seem to know where we’re going, people won’t get suspicious.
- **Identification through authority:** A yellow vest, toolbox or ladder, and a notepad will also get attackers into a surprising number of places.
- **Impersonation:** Pretending to be an employee at the organization also works.

### Baiting[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Baiting)

**Baiting** is a type of social engineering attack where the attacker makes false promises to the victim so that they’ll reveal sensitive information. This attack can involve ads, free games and movies, and lotteries. The hacker can only hope that the password used by the victim in signing up for this is the same as in all other sites, thereby allowing them to access the victim’s information and perform privilege escalation. Russian and Chinese hackers often bait Steam (an online video game store) users with free beta keys and cosmetic skins for free-to-play games.

### Honeytrap[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Honeytrap)

This is an attack that targets those looking for love on online dating websites and social media platforms. The attacker will create a profile of a fictional person and then target people wanting to connect with others. Over a certain period, the attacker will trick the victim into giving them money or even system credentials. These types of attacks are often performed on the aforementioned willing employees.

### Quid pro quo[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Quid-pro-quo)

This attack lures the victim into releasing sensitive information in exchange for different services. For example, an attacker may pose as a computer technician and call the victim to address a common issue in the victim’s computer. Once the attacker gets the information they want, they then perform privilege escalation to then access other information that may interest them.

### Water hole attacks[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Water-hole-attacks)

A particular kind of cyberattack, known as the **water hole attack**, focuses on a website frequently visited by the attacker’s intended targets. Attackers will breach these websites and insert malware or harmful code, which can subsequently be utilized to infect users’ systems. The phrase “water hole” describes a situation where the attackers passively wait for their prey to approach them rather than aggressively looking for victims. Because the attackers can pick their targets carefully, this attack is frequently used to target particular businesses or organizations and can be challenging to identify and fight against.

## Testing for social engineering[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Testing-for-social-engineering)

Many technologies are available that can be used to check for social engineering weaknesses. Several popular choices include:

- **PhishMe:** Users of PhishMe can develop and distribute fake phishing emails to staff members or other stakeholders. It comes with several options for personalizing the look and feel of these emails and monitoring the attacks’ effectiveness. Additionally, it has a reporting function that offers specific details on the outcomes of the phishing assaults, including which workers were duped and which ones correctly recognized the fraudulent email.
- **KnowBe4:** This is a tool that helps organizations simulate a variety of social engineering attacks, including phishing, baiting, scareware, and pretexting. It provides reports on employee susceptibility and offers training to help educate employees on identifying and preventing social engineering attacks.
- **Social-Engineer Toolkit (SET):** This open-source tool allows users to perform a variety of social engineering attacks, including phishing and pretexting. Security professionals primarily use it to test the security of their organizations.
- **Metasploit:** Metasploit has many features, including a database of known vulnerabilities, a framework for creating and testing custom exploits, and user interfaces for managing and launching attacks. It supports many attack types, including network, web application, and social engineering attacks.

> **Note:** No tool is a complete solution for testing for social engineering vulnerabilities. It’s essential to combine multiple testing methods, including manual testing and employee education, to ensure an organization’s security. It’s also vital to follow all the relevant laws and regulations when conducting testing for social engineering vulnerabilities.

Quiz Yourself on Cross-Site Request Forgery

Social-Engineer Toolkit (SET)

Ask

[Introduction to social engineering](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Introduction-to-social-engineering)

[Types of social engineering attacks](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Types-of-social-engineering-attacks)

[Phishing](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Phishing)

[Pretexting](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Pretexting)

[Smishing](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Smishing)

[Physical breaches](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Physical-breaches)

[Baiting](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Baiting)

[Honeytrap](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Honeytrap)

[Quid pro quo](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Quid-pro-quo)

[Water hole attacks](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Water-hole-attacks)

[Testing for social engineering](https://www.educative.io/courses/web-application-penetration-testing/social-engineering#Testing-for-social-engineering)