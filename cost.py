import Cal
def cost(G_A,Gl,Gw,B_A,C_up,C_p,C_SOC_up,C_SOC_down,r,AP_main,AcP,ApP,AP_l,AP_w,Pr_deploy_l,Pr_deploy_w):
    C_A,BE_A=Cal.calculate_C_BE(G_A,B_A,C_up,C_p,C_SOC_up,C_SOC_down,r)
    A_A = Cal.calculate_An(G_A, B_A, C_A,C_up, BE_A)
    Pr_total_A=Cal.Pr_total(AP_main,BE_A,Gl,Gw,AcP,ApP,AP_l,AP_w,C_up,C_p,Pr_deploy_l,Pr_deploy_w)
    Cost_A=Cal.calculate_Cost(Pr_total_A,B_A)
    return Pr_total_A,Cost_A