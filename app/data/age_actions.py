from datetime import datetime
now = datetime.now()

def age_calculator(day: str, month: str, year: str) -> str:
    day = int(day)
    month = int(month)
    year = int(year)

    if month > int(now.month):
        age = now.year - year - 1
        return str(age)
    elif month == int(now.month):
        if day >= now.day:
            age = now.year - year
            return str(age)
        else:
            age = now.year - year - 1
            return str(age)
    else:
        age = now.year - year
        return str(age)
    
def year_calculator(day: str, month: str, age: str) -> str:
    day = int(day)
    month = int(month)
    age = int(age)

    if month > int(now.month):
        year = now.year - age - 1
    elif month == int(now.month):
        if day >= now.day:
            year = now.year - age
        else:
            year = now.year - age - 1
    else:
        year = now.year - age
    
    return str(year)
    
def zodiac_def(day: str, month: str) -> str:
    day = int(day)
    month = int(month)

    match month:
        case 1:
            if day > 20:
                sign = "Водолей"
            else:
                sign = "Козерог"
        case 2:
            if day > 20:
                sign = "Рыбы"
            else:
                sign = "Водолей"
        case 3:
            if day > 20:
                sign = "Овен"
            else:
                sign = "Рыбы"
        case 4:
            if day > 20:
                sign = "Телец"
            else:
                sign = "Овен"
        case 5:
            if day > 20:
                sign = "Близнецы"
            else:
                sign = "Телец"
        case 6:
            if day > 21:
                sign = "Рак"
            else:
                sign = "Близнецы"
        case 7:
            if day > 22:
                sign = "Лев"
            else:
                sign = "Рак"
        case 8:
            if day > 23:
                sign = "Дева"
            else:
                sign = "Лев"
        case 9:
            if day > 23:
                sign = "Весы"
            else:
                sign = "Дева"
        case 10:
            if day > 23:
                sign = "Скорпион"
            else:
                sign = "Весы"
        case 11:
            if day > 22:
                sign = "Стрелец"
            else:
                sign = "Скорпион"
        case 12:
            if day > 21:
                sign = "Козерог"
            else:
                sign = "Стрелец"
        
    return str(sign)

def ch_zodiac(year: str) -> str:
    year = int(year)
    animals = [
        "Обезьяна", "Петух", "Собака", "Свинья", "Крыса", "Бык",
        "Тигр", "Кролик", "Дракон", "Змея", "Лошадь", "Овца"]
    animal = animals[year % 12]
    return str(animal)

def angel_def(date: str) -> str:
    while len(str(date)) != 1:
        sum = 0
        for n in str(date):
            sum += int(n)
        date = sum
            
    
    return str(date)*3