# -*- coding: utf-8 -*-
import telebot
from telebot import types
from itertools import permutations

# Инициализация бота с токеном
f = open("access_to_bot.txt")
s = f.readline()
bot = telebot.TeleBot(str(s))
f.close()


# Cписок всех пользователей, которые взаимодействовали с ботом
users1 = {}

# Функция нахождения ранга матрицы
def rank(a,n1,m1):
    max_rank=min(n1,m1)
    klu=0
    key=1
    tek_rank=2
    rank=0
    bazed_lines=[]
    bazed_columns=[]
    for i in range(n1):
        if klu==1:
            break
        for j in range(m1):
            if a[i][j]!=0:
                bazed_lines.append(i)
                bazed_columns.append(j)
                rank=1
                klu=1
                break
    if klu==0:
        return 0
    else:
        while key:
            if tek_rank>max_rank:
                break
            b=[]
            k=0
            new_matrix=[[0 for i in range(tek_rank)] for j in range(tek_rank)]
            key=0
            tek_lines=(permutations(range(n1), tek_rank))
            tek_columns=(permutations(range(m1),tek_rank))
            bas_tek_lines=[i for i in tek_lines if all(bazed_lines) in i]
            bas_tek_columns=[i for i in tek_columns if all(bazed_columns) in i]
            for i in bas_tek_lines:
                if key==1:
                    break
                for j in bas_tek_columns:
                    if key==1:
                        break
                    for line in sorted(list(i)):
                        if key==1:
                            break
                        for column in sorted(list(j)):
                            if key==1:
                                break
                            b.append(a[line][column])
                    for x in range(tek_rank):
                        for y in range(tek_rank):
                            new_matrix[x][y]=b[k]
                            k+=1
                    if determinant(new_matrix,tek_rank,tek_rank)!=0:
                        key=1
                        tek_rank+=1
                        rank+=1
                        break
    return rank


# Функция сложеня матриц
def sum_matrix(A, B, n1, m1, n2, m2,chat_id):
    c = [[0 for i in range(m1)] for j in range(n1)]
    sign = users1[chat_id]['sign']
    if sign=='-':
        new_b = [[0 for i in range(m2)] for j in range(n2)]
        for i in range(n2):
            for j in range(m2):
                new_b[i][j]=-B[i][j]
        B=new_b
    for i in range(n1):
        for j in range(m1):
            c[i][j] = A[i][j] + B[i][j]
    s = '  '
    for i in range(n1):
        for j in range(len(c[i])):
            if j == 0:
                s += '{:.3f}'.format(c[i][j])
            else:
                s += '{:7.3f}'.format(c[i][j])
            if j != (len(c[i]) - 1):
                s += '  '
        s += '\n'
    s = f'<b>{s}</b>'
    bot.send_message(chat_id, s, parse_mode='HTML')
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


# Функция по нахождению обратной матрицы
def reverse_matrix(a, n1, m1, det, chat_id):
    c = [[0 for i in range(m1)] for j in range(n1)]
    for i in range(n1):
        for j in range(m1):
            alg = (-1) ** (i + j)
            b = []
            for line in range(n1):
                for column in range(m1):
                    if line != i and column != j:
                        b.append(a[line][column])
            B = [[0 for i in range(m1 - 1)] for j in range(n1 - 1)]
            ind = 0
            for line in range(n1 - 1):
                for column in range(m1 - 1):
                    B[line][column] = b[ind]
                    ind += 1
            alg *= determinant(B, n1 - 1, m1 - 1)
            c[i][j] = alg
    trans = transpose_matrix(c)
    number = 1 / det
    users1[chat_id]['A'] = trans
    users1[chat_id]['What_number_product'] = number
    users1[chat_id]['lines_in_A'] = len(trans)
    users1[chat_id]['columns_in_A'] = len(trans[0])
    matrix_product_number(chat_id)


# Функция для транспонирования матрицы
def transpose_matrix(matrix):
    transposed_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    return transposed_matrix


