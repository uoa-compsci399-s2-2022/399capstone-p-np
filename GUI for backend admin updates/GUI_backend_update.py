import PySimpleGUI as sg
import os

import sql_command_execute

exe = sql_command_execute.execute()

dir = os.path.dirname(__file__)
file_name = os.path.join(dir,'399courses.db')

DATABASE = file_name

################## database window ###################
def create_modal(table_array,header):
    database_layout = [[sg.Table(table_array, headings=header,
        num_rows=20,
        display_row_numbers=True,
        auto_size_columns=True,
        def_col_width=10,
        max_col_width=40,
        key="-database_table-",
        row_height=20,
        enable_events=True,
        )],
    [sg.B("return",key="-RETURN-",bind_return_key=True)],
    [sg.Input(key="-INPUT-"),sg.Input(key="-INPUT1-"),sg.B("DELETE",key="-delete-"),sg.B("UPDATE",key="-update-")],
    ]

    table_array = sg.Window("information",database_layout,modal=True)

    while True:
        event, values = table_array.read()
        if event == None or event == "-RETURN-":
            break

        if event == '-database_table-':
            ind = values['-database_table-'][0]
            database = exe.data_fetch()
            delete_item = database[ind][0]
            table_array['-INPUT-'].update(delete_item)
            delete_item1 = database[ind][1]
            table_array['-INPUT1-'].update(delete_item1)

        if event == '-delete-':
            exe.delete_course(values['-INPUT-'],values['-INPUT1-'])
            sg.popup(f"deleted {values['-INPUT-'],values['-INPUT1-']}")
            break

        if event == '-update-':
            create_modal2(values['-INPUT-'],values['-INPUT1-'])

    table_array.close()

def create_modal1(table_array1,header1):
    database_layout1 = [[sg.Table(table_array1, headings=header1,
        num_rows=10,
        display_row_numbers=True,
        auto_size_columns=True,
        def_col_width=20,
        max_col_width=20,
        row_height=20,
        enable_events=True,
        )],
    [sg.B("return",key="-RETURN-",bind_return_key=True)],
    ]

    table_array1 = sg.Window("list_all_majors",database_layout1,modal=True)

    while True:
        event, values = table_array1.read()
        if event == None or event == "-RETURN-":
            break

    table_array1.close()

def create_modal2(subject1, courseNumber1):
    database_layout2 = [ 
        text_row('MajorType: ','-MajorType-',False),
        text_row('pointsValue: ','-pointsValue-',False),
        text_row('GPAreq: ','-GPAreq-',False),
        text_row('level: ','-level-',False),
        text_row('approvalNeeded: ','-approvalNeeded-',False),
        text_row1('description: ','-description-',False),
        text_row('problematicPreReqs: ','-problematicPreReqs-',False),
        text_row('problematicRestrictions: ','-problematicRestrictions-',False),
        text_row('problematicCoReqs: ','-problematicCoReqs-',False),
        text_row('problematicOther: ','-problematicOther-',False),
        [sg.B('update_course',key='-update_course-')],
        [sg.B("return",key="-RETURN-",bind_return_key=True)],
        ]

    table_array2 = sg.Window("update_course",database_layout2,modal=True)

    while True:
        event, values = table_array2.read()
        if event == None or event == "-RETURN-":
            break

        if event == '-update_course-':
            exe.update_course(values['-MajorType-'],values['-pointsValue-']
                                ,values['-GPAreq-'],values['-level-']
                                ,values['-approvalNeeded-'],values['-description-']
                                ,values['-problematicPreReqs-'],values['-problematicRestrictions-']
                                ,values['-problematicCoReqs-'],values['-problematicOther-']
                                ,subject1, courseNumber1)
            
            database = exe.data_fetch()
            database = [list(data) for data in database]
            create_modal(database,header)

    table_array2.close()

################　main window ##################
header = ["subject","couseNumber","MajorType","pointsValue","GPAreq","level","approvalNeeded","description"]
header1 = ["majorID","majorName","totalPointsNeeded","pointGenEd","year","honours","level"]
subject_array = []

def text_row(category,key,focus_check) -> list:
    return [sg.Text(category,s=(14,1),justification="right"),\
        sg.Input(key=key,do_not_clear=False,focus=focus_check)]

def text_row1(category,key,focus_check) -> list:
    return [sg.Text(category,s=(14,1),justification="right"),\
        sg.Multiline(key=key,s=(50,10),do_not_clear=False,focus=focus_check)]

layout = [ 
    text_row('subject: ','-subject-',True),
    text_row('couseNumber: ','-couseNumber-',True),
    text_row('MajorType: ','-MajorType-',False),
    text_row('pointsValue: ','-pointsValue-',False),
    text_row('GPAreq: ','-GPAreq-',False),
    text_row('level: ','-level-',False),
    text_row('approvalNeeded: ','-approvalNeeded-',False),
    text_row1('description: ','-description-',False),
    text_row('problematicPreReqs: ','-problematicPreReqs-',False),
    text_row('problematicRestrictions: ','-problematicRestrictions-',False),
    text_row('problematicCoReqs: ','-problematicCoReqs-',False),
    text_row('problematicOther: ','-problematicOther-',False),
    [sg.B('register',key="-register-",bind_return_key=True),sg.B('END',key='-END-')],
    [sg.B('open_data',key='-open_data-')],
    [sg.B('list_all_majors',key='-list_all_majors-')],
    ]

window = sg.Window("Table_sample", layout)

while True:
    event, values = window.read()
    if event == None or event == '-END-':
        break
    if event == '-register-':
        if values['-subject-'] == "":
            sg.popup('need subject')
        else:
            if not len(subject_array) == 0:
                subject_array.clear()

            subject_array.append([values['-subject-'],values['-couseNumber-']
                                ,values['-MajorType-'],values['-pointsValue-']
                                ,values['-GPAreq-'],values['-level-']
                                ,values['-approvalNeeded-'],values['-description-']
                                ,values['-problematicPreReqs-'],values['-problematicRestrictions-']
                                ,values['-problematicCoReqs-'],values['-problematicOther-']])
            
            exe.insert_paper_to_database(subject_array[0])
            
            database = exe.data_fetch()
            database = [list(data) for data in database]
            create_modal(database,header)

    if event == '-open_data-':
        database = exe.data_fetch()
        database = [list(data) for data in database]
        create_modal(database,header)

    if event == '-list_all_majors-':
        database = exe.list_all_majors()
        database = [list(data) for data in database]
        create_modal1(database,header1)
    
window.close()
