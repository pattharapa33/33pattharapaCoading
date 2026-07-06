print("โปรเเกรมคำนวณเเม่สูตรคูณ")
num1 = int(input("ตัวเลขเริ่มต้น ="))
num2 = int(input("ตัวเลขสิ้สุด ="))

for i in range(num1, num2 + 1):
    print(f"---เเม่--- {i}")
    for i in range(1,13):
        print(i,"x",i,i*i)