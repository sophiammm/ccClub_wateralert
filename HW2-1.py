# v0 = 1
# ques = input()
# for i in range(len(ques)):
#     if ques[0] == ",":
#         ques = " " + ques
#     if ques[-1] == ",":
#         ques = ques + " " 
#     if ",," in ques:
#         ques = ques.replace(",,", ", ,")

# element = ques.split(",")  
# # print(element[0])
# # print(element[1])
# # print(element[2])
# # print(element[3])

# v = float(element[0]) if element[0] != " " else "NA"
# a = float(element[1]) if element[1] != " " else "NA"
# s = float(element[2]) if element[2] != " " else "NA"
# t = float(element[3]) if element[3] != " " else "NA"

# raw_ans = [v,a,s,t]

# for j in range(len(raw_ans)):
#     if raw_ans[j] != "NA":
#         continue
#     else:
#         if j == 0:
#             v = 1 + a * t
#         elif j == 1:
#             if raw_ans[2] != "NA" and s != 0:
#                 a = (v **2 - 1) / (2 * s)
#             elif raw_ans[3] != "NA" and t != 0:
#                 a = (v - 1) / t
#         elif j == 2:
#             s = t + (a * (t ** 2) * 0.5)
#         elif j == 3:
#             if raw_ans[1] != "NA" and a != 0:
#                 t = (v - 1) / a
#             elif raw_ans[2] != "NA":
#                 t = (2 * s) / (v + 1)

# ans = "v="+str(v) + ", v0=1.0" + ", a="+str(a) + ", s="+str(s) + ", t="+str(t)
# print(ans)


v0 = 1
ques = input()

element = ques.split(",")  
# print(element[0])
# print(element[1])
# print(element[2])
# print(element[3])

v = float(element[0]) if element[0] != "" else "NA"
a = float(element[1]) if element[1] != "" else "NA"
s = float(element[2]) if element[2] != "" else "NA"
t = float(element[3]) if element[3] != "" else "NA"

if v == "NA":
    if a != "NA" and s != "NA":
        v = ((2 * a * s) + 1) ** 0.5
    elif a != "NA" and t != "NA":
        v = 1 + a * t
    elif s != "NA" and t != "NA":
        v = ((2 * s) / t) - 1
if a == "NA":        
    if v != "NA" and s != "NA" and s != 0:
        a = (v ** 2 - 1) / (2 * s)
    elif v != "NA" and t != "NA" and t != 0:
        a = (v - 1) / t
    elif s != "NA" and t != "NA" and t != 0:
        a = 2 * (s - t) / (t ** 2)
if s == "NA":        
    if a != "NA" and t != "NA":
        s = t + (a * (t ** 2) * 0.5)
    elif v != "NA" and a != "NA" and a != 0:
        a = (v ** 2 - 1) / 2 * a
    elif t != "NA" and v != "NA": 
        a = t * (v + 1) / 2
if t == "NA":
    if v != "NA" and a != "NA" and a != 0:
        t = (v - 1) / a
    elif s != "NA" and v != "NA":
        t = (2 * s) / (v + 1)

ans = "v="+str(v) + ", v0=1.0" + ", a="+str(a) + ", S="+str(s) + ", t="+str(t)
print(ans)