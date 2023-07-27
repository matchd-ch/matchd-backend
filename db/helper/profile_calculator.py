from db.models.student import Student


def get_relevant_student_profile_fields():
    return [
        'street', 'zip', 'city', 'date_of_birth', 'school_name', 'field_of_study', 'graduation',
        'branch', 'skills', 'distinction', 'soft_skills', 'cultural_fits'
    ]


def calculate_student_profile_completion(student: Student):
    relevant_fields = get_relevant_student_profile_fields()

    n_filled_fields = 0

    for relevant_field in relevant_fields:
        field = getattr(student, relevant_field)

        if field:
            # Check if relationships exists
            try:
                if not field.exists():
                    continue
            # pylint: disable=W0702
            except:
                pass

            n_filled_fields += 1

    return n_filled_fields / len(relevant_fields)


def get_missing_relevant_student_profile_fields(student: Student):
    missing_fields = get_relevant_student_profile_fields()

    for relevant_field in get_relevant_student_profile_fields():
        field = getattr(student, relevant_field)

        if field:
            # Check if relationships exists
            try:
                if not field.exists():
                    continue
            # pylint: disable=W0702
            except:
                pass

            missing_fields.remove(relevant_field)

    return missing_fields
