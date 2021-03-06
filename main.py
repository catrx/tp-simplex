import numpy as np


def next_round_r(table):
    m = min(table[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


def next_round(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


def generate_matrix(var, cons):
    tab = np.zeros((cons + 1, var + cons + 2))
    return tab


def find_neg_r(table):
    lc = len(table[0, :])
    m = min(table[:-1, lc - 1])
    if m <= 0:
        n = np.where(table[:-1, lc - 1] == m)[0][0]
    else:
        n = None
    return n


def find_neg(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m <= 0:
        n = np.where(table[lr - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


def loc_piv_r(table):
    total = []
    r = find_neg_r(table)
    row = table[r, :-1]
    m = min(row)
    c = np.where(row == m)[0][0]
    col = table[:-1, c]
    for i, b in zip(col, table[:-1, -1]):
        if i ** 2 > 0 and b / i > 0:
            total.append(b / i)
        else:
            total.append(0)
    element = max(total)
    for t in total:
        if t > 0 and t < element:
            element = t
        else:
            continue

    index = total.index(element)
    return [index, c]


def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i, b in zip(table[:-1, n], table[:-1, -1]):
            if i ** 2 > 0 and b / i > 0:
                total.append(b / i)
            else:
                total.append(0)
        element = max(total)
        for t in total:
            if 0 < t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index, n]


def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i) * -1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq


def convert_min(table):
    table[-1, :-2] = [-1 * i for i in table[-1, :-2]]
    table[-1, -1] = -1 * table[-1, -1]
    return table


def generate_var(table):
    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    v = []
    for i in range(var):
        v.append('x' + str(i + 1))
    return v


def pivot(row, col, table):
    lr = len(table[:, 0])
    lc = len(table[0, :])
    t = np.zeros((lr, lc))
    pr = table[row, :]
    if table[row, col] ** 2 > 0:  # new
        e = 1 / table[row, col]
        r = pr * e
        for i in range(len(table[:, col])):
            k = table[i, :]
            c = table[i, col]
            if list(k) == list(pr):
                continue
            else:
                t[i, :] = list(k - r * c)
        t[row, :] = list(r)
        return t
    else:
        print('Vous ne pouvez pas pivoter cet ??l??ment')


def add_cons(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            empty.append(total)
    if len(empty) > 1:
        return True
    else:
        return False


def constraint(table, eq):
    if add_cons(table):
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - lr - 1
        j = 0
        while j < lr:
            row_check = table[j, :]
            total = 0
            for i in row_check:
                total += float(i ** 2)
            if total == 0:
                row = row_check
                break
            j += 1

        eq = convert(eq)
        i = 0
        while i < len(eq) - 1:
            row[i] = eq[i]
            i += 1
        row[-1] = eq[-1]

        row[var + j] = 1
    else:
        print('Vous ne pouvez pas ajouter d\'autres contraintes')


def add_object(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            empty.append(total)
    if len(empty) == 1:
        return True
    else:
        return False


def obj(table, eq):
    if add_object(table):
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:, 0])
        row = table[lr - 1, :]
        i = 0
        while i < len(eq) - 1:
            row[i] = eq[i] * -1
            i += 1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('Il faut ajouter des contraintes avant que la fonction objectif puisse etre excecute.')


def minz(table, output='summary'):
    table = convert_min(table)

    while next_round_r(table) == True:
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table) == True:
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)

    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[generate_var(table)[i]] = table[loc, -1]
        else:
            val[generate_var(table)[i]] = 0
    val['min'] = table[-1, -1] * -1
    for k, v in val.items():
        val[k] = round(v, 6)
    if output == 'table':
        return table
    else:
        return val


def maxz(table, output='summary'):
    while next_round_r(table):
        table = pivot(loc_piv_r(table)[0], loc_piv_r(table)[1], table)
    while next_round(table):
        table = pivot(loc_piv(table)[0], loc_piv(table)[1], table)

    lc = len(table[0, :])
    lr = len(table[:, 0])
    var = lc - lr - 1
    i = 0
    val = {}
    for i in range(var):
        col = table[:, i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[generate_var(table)[i]] = table[loc, -1]
        else:
            val[generate_var(table)[i]] = 0
    val['max'] = table[-1, -1]
    for k, v in val.items():
        val[k] = round(v, 6)
    if output == 'table':
        return table
    else:
        return val


if __name__ == "__main__":
    m = generate_matrix(2, 2)
    constraint(m, '2,-1,G,10')
    constraint(m, '1,1,L,20')
    obj(m, '5,10,0')
    print("Solution num??ro 1 : ")
    print(maxz(m))

    m = generate_matrix(2, 3)
    constraint(m, '2,-1,G,10')
    constraint(m, '1,1,L,20')
    constraint(m, '8,3,L,85')
    obj(m, '3,7,0')
    print("Solution num??ro 2 : ")
    print(maxz(m))

    m = generate_matrix(2, 4)
    constraint(m, '2,5,G,30')
    constraint(m, '-3,5,G,5')
    constraint(m, '8,3,L,85')
    constraint(m, '-9,7,L,42')
    obj(m, '2,7,0')
    print("Solution num??ro 3 : ")
    print(minz(m))
