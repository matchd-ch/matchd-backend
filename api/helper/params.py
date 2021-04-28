def retrieve_param_from_info(info, name, index):
    # try to retrieve job posting id parameter from operation
    #
    # query example:
    # query
    # {
    #     student(slug: "{student-slug}", jobPostingId: {id}) {
    #     .....
    #     }
    # }
    try:
        value = info.operation.selection_set.selections[0].arguments[index].value.value
    except Exception:
        value = None

    # fallback if request was sent with variables
    #
    # query example:
    # query($slug: String!, $jobPostingId: ID!) {
    #     student(slug: $slug, jobPostingId: $jobPostingId) {
    #     ....
    #     }
    # }
    # with variables
    # {
    #     "slug": "{student-slug}",
    #     "jobPostingId": {id}
    # }
    if value is None:
        try:
            value = info.variable_values.get(name)
        except Exception:
            value = None
    return value
