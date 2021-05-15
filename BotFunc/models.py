from django.db import models


def_value = 'no_value'


class User(models.Model):

    # Ожидаемые команды ввода
    expected_input = models.CharField(max_length=40, default='surname')
    expected_command = models.CharField(max_length=40, default='')
    is_correct = models.CharField(max_length=1, default='0')

    # Данные о пользователе
    is_mentor = models.CharField(max_length=1, default='0')
    user_id = models.CharField(max_length=32, default=def_value)
    login = models.CharField(max_length=100, default=def_value)
    group = models.CharField(max_length=20, default=def_value)
    name = models.CharField(max_length=100, default=def_value)
    surname = models.CharField(max_length=100, default=def_value)
    father_name = models.CharField(max_length=100, default=def_value)

    # Доп. данные о пользователе
    role_command = models.CharField(max_length=100, default=def_value)
    team = models.CharField(max_length=100, default=def_value)
    team_type = models.CharField(max_length=100, default=def_value)
    user_tech = models.CharField(max_length=1000, default=def_value)
    user_exp = models.CharField(max_length=1000, default=def_value)
    team_idea = models.CharField(max_length=1000, default=def_value)
    who_mentor = models.CharField(max_length=102, default="no_mentor")

    # Уровень ЯП
    python_level = models.CharField(max_length=1, default=def_value)
    c_level = models.CharField(max_length=1, default=def_value)
    c_sharp_level = models.CharField(max_length=1, default=def_value)
    java_level = models.CharField(max_length=1, default=def_value)
    js_level = models.CharField(max_length=1, default=def_value)

    # Удобный вывод Фамилия + Имя в админке БД
    def __str__(self):
        full_name = self.name + ' ' + self.surname
        return full_name
