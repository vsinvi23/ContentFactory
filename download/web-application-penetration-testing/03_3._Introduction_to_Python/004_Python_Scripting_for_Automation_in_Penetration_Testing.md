# Python_Scripting_for_Automation_in_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/python-scripting

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Python Scripting

Explore Python scripting essentials to automate common penetration testing tasks on Linux systems. Learn how to retrieve IP addresses and create custom port scanners, enhancing your efficiency in web application security assessments using simple, effective scripts.

We'll cover the following...

- [Introduction to Python scripting](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Introduction-to-Python-scripting)
  - [Structure of a Python script](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Structure-of-a-Python-script)
- [Scripting to automate basic pentesting task](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Scripting-to-automate-basic-pentesting-task)
  - [Getting an IP address](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Getting-an-IP-address)
  - [Custom port scanner](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Custom-port-scanner)

## Introduction to Python scripting[#](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Introduction-to-Python-scripting)

In penetration testing, writing scripts that automate system tasks is critical knowledge. These scripts help carry out tasks in the Linux environment without the need for compilation every time. It also mitigates the tediousness of a lot of tasks since pentesters find themselves performing the same procedures over and over again.

### Structure of a Python script[#](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Structure-of-a-Python-script)

Python scripting is very similar to Bash scripting; there’s largely only the difference of language syntax.

Let’s create a simple Python script so that we can get familiar with both the structure and process. Let’s start with `greetings.py`.

Create the aforementioned file in the terminal below and ensure it has the following:

```
#!/usr/bin/python3

school = "Educative"

print("Greetings to our students and welcome to "+ school +". Dare I say, the best place to level up your developer skills.")
```

Once the file is ready and permissions have been set up, we can then execute our script with the following command: `./greetings.py`.

Terminal 1

Terminal

Click to Connect...

W

## Scripting to automate basic pentesting task[#](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Scripting-to-automate-basic-pentesting-task)

Let’s look at a few examples of what we can do with Python. Keep in mind that these tasks can also be automated with Bash scripts or even single-line commands with the help of piping, though the latter is a somewhat advanced technique. At the end of the day, it’s about using whatever tools we’re comfortable with to get the job done.

### Getting an IP address[#](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Getting-an-IP-address)

To get the IP address of a device using Python, we can use the `socket` module.

Look below to see how we can grab the IP of our own device, i.e., the Linux machine that is running the code playground:

Python 3.8

```
import socket

# Get the hostname of the device.

hostname = socket.gethostname()

# Get the IP address using the hostname.

ip_address = socket.gethostbyname(hostname)

# Print the IP address.

print(ip_address)
```

⋯

Simple Python script to find out the IP address of the host

### Custom port scanner[#](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Custom-port-scanner)

Scanning for open ports and discovering what services they’re running are among the first things pentesters usually do. There are various reasons for doing so:

- Some services may have publicly known exploits.
- Others may have outdated versions that are vulnerable.
- To utilize the knowledge of the services being used to map the rest of the network.
- Simply for baseline information gathering purposes.

Sophisticated port scanners with a wide range of features and plug-ins do exist: Nmap is highly popular, and Metasploit houses a number of auxiliary scripts to aid in scanning. Nevertheless, it’s still good to know how to write our own scripts in case we need to get the job done without those.

Python 3.8

```
# Now would be a good time to brush up on the basics of socket programming.

import socket

# We grab the IP of the machine running this playground.

target = socket.gethostbyname(socket.gethostname())

ports = []

# Scan all ports between the defined range.

for port in range(1, 65535):

check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

scanned = check.connect_ex((target, port))

if scanned == 0:

ports.append(port)

# Always remember to close connections in our scripts.

check.close()

# Since there are no explicitly open ports on this machine, we should see an empty list most of the time.

# Sometimes, we may see random open ports between 30000 and 65535; these are often false flags.

# We should be able to deduce what is and isn't a false flag in due time.

print("Possible open ports:", ports)
```

⋯

A simple port scanner

Control Flow

Quiz Yourself on Python Basics

Ask

[Introduction to Python scripting](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Introduction-to-Python-scripting)

[Structure of a Python script](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Structure-of-a-Python-script)

[Scripting to automate basic pentesting task](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Scripting-to-automate-basic-pentesting-task)

[Getting an IP address](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Getting-an-IP-address)

[Custom port scanner](https://www.educative.io/courses/web-application-penetration-testing/python-scripting#Custom-port-scanner)