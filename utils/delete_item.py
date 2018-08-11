from database import Item, ItemCategory, ItemToItemCategory


def delete_item(session, item_id):
    '''
    Deletes an item from the database
    '''
    item = session.query(Item).filter_by(id=item_id).first()

    if item is None:
        raise Exception('Invalid item ID!')

    session.delete(item)
    session.commit()

    return item
