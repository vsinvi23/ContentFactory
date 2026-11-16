# Learning_Bash_Scripting_for_Linux_Automation_and_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/bash-scripting

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Bash Scripting

Explore the essentials of Bash scripting to automate tasks in Linux environments. Learn how to create, execute, and manage shell scripts, from simple greetings to practical scripts like fetching an IP address. This lesson builds foundational scripting skills pivotal for penetration testers and system administrators working in automation and task efficiency.

We'll cover the following...

- [Introduction to Bash scripting](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Introduction-to-Bash-scripting)
  - [Creating our first script](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-our-first-script)
  - [Creating a more practical script](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-a-more-practical-script)

## Introduction to Bash scripting[#](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Introduction-to-Bash-scripting)

Every hacker, pentester, or system administrator must be able to write scripts that can be used in the automation of the different tasks.

The **shell** is an application interface between an operating system and the user. It enables the user to run commands to control the different programs in the Linux operating system. It’s also a scripting language interpreter.

For the successful creation and running of shell scripts, we need to keep in mind the following general steps:

1. Write a script as ordinary text files. Ensure that they have the `.sh` extension. Complicated and long scripts will require the use of an editor like Vim, which we discussed in a previous lesson.
2. Make the script file executable by giving permissions to allow execution. This can be accomplished by using `chmod`.
3. Ensure that other necessary files and dependencies are available with the proper paths.
4. Execute the script and enjoy your free time. Or read the logs.

### Creating our first script[#](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-our-first-script)

Keeping in mind all that we’ve learned up till now, use the terminal below to create a shell script called `greetings.sh`, and ensure that it has the following four lines in it:

```
#!/bin/bash

#Make sure that the first line is '!/bin/bash'.

#This tells the OS to use Bash for command interpretation.

echo 'Hello World!'
```

Then execute the script with `./greetings.sh`. Upon execution, we should see the following greeting:

```
Hello World!
```

Terminal 1

Terminal

Click to Connect...

W

### Creating a more practical script[#](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-a-more-practical-script)

Now that we know the basics of creating and executing Bash scripts, let’s try to do something a bit more complicated.

Let’s make a rough script to fetch the IP address of our computer. This can also be achieved with various built-in functions and commands, but the purpose of the exercise is to check out some of the intricacies of Bash scripting.

Shell

```
#!/bin/bash

# Get the specific line from 'ip addr' that pertains to the ethernet adapter.

process=$(ip addr | grep inet | grep eth0)

# Get the length of contents of the variable 'process'.

length=${#process}

# The empty variable where we'll keep appending the characters for our IP address.

ipAddress=""

# A for-loop that runs the full length of the original 'process' string.

# A while-loop could have been used.

for ((i = 0 ; i < length ; i++)); do

# We grab the first character from 'process'.

# We check whether this character is a number or a period.

if [[ ${process:0:1} =~ ^[0-9.]+$ ]]; then

# We append the character to 'ipAddress'

ipAddress+=${process:0:1}

# If the next character is a forward slash, we prematurely break out of the loop.

if [[ ${process:1:1} == "/" ]]; then

break

fi

fi

# We remove the first character (that we used for the earlier comparisons) from the string.

process="${process:1:length}"

done

echo "Through our own script:" ${ipAddress}

echo "Through an inbuilt function:" $(hostname -I)
```

⋯

A simple Bash script

Those are a lot of new concepts. Bash scripting is tricky even for those who possess prior programming experience. It requires a lot of practice, and unlike languages such as Python and Ruby (which any pentester should also be familiar with), it’s impossible to grasp it overnight. In Python, for instance, this script would’ve been much shorter and human readable.

Keep working on improving your Bash scripting skills whenever you can. Quite often, we’ll find ourselves working in environments where it’s the only option left for automation. This lesson is meant to be a brief introduction, but we encourage you to look further into Bash scripting yourself.

Permissions and Process Management

System Logging

Ask

[Introduction to Bash scripting](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Introduction-to-Bash-scripting)

[Creating our first script](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-our-first-script)

[Creating a more practical script](https://www.educative.io/courses/web-application-penetration-testing/bash-scripting#Creating-a-more-practical-script)