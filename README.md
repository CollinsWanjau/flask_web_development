# Flask

## Variable Rules

* You can add variables sections to a URL by making sections with <variable_name>

* Your function then receives the <variable_name> as a keyword argument.

* Optionally, you can use a converter to specify the type of the arg, like
<converter:variable_name>

## Url Building

* To build a URL to a specific function, use the `url_for()` function.
It accepts the name of the function as its first argument and any number
of keyword arguments, each corresponding to a variable part of the URL
rule.

* Why would you want to build URLs using the URL reversing function
`url_for()` instead of hard-coding them into your templates

1. Reversing is often more descriptive than hard-coding the URLs.
2. You can change your URLs in one one go instead of needing to remember
to manually change hard-coded URLs.
3. URL building handles escaping of special characters and Unicode dta
transparently.
4. The generated paths are always absolute, avoiding unexpected behaviour
of relative paths in browsers.

## Static Files

* To generate URLs for static files, use the special `static` endpoint
name:
```
url_for('static', filename='style.css')
```

* This file has to be stored on the filesystem as `static/style.css`.

