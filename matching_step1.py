import csv
import operator

from matching_lib import roles
from matching_lib import bepaal_opdracht_score

from matching_lib import write_students

def readStudentPreference():
    filename = "TICT-VINNO feb24 - studenten.csv"
    print('STUDENT IMPORT', filename)
    preferences = []
    with open(filename, 'r') as csvfile:
        count = 0
        for line in csv.DictReader(csvfile, delimiter=";"):
            count += 1
            student = {}
            student['Naam'] = str.lower(line['Email'].strip())
            rol = line['Rol']
            if rol not in roles:
                continue
            student['Rol'] = rol
            # student['Id'] = line['ID']
#            student['Datum'] = line['Tijdstempel']
            student['Prio'] = []
            if line['Voorkeur_1'][-1] == ';':
                student['Prio'].append(line['Voorkeur_1'][0:-1])
            else:
                student['Prio'].append(line['Voorkeur_1'])
            if line['Voorkeur_2'][-1] == ';':
                student['Prio'].append(line['Voorkeur_2'][0:-1])
            else:
                student['Prio'].append(line['Voorkeur_2'])
            if line['Voorkeur_3'][-1] == ';':
                student['Prio'].append(line['Voorkeur_3'][0:-1])
            else:
                student['Prio'].append(line['Voorkeur_3'])
            # find a student for duplicate item
            for preference in preferences:
                if student['Naam'] == preference['Naam']:
                    preferences.remove(preference)
                    break;
            preferences.append(student)
        print('Inzendingen', count, 'ongefilterd')
    return preferences


def main():
    role_count = {}
    for role in roles:
        role_count[role] = 0

    preferences = readStudentPreference()

    print('Inzendingen',len(preferences))
    print("Afstudeerrichtingen")
    for student in preferences:
        role_count[student['Rol']] += 1
    for role in roles:
        print('{sleutel:3}: {waarde:4}'.format(sleutel=role, waarde=role_count[role]))
    write_students(preferences, "TICT-VINNO feb24 - studenten gefilterd.csv")
    opdrachten = bepaal_opdracht_score(preferences)
    sorted_opdracht_score = sorted(opdrachten.items(), key=operator.itemgetter(1), reverse=True)
    count = 1
    for tupel_x in sorted_opdracht_score:
        print('{count:2} - {waarde:3}: Opdracht: {sleutel:50}'.format(count=count, sleutel=tupel_x[0], waarde=tupel_x[1]))
        count += 1

if __name__ == "__main__":
    main()