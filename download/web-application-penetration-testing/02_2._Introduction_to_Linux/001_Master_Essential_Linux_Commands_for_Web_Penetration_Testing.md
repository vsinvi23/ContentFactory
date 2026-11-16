# Master_Essential_Linux_Commands_for_Web_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/linux-commands

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Linux Commands

Explore fundamental Linux commands critical for effective penetration testing, including directory listing, file management, and directory navigation. Understand how to use commands like ls and cd to navigate the Linux file system and manage permissions. Gain hands-on practice in a terminal to build confidence using the command line interface, which is vital for operating penetration testing tools within Linux environments.

We'll cover the following...

- [Introduction to Linux commands](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Introduction-to-Linux-commands)
- [List directory command](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#List-directory-command)
- [Change directory command](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Change-directory-command)
- [Playground](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Playground)

## Introduction to Linux commands[#](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Introduction-to-Linux-commands)

Most installations of new software on the Linux operating system take place on the terminal. In fact, operations to update and uninstall software must also be performed on the terminal. Even using certain software may require extensive use of the terminal, which makes being familiar with the command-line interface (CLI) very important. Then there’s creating files, editing them, moving them around, changing their permissions, and a plethora of operations that many users today take for granted with a simple mouse click. As such, we will be using terminals throughout the course, especially since some of the most powerful penetration testing tools are best used on the CLI.

## List directory command[#](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#List-directory-command)

A good starting point would be to find out how to check the contents of folders on the terminal. Information on what kinds of files are available on the system, when they were made, who made them, etc., may all come in handy during penetration tests. For example, the `shadow` and `passwd` files in the `etc` folder hold user account and password details, respectively. When we gain unauthorized access to a system, attaining these files is usually an important step.

To list the contents of the current directory, we use the `ls` command. Relative paths can also be provided to check the contents of folders we are not currently in. `ls` also accepts a number of useful options:

- `ls -l`: The `-l` option lets us look at the long listing of directories. This outputs not just the files and directories but their owners, filegroups, sizes, dates, and times of modification.
- `ls -lh`: This option decreases the precision in the description of the file size. Instead of bytes, we get to see file sizes in megabytes, kilobytes, etc.
- `ls -a`: This options allows us to view hidden files. Some files are hidden because they may contain sensitive information or to prevent them from accidental deletion. In Linux and macOS, hidden files begin with a period; for example, `.dockerenv` and `.bashrc` are hidden files.
- `ls -al`: This option simply provides the long listing of hidden files as well.

## Change directory command[#](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Change-directory-command)

It is pertinent to know how to change our current working directory. We can use the `cd` command like so: `cd <name of directory>`. For example, if we’re in `home` and would like to switch to `usr` (both `home` and `usr` are in the root directory), we would use `cd /usr`. If we’re in `opt` and would like to switch to a folder called `google` inside `opt` itself, we would use `cd google`. To quickly go to the root directory, `cd /` will work.

The `cd` command also comes with a couple of useful options:

- `cd -`: This option will change our current directory to the one we previously came from.
- `cd ..`: This option will switch us back to the parent directory.

## Playground[#](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Playground)

Practice makes perfect. As such, try out all the commands discussed above in the terminal below. For the `cd` commands, note the change in the path as you run them.

Terminal 1

Terminal

Loading...

> **Note:** Sometimes, the terminal may not be as verbose or we may get a bit too engrossed in a task and may forget our current working directory. Of course, we could use a combination of `ls` and `cd` to figure it out, but there is also another simpler way; just use `pwd`.

Getting Started

Linux File System

Ask

[Introduction to Linux commands](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Introduction-to-Linux-commands)

[List directory command](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#List-directory-command)

[Change directory command](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Change-directory-command)

[Playground](https://www.educative.io/courses/web-application-penetration-testing/linux-commands#Playground)