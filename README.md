# Rsyslog

Master: [![Build Status](https://travis-ci.org/sansible/rsyslog.svg?branch=master)](https://travis-ci.org/sansible/rsyslog)  
Develop: [![Build Status](https://travis-ci.org/sansible/rsyslog.svg?branch=develop)](https://travis-ci.org/sansible/rsyslog)

* [ansible.cfg](#ansible-cfg)
* [Installation and Dependencies](#installation-and-dependencies)
* [Tags](#tags)
* [Examples](#examples)

This roles installs rsyslog v8 for the log shipping.

For more information on rsyslog please visit [rsyslog docs](http://www.rsyslog.com/doc/v8-stable/).




## ansible.cfg

This role is designed to work with merge "hash_behaviour". Make sure your
ansible.cfg contains these settings

```INI
[defaults]
hash_behaviour = merge
```




## Installation and Dependencies

To install run `ansible-galaxy install sansible.rsyslog` or add this to your
`roles.yml`

```YAML
- name: sansible.rsyslog
  version: v1.0
```

and run `ansible-galaxy install -p ./roles -r roles.yml`




## Tags

This role uses two tags: **build** and **configure**

* `build` - Installs Rsyslog all it's dependencies.





## Examples

To install:

```YAML
- name: Some app
  hosts: "{{ hosts }}"

  roles:
    - role: sansible.rsyslog
      rsyslog:
        app_name: default_app
        builtin_configs:
          # generic handler for text based, unformatted log files
          application_logs:
            enabled: true
            logs:
              - path: "/home/application_user/app_log.log"
          json_logs:
            enabled: true
            logs:
              - path: "/home/application_user/app_log_json.log"
                options:
                  type_tag: "application_log"
          nginx_access_logs:
            enabled: true
            logs:
              - path: "/var/log/nginx/application_access.log"
```

To install without default config:

```YAML
- name: Some app
  hosts: "{{ hosts }}"

  roles:
    - role: sansible.rsyslog
      rsyslog:
        app_name: default_app
        default_config: no
```
