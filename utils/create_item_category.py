from database import ItemCategory

def create_item_category(session, name):
  cat = session.query(ItemCategory).filter_by(name=name).first()

  if cat is not None:
    raise Exception('Item category "{}" already exists!'.format(name))

  cat = ItemCategory(name=name)
  session.add(cat)
  session.commit()

  return cat

def create_item_category_if_not_exists(session, **kwargs):
  try:
    create_item_category(session, **kwargs)
  except:
    pass
  