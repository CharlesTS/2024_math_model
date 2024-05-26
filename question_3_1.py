import pandas as pd
import numpy as np
import Cal
import cost
import matplotlib.pyplot as plt

df1 = pd.read_excel("附件1.xlsx")
df2 = pd.read_excel("附件2.xlsx")
df3 = pd.read_excel("附件3.xlsx")
df4 = pd.read_excel("A_2.xlsx")
print(f"Length of df1: {len(df1)}, df2: {len(df2)}, df3: {len(df3)}, df4: {len(df4)}")
AP_main = 1
AP_l = 0.4
AP_w = 0.5
AcP = 1800
ApP = 800
Pl_A = 750
Pw_A = 0
Pl_B = 0
Pw_B = 1000
Pl_C = 600
Pw_C = 500
Pl_hole = 1350
Pw_hole = 1500
C_p = 50
C_up = 100
SOC_down = 0.1
SOC_up = 0.9
r = 0.95
AlP = 2500
AwP = 3000
B_A = df1.iloc[:, 1] * 1.5
B_B = df1.iloc[:, 2] * 1.5
B_C = df1.iloc[:, 3] * 1.5
B_hole = df4.iloc[:, 1] * 1.5
print(f"Length of B_A: {len(B_A)}, B_B: {len(B_B)}, B_C: {len(B_C)}, B_hole: {len(B_hole)}")
Ll_A = df2.iloc[:, 1]
Lw_A = 0
Ll_B = 0
Lw_B = df2.iloc[:, 2]
Ll_C = df2.iloc[:, 3]
Lw_C = df2.iloc[:, 4]
print(f"Length of Ll_A: {len(Ll_A)}, Lw_B: {len(Lw_B)}, Ll_C: {len(Ll_C)}, Lw_C: {len(Lw_C)}")
C_SOC_up = SOC_up * C_up
C_SOC_down = SOC_down * C_up
G_A = Cal.calculate_G(Ll_A, Pl_A, Lw_A, Pw_A)
Gl_A = Cal.calculate_Gl(Ll_A, Pl_A)
Gw_A = Cal.calculate_Gw(Lw_A, Pw_A)
G_B = Cal.calculate_G(Ll_B, Pl_B, Lw_B, Pw_B)
Gl_B = Cal.calculate_Gl(Ll_B, Pl_B)
Gw_B = Cal.calculate_Gw(Lw_B, Pw_B)
G_C = Cal.calculate_G(Ll_C, Pl_C, Lw_C, Pw_C)
Gl_C = Cal.calculate_Gl(Ll_C, Pl_C)
Gw_C = Cal.calculate_Gw(Lw_C, Pw_C)
print(f"Length of G_A: {len(G_A)}, G_B: {len(G_B)}, G_C: {len(G_C)}")
G = G_A + G_B + G_C
Gl = Gl_A + Gl_B + Gl_C
Gl_max = max(Gl)
Pr_deploy_l = (AlP * Gl_max) / 5 / 365 / 24
Gw = Gw_A + Gw_B + Gw_C
Gw_max = max(Gw)
Pr_deploy_w = (AwP * Gw_max) / 5 / 365 / 24
min_length = min(len(G), len(B_hole))
G = G[:min_length]
B_hole = B_hole[:min_length]
Gl = Gl[:min_length]
Gw = Gw[:min_length]
Pr_total_hole, Cost_hole = cost.cost(G, Gl, Gw, B_hole, C_up, C_p, C_SOC_up, C_SOC_down, r, AP_main, AcP, ApP, AP_l, AP_w, Pr_deploy_l, Pr_deploy_w)
a = sum(Pr_total_hole)
print(a)
C_p_lr_values = []
a_values = []
current_C_p_lr = 0
lr = 0.1
max_C_p_lr = 200
while current_C_p_lr <= max_C_p_lr:
    C_p_lr_values.append(current_C_p_lr)
    Pr_total_hole, _ = cost.cost(G, Gl, Gw, B_hole, C_up, current_C_p_lr, C_SOC_up, C_SOC_down, r, AP_main, AcP, ApP, AP_l, AP_w, Pr_deploy_l, Pr_deploy_w)
    a = sum(Pr_total_hole)
    a_values.append(a)
    current_C_p_lr += lr
plt.plot(C_p_lr_values, a_values)
plt.xlabel('C_p_lr_values')
plt.ylabel('sum of Pr_total_A')
plt.title('Line plot of C_p_lr_values and a_values')
plt.show()
min_a = min(a_values)
min_a_index = a_values.index(min_a)
min_a_C_p_lr = C_p_lr_values[min_a_index]
print(min_a, min_a_C_p_lr)