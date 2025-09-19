from collections import defaultdict

def get_years(date=None):
    if not date:
        return 0
    today = date.today()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))

def get_age_title_stat(teachers, cut_points=[30, 40, 60]):
    groups = ['<{}'.format(cut_points[0])] + \
             ['{}~{}'.format(cut_points[i], cut_points[i+1]-1) for i in range(len(cut_points)-1)] + \
             ['>={}'.format(cut_points[-1])]

    stat = defaultdict(lambda: defaultdict(int))

    for t in teachers:
        age = t.age
        title = t.title if t.title else '无'

        group = None
        if age < cut_points[0]:
            group = groups[0]
        elif age >= cut_points[-1]:
            group = groups[-1]
        else:
            for i in range(len(cut_points)-1):
                if cut_points[i] <= age < cut_points[i+1]:
                    group = groups[i+1]
                    break

        if group:
            stat[title][group] += 1
    
    # 转换为表格格式
    titles = sorted(stat.keys())
    result = {
        'age_groups': groups,
        'titles': titles,
        'data': []
    }
    
    for title in titles:
        row = []
        for group in groups:
            row.append(stat[title][group])
        result['data'].append(row)
    
    return result