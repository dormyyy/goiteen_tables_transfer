from dotenv import load_dotenv
from utils.datetime_funcs import strip_months, find_today
import json, string

load_dotenv()


def generate_column_index(index):
    if index <= 0:
        raise ValueError('Номер столбца должен быть положительным числом.')
    letters = string.ascii_uppercase
    result = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result.append(letters[remainder])
    return ''.join(reversed(result))


def read_table(sheet, sheet_id, sample_range):
    columns = sheet.values().get(spreadsheetId=sheet_id,
                                 range=sample_range, ).execute().get('values', [])
    columns_months = {}
    current_month = columns[8:][0][0]
    for i in range(len(columns[8:])):
        column = columns[8:][i]
        if column[0].count('(') == 0:
            current_month = column[0]
            columns_months.update({current_month: []})
        else:
            columns_months[current_month].append(
                column[0][column[0].find('(') + 1: column[0].find(')')]
            )

    column_dates = strip_months(columns_months)

    result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sample_range, majorDimension="COLUMNS").execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    data = {sample_range: []}
    for i in range(4, len(values), 3):
        row1 = values[i - 2][1:]
        row2 = values[i - 1][1:]
        row3 = values[i][1:]
        name = row1[0]
        current_data = {name: {
                'lead': row1[1],
                'tech_lead': row1[2],
                'soft_lead': row1[3],
                'start_members': row1[4],
                'start_tech': int(row1[5]) if row1[5] else 1,
                'start_soft': int(row1[6]) if row1[6] else 1,
                'lessons': {
                    'tech': [],
                    'soft': [],
                    'count_tech': [],
                    'count_soft': []
                }
            }
        }
        counts = [i for i in row1[8:] if i not in ('tec', 'cnt', 'sof')]
        techs = [i for i in row2[8:] if i not in ('tec', 'cnt', 'sof')]
        softs = [i for i in row3[8:] if i not in ('tec', 'cnt', 'sof')]
        t = 0
        s = 0
        times = find_today(column_dates)
        for j in range(1, times + current_data[name]['start_tech']):
            if j < current_data[name]['start_tech']:
                current_data[name]['lessons']['tech'].append('')
                current_data[name]['lessons']['count_tech'].append('')
            elif current_data[name]['start_tech'] <= j < current_data[name]['start_tech'] + len(techs):
                current_data[name]['lessons']['tech'].append(techs[t] if techs[t] else 'missing')
                current_data[name]['lessons']['count_tech'].append(counts[t] if counts[t] else 'missing')
                t += 1
            else:
                current_data[name]['lessons']['tech'].append('missing')
                current_data[name]['lessons']['count_tech'].append('missing')

        for j in range(1, times + current_data[name]['start_soft']):
            if j < current_data[name]['start_soft']:
                current_data[name]['lessons']['soft'].append('')
                current_data[name]['lessons']['count_soft'].append('')
            elif current_data[name]['start_soft'] <= j < current_data[name]['start_soft'] + len(softs):
                current_data[name]['lessons']['soft'].append(softs[s] if softs[s] else 'missing')
                current_data[name]['lessons']['count_soft'].append(counts[s] if counts[s] else 'missing')
                s += 1
            else:
                current_data[name]['lessons']['count_soft'].append('missing')
                current_data[name]['lessons']['soft'].append('missing')
        data[sample_range].append(current_data)
    f = open('test.json', 'w', encoding='utf-8')
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
    f.close()
    return data


