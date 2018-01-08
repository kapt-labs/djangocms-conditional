===============
djangocms-conditional
===============

.. image:: https://pypip.in/v/djangocms-conditional/badge.png
        :target: https://pypi.python.org/pypi/djangocms-conditional
        :alt: Latest PyPI version

.. image:: https://travis-ci.org/nephila/djangocms-conditional.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-conditional
        :alt: Latest Travis CI build status

.. image:: https://pypip.in/d/djangocms-conditional/badge.png
        :target: https://pypi.python.org/pypi/djangocms-conditional
        :alt: Monthly downloads

.. image:: https://coveralls.io/repos/nephila/djangocms-conditional/badge.png
        :target: https://coveralls.io/r/nephila/djangocms-conditional
        :alt: Test coverage

django CMS plugin that shows content between specified times

Documentation
-------------

The full documentation is at https://djangocms-conditional.readthedocs.org.

Quickstart
----------

Install djangocms-conditional::

    pip install djangocms-conditional


Features
--------

Shows and hides child plugins according to group membership, as configured in the plugin instance.

Caveats
-------

This plugin only prevents rendering of plugins, just like djangocms-timer, and is subject to the same limitations:

In its current form, plugin won't save you from the queries to retrieve child
plugins due to the way plugin rendering works in django CMS. Still, the
``render`` method of child plugins is not executed (and grandchildren plugins
are not retrieved) with mitigating effect on performance hit.
