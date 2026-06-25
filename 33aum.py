print("โปรเเกรมคำนวณค่า BMI เเละเเปลผลสุขภาพ")

kilogram = int(input("ค่าน้ำหนัก"))
height = int(input("ค่าส่วนสูง"))

BMI = kilogram / (height * height)
Total = BMI
 
print("\nหาค่าเฉลี่ยBMI = ", Total)

if BMI < 18.5:
    (print("น้ำหนักน้อย ควรกินเพิ่มขึ้น"))
elif 18.5 < BMI < 22.9:
    (print("ปกติ"))
elif 23 < BMI < 24.9:
    (print("น้ำหนักเกิน กินให้น้อยลง"))
else:
    (print("อ้วน เสี่ยงเป็นโรค"))
