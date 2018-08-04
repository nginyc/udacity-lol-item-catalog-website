from flask import Flask, render_template, request, jsonify, make_response, session, \
  redirect, url_for
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_requests
import requests
from config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, APP_SECRET, \
  SQLITE_DB_URL
  
from utils import upsert_user, get_item_categories, create_item, get_items, get_item
from database import Database

db = Database(SQLITE_DB_URL)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return redirect(url_for('items_page'))

@app.route('/items', methods=['GET'])
def items_page():
  category_id = request.args.get('category_id')
  db.connect()
  item_categories = get_item_categories(db.session)
  items, cat = get_items(db.session, category_id=category_id)
  db.disconnect()
  return render_template(
    'items.html', 
    title=(cat.name if cat is not None else 'All Items'),
    item_categories=item_categories,
    items=items
  )

@app.route('/items/<int:item_id>', methods=['GET'])
def item_page(item_id):
  db.connect()
  item, item_categories = get_item(db.session, item_id)
  db.disconnect()
  return render_template(
    'item.html', 
    item_categories=item_categories,
    item=item
  )

@app.route('/items/create', methods=['GET'])
def create_item_page():
  db.connect()
  item_categories = get_item_categories(db.session)
  db.disconnect()
  return render_template('item-create.html', item_categories=item_categories)

@app.route('/items', methods=['POST'])
def create_item_request():
  if 'name' not in request.form or \
    'description' not in request.form or \
    'category_ids' not in request.form:
    return make_response('An item requires a name, description & \
      belong to at least 1 category.', 400) 

  if 'user_id' not in session:
    return make_response('Authentication is required.', 401)

  db.connect()
  item = create_item(
    db.session, 
    owner_id=session['user_id'],
    name=request.form['name'],
    description=request.form['description'],
    category_ids=request.form.getlist('category_ids')
  )
  db.disconnect()
    
  return jsonify({
    'item_id': item.id,
    'item_name': item.name,
  })

@app.route('/login-with-google', methods=['POST'])
def login_with_google_request():
  # TODO: Implement CSRF
  data = request.get_json()
  token = data.get('token')

  if token is None:
    return make_response('Missing token in request.', 400)

  try:
      idinfo = id_token.verify_oauth2_token(token, google_auth_requests.Request(), GOOGLE_OAUTH_CLIENT_ID)

      if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
          raise ValueError('Wrong issuer.')

      # ID token is valid. Get the user's Google Account ID from the decoded token.
      user_id = idinfo['sub']
      
      # Save credentials in session
      session['token'] = token
      session['user_id'] = user_id
      
  except ValueError:
      # Invalid token
      return make_response('Invalid token in request.', 400)

  try:
    # Create user if not exists
    res = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo', params={
      'id_token': token
    })

    res_data = res.json()
    user_email = res_data['email']
    user_name = res_data.get('given_name', 'User')
    user_profile_image_url = res_data.get('picture', None)

    
    db.connect()
    user = upsert_user(db.session, user_email, user_profile_image_url, user_name)
    db.disconnect() 
        
    return jsonify({
      'user_id': user.id,
      'user_email': user.email,
      'user_name': user.name,
      'user_profile_image_url': user.profile_image_url,
    })
      
  except ValueError:
      # Error logging in as user
      return make_response('Error logging in as user.', 500)


if __name__ == '__main__':
  app.secret_key = APP_SECRET
  app.debug = True
  app.run(host='0.0.0.0', port=5000, debug=True)