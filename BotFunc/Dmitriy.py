from telebot import types

import BotFunc.Pavel
from BotFunc.Alexey import sort_by_team_type, show_command_list, show_my_team, \
    kick_from_team, info_list_teams, info_about_students, print_form, users_no_team, \
    kick_names, change_mentor, no_mentor_teams
from BotFunc.Sergey import check_changes, make_changes, change_registration
from BotFunc.models import User

btn_list = ['Железо', 'Веб', 'Бот', 'Игра', 'Другое']
btn_lead = ['🔎 Набрать команду',
            '⭐ Управление командой', '🖍 Изменить информацию']
btn_mentor = ['🔱 Присоединиться к команде', '✅ Сортировать по направлению команды',
              '👤 Посмотреть анкеты', '🔥 Подбор команды', '🖍 Изменить информацию']
btn_yes_no = ['Да', 'Нет']

# Создание клавиатуры с выбором функций


def pars_login(message):
    message_id = message.text[::-1]
    kick_user = ''
    for i in range(1, len(message_id)):
        kick_user += message_id[i]
        if message_id[i + 1] == '@':
            break
    return kick_user[::-1]


def apply_to_mentor(bot, id, text):
    from_user = User.objects.get(user_id=id)
    to_user = User.objects.get(team=text, role_command='TeamLead')

    markup = types.InlineKeyboardMarkup()
    data = 'да' + '@@@' + str(id) + '@@@' + text
    btn_my_site = types.InlineKeyboardButton(
        text='Добавить', callback_data=data)
    markup.add(btn_my_site)
    data = 'Нет' + '@@@' + str(id) + '@@@' + text
    btn_my_site = types.InlineKeyboardButton(
        text='Не добавлять', callback_data=data)
    markup.add(btn_my_site)
    data = '📮 В Вашу команду хочет добавиться @' + from_user.login + ' Добавить?'
    bot.send_message(to_user.user_id, data, reply_markup=markup)


