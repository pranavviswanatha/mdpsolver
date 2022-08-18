import numpy as np
import random as rd
import argparse,sys,subprocess,os
parser = argparse.ArgumentParser()

opp=dict()
states=dict()
lines=[]
numStates=0
def check(s):
    for i in range(9):
        if s[i]=="0":
            return True
    return False

def ready(s):
    for i in range(3):
        if s[i*3]==s[i*3+1] and s[i*3+1] == s[i*3+2] and s[i*3] != "0":
            return 1.0
        if s[i]==s[3+i] and s[3+i] == s[6+i] and s[i] != "0":
            return 1.0
    if s[0]==s[4] and s[4] == s[8] and s[0] != "0":
        return 1.0
    if s[2]==s[4] and s[4] == s[6] and s[4] != "0":
        return 1.0
    for i in range(9):
        if s[i]=="0":
            return -1
    return 0.0

def transition(j,s,p,n):
    grid=j
    for i in range(3):
        if grid[i*3]==grid[i*3+1] and grid[i*3+1] == grid[i*3+2] and grid[i*3] != "0":
            return
        #print(grid[i],grid[3+i],grid[6+i])
        if grid[i]==grid[3+i] and grid[3+i] == grid[6+i] and grid[i] != "0":
            return
    if grid[0]==grid[4] and grid[4] == grid[8] and grid[0] != "0":
        return
    if grid[2]==grid[4] and grid[4] == grid[6] and grid[4] != "0":
        return
    for i in range(3):
        if s[i*3]==s[i*3+1] and s[i*3+1] == s[i*3+2] and s[i*3] != "0":
            print("transition",states[j],n,numStates-1,0.0,1.0)
            return
        #print("helo",s[i],s[i+3],s[i+6])
        if s[i]==s[3+i] and s[3+i] == s[6+i] and s[i] != "0":
            print("transition",states[j],n,numStates-1,0.0,1.0)
            return
    if s[0]==s[4] and s[4] == s[8] and s[0] != "0":
        print("transition",states[j],n,numStates-1,0.0,1.0)
        return
    if s[2]==s[4] and s[4] == s[6] and s[4] != "0":
        print("transition",states[j],n,numStates-1,0.0,1.0)
        return
    if not check(s):
        print("transition",states[j],n,numStates-1,0.0,1.0)
        return
    for i in range(9):
        if opp[s][i]>0:
            t=s[:i]+p+s[i+1:]
            boolean=ready(t)
            if boolean==-1:
                print("transition",states[j],n,states[t],0.0,opp[s][i])
            else:
                print("transition",states[j],n,numStates-1,boolean,opp[s][i])
        elif s[i]!="0":
            print("transition",states[j],n,numStates-1,-1.0,1.0)
    return

if __name__ == "__main__":
    parser.add_argument("--policy")
    parser.add_argument("--states")
    args = parser.parse_args()
    ln=[]
    with open(args.states) as f:
        ln=f.readlines()
        for i,t in enumerate(ln):
            ln[i]=ln[i].strip()
            states[ln[i]]=i
    numStates=len(ln)+1
    player=0
    p_=0
    print("numStates",numStates)
    print("numActions",9)
    #print("start",0)
    print("end",numStates-1)
    with open(args.policy) as f:
        lines=f.readlines()
        p_=lines[0].strip()
        if p_=="1":
            player='2'
        else:
            player='1'
        lines=lines[1:]
    for i,t in enumerate(lines):
        lines[i]=lines[i].split()
        for n in range(1,10):
            lines[i][n]=float(lines[i][n].strip())
        opp.update({lines[i][0]:lines[i][1:]})
    for i in states:
        t=i
        for n in range(9):
            if t[n]=='0':
                s=t[:n]+player+t[n+1:]
                transition(i,s,p_,n)
            else:
                print("transition",states[i],n,numStates-1,-1.0,1.0)
    print("mdptype","episodic")
    print("discount",1.0)