def read_lines(sheet, sheet_id, sample_range):
    data = {
        'PYTHON': [],
        'FE': [],
        'FE_JUNIOR': [],
        'DA': [],
        'DA_JUNIOR': [],
        'GD': [],
        'MINE': [],
        'MINE_KIDS': [],
        'ROB': [],
        'SCRATCH': [],
        'MOTION': [],
        'SOFT': []
    }
    course_tags = {
        'Scratch': 'SCRATCH',
        'Minecraft Kids': 'MINE_KIDS',
        'Minecraft': 'MINE',
        'Design Junior': 'DA_JUNIOR',
        'Digital Design': 'DA',
        'FrontEnd': 'FE',
        'FrontEnd Junior': 'FE_JUNIOR',
        'Python': 'PYTHON',
        'Roblox': 'ROB',
        'GameDev': 'GD',
        'Soft Skills': 'SOFT'
    }
    course_indexes = {
        'Scratch': 6,
        'Minecraft Kids': 14,
        'Minecraft': 23,
        'Design Junior': 41,
        'Digital Design': 32,
        'FrontEnd': 59,
        'FrontEnd Junior': 50,
        'Python': 68,
        'Roblox': 77,
        'GameDev': 86,
        'Soft Skills': 93
    }
    rows = sheet.values().get(spreadsheetId=sheet_id,
                                 range=sample_range).execute().get('values', [])
    for row in rows[2:]:
        try:
            course = row[5]
            course_index = course_indexes[course]
            name = row[course_index]
        except KeyError:
            print("KeyError")
            continue
        except IndexError:
            print("IndexError")
            continue
        teach = row[2]
        lesson = None
        homeworks = None
        if course in ['Scratch', 'Soft Skills']:
            try:
                lesson = int(row[course_index + 1])
            except:
                lesson = 1
            try:
                homeworks = int(row[course_index + 6])
            except:
                homeworks = 0
        elif course in ['Minecraft Kids', 'Minecraft', 'Digital Design', 'Roblox',
                        'Design Junior', 'FrontEnd Junior', 'FrontEnd', 'Python']:
            try:
                lesson = int(row[course_index + 2])
            except:
                lesson = 1
            try:
                homeworks = int(row[course_index + 7])
            except:
                homeworks = 0
        elif course == 'GameDev':
            try:
                lesson = int(row[course_index + 1])
            except:
                lesson = 1
            try:
                homeworks = int(row[course_index + 5])
            except:
                homeworks = 0
        else:
            print('skipped on', course, '->', name)
            continue
        # local = {
        #         name: {
        #             'course': course,
        #             'teach': teach,
        #             'lesson': lesson,
        #             'homeworks': homeworks,
        #             'complete': False
        #         }
        #     }
        # data[course_tags[course]].update(local)
        local = [name, teach, lesson, homeworks]
        print(local)
        data[course_tags[course]].append(local)
    return data

    # for row in rows[1:]:
    #     try:
    #         course = course_tags[row[4]]
    #     except:
    #         course = None
    #     if not course:
    #         print('error on', row, 'course')
    #         continue
    #     tpe = 'tech' if 'Tech' in row[3] else 'soft' if 'Soft' in row[3] else None
    #     if not tpe:
    #         print('error on', row, 'type')
    #         continue
    #     lead = row[1]
    #     try:
    #         lesson = int(row[7].replace('№', '').split('.')[0])
    #     except:
    #         lesson = None
    #     if not lesson:
    #         print('error on', row, 'lesson')
    #         continue
    #     try:
    #         homeworks = int(row[10])
    #     except:
    #         homeworks = None
    #     if not homeworks:
    #         print('error on', row, 'homeworks')
    #         continue
    #     local = {
    #         row[5]: {
    #             'course': course,
    #             'type': tpe,
    #             'lead': lead,
    #             'kxm': '',
    #             'lesson': lesson,
    #             'homeworks': homeworks,
    #             'complete': False
    #         }
    #     }
    #     data[course].update(local)
    #     print(data)
    # return data


