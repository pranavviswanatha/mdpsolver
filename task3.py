import random,argparse,sys,subprocess,os
import subprocess
import filecmp
import numpy as np


def encoder(policy, player, out):
    cmd_encoder = "python","encoder.py","--policy",policy,"--states","data/attt/states/states_file_p"+str(player)+".txt" 
    #print("\n","Generating the MDP encoding using encoder.py")
    f = open(out,'w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

def policy_value(mdpfile,out):
    cmd_planner = "python","planner.py","--mdp",mdpfile
    #print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open(out,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

def decoder(val, player, out):
    cmd_decoder = "python","decoder.py","--value-policy",val,"--states","data/attt/states/states_file_p"+str(player)+".txt" ,"--player-id",str(player)
    f = open(out,'w')
    subprocess.call(cmd_decoder,stdout=f)
    f.close()

def run(policy1,player,policy2):
    output= 'output.txt'
    val = 'val.txt'
    encoder(policy1, player, output)    
    policy_value(output, val)
    decoder(val, player, policy2)

if __name__ == '__main__':
    for i in range(10):
        pol0 = 'policy1_' +str(i-1) + '.txt'
        pol1 = 'policy2_' +str(i) + '.txt'
        pol2 = 'policy1_' + str(i) +'.txt'
        if i>0:
            run(pol0 ,2 ,pol1)
        run(pol1,1,pol2) 
    for i in range(1,10):
        pol0 = 'policy2_' +str(i-1) + '.txt'
        pol1 = 'policy2_' +str(i) + '.txt' 
        if not filecmp.cmp(pol0,pol1,shallow= False):
            print(pol0+"not same as"+pol1)
    for i in range(1,10):
        pol0 = 'policy1_' +str(i-1) + '.txt'
        pol1 = 'policy1_' +str(i) + '.txt' 
        if not filecmp.cmp(pol0,pol1,shallow= False):
            print(pol0+"not same as"+pol1)