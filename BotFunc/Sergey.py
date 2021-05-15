from telebot import types
import BotFunc.Pavel
import BotFunc.Alexey


def check_registration(message, bot, user):
    """
    Вывод анкеты пользователя.

    Функция выводит анкету пользователя после регистрации или
    изменения какого-либо поля анкеты.

    """

    if message.text == "📝 Посмотреть список" and (user.expected_input == "registration applied" or
                                                  user.expected_input == "registration completed"):
        name_field_list = list()
        field_list = list()

        # Поля анкеты в случае если пользователь - ментор
        if user.is_mentor == "1":
            name_field_list = [
                "✏ Имя: ", "✏ Фамилия: ", "✏ Отчество: ",
                "💻 Уровень заинтересованности в Python: ",
                "💻 Уровень заинтересованности в C/C++: ",
                "💻 Уровень заинтересованности в C#: ",
                "💻 Уровень заинтересованности в Java: ",
                "💻 Уровень заинтересованности в JavaScript: ",
                "💡 Пожелания и ожидания от практики: "
            ]

            field_list = [
                user.name, user.surname, user.father_name,
                user.python_level, user.c_level,
                user.c_sharp_level, user.java_level, user.js_level,
                user.team_idea
            ]

        # Поля анкеты в случае если пользователь - студент
        if user.is_mentor == "0":
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

        message_to_send = "⭐ Ваша анкета ⭐\n"

        for i in range(len(field_list)):
            if field_list[i] == "no_team" or field_list[i] == "no_value":
                message_to_send += name_field_list[i] + "Без команды" + "\n"
            else:
                message_to_send += name_field_list[i] + field_list[i] + "\n"

        BotFunc.Pavel.send_msg(
            bot, message, message_to_send, 2, "🆗 Верно", "🔄 Изменить")


def check_changes(message, bot, user):
    """
    Проверка необходимости изменения анкеты.

    Функция проверяет корректность анкеты и "отправляет"
    на её изменение, в случае если оно требуется.

    """

    if message.text == "🔄 Изменить" or message.text == "🖍 Изменить информацию":
        user.expected_input = "changes_needed"
        user.save()

        if user.is_mentor == "0":
            # Набор полей, которые можно изменить, если пользователь - студент
            if user.team == "no_team":
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде", "Найти команду",
                    "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            elif user.role_command != "TeamLead":
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде",
                    "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            else:
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Название команды",
                    "Профиль команды", "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            BotFunc.Pavel.send_msg(bot, message, "🔧 Пожалуйста, выберите поле анкеты, которое хотите изменить:", 1,
                                   *user_btn_list)
        else:
            # Набор полей, которые можно изменить, если пользователь - ментор
            mentor_btn_list = [
                "Фамилия", "Имя", "Отчество",
                "Уровень заинтересованности в Python",
                "Уровень заинтересованности в C/C++",
                "Уровень заинтересованности в C#",
                "Уровень заинтересованности в Java",
                "Уровень заинтересованности в JavaScript",
                "Пожелания и ожидания от практики", "✅ Верно"
            ]

            BotFunc.Pavel.send_msg(bot, message, "🔧 Пожалуйста, выберите поле анкеты, которое хотите изменить:", 1,
                                   *mentor_btn_list)

    elif message.text == "🆗 Верно":
        # Изменения не требуются
        user.expected_input = ""
        user.is_correct = "1"
        user.save()


