import string


def generate_column_index(index):
    if index <= 0:
        raise ValueError('Номер столбца должен быть положительным числом.')
    letters = string.ascii_uppercase
    result = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result.append(letters[remainder])
    return ''.join(reversed(result))


def drive_table(sheet, sheet_id, sample_range, data):
    drive_list = []
    for name, course_info in data.items():
        row1 = [
            name,
            course_info["lead"],
            course_info["tech_lead"],
            course_info["soft_lead"],
            course_info["start_members"],
            "Tech - >"
        ] + course_info["lessons"]["tech"]
        row2 = [''] * 5 + ["Soft - >"] + course_info["lessons"]["soft"]
        row3 = [''] * 5 + ["Tech Count - >"] + course_info["lessons"]["count_tech"]
        row4 = [''] * 5 + ["Soft Count - >"] + course_info["lessons"]["count_soft"]
        drive_list.append(row1)
        drive_list.append(row2)
        drive_list.append(row3)
        drive_list.append(row4)
    last_column = generate_column_index(len(max(drive_list, key=len)))
    sheet.values().batchUpdate(spreadsheetId=sheet_id, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": f"{sample_range}!A2:{last_column}{len(drive_list) + 1}",
                "majorDimension": "ROWS",
                "values": drive_list
            }
        ]
    }).execute()


def drive_rows(sheet, sheet_id, sample_range, data: dict):
    rows = sheet.values().get(spreadsheetId=sheet_id, range=sample_range).execute().get('values', [])
    rows = rows[1:]
    print('\n', data)
    drive = []
    k = 2
    for i, j in enumerate(rows):
        if i % 4 == 0:
            if j[0] in data.keys():
                local = data[j[0]]
                j[1] = ''
                j[2 if local['type'] == 'tech' else 3] = local['lead']
                if local['type'] == 'tech':
                    try:
                        j[5 + local['lesson']] = local['homeworks']
                    except:
                        ln = 6 + local['lesson']
                        j += [[''] * (len(j) - ln)]
                        j[5 + local['lesson']] = local['homeworks']
                else:
                    k = rows[i + 1]
                    try:
                        k[5 + local['lesson']] = local['homeworks']
                    except:
                        ln = 6 + local['lesson']
                        k += [[''] * (len(k) - ln)]
                        k[5 + local['lesson']] = local['homeworks']
                    rows[i + 1] = k
                data[j[0]]['complete'] = True
        drive.append(j)
    if drive:
        sheet.values().batchUpdate(spreadsheetId=sheet_id, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": f"{sample_range}!A2:{generate_column_index(len(max(drive, key=len)))}{len(drive) + 1}",
                    "majorDimension": "ROWS",
                    "values": drive
                }
            ]
        }).execute()
    drive_list = []
    drive_range = len(rows) + 2
    for name, course_info in data.items():
        if not course_info['complete']:
            row1 = [
                       name,
                       course_info["kxm"],
                       '' if course_info['type'] == 'soft' else course_info["lead"],
                       course_info["lead"] if course_info['type'] == 'soft' else '',
                       '',
                       "Tech - >"
                   ]
            row2 = [''] * 5 + ["Soft - >"]
            row3 = [''] * 5 + ["Tech Count - >"]
            row4 = [''] * 5 + ["Soft Count - >"]
            drive_list.append(row1)
            drive_list.append(row2)
            drive_list.append(row3)
            drive_list.append(row4)
            if course_info['type'] == 'tech':
                row1 += [[''] * course_info['lesson']]
                row1[5 + course_info['lesson']] = course_info['homeworks']
            if course_info['type'] == 'soft':
                row2 += [[''] * course_info['lesson']]
                row2[5 + course_info['lesson']] = course_info['homeworks']
            print(drive_list)
        if drive_list:
            last_column = generate_column_index(len(max(drive_list, key=len)))
            sheet.values().batchUpdate(spreadsheetId=sheet_id, body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": f"{sample_range}!A{drive_range}:{last_column}{len(drive_list) + drive_range + 1}",
                        "majorDimension": "ROWS",
                        "values": drive_list
                    }
                ]
            }).execute()
