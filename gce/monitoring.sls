{# install/configure googles monitoring service (stackdriver)
   https://cloud.google.com/monitoring/docs #}
{%- set gce = salt['pillar.get']('gce') -%}

include:
  - gce.repo

# If we were using a collectd based setup before, we need to remove that
# since the stackdriver agent bundles it
gce-remove-collectd:
  pkg.purged:
    - pkgs:
      - collectd
      - collectd-core

{% if grains.os_family == 'Debian' %}
# need this to enable the debconf module... even though we are using set not get
gce-install-deps-debconf-utils:
  pkg.installed
{% endif %}

gce-stackdriver-agent:
{% if 'stackdriver_api_key' in gce %}
  {% if grains.os_family == 'Debian' %}
  debconf.set:
    - data:
        'stackdriver-agent/apikey': {'type': 'string', 'value': '{{ gce.stackdriver_api_key }}'}
  {% elif grains.osfinger == "CentOS Linux-7" %}
  cmd.run:
    - name: /opt/stackdriver/stack-config --api-key {{ gce.stackdriver_api_key }}
    - require:
      - pkg: stackdriver-agent
  {% endif %}
{% endif %}
  pkg.installed: []
