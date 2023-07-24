# Flask

## Variable Rules
* The `{{ name }}` construct used in the template refs, a variable, a
special placeholder that tells the template engine that the value
that goes in that place should be obtained from data provided at the time
the template is rendered.

* Jinja2 recognizes variables of any type, even complex ones such as lists, tuples, dicts.

```
<p>A value from a dictionary: {{ mydict['key'] }}.<p>
<p>A value from a list: {{ mylist[3] }}.<p>
<p>A value from a list, with a variable index: {{ mylist[myintvar ]}}.</p>
<p>A value from an object's method: {{ myobj.somemthod() }}.<p>
```

* Variables can be modified with filters
`Hello, {{ name|capitalize }}`

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

# The Request-Response Cycle

## Application and Requests Contexts

* When Flask receives a request from a client, it needs to make a few objects available to the view function that will handle it.

* A good example is the request object, which encapsulates the HTTP request sent by the client.

* To avoid cluttering view functions with lots of args that may or may not be needed, Flask uses contexts to temporarily make certain objects globally accessible.

* Contexts enable Flask to make certain variables globally accessible to a thread without intefering with the other threads.

## Control Structures

```
{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

* Rendering a list of elements.This example shows how this can be done with
with a for loop.

```
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

* There is a way to reuse thru `template inheritance`.

## Open a Shell

* To explore data in your app, you can start an interactive Python shell with the
shell command.An app context will be active, and the app instance will be imported.

```
(venv) colloso@colloso-ThinkCentre-M73:~/Documents/flask_web_development/flask_web_development$ flask shell
/index
/login
/login?next=/
/user/John%20Doe
Python 3.10.7 (main, May 29 2023, 13:51:48) [GCC 12.2.0] on linux
App: hello
Instance: /home/colloso/Documents/flask_web_development/flask_web_development/instance
>>> from flask import Flask, url_for
>>> app.config['SERVER_NAME'] = 'localhost:5000'
>>> app.config['APPLICATION_ROOT'] = '/'
>>> app.config['PREFERRED_URL_SCHEME'] = 'http'
>>> with app.app_context():
...     print(url_for('index'))
...     print(url_for('login'))
...     print(url_for('login', next='/'))
...     print(url_for('profile', username='John Doe'))
... 
http://localhost:5000/index
http://localhost:5000/login
http://localhost:5000/login?next=/
http://localhost:5000/user/John%20Doe
>>>
```
