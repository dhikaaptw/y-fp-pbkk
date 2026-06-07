import requests

API_URL = "http://localhost:8000"


def H(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── AUTH
def api_register(username, email, password):
    return requests.post(f"{API_URL}/auth/register",
                         json={"username": username, "email": email, "password": password})

def api_login(email, password):
    return requests.post(f"{API_URL}/auth/login",
                         json={"email": email, "password": password})


# ── USERS / FOLLOW
def api_get_profile(username, token=None):
    headers = H(token) if token else {}
    return requests.get(f"{API_URL}/users/{username}", headers=headers)

def api_toggle_follow(username, token):
    return requests.post(f"{API_URL}/users/{username}/follow", headers=H(token))

def api_get_followers(username):
    return requests.get(f"{API_URL}/users/{username}/followers")

def api_get_following(username):
    return requests.get(f"{API_URL}/users/{username}/following")


# ── POSTS
def api_get_posts(token=None):
    headers = H(token) if token else {}
    return requests.get(f"{API_URL}/posts", headers=headers)

def api_search_posts(username, token=None):
    headers = H(token) if token else {}
    return requests.get(f"{API_URL}/posts/search", params={"username": username}, headers=headers)

def api_get_saved_posts(token):
    return requests.get(f"{API_URL}/posts/saved", headers=H(token))

def api_create_post(content, token):
    return requests.post(f"{API_URL}/posts", json={"content": content}, headers=H(token))

def api_update_post(post_id, content, token):
    return requests.put(f"{API_URL}/posts/{post_id}", json={"content": content}, headers=H(token))

def api_delete_post(post_id, token):
    return requests.delete(f"{API_URL}/posts/{post_id}", headers=H(token))


# ── LIKE
def api_toggle_like(post_id, token):
    return requests.post(f"{API_URL}/posts/{post_id}/like", headers=H(token))


# ── COMMENT
def api_add_comment(post_id, content, token):
    return requests.post(f"{API_URL}/posts/{post_id}/comments",
                         json={"content": content}, headers=H(token))

def api_delete_comment(comment_id, token):
    return requests.delete(f"{API_URL}/comments/{comment_id}", headers=H(token))


# ── SAVE
def api_toggle_save(post_id, token):
    return requests.post(f"{API_URL}/posts/{post_id}/save", headers=H(token))