import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('package', [
    ('libfastjson4'),
    ('rsyslog'),
    ('rsyslog-mmjsonparse'),
])
def test_installed_apt_packages(host, package):
    assert host.package(package).is_installed


@pytest.mark.parametrize('filename', [
    ('/etc/rsyslog.conf'),
    ('/etc/rsyslog.d/10-cloud-init-logs-shipping.conf'),
    ('/etc/rsyslog.d/11-nginx-access-logs-shipping.conf'),
    ('/etc/rsyslog.d/13-json-logs-shipping.conf'),
    ('/etc/rsyslog.d/14-auth-logs-shipping.conf'),
    ('/etc/rsyslog.d/15-docker-text-logs-shipping.conf'),
    ('/etc/rsyslog.d/16-docker-json-logs.shipping.conf'),
    ('/etc/rsyslog.d/17-docker-journald-logs.shipping.conf'),
    ('/etc/rsyslog.d/90-syslog-shipping.conf'),
])
def test_added_files(host, filename):
    assert host.file(filename).exists


@pytest.mark.parametrize('filename', [
    ('/etc/rsyslog.d/20-ufw.conf'),
    ('/etc/rsyslog.d/21-cloudinit.conf'),
])
def test_deleted_files(host, filename):
    assert not host.file(filename).exists


@pytest.mark.parametrize('filename,should_contain_regex', [
    ('/etc/rsyslog.conf', r'maxMessageSize="32K"'),
    ('/etc/rsyslog.conf', r'queue.size="100000"'),
    (
        '/etc/rsyslog.d/10-cloud-init-logs-shipping.conf',
        r'reopenOnTruncate="off"'
    ),
    (
        '/etc/rsyslog.d/90-syslog-shipping.conf',
        r'action.resumeRetryCount="10"'
    ),
])
def test_config(host, filename, should_contain_regex):
    config_file = host.file(filename)
    assert config_file.contains(should_contain_regex)
