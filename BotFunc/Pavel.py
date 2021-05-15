from BotFunc.config import *
from telebot import types
from BotFunc.models import User
from BotFunc.Dmitriy import apply_to_mentor
from BotFunc.Alexey import common_show_command_list

hide_markup = types.ReplyKeyboardRemove(selective=False)
msg_team_err = '''⛔ Ошибка, введенное название команды не существует. Вы вернетесь к предыдущему пункту. \
В случае, если Вы хотите создать команду, выберите роль Тимлид. Если у Вас есть команда, выберите роль \
в ней еще раз и введите корректное название (Возможно Ваш Тимлид еще не создал команду**).'''


def list_teams_func():
    list_teams = list()
    all_users = User.objects.filter(role_command="TeamLead")
    for user in all_users:
        team_name = user.team
        list_teams.append(team_name)
    return list_teams


def alpha_in(str):
    for i in str:
        if i.isalpha():
            return 1
    return 0


def send_msg(bot, message, msg, width, *args):
    args = list(args)
    for i in range(len(args)):
        args[i] = types.KeyboardButton(args[i])
    buttons = [args[i: i + width] for i in range(0, len(args), width)]
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(buttons)):
        print(buttons[i])
        markup.add(*buttons[i])
    bot.send_message(message.chat.id, msg, reply_markup=markup)


def check_name(txt: str, maxim=20, flag=0):
    if flag and txt == '-':
        return 1
    if not txt[0].isupper() or txt[0] in ' -':
        return 0
    if not 1 <= len(txt) <= maxim:
        return 0
    for i in range(1, len(txt)):
        if not txt[i].isalpha() and txt[i] not in '- ':
            return 0

    check = 0
    indexes = (txt.find(' '), txt.find('-'))
    for i in range(2):
        if indexes[i] == -1:
            check += 2
        else:
            check += alpha_in(txt[:indexes[i]])
            check += alpha_in(txt[indexes[i] + 1:])

    return 0 if check != 4 else 1


def check_team(txt, maxim=100):
    if not txt[0].isupper():
        return 0
    if not len(txt) <= maxim or len(txt) <= 2:
        return 0
    for i in range(1, len(txt)):
        if not txt[i].isalpha() and txt[i] not in '- _1234567890':
            return 0
    return 1


def check_group(txt):
    if len(txt) != 7:
        return 0
    if txt[0:2].isupper() and txt[2].isdigit() and txt[3] == '-' and txt[4:6].isdigit()\
            and txt[4] > '0' and txt[5] > '0' and txt[6].isupper():
        return 1
    else:
        return 0


def check_role(role):
    if role in roles:
        return 1
    return 0


def name_input(message, bot, user):
    user.name = message.text
    if check_name(user.name, 40, 0):
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(
            message.chat.id, "🖍 Пожалуйста, введите Вашe имя (c большой буквы):", reply_markup=hide_markup)
        return 0


def surname_input(message, bot, user):
    user.surname = message.text
    if check_name(user.surname, 40, 0):
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(
            message.chat.id, "🖍 Пожалуйста, введите Вашу фамилию (с большой буквы):", reply_markup=hide_markup)
        return 0


def father_name_input(message, bot, user):
    user.father_name = message.text
    if check_name(user.father_name, 40, 0):
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(
            message.chat.id, "🖍 Пожалуйста, введите Ваше отчество (c большой буквы):", reply_markup=hide_markup)
        return 0


def group_input(message, bot, user):
    user.group = message.text.upper()
    if check_group(user.group):
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(message.chat.id, "🖍 Следите за форматом! Пожалуйста, введите Вашу группу \
(в формате \"ИУ7-23Б\"):", reply_markup=hide_markup)
        return 0


