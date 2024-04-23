# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group, User, AnonymousUser
from django.template import RequestContext

from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from djangocms_helper.base_test import BaseTestCase

from djangocms_conditional.cms_plugins import ConditionalContainerPlugin


class TestPlugin(BaseTestCase):
    _pages_data = (
        {'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'Titre', 'publish': True},
         'it': {'title': 'Titolo pagina', 'publish': False}},
    )

    def setup_plugin(self, group, mode='in_group'):
        from cms.api import add_plugin
        page1, = self.get_pages()
        placeholder = page1.placeholders.get(slot='content')
        parent_plugin = add_plugin(
            placeholder,
            ConditionalContainerPlugin,
            'en',
            permitted_group=group,
            mode=mode
        )
        parent_plugin.save()

        text_content = "Child plugin"
        text_plugin = add_plugin(placeholder, "TextPlugin", "en", body=text_content, target=parent_plugin,)
        text_plugin.save()

        parent_plugin.child_plugin_instances = [text_plugin]

        return page1, text_plugin, parent_plugin, text_content

    def setUp(self):
        # create permissions group
        self.group = Group(name="My Test Group")
        self.group.save()
        self.group2 = Group(name="My Test Group 2")
        self.group2.save()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.user.groups.add(self.group)
        self.user.save()

    def tearDown(self):
        self.user.delete()
        self.group.delete()

    def test_plugin_context(self):
        from cms.api import add_plugin
        placeholder = Placeholder.objects.create(slot='content')
        model_instance = add_plugin(
            placeholder,
            ConditionalContainerPlugin,
            'en',
            permitted_group=self.group
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertNotIn('instance', context)
        context = plugin_instance.render({"user": self.user}, model_instance, None)
        self.assertIn('instance', context)

    def test_children_shown(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group)

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, text_content)

    def test_children_not_shown(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group2)

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')

    def test_children_not_shown_anon(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group2)

        request = self.get_page_request(page1, AnonymousUser(), r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": AnonymousUser(),
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')

    def test_exclude_mode_not_member(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group2,
                                                                            mode='not_in_group')

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, text_content)

    def test_exclude_mode_member(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='not_in_group')

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')

    def test_exclude_mode_anon(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='not_in_group')

        request = self.get_page_request(page1, AnonymousUser(), r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": AnonymousUser(),
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')

    def test_exclude_anon_mode_not_member(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group2,
                                                                            mode='not_in_group_plus_anon')

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, text_content)

    def test_exclude_anon_mode_member(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='not_in_group_plus_anon')

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')

    def test_exclude_anon_mode_anon(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='not_in_group_plus_anon')

        request = self.get_page_request(page1, AnonymousUser(), r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": AnonymousUser(),
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, text_content)

    def test_anon_mode_anon(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='anonymous')

        request = self.get_page_request(page1, AnonymousUser(), r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": AnonymousUser(),
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, text_content)

    def test_anon_mode_registered(self):
        page1, text_plugin, parent_plugin, text_content = self.setup_plugin(group=self.group,
                                                                            mode='anonymous')

        request = self.get_page_request(page1, self.user, r'/en/', lang='en')
        renderer = ContentRenderer(request=request)
        context = RequestContext(request, {
            "user": self.user,
            "cms_content_renderer": renderer})

        child_html = renderer.render_plugin(text_plugin, context)
        parent_html = renderer.render_plugin(parent_plugin, context)

        self.assertEqual(child_html, text_content)
        self.assertEqual(parent_html, '')
