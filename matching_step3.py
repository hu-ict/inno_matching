import json
import random
import csv
from matching_lib import roles, read_students, print_result, read_opdrachten, read_teachers, find_teacher_by_opdracht, \
    export_solution, semester, findMembers, export_groups_html


def maak_project_plekken(opdrachten):
    project_spaces = {}
    for role in roles:
        project_spaces[role] = []
    for opdracht in opdrachten:
        for role in roles:
            for aantal in range(int(opdracht[role])):
                project_spaces[role].append({'opdracht': opdracht['opdracht'], 'student': ''})
    return project_spaces

def randomSolution(project_spaces, studenten):
    studenten_kopie = studenten.copy()

    # bepalen team plaatsen

    projects = []
    index = 0
    for student in studenten:
        projects.append(project_spaces[index]['opdracht'])
        if index >= len(project_spaces)-1:
            index = 0
        else:
            index += 1

    # random toewijzen team plaatsen
    solution = []
    for i in range(len(studenten)):
        randomStudent = studenten_kopie[random.randint(0, len(studenten_kopie) - 1)]
        randomProject = projects[random.randint(0, len(projects) - 1)]
        student = {"email": randomStudent['email'], "project": randomProject}
        solution.append(student)
        studenten_kopie.remove(randomStudent)
        projects.remove(randomProject)
    return solution

def fitenessForStudent(tsp, student):
    for voorkeur in tsp:
        if voorkeur['email'] == student['email']:
            if voorkeur['prio'].count(student['project']) > 0:
                if voorkeur['prio'].index(student['project']) == 0:
                    # eerste voorkeur
                    return 10
                elif voorkeur['prio'].index(student['project']) == 1:
                    # tweede voorkeur
                    return 2
                else:
                    # derde voorkeur
                    return 1
            else:
                # geen voorkeur
                return 0
    return 0


def fitness(tsp, solution):
    fitness = 0
    for student in solution:
        fitness += fitenessForStudent(tsp, student)
    return fitness


def copySolution(solution):
    neighbour = []
    for row in solution:
        newRow = {'email': row['email'], 'project': row['project']}
        neighbour.append(newRow)
    return neighbour


