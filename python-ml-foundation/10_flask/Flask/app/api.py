### put and delete HTTP verbs
### working with API json

from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {"id": 1, "name": "item 1", "description": "This is item 1"},
    {"id": 2, "name": "item 2", "description": "This is item 2"},
]


@app.route('/')
def home():
    return "Welcome to the to do list app"


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)


@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)


@app.route('/item', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': "Missing 'name' in request"}), 400
    new_id = max((i['id'] for i in items), default=0) + 1
    item = {"id": new_id, "name": data.get('name'), "description": data.get('description', '')}
    items.append(item)
    return jsonify(item), 201


@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
    item['name'] = data.get('name', item['name'])
    item['description'] = data.get('description', item['description'])
    return jsonify(item)


@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((i for i in items if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    items = [i for i in items if i['id'] != item_id]
    return jsonify({'message': f'Item {item_id} deleted'})


if __name__ == '__main__':
    app.run(debug=True)
   