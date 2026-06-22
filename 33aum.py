print("โปรเเกรมคำนวณคะเเนนรวม \n ")

science = int(input("คะเเนนวิทยาศาสตร์"))
thai = int(input("คะเเนนภาษาไทย"))
english = int(input("คะเเนนภาษาอังกฤษ"))

total_point = science + thai + english
average = total_point /3

print("\nคะเเนนรวมของคุณ = ", total_point)
print("คะเเนนเฉลี่ยของคุณ = ", average)

if average < 60:
    print("คะเเนนของคุณควรปรับปรุง")
elif average < 80:
    print("คะเเนนของคุณผ่าน")
else: 
    print("คะเเนนของคุณดีเยี่ยม")

print("จัดทำโดย ภัทรลาภา การะเกตุ เลขที่ 33 ")