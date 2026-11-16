# Network_Information_Modification_Techniques_for_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Modification of Network Information

Explore how to modify network information including IP addresses, network masks, broadcast addresses, and MAC addresses. Understand the implications of these changes in network security, how attackers use these techniques, and the importance of these skills in penetration testing and defending network systems.

We'll cover the following...

- [Modifying the network](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modifying-the-network)
  - [Modification of IP address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-IP-address)
  - [Modification of network mask and broadcast address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-network-mask-and-broadcast-address)
  - [Changing the MAC address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Changing-the-MAC-address)

## Modifying the network[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modifying-the-network)

Modification of network information is an essential skill because it helps a user of the system to access the network while appearing as a trusted device. A system administrator should be careful since somebody can modify network information and launch a DDoS (denial-of-service) attack on the web server using a spoofed IP address. Man-in-the-middle attacks can also be performed by an attacker pretending to be our intended recipient. Let’s now look at how an attacker can modify network information.

> **Note:** Trying to modify `eth0` in our terminals will unfortunately close our connection to it.

### Modification of IP address[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-IP-address)

A hacker can change their IP address in the network using the `ifconfig` command. The `ifconfig` command enables the hacker to reassign the IP address, which helps them evade IP capture during forensic analysis. Assigning an IP address for an interface in the system has the following syntax: `ifconfig <interface> <IP address of your choice>`.

If we check `eth0` on our standalone system, we’ll find that the machine’s IP address is 172.17.0.2, as shown below:

```
┌──(root㉿6a44e00aa4f40b3f)-[/]

└─# ifconfig eth0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500

inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255

inet6 fe80::40e0:74ff:fe6f:10d  prefixlen 64  scopeid 0x20<link>

ether 42:e0:74:6f:01:0d  txqueuelen 1000  (Ethernet)

RX packets 423  bytes 48192 (47.0 KiB)

RX errors 0  dropped 0  overruns 0  frame 0

TX packets 302  bytes 50303 (49.1 KiB)

TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

We can change this IP address by using the following comnand: `ifconfig eth0 172.17.12.7`. Trying this out below will result in the following change:

```
┌──(root㉿92d0fea2f9de1285)-[/]

└─# ifconfig eth0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500

inet 172.17.12.7 netmask 255.255.0.0  broadcast 172.17.255.255

inet6 fe80::9cbd:7cff:fe45:172e  prefixlen 64  scopeid 0x20<link>

ether 9e:bd:7c:45:17:2e  txqueuelen 1000  (Ethernet)

RX packets 431  bytes 48708 (47.5 KiB)

RX errors 0  dropped 0  overruns 0  frame 0

TX packets 304  bytes 50377 (49.1 KiB)

TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### Modification of network mask and broadcast address[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-network-mask-and-broadcast-address)

Users of the system can also modify their network mask and broadcast address in a network. The **network mask** indicates the range of IP addresses assignable to devices in the internal network. For example, a network mask of 255.255.0.0 means that there can be 65,534 devices in the network. The broadcast address simply means that all the devices in a network are reachable despite not knowing their specific IP addresses. For example, the value 172.17.255.255 means that all the devices in the network will have IP addresses like 172.17.12.71 or 172.17.193.34. The reasons for modifying these values are similar to the reasons why hackers would want to change IP addresses.

Entering `ifconfig eth0 117.120.170.110 netmask 255.255.255.0 broadcast 117.120.1.255` will make changes to the IP address, network mask address, and broadcast address, respectively.

### Changing the MAC address[#](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Changing-the-MAC-address)

The **MAC (media access control) address** is a unique address that identifies the devices connected in a network. An example of a MAC address is 9e:bd:7c:45:17:2e (the value of Ether when we run `ifconfig`). Because this is unique, it can be used to trace hackers since it’s hardcoded into the system. Modifying the MAC address is possible, but the BIA (burned-in MAC address) will always remain and be reverted to once the override is reverted. Investigators can then use the BIA values to find out where the hacker’s hardware was sourced from.

As web pentesters, we must be aware that this hardware code can be modified and can give us a false alert from where the attack is coming. Changing the MAC address is also a critical skill for bypassing network access controls in a system.

To change the MAC address of `eth0`, we use the following set of commands:

```
ifconfig eth0 down

ifconfig eth0 hw ether 00.44.77.88.99.66

ifconfig eth0 up
```

It’s important to note that the network interface must first be disabled in order to change the MAC address.

Network Analysis Using ifconfig and iwconfig

Modification of Domain Name System

Ask

[Modifying the network](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modifying-the-network)

[Modification of IP address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-IP-address)

[Modification of network mask and broadcast address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Modification-of-network-mask-and-broadcast-address)

[Changing the MAC address](https://www.educative.io/courses/web-application-penetration-testing/modification-of-network-information#Changing-the-MAC-address)