from charms.reactive import hook, set_state
from charms import ansible
from charmhelpers.core.hookenv import status_set


@hook('install', 'upgrade-charm')
def install_and_upgrade_ansible():
    ''' Install Ansible from archive '''
    # TODO - support offline installation from resources
    status_set('maintenance', 'installing ansible')
    ansible.install_ansible_support()
    status_set('active', '')
    set_state('ansible.available')
