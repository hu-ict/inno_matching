import csv
import operator
from matching_lib import roles, read_opdrachten
from matching_lib import bepaal_opdracht_score
from matching_lib import read_students

perTeam = 5.5


def bepaal_opdracht_score(studenten, role):
    opdrachten = {}
    for student in studenten:
        if student["role"] == role or role == "":
            for prio in range(3):
                if student['prio'][prio] in opdrachten:
                    opdrachten[student['prio'][prio]] += 3 - prio
                else:
                    opdrachten[student['prio'][prio]] = 3 - prio
    return opdrachten


def selecteer_opdrachten(opdrachten, studenten):
    print('selecteer_opdrachten')
    opdracht_score = bepaal_opdracht_score(studenten, "")
    print('Opdrachten gekozen', len(opdracht_score))
    aantal_projecten = int(len(studenten) / perTeam)
    print('Opdrachten top', aantal_projecten)

    sorted_opdracht_score = sorted(opdracht_score.items(), key=operator.itemgetter(1), reverse=True)
    project_aantal = 0
    for tupel_x in sorted_opdracht_score:
        project_aantal += 1

    geselecteerde_opdrachten = []
    for geselecteerde_opdracht in sorted_opdracht_score[:aantal_projecten]:
        for opdracht in opdrachten:
            if geselecteerde_opdracht[0] == opdracht['opdracht']:
                geselecteerde_opdrachten.append(opdracht)
    print('geselecteerde_opdrachten', len(geselecteerde_opdrachten))
    return geselecteerde_opdrachten


def schrijf_opdrachten(opdrachten, filename):
    print('PROJECTEN EXPORT', filename)
    print('Aantal opdrachten', len(opdrachten))
    for opdracht in opdrachten:
        totaal = 0
        for role in roles:
            totaal += opdracht[role]
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write('Opdracht;AI;BIM;CSC;SD;TI\n')
        for opdracht in opdrachten:
            csvfile.write(opdracht['opdracht'])
            for role in roles:
                csvfile.write(";" + str(opdracht[role]))
            csvfile.write("\n")


def bepaal_vraag_en_aanbod(opdrachten, studenten):
    print('bepaal_vraag_en_aanbod')
    vraag_en_aanbod = {'totaal': {'vraag': 0, 'aanbod': 0}}
    for role in roles:
        vraag_en_aanbod[role] = {'vraag': 0, 'aanbod': 0}

    for role in roles:
        for opdracht in opdrachten:
            # print(opdracht)
            vraag_en_aanbod[role]['aanbod'] += int(opdracht[role])
            vraag_en_aanbod['totaal']['aanbod'] += int(opdracht[role])
    for student in studenten:
        vraag_en_aanbod[student['role']]['vraag'] += 1
        vraag_en_aanbod['totaal']['vraag'] += 1
#    for role in roles:
#        print(role+' student vraag: ', vraag_en_aanbod[role]['vraag'], 'project aanbod:', vraag_en_aanbod[role]['aanbod'])
    print('Totaal student vraag: ', vraag_en_aanbod['totaal']['vraag'],'Totaal project aanbod:',vraag_en_aanbod['totaal']['aanbod'])
    for role in roles:
        print("{role:3} - vraag {vraag:2} - aanbod {aanbod:2}".format(role=role, vraag=vraag_en_aanbod[role]['vraag'],aanbod=vraag_en_aanbod[role]['aanbod']))
#    return vraag_en_aanbod


def sum_roles(opdracht):
    sum = 0
    for role_1 in roles:
        sum += opdracht[role_1]
    return sum

def report_students(a_studenten):
    print('Inzendingen',len(a_studenten))
    print("Afstudeerrichtingen")
    role_count = {}
    for role in roles:
        role_count[role] = 0
    for student in a_studenten:
        role_count[student['role']] += 1
    for role in roles:
        print('{sleutel:3}: {waarde:4}'.format(sleutel=role, waarde=role_count[role]))

def report_opdrachten(a_opdrachten, role):
    print("Opdracht populariteit", role)
    sorted_opdracht_score = sorted(a_opdrachten.items(), key=operator.itemgetter(1), reverse=True)
    count = 1
    for tupel_x in sorted_opdracht_score:
        print('{count:2} - {waarde:3}: Opdracht: {sleutel:50}'.format(count=count, sleutel=tupel_x[0], waarde=tupel_x[1]))
        count += 1

def main():
    studenten = read_students("TICT-VINNO feb24 - studenten.csv")
    report_students(studenten)
    opdrachten = bepaal_opdracht_score(studenten, "")
    report_opdrachten(opdrachten, "")
    for role in roles:
        opdrachten = bepaal_opdracht_score(studenten, role)
        report_opdrachten(opdrachten, role)

    opdrachten = read_opdrachten("TICT-VINNO feb24 - opdrachten.csv")
    vraag_en_aanbod = bepaal_vraag_en_aanbod(opdrachten, studenten)
    print('Studenten', len(studenten))

    print('Opdrachten', len(opdrachten))
    # schrijf_opdrachten(opdrachten, "TICT-VINNO feb24 - opdrachten.csv")

if __name__ == "__main__":
    main()