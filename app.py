from flask import Flask, render_template, request, jsonify, \
    make_response, session, \
    redirect, url_for, flash
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_requests
import requests
import random
import string

from config import GOOGLE_OAUTH_CLIENT_ID, \
    GOOGLE_OAUTH_CLIENT_SECRET, APP_SECRET, \
    DB_URL
from utils import upsert_user, get_item_categories, create_item, \
    get_items, get_item, delete_item, update_item, get_user
from database import Database, User, Item, ItemCategory, ItemToItemCategory

db = Database(DB_URL)

app = Flask(__name__)


@app.context_processor
def inject_config():
    '''
    Injects the Google OAuth Client ID & CSRF token into Flask templates
    '''
    return {
        'google_oauth_client_id': GOOGLE_OAUTH_CLIENT_ID,
        'csrf_token': session.get('csrf_token')
    }


@app.context_processor
def inject_user():
    '''
    Injects the current authenticated user's user data into Flask templates
    '''
    if 'user_id' not in session:
        return {
            'user': None
        }

    db.connect()
    user = get_user(db.session, user_id=session['user_id'])
    db.disconnect()

    return {
        'user': user
    }


@app.route('/', methods=['GET'])
def index():
    '''
    Index page
    Redirects to the main item catalog page
    '''
    return redirect(url_for('items_page'))


@app.route('/items', methods=['GET'])
def items_page():
    '''
    The main item catalog page
    '''
    category_id = request.args.get('category_id')
    db.connect()
    item_categories = get_item_categories(db.session)
    items, cat = get_items(db.session, category_id=category_id)
    db.disconnect()
    return render_template(
        'page-items.html',
        title=('Items - {}'.format(cat.name)
               if cat is not None else 'All Items'),
        item_categories=item_categories,
        items=items
    )


@app.route('/items/json', methods=['GET'])
def items_json():
    '''
    JSON endpoint for retrieving the full list of items in the catalog
    '''
    category_id = request.args.get('category_id')
    db.connect()
    items, cat = get_items(db.session, category_id=category_id)
    db.disconnect()

    return jsonify({
        'category': cat.serialize() if cat else None,
        'items': [x.serialize() for x in items]
    })


@app.route('/items/<int:item_id>', methods=['GET'])
def item_page(item_id):
    '''
    The item detail page
    '''
    db.connect()
    item, item_categories = get_item(db.session, item_id)
    db.disconnect()
    return render_template(
        'page-item.html',
        item_categories=item_categories,
        item=item
    )


@app.route('/item/<int:item_id>/json', methods=['GET'])
def item_json(item_id):
    '''
    JSON endpoint for retrieving an item's details
    '''
    db.connect()
    item, item_categories = get_item(db.session, item_id)
    db.disconnect()

    return jsonify({
        'item_categories': [x.serialize() for x in item_categories],
        'item': item.serialize()
    })


@app.route('/items/create', methods=['GET'])
def create_item_page():
    '''
    The add item page
    '''
    db.connect()
    item_categories = get_item_categories(db.session)
    db.disconnect()
    return render_template(
        'page-item-create.html',
        item_categories=item_categories
    )


@app.route('/items/<int:item_id>/delete', methods=['GET'])
def delete_item_page(item_id):
    '''
    The delete item page
    '''
    db.connect()
    item, _ = get_item(db.session, item_id)
    db.disconnect()
    return render_template('page-item-delete.html', item=item)


@app.route('/items/<int:item_id>/update', methods=['GET'])
def update_item_page(item_id):
    '''
    The update item page
    '''
    db.connect()
    item, categories = get_item(db.session, item_id)
    item_category_ids = [x.id for x in categories]
    item_categories = get_item_categories(db.session)
    db.disconnect()
    return render_template('page-item-update.html',
                           item=item,
                           item_category_ids=item_category_ids,
                           item_categories=item_categories)


