import csv
import re

#  Шаблон для номера телефона phone_number_pattern и внесения изменений phone_substitution
phone_number_pattern = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*"
phone_substitution = r"+7(\2)-\3-\4-\5 \6\7"


#  обработка данных
def name_info(contact_list):
    """ Если ФИО написаны через пробел в одно поле, возьмем первые три значения,
        преобразуем в строку и разбиваем в список по пробелам
    """
    temp_list = list()
    for i in contact_list:
        name = ' '.join(i[:3]).split(' ')
        #  получили список ФИО
        name_info = [name[0], name[1], name[2], i[3], i[4]]
        #  составили ФИО раздельно по полям и остальную инфу о человеке
        pnone_number = [re.sub(phone_number_pattern, phone_substitution, i[5]), i[6]]
        #  составили номер телефона в правильной форме + добавочный
        result = name_info + pnone_number
        temp_list.append(result)
    return delete_repeat(temp_list)


def delete_repeat(contacts):
    """Найходим и удаляем повторы.
    Если имя и фамилия совпадают, то суммируем их данные по позициям.
    Позицию заносим в список для удаления contacts.remove и после перебора удаляем первого из их из списка.
    """
    remove_list = []
    for i in range(len(contacts)-1):
        for j in range(i+1, len(contacts)):
            if contacts[i][:2] == contacts[j][:2]:
                contacts[j][2] = contacts[i][2] or contacts[j][2]
                contacts[j][3] = contacts[i][3] or contacts[j][3]
                contacts[j][4] = contacts[i][4] or contacts[j][4]
                contacts[j][5] = contacts[i][5] or contacts[j][5]
                contacts[j][6] = contacts[i][6] or contacts[j][6]

                remove_list.append(contacts[i])
    for i in remove_list:
        contacts.remove(i)
    return (contacts)


#  Получаем данные из файла, вызываем функцию обработки имени, телефона и заносим в список contact_list
with open("files/phonebook_raw.csv", encoding="UTF-8") as f:
    rows = csv.reader(f, delimiter=",")
    contact_list = list(rows)


#  Записываем полученный список в файл
with open("files/phonebook_out.csv", "w", newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(name_info(contact_list))