# Функция перемножения матриц
def product_matrix(A, B, n1, m1, n2, m2, chat_id):
    c = [[0 for i in range(m2)] for i in range(n1)]
    for i in range(n1):
        for j in range(m2):
            for k in range(m1):
                c[i][j] += (A[i][k] * B[k][j])
    s = '  '
    for i in range(n1):
        for j in range(len(c[i])):
            if j == 0:
                s += '{:.3f}'.format(c[i][j])
            else:
                s += '{:7.3f}'.format(c[i][j])
            if j != (len(c[i]) - 1):
                s += '  '
        s += '\n'
    s = f'<b>{s}</b>'
    bot.send_message(chat_id, s, parse_mode='HTML')
    users1[chat_id]['state'] = 'idle'
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


# Функция умножения матрицы на число
def matrix_product_number(chat_id):
    A = users1[chat_id]['A']
    x = float(users1[chat_id]['What_number_product'])
    n = int(users1[chat_id]['lines_in_A'])
    m = int(users1[chat_id]['columns_in_A'])
    for i in range(n):
        for j in range(m):
            A[i][j] *= x
    s = '  '
    for i in range(n):
        for j in range(len(A[i])):
            if j == 0:
                s += '{:.3f}'.format(A[i][j])
            else:
                s += '{:7.3f}'.format(A[i][j])
            if j != (len(A[i]) - 1):
                s += '  '
        s += '\n'
    s = f'<b>{s}</b>'
    bot.send_message(chat_id, s, parse_mode='HTML')
    users1[chat_id]['state'] = 'idle'
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


# Поиск детерминанта матрицы
def determinant(a, n, m):
    su = 0
    if n == m == 1:
        return a[0][0]
    for column in range(m):
        new_a = [[0 for i in range(m - 1)] for i in range(m - 1)]
        b = []
        for i in range(1, n):
            for j in range(m):
                if j == column:
                    continue
                else:
                    b.append(a[i][j])
        ind = 0
        for i in range(m - 1):
            for j in range(m - 1):
                new_a[i][j] = b[ind]
                ind += 1
        su = su + ((-1) ** column) * a[0][column] * determinant(new_a, n - 1, m - 1)
    return su


# Отправка рассылки
def send_broadcast(message):
    f = open("data.txt")
    for i in f:
        username, chat_id = i.split(':')[0], int(i.split(':')[1])
        bot.send_message(chat_id, f"{message}")
    f.close()


# Обработчик команды для рассылки
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    chat_id = message.chat.id
    if chat_id == 697156742:  # Проверка, что команду отправляет создатель бота
        f=open('broadcast.txt', encoding='utf-8')
        s=f.readline()
        f.close()
        send_broadcast(s)
    else:
        bot.send_message(chat_id, 'У вас нет прав на выполнение этой команды.')


# Обработчик команды для рассылки ответов на вопросы
@bot.message_handler(commands=['answers'])
def answers_message(message):
    chat_id = message.chat.id
    if chat_id == 697156742:  # Проверка, что команду отправляет создатель бота
        f = open("answers_broadcast.txt", 'r+', encoding='utf-8')
        i = f.readline()
        while i != '\n' and i != '':
            chat_id, mes = int(i.split(":")[0]), (i.split(":")[1])
            bot.send_message(chat_id, 'Вот ответ на ваш запрос от службы поддержки:')
            bot.send_message(chat_id, mes)
            i = f.readline()
        f.close()
        print("Отправка ответов на вопросы закончилась")
    else:
        bot.send_message(chat_id, 'У вас нет прав на выполнение этой команды.')


