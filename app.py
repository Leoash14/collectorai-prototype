from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import json
import os
from PIL import Image
import imagehash
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load collectibles
with open('data/collectibles.json') as f:
    collectibles = json.load(f)

# Precompute image hashes
hashes = {}
for item in collectibles:
    try:
        img_path = os.path.join('reference_images', item['image'])
        img = Image.open(img_path)
        img_hash = imagehash.average_hash(img)
        hashes[item['id']] = img_hash
    except Exception as e:
        print(f"Error loading image: {e}")

# Ensure necessary files exist
os.makedirs('data', exist_ok=True)
if not os.path.exists('data/collection.json'):
    with open('data/collection.json', 'w') as f:
        json.dump([], f)

if not os.path.exists('data/price_history.json'):
    with open('data/price_history.json', 'w') as f:
        json.dump({}, f)

@app.route('/api/identify', methods=['POST'])
def identify_item():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400
    try:
        img = Image.open(file.stream)
        img_hash = imagehash.average_hash(img)
        best_match = None
        best_score = 10
        for item_id, ref_hash in hashes.items():
            score = img_hash - ref_hash
            if score < best_score:
                best_score = score
                best_match = item_id
        if best_match:
            item = next((i for i in collectibles if i['id'] == best_match), None)
            return jsonify({'match': item})
        return jsonify({'match': None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/collection', methods=['GET'])
def get_collection():
    with open('data/collection.json') as f:
        return jsonify(json.load(f))

@app.route('/api/collection', methods=['POST'])
def save_to_collection():
    new_item = request.json
    with open('data/collection.json') as f:
        collection = json.load(f)
    collection.append(new_item)
    with open('data/collection.json', 'w') as f:
        json.dump(collection, f)
    track_price(new_item)
    return jsonify({'status': 'added'})

@app.route('/api/price_history/<item_id>', methods=['GET'])
def get_price_history(item_id):
    with open('data/price_history.json') as f:
        prices = json.load(f)
    return jsonify(prices.get(item_id, []))
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api/collection', methods=['DELETE'])
def delete_from_collection():
    index = request.json.get('index')
    with open('data/collection.json') as f:
        collection = json.load(f)
    if index is not None and 0 <= index < len(collection):
        removed = collection.pop(index)
        with open('data/collection.json', 'w') as f:
            json.dump(collection, f)
        return jsonify({'status': 'deleted', 'item': removed})
    return jsonify({'error': 'Invalid index'}), 400


def track_price(item):
    try:
        with open('data/price_history.json') as f:
            prices = json.load(f)
        item_id = item['id']
        price_record = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'value': item['estimated_value']
        }
        if item_id not in prices:
            prices[item_id] = []
        prices[item_id].append(price_record)
        with open('data/price_history.json', 'w') as f:
            json.dump(prices, f)
    except Exception as e:
        print(f"Error tracking price: {e}")

if __name__ == '__main__':
    app.run(debug=True)