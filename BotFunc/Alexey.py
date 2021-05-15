from BotFunc.models import User
import random

# Подсчёт совместимости < Ментор === Команда >


def diff_team_mentor(list_team, mentor_obj):
    list_lang_lvl = [0] * 5
    i = 0
    total_sum = 0
    total_mentor = 0

    # Подсчёт силы каждого ЯП для команды
    try:
        for members in list_team:
            list_lang_lvl[i] += int(members.python_level)
            total_sum += list_lang_lvl[i]
            i += 1
            list_lang_lvl[i] += int(members.c_level)
            total_sum += list_lang_lvl[i]
            i += 1
            list_lang_lvl[i] += int(members.c_sharp_level)
            total_sum += list_lang_lvl[i]
            i += 1
            list_lang_lvl[i] += int(members.java_level)
            total_sum += list_lang_lvl[i]
            i += 1
            list_lang_lvl[i] += int(members.js_level)
            total_sum += list_lang_lvl[i]
            i = 0
        for i in range(len(list_lang_lvl)):
            list_lang_lvl[i] /= total_sum
    except:
        return 'ERROR'

    # Подсчёт силы кадого ЯП для ментора
    pyth_mentor = float(mentor_obj.python_level)
    total_mentor += pyth_mentor
    c_mentor = float(mentor_obj.c_level)
    total_mentor += c_mentor
    sharp_mentor = float(mentor_obj.c_sharp_level)
    total_mentor += sharp_mentor
    java_mentor = float(mentor_obj.java_level)
    total_mentor += java_mentor
    js_mentor = float(mentor_obj.js_level)
    total_mentor += js_mentor

    # Подсчёт того самого числа
    difference = (abs((pyth_mentor / total_mentor) - list_lang_lvl[0]) + 1) * \
        (abs((c_mentor / total_mentor) - list_lang_lvl[1]) + 1) * \
        (abs((sharp_mentor / total_mentor) - list_lang_lvl[2]) + 1) * \
        (abs((java_mentor / total_mentor) - list_lang_lvl[3]) + 1) * \
        (abs((js_mentor / total_mentor) - list_lang_lvl[4]) + 1)
    # Рандом нужен чтобы не получилось одинаковых ключей
    difference += random.uniform(0.00001, 0.0001)

    return difference


# Функция выводящая список зарегистрированных команд (для менторов) + подбор команды по рейтингу
def show_command_list(message, bot):
    list_teamleads = User.objects.filter(role_command='TeamLead')
    mentor = User.objects.get(user_id=message.chat.id)
    dict_teams = {}  # Список команд в формате {Разница ЯП с ментором : Название команды}
    no_value_numb = 100
    message_to_send = '🔥 Список зарегистрированных команд\n' \
        '⚠ Чем выше команда в данном списке - тем больше она Вам подходит\n\n'

    for leads in list_teamleads:
        team_name = leads.team
        if team_name == 'no_value' or team_name == 'no_team':
            continue
        list_team = User.objects.filter(team=leads.team)
        key = diff_team_mentor(list_team, mentor)
        if key != 'ERROR':
            dict_teams[key] = team_name
        else:
            dict_teams[no_value_numb] = team_name
            no_value_numb += 1

    # Привожу все ключи совместимости в список, чтобы его отсортировать
    list_teams = list(dict_teams.keys())
    list_teams.sort()

    # Вызов по отсортированым ключам совместимости список команд
    for i in range(len(list_teams)):
        # Список участников текущей команды
        list_members = User.objects.filter(team=dict_teams[list_teams[i]])
        for member in list_members:
            if member.role_command == 'TeamLead':
                teamlead = member.login
                teamtype = member.team_type
                if teamtype == 'no_value':
                    teamtype = '❓ пока не определились'
        message_to_send += '✅ Команда «‎' + dict_teams[list_teams[i]] + '»‎. ⭐ TeamLead: @' +\
            teamlead + '. Направление: ' + teamtype + '.\n'
    if len(list_teams) != 0:
        message_to_send += '\n❗ Обратите внимание: данный список сформирован ТОЛЬКО на основе данных, введенных ' \
            'Вами и участниками каждой из команд.'
        bot.send_message(message.chat.id, message_to_send)
    else:
        bot.send_message(
            message.chat.id, '‼ На данный момент нет зарегистрированных команд.')


# Список команд для обычных пользователей (студентов)
# ДА, я знаю что она частично дублирует вышестоящую функцию
def common_show_command_list(message, bot):
    list_leads = User.objects.filter(role_command='TeamLead')
    message_to_send = '🔥 Список зарегистрированных команд: \n\n'
    count_teams = 0

    for leads in list_leads:
        team = leads.team
        if team == 'no_value' or team == 'no_team':
            continue
        message_to_send += '✅ Команда «‎' + team + '»‎. ⭐ TeamLead: @' +\
            leads.login + '.\n'
        count_teams += 1

    if count_teams:
        bot.send_message(message.chat.id, message_to_send)
    else:
        bot.send_message(
            message.chat.id, '‼ На данный момент нет зарегистрированных команд')


