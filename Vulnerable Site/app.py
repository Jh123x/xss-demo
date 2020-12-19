from flask import Flask, render_template, request, make_response
import db
import random
import string

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')

    comments = db.get_comments(search_query)

    return render_template('index.html',
                           comments=comments,
                           search_query=search_query)

@app.route('/img')
def load_img():
    return render_template('image.html')

@app.route('/cookie/')
def cookie():
    cookie_name = 'cookie'
    if not request.cookies.get(cookie_name):
        res = make_response("Setting a cookie")

        #Generate random cookie of length 32 with expiry of 2 years

        res.set_cookie(cookie_name, ''.join(random.choice(string.ascii_letters) for _ in range(32)), max_age=60*60*24*365*2)
    else:
        res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
    return res
