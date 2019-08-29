import time
chinese_wday_dict = {
    "一": '1',
    "二": '2',
    "三": '3',
    "四": '4',
    "五": '5',
    "六": '6',
    "日": '7'
}
str_number_wday_dict = {v: k for k, v in chinese_wday_dict.items()}


def week_course(course_table):
    body = course_table["body"]
    result = body["result"]
    curr_week = body['week']
    # 课程字典 key: 星期几 value: 那一天的课
    wday_course_dict = dict()
    for i in range(1, 8):
        wday_course_dict.setdefault(str(i), [])
    for x in result:
        # 当周
        if curr_week >= int(x["qsz"]) and curr_week <= int(x["zzz"]):
            for _time, _location in zip(x["class_time"], x["location"]):

                _course = {
                    "class_name": x["class_name"],
                    "class_time": _time[2:],
                    "location": _location,
                    "teacher_name": x["teacher_name"],
                }
                # class_time [1@2-2, 3@3-2]
                wday_course_dict[str(_time[0])].append(_course)

    sorted_wday_course_dict = sorted(wday_course_dict.items(),
                                     key=lambda e: int(e[0]))

    r_course_list = []
    for wday, course_list in sorted_wday_course_dict:
        r_course_list.append(parse_course_by_wday(course_list, wday))

    today = str(time.localtime(time.time()).tm_wday + 1)
    return {
        'week_course_list': r_course_list,
        'today': parse_course_by_wday(wday_course_dict[today], today)
    }


def tip(strs: str) -> str:
    after = strs.split('-')
    start = int(after[0])
    last = int(after[1])
    if start == 1 and last == 2:
        return "上午第一讲"
    if start == 2 and last == 2:
        return "上午第二讲"
    if start == 3 and last == 2:
        return "下午第一讲"
    if start == 4 and last == 2:
        return "下午第二讲"
    if start == 5 and last == 2:
        return "晚上第一讲"
    if start == 6 and last == 2:
        return "晚上第二讲"

    if start == 1 and last == 4:
        return "上午一到二讲"
    if start == 3 and last == 4:
        return "下午一到二讲"
    if start == 5 and last == 4:
        return "晚上一到二讲"

    return f'第{start}讲，持续{last}节'


def parse_course_by_wday(course_list, day: str):
    if len(course_list) == 0:
        return f'星期{str_number_wday_dict.get(day, day)}没有课\n'
    msg = f'星期{str_number_wday_dict.get(day, day)}的课程如下:\n'

    course_list.sort(key=lambda e: e['class_time'][0])
    for course in course_list:
        t = '{}--{}--{}({})\n'.format(tip(course["class_time"]),
                                      course["location"], course["class_name"],
                                      course["teacher_name"])
        msg = msg + t
    return msg
