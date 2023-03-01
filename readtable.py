import os
from dotenv import load_dotenv
from utils.datetime_funcs import strip_months, find_today

load_dotenv()


def read_table(sheet, sheet_id, sample_range):
    columns = sheet.values().get(spreadsheetId=sheet_id,
                                 range=sample_range, ).execute().get('values', [])
    columns_months = {}
    for i in range(len(columns[10:])):
        column = columns[10:][i]
        if i == 0:
            current_month = column[0]
        if column[0].count('(') == 0:
            current_month = column[0]
            columns_months.update({current_month: []})
        else:
            columns_months[current_month].append(
                column[0][column[0].find('(') + 1: column[0].find(')')]
            )

    column_dates = strip_months(columns_months)
    print(column_dates)

    result = sheet.values().get(spreadsheetId=sheet_id,
                                    range=sample_range, majorDimension="COLUMNS").execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    print('Name, Major:')

    data = {}
    start_i = 2
    for i in range(4, len(values), 3):
        row1 = values[i - 2][2:]
        row2 = values[i - 1][2:]
        row3 = values[i][2:]
        name = row1[0]
        current_data = {name: {
                'lead': row1[2],
                'tech_lead': row1[3],
                'soft_lead': row1[4],
                'start_members': row1[5],
                'start_tech': row1[6] if row1[6] else 1,
                'start_soft': row1[7] if row1[7] else 1,
                'lessons': {
                    'tech': [],
                    'soft': [],
                    'count': []
                }
            }
        }
        counts = [i for i in row1[8:] if i not in ('tec', 'cnt', 'sof')]
        techs = [i for i in row2[8:] if i not in ('tec', 'cnt', 'sof')]
        softs = [i for i in row3[8:] if i not in ('tec', 'cnt', 'sof')]
        print(counts)
        print(techs)
        print(softs)
        # for j in range(1, find_today(column_dates) + 1):
        #     if i < current_data[name]['start_tech']:
        #         current_data[name]['lessons']['tech'].append(None)
        # # current_data[name]['lessons']
    return data
