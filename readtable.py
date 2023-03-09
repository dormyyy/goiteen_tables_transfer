from dotenv import load_dotenv
from utils.datetime_funcs import strip_months, find_today
import json

load_dotenv()


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
        'MINE_JUNIOR': [],
        'MINE_KIDS': [],
        'ROB': [],
        'SCRATCH': [],
        'MOTION': []
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
        'GameDev': 'GD'
    }
    rows = sheet.values().get(spreadsheetId=sheet_id,
                                 range=sample_range).execute().get('values', [])
    for row in rows[1:]:
        try:
            course = course_tags[row[4]]
        except:
            course = None
        if not course:
            print('error on', row, 'course')
            continue
        tpe = 'tech' if 'Tech' in row[3] else 'soft' if 'Soft' in row[3] else None
        if not tpe:
            print('error on', row, 'type')
            continue
        lead = row[1]
        try:
            lesson = row[7].replace('№', '').split('.')[0]
        except:
            lesson = None
        if not lesson:
            print('error on', row, 'lesson')
            continue
        try:
            homeworks = int(row[10])
        except:
            homeworks = None
        if not homeworks:
            print('error on', row, 'homeworks')
            continue
        local = {
            'title': row[5],
            'course': course,
            'type': tpe,
            'lead': lead,
            'kxm': '',
            'lesson': lesson,
            'homeworks': homeworks
        }
        data[course].append(local)
        print(data)




