#importing dependencies
#using flask to render a template, redirecting to amother url, and creating a URL
from flask import Flask, render_template, redirect, url_for
#using PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#usign the scraping code from Jupyter notebook to python
import scraping

#set up flask
app = Flask(__name__)

#tell python how to connect to Mongo using PyMongo
#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#defining home route
@app.route("/")

def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run()