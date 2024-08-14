def calc_rate(grades: list) -> float:
    if len(grades) > 0:
        rate = [grade.grade for grade in grades]
        return round(sum(rate) / len(rate), 1)
    return -1