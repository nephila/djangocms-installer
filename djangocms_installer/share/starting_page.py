import json


def create_pages():
    from cms.api import add_plugin, create_page, publish_page
    from cms.models import Placeholder
    from django.conf import settings
    from django.contrib.auth.models import User
    from django.utils.translation import ugettext_lazy as _

    placeholder = {}

    with open("starting_page.json") as data_file:
        content = json.load(data_file)

    try:
        # try to get a feature template with fallback
        template = settings.CMS_TEMPLATES[1][0]
        if template != "feature.html":
            template = settings.CMS_TEMPLATES[0][0]
    except IndexError:
        template = settings.CMS_TEMPLATES[0][0]

    lang = settings.LANGUAGES[0][0]
    page = create_page(_("Home"), template, lang)
    placeholder["main"] = page.placeholders.get(slot="content")

    try:
        # try to get a feature placeholder
        placeholder_feature = page.placeholders.get(slot="feature")
        add_plugin(placeholder_feature, "TextPlugin", lang, body=content["feature"])
    except Placeholder.DoesNotExist:
        # fallback, add it to the
        add_plugin(placeholder["main"], "TextPlugin", lang, body=content["feature"])

    # Add main content to a Bootstrap4GridRow
    row_plugin = add_plugin(placeholder["main"], "Bootstrap4GridRowPlugin", lang)
    for column_content in content["main"]:
        col = add_plugin(placeholder["main"], "Bootstrap4GridColumnPlugin", lang, target=row_plugin)
        add_plugin(placeholder["main"], "TextPlugin", lang, body=column_content, target=col)

    # In order to publish the page there needs to be at least one user
    if User.objects.count() > 0:
        publish_page(page, User.objects.all()[0], lang)


if __name__ == "__main__":
    import django

    django.setup()
    create_pages()
