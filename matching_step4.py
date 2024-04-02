import csv
from matching_lib import roles, read_students


def lees_studenten_canvas():
    print('CANVAS IMPORT')
    filename = "../canvas_import/canvas_email_export.csv"
    studenten = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():

            studenten.append(line.strip())
    return studenten

def main():
    studenten = read_students("formulierreacties_gefilterd.csv")
    print('studenten', len(studenten))
    studenten_canvas = lees_studenten_canvas()
    print('studenten_canvas',len(studenten_canvas))
    print(studenten_canvas)
    onbekend = []
    for student in studenten:
        if student['Email'] in studenten_canvas:
            studenten_canvas.remove(student['Email'])
        else:
            onbekend.append(student['Email'])

    #print('NO SHOW')
    #for student in studenten_canvas:
    #    print(student+"; ")
    print('ONBEKEND')
    for student in onbekend:
        print(student+"; ")


if __name__ == "__main__":
    main()