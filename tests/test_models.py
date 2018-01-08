# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.template import RequestContext
from django.test import Client
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from cms.api import add_plugin
from cms.plugin_rendering import ContentRenderer
from djangocms_helper.base_test import BaseTestCase


class TestPlugin(BaseTestCase):
    _pages_data = (
        {'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'Titre', 'publish': True},
         'it': {'title': 'Titolo pagina', 'publish': False}},
    )

    def setUp(self):
        #create permissions group
        self.group = Group(name="My Test Group")
        self.group.save()
        self.group2 = Group(name="My Test Group 2")
        self.group2.save()
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.user.groups.add(self.group)
        self.user.save()

    def tearDown(self):
        self.user.delete()
        self.group.delete()

    def test_basic_context_setup(self):
        page1, = self.get_pages()
        ph = page1.placeholders.get(slot='content')

        plugin_data = {
            'permitted_group': self.group
        }
        plugin = add_plugin(ph, 'ConditionalContainerPlugin', language='en', **plugin_data)
        instance, plugin_class = plugin.get_plugin_instance()
        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        context = RequestContext(request, {})
        pl_context = plugin_class.render(context, instance, ph)
        self.assertTrue('instance' in pl_context)
        self.assertEqual(pl_context['instance'], instance)
        self.assertEqual(force_text(instance),
                         _(u'Access granted to %s') % self.group.name)

        plugin_data = {
            'permitted_group': self.group2
        }
        plugin = add_plugin(ph, 'ConditionalContainerPlugin', language='en', **plugin_data)
        instance, plugin_class = plugin.get_plugin_instance()
        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        context = RequestContext(request, {})
        pl_context = plugin_class.render(context, instance, ph)
        self.assertFalse('instance' in pl_context)

    def test_children_shown(self):
        page1, = self.get_pages()
        ph = page1.placeholders.get(slot='content')

        text_content = u"Child plugin"

        plugin_data = {
            'permitted_group': self.group
        }
        plugin_1 = add_plugin(ph, 'ConditionalContainerPlugin', language='en', **plugin_data)
        plugin_1.save()

        # child of plugin_1
        plugin_2 = add_plugin(ph, u"TextPlugin", u"en", body=text_content)
        plugin_1 = self.reload_model(plugin_1)
        plugin_2.parent = plugin_1
        plugin_2.save()

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {})
        context['user'] = self.user
        content = renderer.render_plugin(plugin_1, context)
        self.assertEqual(content, text_content)

    def test_children_hidden(self):
        page1, = self.get_pages()
        ph = page1.placeholders.get(slot='content')

        text_content = u"Child plugin"

        plugin_data = {
            'permitted_group': self.group2
        }
        plugin_1 = add_plugin(ph, 'ConditionalContainerPlugin', language='en', **plugin_data)
        plugin_1.save()

        # child of plugin_1
        plugin_2 = add_plugin(ph, u"TextPlugin", u"en", body=text_content)
        plugin_1 = self.reload_model(plugin_1)
        plugin_2.parent = plugin_1
        plugin_2.save()

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {})
        context['user'] = self.user
        content = renderer.render_plugin(plugin_1, context)
        self.assertEqual(content, u'')
