from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2PasswordRequestFormNoGrant(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Form(...), password: str = Form(...)):
        # ignore grant_type, scope, etc.
        self.username = username
        self.password = password
        self.scopes = []
        self.client_id = None
        self.client_secret = None