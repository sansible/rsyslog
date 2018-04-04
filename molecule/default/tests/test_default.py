import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_installed_packages(host):
    assert host.package('libfastjson4').is_installed
    assert host.package('rsyslog').is_installed
    assert host.package('rsyslog-mmjsonparse').is_installed


def test_files(host):
    to_add = [
        '/etc/rsyslog.conf',
        '/etc/rsyslog.d/10-cloud-init-logs-shipping.conf',
        '/etc/rsyslog.d/11-nginx-access-logs-shipping.conf',
        '/etc/rsyslog.d/13-json-logs-shipping.conf',
        '/etc/rsyslog.d/14-auth-logs-shipping.conf',
        '/etc/rsyslog.d/15-docker-text-logs-shipping.conf',
        '/etc/rsyslog.d/16-docker-json-logs.shipping.conf',
        '/etc/rsyslog.d/90-syslog-shipping.conf',
    ]
    for config in to_add:
        assert host.file(config).exists

    to_delete = [
        '/etc/rsyslog.d/20-ufw.conf', '/etc/rsyslog.d/21-cloudinit.conf',
    ]
    for config in to_delete:
        assert not host.file(config).exists
