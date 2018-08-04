from database import ItemCategory

def get_item_categories(session):
  item_categories = session.query(ItemCategory)
  return item_categories
