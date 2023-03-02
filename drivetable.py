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
