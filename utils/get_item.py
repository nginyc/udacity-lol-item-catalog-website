from database import ItemCategory, Item, ItemToItemCategory

def get_item(session, item_id):
  '''
    Returns an item by ID, including categories it's in 
  '''
  item = session.query(Item).filter_by(id=item_id).first()

  cats = session.query(ItemCategory) \
    .join(ItemToItemCategory, ItemToItemCategory.item_category_id == ItemCategory.id) \
    .filter(ItemToItemCategory.item_id == item_id) \
    .all()

  return item, cats