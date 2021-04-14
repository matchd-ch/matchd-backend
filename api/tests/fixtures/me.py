import pytest

# pylint: disable=C0103


def me_query():
    return '''
    query {
        me {
            username
            firstName
            lastName
            email
            type
            student {
                profileStep
                state
                mobile
                zip
                street
                city
                dateOfBirth
                nickname
                schoolName
                fieldOfStudy
                graduation
                distinction
                slug
                branch {
                    id
                    name
                }
                jobType {
                    id
                    name
                    mode
                }
                skills {
                    id
                    name
                }
                hobbies {
                    id
                    name
                }
                languages {
                    id
                    language {
                        id
                        name
                    }
                    languageLevel {
                        id
                        level
                        description
                    }
                }
                onlineProjects {
                    id
                    url
                }
                softSkills {
                    id
                    student
                    company
                }
                culturalFits {
                    id
                    student
                    company
                }
            }
            company {
                uid
                type
                name
                slug
                zip
                city
                street
                phone
                website
                description
                services
                memberItStGallen
                state
                profileStep
                benefits {
                    id
                    icon
                }
                branches {
                    id
                    name
                }
                employees {
                    id
                    role
                    user {
                        id
                        username
                        email
                        type
                        firstName
                        lastName
                    }
                }
                softSkills {
                    id
                    student
                    company
                }
                culturalFits {
                    id
                    student
                    company
                }
                topLevelOrganisationDescription
                topLevelOrganisationWebsite
                linkEducation
                linkProjects
                linkThesis
            }
        }
    }
    '''


@pytest.fixture
def me(execute):
    def closure(user):
        return execute(me_query(), **{'user': user})
    return closure