def getNeighbours(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = copySolution(solution)
#            print('--> solution:  ', solution)
#            print('--> neighbour: ', neighbour)
            temp = neighbour[i]['project']
            neighbour[i]['project'] = neighbour[j]['project']
            neighbour[j]['project'] = temp
            neighbours.append(neighbour)
#            print('---> solution: ', solution)
#            print('-> neighbour:', neighbour)
    return neighbours

def getBestNeighbour(tsp, neighbours):
    bestFitness = fitness(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentFitness = fitness(tsp, neighbour)
        if currentFitness > bestFitness:
            bestFitness = currentFitness
            bestNeighbour = neighbour
    return bestNeighbour, bestFitness


def export_canvas(opdrachten, solution):
    filename = 'TICT-VINNO feb24 - canvas.csv'
    print('SOLUTION CANVAS', filename)
    with open(filename, mode='w', encoding="utf-8") as outfile:
        outfile.write('canvas_user_id ,user_id,login_id,group_name\n')
        for opdracht in opdrachten:
            members = findMembers(roles, solution, opdracht['opdracht'])
            for member in members:
                outfile.write(',,'+member+','+opdracht['opdracht']+', \n')


def print_voorkeur(voorkeuren, solution):
    voorkeurAantal = {'prio1': 0, 'prio2': 0, 'prio3': 0}
    aantal_studenten = 0
    for role in roles:
        aantal_studenten += len(solution[role])

    for role in roles:
        for student in solution[role]:
            student["ranking"] = 0
            for voorkeur in voorkeuren[role]:
                if voorkeur['email'] == student['email']:
                    if voorkeur['prio'][0] == student['project']:
                        voorkeurAantal['prio1'] += 1;
                        student["ranking"] = 1
                        break
                    if voorkeur['prio'][1] == student['project']:
                        voorkeurAantal['prio2'] += 1;
                        student["ranking"] = 2
                        break
                    if voorkeur['prio'][2] == student['project']:
                        voorkeurAantal['prio3'] += 1;
                        student["ranking"] = 3
                        break
    # for role in roles:
    #     for student in solution[role]:
    #         print(student)
    print_result(voorkeurAantal, aantal_studenten)

def hillClimbing(project_spaces, studenten):
    #Wordt uitgevoerd per role
    project_spaces_copy = project_spaces.copy()
    currentSolution = randomSolution(project_spaces_copy, studenten)
    currentFitness = fitness(studenten, currentSolution)

    neighbours = getNeighbours(currentSolution)
    bestNeighbour, bestNeighbourFitness = getBestNeighbour(studenten, neighbours)

    while bestNeighbourFitness > currentFitness:
        currentSolution = bestNeighbour
        currentFitness = bestNeighbourFitness
        neighbours = getNeighbours(currentSolution)
        bestNeighbour, bestNeighbourFitness = getBestNeighbour(studenten, neighbours)
    return currentSolution, currentFitness

def main():
    opdrachten = read_opdrachten("TICT-VINNO feb24 - opdrachten.csv")
    studenten = read_students("TICT-VINNO feb24 - studenten.csv")
    teachers = read_teachers("TICT-VINNO feb24 - docenten.csv")
    for opdracht in opdrachten:
        teacher = find_teacher_by_opdracht(teachers, opdracht[ "opdracht"])
        opdracht["docent"] = teacher["docent"]
        opdracht["lokaal"] = teacher["lokaal"]
        opdracht["dagdeel"] = teacher["dagdeel"]
        opdracht["opdrachtgever"] = teacher["opdrachtgever"]

    project_spaces = maak_project_plekken(opdrachten)
#    for role in roles:
#        for project in project_spaces[role]:
#            print(role,project)
    finalSolution = {}
    preferences = {}
    for role in roles:
        finalSolution[role] = []
        preferences[role] = []
    for student in studenten:
        preferences[student['role']].append(student)

    for role in roles:
        if len(project_spaces[role]) == 0:
            continue

        project_spaces_copy = project_spaces[role].copy()
        finalSolution[role] = randomSolution(project_spaces_copy, preferences[role])

        finalFitness = 0;
        #
        for attempt in range(10):
            currentSolution, currentFitness = hillClimbing(project_spaces[role], preferences[role])
            if finalFitness < currentFitness:
                finalFitness = currentFitness
                finalSolution[role] = currentSolution
#        print(role, 'finalFitness:', finalFitness)
#     look_up_opdrachten = {}
#     for opdracht in opdrachten:
#         look_up_opdrachten[opdracht['Opdracht']] = (opdracht['Docent'], opdracht['Lokaal'])
#     for role in roles:
#         for student in finalSolution[role]:
#             student['Docent'], student['Lokaal'] = look_up_opdrachten[student['Project']]

    print_voorkeur(preferences, finalSolution)

    with open("solution.json", 'w') as f:
        dict_result = finalSolution
        json.dump(dict_result, f, indent=2)
    export_canvas(opdrachten, finalSolution)
    # export_html(opdrachten, finalSolution)
    students = []
    for role in roles:
        for student in finalSolution[role]:
            new_student = {}
            new_student["role"] = role
            new_student["match"] = student['project']
            new_student["email"] = student["email"]
            new_student['ranking'] = student['ranking']
            teacher = find_teacher_by_opdracht(teachers, student['project'])
            if teacher:
                new_student["docent"] = teacher["docent"]
                new_student["lokaal"] = teacher["lokaal"]
                new_student["dagdeel"] = teacher["dagdeel"]
            else:
                new_student["docent"] = ""
                new_student["lokaal"] = ""
                new_student["dagdeel"] = ""
            students.append(new_student)
    export_solution(semester, students)
    export_groups_html(semester, opdrachten, students)

if __name__ == "__main__":
    main()