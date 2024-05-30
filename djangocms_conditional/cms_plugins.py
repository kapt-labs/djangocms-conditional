# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import gettext_lazy as _

from .models import ConditionalPluginModel, MODE_IN_GROUP, MODE_NOT_IN_GROUP, MODE_NOT_IN_GROUP_PLUS_ANON, \
    MODE_ANONYMOUS
from .forms import ConditionalPluginForm


class ConditionalContainerPlugin(CMSPluginBase):
    name = _('Conditional content')
    model = ConditionalPluginModel
    form = ConditionalPluginForm
    allow_children = True
    cache = False
    render_template = 'djangocms_conditional/conditional.html'

    def render(self, context, instance, placeholder):
        # Obtain user
        user = None  # type: User
        if hasattr(context, 'request') and hasattr(context.request, 'user'):
            user = context.request.user
        if 'user' in context:
            user = context['user']

        if not user:
            user = AnonymousUser()  # Should never happen

        # This could be coded more efficiently, but is this way for clarity
        if user.is_superuser:
            context['conditional_config'] = instance
        elif instance.mode == MODE_IN_GROUP:
            if user.groups.filter(id=instance.permitted_group.id).exists():
                context['conditional_config'] = instance
        elif instance.mode == MODE_NOT_IN_GROUP:
            if not (user.is_anonymous or user.groups.filter(id=instance.permitted_group.id).exists()):
                context['conditional_config'] = instance
        elif instance.mode == MODE_ANONYMOUS:
            if user.is_anonymous:
                context['conditional_config'] = instance
        elif instance.mode == MODE_NOT_IN_GROUP_PLUS_ANON:
            if user.is_anonymous or not user.groups.filter(id=instance.permitted_group.id).exists():
                context['conditional_config'] = instance

        return context


plugin_pool.register_plugin(ConditionalContainerPlugin)