def change_registration(message, bot, user):
    """
    Функция информирования о необходимости изменения конкретного поля.

    Данная функция позволяет изменить отдельное поле анкеты пользователя.

    """

    hide_markup = types.ReplyKeyboardRemove(selective=False)

    if user.expected_input == "changes_needed":
        user.is_correct = "0"

        skills_btn_list = [
            "1", "2", "3", "4", "5"
        ]

        if user.is_mentor == "0":
            # Набор полей, которые можно изменить, если пользователь - студент
            if user.team == "no_team":
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде", "Найти команду",
                    "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            elif user.role_command != "TeamLead":
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде",
                    "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            else:
                user_btn_list = [
                    "Фамилия", "Имя", "Отчество", "Учебная группа", "Название команды",
                    "Профиль команды", "Уровень знания Python", "Уровень знания C/C++",
                    "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                    "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
                ]

            roles_btn_list = [
                "Разработчик", "Тестировщик", "Дизайнер", "Другое"
            ]

            profile_btn_list = [
                "Железо", "Веб", "Бот", "Игра", "Другое"
            ]

            if message.text == "Фамилия":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Вашу фамилию (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Фамилия"
                user.save()

            elif message.text == "Имя":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше имя (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Имя"
                user.save()

            elif message.text == "Отчество":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше отчество (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Отчество"
                user.save()

            elif message.text == "Учебная группа":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Вашу группу (в формате \"ИУ7-23Б\"):",
                                 reply_markup=hide_markup)
                user.expected_input = "Учебная группа"
                user.save()

            elif message.text == "Роль в команде":
                if message.text not in user_btn_list:
                    bot.send_message(
                        message.chat.id, "🔧 Пожалуйста, выберите поле только из предложенных вариантов:")

                else:
                    BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, выберите Вашу роль в команде ",
                                           1, *roles_btn_list)
                    user.expected_input = "Роль в команде"
                    user.save()

            elif message.text == "Название команды" or message.text == "Найти команду":
                if message.text not in user_btn_list:
                    bot.send_message(
                        message.chat.id, "🔧 Пожалуйста, выберите поле только из предложенных вариантов:")

                else:
                    if user.team.endswith("(unreg)"):
                        BotFunc.Pavel.send_msg(bot, message, "🆘 Вы уже подали запрос в какую-либо команду. Дождитесь ответа "
                                                             "ТимЛида!\n"
                                                             "🔧 Пожалуйста, выберите поле анкеты, "
                                                             "которое хотите изменить:",
                                               1, *user_btn_list)
                        user.expected_input = "changes_needed"
                        user.save()

                    elif user.team != "no_team" and user.role_command == "TeamLead":
                        bot.send_message(message.chat.id, "🖍 Пожалуйста, введите новое название Вашей команды "
                                                          "(с большой буквы):", reply_markup=hide_markup)
                        user.expected_input = "Название команды"
                        user.save()

                    elif user.team == "no_team" and user.role_command != "TeamLead":
                        BotFunc.Alexey.common_show_command_list(message, bot)
                        BotFunc.Pavel.send_msg(bot, message,
                                               "🖍 Пожалуйста, введите название команды, в которую Вы хотите подать заявку. \n "
                                               "Вам придет сообщение, как только тимлид примет Вас.", 1, 'Без команды',
                                               *BotFunc.Pavel.list_teams_func())
                        user.expected_input = "Название команды"
                        user.save()

            elif message.text == "Профиль команды":
                if message.text not in user_btn_list:
                    bot.send_message(
                        message.chat.id, "🔧 Пожалуйста, выберите поле только из предложенных вариантов:")

                else:
                    BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите направление команды:",
                                           3, *profile_btn_list)
                    user.expected_input = "Профиль команды"
                    user.save()

            elif message.text == "Уровень знания Python":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания Python (от 1 до 5, где 1 - новичок, 5 - эксперт):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень знания Python"
                user.save()

            elif message.text == "Уровень знания C/C++":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания C/C++ (от 1 до 5, где 1 - новичок, 5 - эксперт):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень знания C/C++"
                user.save()

            elif message.text == "Уровень знания C#":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания C# (от 1 до 5, где 1 - новичок, 5 - эксперт):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень знания C#"
                user.save()

            elif message.text == "Уровень знания Java":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания Java (от 1 до 5, где 1 - новичок, 5 - эксперт):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень знания Java"
                user.save()

            elif message.text == "Уровень знания JavaScript":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, введите уровень знания JavaScript (от 1 до 5, где 1 - новичок, 5 - эксперт):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень знания JavaScript"
                user.save()

            elif message.text == "Знание технологий":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите технологии, которыми планируете пользоваться "
                                                  "для создания проекта (Под технологиями подразумеваются инструменты "
                                                  "раработки: различные фреймворки, платформы и прочее):",
                                 reply_markup=hide_markup)
                user.expected_input = "Знание технологий"
                user.save()

            elif message.text == "Опыт в программировании":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваш опыт (Пример приложения, "
                                                  "которое вы когда-то разработали и т.п.):",
                                 reply_markup=hide_markup)
                user.expected_input = "Опыт в программировании"
                user.save()

            elif message.text == "Идея проекта":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, опишите идею Вашего проекта и  поделитесь вашими "
                                                  "ожиданиями и пожеланиями по поводу проведения летней практики "
                                                  "(от 40 символов):",
                                 reply_markup=hide_markup)
                user.expected_input = "Идея проекта"
                user.save()

            elif message.text == "✅ Верно":
                BotFunc.Pavel.send_msg(bot, message, "🍻 Поздравляем, ваши данные обработаны. \n"
                                                     "Нажмите, чтобы посмотреть список данных:",
                                       1, '📝 Посмотреть список')
                user.expected_input = "registration applied"
                user.is_correct = "1"
                user.save()

        else:
            # Набор полей, которые можно изменить, если пользователь - ментор
            if message.text == "Фамилия":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Вашу фамилию (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Фамилия"
                user.save()

            elif message.text == "Имя":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше имя (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Имя"
                user.save()

            elif message.text == "Отчество":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, введите Ваше отчество (с большой буквы):",
                                 reply_markup=hide_markup)
                user.expected_input = "Отчество"
                user.save()

            elif message.text == "Уровень заинтересованности в Python":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в Python (от 1 до 5, где 1 - минимум, 5 - максимум):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень заинтересованности в Python"
                user.save()

            elif message.text == "Уровень заинтересованности в C/C++":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в C/C++ (от 1 до 5, где 1 - минимум, 5 - максимум):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень заинтересованности в C/C++"
                user.save()

            elif message.text == "Уровень заинтересованности в C#":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в C# (от 1 до 5, где 1 - минимум, 5 - максимум):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень заинтересованности в C#"
                user.save()

            elif message.text == "Уровень заинтересованности в Java":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в Java (от 1 до 5, где 1 - минимум, 5 - максимум):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень заинтересованности в Java"
                user.save()

            elif message.text == "Уровень заинтересованности в JavaScript":
                BotFunc.Pavel.send_msg(bot, message, "🖍 Пожалуйста, оцените заинтересованность в JavaScript (от 1 до 5, где 1 - минимум, 5 - максимум):",
                                       5, *skills_btn_list)
                user.expected_input = "Уровень заинтересованности в JavaScript"
                user.save()

            elif message.text == "Пожелания и ожидания от практики":
                bot.send_message(message.chat.id, "🖍 Пожалуйста, поделитесь вашими ожиданиями и пожеланиями по поводу "
                                                  "проведения летней практики (от 40 символов):",
                                 reply_markup=hide_markup)
                user.expected_input = "Пожелания и ожидания от практики"
                user.save()

            elif message.text == "✅ Верно":
                BotFunc.Pavel.send_msg(bot, message,
                                       "🍻 Поздравляем, ваши данные обработаны. \nНажмите, чтобы посмотреть "
                                       "список данных:", 1, '📝 Посмотреть список')
                user.expected_input = "registration applied"
                user.is_correct = "1"
                user.save()


def make_changes(message, bot, user):
    """
    Функция изменения известного поля анкеты.

    Данная функция позволяет по ключу изменить определенное поле анкеты.

    """

    rwr_info_msg = "♻️ Данные успешно перезаписаны\n🔧 Пожалуйста, выберите поле анкеты, которое хотите изменить:"

    change_team_msg = "🔧 Пожалуйста, выберите поле анкеты, которое хотите изменить:"

    if user.is_mentor == "0":
        # Набор полей, которые можно изменить, если пользователь - студент
        if user.team == "no_team":
            user_btn_list = [
                "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде", "Найти команду",
                "Уровень знания Python", "Уровень знания C/C++",
                "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
            ]

        elif user.role_command != "TeamLead":
            user_btn_list = [
                "Фамилия", "Имя", "Отчество", "Учебная группа", "Роль в команде",
                "Уровень знания Python", "Уровень знания C/C++",
                "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
            ]

        else:
            user_btn_list = [
                "Фамилия", "Имя", "Отчество", "Учебная группа", "Название команды",
                "Профиль команды", "Уровень знания Python", "Уровень знания C/C++",
                "Уровень знания C#", "Уровень знания Java", "Уровень знания JavaScript",
                "Знание технологий", "Опыт в программировании", "Идея проекта", "✅ Верно"
            ]

        roles_btn_list = [
            "Разработчик", "Тестировщик", "Дизайнер", "Другое"
        ]

        profile_btn_list = [
            "Железо", "Веб", "Бот", "Игра", "Другое"
        ]

        if user.expected_input == "Фамилия":
            if BotFunc.Pavel.surname_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Имя":
            if BotFunc.Pavel.name_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Отчество":
            if BotFunc.Pavel.father_name_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Учебная группа":
            if BotFunc.Pavel.group_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Роль в команде":
            if message.text not in roles_btn_list:
                bot.send_message(message.chat.id, "🖍 Пожалуйста, выберите Вашу роль в команде "
                                 "(только из предложенных вариантов):")

            elif BotFunc.Pavel.role_command_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Название команды":
            old_name = user.team
            if BotFunc.Pavel.team_input(message, bot, user):
                if user.team.endswith("(unreg)"):
                    BotFunc.Pavel.send_msg(
                        bot, message, change_team_msg, 1, *user_btn_list)
                else:
                    BotFunc.Pavel.send_msg(
                        bot, message, rwr_info_msg, 1, *user_btn_list)
                BotFunc.Alexey.update_team_name(user, old_name)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Профиль команды":
            if message.text not in profile_btn_list:
                bot.send_message(message.chat.id, "🖍 Пожалуйста, выберите профиль Вашей команды "
                                 "(только из предложенных вариантов):")

            elif BotFunc.Pavel.team_type_input(message, bot, user):
                BotFunc.Alexey.update_team_type(user.team_type, user.team)
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень знания Python":
            if BotFunc.Pavel.python_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень знания C/C++":
            if BotFunc.Pavel.c_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень знания C#":
            if BotFunc.Pavel.c_sharp_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень знания Java":
            if BotFunc.Pavel.java_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень знания JavaScript":
            if BotFunc.Pavel.js_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Знание технологий":
            if BotFunc.Pavel.user_tech_input(message, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Опыт в программировании":
            if BotFunc.Pavel.user_exp_input(message, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Идея проекта":
            if BotFunc.Pavel.team_idea_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *user_btn_list)
                user.expected_input = "changes_needed"
                user.save()

    else:
        # Набор полей, которые можно изменить, если пользователь - ментор
        mentor_btn_list = [
            "Фамилия", "Имя", "Отчество",
            "Уровень заинтересованности в Python",
            "Уровень заинтересованности в C/C++",
            "Уровень заинтересованности в C#",
            "Уровень заинтересованности в Java",
            "Уровень заинтересованности в JavaScript",
            "Пожелания и ожидания от практики", "✅ Верно"
        ]

        if user.expected_input == "Фамилия":
            if BotFunc.Pavel.surname_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Имя":
            if BotFunc.Pavel.name_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Отчество":
            if BotFunc.Pavel.father_name_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень заинтересованности в Python":
            if BotFunc.Pavel.python_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень заинтересованности в C/C++":
            if BotFunc.Pavel.c_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень заинтересованности в C#":
            if BotFunc.Pavel.c_sharp_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень заинтересованности в Java":
            if BotFunc.Pavel.java_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Уровень заинтересованности в JavaScript":
            if BotFunc.Pavel.js_level_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()

        elif user.expected_input == "Пожелания и ожидания от практики":
            if BotFunc.Pavel.team_idea_input(message, bot, user):
                BotFunc.Pavel.send_msg(
                    bot, message, rwr_info_msg, 1, *mentor_btn_list)
                user.expected_input = "changes_needed"
                user.save()
