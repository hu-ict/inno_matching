import csv

roles = ['AI', 'BIM', 'CSC', 'SD', 'TI']
semester = "feb24"


def findMembers(roles, solution, project):
    members = []
    for role in roles:
        for student in solution[role]:
            if student['project'] == project:
                members.append(student['email'])
    members.sort()
    return members


def findMembersByProject(students, project):
    members = []
    for student in students:
       if student['match'] == project:
            members.append(student['email'])
    members.sort()
    return members


def read_opdrachten(a_filename):
    print('READ OPDRACHTEN', a_filename)
    opdrachten = []
    with open(a_filename, 'r') as csvfile:
        for opdracht in csv.DictReader(csvfile, delimiter=";"):
            new_opdracht = {}
            for role in roles:
                if opdracht[role] == '':
                    new_opdracht[role] = 0
                else:
                    new_opdracht[role] = int(opdracht[role])
            new_opdracht["opdracht"] = opdracht["Opdracht"]
            opdrachten.append(new_opdracht)
    return opdrachten


def read_students(a_filename):
    print('READ STUDENTS:', a_filename)
    students = []
    with open(a_filename, 'r') as csvfile:
        for line in csv.DictReader(csvfile, delimiter=";"):
            student = {}
            student['email'] = line['Email']
            student['role'] = line['Rol']
            student['prio'] = [line['Voorkeur_1'], line['Voorkeur_2'], line['Voorkeur_3']]
            students.append(student)
    return students


def read_teachers(a_filename):
    print('READ TEACHERS:', a_filename)
    teachers = []
    with open(a_filename, 'r') as csvfile:
        for line in csv.DictReader(csvfile, delimiter=";"):
            teacher = {}
            teacher['docent'] = line['Docent']
            teacher['opdracht'] = line['Opdracht']
            teacher['lokaal'] = line['Lokaal']
            teacher['dagdeel'] = line['Dagdeel']
            teacher['opdrachtgever'] = line['Opdrachtgever']
            teachers.append(teacher)
    return teachers


def find_teacher_by_opdracht(teachers, opdracht):
    for teacher in teachers:
        if teacher["opdracht"] == opdracht:
            # print("["+teacher["opdracht"]+"]", "["+opdracht+"]")
            return teacher
    return None