def role_command_input(message, bot, user):
    user.role_command = message.text
    if check_role(user.role_command):
        user.role_command = roles_en[roles.index(user.role_command)]
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(message.chat.id, "🖍 Пожалуйста, выберите Вашу роль в команде (в случае выбора Тимлида \
будет создана новая команда во главе с вами. Если ваш тимлид еще не зарегистрировался, то сделайте это ПОСЛЕ \
него):")
        return 0


def team_input(message, bot, user):
    if check_team(message.text):
        if user.role_command == 'TeamLead':
            if not User.objects.filter(team=message.text):
                user.team = message.text
                user.expected_input = ''
                user.save()
                return 1
            else:
                bot.send_message(
                    message.chat.id, "⛔ Данное название занято. \n🖍 Пожалуйста, введите другое название команды:", reply_markup=hide_markup)
                return 0
        if message.text == 'Без команды':
            user.team = 'no_team'
            user.expected_input = ''
            user.save()
            return 1
        if User.objects.filter(team=message.text):
            user.team = message.text + '(unreg)'
            apply_to_mentor(bot, message.chat.id, message.text)
            user.expected_input = ''
            user.save()
            bot.send_message(
                message.chat.id, "🔜 Запрос отправлен", reply_markup=hide_markup)
            return 1
        else:
            return -1
    else:
        if user.role_command != 'TeamLead':
            common_show_command_list(message, bot)
            send_msg(bot, message, "🖍 Пожалуйста, введите название команды, в которую Вы хотите подать заявку. \n "
                     "Вам придет сообщение, как только тимлид примет Вас.", 1, 'Без команды', *list_teams_func())
        else:
            bot.send_message(message.chat.id, "📛 Название некорректное, пожалуйста, введите корректное название команды "
                             "(с большой буквы; разрешается использовать буквы, цифры, пробелы и символы '-', '_'; режим создания):", reply_markup=hide_markup)
        return 0


def team_type_input(message, bot, user):
    user.team_type = message.text
    if user.team_type in team_types:
        user.expected_input = ''
        user.save()
        return 1
    else:
        bot.send_message(
            message.chat.id, "🖍 Пожалуйста, введите направление команды:")
        return 0


def python_level_input(message, bot, user):
    user.python_level = message.text
    if user.python_level in marks:
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите уровень знания Python "
                             "(от 1 до 5, где 1 - новичок, 5 - эксперт):")
        else:
            bot.send_message(message.chat.id, "🖍 Пожалуйста, оцените Вашу заинтересованность в Python "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум):")
        return 0


def c_level_input(message, bot, user):
    user.c_level = message.text
    if user.c_level in marks:
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите уровень знания С/C++ "
                             "(от 1 до 5, где 1 - новичок, 5 - эксперт):")
        else:
            bot.send_message(message.chat.id, "🖍 Пожалуйста, оцените Вашу заинтересованность в C/C++ "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум): ")
        return 0


def c_sharp_level_input(message, bot, user):
    user.c_sharp_level = message.text
    if user.c_sharp_level in marks:
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите уровень знания С# "
                             "(от 1 до 5, где 1 - новичок, 5 - эксперт):")
        else:
            bot.send_message(message.chat.id, "🖍 Пожалуйста, оцените Вашу заинтересованность в C# "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум):")
        return 0


def java_level_input(message, bot, user):
    user.java_level = message.text
    if user.java_level in marks:
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите уровень знания Java "
                             " (от 1 до 5, где 1 - новичок, 5 - эксперт):")
        else:
            bot.send_message(message.chat.id, "🖍 Пожалуйста, оцените Вашу заинтересованность в Java "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум):")
        return 0


def js_level_input(message, bot, user):
    user.js_level = message.text
    if user.js_level in marks:
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите уровень знания JavaScript "
                             "(от 1 до 5, где 1 - новичок, 5 - эксперт):")
        else:
            bot.send_message(message.chat.id, "🖍 Пожалуйста, оцените Вашу заинтересованность в JavaScript "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум):")
        return 0


