# Understanding_Web_Encoding_in_Web_Application_Security

Source: https://www.educative.io/courses/web-application-penetration-testing/web-encoding

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Web Application Penetration Testing](https://www.educative.io/courses/web-application-penetration-testing)

# Web Encoding

Explore how web encoding transforms special, accented, and non-Latin characters into safe, transmittable formats over the internet. Understand its significance in web application security and penetration testing, including practical use cases for encoding to detect vulnerabilities. Gain foundational knowledge of encoding processes essential for web and server technology security.

We'll cover the following...

- [What is web encoding?](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#What-is-web-encoding)
- [A simple encoder and decoder](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#A-simple-encoder-and-decoder)

## What is web encoding?[#](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#What-is-web-encoding)

**Encoding** is the process of converting information from one format into another, mostly for processing needs.

URLs are largely sent over the internet using the ASCII or UTF-8 character sets. Oftentimes, special characters, such as = and #; letters with accents, such as ä; and even non-Latin scripts, such as the Japanese kanji for “character,” 字, have to be used in URLs. These have to be encoded in order to be transmitted. This involves basically replacing these characters with one or more % followed by two hexadecimal characters.

Here are the encoded equivalents of the previous examples:

- The “=” character is encoded to “%3D”
- The “#” character is encoded to “%23”
- The “ä” character is encoded to “%C3%A4”
- The “字” character is encoded to “%E5%AD%97”

> **Note:** Modern browsers now automatically make URLs human friendly and readable, i.e., we don’t get to see the encoding take place.

There are thousands of characters that can be encoded, so of course, we can’t display all of them here. You can still check out the table below to see a list of common special characters that have to be encoded.

## Encoding of Common Special Characters

|  |  |  |
| --- | --- | --- |
| **ASCII Encoding** | **Character** | **HTML Entity Number** |
| 20 | (space) | &#32; |
| 21 | ! | &#33; |
| 22 | " | &#34; |
| 23 | # | &#35; |
| 24 | $ | &#36; |
| 25 | % | &#37; |
| 26 | & | &#38; |
| 27 | ' | &#39; |
| 28 | ( | &#40; |
| 29 | ) | &#41; |
| 2A | \* | &#42; |
| 2B | + | &#43; |
| 2C | , | &#44; |
| 2D | - | &#45; |
| 2E | . | &#46; |
| 2F | / | &#47; |
| 3A | : | &#58; |
| 3B | ; | &#59; |
| 3C | < | &#60; |
| 3D | = | &#61; |
| 3F | > | &#62; |

We can also use HTML entity numbers when writing safe code for web applications or testing for vulnerabilities. For example, a website has a search bar. We can submit a query and the URL is updated with our search parameters. The developers of the website have blacklisted the use of special characters in search queries by cleaning the submitted search parameters of relevant ASCII encoding. We could then try probing by using the equivalent HTML entity numbers instead. We’ll see a practical example of this later in the course.

## A simple encoder and decoder[#](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#A-simple-encoder-and-decoder)

There’s a basic web encoder and decoder running on our Apache web server below. Click “Run” to navigate to the localhost on the browser. Type in the URL of any website (for example, “https:educative.io”) and see how it gets encoded. Compare your results to the table above.

```
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
		<title>URL Decoder/Encoder</title>
		<style type="text/css">
			body {background: white; color: black;}
			form {margin: 0;}
			h1 {font-family: Arial, sans-serif; line-height: 0.85em; border-bottom: 2px solid; margin-bottom: 0.33em; padding-bottom: 0;}
			textarea {background: #EEF;}
			#footer {border-top: 1px solid #000; color: #999; font: italic 75% sans-serif;}
			#footer p {margin: 0 0 1em 0;}
			#footer img {float: right; margin: 0 0 0.5em 2em;}
		</style>
		<script type="text/javascript">
			function encode() {
				var obj = document.getElementById('dencoder');
				var unencoded = obj.value;
				obj.value = encodeURIComponent(unencoded).replace(/'/g,"%27").replace(/"/g,"%22");
			}
			function decode() {
				var obj = document.getElementById('dencoder');
				var encoded = obj.value;
				obj.value = decodeURIComponent(encoded.replace(/\+/g,  " "));
			}
		</script>
	</head>
	<body>
		<form onsubmit="return false;">
			<h1>URL Decoder/Encoder</h1>
			<textarea cols="100" rows="20" id="dencoder"></textarea>
			<div>
				<input type="button" onclick="decode()" value="Decode">
				<input type="button" onclick="encode()" value="Encode">
			</div>
			<ul>
				<li>Input a string of text and encode or decode it as we like.</li>
			</ul>
		</form>
	</body>
</html>
```

Running our own encoder and decoder

Running a Web Server with Apache

Cookies

Ask

[What is web encoding?](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#What-is-web-encoding)

[A simple encoder and decoder](https://www.educative.io/courses/web-application-penetration-testing/web-encoding#A-simple-encoder-and-decoder)