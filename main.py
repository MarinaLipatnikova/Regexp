import re
from pprint import pprint
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

wrong_data = []
for contact in contacts_list:
    lastname = [contact[0].split(' ')]
    if len(lastname[0]) > 1:
        contact[0] = lastname[0][0]
        lastname = lastname[0][1:]
        wrong_data.append(lastname)
    else:
        wrong_data.append('')

i = 0
for contact in contacts_list:
    firstname = [contact[1].split(' ')]
    if len(contact[1]) > 1:
        contact[1] = firstname[0][0]
        firstname = firstname[0][1:]
        wrong_data[i] = firstname
        i += 1
    elif contact[1] == '':
        if firstname[0][0] == '':
            contact[1] = wrong_data[i][0]
            wrong_data[i] = wrong_data[i][1:]
        else:
            contact[1] = firstname[0][0]
            firstname = firstname[0][1:]
            wrong_data[i] = firstname
        i += 1
    else:
        i += 1
        break
i = 0
for contact in contacts_list:
    if contact[2] == '':
        if wrong_data[i] != []:
            contact[2] = wrong_data[i][0]
    i += 1

pattern = r"(\+7|8)+(\s)?(\()?(\d{3})(\))?([\s-])?(\s)?(\d{3})([\s-])?(\d{2})([\s-])?(\d+)"
substr = r"+7(\4)\8-\10-\12"
pattern_comp = re.compile(pattern)
pattern2 = r"(\+7|8)+(\s)?(\()?(\d{3})(\))?([\s-])?(\s)?(\d{3})([\s-])?(\d{2})([\s-])?(\d+).(\()?доб\.\s(\d+)(\))?"
substr2 = r"+7(\4)\8-\10-\12 доб.\14"
pattern_comp2 = re.compile(pattern2)

for contact in contacts_list:
    contact[5] = pattern_comp.sub(substr, contact[5])
    contact[5] = pattern_comp2.sub(substr2, contact[5])

contacts_list2 = []
for contact in contacts_list:
    lfname = ' '.join(contact[0:2])
    for contact2 in contacts_list:
        lfname2 = ' '.join(contact2[0:2])
        if lfname == lfname2:
            sname = ''.join(contact[2])
            sname2 = ''.join(contact2[2])
            if sname == sname2 or sname2 == '':
                for i, (el1, el2) in enumerate(zip(contact, contact2)):
                    if el1 == '':
                        contact[i] = el2

for contact in contacts_list:
    lfname = ' '.join(contact[0:2])
    for i, contact2 in enumerate(contacts_list):
        lfname2 = ' '.join(contact2[0:2])
        if lfname == lfname2:
            sname = ''.join(contact[2])
            sname2 = ''.join(contact2[2])
            if sname == sname2 or sname2 == '':
                if len(lfname2) < 2 or sname2 == '':
                    contacts_list.remove(contact2)
                if contact.count('') <= contact2.count(''):
                    if contact not in contacts_list2:
                        contacts_list2.append(contact)

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list2)