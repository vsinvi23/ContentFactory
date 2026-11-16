# Understanding_Authentication_and_Authorization_in_Web_Security

Source: https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Fundamentals of Authentication and Authorization

Explore the fundamental concepts of authentication and authorization, focusing on how systems verify user identities and manage access rights. Learn about single-factor and multi-factor authentication methods, and understand the importance of clear authorization policies in protecting system resources and enforcing user permissions.

We'll cover the following...

- [Authentication](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authentication)
  - [Methods of authentication](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Methods-of-authentication)
- [Authorization](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authorization)

## Authentication[#](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authentication)

This is the mechanism for establishing the identities of users in a system. When users have stated their identity, it’s necessary to validate that they are the rightful owners of that identity. Verifying the user’s identification is known as **authentication**.

A simple example of authentication is when operating systems authenticate users when they try to log in to the system. Another more involved example is when we try to log in to our Gmail account and Google asks us to verify our identity through two-factor authentication (2FA) by sending our phone or other email account a one-time password (OTP) code.

### Methods of authentication[#](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Methods-of-authentication)

The basic login method of authentication stated previously is known as single-factor authentication (SFA). Let’s assume we want to look at the latest emails received on our Gmail account. We go to Gmail and are sent to its login page, where Gmail requests us to input our username and password. We do as asked, are logged in, and are then shown our emails.

![An example of SFA](001_Understanding_Authentication_and_Authorization_in_Web_Security_images/img_e7c5f7035d63.svg "An example of SFA")

An example of SFA

Granting users access only after successfully demonstrating or displaying two or more authentication methods is known as **multi-factor authentication (MFA)**.

The best practice is to implement at least two of the three main methods of authentication:

- **Knowledge:** This is something we know, e.g., passwords and paraphrases.
- **Token:** This is something we have, e.g., tokens, memory cards, and smart cards.
- **Characteristic:** This is something we are, e.g., fingerprint scan, retina scan, and other measurable characteristics.

Knowledge-based authentication uses a passphrase or secret code to differentiate between an authorized and unauthorized user. If we’ve selected a personal identification (PIN) number and created a password or secret value only we know, then we have experienced knowledge-based authentication. The problem with using this type of authentication alone is that it’s often vulnerable to various attacks. For example, the help desk might receive a call to reset a user’s password. The challenge is ensuring that the password is reset only for the correct user and not someone else pretending to be that user.

For better security, a second or third form of authentication based on a token or characteristic should be required before resetting the password. To further comment on a previous example, Google has now made 2FA mandatory. Even Microsoft has introduced measures to try and make Windows’ SFA more robust with settings such as password expiration, where users are forced to changed passwords after about every month.

## Authorization[#](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authorization)

**Authorization** is the process of defining the rights and permissions a user has in a system. It’s also the process of allowing an authenticated user to perform certain actions or access specific data. This means users need to have the appropriate clearance to execute an operation in the system.

Authorization is performed every time a user does privileged actions in the system, such as installing an application, deleting read-only documents, opening system files, etc. Organizations should have clearly defined authorization policies; otherwise, users will then have access to data they really shouldn’t be looking at. This is where a systems administrator comes in handy. After a policy is drafted, the systems administrator reinforces it. Recall the `chown` and `chmod` commands discussed earlier in the course; they’re a form of manipulating authorization rights.

Let’s look at a brief example. Assume that there’s a blogging website that has four types of users: writers, proofreaders, moderators, and the administrator. The administrator decides which type of user can perform what actions and access which pages. As such, writers and proofreaders can only edit their own profile information, unlike moderators who can edit the profile information of all the users so that disallowed information is not set. The illustration below provides more examples. It also shows that moderators posses the same privileges as proofreaders but not vice versa.

![A basic example of what the authorization policy for a blogging website would be](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A basic example of what the authorization policy for a blogging website would be")

A basic example of what the authorization policy for a blogging website would be

Quiz Yourself on SQL injection

Common Vulnerabilities

Ask

[Authentication](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authentication)

[Methods of authentication](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Methods-of-authentication)

[Authorization](https://www.educative.io/courses/web-application-penetration-testing/fundamentals-of-authentication-and-authorization#Authorization)