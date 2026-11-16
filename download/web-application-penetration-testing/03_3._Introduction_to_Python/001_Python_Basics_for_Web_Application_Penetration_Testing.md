# Python_Basics_for_Web_Application_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/python-basics

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Python Basics

Explore the essentials of Python programming tailored for penetration testing. Understand how to write and interpret Python scripts, use prebuilt libraries, manipulate strings, and perform arithmetic operations to automate security tasks efficiently.

We'll cover the following...

- [Introduction to Python](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Introduction-to-Python)
  - [What’s so good about Python 3?](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Whats-so-good-about-Python-3)
- [Using Python](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Using-Python)
  - [String manipulation](https://www.educative.io/courses/web-application-penetration-testing/python-basics#String-manipulation)
  - [Arithmetic](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Arithmetic)

## Introduction to Python[#](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Introduction-to-Python)

Python is the most widely used language for scripting a wide range of tasks performed by hackers, pentesters, and system administrators. Scripting skills in Python are critical for one to become a master pentester or hacker.

Python has prebuilt library modules that can be easily imported, used, and reused. These libraries allow users to quickly automate tedious tasks in a few lines of highly readable code. As such, being able to read and write Python scripts is essential.

We will approach Python programming from the information security perspective. We’ll be using Python 3 for this course but it should be noted that certain tools and scripts require Python 2 to function.

### What’s so good about Python 3?[#](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Whats-so-good-about-Python-3)

Python 3 is the latest major version of Python (at the time of writing). A lot of improvements have been made to increase the efficiency and simplicity of written code, allowing many users, even first-time learners, to quickly make use of its versatility. Also, most Linux operating systems come preinstalled with Python 3. We can confirm this with `python3 --version`.

Python can be used to quickly spin up servers for further data analysis of output gained from other tools, check transmission of network traffic, and many other things. In fact, with knowledge of socket programming, we could mimic the functionalities of popular tools such as Nmap and Metasploit to a decent extent with our own custom scripts.

## Using Python[#](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Using-Python)

Python can be used in two main ways:

- We can run a script with `python3 <script_name>.py argument_1 argument_2 ...`. For example, let’s assume there’s a script called `data.py` that asks us for a name and age. We would use the command `python3 data.py David 26`.
- We can use the interpreter. Simply enter `pyhton3` in a terminal and we’ll be taken to the interpreter. This is largely used for quick arithmetic operations. We can quit the interpreter using `exit()`.

### String manipulation[#](https://www.educative.io/courses/web-application-penetration-testing/python-basics#String-manipulation)

Python 3 makes working with strings very convenient. Those who’re familiar with languages such as C++ or Java will find that the ease of use can end up saving hours of their time.

Let’s look at the script below. It details various ways to play around with strings. These are, of course, just baby steps. Make sure to check out the official Python documentation for more advanced things that can be done.

Python 3.8

```
# Simple print statement.

print("Hello World!")

# Let's use a bit of formatting.

print("Hello World!\nHow are you doing?\nI\'m quite alright.")

# We can store strings in variables and print them too.

statement = "This is a bold statement!"

print(statement)

# Let's try to index and slice the contents of 'statement' now.

question = statement[5] + statement[15] + statement[0:4] + statement[-17] + statement[15:] + '?'

print(question)

# What about cases?

statement.upper

print(statement)

statement.lower

print(statement)

# How about joining together a list of strings?

introduction = ' '.join(['My', 'name', 'is', 'David'])

groceries_list = ','.join(['bananas', 'milk', 'bread'])

print(introduction)

print(groceries_list)

# Now let's do the opposite.

introduction = introduction.split()

groceries_list = groceries_list.split(',')

print(introduction)

print(groceries_list)
```

⋯

A brief introduction to basic string manipulation

### Arithmetic[#](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Arithmetic)

Let’s now perform some arithmetic operations in the Python interpreter. You should first do the math yourself and then confirm with the interpreter. The order of operations matters a lot.

```
40 + 30

40 / 20

40 // 20

60 - 30

70 * 10

(40 / 10) * 20

(340 - (45 * 32) / 34 + (23 - -23)) // 10
```

Terminal 1

Terminal

Loading...

Quiz Yourself on Basic Linux Commands

Variables, Functions, and Lists

Ask

[Introduction to Python](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Introduction-to-Python)

[What’s so good about Python 3?](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Whats-so-good-about-Python-3)

[Using Python](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Using-Python)

[String manipulation](https://www.educative.io/courses/web-application-penetration-testing/python-basics#String-manipulation)

[Arithmetic](https://www.educative.io/courses/web-application-penetration-testing/python-basics#Arithmetic)