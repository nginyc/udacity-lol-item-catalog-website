from database import ItemCategory


def get_item_categories(session):
    '''
    Retrieves the full list of item catagories from the database
    '''
    item_categories = session.query(ItemCategory)
    return item_categories
