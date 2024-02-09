# Объявляем глобальные переменные:
# для матчей
HOME = 0
SCORE = 1
GUEST = 2
DATE = 3
# для параметров рейтинга
MATCHES = 0
WINS = 1
DRAWS = 2
LOSES = 3
TEAM_GOALS = 4
OP_GOALS = 5
SCORES = 6
# для клубов при расставлении мест
PLACE, NAME = 0, 0
N_S, STAT = 1, 1


# Функция получает таблицу матчей и запрос,
# выводит все матчи, сыгранные запрошенным клубом на домашней или гостевой стороне
def team_match(table, request):
    for match in table:
        if match[HOME] == request or match[GUEST] == request:
            print(match)


# Функция получает таблицу матчей и запрос,
# выводит все матчи, сыгранные в запрошенный день
def date_match(table, request):
    for match in table:
        if match[DATE] == request:
            print(match)


# Функция получает таблицу матчей и словарь клубов,
# в зависимости от данных в таблице меняет параметры словаря для каждого клуба
def team_ranking(table, dict, rules):
    for match in table:
        for team in dict:
            # для домашней стороны
            if team == match[HOME]:
                dict[match[HOME]][MATCHES] += 1
                if match[SCORE][HOME] > match[SCORE][GUEST]:
                    dict[match[HOME]][WINS] += 1
                    dict[match[HOME]][SCORES] += 3
                elif match[SCORE][HOME] == match[SCORE][GUEST]:
                    dict[match[HOME]][DRAWS] += 1
                    dict[match[HOME]][SCORES] += 1
                elif match[SCORE][HOME] < match[SCORE][GUEST]:
                    dict[match[HOME]][LOSES] += 1
                dict[match[HOME]][TEAM_GOALS] += int(match[SCORE][HOME])
                dict[match[HOME]][OP_GOALS] += int(match[SCORE][GUEST])
            # для гостевой стороны
            elif team == match[GUEST]:
                dict[match[GUEST]][MATCHES] += 1
                if match[SCORE][GUEST] > match[SCORE][HOME]:
                    dict[match[GUEST]][WINS] += 1
                    dict[match[GUEST]][SCORES] += 3
                elif match[SCORE][GUEST] == match[SCORE][HOME]:
                    dict[match[GUEST]][DRAWS] += 1
                    dict[match[GUEST]][SCORES] += 1
                elif match[SCORE][GUEST] < match[SCORE][HOME]:
                    dict[match[GUEST]][LOSES] += 1
                dict[match[GUEST]][TEAM_GOALS] += int(match[SCORE][GUEST])
                dict[match[GUEST]][OP_GOALS] += int(match[SCORE][HOME])
    # Создаём список из словаря и работаем с местами в турнирной таблице
    list_dict = list(dict.items())
    list_dict.sort(key=lambda team: team[1][SCORES], reverse=True)
    # в новый список добавляем место для каждого клуба в зависимости от его очков
    # при равенстве очков считаем, что клубы на одинаковом месте
    last = 0
    last_score = 0
    new = 1
    new_list = []
    for team in list_dict:
        if last_score == team[STAT][SCORES]:
            new_list.append([last, team])
        else:
            new_list.append([new, team])
            last = new
        new += 1
        last_score = team[STAT][SCORES]
    # Начинаем работу с ничьими
    # находя клубы с одинаковыми местами делаем срезы и отдаём их функциям-правилам, в зависимости от цифр в файле rules
    # с помощью переменной cont (в функциях - proceeding), которую мы получаем из функций-правил, двигаемся по ним
    # цикл продолжается пока не закончится проверка всех срезов
    # во избежание бесконечности цикла while начинаем цикл for с переменной begin_cycle равной последнему элементу среза
    # также создаём переменные alarm для начала среза и его продолжения и total_alarm для проверки присутствия ничьих
    start = 0
    finish = 0
    alarm = 0
    begin_cycle = 0
    total_alarm = 0
    cont = 0
    while total_alarm == 0:
        total_alarm = 1
        alarm = 0
        for j in range(begin_cycle, (len(new_list) - 1)):
            if new_list[j][PLACE] == new_list[j + 1][PLACE]:
                total_alarm = 0
                if alarm == 0:
                    start = j
                    alarm = 1
                if j == len(new_list)-2:
                    finish = j + 1
                    begin_cycle = finish + 1
                    for rule in rules:
                        if str(rule) == '1.1':
                            cont = rule_1_1(rule_1(new_list[start:finish + 1], table))[1]
                        if str(rule) == '1.2':
                            cont = rule_1_2(rule_1(new_list[start:finish + 1], table))[1]
                        if str(rule) == '1.3':
                            cont = rule_1_3(rule_1(new_list[start:finish + 1], table))[1]
                        if str(rule) == '2':
                            cont = rule_2(rule_1(new_list[start:finish + 1], table))[1]
                        if str(rule) == '3':
                            cont = rule_3(new_list[start:finish + 1])[1]
                        if str(rule) == '4':
                            cont = rule_4(new_list[start:finish + 1])[1]
                        if str(rule) == '5':
                            cont = rule_5(new_list[start:finish + 1])[1]
                        if cont == 0:
                            break
            elif new_list[j][PLACE] == new_list[j - 1][PLACE]:
                finish = j
                begin_cycle = finish + 1
                for rule in rules:
                    if str(rule) == '1.1':
                        cont = rule_1_1(rule_1(new_list[start:finish + 1], table))[1]
                    if str(rule) == '1.2':
                        cont = rule_1_2(rule_1(new_list[start:finish + 1], table))[1]
                    if str(rule) == '1.3':
                        cont = rule_1_3(rule_1(new_list[start:finish + 1], table))[1]
                    if str(rule) == '2':
                        cont = rule_2(rule_1(new_list[start:finish + 1], table))[1]
                    if str(rule) == '3':
                        cont = rule_3(new_list[start:finish + 1])[1]
                    if str(rule) == '4':
                        cont = rule_4(new_list[start:finish + 1])[1]
                    if str(rule) == '5':
                        cont = rule_5(new_list[start:finish + 1])[1]
                    if str(cont) == '0':
                        break
                break
    # После работ с функциями-правилами элементы нужно упорядочить
    new_list.sort(key=lambda team: team[PLACE])
    # Создаём выравненную таблицу, для этого откладываем под каждую цифру в параметрах нужное кол-во пробелов
    for team in new_list:
        for j in range(len(team[N_S][STAT])):
            if len(str(team[N_S][STAT][j])) == 1:
                team[N_S][STAT][j] = ' ' + str(team[1][1][j])
    # Создаём верхнюю строку обозначений
    print(' ' * 4, 'Club', ' ' * 11, ' M', ' W', ' D', ' L', 'TG', 'OG', ' S')
    # Создаём пробелы в зависимости от длины мест и длины названия клуба, в конце добавляем отформатированные параметры
    for team in new_list:
        print(str(team[PLACE]) + '.', ' ' * (len(str(team[PLACE])) - (2 * (team[PLACE] // 10))),
              team[N_S][NAME], ' ' * (15 - len(team[N_S][NAME])),
              *team[N_S][STAT])


# Для правил head-to-head создаём словарь с изменяемыми параметрами в зависимости только от игр клубов друг с другом
# сохраняем старую статистику клубов и возвращаем её в конце работы с каждым правилом группы head-to-head
# таким образом, переменная food_4_head2head_rules будет содержать измененный список и старую статистику
def rule_1(our_problem_list, table):
    problem_teams = []
    old_stat = []
    for team in our_problem_list:
        current = [team[N_S][NAME], [0, 0, 0, 0, 0, 0, 0]]
        for j in range(7):
            current[STAT][j] = team[N_S][STAT][j]
        old_stat.append(current)
        for j in range(7):
            team[N_S][STAT][j] = 0
        problem_teams.append(team[N_S][NAME])
    for club1 in problem_teams:
        for club2 in problem_teams:
            for match in table:
                for team in our_problem_list:
                    if club1 == match[HOME] and club2 == match[GUEST]:
                        # для домашней стороны
                        if team[N_S][NAME] == match[HOME]:
                            if match[SCORE][HOME] > match[SCORE][GUEST]:
                                team[N_S][STAT][WINS] += 1
                                team[N_S][STAT][SCORES] += 3
                            elif match[SCORE][HOME] == match[SCORE][GUEST]:
                                team[N_S][STAT][SCORES] += 1
                            team[N_S][STAT][TEAM_GOALS] += int(match[SCORE][HOME])
                            team[N_S][STAT][OP_GOALS] += int(match[SCORE][GUEST])
                            # для гостевой стороны
                        elif team == match[GUEST]:
                            if match[SCORE][GUEST] > match[SCORE][HOME]:
                                team[N_S][STAT][WINS] += 1
                                team[N_S][STAT][SCORES] += 3
                            elif match[SCORE][GUEST] == match[SCORE][HOME]:
                                team[N_S][STAT][SCORES] += 1
                            team[N_S][STAT][TEAM_GOALS] += int(match[SCORE][GUEST])
                            team[N_S][STAT][OP_GOALS] += int(match[SCORE][HOME])
    food_4_head2head_rules = [our_problem_list, old_stat]
    return food_4_head2head_rules


# Функции rule_1_1, rule_1_2, rule_1_3 и rule_2 работают в связке с rule_1
# получая food, они отделяют список и старую статистику, при нахождении неразрешимой ничьи в списке, proceeding = 1
# таким образом our_problem_list становится равен списку из него и proceeding на 1 месте, его забирает team_ranking
def rule_1_1(food):
    our_problem_list = food[0]
    old_stat = food[1]
    our_problem_list.sort(key=lambda team: team[N_S][STAT][SCORES], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][SCORES]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][SCORES]
    for team1 in our_problem_list:
        for team2 in old_stat:
            if team1[N_S][NAME] == team2[NAME]:
                for j in range(7):
                    team1[N_S][STAT][j] = team2[STAT][j]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


def rule_1_2(food):
    our_problem_list = food[0]
    old_stat = food[1]
    our_problem_list.sort(key=lambda team: team[N_S][STAT][WINS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][WINS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][WINS]
    for team1 in our_problem_list:
        for team2 in old_stat:
            if team1[N_S][NAME] == team2[NAME]:
                for j in range(7):
                    team1[N_S][STAT][j] = team2[STAT][j]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


def rule_1_3(food):
    our_problem_list = food[0]
    old_stat = food[1]
    our_problem_list.sort(key=lambda team: team[N_S][STAT][TEAM_GOALS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][TEAM_GOALS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][TEAM_GOALS]
    for team1 in our_problem_list:
        for team2 in old_stat:
            if team1[N_S][NAME] == team2[NAME]:
                for j in range(7):
                    team1[N_S][STAT][j] = team2[STAT][j]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


def rule_2(food):
    our_problem_list = food[0]
    old_stat = food[1]
    our_problem_list.sort(key=lambda team: team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS]
    for team1 in our_problem_list:
        for team2 in old_stat:
            if team1[N_S][NAME] == team2[NAME]:
                for j in range(7):
                    team1[N_S][STAT][j] = team2[STAT][j]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


# Функции rule_3, rule_4, rule_5 работают самостоятельно, используя общую статистику, полученную в team_ranking
def rule_3(our_problem_list):
    our_problem_list.sort(key=lambda team: team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][TEAM_GOALS]-team[N_S][STAT][OP_GOALS]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


def rule_4(our_problem_list):
    our_problem_list.sort(key=lambda team: team[N_S][STAT][TEAM_GOALS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][TEAM_GOALS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][TEAM_GOALS]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list


def rule_5(our_problem_list):
    our_problem_list.sort(key=lambda team: team[N_S][STAT][WINS], reverse=True)
    last = our_problem_list[0][PLACE]
    last_score = 100
    new = last
    proceeding = 0
    for team in our_problem_list:
        if last_score == team[N_S][STAT][WINS]:
            team[PLACE] = last
            proceeding = 1
        else:
            team[PLACE] = new
            last = new
        new += 1
        last_score = team[N_S][STAT][WINS]
    our_problem_list = [our_problem_list, proceeding]
    return our_problem_list
# О назначении каждого правила можно узнать в файлах rules


# Создаём главный модуль для работы с пользователем, в зависимости от его выбора открываем нужные файлы на первом уровне
print()
print("Перед вами проект, содержащий данные о матчах пяти различных футбольных лиг, сыгранных в 2018/19")
print("Старое доброе время когда ещё можно было наблюдать игры на полных стадионах...")
print("Have fun!")
print()
choice = 1
while (4 > choice > 0) or choice == 9:
    print("Введите 1, чтобы открыть премьер-лигу Англии")
    print("Введите 2, чтобы открыть премьер-лигу России")
    print("Введите 3, чтобы открыть Бундеслигу")
    print("Введите 4, чтобы открыть Чемпионат Италии, Серия А")
    print("Введите 5, чтобы открыть Чемпионат Испании, Ла Лига")
    print("Введите любое другое число или нецелочисленное значение, чтобы завершить работу программы")
    try:
        choice = int(input())
    except ValueError:
        break
    if choice <= 0 or choice >= 6:
        break
    file = open(f'files/tournament_{choice}', 'r', encoding='utf-8')
    file_rules = open(f'files/rules_{choice}', 'r', encoding='utf-8')
    content = file.readlines()
    content_rules = file_rules.readlines()
    # Убираем ненужные туры
    for elem in content:
        if elem[1] == '-' or elem[2] == '-':
            content.remove(elem)
    # Собираем содержимое в список списков
    my_table = []
    current = []
    count = 0
    elem = ''
    for i in range(len(content)):
        elem = content[i][:len(content[i]) - 1]
        current.append(elem)
        count += 1
        if count == 4:
            my_table.append(current)
            count = 0
            current = []
    # Создаём список правил
    my_rules = []
    for elem in content_rules:
        if int(elem[0]) == 1:
            my_rules.append(elem[0:3])
        else:
            my_rules.append(elem[0])
    # Создаем словарь всех клубов, параметры обнуляем
    my_dict = {my_table[0][0]: [0, 0, 0, 0, 0, 0, 0]}
    button = 0
    for event in my_table:
        for club in my_dict:
            if club == event[HOME]:
                button = 1
        if button == 0:
            my_dict[event[HOME]] = [0, 0, 0, 0, 0, 0, 0]
        button = 0
    # На втором уровне, в зависимости от выбора пользователя отдаём данные функциям
    choice = 1
    while 4 > choice > 0:
        print("Введите 1, чтобы узнать обо всех матчах запрошенного клуба")
        print("Введите 2, чтобы узнать обо всех матчах сыгранных в запрошенный день")
        print("Введите 3, чтобы получить полную турнирную таблицу")
        print("Введите 9, чтобы вернуться к выбору лиги")
        print("Введите любое другое число или нецелочисленное значение, чтобы завершить работу программы")
        try:
            choice = int(input())
        except ValueError:
            choice = 0
        if choice == 1:
            my_request = input("Введите название клуба: ")
            team_match(my_table, my_request)
            print()
        if choice == 2:
            my_request = input("Введите дату (ДД.ММ.ГГГГ): ")
            date_match(my_table, my_request)
            print()
        if choice == 3:
            team_ranking(my_table, my_dict, my_rules)
            print()
        if choice == 9:
            break