@app.route('/items/<int:item_id>/update', methods=['POST'])
def update_item_request(item_id):
    '''
    The endpoint to handle a request to update an item
    '''
    res = assert_user_is_authenticated()
    if res:
        return res

    db.connect()
    item = update_item(
        db.session,
        item_id=item_id,
        name=request.form.get('name'),
        description=request.form.get('description'),
        image_url=request.form.get('image_url'),
        category_ids=(request.form.getlist('category_ids')
                      if 'category_ids' in request.form else None)
    )
    db.disconnect()

    flash('Item "{}" edited!'.format(item.name))

    # Redirect to item page
    return redirect(url_for('item_page', item_id=item.id))


@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item_request(item_id):
    '''
    The endpoint to handle a request to delete an item
    '''
    res = assert_user_is_authenticated()
    if res:
        return res

    db.connect()
    item = delete_item(db.session, item_id)
    db.disconnect()

    flash('Item "{}" deleted!'.format(item.name))

    # Redirect to items page
    return redirect(url_for('items_page'))


@app.route('/items/create', methods=['POST'])
def create_item_request():
    '''
    The endpoint to handle a request to create an item
    '''
    if 'name' not in request.form or \
        'description' not in request.form or \
            'category_ids' not in request.form:
        return make_response('An item requires a name, description & \
      belong to at least 1 category.', 400)

    res = assert_user_is_authenticated()
    if res:
        return res

    db.connect()
    item = create_item(
        db.session,
        owner_id=session['user_id'],
        name=request.form['name'],
        description=request.form['description'],
        image_url=request.form.get('image_url'),
        category_ids=request.form.getlist('category_ids')
    )
    db.disconnect()

    flash('Item "{}" added!'.format(item.name))

    # Redirect to item page
    return redirect(url_for('item_page', item_id=item.id))


@app.route('/login-with-google', methods=['POST'])
def login_with_google_request():
    '''
    The endpoint to handle a request to login with Google using OAuth
    '''
    data = request.get_json()
    token = data.get('token')

    if token is None:
        return make_response('Missing token in request.', 400)

    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_auth_requests.Request(),
            GOOGLE_OAUTH_CLIENT_ID
        )

        if idinfo['iss'] not in \
                ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # ID token is valid
        # Get the user's Google Account ID from the decoded token
        user_id = idinfo['sub']

        # Save token in session
        session['token'] = token

    except ValueError:
        # Invalid token
        return make_response('Invalid token in request.', 400)

    try:
        # Create user in database if not exists
        res = requests.get(
            'https://www.googleapis.com/oauth2/v3/tokeninfo',
            params={
                'id_token': token
            })

        res_data = res.json()
        user_email = res_data['email']
        user_name = res_data.get('given_name', 'User')
        user_profile_image_url = res_data.get('picture', None)

        db.connect()
        user = upsert_user(db.session, user_email,
                           user_profile_image_url, user_name)

        # Put the authenticated user's ID into the session
        # Also generate a CSRF token for the user's session
        session['user_id'] = user.id
        session['csrf_token'] = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in range(32))
        db.disconnect()

        flash('Successfully logged in with Google!')

        return make_response('Successfully logged in with Google!')

    except ValueError:
        # Error logging in as user
        return make_response('Error logging in as user.', 500)


@app.route('/logout', methods=['GET'])
def logout():
    '''
    The endpoint to handle a request to logout
    '''
    if 'token' not in session:
        return make_response('User is unauthenticated.', 401)

    # Clear the user's session data
    session.clear()

    flash('Successfully logged out.')

    return redirect(url_for('items_page'))


def assert_user_is_authenticated():
    '''
    Checks if the user is authenticated based on the session

    Returns:
    A Flask response describing the error if authentication failed;
    None otherwise
    '''
    csrf_token = request.args.get('csrf_token')

    if 'user_id' not in session:
        return make_response('Authentication is required.', 401)

    if csrf_token != session.get('csrf_token'):
        return make_response('Invalid CSRF token', 401)

    return None


if __name__ == '__main__':
    app.secret_key = APP_SECRET
    app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)