# Функция выводящая участников команды (для студента)
def show_my_team(message, bot, user_obj):
    # Если пользователь ещё не состоит в команде
    team = user_obj.team
    if team == 'no_team' or '(unreg)' in team:
        bot.send_message(
            message.chat.id, '‼ На данный момент вы не состоите в команде.')
        return

    list_teammates = User.objects.filter(team=team)
    message_to_send = '💥 Список участников вашей команды ' + '«' + team + '» \n\n'
    if user_obj.who_mentor != 'no_mentor':
        mentor = User.objects.get(login=user_obj.who_mentor)
        message_to_send += '🎓 Ментор: ' + mentor.name + \
            ' ' + mentor.surname + '. @' + mentor.login + '\n'
    else:
        message_to_send += '🎓 Без ментора\n'
    teamlead = User.objects.get(team=team, role_command='TeamLead')
    message_to_send += '⭐ ' + teamlead.name + ' ' + \
        teamlead.surname + '. Роль в команде: TeamLead.\n'
    for users in list_teammates:
        role = users.role_command
        if role != 'TeamLead':
            message_to_send += '✅ '
            message_to_send += users.name + ' ' + \
                users.surname + '. Роль в команде: ' + role + '.\n'
    bot.send_message(message.chat.id, message_to_send)

    return list_teammates


# Вывод команд по заданому направлению (для ментора)
def sort_by_team_type(message):
    type_sort = message.text
    message_to_send = '🔥 Список команд с направлением ' + type_sort + ': \n\n'
    sorted_teams = User.objects.filter(
        team_type=type_sort, role_command='TeamLead')
    for leads in sorted_teams:
        message_to_send += '✅ Команда «‎' + leads.team + '»‎. ⭐ TeamLead: @' +\
            leads.login + '.\n'
    if sorted_teams:
        return message_to_send
    else:
        return '‼ На данный момент нет зарегистрированных команд с направлением ' + type_sort


# Функция кика пользователя из команды (для тимлида)
def kick_from_team(login, bot):
    loser = User.objects.get(login=login)
    kicked_team = loser.team
    loser.team = 'no_team'
    loser.team_type = 'no_value'
    loser.who_mentor = 'no_mentor'
    loser.save()
    bot.send_message(
        loser.user_id, '🚮 Поздравляем, Вы были кикнуты из команды ' + kicked_team + '! 🚮')


# Обновление названия команды, если тимлид поменял название
def update_team_name(user, old_name):
    team_list = User.objects.filter(team=old_name)
    for users in team_list:
        users.team = user.team
        users.save()


# Обновление направления команды, если тимлид поменял направление
def update_team_type(new_type, team_name):
    team_list = User.objects.filter(team=team_name)
    for users in team_list:
        users.team_type = new_type
        users.save()


# Формируется полный список команд (для кнопок, когда ментор жмёт "Посмотреть анкеты")
def info_list_teams():
    list_teams = list()
    all_users = User.objects.filter(role_command='TeamLead')
    for user in all_users:
        team_name = "✅ Команда: " + user.team
        list_teams.append(team_name)

    return list_teams


# Парсинг списка команды (из сообщения)
def info_about_students(team_name):
    users_list = list()
    team = User.objects.filter(team=team_name)
    for user in team:
        user = '📋 Анкета: ' + user.name + ' ' + \
            user.surname + ' (@' + user.login + ')'
        users_list.append(user)

    return users_list


# Формирования анкеты студента
def print_form(user):
    name_field_list = [
        "✏ Имя: ", "✏ Фамилия: ", "✏ Отчество: ", "💼 Учебная группа: ",
        "👫 Роль в команде: ", "👫 Название команды: ", "👫 Профиль команды: ",
        "💻 Уровень знания Python: ", "💻 Уровень знания C/C++: ",
        "💻 Уровень знания C#: ", "💻 Уровень знания Java: ",
        "💻 Уровень знания JavaScript: ", "💻 Знание технологий: ",
        "💻 Опыт в программировании: ", "💡 Идея проекта: "
    ]

    field_list = [
        user.name, user.surname, user.father_name,
        user.group, user.role_command, user.team,
        user.team_type, user.python_level, user.c_level,
        user.c_sharp_level, user.java_level, user.js_level,
        user.user_tech, user.user_exp, user.team_idea
    ]

    message_to_send = "⭐ Анкета " + user.name + " " + user.surname + " ⭐\n"

    for i in range(len(field_list)):
        if field_list[i] == "no_team" or field_list[i] == "no_value":
            message_to_send += name_field_list[i] + "Без команды" + "\n"
        else:
            message_to_send += name_field_list[i] + field_list[i] + "\n"

    return message_to_send


# Формирования списка юзеров без команды
def users_no_team():
    users = User.objects.filter(team="no_team", is_mentor="0")
    if len(users) != 0:
        msg = "🛀 Пользователи без команды: \n\n"
    else:
        msg = '❗ На данный момент нет пользователей, у которых нет команды.'
    for user in users:
        msg += user.name + ' ' + user.surname + '. Роль в команде: ' + \
            user.role_command + '. @' + user.login + '\n'

    return msg

# Формирование списка людей из команды, которых можно кикнуть


def kick_names(team_list):
    names_list = list()
    for users in team_list:
        if users.role_command != 'TeamLead':
            name_kick = '🔴 Исключить ' + users.name + ' (@' + users.login + ')'
            names_list.append(name_kick)

    return names_list


# Изменени поля who_mentor, если ментор взял себе команду
def change_mentor(team_name, login, bot):
    team = User.objects.filter(team=team_name)
    for user in team:
        if user.role_command == 'TeamLead':
            bot.send_message(
                user.user_id, '🎉 Поздравляем! У Вашей команды появился ментор: @' + login)
        user.who_mentor = login
        user.save()


# Возвращает список команд, у которых не метора
def no_mentor_teams():
    list_teams = list()
    teams = User.objects.filter(
        role_command='TeamLead', who_mentor='no_mentor')
    for leads in teams:
        list_teams.append(leads.team)

    return list_teams
