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

cfg = config()

@when_not('ansible-charm-v2.configured')
def not_configured():
    """Check the current configuration.

    Check the current values in config to see if we have enough
    information to continue.
    """
    config_changed()


@when('config.changed', 'sshproxy.configured')
def config_changed():
    """Verify the configuration.

    Verify that the charm has been configured
    """

    try:
        status_set('maintenance', 'Verifying configuration data...')
        set_flag('actions.ansible-playbook')

        (validated, output) = charms.sshproxy.verify_ssh_credentials()
        if not validated:
            status_set('blocked', 'Unable to verify SSH credentials: {}'.format(
                output
            ))
            return
        set_flag('ansible-charm-v2.configured')
        status_set('active', 'configuration ready!')

    except Exception as err:
        status_set('blocked', 'Waiting for valid configuration ({})'.format(err))


@when('config.changed')
@when_not('sshproxy.configured')
def invalid_credentials():
    status_set('blocked', 'Waiting for SSH credentials.')
    pass


#@when('ansible-charm-v2.configured')
#@when('actions.install-ansible')
#def install_ansible():
#    try:
#        call_install = ['apt', 'install', 'ansible', 'sshpass', '-y']
#        subprocess.check_call(call_install)
#    except Exception as e:
#        err = "{}".format(e)
#        action_fail('command failed: {}'.format(err))
#        remove_flag('actions.install-ansible')
#        return
#    finally:
#        remove_flag('actions.install-ansible')


#@when('ansible-charm-v2.configured')
#@when('actions.start')
#def start():
#    try:
#        # edit ansible hosts file with the VNF parameters
#        h = open("/etc/ansible/hosts", "wt")
#        h.write("[targets]\n")
#        #h1 = "{} ansible_connection=ssh ansible_ssh_user={} ansible_ssh_pass={}\n".format(cfg['ssh-hostname'],cfg['ssh-username'],cfg['ssh-password'])
#        h1 = "{} ansible_connection=ssh ansible_ssh_user={} ansible_ssh_pass={} ansible_become_pass={}\n".format(cfg['ssh-hostname'],cfg['ssh-username'],cfg['ssh-password'],cfg['ssh-password'])
#        h.write(h1)
#        h.close()
#        # edit ansible config to enable ssh connection with th VNF
#        c = open("/etc/ansible/ansible.cfg", "wt")
#        c.write("[defaults]\n")
#        c.write("host_key_checking = False\n")
#        c.close()
#        # execute the ansible playbook
#        path = find('playbook.yaml','/var/lib/juju/agents/')
#        call = ['ansible-playbook', path]
#        subprocess.check_call(call)
#    except Exception as e:
#        action_fail('command failed: {}'.format(e))
#        remove_flag('actions.start')
#        return
#    finally:
#        remove_flag('actions.start')


@when('ansible-charm-v2.configured')
@when('actions.ansible-playbook')
def ansible_playbook():
    try:
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
        status_set('active', 'ready!')
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
