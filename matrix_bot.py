import telebot
from copy import deepcopy

bot = telebot.TeleBot('7463524489:AAEy_NLXqVssE9jIsCNMfR4AwroV10fiSlk')


class Matrix:
    def __init__(self):
        ...

    def add_rank(self, rank):
        self.rank = int(rank)

    def get_matrix(self, message):
        """Ввод СЛАУ"""
        self.A = []  # матрица коэффициентов
        self.B = []  # матрица свободных членов
        message_text = message.text.split()
        message_text = list(map(float, message_text))
        for i in range(self.rank):
            self.A.append(message_text[i * (self.rank + 1):(i + 1) * (self.rank + 1)][:self.rank])
            self.B.append(message_text[i * (self.rank + 1):(i + 1) * (self.rank + 1)][self.rank:])
        self.show_matrix(message)

    def show_matrix(self, message):
        """Вывод СЛАУ"""
        text = 'Ваша матрица:\n\n'
        for a, b in zip(self.A, self.B):
            for i in range(len(a)):
                text += f'{a[i]} '
            text += f'| {b[0]}\n'
        bot.send_message(message.chat.id, text)
        self.show_answer(message)

    def show_answer(self, message):
        det = self.determinant(self.A)
        ans = self.Kramer_Function(self.A, self.B, det)
        if isinstance(ans, list):
            text = 'Ответ:\n\n'
            for i in range(len(ans)):
                text += f'x{i + 1} = {ans[i]}\n'
        else:
            text = f'Ответ: {ans}'
        bot.send_message(message.chat.id, text)



    def get_rank(self, message):
        self.add_rank(message.text)
        bot.send_message(message.chat.id, 'Введите матрицу по инструкции')
        bot.register_next_step_handler(message, self.get_matrix)

    def get_descr(self, message):
        bot.send_message(message.chat.id, '''
    Для начала программа попросит вас ввести ранг матрицы. Ранг 
    матрицы - это количество строчек в квадратной матрице
    (матрице, количество строк и столбцов в которой одинаково).
    Затем необходимо ввести саму матрицу построчно. Это значит, 
    что сначала вводится строчка коэффициентов при переменных 
    через пробел, а затем свободный член уравнения. К примеру,
    для матрицы: 
    
           1 2 3 4 | 5
    А = 6 7 8 9 | 10
           1 2 3 4 | 5
    
    ранг равен 3, а саму матрицу следует вводить таким образом:
    
    1 2 3 4 5 "shift + enter"
    6 7 8 9 10 "shift + enter"
    1 2 3 4 5 "shift + enter"
    ''')

    def minor(self, M, row2del, col2del):
        """Вычеркивание строки и столбца"""
        Mi = []  # результат работы функции
        for r in range(len(M)):
            if row2del != r:
                Mi.append([])
                for c in range(len(M[row2del])):
                    if col2del != c:
                        Mi[-1].append(M[r][c])
        return Mi

    def determinant(self, M):
        """Нахождение определителя матрицы"""
        if len(M) == 1:
            return M[0][0]  # выход из рекурсии
        res = 0
        k = 1
        for c in range(len(M[0])):
            res += k * M[0][c] * self.determinant(self.minor(M, 0, c))
            k *= -1
        return res

    def Kramer_Function(self, A, B, det):
        """Нахождение корней СЛАУ методом Крамера"""
        res_list = []
        for j in range(len(A)):
            A_copy = deepcopy(A)
            for row in range(len(A)):
                for col in range(len(A)):
                    A_copy[col][j] = B[col][0]
            res_list.append(self.determinant(A_copy))
        if det != 0:
            ans = []
            for i in range(len(res_list)):
                ans.append(res_list[i] / det)
            return ans
        else:
            if res_list.count(0) == len(res_list):
                return  'СЛАУ имеет бесконечное множество решений'
            else:
                return  'СЛАУ не имеет решений'


if __name__ == '__main__':
    @bot.message_handler(commands=['start'])
    def start_func(message):
        bot.send_message(message.chat.id, 'Привет! Я помог тебе решить СЛАУ')
        matrix = Matrix()
        matrix.get_descr(message)
        bot.send_message(message.chat.id, 'Введите ранг матрицы')
        bot.register_next_step_handler(message, matrix.get_rank)


    bot.infinity_polling()
