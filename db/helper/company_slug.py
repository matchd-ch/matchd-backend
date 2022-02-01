from django.apps import apps
from django.utils.text import slugify


def get_company_slug(name):
    company_model = apps.get_model('db', 'company')
    slug = slugify(name)
    slug_exists = company_model.objects.filter(slug=slug).exists()
    if not slug_exists:
        return slug

    count = 1
    while slug_exists:
        slug_with_counter = f'{slug}-{count}'
        slug_exists = company_model.objects.filter(slug=slug_with_counter).exists()
        if slug_exists:
            count += 1
        else:
            slug = slug_with_counter
    return slug
