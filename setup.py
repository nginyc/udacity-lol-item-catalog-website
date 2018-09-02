from database import Database
import json
from config import DB_URL
from utils import create_item_category_if_not_exists, \
    create_item_if_not_exists, get_item_categories

db = Database(DB_URL)
db.setup()

db.connect()

# Initialize item categories
with open('./data/item_categories.json') as json_data:
    item_categories = json.load(json_data)
    for cat in item_categories:
        create_item_category_if_not_exists(
            db.session,
            name=cat['name']
        )

# Seed full list of items
with open('./data/items.json') as json_data:
    items = json.load(json_data)
    for item in items:
        cats = get_item_categories(db.session)
        category_ids = [x.id for x in cats if x.name in item['categories']]

        create_item_if_not_exists(
            db.session,
            name=item['name'],
            description=item['description'],
            category_ids=category_ids,
            image_url=item['image_url']
        )

db.disconnect()
