print("โปเเกรมคำนวณคะเเนนรวม")

score1 = int(input("คะเเนนวิชาที่่1"))
score2 = int(input("คะเเนนวิชาที่2"))
score3 = int(input("คะเเนนวิชาที่3"))

total_score = score1 + score2 + score3
average = total_score/3

if average < 60:
    print("คะเเนนรวมของคุณ = ", total_score)
    print("คะเเนนเฉลี่ย 3 วิชา = , average")
    print("ควรปรับปรุง")
elif average > 80:
    print("คะเเนนรวมของคุณ = ", total_score)
    print("คะเเนนเฉลี่ย 3 วิชา = , average")
    print("ผ่านเกณฑ์")
else:
    print("คะเเนนรวมของคุณ = ", total_score)
    print("คะเเนนเฉลี่ย 3 วิชา = , average")
    print("ดีเยี่ยม")