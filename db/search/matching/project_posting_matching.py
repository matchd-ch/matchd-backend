from db.models import ProjectPosting, ProjectPostingState, MatchType


class ProjectPostingMatching:

    def __init__(self, user):
        self.user = user

    def find_matches(self):
        project_postings = ProjectPosting.objects.filter(state=ProjectPostingState.PUBLIC)

        matches = []
        for project_posting in project_postings:
            if project_posting.student is not None:
                name = project_posting.student.nickname
            else:
                name = project_posting.company.name

            matches.append({
                'id': project_posting.id,
                'name': name,
                'avatar': None,
                'type': MatchType.PROJECT_POSTING,
                'slug': project_posting.slug,
                'score': 1,
                'raw_score': 1,
                'title': project_posting.title,
                'match_status': None
            })

        return matches
