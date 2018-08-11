from database import Item, ItemCategory, ItemToItemCategory


def update_item(session, item_id, name=None,
                description=None, category_ids=None, image_url=None):
    '''
      Updates an existing item by ID in the database
    '''
    item = session.query(Item).filter_by(id=item_id).first()

    if item is None:
        raise Exception('Invalid item ID!')

    if name is not None:
        item.name = name

    if description is not None:
        item.description = description

    if image_url is not None:
        item.image_url = image_url

    session.add(item)
    session.commit()

    # If category IDs have changed, delete from the ItemToItemCategory
    #   association table the old category IDs and add to the association
    #   table the new category IDs
    if category_ids is not None:
        cats = session.query(ItemCategory).filter(
            ItemCategory.id.in_(category_ids)).all()
        if len(cats) != len(category_ids):
            raise Exception('Invalid category IDs!')

        old_item_to_cats = session.query(ItemToItemCategory) \
            .filter_by(item_id=item_id) \
            .all()

        for item_to_cat in old_item_to_cats:
            session.delete(item_to_cat)

        session.commit()

        for cat_id in category_ids:
            item_to_cat = ItemToItemCategory(
                item_id=item_id, item_category_id=cat_id)
            session.add(item_to_cat)

        session.commit()

    return item
