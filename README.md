# Rsyslog

This roles installs rsyslog v8 for the log shipping.

For more information on rsyslog please visit [rsyslog docs](http://www.rsyslog.com/doc/v8-stable/).

## Example Playbook

To install:

```YAML
- name: Some app
  hosts: "{{ hosts }}"

  roles:
    - role: rsyslog
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
