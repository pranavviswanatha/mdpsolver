import numpy as np
import random as rd
import argparse,sys,subprocess,os
parser = argparse.ArgumentParser()

if __name__ == "__main__":
    parser.add_argument("--value-policy")
    parser.add_argument("--states")
    parser.add_argument("--player-id")
    args = parser.parse_args()
    lines=[]
    ln=[]
    with open(args.value_policy) as f:
        lines=f.readlines()
    with open(args.states) as f:
        ln=f.readlines()
    print(args.player_id)
    #print(lines,ln)
    for i,t in enumerate(ln):
        x=[0 for i in range(9)]
        x[int(lines[i].split()[1])]=1
        print(t.strip(),x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])