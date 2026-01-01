### put and delete HTTP verbs
### working with API json

from flask import Flask, jsonify, request
app=Flask(__name__)

items= [
    {"id": 1, "name": "item 1", "description": "This is item 1"},
    {"id": 2, "name": "item 2", "description": "This is item 2"},
]

@app.route('/')
def home():
    return "Welcome to the to do list app"

## get: retirve all the items

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

## get: retrieve a specicfin=c item

@app.route('/item/<int:itrm_id>', methods=['GET'])
def get_item(item_id):
   