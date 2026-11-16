# Google_Hacking_Techniques_for_Penetration_Testing

Source: https://www.educative.io/courses/web-application-penetration-testing/google-hacking

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Google Hacking

Explore Google hacking methods in penetration testing using advanced search filters to gather detailed information about target websites, detect vulnerable files, and identify security risks. Understand how to apply commands like site, inurl, intext, intitle, and filetype to refine your searches and uncover exploitable data for security assessments.

We'll cover the following...

- [Introduction to Google hacking](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Introduction-to-Google-hacking)
- [Google hacking for pentesting](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Google-hacking-for-pentesting)
  - [The site filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-site-filter)
  - [The intext filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intext-filter)
  - [The inurl command](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-inurl-command)
  - [The intitle filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intitle-filter)
  - [The filetype filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-filetype-filter)

## Introduction to Google hacking[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Introduction-to-Google-hacking)

**Google hacking**, also referred to as **Google dorking**, is the process through which a user can gather information about a target with the help of the advanced search and indexing capabilities of Google’s search engine. It allows hackers to target keywords, URLs, file types, and software versions on the target website.

Google hacking helps pentesters narrow the investigation down to a particular domain that has been identified as a target and further specify what technologies and their relevant information to search for. For example, a website for a hotel may also have an insecure security camera system (mostly just webcams) on its network. We could find such publicly viewable cameras with the query `inurl:"ViewerFrame?Mode="`. We could also use quotation marks to query for exact text, like so: `"Only phrases just like this"`.

## Google hacking for pentesting[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Google-hacking-for-pentesting)

In the table below we’ll look at some of the commands that are used in Google hacks for penetration testing:

## Search Filters

|  |  |
| --- | --- |
| **Command** | **Description** |
| `intext` | This is used as a lookup for a keyword in the text content of a website. |
| `allintext` | This is used as a lookup for multiple keywords. |
| `inurl` | This is used to search for the keyword matching in the URL of a website. |
| `allinurl` | This is used to search for all the keywords matching in the URL. |
| `intitle` | This is used to search the keyword matching in the HTML page title. |
| `allintitle` | This is used to search all the keywords matching in the HTML page title. |
| `site` | This is used to list all the results (web pages) for a particular site. |
| `filetype` | This is used to search for a particular file type. |
| `link` | This is used as a lookup for external links. |
| `numrange` | This is used as a lookup for a (range of) numbers. |
| `daterange` | This is used as a lookup for a time frame. |

Let's try some of these filters below. Open up Chrome by clicking the “Run” button, and head on over to Google. We'll try one filter first, then move on to the next, and so on.

Chrome browser

### The `site` filter[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-site-filter)

The `site` command is used to search for a particular domain and list all the results for it. This comes in handy when looking for admin pages or non-obfuscated `.env` files.

In the search bar, we enter `site:"testphp.vulnweb.com" admin login`. We are passing `admin login` as an argument to the filter to find the admin login page for the particular website. We’ll see that while we don’t find the page for the admin login, we do find an interesting page (<http://testphp.vulnweb.com/admin/>) that reveals that a `create.sql` file could’ve been used to create the database for the website.

### The `intext` filter[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intext-filter)

This filter returns web pages that contain specified occurrences of the keywords that have been supplied as arguments.

[Heroku](https://www.heroku.com/) used to be quite popular with aspiring developers back when it used to have a free tier. Unfortunately, some of these developers never got around to implementing privacy and security measures for their web applications. If we were to register with Heroku and host our web app with them, we’d receive a URL such as [mywebsite.herokuapp.com](http://mywebsite.herokuapp.com). We can use this knowledge to do interesting things. For example, we can look for new web applications that haven’t hidden their admin panels from Google’s crawlers with the following command: `site:"*.herokuapp.com" intext:"admin"`.

### The `inurl` command[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-inurl-command)

This command helps search URLs that match the keyword that has been passed to it. For example, let’s assume that a developer has put up their web application source code on GitHub to help others out. They may have forgotten to remove their API keys and other credentials from the `.env` file and similar configuration files of their project. We could perform a broad sweep with `site:"github.com" inurl:.env` and find projects like these.

### The `intitle` filter[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intitle-filter)

This filter helps search for the URL from the keyword that has been supplied as an argument. It’s quite useful, especially when searching for URLs that have their index files without extensions like PHP, ASP, ASPX, or even HTML in the actual directory where the file structure is located. It enables pentesters to pull out the directory structure of a website that has very sensitive information. This can even enable a hacker to take control of the website. We already saw an example of such a scenario earlier when we found that `create.sql` file.

People often host unsecured media servers at home and are mostly unaware that outsiders can snoop around their files and folders. These unsecured servers are known as **open directories**. We can try finding some using `intitle:"index of/"`. Beware that this may be illegal depending on where you live.

We can also run `intitle:"index of/" passwd.txt` to find the password files or `intitle:"index of/" passwd.bak` to find backup password files for different open directories.

### The `filetype` filter[#](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-filetype-filter)

This filter comes in handy when searching for certain filetypes. Let’s assume that we’re looking for a manual for the electrical wiring system of a 1985 Toyota Celica Supra. This can become an easy find with `allintext:1985 toyota celica supra electrical wiring filetype:pdf`.

In the case of web pentesting, the `filetype` filter is useful when we’re searching for certain files on servers that either really shouldn’t be there or shouldn’t contain certain content. For example, if we were to revisit `.env` files, we could find projects with poorly or default set database passwords using `filetype:env intext:db_password`.

Web Fingerprinting Infrastructure

Shodan

Ask

[Introduction to Google hacking](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Introduction-to-Google-hacking)

[Google hacking for pentesting](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#Google-hacking-for-pentesting)

[The site filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-site-filter)

[The intext filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intext-filter)

[The inurl command](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-inurl-command)

[The intitle filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-intitle-filter)

[The filetype filter](https://www.educative.io/courses/web-application-penetration-testing/google-hacking#The-filetype-filter)