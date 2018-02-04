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
)
import charms.sshproxy

from subprocess import (
    Popen,
    CalledProcessError,
    PIPE,
)

#from charms.ansible import apply_playbook
import os, fnmatch
import subprocess

cfg = config()


# Sets the status of the charm to show in OSM: configured
@when('config.changed')
def config_changed():
    set_flag('ansible-charm.configured')
    status_set('active', 'ready!')
    return


# Edits ansible config files and executes ansible-playbook
@when('ansible-charm.configured')
@when('actions.ansible-playbook')
def ansible_playbook():
    try:
        # Retrieve the ssh parameter
        cfg = config()
        # edit ansible hosts file with the VNF parameters
        h = open("/etc/ansible/hosts", "wt")
        h.write("[targets]\n")
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
    except Exception as e:
        action_fail('command failed: {}, errors: {}'.format(e, e.output))
        remove_flag('actions.ansible-playbook')
        return
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
