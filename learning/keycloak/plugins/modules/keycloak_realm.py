#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.learning.keycloak.plugins.module_utils.keycloak import KeycloakAPI

def main():
    module_args = {
        "url": {"type": "str", "required": True},
        "token": {"type": "str", "required": True, "no_log": True},
        "realm": {"type": "str", "required": True},
        "validate_certs": {"type": "bool", "default": False}
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    keycloak = KeycloakAPI(module.params['url'], module.params['token'], module.params['validate_certs'])

    try:
        result = keycloak.create_realm(module.params['realm'])
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()