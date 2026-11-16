# Mitigation_Techniques_for_Cross-Site_Scripting_Attacks_in_Web_Apps

Source: https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Mitigation of XSS

Understand how to protect web applications from Cross-Site Scripting (XSS) attacks by exploring secure coding practices, input filtering, and using Content Security Policies. This lesson helps you develop skills to mitigate vulnerabilities that arise from user input and coding weaknesses by applying practical defenses with modern frameworks and security tools.

We'll cover the following...

- [Overview](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Overview)
- [Mitigation methods](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Mitigation-methods)
  - [Modern frameworks](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Modern-frameworks)
  - [Avoid untrusted input](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Avoid-untrusted-input)
  - [Filter user input](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Filter-user-input)
  - [Use a Content Security Policy (CSP)](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Use-a-Content-Security-Policy-CSP)

## Overview[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Overview)

XSS attacks can be truly annoying, especially since most are due to shoddy coding practices. With the examples discussed in the previous lesson, we can easily infer how much damage someone with malicious intent can cause. Fortunately, most XSS-related vulnerabilities can be addressed by just writing good code and simple manual checks. Tools like [OWASP ZAP](https://www.zaproxy.org/) can also work quite nicely (since it has a good success rate with Juice Shop).

## Mitigation methods[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Mitigation-methods)

Let’s look at a few golden rules that need to be kept in mind when coding web applications.

### Modern frameworks[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Modern-frameworks)

If we’re using modern frameworks, such as React, Angular, or Vue, to build our web applications, then we’re mostly safe from XSS attacks. These frameworks ensure secure coding practices due to the way they work. Keep in mind though, we can intentionally make our web application insecure with special configurations, so be wary of that. Also, there are still some avenues where frameworks can’t provide security, so proper knowledge is required to handle such cases.

### Avoid untrusted input[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Avoid-untrusted-input)

Users should only be allowed to input data where they’re supposed to. They should also only be able to make changes to pages they’re authorized and authenticated to do so. The reflected and DOM XSS examples show that anyone could be affected by such attacks. Using unique identifiers could prevent such wide-net attacks.

The Mozilla Firefox browser and applications such as Burp Suite allow users to repeat requests with custom parameters. This might prove dangerous if we don’t check for this custom input since since it deviates from the intended behavior of the web application.

### Filter user input[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Filter-user-input)

User input should always go through validation. Rigorous testing is required to ensure that users cannot input content they’re not supposed to. For example, the username field of a login form really shouldn’t be able to accept HTML tags as input.

Additionally, we should encode output to prevent user-provided data from being automatically executed by a browser.

### Use a Content Security Policy (CSP)[#](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Use-a-Content-Security-Policy-CSP)

A **Content Security Policy (CSP)** determines what websites the browser can consider trustworthy sources of executable scripts when the scripts are being queried by a website. For example, let’s assume we want to visit [niceshoes.com](http://niceshoes.com). This website gets content and some business logic from third-party sites, such as [store.niceshoes.com](http://store.niceshoes.com) and [google-ads.net](http://google-ads.net). An adversary realizes that there is a form on the website that doesn’t sanitize input, and they enter malicious code that tries to steal users’ cookies and send them to their own evil web server. However, since the CSP dictates that scripts with origins other than [store.niceshoes.com](http://store.niceshoes.com) and [google-ads.net](http://google-ads.net) should be ignored, the attack will fail.

XSS Exploitation

Quiz Yourself on Cross-Site Scripting

Ask

[Overview](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Overview)

[Mitigation methods](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Mitigation-methods)

[Modern frameworks](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Modern-frameworks)

[Avoid untrusted input](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Avoid-untrusted-input)

[Filter user input](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Filter-user-input)

[Use a Content Security Policy (CSP)](https://www.educative.io/courses/web-application-penetration-testing/mitigation-of-xss#Use-a-Content-Security-Policy-CSP)