# Linux_Software_Management_with_apt-get_Commands

Source: https://www.educative.io/courses/web-application-penetration-testing/software-management

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Software Management

Understand key Linux package management commands using apt-get on Debian-based systems. This lesson helps you confidently install, update, upgrade, remove, and purge software packages from the terminal while managing dependencies and configurations.

We'll cover the following...

- [Introduction to package management](https://www.educative.io/courses/web-application-penetration-testing/software-management#Introduction-to-package-management)
  - [The apt-get update command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-update-command)
  - [The apt-get upgrade command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-upgrade-command)
  - [The apt-get install command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-install-command)
  - [The apt-get remove command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-remove-command)
  - [The apt-get purge command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-purge-command)
- [Demo](https://www.educative.io/courses/web-application-penetration-testing/software-management#Demo)

## Introduction to package management[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#Introduction-to-package-management)

In the default Debian-based Linux operating system distributions, the default software management is the Advanced Package Tool, commonly referred to as `apt`.

The primary command for this is `apt-get`, which is used to download, install, update, and remove software packages.

### The `apt-get update` command[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-update-command)

This command updates most or all software packages that are available within a repository. However, it does not perform the overall system update because it is limited to just user applications on the system.

### The `apt-get upgrade` command[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-upgrade-command)

This command is used to enhance the packages in a system to the latest version available in the repository. Unlike `apt-get update`, it performs the overall system upgrade.

> **Note:** The system upgrade makes changes to the software. For the command to work efficiently, we must be logged in as the administrator of the system. Upgrading the system can be time-consuming depending on the type of computer hardware specification that we’re using; however, it’s best when it comes to repairing the vulnerabilities within the Linux software packages.

### The `apt-get install` command[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-install-command)

This command enables users to install software packages via the terminal. If the packages are available in the `apt` repository, then they’ll be downloaded. Sometimes during installations, we may be prompted to accept or decline the installation process; we can skip this with the `-y` argument.

### The `apt-get remove` command[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-remove-command)

This command enables us to remove a software package from the system. When removing software that we’ve installed, we simply use `apt-get remove` and the name of the program that we’d like to remove.

> **Note:** This deletes the software package but not the configuration files. We can therefore reinstall the software without reconfiguring it.

### The `apt-get purge` command[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-purge-command)

This command enables users of the Linux system to remove software packages with all their dependencies and configuration files. For example, when we install nano (a text editor), the process comes with several dependencies or libraries with it that are required for it to run successfully.

## Demo[#](https://www.educative.io/courses/web-application-penetration-testing/software-management#Demo)

In the terminal below, let’s use the commands that we’ve just learned to install nano, uninstall it, install it again, and then purge it.

Terminal 1

Terminal

Loading...

Git and Git Version Control

Permissions and Process Management

Ask

[Introduction to package management](https://www.educative.io/courses/web-application-penetration-testing/software-management#Introduction-to-package-management)

[The apt-get update command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-update-command)

[The apt-get upgrade command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-upgrade-command)

[The apt-get install command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-install-command)

[The apt-get remove command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-remove-command)

[The apt-get purge command](https://www.educative.io/courses/web-application-penetration-testing/software-management#The-apt-get-purge-command)

[Demo](https://www.educative.io/courses/web-application-penetration-testing/software-management#Demo)