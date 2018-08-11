from database import User


def get_user(session, user_id):
    '''
      Retrieves a user by ID from the database
    '''
    user = session.query(User).filter_by(id=user_id).first()

    if user is None:
        raise Exception('User does not exist!')

    return user