# def get_table(sheet, sheet_id, sample_range):
#     # вересень
#     rows = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range, majorDimension="COLUMNS").execute().get('values', [])
#     groups = set(rows[3][1:])
#     data = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range).execute().get('values', [])
#     print(data, '\n\n\n')
#     drive_data = []
#     for group in groups:
#         row1 = [group, 'name', 'Дата']
#         row2 = ['', '', 'Введіть номер заняття та тему:']
#         row3 = ['', '', 'Залиште свої підсумки після уроку та ДЗ тут:']
#         row4 = ['', '', 'Скільки було здано ДЗ?']
#         row5 = ['', '', 'Cкільки у вас було сьогодні студентів? ']
#         row6 = ['', '', 'Коментар щодо заняття (реакція студентів на програму; зрозумілість дітьми програми; що вважаєте зручним / що треба покращити)']
#         row7 = ['', '', 'Додаткові файли до ДЗ']
#         first = True
#         for row in data:
#             if row[3] == group:
#                 if first:
#                     row1[1] = row[2]
#                 row1.append(row[4])
#                 row2.append(row[6])
#                 row3.append(row[7])
#                 row4.append(row[8])
#                 row5.append(row[9])
#                 row6.append(row[10])
#                 try:
#                     row7.append(row[12])
#                 except:
#                     row7.append(' ')
#         drive_data.append(row1)
#         drive_data.append(row2)
#         drive_data.append(row3)
#         drive_data.append(row4)
#         drive_data.append(row5)
#         drive_data.append(row6)
#         drive_data.append(row7)
#     last_column = generate_column_index(len(max(drive_data, key=len)))
#     print(drive_data)
#     sheet.values().batchUpdate(spreadsheetId='1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8', body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {
#                 "range": f"вересень!A2:{last_column}{len(drive_data) + 1}",
#                 "majorDimension": "ROWS",
#                 "values": drive_data
#             }
#         ]
#     }).execute()

# def get_table(sheet, sheet_id, sample_range):
#     # жовтень - січень
#     rows = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range, majorDimension="COLUMNS").execute().get('values', [])
#     groups = set(rows[3][1:])
#     data = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range).execute().get('values', [])
#     print(data, '\n\n\n')
#     drive_data = []
#     for group in groups:
#         row1 = [group, 'name', 'Дата']
#         row2 = ['', '', 'Введіть номер заняття та тему:']
#         row3 = ['', '', 'Залиште свої підсумки після уроку та ДЗ тут:']
#         row4 = ['', '', 'Скільки було здано ДЗ?']
#         row5 = ['', '', 'Cкільки у вас було сьогодні студентів? ']
#         row6 = ['', '', 'Коментар щодо заняття (реакція студентів на програму; зрозумілість дітьми програми; що вважаєте зручним / що треба покращити)']
#         row7 = ['', '', 'Додаткові файли до ДЗ']
#         first = True
#         for row in data:
#             if row[3] == group:
#                 if first:
#                     row1[1] = row[2]
#                     first = False
#                 row1.append(row[5])
#                 row2.append(row[7])
#                 row3.append(row[8])
#                 row4.append(row[10])
#                 row5.append(' ')
#                 row6.append(row[11])
#                 try:
#                     row7.append(row[9])
#                 except:
#                     row7.append(' ')
#         drive_data.append(row1)
#         drive_data.append(row2)
#         drive_data.append(row3)
#         drive_data.append(row4)
#         drive_data.append(row5)
#         drive_data.append(row6)
#         drive_data.append(row7)
#     last_column = generate_column_index(len(max(drive_data, key=len)))
#     print(drive_data)
#     sheet.values().batchUpdate(spreadsheetId='1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8', body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {
#                 "range": f"січень!A2:{last_column}{len(drive_data) + 1}",
#                 "majorDimension": "ROWS",
#                 "values": drive_data
#             }
#         ]
#     }).execute()

# def get_table(sheet, sheet_id, sample_range):
#     # лютий - березень
#     rows = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range, majorDimension="COLUMNS").execute().get('values', [])
#     groups = set(rows[3][1:])
#     data = sheet.values().get(spreadsheetId=sheet_id,
#                               range=sample_range).execute().get('values', [])
#     print(data, '\n\n\n')
#     drive_data = []
#     for group in groups:
#         row1 = [group, 'name', 'Дата']
#         row2 = ['', '', 'Введіть номер заняття та тему:']
#         row3 = ['', '', 'Залиште свої підсумки після уроку та ДЗ тут:']
#         row4 = ['', '', 'Скільки було здано ДЗ?']
#         row5 = ['', '', 'Cкільки у вас було сьогодні студентів? ']
#         row6 = ['', '', 'Коментар щодо заняття (реакція студентів на програму; зрозумілість дітьми програми; що вважаєте зручним / що треба покращити)']
#         row7 = ['', '', 'Додаткові файли до ДЗ']
#         first = True
#         for row in data:
#             if row[3] == group:
#                 if first:
#                     row1[1] = row[2]
#                     first = False
#                 row1.append(row[5])
#                 row2.append(row[7])
#                 row3.append(row[8])
#                 row4.append(row[10])
#                 row5.append(' ')
#                 row6.append(row[11])
#                 try:
#                     row7.append(row[9])
#                 except:
#                     row7.append(' ')
#         drive_data.append(row1)
#         drive_data.append(row2)
#         drive_data.append(row3)
#         drive_data.append(row4)
#         drive_data.append(row5)
#         drive_data.append(row6)
#         drive_data.append(row7)
#     last_column = generate_column_index(len(max(drive_data, key=len)))
#     print(drive_data)
#     sheet.values().batchUpdate(spreadsheetId='1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8', body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {
#                 "range": f"березень!A2:{last_column}{len(drive_data) + 1}",
#                 "majorDimension": "ROWS",
#                 "values": drive_data
#             }
#         ]
#     }).execute()

