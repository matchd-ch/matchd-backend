from db.seed.base import BaseSeed
from db.models import Employee as EmployeeModel


# pylint: disable=W0612
class Employee(BaseSeed):

    def create_or_update(self, data, *args, **kwargs):
        if data is None:
            return
        employee, created = EmployeeModel.objects.get_or_create(user=kwargs.get('user'))
        employee.role = data.get('role')
        employee.save()

    def random(self, *args, **kwargs):
        pass
