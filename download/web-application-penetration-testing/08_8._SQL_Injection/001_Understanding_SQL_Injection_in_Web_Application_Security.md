# Understanding_SQL_Injection_in_Web_Application_Security

Source: https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Introduction to SQL Injection

Explore the fundamentals of SQL injection, how attackers exploit database inputs in web applications, and the different types of SQL injection attacks. Understand techniques for detection, exploitation, and mitigation to improve your web security skills.

We'll cover the following...

- [Overview](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Overview)
  - [How does an SQL injection work?](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#How-does-an-SQL-injection-work)
  - [Types of SQL injections](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Types-of-SQL-injections)
    - [Error based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Error-based)
    - [Union based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Union-based)
    - [Blind](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Blind)
      - [Boolean](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Boolean)
      - [Time based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Time-based)

# Overview[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Overview)

Most web applications use some sort of database as a way of storing information. Quite a lot of these databases are programmed using the Structured Query Language (SQL). Consequently, **SQL injection** came about as one of the more prevalent vulnerabilities on the internet.

SQL injection works primarily with web applications with a database that takes input from users querying the database for a response.

The aim of an SQL injection technique is either to bypass the SQL query being made and execute malicious code or to have the database dump all its data. As such, pentesters should keenly look for SQL-related vulnerabilities within web applications because the consequences are often disastrous.

![](001_Understanding_SQL_Injection_in_Web_Application_Security_images/img_f09006a57a5d.svg)

## How does an SQL injection work?[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#How-does-an-SQL-injection-work)

The adversary first ensures that their target has a database. After that, the adversary notes all the areas of the web application where the user is allowed to provide input. They then try to probe those areas with basic checks to find out whether the areas are susceptible to SQL injection. They craft queries to achieve their goal, be it dumping schemas, bypassing logins, or overwriting the data in the database.

Let’s look at a brief example. Assume that we’re trying to log in to a web application. The web application handles input from the login fields like so:

```
query = "

SELECT *

FROM users

WHERE username = " &

Request.QueryString("username") & "

AND password = " &

Request.QueryString("password")
```

This means that if we were to enter credentials such as `this_username` and `that_password`, the query sent to the database will be:

```
SELECT * FROM users WHERE username = 'this_username' AND password = 'that_password'
```

Then there’ll be server-side logic to check if one user has been returned by the query. The positive case would result in our being logged in.

An adversary could try inputs such as `'`, `"`, `')`, or `--` to check how the login function differs in response to normal use. The logic here is that an apostrophe, double hyphen, or some other trick would break the original SQL query being used and force the server to send off another query as well—one that’s been crafted to do harmful things.

If the attacker were to input `"` in the username field and `"; DROP TABLES users` in the password field, then the queries being passed to the server will look like this:

```
SELECT * FROM users WHERE username = '' AND password = ''; DROP TABLES users
```

This will result in the table being removed from the database, and that really won’t be a fun time for the web application owners or the developers.

## Types of SQL injections[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Types-of-SQL-injections)

As with most bad things in cybersecurity, SQL injections also come in several types. Let’s discuss each.

### Error based[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Error-based)

This is easiest and most common type of injection. This attack happens when the web application gives wrong feedback or errors to the users from the underlying database server. This is a basic attack because the database can give more information on the details of its structure, such as tables, columns, and rows, all the way through to what the actual data is in the database. The attacker relies on the errors displayed to craft targeted malicious code for further data retrieval or even to directly damage the database itself.

The strategy we discussed in the previous section is an example of an error-based SQL injection. We probed for errors and then crafted a response using probable hints from them.

### Union based[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Union-based)

The adversary can make use of the `UNION` operator, which fuses multiple select statements created by the database. This largely comes in handy when trying for data retrieval. Keep in mind that we still have to probe for SQL injection susceptibility first, which causes some people to argue that it’s just an extension of an error-based attack.

If the attacker were to input `'` in the username field and `' UNION SELECT * FROM users` in the password field, the query sent to the database would be:

```
SELECT * FROM users WHERE username = '' AND password = '' UNION SELECT * FROM users
```

This will result in a response that’ll contain every single user that exists in the database.

### Blind[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Blind)

Unlike the previous two types where there’s a response with some sort of data from the database server, blind SQL injections consider those cases where the response is not directly related to the database. These can be classified into two kinds. Let’s discuss both.

#### Boolean[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Boolean)

Suppose that there’s a query where the database confirms whether the user who’s logged in is an administrator:

```
query = "

SELECT *

FROM users

WHERE username = " &

Request.QueryString("username") & "

AND is_admin = TRUE"
```

Whatever the attacker inputs in the username, the response from the server will not respond with the result of this query, but there is a suspicious message in the browser’s console that says `failed`. Since the attacker’s recon phase has revealed that there is only one admin, they then decide to get craftier.

Let’s suppose that the admin’s username is `whataladmin`. If the attacker were to input the code below, they would notice that the message in the console is now `passed`.

```
# Check whether the first character of the password being retrieved is greater than 'y'.

' AND SUBSTRING((SELECT password FROM Users WHERE is_admin = TRUE), 1, 1) < 'y --`
```

If they try again with `'u`, they’ll notice that the message is failed. Trying with `= 'w` will reveal `passed` yet again. This confirms to the attacker that the password’s first character is `w`. In this way, the attacker can craft the admin account’s password.

#### Time based[#](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Time-based)

Consider the case where there’s no message being printed in the browser’s console. How will the adversary figure out the admin’s password now? Using differences in time, of course!

Simply appending the following before the double hyphen in the attacker’s input will ensure that if a correct character has been found, it will take 15 seconds before the login will fail.

```
= TRUE DELAY FOR '0:0:15'
```

> **Note:** Different databases handle time delays differently. Unlike what the attack type’s name suggests, we shouldn’t actually go testing out time delays blindly without checking the documentation first. Also, the syntax above for the time delay is just pseudocode.

Quiz Yourself on Cross-Site Scripting

Automatically Finding SQL Injections

Ask

[Overview](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Overview)

[How does an SQL injection work?](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#How-does-an-SQL-injection-work)

[Types of SQL injections](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Types-of-SQL-injections)

[Error based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Error-based)

[Union based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Union-based)

[Blind](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Blind)

[Boolean](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Boolean)

[Time based](https://www.educative.io/courses/web-application-penetration-testing/introduction-to-sql-injection#Time-based)