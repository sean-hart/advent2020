policy = [
"1-3 a: abcde",
"1-3 b: cdefg",
"2-9 c: ccccccccc"
]

for line in (policy):
    num,name,letters = line.split()
    if len(num) == 4:
        print ("more than one digit place")
        min_num = num[0]
        dig1 = num[2]
        dig2 = num[3]
        max_num = dig1 + dig2 
        #print (num, min_num, max_num)
    else:
        print ("only one digit")
        min_num = num[0]
        max_num = num[2]
        #print (num, min_num, max_num)

