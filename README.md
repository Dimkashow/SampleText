# IU7 Summer Practice Optimizer Bot by SampleText

TelegramBot для оптимизации процесса регистрации, подбора команды, ментора на 
летней практике в университете МГТУ им. Н. Э. Баумана на кафедре ИУ7

* [О команде разработчиков](#о-команде-разработчиков)
* [Используемый технологический стек](#используемый-технологический-стек)
* [Функционал бота](#функционал-бота)
  * [Регистрация в системе](#регистрация-в-системе)
  * [Изменение анкеты](#изменение-анкеты)
  * [Управление командой](#управление-командой)
  * [TODO]

## О команде разработчиков

* **Романов Алексей** - TeamLead, Python-developer
* **Пересторонин Павел** - Python-developer
* **Ковалёв Дмитрий** - Python/Web-developer
* **Симоненко Эмиль** - Python/Web-developer, Tester
* **Кононенко Сергей** - Python-developer, DevOps

## Используемый технологический стек

* **Основной язык программирования** - Python 3.7
* **Используемые модули:**
  * [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 
  * [Django](https://github.com/django/django)
* **Технологии веб-разработки:**
  * HTML5
  * CSS
  * JavaScript
  * [Django](https://github.com/django/django)

## Функционал бота


### Регистрация в системе

* **Система регистрации:**

Функция регистрации (`registration`) вызывается 1 раз - когда пользователь вызывает команду `/start`. При вызове 
команды старт создается объект пользователя в БД и полю `expected_input` по умолчанию присваивается значение `surname`. 
Далее проверяется: если `expected_input` не пустой, то запускается функция `registration`. После того как она исполнится
 пользователю потребуется ответить на вопрос, все ли его устраивает. если нет, то функция перезапустится, если да, то 
 поле `expected_input` станет пустым и функция регистрации больше не запустится.
 

* **Функция изнутри:**

Работа функции внутри предельно проста. 1 большая функция `registration` разбита на части: функции вида 
`<имя_поля_объекта_пользователя>_input`, которые записывают информацию в определенное поле объекта и возвращают 1 в 
случае успеха и 0 - в обратном. Функции, обрабатывающие ввод, также отвечают за выгрузку информации в базу данных. 
Каждый раз, когда обрабатывается какое-либо поле, аттрибут юзера `expected_input` ссылается на следующее поле. 
 Когда регистраия заканчивается, `expected_input` приборетает значение пустой строки.


* **Вспомогательные объекты:**

`send_msg` (отправляет сообщение создавая кастомную клавиатуру, аргументы: bot - ссылка на объект бота, message - ссылка
 на объект сообщения (оттуда берется чат id), msg - сообщение, которое отправится пользователю, row_width - кол-во 
 клавиш в строке, arg1, arg2... -- название клавиш (сколько угодно штук));
 
`hide_markup` (объект, прятающий кастомную клаву);

### Изменение анкеты

### Управление командой

* **Состав команды**
По нажатию кнопки "Управление команды", вызывается функция `show_my_team`. Функция принимает объект сообщения (__message__), объект
бота (__bot__), и объект пользователя, который отправил данное сообщение (то есть нажал на кнопку) (__user_obj__). Далее с помощью (__filter__) происходит "вытаскивание" из БД всех участников команды данного юзера, и все участники и их роли помещаются в отдельный список. Далее происходит компановка
списка в сообщение, и последующая её отправка юзеру через объекта бота (__bot__)

* **Выгнать из команды: (доступно только для TeamLead)**
Если на кнопку "Управление командой" нажимает __TeamLead__, то у него появляется клавиатура с выбором кика (исключения) любого из участников из команды. За исключение из команды отвечает функция `kick_from_team`, которая принимает логин юзера, которого нужно кикнуть (__login__), объект бота и объект юзера (__bot__, __user__). Далее, у юзера, которого нужно кикнуть, в БД меняется поле team на 'no_team', и с помощью объекта бота ему отправляется уведомление о том, что он был исключен из команды. 

### Функции ментора

* **Сортировка по совместимости:**
За сортировку по совместимости (ментор <> команда) отвечает функция `show_command_list`. На вход функция принимает объект сообщения и объект бота (__message__, __bot__). Далее, эта функция получает полный список команд и их тимлидов из БД (с помощью __filter__, и записывает их в словарь. Каждой команде присваивается коэффициент совместимости с ментором, который подсчитывается в функции 
`diff_team_mentor` (подробнее о функции и коэфициенте см. ниже). Далее происходит сортировка словаря по коэфициенту совместимости, и компановка списка команд в единое сообщение. Далее с помощью объекта бота (__bot__), сообщение со списком команд, отсортированных по совместимости, отправляется ментору.

* **Коэффициент совместимости:**
Коэффициент совместимости команды и ментора подсчитывается в функции `diff_team_mentor`. Суть коэфициента: 
1. Подсчитываем "мощность" каждого ЯП для команды. (Например: берется сумма баллов всех участников команды по ЯП __Python__ и делится на общую сумму баллов по всем ЯП -> посчитана "мощность" __Python__ для команды.)
2. Подсчитываем "мощность" каждого ЯП для ментора. (Количество баллов по каждому ЯП делится на общуюу сумму баллов)
3. С помощью формулы
 (|Сила языка __Python__ для команды - сила языка __Python__ для ментора| + 1) x  (|Сила языка __С/C++__ для команды - сила языка __С/C++__ для ментора| + 1) x (|Сила языка __С#__ для команды - сила языка __C#__ для ментора| + 1) x (|Сила языка __Java__ для команды - сила языка __Java#__ для ментора| + 1) x  (|Сила языка __JavaScript__ для команды - сила языка __JavaScript__ для ментора| + 1) 
получаем коэффициент cовместимости. 

Чем коэфициент меньше, тем больше ментор и команда подходит друг другу. Сама же функция на вход получает список команды (__list_team__) и объект ментора (__mentor_obj__). Далее просто "вытягиваем" из БД баллы ЯП участников команды и ментора и подставляем в математическую формулу. Функция уже готовый коэффициент (__difference__)

* **Сортировка по направлению команды:**
Функция `sort_by_team_type` отвечает за сортировку команд по определнному направлению. На вход в функцию приходит объект самого сообщения, 
которое содержит направление сортировки (__message__), и объект бота (__bot__). Далее в функции происходит поиск всех команд и их тимлидов (с помощью __filter__) с заданным направлением. После этого данный список команд и тимлидов компануется в одно сообщение, которое отправляется с помощью
объекта бота.