# def transfer_table(sheet, sheet_id):
#     courses = {
#         'Scratch': [],
#         'Minecraft Kids': [],
#         'Minecraft': [],
#         'Design Junior': [],
#         'Digital Art': [],
#         'FrontEnd': [],
#         'FrontEnd Junior': [],
#         'Python': [],
#         'Roblox': [],
#         'GameDev': [],
#         'unsorted': []
#     }
#     sheet_metadata = sheet.get(spreadsheetId="1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8").execute()
#     properties = sheet_metadata.get('sheets')
#     sheets = [item.get('properties').get('title') for item in properties][:7]
#
#     for item in sheets:
#         data = sheet.values().get(spreadsheetId="1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8",
#                                       range=item).execute().get('values', [])[1:]
#         for i in range(6, len(data), 7):
#             group = data[i - 6][0].lower()
#             push = 'unsorted'
#             if "da_jun" in group:
#                 push = 'Design Junior'
#             elif "fe_jun" in group:
#                 push = 'FrontEnd Junior'
#             elif "mine_jun" in group or "mine_kids" in group:
#                 push = 'Minecraft Kids'
#             elif "goiteens_ua_kids" in group:
#                 push = 'Scratch'
#             elif "gd" in group or "gamedev" in group:
#                 push = 'GameDev'
#             elif "python" in group or "py" in group:
#                 push = 'Python'
#             elif "rob" in group:
#                 push = 'Roblox'
#             elif "fe" in group or "frontend" in group or "front-end" in group:
#                 push = 'FrontEnd'
#             elif "da" in group or "motion" in group or "design" in group:
#                 push = 'Digital Art'
#             elif "mine" in group:
#                 push = 'Minecraft'
#             names = [i[0].lower() for i in courses[push]]
#             is_new = True
#             if names:
#                 if group in names:
#                     is_new = False
#                     place = names.index(group) + 6
#                     courses[push][place - 6].extend(data[i - 6][3:])
#                     courses[push][place - 5].extend(data[i - 5][3:])
#                     courses[push][place - 4].extend(data[i - 4][3:])
#                     courses[push][place - 3].extend(data[i - 3][3:])
#                     courses[push][place - 2].extend(data[i - 2][3:])
#                     courses[push][place - 1].extend(data[i - 1][3:])
#                     courses[push][place].extend(data[i][3:])
#             if is_new:
#                 courses[push].append(data[i - 6])
#                 courses[push].append(data[i - 5])
#                 courses[push].append(data[i - 4])
#                 courses[push].append(data[i - 3])
#                 courses[push].append(data[i - 2])
#                 courses[push].append(data[i - 1])
#                 courses[push].append(data[i])
#     print(courses['FrontEnd Junior'])
#     for key, value in courses.items():
#         last_column = generate_column_index(len(max(value, key=len)))
#         sheet.values().batchUpdate(spreadsheetId='1NAvhAQS1wSIhpVA2MPH4rLeVpfwhSUQDyGAn3GosSE8', body={
#             "valueInputOption": "USER_ENTERED",
#             "data": [
#                 {
#                     "range": f"{key}!A2:{last_column}{len(value) + 1}",
#                     "majorDimension": "ROWS",
#                     "values": value
#                 }
#             ]
#         }).execute()
