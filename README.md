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
  version: v1.1
```

and run `ansible-galaxy install -p ./roles -r roles.yml`




## Tags

This role uses two tags: **build** and **configure**

* `build` - Installs Rsyslog all it's dependencies.




## Builtin log configs

Several builtin configs are included for shipping log files to Logstash, these
builtins are designed for certain log file formats and always output in JSON,
you can see the example settings for each builtin handler in defaults/main.yml
under builtin_configs.

### Syslog files

By default syslog messages are shipped as JSON, no extra config is required for
this.

Syslog messages are shipped in the following format:

* type - always syslog
* host - hostname of origin machine
* timestamp - RFC-3339 formatted date
* version - always 2 for JSON logs
* role - this the app_name field from the rsyslog roles config
* message - the log line itself
* priority - syslog severity number
* program - name of the service that originated the message
* facility - syslog facility
* severity - syslog severity name

```JSON
{
  "type": "syslog",
  "host": "192.168.1.1",
  "timestamp": "2017-10-21T14:29:30.739200+00:00",
  "@version": "2",
  "role": "some_application",
  "message": "Something happened",
  "priority": "3",
  "program": "some-local-service",
  "facility": "daemon",
  "severity": "err"
}
```

### Auth log files

```YAML
rsyslog:
  app_name: some_application
  builtin_configs:
    auth_logs:
      enabled: true
```

Ships auth and authpriv facility messages, uses the same template as Syslog
messages with the type field set to authlog:

```JSON
{
  "type": "authlog",
  "host": "192.168.1.1",
  "timestamp": "2018-01-09T10:45:01.117615+00:00",
  "@version": "2",
  "role": "some_application",
  "message": " pam_unix(cron:session): session closed for user some_user",
  "priority": "6",
  "program": "CRON",
  "facility": "authpriv",
  "severity": "info"
}
```

### Plain text log files

```YAML
rsyslog:
  app_name: some_application
  builtin_configs:
    application_logs:
      enabled: true
      logs:
        - path: "/var/log/some_log.log"
          # type defaults to application_log if not specified
          options:
            type: some_application_log
```

The application_logs builtin is designed to handle log files that are in
plaintext, lines in these log files are shipped as they are to Logstash in the
following JSON format:

* type - type field from the log files config, useful for Logstash filters
* host - hostname of origin machine
* timestamp - RFC-3339 formatted date
* version - always 1 for plain text logs
* role - this the app_name field from the rsyslog roles config
* sourcefile - location of the log file that the line was taken from
* message - the log line itself

For example:

```JSON
{
  "type": "application_log",
  "host": "192.168.1.1",
  "timestamp": "2017-10-21T13:58:40.098660+00:00",
  "@version": "1",
  "role": "some_application_log",
  "sourcefile": "/var/log/some_log.log",
  "message": "A plain text log line"
}
```

### JSON log files

```YAML
rsyslog:
  app_name: some_application
  builtin_configs:
    json_logs:
      enabled: true
      logs:
        - path: "/var/log/some_log.log"
          options:
            type: some_application_log
```

The json_logs builtin is designed to handle log files that are in JSON,
all fields are shipped as JSON with some extras added in:

* type - type field from the log files config, useful for Logstash filters
* host - hostname of origin machine
* version - always 2 for JSON logs
* role - this the app_name field from the rsyslog roles config
* sourcefile - location of the log file that the line was taken from

For example, given the log line:

```JSON
{ "message": "Some log message", "datetime": "2017-01-01 00:00:00", "level": "info" }
```

This would be shipped as:

```JSON
{
  "type": "some_application_log",
  "host": "192.168.1.1",
  "@version": "2",
  "role": "some_application",
  "sourcefile": "/var/log/some_log.log",
  "message": "Some log message",
  "datetime": "2017-01-01 00:00:00",
  "level": "info"
}
```

### Nginx access log files

The nginx_access_logs builtin is essentially the same as the json_logs builtin,
the only difference is that the type field is hardcoded to nginx-access-logs.

To render Nginx access logs in JSON you can use the following config in
nginx.conf:

```
log_format main '{ '
	'"http_host": "$http_host", '
	'"clientip": "$remote_addr", '
	'"datetime": "$time_iso8601", '
	'"verb": "$request_method", '
	'"request_full": "$request", '
	'"response": "$status", '
	'"response_length": "$body_bytes_sent", '
	'"request_length": "$request_length", '
	'"referrer": "$http_referer", '
	'"agent": "$http_user_agent", '
	'"request_time": "$request_time", '
	'"upstream_time": "$upstream_response_time", '
	'"user_id": "$http_x_user", '
	'"request_id": "$http_x_request_id" '
'}';

access_log  /var/log/nginx/access.log main;
```




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

To install specific package versions:

```YAML
- name: Some app
  hosts: "{{ hosts }}"

  roles:
    - role: sansible.rsyslog
      rsyslog:
        version: "8.30*"
        version_libfastjson4: "0.99.*"
        version_mmjsonparse: "8.30.*"
```
