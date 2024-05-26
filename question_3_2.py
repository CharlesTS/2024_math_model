import os
import pandas as pd
import numpy as np
import Cal
import cost
import matplotlib.pyplot as plt

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

try:
    df1 = pd.read_excel("附件1.xlsx")
    df2 = pd.read_excel("附件2.xlsx")
    df3 = pd.read_excel("附件3.xlsx")
    df4 = pd.read_excel("A_2.xlsx")
except FileNotFoundError as e:
    print("Error: File not found. Please check the file path and name.")
    print(e)
    exit()

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

# Convert columns to numeric, coerce errors to NaN
B_A = pd.to_numeric(df1.iloc[:, 1], errors='coerce')
B_B = pd.to_numeric(df1.iloc[:, 2], errors='coerce')
B_C = pd.to_numeric(df1.iloc[:, 3], errors='coerce')
B_hole = pd.to_numeric(df4.iloc[:, 1], errors='coerce')
Ll_A = pd.to_numeric(df2.iloc[:, 1], errors='coerce')
Lw_A = 0
Ll_B = 0
Lw_B = pd.to_numeric(df2.iloc[:, 2], errors='coerce')
Ll_C = pd.to_numeric(df2.iloc[:, 3], errors='coerce')
Lw_C = pd.to_numeric(df2.iloc[:, 4], errors='coerce')

# Drop rows with NaN values
B_A = B_A.dropna()
B_B = B_B.dropna()
B_C = B_C.dropna()
B_hole = B_hole.dropna()
Ll_A = Ll_A.dropna()
Lw_B = Lw_B.dropna()
Ll_C = Ll_C.dropna()
Lw_C = Lw_C.dropna()

C_SOC_up = SOC_up * C_up
C_SOC_down = SOC_down * C_up

print(f"Length of B_A: {len(B_A)}, B_B: {len(B_B)}, B_C: {len(B_C)}, B_hole: {len(B_hole)}")
print(f"Length of Ll_A: {len(Ll_A)}, Lw_B: {len(Lw_B)}, Ll_C: {len(Ll_C)}, Lw_C: {len(Lw_C)}")

G_A = Cal.calculate_G(Ll_A, Pl_A, Lw_A, Pw_A)
Gl_A = Cal.calculate_Gl(Ll_A, Pl_A)
Gw_A = Cal.calculate_Gw(Lw_A, Pw_A)
G_B = Cal.calculate_G(Ll_B, Pl_B, Lw_B, Pw_B)
Gl_B = Cal.calculate_Gl(Ll_B, Pl_B)
Gw_B = Cal.calculate_Gw(Lw_B, Pw_B)
G_C = Cal.calculate_G(Ll_C, Pl_C, Lw_C, Pw_C)
Gl_C = Cal.calculate_Gl(Ll_C, Pl_C)
Gw_C = Cal.calculate_Gw(Lw_C, Pw_C)

print(f"Type of G_A: {type(G_A)}, length: {len(G_A) if hasattr(G_A, '__len__') else 'N/A'}")
print(f"Type of G_B: {type(G_B)}, length: {len(G_B) if hasattr(G_B, '__len__') else 'N/A'}")
print(f"Type of G_C: {type(G_C)}, length: {len(G_C) if hasattr(G_C, '__len__') else 'N/A'}")
print(f"Type of Gl_A: {type(Gl_A)}, length: {len(Gl_A) if hasattr(Gl_A, '__len__') else 'N/A'}")
print(f"Type of Gl_B: {type(Gl_B)}, length: {len(Gl_B) if hasattr(Gl_B, '__len__') else 'N/A'}")
print(f"Type of Gl_C: {type(Gl_C)}, length: {len(Gl_C) if hasattr(Gl_C, '__len__') else 'N/A'}")
print(f"Type of Gw_A: {type(Gw_A)}, length: {len(Gw_A) if hasattr(Gw_A, '__len__') else 'N/A'}")
print(f"Type of Gw_B: {type(Gw_B)}, length: {len(Gw_B) if hasattr(Gw_B, '__len__') else 'N/A'}")
print(f"Type of Gw_C: {type(Gw_C)}, length: {len(Gw_C) if hasattr(Gw_C, '__len__') else 'N/A'}")

min_length = min(len(B_A), len(B_B), len(B_C), len(B_hole), len(Ll_A), len(Lw_B), len(Ll_C), len(Lw_C))
B_A = B_A[:min_length]
B_B = B_B[:min_length]
B_C = B_C[:min_length]
B_hole = B_hole[:min_length]
Ll_A = Ll_A[:min_length]
Lw_B = Lw_B[:min_length]
Ll_C = Ll_C[:min_length]
Lw_C = Lw_C[:min_length]
G_A = G_A[:min_length] if hasattr(G_A, '__len__') else [G_A] * min_length
G_B = G_B[:min_length] if hasattr(G_B, '__len__') else [G_B] * min_length
G_C = G_C[:min_length] if hasattr(G_C, '__len__') else [G_C] * min_length
Gl_A = Gl_A[:min_length] if hasattr(Gl_A, '__len__') else [Gl_A] * min_length
Gl_B = Gl_B[:min_length] if hasattr(Gl_B, '__len__') else [Gl_B] * min_length
Gl_C = Gl_C[:min_length] if hasattr(Gl_C, '__len__') else [Gl_C] * min_length
Gw_A = Gw_A[:min_length] if hasattr(Gw_A, '__len__') else [Gw_A] * min_length
Gw_B = Gw_B[:min_length] if hasattr(Gw_B, '__len__') else [Gw_B] * min_length
Gw_C = Gw_C[:min_length] if hasattr(Gw_C, '__len__') else [Gw_C] * min_length

G = np.array(G_A) + np.array(G_B) + np.array(G_C)
Gl = np.array(Gl_A) + np.array(Gl_B) + np.array(Gl_C)
Gw = np.array(Gw_A) + np.array(Gw_B) + np.array(Gw_C)

AlP = 2500
AwP = 3000
Gl_max = max(Gl)
Gw_max = max(Gw)
Pr_deploy_l = (AlP * Gl_max) / 5 / 365 / 24
Pr_deploy_w = (AwP * Gw_max) / 5 / 365 / 24

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
