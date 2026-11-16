# Linux_Permissions_and_Process_Management_for_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Permissions and Process Management

Explore the essentials of Linux permissions and process management, including how to set and modify file access rights using chmod, chown, and chgrp commands. Understand how processes run and how to manage them effectively, critical skills for system administration and penetration testing.

We'll cover the following...

- [Introduction to process management](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Introduction-to-process-management)
- [File and directory permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-and-directory-permissions)
  - [File permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-permissions)
  - [Directory permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Directory-permissions)
- [Granting and revoking permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Granting-and-revoking-permissions)
  - [The chmod command](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chmod-command)
  - [The chown command](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chown-command)
  - [The chgrp commmand](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chgrp-commmand)
- [Managing processes](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Managing-processes)

## Introduction to process management[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Introduction-to-process-management)

The Linux operating system has hundreds if not thousands of processes running simultaneously. These can include the terminal, web servers, executed commands, and any databases that are running in the background or the foreground.

A system administrator or a pentester should be able to efficiently manage these processes. They need to understand that certain permissions have been granted to the different files and directories that form the Linux system.

In this lesson, we’ll learn about these files and directory permissions and the management of the different processes within the Linux system.

## File and directory permissions[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-and-directory-permissions)

The act of granting permission to different files and folders is a critical aspect of the Linux system. It’s used in the optimization of the system because it ensures that only the required tasks are running. This involves different access levels among the different users.

The Linux system has a way of securing files and directories through the segmentation of administrators (root users) and normal users. The segmentation allows the administrators the ownership of files and the ability to secure them as well.

We’ll cover the following commands:

## Commands for File and Directory Permissions

|  |  |
| --- | --- |
| **Command** | **Description** |
| `chmod` | This command modifies file access rights. |
| `su` | This command temporarily grants a user to be a superuser or have administrative privileges. |
| `sudo` | This command temporarily grants users superuser privileges for the execution of commands. It can be used in place of the `su` command. |
| `chown` | This command allows for changes in file ownership within the Linux system. |
| `chgrp` | This command enables a user to change group file ownership within the Linux system. |

### File permissions[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-permissions)

The Linux system has different file access rights depending on the creators among the system users. These rights include reading, writing, and executing files.

Using the `ls -l` command in the terminal below, we can view file permissions.

Terminal 1

Terminal

Loading...

As seen from the terminal, every file and directory is allocated a particular permission level unique to it. These levels of permission are:

- `r`: This allows users of the system to read the file.
- `w`: This grants the users of the system permission to write to or edit the file.
- `x`: This allows users to execute the file within the system.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTQxIiBoZWlnaHQ9IjIxMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

File permissions in the Linux file system

> **Note:** The `l` in some of the files indicates that this file is a **symlink** (a file that contains a link to another file), in contrast to `-`, which indicates a regular file, and `d`, which indicates a directory.

### Directory permissions[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Directory-permissions)

The octal notation is also used here; however, the meaning of read, write, and execute attributes are different, as described below:

- `r`: This allows for the content of the directory to be read.
- `w`: This allows for the creation, deletion, or even renaming of files within a directory.
- `x`: This allows users to change directories (i.e., `cd dir`).

For further illustration, here are some settings for when we’re working with directories:

## Directory Settings

|  |  |
| --- | --- |
| **Setting** | **Description** |
| `777 (rwxrwxrwx)` | Here, there are no restrictions on permissions to the directories, and therefore, anybody can list, create, and delete files in the directory. |
| `755 (rwxr-xr-x)` | This allows for the owner of the directory to have full access while others are able to just list the directory and do not have the rights to delete and or create files. |
| `700 (rwx------)` | This allows for only the directory owner to have full access rights, and it helps in enhancing privacy. |

## Granting and revoking permissions[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Granting-and-revoking-permissions)

Let’s look at how to adjust the permissions of the different files and directories.

- `chmod`: This is used to modify file access rights.
- `chown`: This is used to change file ownership.
- `chgrp`: This is used to change group file ownership.

### The `chmod` command[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chmod-command)

This command is used in changing file permissions by specifying the rights that a given file or directory within the system should have.

