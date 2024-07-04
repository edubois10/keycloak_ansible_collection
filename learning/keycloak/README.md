# Keycloak Ansible Collection

This collection provides modules to manage Keycloak realms and users through the Keycloak API.

## First Steps:
```
ansible-galaxy collection init learning.keycloak

ansible-galaxy collection build

ansible-galaxy collection install learning-keycloak-1.0.0.tar.gz
```
## Modules

### keycloak_realm

Creates or manages Keycloak realms.

#### Parameters

- `url` (required): The base URL of the Keycloak server.
- `token` (required): The admin token for authentication.
- `realm` (required): The name of the realm to create.

## Example Playbook

```yaml
---
- name: Manage Keycloak Realm
  hosts: localhost
  tasks:
    - name: Create Keycloak realm
      learning.keycloak.keycloak_realm:
        url: "http://localhost:8080"
        token: "your_keycloak_admin_token"
        realm: "my_realm"

