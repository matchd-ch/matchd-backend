import pytest

# pylint: disable=C0103


def me_query():
    return '''
    query {
        me {
            id
            username
            firstName
            lastName
            email
            type
            student {
                id
                email
                firstName
                lastName
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
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
                distinction
                state
                softSkills {
                    edges {
                        node {
                            id
                        }
                    }
                }
                culturalFits {
                    edges {
                        node {
                            id
                        }
                    }
                }
                slug
                hobbies {
                    name
                }
                onlineChallenges {
                    url
                }
                languages {
                    edges {
                        node {
                            language {
                                name
                            }
                            languageLevel {
                                level
                            }
                        }
                    }
                }
                challenges {
                    slug
                }
            }
            company {
                uid
                type
                name
                displayName
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
                benefits {
                    edges {
                        node {
                            id
                            icon
                        }
                    }
                }
                branches {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
                employees {
                    id
                    role
                    email
                    firstName
                    lastName
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
                linkChallenges
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
