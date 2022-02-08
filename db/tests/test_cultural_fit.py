import pytest

from db.models.cultural_fit import CulturalFit


@pytest.mark.django_db
def test_create_cultural_fit(cultural_fit_valid_args):
    cultural_fit = CulturalFit.objects.create(**cultural_fit_valid_args)

    assert isinstance(cultural_fit, CulturalFit)


@pytest.mark.django_db
def test_get_cultural_fit(cultural_fit_valid_args):
    cultural_fit = CulturalFit.objects.create(**cultural_fit_valid_args)
    cultural_fit = CulturalFit.objects.get(id=cultural_fit.id)

    assert isinstance(cultural_fit, CulturalFit)
    assert isinstance(cultural_fit.student, str)
    assert isinstance(cultural_fit.company, str)

    assert cultural_fit.student == cultural_fit_valid_args.get('student')
    assert cultural_fit.company == cultural_fit_valid_args.get('company')


@pytest.mark.django_db
def test_update_cultural_fit(cultural_fit_valid_args):
    new_company = 'all'
    cultural_fit = CulturalFit.objects.create(**cultural_fit_valid_args)
    CulturalFit.objects.filter(id=cultural_fit.id).update(company=new_company)
    cultural_fit.refresh_from_db()

    assert isinstance(cultural_fit, CulturalFit)
    assert isinstance(cultural_fit.company, str)

    assert cultural_fit.company == new_company


@pytest.mark.django_db
def test_delete_cultural_fit(cultural_fit_valid_args):
    cultural_fit = CulturalFit.objects.create(**cultural_fit_valid_args)
    number_of_deletions, _ = cultural_fit.delete()

    assert number_of_deletions == 1
