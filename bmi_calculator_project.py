#body mass index (BMI)

def bmi_calculation():
    height = float(input("height (cm): "))
    weight = float(input("weight (kg): "))
    return 0 if (height <= 0 or weight <= 0) else round(weight / ((height / 100) ** 2), 1)

def bmi_category(num):
    if (num <= 0):
        return "error!"
    elif (num < 18.5):
        return "underweight!"
    elif (num < 24.9):
        return "healthy weight!"
    elif (num < 29.9):
        return "overweight!"
    elif (num >= 30):
        return "obese!"

def bmi_show(num, stat):
    print(num)
    print(stat)

#main program

BMI = bmi_calculation()
status = bmi_category(BMI)
bmi_show(BMI, status)