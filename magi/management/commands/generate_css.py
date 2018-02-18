# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings as django_settings
from magi.settings import USER_COLORS
import pkg_resources

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        resource_package = 'magi'
        resource_path = os.path.join('static', 'less', 'per-color-generator.less')
        template = pkg_resources.resource_string(resource_package, resource_path)

        all_colors = u'// This is a generated file. Do not edit this file manually\n\
// To re-generate this file, use `python manage.py generate_css`\n\n'
        for color in USER_COLORS:
            all_colors += template.replace('HEX_COLOR', color[3]).replace('COLOR_NAME', color[0]).replace('COLOR', color[2])
        print all_colors

        path = os.path.join(django_settings.BASE_DIR, django_settings.SITE, 'static', 'less', 'generated_colors.less')
        print path

        with open(path, 'w+') as f:
            f.write(all_colors.encode('UTF-8'))
            f.close()