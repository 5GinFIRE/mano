from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    config,
    status_set,
)
from charms.reactive import (
    remove_state as remove_flag,
    set_state as set_flag,
    when,
    when_not,
)
import charms.sshproxy
import os, fnmatch
import subprocess


@when('sshproxy.configured')
@when('ansible.available')
@when_not('ansible-charm-v2.installed')
def install_ansible_v2_proxy_charm():
    """Post-install actions.

    This function will run when two conditions are met:
    1. The 'sshproxy.configured' state is set
    2. The 'ansible.available' state is set
    3. The 'ansible-charm-v2.installed' state is not set

    This ensures that the workload status is set to active only when the SSH
    proxy is properly configured and the ansible software is installed.
    """
    set_flag('ansible-charm-v2.installed')
    set_flag('actions.ansible-playbook')
    status_set('active', 'Ready!')

@when('ansible-charm-v2.installed')
@when('actions.ansible-playbook')
def ansible_playbook():
    try:
        cfg = config()
        # edit ansible hosts file with the VNF parameters
        h = open("/etc/ansible/hosts", "wt")
        h.write("[targets]\n")
        #h1 = "{} ansible_connection=ssh ansible_ssh_user={} ansible_ssh_pass={}\n".format(cfg['ssh-hostname'],cfg['ssh-username'],cfg['ssh-password'])
        h1 = "{} ansible_connection=ssh ansible_ssh_user={} ansible_ssh_pass={} ansible_become_pass={}\n".format(cfg['ssh-hostname'],cfg['ssh-username'],cfg['ssh-password'],cfg['ssh-password'])
        h.write(h1)
        h.close()
        # edit ansible config to enable ssh connection with th VNF
        c = open("/etc/ansible/ansible.cfg", "wt")
        c.write("[defaults]\n")
        c.write("host_key_checking = False\n")
        c.close()
        # execute the ansible playbook
        path = find('playbook.yaml','/var/lib/juju/agents/')
        call = ['ansible-playbook', path]
        subprocess.check_call(call)
        #status_set('active', 'ready!')
    except Exception as e:
        action_fail('command failed: {}'.format(e))
    else:
        remove_flag('actions.ansible-playbook')
    finally:
        remove_flag('actions.ansible-playbook')


# Function to find the playbook path
def find(pattern, path):
    result = ''
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result = os.path.join(root, name)
    return result
