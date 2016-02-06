# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
from distutils.version import LooseVersion


def create_pages():
    from cms.models import Placeholder
    from cms.api import create_page, add_plugin, publish_page
    from django.conf import settings
    from django.contrib.auth.models import User
    from django.utils.translation import ugettext_lazy as _

    placeholder = {}

    with open('starting_page.json') as data_file:
        content = json.load(data_file)

    try:
        # try to get a feature template with fallback
        template = settings.CMS_TEMPLATES[1][0]
        if template != 'feature.html':
            template = settings.CMS_TEMPLATES[0][0]
    except IndexError:
        template = settings.CMS_TEMPLATES[0][0]

    lang = settings.LANGUAGES[0][0]
    page = create_page(_('Home'), template, lang)
    placeholder['main'] = page.placeholders.get(slot='content')

    try:
        # try to get a feature placeholder
        placeholder_feature = page.placeholders.get(slot='feature')
        add_plugin(placeholder_feature, 'TextPlugin', lang,
                   body=content['feature'])
    except Placeholder.DoesNotExist:
        # fallback, add it to the
        add_plugin(placeholder['main'], 'TextPlugin', lang, body=content['feature'])

    # Add main content to a MultiColumnPlugin
    multi_columns_plugin = add_plugin(placeholder['main'], 'MultiColumnPlugin', lang)
    for column_content in content['main']:
        col = add_plugin(placeholder['main'], 'ColumnPlugin', lang,
                         target=multi_columns_plugin, **{'width': '33%'})
        add_plugin(placeholder['main'], 'TextPlugin', lang, body=column_content,
                   target=col)

    # In order to publish the page there needs to be at least one user
    if User.objects.count() > 0:
        try:
            publish_page(page, User.objects.all()[0], lang)
        except TypeError:
            # supporting old cms versions
            publish_page(page, User.objects.all()[0])

if __name__ == '__main__':
    import django

    if LooseVersion(django.get_version()) >= LooseVersion('1.7'):
        django.setup()
    create_pages()
