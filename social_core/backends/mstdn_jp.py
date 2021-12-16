"""
mastodon_jp OAuth2 backend, docs at:
"""
from __future__ import unicode_literals
from .oauth import BaseOAuth2
import json

class Mastodon_jpOAuth2(BaseOAuth2):
    """mastodon_jp OAuth authentication backend"""
    name = 'mastodon_jp'
    AUTHORIZATION_URL = 'https://mstdn.jp/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://mstdn.jp/api/oauth.access'
    ACCESS_TOKEN_METHOD = 'POST'
    DEFAULT_SCOPE = ['read', 'write']
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = True
    EXTRA_DATA = [
        ('id', 'id'),
        ('acct', 'acct'),
        ('locked', 'locked'),
        ('bot', 'bot'),
        ('note', 'note'),
        ('url', 'url'),
        ('avatar', 'avatar')
    ]

    def auth_complete_params(self, state=None):
        data = super().auth_complete_params(state)
        if 'grant_type' in data:
            del data['grant_type']
        if 'redirect_uri' in data:
            del data['redirect_uri']
        return json.dumps(data)

    def auth_headers(self):
        return {'Content-Type': 'application/json'}

    def request_access_token(self, *args, **kwargs):
        data = super().request_access_token(*args, **kwargs)
        data.update({'access_token': data['token']})
        return data

    def get_user_details(self, response):
        """Return user details from mstdn.jp account"""
        return {
            'username': response['username'],
            'fullname': response['display_name'],
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://mstdn.jp/api/v1/accounts/verify_credentials',
            headers={
                'User-Agent': 'Tootutil',
                'Authorization': 'Bearer {0}'.format(access_token)
            }
        )