In the octal notation method, permission setting is done as a series of bits or binaries. From the understating of bit and binary, we can represent some of the permissions as shown below:

- The `rwx rwx rwx` notation is represented as `111 111 111` in binary.
- The `rwx r-x r--` notation is represented as `110 101 100` in binary.
- The `rwx r-- r--` notation is represented as `111 100 100` in binary.

Where:

- `rwx` represents `111` in binary and `7` in decimal.
- `rw-` represents `110` in binary and `6` in decimal.
- `r-x` represents `101` in binary and `5` in decimal.
- `r--` represents `100` in binary and `4` in decimal.

We can change permissions using decimal numbers in the Linux system. For example, suppose we had a file named `test.txt`, and we want only the directory owner to possess read and write permissions. In this case, we would use the `chmod` command with the digits and file name as our arguments: `chmod 600 test.txt`.

Terminal 1

Terminal

Loading...

The `chmod` command also uses **symbolic notation** for changing file permissions. These symbolic notations are mostly provided in three parts:

- Who is affected by changes in the system?
- Which operation will be performed in the system or server?
- What permission will be set in the system or server?

Symbolic notation uses a combination of the characters `u`, `g`, `o`, and `a`, as shown in the table below:

## Symbolic Notations

|  |  |
| --- | --- |
| Symbol | Meaning |
| `u` | This symbol is used to denote the user; however, it means the file or directory owner in the Linux system. |
| `g` | This means group owner. |
| `o` | This is a short form for others but means "world" or "anybody." |
| `a` | This is to denote all. Therefore, it combines the owner, group owner, and others with the Linux file permission system. |

When using the `chmod` command with symbolic notation, where there are no characters supplied as an argument, all is always assumed. Symbolic notation also uses the plus symbol (`+`) to indicate the addition of permissions, a negative symbol (`-`) to indicate the subtraction of permissions, or even the equal symbol (`=`) to indicate only specific permission is given to a file. These permissions are given using the `r`, `w`, and `x` characters. For example, using our `test.txt` file, we can execute `chmod u+x test.txt` to make our file executable. We can then apply the command `chmod u-x test.txt` to remove the execution permission from the file.

### The `chown` command[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chown-command)

The `chown` command is used to change the owner and group owner of a file or directory, and it requires superuser privileges for it to work. To do this, we use the `sudo` command for administrative purposes to execute `chown`. This command is used when there are different users with different access levels in the system.

The syntax for `chown` is somewhat similar to that of `chmod`, i.e., `sudo chown [owner][:[group]] file`.

### The `chgrp` commmand[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chgrp-commmand)

Only the root user can use `chown` for changing the ownership of a file. Other users can change the group permissions to another group they belong to. This minimizes the risks of accidentally breaking permissions for important files and directories.

## Managing processes[#](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Managing-processes)

The ability to multitask is the greatest benefit gained from modern operating systems. This means the OS can process different tasks by switching from one task to another. The system, through its kernel, can manage these tasks through the processes. **Processes** are the way the system arranges tasks or information that has been sent by the user to the CPU for execution.

Let’s now learn how to view, find, and delete a process within the Linux system:

## Commands for Managing Processes

|  |  |
| --- | --- |
| **Command** | **Description** |
| `ps` | This is used to get a list of processes that are running in the system. |
| `kill` | This sends a signal to a process, especially when we want to stop it (usually used to kill a process). |
| `jobs` | This command is used to list processes or tasks. |
| `bg` | This enables users to put a process in the background. |
| `fg` | This is used to put a process in the foreground. |

Be careful when killing processes, though, because confirming a kill may result in data loss or even system malfunction.

Software Management

Bash Scripting

Ask

[Introduction to process management](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Introduction-to-process-management)

[File and directory permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-and-directory-permissions)

[File permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#File-permissions)

[Directory permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Directory-permissions)

[Granting and revoking permissions](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Granting-and-revoking-permissions)

[The chmod command](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chmod-command)

[The chown command](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chown-command)

[The chgrp commmand](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#The-chgrp-commmand)

[Managing processes](https://www.educative.io/courses/web-application-penetration-testing/permissions-and-process-management#Managing-processes)