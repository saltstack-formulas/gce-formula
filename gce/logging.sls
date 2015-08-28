{# install/configure Googles logging, for more info, se the following
   https://cloud.google.com/logging/docs/ #}
{%- set gce = salt['pillar.get']('gce') -%}
include:
  - gce.repo

gce-logging-install-pkgs:
  pkg.installed:
    - pkgs:
      - google-fluentd
      - google-fluentd-catch-all-config

{% if 'config_private_key' in gce %}
gce-logging-private-key:
  file.managed:
    - name: /etc/google-fluentd/keyfile.p12
    - contents_pillar: gce:config_private_key
    - makedirs: True
    - user: root
    - group: root
    - mode: 400
    - listen_in:
      - service: gce-logging-service
    - unless:
      - /usr/share/google/get_metadata_value service-accounts/default/scopes | grep -q logging.write
{% endif %}

gce-logging-main-config-file:
  file.managed:
    - name: /etc/google-fluentd/google-fluentd.conf
    - source: salt://gce/files/google-fluentd.conf
    - template: jinja
    - listen_in:
      - service: gce-logging-service
    # dont need to do any configuration if the instance has the logging.write scope
    - unless:
      - /usr/share/google/get_metadata_value service-accounts/default/scopes | grep -q logging.write
{#
    You can put your own custom fluentd config files in <file_roots>/gce/files/config.d/
    and they will automatically be included during install
#}
gce-logging-config-extra:
  file.recurse:
    - name: /etc/google-fluentd/config.d/
    - source: salt://gce/files/config.d/

gce-logging-service:
  service.running:
    - name: google-fluentd
    - enable: True
