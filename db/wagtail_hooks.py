from wagtail.core import hooks


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    hidden_items = ['explorer', 'images', 'documents', 'reports']
    menu_items[:] = [item for item in menu_items if item.name not in hidden_items]


@hooks.register('construct_settings_menu')
def hide_user_menu_item(request, menu_items):
    hidden_items = ['redirects', 'sites', 'collections', 'workflows', 'workflow-tasks']
    menu_items[:] = [item for item in menu_items if item.name not in hidden_items]
