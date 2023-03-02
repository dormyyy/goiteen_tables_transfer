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
        # print(counts)
        # print(techs)
        # print(softs)
        t = 0
        s = 0
        times = find_today(column_dates)
        for j in range(1, times + current_data[name]['start_tech']):
            if j < current_data[name]['start_tech']:
                current_data[name]['lessons']['tech'].append('')
                current_data[name]['lessons']['count_tech'].append('')
            elif current_data[name]['start_tech'] <= j < current_data[name]['start_tech'] + len(techs):
                current_data[name]['lessons']['tech'].append(techs[t] if techs[t] else None)
                current_data[name]['lessons']['count_tech'].append(counts[t] if counts[t] else None)
                t += 1
            else:
                current_data[name]['lessons']['tech'].append(None)
                current_data[name]['lessons']['count_tech'].append(None)

        for j in range(1, times + current_data[name]['start_soft']):
            if j < current_data[name]['start_soft']:
                current_data[name]['lessons']['soft'].append('')
                current_data[name]['lessons']['count_soft'].append('')
            elif current_data[name]['start_soft'] <= j < current_data[name]['start_soft'] + len(softs):
                current_data[name]['lessons']['soft'].append(softs[s] if softs[s] else None)
                current_data[name]['lessons']['count_soft'].append(counts[s] if counts[s] else None)
                s += 1
            else:
                current_data[name]['lessons']['count_soft'].append(None)
                current_data[name]['lessons']['soft'].append(None)
        # print(current_data[name]['lessons']['tech'])
        # print(current_data[name]['lessons']['soft'])
        # print(current_data[name]['lessons']['count_tech'])
        # print(current_data[name]['lessons']['count_soft'])
        # min_range = min(current_data[name]['start_soft'], current_data[name]['start_tech'])
        # max_range = max(current_data[name]['start_soft'], current_data[name]['start_tech'])
        data[sample_range].append(current_data)
    f = open('test.json', 'w', encoding='utf-8')
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
    f.close()
    return data
