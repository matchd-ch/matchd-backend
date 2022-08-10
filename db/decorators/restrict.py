from db.models.project_posting import ProjectPosting


def hide_project_posting_attributes(project_posting):
    project_posting.team_size = None
    project_posting.compensation = None
    project_posting.website = ""
    project_posting.employee = None
    project_posting.student = None
    project_posting.company = None
    project_posting.match_status = None
    project_posting.match_hints = None
    project_posting.form_step = 0

    return project_posting


def restrict_project_posting(func):

    def wrapper(self, info, **kwargs):
        result = func(self, info, **kwargs)

        if info.context.user is None or not info.context.user.is_authenticated:
            if isinstance(result, ProjectPosting):
                result = hide_project_posting_attributes(result)
            else:
                result = list(map(hide_project_posting_attributes, result))

        return result

    return wrapper


def restrict_project_posting_node(func):

    def wrapper(self, info, node_id):
        result = func(self, info, node_id)

        if info.context.user is None or not info.context.user.is_authenticated:
            if isinstance(result, ProjectPosting):
                result = hide_project_posting_attributes(result)
            else:
                result = None

        return result

    return wrapper
