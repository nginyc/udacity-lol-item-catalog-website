from database import ItemCategory, Item, ItemToItemCategory


def get_item(session, item_id):
    '''
      Retrieves an item by ID, including categories it's in, from the database
      Returns (items, categories)
    '''
    item = session.query(Item).filter_by(id=item_id).first()

    cats = session.query(ItemCategory) \
        .join(
          ItemToItemCategory,
          ItemToItemCategory.item_category_id == ItemCategory.id
        ) \
        .filter(ItemToItemCategory.item_id == item_id) \
        .all()

    return item, cats
