#sample: [1, 3, 1, 5, 8, 2, 6, 4, 9, 6, 1, 4]
input_list=list(map(int,input().split(",")))

result=[]
result.append(input_list[0])
for i in range(1,len(input_list)-1):
    if input_list[i-1]<=input_list[i] and result[-1]<=input_list[i]:
        result.append(input_list[i])

#sample: [1, 3, 5, 8, 9]
print(result)