def write_students(a_filename, a_students):
    print('WRITE STUDENTS', a_filename)
    with open(a_filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write('Email;Rol;Voorkeur_1;Voorkeur_2;Voorkeur_3\n')
        for student in a_students:
            csvfile.write(student['email'] + ";" + student['role'] + ";" + student['prio'][0]+ ";" + student['prio'][1]+ ";" + student['prio'][2] + "\n")


def export_solution(semester, students):
    filename = "TICT-VINNO "+semester+" - matching.csv"
    print('SOLUTION EXPORT', filename)
    with open(filename, mode='w', encoding="utf-8") as outfile:
        outfile.write('Email;Rol;Opdracht;Voorkeur;Docent;Lokaal;Dagdeel\n')
        for student in students:
            outfile.write(student['email']+";"+student['role']+";"+student['match']+";"+str(student['ranking'])+";"+student['docent']+";"+student['lokaal']+";"+student['dagdeel']+"\n")


def export_groups_html(semester, opdrachten, students):
    filename = "TICT-VINNO "+semester+" - sheets.html"
    print('SHEETS EXPORT', filename)
    with open(filename, mode='w', encoding="utf-8") as outfile:
        outfile.write('<!DOCTYPE html><html><head><st'
                      'yle>ol {font-size: 20pt;} div {page-break-after: always;} h1 {font-size: 40pt;} h2 {font-size: 20pt;} body {font-family: "Lato Extended","Lato","Helvetica Neue",Helvetica,Arial,sans-serif;}</style></head><body>');
        for opdracht in opdrachten:
            members = findMembersByProject(students, opdracht['opdracht'])
            outfile.write('<div><h1>'+opdracht['opdracht']+'</h1><hr>\n')
            outfile.write('<h2>Opdrachtgever: '+opdracht['opdrachtgever']+'</h2>\n')
            outfile.write('<h2>Teambegeleider: '+opdracht['docent']+'</h2>\n')
            outfile.write('<h2>Lokaal (na 15:30): '+opdracht['lokaal']+'</h2>\n')
            outfile.write('<h2>Studenten:</h2><ol>')
            for member in members:
                outfile.write('<li>'+member+',</li> \n')
            outfile.write('</ol></div>')
        outfile.write('</body></html>')

def write_opdrachten(a_filename, a_opdrachten):
    print('WRITE OPDRACHTEN', a_filename)
    with open(a_filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write('Opdracht;AI;BIM;CSC;SD;TI\n')
        for opdracht in a_opdrachten:
            csvfile.write(opdracht['opdracht'] + ";" + str(opdracht['AI']) + ";" + str(opdracht['BIM']) + ";" + str(opdracht['CSC'])+ ";" + str(opdracht['SD'])+ ";" + str(opdracht['TI']) + "\n")


def bepaal_opdracht_score(studenten):
    projecten = {}
    for student in studenten:
        for prio in range(3):
            if student['prio'][prio] in projecten:
                projecten[student['prio'][prio]] += 3 - prio
            else:
                projecten[student['prio'][prio]] = 3 - prio
    return projecten


# def optimaliseer_samenstelling(geselecteerde_opdrachten, vraag_en_aanbod, sum_roles):
#     print('optimaliseer_samenstelling')
#     for role in roles:
#         print(role)
#         delta_role = vraag_en_aanbod[role]['vraag'] - vraag_en_aanbod[role]['aanbod']
#         if delta_role == 0:
#             #vraag en aanbod in evenwicht
#             continue
#         elif delta_role < 0:
#             #minder aanbod
#             for opdracht in reversed(geselecteerde_opdrachten):
#                 if delta_role == 0:
#                     break
#                 if sum_roles(opdracht) > 5:
#                     if opdracht[role] > 1:
#                         opdracht[role] += -1
#                         delta_role += 1
#         else:
#             #meer aanbod maken
#             for opdracht in geselecteerde_opdrachten:
#                 if delta_role == 0:
#                     break
#                 if sum_roles(opdracht) < 6:
#                     if opdracht[role] > 0:
#                         opdracht[role] += 1
#                         delta_role += -1
#
#     print('optimaliseer_samenstelling einde')
#
#     return geselecteerde_opdrachten


def read_students_old():
    filename = "TICT-VINNO sep23 - studenten.csv"
    print('LEES STUDENTEN', filename)
    preferences = []
    with open(filename, 'r') as csvfile:
        count = 0
        for line in csv.DictReader(csvfile, delimiter=";"):
            count += 1
            student = {}
            student['Naam'] = str.lower(line['email'].strip())
            rol = line['afstudeerrichting']
            if rol not in roles:
                continue
            student['Rol'] = rol
            student['Id'] = line['ID']
#            student['Datum'] = line['Tijdstempel']
            student['Prio'] = []
            if line['voorkeur_1'][-1] == ';':
                student['Prio'].append(line['voorkeur_1'][0:-1])
            else:
                student['Prio'].append(line['voorkeur_1'])
            if line['voorkeur_2'][-1] == ';':
                student['Prio'].append(line['voorkeur_2'][0:-1])
            else:
                student['Prio'].append(line['voorkeur_2'])
            if line['voorkeur_3'][-1] == ';':
                student['Prio'].append(line['voorkeur_3'][0:-1])
            else:
                student['Prio'].append(line['voorkeur_3'])
            # find a student for duplicate item
            for preference in preferences:
                if student['Naam'] == preference['Naam']:
                    preferences.remove(preference)
                    break;
            preferences.append(student)
        print('Inzendingen', count, 'ongefilterd')
    return preferences

def print_result(voorkeurAantal, aantal_studenten):
    print("Matching result")
    print('1ste   voorkeur {perc:2.0f} % {aantal:3}'.format(aantal=voorkeurAantal['prio1'],
                                                            perc=voorkeurAantal['prio1'] / aantal_studenten * 100))
    print('2de    voorkeur {perc:2.0f} % {aantal:3}'.format(aantal=voorkeurAantal['prio2'],
                                                            perc=voorkeurAantal['prio2'] / aantal_studenten * 100))
    print('3de    voorkeur {perc:2.0f} % {aantal:3}'.format(aantal=voorkeurAantal['prio3'],
                                                            perc=voorkeurAantal['prio3'] / aantal_studenten * 100))
    print('Totaal voorkeur {perc:2.0f} %'.format(
        perc=(voorkeurAantal['prio1'] + voorkeurAantal['prio2'] + voorkeurAantal['prio3']) / aantal_studenten * 100))
    fit = voorkeurAantal['prio1'] * 3 + voorkeurAantal['prio2'] * 2 + voorkeurAantal['prio1'] * 1
    print('Totaal fit:', fit)