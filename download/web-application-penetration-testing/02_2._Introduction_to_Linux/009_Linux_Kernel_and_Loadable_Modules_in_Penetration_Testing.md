# Linux_Kernel_and_Loadable_Modules_in_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Linux Kernel and Loadable Modules

Explore the role of the Linux kernel and loadable modules in system control. Understand how to check kernel status, manage loadable modules, and safely tune kernel settings. This lesson enhances your ability to handle kernel interactions carefully during web application penetration testing.

We'll cover the following...

- [Introduction to the kernel](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Introduction-to-the-kernel)
  - [Kernel modules](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-modules)
    - [Checking the kernel status](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Checking-the-kernel-status)
  - [Kernel tuning](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-tuning)

## Introduction to the kernel[#](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Introduction-to-the-kernel)

The **kernel** is the central engine that controls everything in the operating system. Administrative privileges can change how the system works, looks, and feels in operation. This means that an unauthorized person can change any of the given operations within the system.

A pentester needs to be very careful when accessing the kernel because any wrong change in how the operating system works would result in crashing a web server or the operating system. Keeping this in mind, we’ll now examine the modules of the kernel and how to manage them.

### Kernel modules[#](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-modules)

When a user with administrative privileges working on the Linux system installs a driver in the kernel, that user has to rebuild, compile, and reboot the entered system so that the changes can take effect in the kernel. These modules are known as **loadable kernel modules**. This means that when adversaries successfully manage to get a hold of the Linux kernel system, they can control the system. Understanding loadable kernel modules is necessary to be an effective pentester, system administrator, and sneaky hacker.

#### Checking the kernel status[#](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Checking-the-kernel-status)

For a pentester, the first thing to do before checking the kernel version is to check whether the kernel is working or running.

This is done using the command `uname` followed by `-a` as an argument:

Terminal 1

Terminal

Click to Connect...

W

As we can see, the kernel responds by telling us the distribution of the operating system in Linux and the kernel build.

> **Note:** The output is dependent on the operating system and hardware, so the output will differ on different machines.

Another way to get the information above is by the use of the `cat` command on the `/proc/version` file `cat /proc/version`. We can verify this in the terminal above.

### Kernel tuning[#](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-tuning)

When we have the right commands, we can tune the kernel by changing the memory allocations, enabling and disabling networking features, and even hardening it against outside attacks.

The recent version of the Linux system uses the `sysctl` command for tuning the kernel. However, these changes can only be added after rebooting the system. To make permanent changes in the kernel when tuning it, the system administrators can edit the `sysctl` configurations directly in the `/etc/sysctl.conf` file.

> **Note:** Be very careful when using `sysctl` since any wrong configuration here can crash the entire system and make it unbootable.

Let’s use `sysctl -a | less` in the terminal below. Press the “Enter” key to scroll through the available modules. Finally, press the “Q” key to exit the kernel modules.

Terminal 1

Terminal

Loading...

System Logging

Quiz Yourself on Basic Linux Commands

Ask

[Introduction to the kernel](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Introduction-to-the-kernel)

[Kernel modules](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-modules)

[Checking the kernel status](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Checking-the-kernel-status)

[Kernel tuning](https://www.educative.io/courses/web-application-penetration-testing/linux-kernel-and-loadable-modules#Kernel-tuning)