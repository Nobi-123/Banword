AUTHORIZED_USERS = []  # starts empty, gets filled at runtime

def is_authorized(user_id: int) -> bool:
    """Check if user is in the authorized list."""
    return user_id in AUTHORIZED_USERS

def add_authorized_user(user_id: int) -> bool:
    """Add a user to authorized list. Returns True if added, False if already exists."""
    if user_id not in AUTHORIZED_USERS:
        AUTHORIZED_USERS.append(user_id)
        return True
    return False
