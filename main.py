import telebot
from telebot import types

# Инициализация бота с токеном
f = open("access_to_bot.txt")
s = f.readline()
bot = telebot.TeleBot(str(s))
f.close()

# Cписок всех пользователей, которые взаимодействовали с ботом
users1 = {}



def matrix_product_number(chat_id):
    A=users1[chat_id]['A']
    x=float(users1[chat_id]['What_number_product'])
    n = int(users1[chat_id]['lines_in_A'])
    m = int(users1[chat_id]['columns_in_A'])
    for i in range(n):
        for j in range(m):
            A[i][j]*=x
    for i in range(n):
        s = ' '.join(map(str, A[i]))
        bot.send_message(chat_id, s)
    users1[chat_id]['state']='idle'
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text="Транспонировать", callback_data=f'button1:{chat_id}')
    button2 = types.InlineKeyboardButton(text="Умножить на число", callback_data=f'button2:{chat_id}')
    button3 = types.InlineKeyboardButton(text="Найти определитель", callback_data=f'button3:{chat_id}')
    button4 = types.InlineKeyboardButton(text="Возвести в квадрат", callback_data=f'button4:{chat_id}')
    button5 = types.InlineKeyboardButton(text="Найти ранг", callback_data=f'button5:{chat_id}')
    button6 = types.InlineKeyboardButton(text="Обратная матрица", callback_data=f'button6:{chat_id}')
    button7 = types.InlineKeyboardButton(text="Сумма/разность матриц", callback_data=f'button7:{chat_id}')
    button8 = types.InlineKeyboardButton(text="Произведение матриц", callback_data=f'button8:{chat_id}')
    markup.add(button1, button8, button7, button6, button5, button4, button3, button2)
    bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=markup)


# Отправка рассылки
def send_broadcast(message):
    f = open("data.txt")
    for i in f:
        username, chat_id = i.split(':')[0], int(i.split(':')[1])
        bot.send_message(chat_id, f"{message}")
        # добавить удаление лишней строки!!!
    f.close()


# Обработчик команды для рассылки
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    chat_id = message.chat.id
    print(type(chat_id))
    if chat_id == 697156742:  # Проверка, что команду отправляет создатель бота
        send_broadcast('Это рассылка для всех пользователей.')
    else:
        bot.send_message(chat_id, 'У вас нет прав на выполнение этой команды.')


# Обработчик команды для рассылки ответов на вопросы
@bot.message_handler(commands=['answers'])
def answers_message(message):
    chat_id = message.chat.id
    if chat_id == 697156742:  # Проверка, что команду отправляет создатель бота
        bot.send_message(756603394, "Вай малыха!! Я генекалог по работа скинь свой писка я посмотрю простудилась нет")
    else:
        bot.send_message(chat_id, 'У вас нет прав на выполнение этой команды.')




# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    username = message.from_user.username
    f = open("data.txt", 'a')
    f.write(f'{username}:{chat_id}\n')
    f.close()
    users1[chat_id] = {'username': username,'lines_in_A': None, 'lines_in_B':None,'column_in_A':None,'column_in_B':None, 'What_number_product':None, 'A':None, 'B': None, 'goal': None ,'state':'idle'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton("Работа с матрицами")
    button2 = types.KeyboardButton("Информация о боте")
    button3 = types.KeyboardButton("Написать в поддержку")
    markup.add(button1).row(button2, button3)
    bot.send_message(chat_id, f'Привет, {username}! Я бот, который упростит твою работу с матрицами.', reply_markup=markup)


# Обработчик команды /help
@bot.message_handler(commands=['support'])
def help_message(message):
    chat_id = message.chat.id
    creator_chat_id = '697156742'  # Замените на свой chat_id
    if message.text == '/support':
        bot.send_message(chat_id, "Введите ваш вопрос сразу после команды /support через пробел.")
    elif message.text == 'Написать в поддержку':
        bot.send_message(chat_id, "Введите ваш вопрос сразу после команды /support через пробел.")
    else:
        bot.send_message(creator_chat_id, f'Пользователь {chat_id} запрашивает помощь:\n\n{message.text}')
        bot.send_message(chat_id, 'Ваш запрос успешно отправлен, в скором времени вы получите ответ.')


# Реакция бота на разные сообщения от пользователя
@bot.message_handler(func=lambda message: True)
def message_from_user(message):
    chat_id=message.chat.id
    if chat_id in users1:
        state=users1[chat_id]['state']
        goal=users1[chat_id]['goal']
    else:
        users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'column_in_A': None,
                           'column_in_B': None, 'What_number_product': None, 'A': None, 'B': None, 'goal': None,
                           'state': 'idle'}
        state = users1[chat_id]['state']
        goal = users1[chat_id]['goal']
    if (message.text == "Написать в поддержку"):
        help_message(message)
    elif (message.text == "Информация о боте"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Что я умею?")
        button2 = types.KeyboardButton("Создатели")
        button3 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(button1).row(button2, button3)
        bot.send_message(message.chat.id, 'Что конкретно вас интересует?', reply_markup=markup)
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Работа с матрицами")
        button2 = types.KeyboardButton("Информация о боте")
        button3 = types.KeyboardButton("Написать в поддержку")
        markup.add(button1).row(button2, button3)
        bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=markup)
    elif (message.text == 'Работа с матрицами'):
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(text="Транспонировать", callback_data = f'button1:{chat_id}')
        button2 = types.InlineKeyboardButton(text="Умножить на число", callback_data= f'button2:{chat_id}')
        button3 = types.InlineKeyboardButton(text="Найти определитель", callback_data= f'button3:{chat_id}')
        button4 = types.InlineKeyboardButton(text="Возвести в квадрат", callback_data= f'button4:{chat_id}')
        button5 = types.InlineKeyboardButton(text="Найти ранг", callback_data= f'button5:{chat_id}')
        button6 = types.InlineKeyboardButton(text="Обратная матрица", callback_data= f'button6:{chat_id}')
        button7 = types.InlineKeyboardButton(text="Сумма/разность матриц", callback_data= f'button7:{chat_id}')
        button8 = types.InlineKeyboardButton(text="Произведение матриц", callback_data= f'button8:{chat_id}')
        markup.add(button1, button8, button7, button6, button5, button4, button3, button2)
        bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=markup)
    elif state == 'waiting_for_number_lines_A':
        try:
            n = int(message.text)
            users1[chat_id]['lines_in_A'] = n
            users1[chat_id]['state'] = 'waiting_for_number_column_A'
            bot.send_message(chat_id, 'Введите число столбцов матрицы:')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state == 'waiting_for_number_column_A':
        try:
            m = int(message.text)
            users1[chat_id]['columns_in_A'] = m
            if goal=='matrix_product_number':
                users1[chat_id]['state']='waiting_for_matrix_A'
                bot.send_message(chat_id, 'Введите матрицу (в строку)')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state == 'waiting_for_matrix_A':
        try:
            tx=message.text.split(" ")
            n=int(users1[chat_id]['lines_in_A'])
            m=int(users1[chat_id]['columns_in_A'])
            A=[[0 for i in range(m)] for i in range(n)]
            tx=[int(i) for i in tx]
            if len(tx)==n*m:
                k=0
                for i in range(n):
                    for j in range(m):
                        A[i][j]=tx[k]
                        k+=1
                users1[chat_id]['A'] = A
                if users1[chat_id]['goal'] == 'matrix_product_number':
                    users1[chat_id]['state'] = 'waiting_for_number'
                    bot.send_message(chat_id, 'Введите число, на которое хотите умножить матрицу:')
            else:
                bot.send_message(chat_id, 'Неправильный формат данных. Попробуйте ещё раз.')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат данных. Попробуйте ещё раз.')
    elif state == 'waiting_for_number':
        try:
            n = float(message.text)
            users1[chat_id]['What_number_product'] = n
            users1[chat_id]['state'] = 'idle'
            matrix_product_number(chat_id)
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')



# Обработка кнопок, связанных с работой с матрицами
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if "button2" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None, 'goal': 'matrix_product_number',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'matrix_product_number'
            bot.send_message(chat_id, 'Введите число строк матрицы:')


# Запуск бота
bot.polling(none_stop=True)
