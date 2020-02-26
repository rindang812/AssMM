import pulp
from readdata import *

import os

path = "E:/E/HKII NĂM 2/MÔ HÌNH HÓA TOÁN HỌC/MHH/dataset02"
FJoin = os.path.join
files = [FJoin(path, f) for f in os.listdir(path)]


data1 = []
data2 = []                                 
data3 = []

for i in files:
    path1 = i
    N = 10000000000000000000
    n, m, M, alpha, beta, T, epsilon, S_u, V_u, confirms, S_o, V_o = getData(path1)

    # ----------------------- MODEL 1---------------------------------
    model = pulp.LpProblem("Model_1", pulp.LpMinimize)



    # ---------------------- Các biến trong model 1
    # ------------------------------
    z_v = pulp.LpVariable('z_v', lowBound= 0)

    sigma = pulp.LpVariable('sigma', cat='Binary')

    x = {}
    for i in range(n):
        x[i] = pulp.LpVariable('x[%s]' % i, cat= 'Binary')
        
    sizeInput = pulp.lpSum([S_u[i] * x[i] for i in range(n)])
    sizeOutput = pulp.lpSum([S_o[j] for j in range(m)])
    valueInput = pulp.lpSum([V_u[i] * x[i] for i in range(n)])
   

    valueOutput = pulp.lpSum([V_o[j] for j in range(m)])
    fee = alpha * (sizeInput + sizeOutput + beta * sigma)


    # ---------------------- Hàm mục tiêu ---------------------------
    # Tối ưu size giao dịch
    model +=  sizeInput + sizeOutput + beta * sigma
    # ---------------------- Ràng buộc ---------------------------
    # Kích thước giao dịch không được vượt quá kích thước khối dữ liệu tối đa
    model += sizeInput + sizeOutput + beta * sigma <= M
    # Một giao dịch phải có đủ giá trị tiêu thụ
    model += valueInput == valueOutput + fee + z_v
    # Tất cả đầu ra giao dịch phải lớn hơn ngưỡng DUST
    model += pulp.lpSum([V_o[j] for j in range(m)]) >= T

    # Nếu z_v >= epsilon thì z_s = 34, ngược lại thì z_s = 0
    model += z_v >= epsilon + 0.001 - N * (1 - sigma)
    model += z_v <= epsilon + N * sigma



    # -------------------------- Tối ưu ---------------------------------
    model.solve()

 










    #---------------Model 2-----------
    prob = pulp.LpProblem("Model_2", pulp.LpMaximize)



    #Các tham số truyền vào như model 1, chỉ thêm tham số gamma và ymin để xác
    #định được size tối đa của model 2
    gamma = 0.1
    ymin = pulp.value(model.objective)  # Lấy từ kết quả tối ưu của model 1




    #----------- Các biến của Model 2 ----------
    z_v = pulp.LpVariable('z_v', lowBound= 0)

    sigma = pulp.LpVariable('sigma', cat='Binary')

    x = {}
    for i in range(n):
        x[i] = pulp.LpVariable('x[%s]' % i, cat= 'Binary')
        
    sizeInput = pulp.lpSum([S_u[i] * x[i] for i in range(n)])

    sizeOutput = pulp.lpSum([S_o[j] for j in range(m)])

    valueInput = pulp.lpSum([V_u[i] * x[i] for i in range(n)])

    valueOutput = pulp.lpSum([V_o[j] for j in range(m)])

    fee = alpha * (sizeInput + sizeOutput + beta * sigma)
    y = sizeInput + sizeOutput + beta * sigma





    # ---------------------- OBJECTIVE FUNCTION ---------------------------
    # Tìm số lượng tối đa mà UTXO được chọn để thu hẹp lại kích thước của nhóm
    # UTXO ban đầu
    prob += pulp.lpSum([1 * x[i] for i in range(n)]) - sigma



    # ---------------------- Ràng buộc ---------------------------
    # Kích thước giao dịch không được vượt quá kích thước khối dữ liệu tối đa
    prob += sizeInput + sizeOutput + beta * sigma <= M
    # Một giao dịch phải có đủ giá trị tiêu thụ
    prob += valueInput == valueOutput + fee + z_v 
    # Tất cả đầu ra giao dịch phải lớn hơn ngưỡng DUST
    prob += pulp.lpSum([V_o[j] for j in range(m)]) >= T
    #Nếu z_v >= epsilon thì z_s = 34, ngược lại thì z_s = 0
    prob += z_v >= epsilon + 0.001 - N * (1 - sigma)
    prob += z_v <= epsilon + N * sigma
    #Xác định size tối đa để lựa chọn được số lượng tối đa các UTXO
    prob += y <= (1 + gamma) * ymin




    # ------------ Tối ưu -----------
    prob.solve()

    if (n == 1):
        data1.append(pulp.value(prob.objective))
    elif (n >= 2 and n <= 1000):
        data2.append(pulp.value(prob.objective))
    else:
        data3.append(pulp.value(prob.objective))
    
   


    



   

sum1 = 0
sum2 = 0
sum3 = 0
for i in data1:
    sum1 = sum1 + i
for i in data2:
    sum2 = sum2 + i
for i in data3:
    sum3 = sum3 + i

print("DS1: ",sum1)  
print("DS2: ",sum2)  
print("DS3: ",sum3)







