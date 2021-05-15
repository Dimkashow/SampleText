from BotFunc.models import User


# Функция для добавления в команду
def team_management(bot, db_user_id, team_name, adding_flag):
    user = User.objects.get(user_id=str(db_user_id))

    if adding_flag and '(unreg)' in user.team:
        bot.send_message(
            user.user_id, "❇️ Вы были приняты в команду " + team_name)
        user.team = team_name
        lead = User.objects.get(team=team_name, role_command='TeamLead')
        user.team_type = lead.team_type
        user.who_mentor = lead.who_mentor
    elif not adding_flag and '(unreg)' in user.team:
        bot.send_message(
            user.user_id, "⛔️ Вы не были приняты в команду " + team_name)
        user.team = "no_team"
        user.team_type = "no_value"
        user.who_mentor = "no_mentor"
    user.save()
