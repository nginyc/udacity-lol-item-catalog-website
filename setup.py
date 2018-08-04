from database import Database
import json
from config import SQLITE_DB_URL
from utils import create_item_category_if_not_exists

db = Database(SQLITE_DB_URL)
db.setup()

# Initialize item categories
db.connect()

with open('./data/item_categories.json') as json_data:
  item_categories = json.load(json_data)
  for cat in item_categories:
    create_item_category_if_not_exists(
      db.session,
      name=cat['name']
    )

db.disconnect()