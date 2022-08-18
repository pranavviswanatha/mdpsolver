import numpy as np
import pulp
from pulp.apis import PULP_CBC_CMD
import random as rd
import argparse,sys,subprocess,os
parser = argparse.ArgumentParser()

############################################################
def vi(numStates,numActions,R,T,typ,discount,start,end):
    V=np.zeros(numStates)
    old=np.ones(numStates)
    ep=0.000000001
    while np.amax(np.abs(old-V))>=ep:
        old=np.copy(V)
        for s in range(numStates):
            temp=np.zeros(numActions)
            for a in range(numActions):
                temp[a]=sum((T[s][a][s_]*(R[s][a][s_]+discount*old[s_])) for s_ in range(numStates))
            V[s]=np.amax(temp)
        
        #print(V,old)
    Q=np.zeros((numStates,numActions))
    for s in range(numStates):
        for a in range(numActions):
            Q[s][a]=sum((T[s][a][s_]*(R[s][a][s_]+discount*V[s_]) for s_ in range(numStates)))
    policy=np.argmax(Q,axis=1)
    return V,policy    

############################################################
def lp(numStates,numActions,R,T,typ,discount,start,end):
    lp=pulp.LpProblem("mdp",pulp.LpMinimize)
    V=pulp.LpVariable.dict("V",range(numStates))
    S=np.array(range(numStates))
    Q=np.zeros((numStates,numActions))
    lp+=pulp.lpSum([V[s] for s in S])
    for s in range(numStates):
        for a in range(numActions):
            lp+=V[s] >= pulp.lpSum((T[s][a][s_]*(R[s][a][s_]+discount*V[s_])) for s_ in range(numStates))
    lp.solve(PULP_CBC_CMD(msg=0))
    #pulp.GUROBI(msg=0).solve(lp)
    for s in range(numStates):
        for a in range(numActions):
            Q[s][a]=sum((T[s][a][s_]*(R[s][a][s_]+discount*pulp.value(V[s_]))) for s_ in range(numStates))
    policy=np.argmax(Q,axis=1)
    v=np.zeros(numStates)
    for s in range(numStates):
        v[s]=pulp.value(V[s])
    return v,policy

###################################################################
def hpi(numStates,numActions,R,T,typ,discount,start,end):
    policy=np.zeros(numStates,dtype=int)
    old=np.ones(numStates,dtype=int)
    V=np.zeros(numStates)
    while not (old==policy).all():
        old=np.copy(policy)
        mat=np.zeros(numStates)#corresponding to V for the step
        mat_=np.zeros((numStates,numStates))#computation matrix
        Q=np.zeros((numStates,numActions))
        for s in range(numStates):
            a=policy[s]
            for s_ in range(numStates):
                mat_[s][s_]=-T[s][a][s_]*discount
                mat[s]+=R[s][a][s_]*T[s][a][s_]
        mat_+=np.eye(numStates)#V(s)=sigma(T[s,a,s'](R[s,a,s']+discount.V[s'])) in matrix form for V
        V=np.matmul(np.linalg.inv(mat_),mat)
        for s in range(numStates):
            for a in range(numActions):
                Q[s][a]=sum((T[s][a][s_]*(R[s][a][s_]+discount*V[s_]) for s_ in range(numStates)))
        policy=np.argmax(Q,axis=1)
    return V,policy

#####################################################################
if __name__ == "__main__":
    parser.add_argument("--mdp")
    parser.add_argument("--algorithm",default=hpi)
    args = parser.parse_args()
    with open(args.mdp) as f:
        lines=f.readlines()
        numStates=int(lines[0].split()[1])
        numActions=int(lines[1].split()[1])
        start=0
        end=list(map(int,lines[2].split()[1:]))
        typ=lines[-2].split()[1]
        discount=float(lines[-1].split()[1])
        R=np.zeros((numStates,numActions,numStates))
        T=np.zeros((numStates,numActions,numStates))
        for l in lines[3:-2]:
            l=l.split()
            R[int(l[1])][int(l[2])][int(l[3])]=float(l[4])
            T[int(l[1])][int(l[2])][int(l[3])]=float(l[5])
        #print(R,T)

        V=np.zeros(numStates)
        pi=np.zeros(numStates)
        if args.algorithm=="vi":
            V,pi=vi(numStates,numActions,R,T,typ,discount,start,end)
        elif args.algorithm=="lp":
            V,pi=lp(numStates,numActions,R,T,typ,discount,start,end)
        else:
            V,pi=hpi(numStates,numActions,R,T,typ,discount,start,end)
        
        for i in range(numStates):
            print(V[i],pi[i])