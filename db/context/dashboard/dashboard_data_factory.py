from db.context.dashboard.company_dashboard_data import CompanyDashboardData
from db.context.dashboard.dashboard_data import DashboardData
from db.context.dashboard.empty_dashboard_data import EmptyDashboardData
from db.context.dashboard.student_dashboard_data import StudentDashboardData
from db.models.user import User
from db.models.profile_type import ProfileType


class DashboardDataFactory():

    @staticmethod
    def get_dashboard_data_for(user: User) -> DashboardData:
        dashboard_data = EmptyDashboardData(user)

        if user.type in ProfileType.valid_company_types():
            dashboard_data = CompanyDashboardData(user)

        if user.type in ProfileType.valid_student_types():
            dashboard_data = StudentDashboardData(user)

        return dashboard_data
