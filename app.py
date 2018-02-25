import scrape_mars
from splinter import Browser
from flask import Flask, render_template, redirect
from flask import jsonify
import pymongo
from flask_pymongo import PyMongo


app = Flask(__name__)


mongo = PyMongo(app)

@app.route("/")
def index():
    news = mongo.db.mars.find_one()
    print(news)
    return render_template("mars.html", news=news)





@app.route("/scrape")
def scrape():
    news = mongo.db.mars
    data = scrape_mars.scrape()
    news.update(
        {},
        data,
        upsert=True
    )


    

    return redirect("http://localhost:5000/", code=302)


    #db.mars.find()

if __name__ == '__main__':
    app.run(debug=True)