def user_tech_input(message, user):
    user.user_tech = message.text
    user.expected_input = ''
    user.save()
    return 1


def user_exp_input(message, user):
    user.user_exp = message.text
    user.expected_input = ''
    user.save()
    return 1


def team_idea_input(message, bot, user, min_msg_size=40):
    if len(message.text) >= min_msg_size:
        user.team_idea = message.text
        user.expected_input = ''
        user.save()
        return 1
    else:
        if user.is_mentor == '0':
            bot.send_message(message.chat.id, f"🖍 Пожалуйста, поделитесь идеей Вашего проекта \
(информация для менторов и преподавателей, кратко расскажите про ваш проект; \
также можете рассказать про ваши ожидания от практики (может быть какие-нибудь пожелания?); от 40 символов):",
                             reply_markup=hide_markup)
        else:
            bot.send_message(message.chat.id, f"🖍 Пожалуйста, поделитесь вашими ожиданиями и пожеланиями по \
поводу проведения летней практики (от {min_msg_size} символов):")
        return 0


def registration(message, bot, user):

    if user.expected_input == "surname":
        if surname_input(message, bot, user):
            user.expected_input = 'name'
            user.save()
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше имя (с большой буквы):",
                             reply_markup=hide_markup)

    elif user.expected_input == "name":
        if name_input(message, bot, user):
            user.expected_input = 'father_name'
            user.save()
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше отчество (с большой буквы):",
                             reply_markup=hide_markup)

    elif user.expected_input == "father_name":
        if father_name_input(message, bot, user):
            if user.is_mentor == '0':
                user.expected_input = 'group'
                user.save()
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Вашу группу (в формате \"ИУ7-23Б\"):",
                                 reply_markup=hide_markup)
            else:
                user.expected_input = 'python_level'
                user.save()
                send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в Python:"
                         "(от 1 до 5, где 1 - минимум, 5 - максимум):", 5, '1', '2', '3', '4', '5')

    elif user.expected_input == "group":
        if group_input(message, bot, user):
            user.expected_input = 'role_command'
            user.save()
            send_msg(bot, message, "🖍 Пожалуйста, выберите Вашу роль в команде (в случае выбора Тимлида \
будет создана новая команда во главе с вами. Если ваш тимлид еще не зарегистрировался, то сделайте это ПОСЛЕ \
него):", 2, 'Тимлид', 'Разработчик', 'Тестировщик', 'Дизайнер', 'Другое')

    elif user.expected_input == "role_command":
        if role_command_input(message, bot, user):
            user.expected_input = 'team'
            user.save()
            if user.role_command != 'TeamLead':
                common_show_command_list(message, bot)
                send_msg(bot, message, "🖍 Пожалуйста, введите название Вашей команды (с большой буквы; *Вам придет "
                                       "сообщение, как только тимлид примет вас*):", 1, 'Без команды', *list_teams_func())
            else:
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите название Вашей команды (режим создания, \
ввод с большой буквы):", reply_markup=hide_markup)

    elif user.expected_input == "team":
        check = team_input(message, bot, user)
        if check == 1:
            if user.role_command == 'TeamLead':
                user.expected_input = 'team_type'
                user.save()
                send_msg(bot, message, "🖍 Пожалуйста, введите направление команды:", 2, 'Железо', 'Веб', 'Бот', 'Игра',
                         'Другое')
            else:
                user.expected_input = 'python_level'
                user.save()
                if user.is_mentor == '0':
                    send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания Python "
                             "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
                else:
                    send_msg(bot, message, "🖍 Пожалуйста, оцените уровень заинтересованности Python "
                             "(от 1 до 5, где 1 - минимум, 5 - максимум):", 5, '1', '2', '3', '4', '5')
        elif check == -1:
            user.expected_input = 'role_command'
            user.save()
            send_msg(bot, message, msg_team_err + "\n\n🖍 Пожалуйста, введите Вашу роль в команде:", 2, 'Тимлид',
                     'Разработчик', 'Тестировщик', 'Дизайнер', 'Другое')

    elif user.expected_input == "team_type":
        if team_type_input(message, bot, user):
            user.expected_input = 'python_level'
            user.save()
            if user.is_mentor == '0':
                send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания Python "
                         "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
            else:
                send_msg(bot, message, "🖍 Пожалуйста, оцените уровень заинтересованности Python "
                         "(от 1 до 5, где 1 - минимум, 5 - максимум): ", 5, '1', '2', '3', '4', '5')

    elif user.expected_input == "python_level":
        if python_level_input(message, bot, user):
            if user.is_mentor == '0':
                send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания C/C++ "
                         "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
            else:
                send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в C/C++ "
                         "(от 1 до 5, где 1 - минимум, 5 - максимум): ", 5, '1', '2', '3', '4', '5')
            user.expected_input = 'c_level'
            user.save()

    elif user.expected_input == "c_level":
        if c_level_input(message, bot, user):
            if user.is_mentor == '0':
                send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания C# "
                         "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
            else:
                send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в C# "
                         "(от 1 до 5, где 1 - минимум, 5 - максимум): ", 5, '1', '2', '3', '4', '5')
            user.expected_input = 'c_sharp_level'
            user.save()

    elif user.expected_input == "c_sharp_level":
        if c_sharp_level_input(message, bot, user):
            if user.is_mentor == '0':
                send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания Java "
                         "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
            else:
                send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в Java "
                         "(от 1 до 5, где 1 - минимум, 5 - максимум): ", 5, '1', '2', '3', '4', '5')
            user.expected_input = 'java_level'
            user.save()

    elif user.expected_input == "java_level":
        if java_level_input(message, bot, user):
            if user.is_mentor == '0':
                send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания JavaScript "
                         "(от 1 до 5, где 1 - новичок, 5 - эксперт):", 5, '1', '2', '3', '4', '5')
            else:
                send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в JavaScript "
                         "(от 1 до 5, где 1 - минимум, 5 - максимум): ", 5, '1', '2', '3', '4', '5')
            user.expected_input = 'js_level'
            user.save()

    elif user.expected_input == "js_level":
        if js_level_input(message, bot, user):
            if user.is_mentor == '0':
                user.expected_input = 'user_tech'
                user.save()
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите технологии, которыми планируете \
пользоваться для создания проекта (Под технологиями подразумеваются \
инструменты разработки: различные фреймворки, платформы и прочее):", reply_markup=hide_markup)
            else:
                user.expected_input = 'team_idea'
                user.save()
                bot.send_message(message.chat.id, f"🖍 Пожалуйста, расскажите про Ваши ожидания от летней практики \
и пожелание к ее проведению (от 40 символов):", reply_markup=hide_markup)

    elif user.expected_input == "user_tech":
        if user_tech_input(message, user):
            user.expected_input = 'user_exp'
            user.save()
            bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваш опыт (Пример приложения, которое вы когда-то \
разработали и т.п.):", reply_markup=hide_markup)

    elif user.expected_input == "user_exp":
        if user_exp_input(message, user):
            user.expected_input = 'team_idea'
            user.save()
            bot.send_message(message.chat.id, f"🖍 Пожалуйста, поделитесь идеей Вашего проекта \
(информация для менторов и преподавателей, кратко расскажите про ваш проект; \
также можете рассказать про ваши ожидания от практики (может быть какие-нибудь пожелания?); от 40 символов):",
                             reply_markup=hide_markup)

    elif user.expected_input == "team_idea":
        if team_idea_input(message, bot, user):
            user.expected_input = 'registration completed'
            user.save()
            send_msg(bot, message, "🍻 Поздравляем, Ваши данные обработаны. \nНажмите, чтобы посмотреть список данных:",
                     1, '📝 Посмотреть список')
