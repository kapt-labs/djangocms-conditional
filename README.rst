===============
djangocms-conditional
===============

.. image:: https://pypip.in/v/djangocms-conditional/badge.png
        :target: https://pypi.python.org/pypi/djangocms-conditional
        :alt: Latest PyPI version

.. image:: https://pypip.in/d/djangocms-conditional/badge.png
        :target: https://pypi.python.org/pypi/djangocms-conditional
        :alt: Monthly downloads

django CMS plugin that shows content between specified times


Quickstart
----------

Install djangocms-conditional::

1.  pip install djangocms-conditional


2. Add "djangocms_conditional" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangocms_conditional',
    ]

3. Run `python manage.py migrate` to create the djangocms_conditional models.

Features
--------

Shows and hides child plugins according to group membership, as configured in the plugin instance.

Caveats
-------

This plugin only prevents rendering of plugins, just like djangocms-timer,
and is subject to the same limitations:

In its current form, plugin won't save you from the queries to retrieve child
plugins due to the way plugin rendering works in django CMS. Still, the
``render`` method of child plugins is not executed (and grandchildren plugins
are not retrieved) with mitigating effect on performance hit.
