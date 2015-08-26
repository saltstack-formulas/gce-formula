stackdriver-common-repo:
  pkgrepo.managed:
{% if grains.os_family == 'Debian' %}
    - name: deb http://repo.stackdriver.com/apt {{ salt.grains.get('oscodename') }} main
    - key_url: https://app.google.stackdriver.com/RPM-GPG-KEY-stackdriver
{% elif grains.os_family == "RedHat" %}
    - humanname: Stackdriver Agent Repository
    - baseurl: http://repo.stackdriver.com/repo/el$releasever/$basearch/
    - gpgcheck: 1
    - gpgkey: https://app.stackdriver.com/RPM-GPG-KEY-stackdriver
{% endif %}
    - require_in:
      - pkg: stackdriver-agent
      - pkg: gce-logging-install-pkgs
