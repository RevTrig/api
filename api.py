import flask
from flask import request, jsonify,render_template
import controller
from database import create_tables
import json
from werkzeug.utils import secure_filename
from uuid import uuid4
 

app = flask.Flask(__name__, template_folder='template')
app.config["DEBUG"] = True

 
@app.route('/', methods=['GET'])
def home():
    productlist = controller.load_products()
    
    return render_template('index.html', productlist=productlist)
 
@app.route('/upload_articles', methods = ['POST'])
def upload():
    f = request.files['File']
    f.save(secure_filename(f.filename))
    f = open(f.filename,)  
    # returns JSON object as a dictionary
    data = json.load(f) 
    # Iterating through the json list
    for article_details in data['inventory']:
        art_id= article_details["art_id"]
        name = article_details["name"]
        stock = article_details["stock"]
        result = controller.insert_article(art_id,name,stock)   
    # Closing file
    f.close()
    return render_template('articles.html')

@app.route('/upload_products', methods = ['POST'])
def upload_products():
    f = request.files['File']
    f.save(secure_filename(f.filename))
    f = open(f.filename,)
    # returns JSON object as  a dictionary
    data = json.load(f)  
    # Iterating through the json list
    for product_details in data['products']:
        #art_id= product_details["art_id"]
        name = product_details["name"]
        price = 50
        contain_articles_id = str(uuid4())
        if(controller.insert_products(name,price,contain_articles_id)):
            contained_articles = product_details['contain_articles']
            for contained_article in contained_articles:
                article_art_id = contained_article['art_id']
                amount_of = contained_article['amount_of']
                contained_articles = controller.insert_contain_articles(contain_articles_id,article_art_id,amount_of)
        else:
            return render_template('error_products.html')
    # Closing file
    f.close()
    return render_template('products.html')

@app.route("/products/<name>", methods=["DELETE"])
def delete_products(name):
    article_id = controller.get_contained_article_id(name)
    entries_to_update = controller.get_articles_to_update(article_id)
    for entries in entries_to_update:
        controller.update_articles(entries['article_art_id'], entries['amount_of'])
        controller.update_contain_articles(article_id[0])
    result = controller.delete_products(name)
    return jsonify(result)

@app.route('/products', methods = ['GET'])
def get_products():
    results = controller.get_all_products()
    return jsonify(results)


if __name__ =="__main__":
    create_tables()
    app.run()