"""
Netology. Modules. Lesson 2.

Ваша задача: починить адресную книгу, используя регулярные выражения.
Структура данных будет всегда:
lastname,firstname,surname,organization,position,phone,email
Предполагается, что телефон и e-mail у человека может быть только один.


- поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
- В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
- привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер,
- формат будет такой: +7(999)999-99-99 доб.9999;
- объединить все дублирующиеся записи о человеке в одну.

"""

import csv
import re

#  Шаблон для номера телефона phone_number_pattern и внесения изменений phone_sub
phone_number_pattern = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*"
phone_sub = r"+7(\2)-\3-\4-\5 \6\7"


#  функции обработки данных.
def name_info(contact_list):
    """Обработка имени, номера телефона.
    Если ФИО написаны через пробел в одно поле, берем из списка первые три занчения,
    преобразуем в строку и разбиваем в список по пробелам
    """
    temp = list()
    for i in contact_list:
        name = ' '.join(i[:3]).split(' ')
        #  получили список ФИО
        name_info = [name[0], name[1], name[2], i[3], i[4]]
        #  составили ФИО раздельно по полям и прочую информацию о человеке
        pnone_number = [re.sub(phone_number_pattern, phone_sub, i[5]), i[6]]
        #  составили номер телефона в установленной форме + добавочный
        result = name_info + pnone_number
        temp.append(result)
    return delete_repeat(temp)


def delete_repeat(contacts):
    """Найходим и удаляем повторы.
    Перебирая данные сравниваем каждого с последующими. Если имя и фамилия совпадают то
    логически суммируем их данные по позициям и заносим во второй из них.
    Позицию заносим в список для удаления contacts.remove и после перебора удаляем первого из инх из списка.
    """
    repeat_for_remove = []
    for i in range(len(contacts)-1):
        for j in range(i+1, len(contacts)):
            if contacts[i][:2] == contacts[j][:2]:
                contacts[j][2] = contacts[i][2] or contacts[j][2]
                contacts[j][3] = contacts[i][3] or contacts[j][3]
                contacts[j][4] = contacts[i][4] or contacts[j][4]
                contacts[j][5] = contacts[i][5] or contacts[j][5]
                contacts[j][6] = contacts[i][6] or contacts[j][6]

                repeat_for_remove.append(contacts[i])
    for i in repeat_for_remove:
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