user = []


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if chat_id not in user:
        f = open("data.txt", 'r+')
        i = f.readline()
        while i != '\n' and i != '':
            i = int(i.split(":")[1])
            if i == chat_id:
                break
            else:
                user.append(i)
                i = f.readline()
        else:
            f.write(f'{username}:{chat_id}\n')
        f.close()
    users1[chat_id] = {'username': username, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                       'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None, 'goal': None,
                       'state': 'idle'}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton("Работа с матрицами")
    button2 = types.KeyboardButton("Информация о боте")
    button3 = types.KeyboardButton("Написать в поддержку")
    markup.add(button1).row(button2, button3)
    bot.send_message(chat_id, f'Привет, <b>{username}</b>! Я бот, который упростит твою работу с матрицами.',
                     reply_markup=markup, parse_mode='HTML')


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
    chat_id = message.chat.id
    if chat_id in users1:
        state = users1[chat_id]['state']
        goal = users1[chat_id]['goal']
    else:
        users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                           'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None, 'goal': None,
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
    elif (message.text=="Что я умею?"):
        bot.send_message(message.chat.id, 'Привет! Я <b>Matrix_assistant</b> бот и я помогу тебе быстро работать с матрицами. Я могу:\nТранспонировать матрицу\nНайти произведение двух матриц\nНайти сумму двух матриц\nНайти разность двух матриц\nНайти обратную матрицу\nНайти ранг матрицы\nВозвести матрицу в квадрат\nНайти определитель матрицы\nУмножить матрицу на число\nНачнем?', parse_mode='HTML')
    elif (message.text == "Создатели"):
        bot.send_message(message.chat.id, 'Telegram-bot создали <b>Муслин Артемий</b>, <b>Яшина Нина</b>, <b>Калетурина Полина</b> и <b>Гарин Андрей</b>.\nПроектная работа от 25.10.23', parse_mode='HTML')
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Работа с матрицами")
        button2 = types.KeyboardButton("Информация о боте")
        button3 = types.KeyboardButton("Написать в поддержку")
        markup.add(button1).row(button2, button3)
        bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=markup)
    elif (message.text == 'Работа с матрицами'):
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
        bot.send_message(message.chat.id, "Выберите дальнейшее действие", reply_markup=markup)
    elif state == 'waiting_for_number_lines_A':
        try:
            n = int(message.text)
            users1[chat_id]['lines_in_A'] = n
            users1[chat_id]['state'] = 'waiting_for_number_columns_A'
            bot.send_message(chat_id, 'Введите число <b>столбцов</b> матрицы:', parse_mode='HTML')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state == 'waiting_for_number_columns_A':
        try:
            m = int(message.text)
            n = users1[chat_id]['lines_in_A']
            users1[chat_id]['columns_in_A'] = m
            if goal == 'determinant':
                if n != m:
                    bot.send_message(chat_id,
                                     "Детерминанта у данной матрицы <b>не существует</b>.\nОн существует только у квадратных матриц.",
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    users1[chat_id]['state'] = 'waiting_for_matrix_A'
                    bot.send_message(chat_id, 'Введите матрицу:')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')
            elif goal == 'matrix_product_number' or goal == 'product_matrix' or goal == 'trans' or goal == 'sum_matrix' or goal=='rank':
                users1[chat_id]['state'] = 'waiting_for_matrix_A'
                bot.send_message(chat_id, 'Введите матрицу:')
                bot.send_message(chat_id,
                                 '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                 parse_mode='HTML')
            elif goal == 'square_matrix':
                if n != m:
                    bot.send_message(chat_id,
                                     "Возвести в квадрат данную матрицу <b>нельзя</b>, так как кол-во строк не равно кол-ву столбцов.",
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    users1[chat_id]['state'] = 'waiting_for_matrix_A'
                    bot.send_message(chat_id, 'Введите матрицу:')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')
            elif goal == 'reversed_matrix':
                if n != m:
                    bot.send_message(chat_id,
                                     "Обратная матрица <b>не существует</b>.\nПримечание: ее можно найти только у квадратных матриц.",
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    users1[chat_id]['state'] = 'waiting_for_matrix_A'
                    bot.send_message(chat_id, 'Введите матрицу:')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')

        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state == 'waiting_for_matrix_A' or state == 'waiting_for_matrix_B':
        try:
            if state == 'waiting_for_matrix_A':
                n = int(users1[chat_id]['lines_in_A'])
                m = int(users1[chat_id]['columns_in_A'])
                A = [[0 for i in range(m)] for i in range(n)]
                tx = [float(i) for i in message.text.split(" ")]
                if len(tx) == n * m:
                    k = 0
                    for i in range(n):
                        for j in range(m):
                            A[i][j] = tx[k]
                            k += 1
                    users1[chat_id]['A'] = A
                    if users1[chat_id]['goal'] == 'matrix_product_number':
                        users1[chat_id]['state'] = 'waiting_for_number'
                        bot.send_message(chat_id, 'Введите <b>число</b>, на которое хотите умножить матрицу:',
                                         parse_mode='HTML')
                    elif users1[chat_id]['goal'] == 'reversed_matrix':
                        det = determinant(users1[chat_id]['A'], users1[chat_id]['lines_in_A'],
                                          users1[chat_id]['columns_in_A'])
                        if det != 0:
                            reverse_matrix(users1[chat_id]['A'], users1[chat_id]['lines_in_A'],
                                           users1[chat_id]['columns_in_A'], det, chat_id)
                        else:
                            bot.send_message(chat_id,
                                             'Обратной матрицы <b>не существует</b>.\nПримечание: ее можно найти если определитель матрицы не равен нулю',
                                             parse_mode='HTML')
                    elif users1[chat_id]['goal']=='rank':
                        r = rank(users1[chat_id]['A'], users1[chat_id]['lines_in_A'], users1[chat_id]['columns_in_A'])
                        users1[chat_id]['state']='idle'
                        bot.send_message(chat_id, f'Ранг данной матрицы равен: <b>{r}</b>', parse_mode='HTML')
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        button1 = types.InlineKeyboardButton(text="Транспонировать", callback_data=f'button1:{chat_id}')
                        button2 = types.InlineKeyboardButton(text="Умножить на число",
                                                             callback_data=f'button2:{chat_id}')
                        button3 = types.InlineKeyboardButton(text="Найти определитель",
                                                             callback_data=f'button3:{chat_id}')
                        button4 = types.InlineKeyboardButton(text="Возвести в квадрат",
                                                             callback_data=f'button4:{chat_id}')
                        button5 = types.InlineKeyboardButton(text="Найти ранг", callback_data=f'button5:{chat_id}')
                        button6 = types.InlineKeyboardButton(text="Обратная матрица",
                                                             callback_data=f'button6:{chat_id}')
                        button7 = types.InlineKeyboardButton(text="Сумма/разность матриц",
                                                             callback_data=f'button7:{chat_id}')
                        button8 = types.InlineKeyboardButton(text="Произведение матриц",
                                                             callback_data=f'button8:{chat_id}')
                        markup.add(button1, button8, button7, button6, button5, button4, button3, button2)
                        bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=markup)
                    elif users1[chat_id]['goal'] == 'determinant':
                        users1[chat_id]['state'] = 'idle'
                        det = determinant(A, n, m)
                        bot.send_message(chat_id, "Детерминант данной матрицы равен: <b>{:.3f}</b>".format(det),
                                         parse_mode='HTML')
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        button1 = types.InlineKeyboardButton(text="Транспонировать", callback_data=f'button1:{chat_id}')
                        button2 = types.InlineKeyboardButton(text="Умножить на число",
                                                             callback_data=f'button2:{chat_id}')
                        button3 = types.InlineKeyboardButton(text="Найти определитель",
                                                             callback_data=f'button3:{chat_id}')
                        button4 = types.InlineKeyboardButton(text="Возвести в квадрат",
                                                             callback_data=f'button4:{chat_id}')
                        button5 = types.InlineKeyboardButton(text="Найти ранг", callback_data=f'button5:{chat_id}')
                        button6 = types.InlineKeyboardButton(text="Обратная матрица",
                                                             callback_data=f'button6:{chat_id}')
                        button7 = types.InlineKeyboardButton(text="Сумма/разность матриц",
                                                             callback_data=f'button7:{chat_id}')
                        button8 = types.InlineKeyboardButton(text="Произведение матриц",
                                                             callback_data=f'button8:{chat_id}')
                        markup.add(button1, button8, button7, button6, button5, button4, button3, button2)
                        bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=markup)
                    elif users1[chat_id]['goal'] == 'product_matrix':
                        users1[chat_id]['state'] = 'waiting_for_number_lines_B'
                        bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы, на которую хотите умножить:',
                                         parse_mode='HTML')
                    elif users1[chat_id]['goal'] == 'sum_matrix':
                        users1[chat_id]['state'] = 'waiting_for_number_lines_B'
                        bot.send_message(chat_id, 'Введите число <b>строк</b> второй матрицы:',
                                         parse_mode='HTML')
                    elif users1[chat_id]['goal'] == 'square_matrix':
                        users1[chat_id]['state'] = 'idle'
                        product_matrix(A, A, n, m, n, m, chat_id)
                    elif users1[chat_id]['goal'] == 'trans':
                        users1[chat_id]['state'] = 'idle'
                        trans = transpose_matrix(users1[chat_id]['A'])
                        s = '  '
                        for i in range(len(trans)):
                            for j in range(len(trans[i])):
                                if j == 0:
                                    s += '{:.3f}'.format(trans[i][j])
                                else:
                                    s += '{:7.3f}'.format(trans[i][j])
                                if j != (len(trans[i]) - 1):
                                    s += '  '
                            s += '\n'
                        bot.send_message(chat_id, s)
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        button1 = types.InlineKeyboardButton(text="Транспонировать", callback_data=f'button1:{chat_id}')
                        button2 = types.InlineKeyboardButton(text="Умножить на число",
                                                             callback_data=f'button2:{chat_id}')
                        button3 = types.InlineKeyboardButton(text="Найти определитель",
                                                             callback_data=f'button3:{chat_id}')
                        button4 = types.InlineKeyboardButton(text="Возвести в квадрат",
                                                             callback_data=f'button4:{chat_id}')
                        button5 = types.InlineKeyboardButton(text="Найти ранг", callback_data=f'button5:{chat_id}')
                        button6 = types.InlineKeyboardButton(text="Обратная матрица",
                                                             callback_data=f'button6:{chat_id}')
                        button7 = types.InlineKeyboardButton(text="Сумма/разность матриц",
                                                             callback_data=f'button7:{chat_id}')
                        button8 = types.InlineKeyboardButton(text="Произведение матриц",
                                                             callback_data=f'button8:{chat_id}')
                        markup.add(button1, button8, button7, button6, button5, button4, button3, button2)
                        bot.send_message(chat_id, "Выберите дальнейшее действие", reply_markup=markup)

                else:
                    bot.send_message(chat_id, 'Неправильный формат данных. Попробуйте ещё раз.')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')
            elif state == 'waiting_for_matrix_B':
                n2 = int(users1[chat_id]['lines_in_B'])
                m2 = int(users1[chat_id]['columns_in_B'])
                B = [[0 for i in range(m2)] for i in range(n2)]
                tx = [int(i) for i in message.text.split(" ")]
                if len(tx) == n2 * m2:
                    k = 0
                    for i in range(n2):
                        for j in range(m2):
                            B[i][j] = tx[k]
                            k += 1
                    users1[chat_id]['B'] = B
                    if users1[chat_id]['goal'] == 'product_matrix':
                        product_matrix(users1[chat_id]['A'], users1[chat_id]['B'], users1[chat_id]['lines_in_A'],
                                       users1[chat_id]['columns_in_A'], users1[chat_id]['lines_in_B'],
                                       users1[chat_id]['columns_in_B'], chat_id)
                    elif users1[chat_id]['goal'] == 'sum_matrix':
                        users1[chat_id]['state'] = 'sign'
                        bot.send_message(chat_id, 'Введите действие, которое хотите выполнить: <b>+</b> или <b>-</b>', parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Неправильный формат данных. Попробуйте ещё раз.')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')
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
    elif state == 'waiting_for_number_lines_B':
        try:
            n2 = int(message.text)
            users1[chat_id]['lines_in_B'] = n2
            users1[chat_id]['state'] = 'waiting_for_number_columns_B'
            m1 = users1[chat_id]['columns_in_A']
            if users1[chat_id]['goal'] == 'product_matrix':
                if n2 != m1:
                    bot.send_message(chat_id,
                                     'Перемножение этих матриц <b>невозможно</b>.\nПримечание: чтобы умножить матрицы A*B\nкол-во столбцов матрицы A должно быть равно кол-ву строк матрицы B',
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    bot.send_message(chat_id, 'Введите число <b>столбцов</b> этой матрицы:', parse_mode='HTML')
            elif users1[chat_id]['goal'] == 'sum_matrix':
                if n2!=users1[chat_id]['lines_in_A']:
                    bot.send_message(chat_id,
                                     'Выполнить действие с этими матрицами <b>невозможно</b>.\nПримечание: размерности матриц должны быть одинаковыми',
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    bot.send_message(chat_id, 'Введите число <b>столбцов</b> этой матрицы:', parse_mode='HTML')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state == 'waiting_for_number_columns_B':
        try:
            m2 = int(message.text)
            users1[chat_id]['columns_in_B'] = m2
            users1[chat_id]['state'] = 'waiting_for_matrix_B'
            if goal == 'product_matrix':
                bot.send_message(chat_id, 'Введите матрицу:')
                bot.send_message(chat_id,
                                 '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                 parse_mode='HTML')
            elif goal=='sum_matrix':
                if users1[chat_id]['columns_in_A']!=m2:
                    bot.send_message(chat_id,
                                     'Выполнить действие с этими матрицами <b>невозможно</b>.\nПримечание: размерности матриц должны быть одинаковыми',
                                     parse_mode='HTML')
                    users1[chat_id]['state'] = 'idle'
                else:
                    bot.send_message(chat_id, 'Введите матрицу:')
                    bot.send_message(chat_id,
                                     '<b>ВАЖНО!</b>\nОбязательно посмотрите, как нужно вводить данные\nЕсли у вас есть матрица:\n1 2 3\n4 5 6\n7 8 9\nТо введите :"1 2 3 4 5 6 7 8 9"\nТо есть сначала вводите элементы первой строки через пробел, потом второй строки и т.д.',
                                     parse_mode='HTML')
        except ValueError:
            bot.send_message(chat_id, 'Неправильный формат числа. Попробуйте ещё раз.')
    elif state=='sign':
        try:
            sign=message.text
            if sign=='+':
                users1[chat_id]['sign'] = '+'
                sum_matrix(users1[chat_id]['A'], users1[chat_id]['B'], users1[chat_id]['lines_in_A'],
                               users1[chat_id]['columns_in_A'], users1[chat_id]['lines_in_B'],
                               users1[chat_id]['columns_in_B'], chat_id)
                users1[chat_id]['state']='idle'
            elif sign=='-':
                users1[chat_id]['sign'] = '-'
                sum_matrix(users1[chat_id]['A'], users1[chat_id]['B'], users1[chat_id]['lines_in_A'],
                           users1[chat_id]['columns_in_A'], users1[chat_id]['lines_in_B'],
                           users1[chat_id]['columns_in_B'], chat_id)
                users1[chat_id]['state'] = 'idle'
            else:
                bot.send_message(chat_id, 'Неправильный формат. Введите <b>+</b> или <b>-</b>', parse_mode='HTML')
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
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'matrix_product_number',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'matrix_product_number'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button3" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'determinant',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'determinant'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button8" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'product_matrix',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'product_matrix'
            bot.send_message(chat_id,
                             'Введите число <b>строк</b> матрицы:\nЕсли у вас умножение матриц A*B,\nто введите число строк матрицы A',
                             parse_mode='HTML')
        elif "button4" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'square_matrix',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'square_matrix'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button1" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'trans',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'trans'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button6" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'reversed_matrix',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'reversed_matrix'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button7" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'sum_matrix',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'sum_matrix'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')
        elif "button5" in call.data:
            chat_id = int(call.data.split(':')[1])
            if chat_id not in users1:
                users1[chat_id] = {'username': None, 'lines_in_A': None, 'lines_in_B': None, 'columns_in_A': None,
                                   'columns_in_B': None, 'What_number_product': None, 'A': None, 'B': None,
                                   'goal': 'rank',
                                   'state': 'waiting_for_number_lines_A'}
            else:
                users1[chat_id]['state'] = 'waiting_for_number_lines_A'
                users1[chat_id]['goal'] = 'rank'
            bot.send_message(chat_id, 'Введите число <b>строк</b> матрицы:', parse_mode='HTML')


# Запуск бота
bot.polling(none_stop=True)
