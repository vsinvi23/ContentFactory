# Understanding_Web_Proxies_and_Their_Role_in_Network_Security

Source: https://www.educative.io/courses/web-application-penetration-testing/proxies

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Proxies

Explore the concept of proxies in web security by understanding how forward, open, and reverse proxies function. Learn to set up proxy servers and configure proxy chains using proxychains4 to anonymize traffic, enhancing your skills in managing and securing network communications during penetration testing.

We'll cover the following...

- [Introduction to proxies](https://www.educative.io/courses/web-application-penetration-testing/proxies#Introduction-to-proxies)
  - [Type of proxies](https://www.educative.io/courses/web-application-penetration-testing/proxies#Type-of-proxies)
    - [Forward proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Forward-proxy)
    - [Open proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Open-proxy)
  - [Reverse proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Reverse-proxy)
  - [Setting up a proxy server](https://www.educative.io/courses/web-application-penetration-testing/proxies#Setting-up-a-proxy-server)

## Introduction to proxies[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Introduction-to-proxies)

When users are browsing the internet, their data is sent or tagged with their IP address, making it easier to track their web activities. When we take a deeper look, we see that when a user sends a packet request, the packet contains the IP address of the source (i.e., the user), which helps the receiver to identify where it should send the response back. Keep in mind that if the packet is intercepted as it traverses the internet, the interceptor can see the packet's destination and source. Anyway, websites will always be able to tell who the packet belongs to and subsequently log the user's activity. Trying to mitigate this tracking is where proxies come in.

A web proxy is a server that stands between the user's browser and the rest of the internet. It serves many purposes: blocking access to certain websites, circumventing the blocking of websites, acting as a tool for browsing anonymously, intercepting traffic, and many more.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzYxIiBoZWlnaHQ9IjE5MiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

A proxy server can be thought of as a guard

### Type of proxies[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Type-of-proxies)

#### Forward proxy[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Forward-proxy)

A **forward proxy** allows the user to request their internal network server to forward their packet or information to the internet. The proxy server makes the request on the internet on behalf of the client in the internal network. The receiving server doesn’t know what the exact user identification is or where the request is specifically coming from.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDc0IiBoZWlnaHQ9IjI1MiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

The forward proxy server speaks for the collective

#### Open proxy[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Open-proxy)

An **open proxy** allows any user to connect to it and be anonymous while browsing the internet.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDcwIiBoZWlnaHQ9IjMyNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

The open proxy can be used by anyone

### Reverse proxy[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Reverse-proxy)

A **reverse proxy** does the request processing as it's being forwarded to several proxies in which the feedback is retrieved as it came directly from the original server. It's used to prevent internet users from having direct access to sensitive data that's in the isolated network.

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjUxIiBoZWlnaHQ9IjI5MSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2ZXJzaW9uPSIxLjEiLz4=)

A reverse proxy isolates a network from the rest of the internet

### Setting up a proxy server[#](https://www.educative.io/courses/web-application-penetration-testing/proxies#Setting-up-a-proxy-server)

A proxy server acts as a middleman for the traffic that’s moving between the client and server. The user can connect to the proxy and is given an IP address from the proxy before the traffic is passed to the server. In this way, the network traffic appears to be coming from the proxy and not from the client within the network. Proxy servers, especially free ones, normally log the user’s traffic, meaning it can be tracked easily. To make traffic difficult to trace, hackers or adversaries use more than one proxy. This is known as a **proxy chain**.

Most security-focused operating systems, such as Kali or Parrot Linux, come configured with proxy chains that we can configure to anonymize the traffic that’s coming from the user’s network.

We’ll use the latest version of ProxyChains, which is aptly named proxychains4. The syntax for it is:

```
proxychains4 <command from user> <arguments>
```

The proxies can be configured in `proxychains4.conf`, which is usually found in `/etc/`. We should check the contents using the `cat` command.

In the playground below, you’ll see `proxychains4.conf`. We’ve edited it so you can test out a basic proxy chain. Click the “Run” button to check it out:

```
# proxychains.conf  VER 4.x
#
#        HTTP, SOCKS4a, SOCKS5 tunneling proxifier with DNS.

# The option below identifies how the ProxyList is treated.
# only one option should be uncommented at a time,
# otherwise the last appearing option will be accepted
#
dynamic_chain
#
# Dynamic - Each connection will be done via chained proxies
# all proxies chained in the order as they appear in the list
# at least one proxy must be online to play in chain
# (dead proxies are skipped)
# otherwise EINTR is returned to the app
#
#strict_chain
#
# Strict - Each connection will be done via chained proxies
# all proxies chained in the order as they appear in the list
# all proxies must be online to play in chain
# otherwise EINTR is returned to the app
#
#round_robin_chain
#
# Round Robin - Each connection will be done via chained proxies
# of chain_len length
# all proxies chained in the order as they appear in the list
# at least one proxy must be online to play in chain
# (dead proxies are skipped).
# the start of the current proxy chain is the proxy after the last
# proxy in the previously invoked proxy chain.
# if the end of the proxy chain is reached while looking for proxies
# start at the beginning again.
# otherwise EINTR is returned to the app
# These semantics are not guaranteed in a multithreaded environment.
#
#random_chain
#
# Random - Each connection will be done via random proxy
# (or proxy chain, see  chain_len) from the list.
# this option is good to test your IDS :)

# Make sense only if random_chain or round_robin_chain
#chain_len = 2

# Quiet mode (no output from library)
#quiet_mode

## Proxy DNS requests - no leak for DNS data
# (disable all of the 3 items below to not proxy your DNS requests)

# method 1. this uses the proxychains4 style method to do remote DNS:
# a thread is spawned that serves DNS requests and hands down an IP
# assigned from an internal list (via remote_dns_subnet).
# this is the easiest (setup-wise) and fastest method, however on
# systems with buggy libcs and very complex software like webbrowsers
# this might not work and/or cause crashes.
proxy_dns

# method 2. use the old proxyresolv script to proxy DNS requests
# in proxychains 3.1 style. requires `proxyresolv` in $PATH
# plus a dynamically linked `dig` binary.
# this is a lot slower than `proxy_dns`, doesn't support .onion URLs,
# but might be more compatible with complex software like webbrowsers.
#proxy_dns_old

# method 3. use proxychains4-daemon process to serve remote DNS requests.
# this is similar to the threaded `proxy_dns` method, however it requires
# that proxychains4-daemon is already running on the specified address.
# on the plus side it doesn't do malloc/threads so it should be quite
# compatible with complex, async-unsafe software.
# note that if you don't start proxychains4-daemon before using this,
# the process will simply hang.
#proxy_dns_daemon 127.0.0.1:1053

# set the class A subnet number to use for the internal remote DNS mapping
# we use the reserved 224.x.x.x range by default,
# if the proxified app does a DNS request, we will return an IP from that range.
# on further accesses to this ip we will send the saved DNS name to the proxy.
# in case some control-freak app checks the returned IP, and denies to 
# connect, you can use another subnet, e.g. 10.x.x.x or 127.x.x.x.
# of course you should make sure that the proxified app does not need
# *real* access to this subnet. 
# i.e. dont use the same subnet then in the localnet section
#remote_dns_subnet 127 
#remote_dns_subnet 10
remote_dns_subnet 224

# Some timeouts in milliseconds
tcp_read_time_out 15000
tcp_connect_time_out 8000

### Examples for localnet exclusion
## localnet ranges will *not* use a proxy to connect.
## note that localnet works only when plain IP addresses are passed to the app,
## the hostname resolves via /etc/hosts, or proxy_dns is disabled or proxy_dns_old used.

## Exclude connections to 192.168.1.0/24 with port 80
# localnet 192.168.1.0:80/255.255.255.0

## Exclude connections to 192.168.100.0/24
# localnet 192.168.100.0/255.255.255.0

## Exclude connections to ANYwhere with port 80
# localnet 0.0.0.0:80/0.0.0.0
# localnet [::]:80/0

## RFC6890 Loopback address range
## if we enable this, we have to make sure remote_dns_subnet is not 127
## we'll need to enable it if we want to use an application that 
## connects to localhost.
# localnet 127.0.0.0/255.0.0.0
# localnet ::1/128

## RFC1918 Private Address Ranges
# localnet 10.0.0.0/255.0.0.0
# localnet 172.16.0.0/255.240.0.0
# localnet 192.168.0.0/255.255.0.0

### Examples for dnat
## Trying to proxy connections to destinations which are dnatted,
## will result in proxying connections to the new given destinations.
## Whenever I connect to 1.1.1.1 on port 1234 actually connect to 1.1.1.2 on port 443
# dnat 1.1.1.1:1234  1.1.1.2:443

## Whenever I connect to 1.1.1.1 on port 443 actually connect to 1.1.1.2 on port 443
## (no need to write :443 again)
# dnat 1.1.1.2:443  1.1.1.2

## No matter what port I connect to on 1.1.1.1 port actually connect to 1.1.1.2 on port 443
# dnat 1.1.1.1  1.1.1.2:443

## Always, instead of connecting to 1.1.1.1, connect to 1.1.1.2
# dnat 1.1.1.1  1.1.1.2

# ProxyList format
#       type  ip  port [user pass]
#       (values separated by 'tab' or 'blank')
#
#       only numeric ipv4 addresses are valid
#
#
#        Examples:
#
#               socks5  192.168.67.78   1080    lamer   secret
#               http    192.168.89.3    8080    justu   hidden
#               socks4  192.168.1.49    1080
#               http    192.168.39.93   8080
#
#
#       proxy types: http, socks4, socks5, raw
#         * raw: The traffic is simply forwarded to the proxy without modification.
#        ( auth types supported: "basic"-http  "user/pass"-socks )
#
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
socks5 127.0.0.1 9050
```

Note the change in IP addresses between the normal curl and proxied curl commands

We’ve set up proxychains4 to use dynamic chaining, and we’re also using the basic `proxy_dns` to speed up the IP assignment process. At the end of the file, we’ve also set up our first (and only) link in the chain using the SOCKS5 protocol. SOCKS5 is used by proxies to do the routing of the different packets between the users and requests that have been made to a server. The 127.0.0.1 protocol is a loopback protocol for the localhost machine, and `9050` is the port number for listening to inbound and outbound traffic.

Every time we restart the `tor` service, a new IP is assigned whenever we use proxychains4 with the `curl https://suip.biz/ip/` command. We can also use proxychains4 with tools such as Nmap, WPScan, and even web browsers, though we might need to do some extra configuration to make it work.

Cookies

Quiz Yourself on Web and Server Technology

Ask

[Introduction to proxies](https://www.educative.io/courses/web-application-penetration-testing/proxies#Introduction-to-proxies)

[Type of proxies](https://www.educative.io/courses/web-application-penetration-testing/proxies#Type-of-proxies)

[Forward proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Forward-proxy)

[Open proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Open-proxy)

[Reverse proxy](https://www.educative.io/courses/web-application-penetration-testing/proxies#Reverse-proxy)

[Setting up a proxy server](https://www.educative.io/courses/web-application-penetration-testing/proxies#Setting-up-a-proxy-server)