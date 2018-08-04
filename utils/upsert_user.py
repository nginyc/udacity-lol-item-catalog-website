from database import User

def upsert_user(session, email, profile_image_url, name):
  user = session.query(User).filter_by(email=email).first()
  
  if user is None:
    user = User(email=email, name=name, profile_image_url=profile_image_url)
  else:
    user.name = name
    user.profile_image_url = profile_image_url

  session.add(user)
  session.commit()
  return user
