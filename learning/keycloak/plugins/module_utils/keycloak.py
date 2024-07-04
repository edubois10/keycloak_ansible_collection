import requests

class KeycloakAPI:
    def __init__(self, url, token, validate_certs=True):
        self.url = url
        self.token = token
        self.validate_certs = validate_certs
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def create_realm(self, realm):
        endpoint = f"{self.url}/admin/realms"
        payload = {"realm": realm, "enabled": True}
        response = requests.post(endpoint, json=payload, headers=self.headers, verify=self.validate_certs)
        return self._handle_response(response)

    def create_user(self, realm, user):
        user_payload = {k: v for k, v in user.items() if k != 'password'}
        endpoint = f"{self.url}/admin/realms/{realm}/users"
        response = requests.post(endpoint, json=user_payload, headers=self.headers, verify=self.validate_certs)
        result = self._handle_response(response)
        if result['changed']:
            # Set the user's password if user creation is successful
            self.set_user_password(realm, user['username'], user['password'])
        return result

    def set_user_password(self, realm, username, password):
        # Retrieve user ID by username
        user_id = self.get_user_id_by_username(realm, username)
        if not user_id:
            raise Exception(f"User {username} not found")

        endpoint = f"{self.url}/admin/realms/{realm}/users/{user_id}/reset-password"
        payload = {
            "type": "password",
            "value": password,
            "temporary": False
        }
        response = requests.put(endpoint, json=payload, headers=self.headers, verify=self.validate_certs)
        response.raise_for_status()
        return {"changed": True, "msg": "Password set"}

    def get_user_id_by_username(self, realm, username):
        endpoint = f"{self.url}/admin/realms/{realm}/users"
        params = {"username": username}
        response = requests.get(endpoint, headers=self.headers, params=params, verify=self.validate_certs)
        response.raise_for_status()
        users = response.json()
        if users:
            return users[0]['id']
        return None

    def _handle_response(self, response):
        if response.status_code == 201:
            return {"changed": True, "msg": "Resource created"}
        elif response.status_code == 409:
            return {"changed": False, "msg": "Resource already exists"}
        else:
            response.raise_for_status()