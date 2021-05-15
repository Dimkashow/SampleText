from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import telebot
from BotFunc.config import TOKEN_practice
from telebot.types import Message
from BotFunc.models import User
from BotFunc.Pavel import registration
from BotFunc.Dmitriy import main_func
from BotFunc.Emil import team_management
from BotFunc.Sergey import check_registration, check_changes, change_registration, make_changes
from telebot import types


hide_markup = types.ReplyKeyboardRemove(selective=False)
bot = telebot.TeleBot(TOKEN_practice)


@csrf_exempt
def event(request):
    json_list = json.loads(request.body)
    update = telebot.types.Update.de_json(json_list)
    try:
        bot.process_new_messages([update.message])
    except:
        bot.process_new_callback_query([update.callback_query])
    return HttpResponse()


@bot.callback_query_handler(func=lambda call: True)
def add_to_team(call):
    print(type(call))
    arr = call.data.split('@@@')
    user = User.objects.get(user_id=str(arr[1]))
    if arr[0] == 'да':
        flag = True
        info = "Пользователь @" + user.login + " добавлен в команду " + arr[2]
    else:
        flag = False
        info = "Пользователь @" + user.login + \
            " не добавлен в команду " + arr[2]

    team_management(bot, arr[1], arr[2], flag)
    bot.answer_callback_query(call.id, info)


@bot.message_handler(commands=["start"])
def test_message(message: Message):
    if User.objects.filter(user_id=str(message.chat.id)):
        bot.send_message(
            message.chat.id, "💡 Вы уже зарегистрированы в системе.", reply_markup=hide_markup)
    else:
        try:
            update_reg_info = User.objects.create(user_id=str(
                message.chat.id), login=message.chat.username)
            if message.text[7:] == "23CBEACDEA458E9CED9807D6CBE2F4D6":
                bot.send_message(
                    message.chat.id, "🎓 Ваша роль: ментор.", reply_markup=hide_markup)
                update_reg_info.is_mentor = "1"
            update_reg_info.save()
            bot.send_message(
                message.chat.id, "💡 Добро пожаловать в систему. Пожалуйста, пройдите регистрацию\n\n", reply_markup=hide_markup)
            bot.send_message(
                message.chat.id, "🖍 Пожалуйста, введите Вашу фамилию (с большой буквы): ", reply_markup=hide_markup)
        except:
            bot.send_message(message.chat.id, "✈ Пожалуйста, укажите имя пользователя в настройках Telegram. \n"
                             "После того, как укажете имя пользователя, снова наберите команду /start", reply_markup=hide_markup)


@bot.message_handler(commands=["help"])
def help_message(message: Message):
    help_txt = "🌍 IU7 SUMMER PRACTICE TELEGRAM BOT 🌍\n\n" \
        "Данный бот предназначен для оптимизации процесса подбора команды (как для " \
        "ментора, так и для студентов) " \
        "на летней практике для студентов первого курса " \
        "в МГТУ им. Н. Э. Баумана, на кафедре ИУ7. \n\n" \
        "🛠 Разработчики:\n" \
        "📍 Романов Алексей @mrrvz1\n" \
        "📍 Пересторонин Павел @Justarone\n" \
        "📍 Кононенко Сергей @hackfeed\n" \
        "📍 Дмитрий Ковалёв @dimkov27\n" \
        "📍 Симоненко Эмиль @A_Mill\n\n" \
        "🔱 Все права защищены. 2019 год."
    bot.send_message(message.chat.id, help_txt)


@bot.message_handler(content_types=["text"])
def main(message: Message):
    if User.objects.filter(user_id=str(message.chat.id)):
        user = User.objects.get(user_id=str(message.chat.id))
        if user.expected_command == "wait agree":
            pass
        if user.expected_input != "":
            registration(message, bot, user)
            check_registration(message, bot, user)
            check_changes(message, bot, user)
            make_changes(message, bot, user)
            change_registration(message, bot, user)
            if user.expected_input == "":
                main_func(message, bot, user)
        else:
            main_func(message, bot, user)
