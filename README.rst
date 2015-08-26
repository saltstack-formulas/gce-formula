===
GCE
===

Formula to ease working with Google Compute Engine

.. note::

    See the full `Salt Formulas installation and usage instructions
    <http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html>`_.

Available states
================

.. contents::
    :local:

``gce.repo``
------------

Set up GCE/Stackdriver repo (shouldn't need to assign this manually, it's
included by the logging and monitoring states)

``gce.logging``
---------------

Install Google Cloud Logging agent

``gce.monitoring``
------------------

Install Google Cloud Monitoring agent


Optional states
===============

.. contents::
    :local:

``gce.config``
--------------

TODO
If you have "legacy" instances that don't have the logging.write scope, then you
will want to enable this. It enables the use of a private key to write the logs.
See https://cloud.google.com/logging/docs for more info.
