import random
number = random.randint(1 , 101)
count = 1

print("random_numbers")
print(1 , 101)

while True:
    guess = int(input("กรอกตัวเลข: "))
    count = count + 1
    if guess > number:
        print("มากไป")
    elif guess < number:
        print("น้อยไป")
    else:
        print("ถูกต้อง!")
        print("คุณทายทั้งหมด", count, "ครั้ง")