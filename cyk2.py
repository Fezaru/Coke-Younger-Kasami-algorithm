import os


def create_cell(first, second):
    res = set()
    if first == set() or second == set():
        return set()
    for f in first:
        for s in second:
            res.add(f+s)  # создаем все возможные комбинации из нетерминалов, например
    return res            # B,E и B,E = B,E  E,B  B,B  E,E


def read_grammar(filename="./grammar.txt"):
    filename = os.path.join(os.curdir, filename)
    with open(filename) as grammar:
        rules = grammar.readlines()
        v_rules = []
        t_rules = []

        for rule in rules:
            left, right = rule.split(" -> ")

            right = right[:-1].split(" | ")  # если в правиле справа например AB | BE
            for ri in right:

                if str.islower(ri):
                    t_rules.append([left, ri])  # отдельно добавляю терминалы, т.к. они по определению продукцией
                    # изменяться не могут

                else:
                    v_rules.append([left, ri])
        return v_rules, t_rules


def read_input(filename="./input.txt"):
    filename = os.path.join(os.curdir, filename)
    res = []
    with open(filename) as inp:
        inputs = inp.readlines()
        for i in inputs:
            res.append(i)
    return res


def cyk_alg(varies, terms, inp):
    length = len(inp)
    var0 = [va[0] for va in varies]
    var1 = [va[1] for va in varies]
    print(var0)
    print(var1)

    # создаем пустую ступенчатую таблицу, заполненную пустыми множествами set()
    table = [[set() for _ in range(length-i)] for i in range(length)]

    # Выводим нетерминал, соответствующий терминалу (заполняем 1 строчку)
    for i in range(length):
        for te in terms:
            if inp[i] == te[1]:  # если символ соответссует терминалу, то выводим соответствубщий нетерминал
                table[0][i].add(te[0])

    # Deal with terminals
    for i in range(1, length):  # начинаем со второй строки, т.к первая уже заполнена
        for j in range(length - i):  # для ступенчатой матрицы, элементов в каждой строке длина - кол-во строк
            for k in range(i):  # начинаем идти сверху вниз к текущей ячейке
                row = create_cell(table[k][j], table[i-k-1][j+k+1])  # на каждой итерации приближения к текущей ячейке
                for ro in row:                                       # мы берем элемент над ней и по диагонали
                    # справа, с каждой итерацией удаляясь по диагонали и приближаясь по вертикали
                    if ro in var1:  # проверяем созданные комбинации, если такая комбинация есть в грамматике,
                        # то добавляем в ячейку нетерминал слева для этой комбинации
                        table[i][j].add(var0[var1.index(ro)])  # сначала получаем индекс элемента, далее по индексу
                        # находим его в левых частях правил грамматики

    return table


def print_grid(table, word):
    length = 7
    word = list(word)

    for w in word:
        print(w, end='')
        for i in range(length - len(w)):
            print(' ', end='')
        print('|', end='')

    print()
    for i in range((len(word) + 1) * length):
        print('-', end='')
    print()

    for line in table:
        for cell in line:
            if cell == set():
                print('__', end='')
                for i in range(length - 2):
                    print(' ', end='')
                print('|', end='')
            else:
                print(*cell, end='')
                for i in range(length - len(cell)):
                    print(' ', end='')
                print('|', end='')
        print()
        for i in range(((len(line) + 1)*length)):
            print('-', end='')
        print()


if __name__ == '__main__':
    v, t = read_grammar()
    r = read_input()[0]
    ta = cyk_alg(v, t, r)
    print(ta)
    print_grid(ta, r)
