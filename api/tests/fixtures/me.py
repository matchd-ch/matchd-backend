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
                user {
                    id
                    username
                    email
                    firstName
                    lastName
                }
                mobile
                street
                zip
                city
                dateOfBirth
                nickname
                schoolName
                fieldOfStudy
                graduation
                branch {
                    id
                    name
                }
                jobType {
                    id
                    name
                }
                jobFromDate
                jobToDate
                skills {
                    id
                    name
                }
                distinction
                state
                profileStep
                softSkills {
                    id
                }
                culturalFits {
                    id
                }
                slug
                hobbies {
                    name
                }
                onlineProjects {
                    url
                }
                languages {
                  language {
                        name
                  }
                  languageLevel {
                        level
                  }
                }
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
