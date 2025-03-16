#Basal Metabolic Rate (BMR)

def bmr_calculation():
    age = float(input("age: "))
    gender = str(input("gender (m/f): "))
    height = float(input("height (cm): "))
    weight = float(input("weight (kg): "))
    if (age <= 0 or height <= 0 or weight <= 0):
        return 0
    elif (gender == 'm' or gender == 'M'):
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    elif (gender == 'f' or gender == 'F'):
        return round(10 * weight + 6.25 * height - 5 * age - 161)
    else:
        return 0

def bmr_show(num):
    print("error!") if (num == 0) else print(f"{num} calories")

#main program

bmr_show(bmr_calculation())