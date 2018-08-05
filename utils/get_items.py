from database import ItemCategory, Item, ItemToItemCategory

def get_items(session, category_id=None):
  if category_id is None:
    items = session.query(Item).all()

    return items, None
  else:
    cat = session.query(ItemCategory).filter_by(id = category_id).first()

    if cat is None:
      raise Exception('Invalid category ID')

    items = session.query(Item) \
      .join(ItemToItemCategory, ItemToItemCategory.item_id == Item.id) \
      .filter(ItemToItemCategory.item_category_id == category_id) \
      .all()

    return items, cat
