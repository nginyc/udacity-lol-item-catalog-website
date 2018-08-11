from database import Item, ItemCategory, ItemToItemCategory


def create_item(session, name, description, category_ids,
                owner_id=None, image_url=None):
    '''
    Creates an item in the database
    Also raises an Exception if there is an existing
      item of the same name
    '''
    item = session.query(Item).filter_by(name=name).first()

    if item is not None:
        raise Exception('Item "{}" already exists!'.format(name))

    cats = session.query(ItemCategory).filter(
        ItemCategory.id.in_(category_ids)).all()
    if len(cats) != len(category_ids):
        raise Exception('Invalid category IDs!')

    item = Item(name=name, description=description, image_url=image_url)
    session.add(item)
    session.commit()

    for cat in cats:
        item_to_cat = ItemToItemCategory(
            item_id=item.id, item_category_id=cat.id)
        session.add(item_to_cat)

    session.commit()

    return item


def create_item_if_not_exists(session, **kwargs):
    '''
    Creates an item category in the database
    Does nothing if an item of the same name already exists
    '''
    try:
        create_item(session, **kwargs)
    except:
        pass