def main_func(message, bot, user):
    markup = types.ReplyKeyboardMarkup()
    if message.text == '🔥 Подбор команды' and user.is_mentor == '1':
        show_command_list(message, bot)

    # Функция "Управления командой"
    elif message.text == '⭐ Управление командой':
        team_list = show_my_team(message, bot, user)
        # Если кнопку нажал Тимлид (функция кика)
        if user.role_command == 'TeamLead':
            names_list = kick_names(team_list)
            if len(team_list) > 1:
                BotFunc.Pavel.send_msg(
                    bot, message, '❌ Выберите участника, котрого Вы хотите исключить: ', 1, *names_list, '🔙 Назад')

    # Функция изменения информации о себе
    elif message.text == '🖍 Изменить информацию':
        check_changes(message, bot, user)
        make_changes(message, bot, user)
        change_registration(message, bot, user)

    # Сортировка по направлению команды (Mentor only)
    elif message.text == '✅ Сортировать по направлению команды' and user.is_mentor == '1':
        BotFunc.Pavel.send_msg(
            bot, message, '📝 Выберите направление, по которому Вы хотите сортировать', 3, *btn_list)

    # Вывод клавиш с направлением команд (Mentor only)
    elif message.text in btn_list:
        msg = sort_by_team_type(message)
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *btn_mentor)

    # Вывод клавиш с киком юзеров (TeamLead only)
    elif 'Исключить' in message.text and user.role_command == 'TeamLead':
        login = pars_login(message)
        kick_from_team(login, bot)
        BotFunc.Pavel.send_msg(bot, message, '@' + login +
                               ' был исключён из команды.', 1, *btn_lead)

    # Вывод команд, для дальнейшего просмотра анкет их участников (Mentor only)
    elif message.text == '👤 Посмотреть анкеты' and user.is_mentor == '1':
        teams = info_list_teams()
        msg = "📖 Выберите команду из списка: \n\n"
        for team in teams:
            msg += team + '\n'
        teams.append('🔙 Назад')
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *teams)

    # Выбор команды, анкеты чьих участников нужно посмтреть (Mentor only)
    elif '✅ Команда: ' in message.text and user.is_mentor == '1':
        students = info_about_students(message.text[11:])
        msg = "🎓 Выберите студента из списка: \n\n"
        for student in students:
            msg += student + '\n'
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *students)

    # Выбор анкеты, которую нужно посмтреть (Mentor only)
    elif '📋 Анкета:' in message.text and user.is_mentor == '1':
        login = pars_login(message)
        user_obj = User.objects.get(login=login)
        msg = print_form(user_obj)
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *btn_mentor)

    # Вывод сообщения о юезрах без команды (TeamLead only)
    elif '🔎 Набрать команду' == message.text and user.role_command == 'TeamLead':
        msg = users_no_team()
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *btn_lead)

    # Присоединиться к команде (Mentor only)
    elif '🔱 Присоединиться к команде' == message.text and user.is_mentor == '1':
        list_teams = no_mentor_teams()
        if len(list_teams) != 0:
            msg = '🔥 Список команд, у которых ещё нет ментора\n🧠 Выберите команду, в которой вы хотите стать ментором: \n\n'
        else:
            msg = '‼ На данный момент нет команд, у которых нет ментора'
        for i in range(len(list_teams)):
            msg += '💼 ' + list_teams[i] + '\n'
            list_teams[i] = '💼 Команда: ' + list_teams[i]
        list_teams.append('🔙 Назад')
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *list_teams)

    # Подтверждение того, что ментор хочет присоединиться к команде (Mentor only)
    elif '💼 Команда:' in message.text and user.is_mentor == '1':
        team_name = message.text[11:]
        msg = '❓ Вы действительно хотите стать ментором в команде «' + team_name + '»‎?\n\
‼ Команда для ментора выбирается один раз, без возможности отказа от команды.'
        user.who_mentor = team_name
        user.save()
        BotFunc.Pavel.send_msg(bot, message, msg, 2, *btn_yes_no)

    elif 'Да' == message.text and user.is_mentor == '1' and user.who_mentor != 'no_mentor':
        lead = User.objects.get(role_command='TeamLead', team=user.who_mentor)
        if lead.who_mentor == 'no_mentor':
            msg = '🎉 Поздравляем! Теперь вы курируете команду «' + user.who_mentor + '».'
            change_mentor(user.who_mentor, user.login, bot)
        else:
            msg = '⛔ Извините, но кто то успел взять команду «' + \
                user.who_mentor + '» на курирование раньше Вас.'
        user.who_mentor = 'no_mentor'
        user.save()
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *btn_mentor)

    elif 'Нет' == message.text and user.is_mentor == '1' and user.who_mentor != 'no_mentor':
        msg = '⛔ Вы не стали ментором в команде «' + user.who_mentor + '»'
        user.who_mentor = 'no_mentor'
        user.save()
        BotFunc.Pavel.send_msg(bot, message, msg, 1, *btn_mentor)

    # Создание кнопок после регистрации
    else:
        # Если пользователь студент
        if user.is_mentor == "0":
            itembt_edit = types.KeyboardButton(btn_lead[2])
            itembt_team = types.KeyboardButton(btn_lead[1])
            # Дополнительная кнопка поиска стдуентов (TeamLead only)
            if user.role_command == "TeamLead":
                itembt_find = types.KeyboardButton(btn_lead[0])
                markup.row(itembt_find)
        # Если пользователь ментор
        else:
            itembt_edit = types.KeyboardButton(btn_mentor[4])
            itembt_team = types.KeyboardButton(btn_mentor[3])
            itembt_sort_type = types.KeyboardButton(btn_mentor[1])
            itembt_info = types.KeyboardButton(btn_mentor[2])
            itembt_take_team = types.KeyboardButton(btn_mentor[0])
            markup.row(itembt_take_team)
            markup.row(itembt_sort_type)
            markup.row(itembt_info)
        markup.row(itembt_team)
        markup.row(itembt_edit)

        bot.send_message(
            message.chat.id, "⚙️ Выберите дальнейшее действие:", reply_markup=markup)
