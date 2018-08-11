from database import ItemCategory


def create_item_category(session, name):
    '''
    Creates an item category in the database
    Also raises an Exception if there is an existing
      item category of the same name
    '''
    cat = session.query(ItemCategory).filter_by(name=name).first()

    if cat is not None:
        raise Exception('Item category "{}" already exists!'.format(name))

    cat = ItemCategory(name=name)
    session.add(cat)
    session.commit()

    return cat


def create_item_category_if_not_exists(session, **kwargs):
    '''
    Creates an item category in the database
    Does nothing if an item category of the same name already exists
    '''
    try:
        create_item_category(session, **kwargs)
    except:
        pass
