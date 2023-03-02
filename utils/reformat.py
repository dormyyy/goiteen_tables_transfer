def reformat(data):
    course_by_tags = {
        'PYTHON': {},
        'FE': {},
        'FE_JUNIOR': {},
        'DA': {},
        'DA_JUNIOR': {},
        'GD': {},
        'MINE': {},
        'MINE_JUNIOR': {},
        'MINE_KIDS': {},
        'ROB': {},
        'SCRATCH': {},
        'MOTION': {}
    }
    new_data = {}
    for sheet in data:
        for courses in sheet.values():
            for course in courses:
                new_data.update(course)
    test_data = new_data.copy()
    for name, course_info in new_data.items():
        course = {name: course_info}
        select = name.lower().split('_')
        # print(name, ' ->', end=" ")
        if 'mine' in select:
            if 'kids' in select:
                course_by_tags["MINE_KIDS"].update(course)
                # print("MINE_KIDS")
            elif 'jun' in select:
                course_by_tags["MINE_JUNIOR"].update(course)
                # print("MINE_JUNIOR")
            else:
                course_by_tags["MINE"].update(course)
                # print("MINE")
            test_data.pop(name)
        elif 'py' in select:
            course_by_tags["PYTHON"].update(course)
            # print("PYTHON")
            test_data.pop(name)
        elif 'python' in select:
            course_by_tags["PYTHON"].update(course)
            # print("PYTHON")
            test_data.pop(name)
        elif 'fe' in select:
            if 'jun' in select:
                course_by_tags["FE_JUNIOR"].update(course)
                # print("FE_JUNIOR")
            else:
                course_by_tags["FE"].update(course)
                # print("FE")
            test_data.pop(name)
        elif 'rob' in select:
            course_by_tags["ROB"].update(course)
            # print("ROB")
            test_data.pop(name)
        elif 'da' in select:
            if 'jun' in select:
                course_by_tags["DA_JUNIOR"].update(course)
                # print("DA_JUNIOR")
            else:
                course_by_tags["DA"].update(course)
                # print("DA")
            test_data.pop(name)
        elif 'motion' in select:
            course_by_tags["MOTION"].update(course)
            # print("MOTION")
            test_data.pop(name)
        elif 'gd' in select:
            course_by_tags["GD"].update(course)
            # print("GD")
            test_data.pop(name)
        else:
            if 'goiteens' in select:
                course_by_tags["SCRATCH"].update(course)
                # print("SCRATCH")
                test_data.pop(name)
            elif 'jun' in select:
                course_by_tags["MINE_JUNIOR"].update(course)
                # print("MINE_JUNIOR")
                test_data.pop(name)
    return course_by_tags
