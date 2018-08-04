from database import Item, ItemCategory, ItemToItemCategory

def create_item(session, name, owner_id, description, category_ids):
  item = session.query(Item).filter_by(name=name).first()

  if item is not None:
    raise Exception('Item "{}" already exists!'.format(name))

  cats = session.query(ItemCategory).filter(ItemCategory.id.in_(category_ids)).all()
  if len(cats) != len(category_ids):
    raise Exception('Invalid category IDs!')

  item = Item(name=name, description=description)
  session.add(item)
  session.commit()

  for cat in cats:
    item_to_cat = ItemToItemCategory(item_id=item.id, item_category_id=cat.id)
    session.add(item_to_cat)

  session.commit()
  
  return item
  