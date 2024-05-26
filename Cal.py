def calculate_Gw(Lw,Pw):
    return Lw*Pw
def calculate_Gl(Ll,Pl):
    return Ll*Pl
def calculate_G(Ll,Pl,Lw,Pw):
    Gl=calculate_Gl(Ll,Pl)
    Gw=calculate_Gw(Lw,Pw)
    G=Gw+Gl
    return G
def calculate_C_BE(G,B,C_up,C_p,C_SOC_up,C_SOC_down,r):
    C = [C_SOC_down]
    BE = [B[0]-G[0]]
    if BE[0]>=0:
        BE[0]=BE[0]
    else:
        BE[0]=0
    C_in=[0]
    C_out=[0]
    for i in range(1, len(G)):
        C_outn=(B[i]-G[i])/r
        if C_outn<0:
            C_out.append(0)
        elif C_outn>=C_p:
            C_out.append(C_p)
            Cn= C[i-1]-C_out[i]
            if Cn<=C_SOC_down:
                C_out[i]=(C[i-1]-C_SOC_down)
                C.append(C_SOC_down)
            else:
                C_out[i]=C_out[i]
                C.append(Cn)
        else:
            C_out.append(C_outn)
            Cn= C[i-1]-C_out[i]
            if Cn<=C_SOC_down:
                C_out[i]=C[i-1]-C_SOC_down
                C.append(C_SOC_down)
            else:
                C_out[i]=C_out[i]
                C.append(Cn)
        C_inn=(G[i]-B[i])*r
        if C_inn<0:
            C_in.append(0)
        elif C_inn>=C_p:
            C_in.append(C_p*r)
            Cn=C[i-1]+C_in[i]
            if Cn>=C_SOC_up:
                C_in[i]=C_SOC_up-C[i-1]
                C.append(C_SOC_up)
            else:
                C_in[i]=C_in[i]
                C.append(Cn)
        else:
            C_in.append(C_inn)
            if Cn>=C_SOC_up:
                C_in[i]=C_SOC_up-C[i-1]
                C.append(C_SOC_up)
            else:
                C_in[i]=C_in[i]
                C.append(Cn)
        Ca_out = C_out[i]*r
        BEn = B[i] - (G[i] + Ca_out)
        if BEn <= 0:
            BE.append(0)
        else:
            BE.append(BEn)
        
    return C, BE
def calculate_An(G, B, C ,C_up, BE):
    A = [G[0]-B[0]-C_up]
    if A[0]<0:
        A[0]=0
    for i in range(1,len(G)):
        An = G[i] + (C[i-1] if i > 0 else 0) - B[i] - C_up
        if BE[i] != 0:
            A.append(0)
        elif An < 0:
            A.append(0)
        else:
            A.append(An)
    return A
def Pr_main(AP_main,BE):
    return AP_main*BE
def Pr_l(Ll,Pl,AP_l):
    Gl=calculate_Gl(Ll,Pl)
    Pr_l=AP_l*Gl
    return Pr_l
def Pr_w(Lw,Pw,AP_w):
    Gw=calculate_Gw(Lw,Pw)
    Pr_w=AP_w*Gw
    return Pr_w
def Pr_C(AcP,C_up):
    Pr_C_10year = AcP*C_up
    Pr_C = Pr_C_10year/365/10/24
    return Pr_C
def Pr_P(ApP,C_p):
    Pr_P_10year = ApP*C_p
    Pr_P = Pr_P_10year/365/10/24
    return Pr_P
def Pr_total(AP_main,BE,Gl,Gw,AcP,ApP,AP_l,AP_w,C_up,C_p,Pr_deploy_l,Pr_deploy_w):
    Pr_m=Pr_main(AP_main,BE)
    Pr_l1=Gl*AP_l
    Pr_w1=Gw*AP_w
    Pr_deploy_l = Pr_deploy_l
    Pr_deploy_w = Pr_deploy_w
    Pr_C1=Pr_C(AcP,C_up)
    Pr_P1=Pr_P(ApP,C_p)
    Pr_total=Pr_m+Pr_l1+Pr_w1+Pr_C1+Pr_P1+Pr_deploy_l+Pr_deploy_w
    return Pr_total
def calculate_Cost(Pr_total,B):
    return Pr_total/B