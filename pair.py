#!/usr/bin/env python 
import os 
import numpy as np 

# Score function 
def Score(u, v): 
    if (u,v) in [ ('A','U'), ('U','A') ]: 
        return 2 
    if (u,v) in [ ('G','C'), ('C','G') ]: 
        return 3 
    return 0 

# Traceback 
def TraceBack(i,j): 
    pairs = [] 
    def TcBk(i, j): 
        i = int(i) 
        j = int(j) 
        if i <= j: 
            if 0 == fTb[i,j]: 
                return 
            elif -1 == kTb[i,j]: 
                pairs.append((i,j)) 
                TcBk(i+1, j-1) 
            elif -2 == kTb[i,j]: 
                TcBk(i+1, j-1) 
            else: 
                TcBk(i,kTb[i,j]) 
                TcBk(kTb[i,j]+1,j) 
    TcBk(i,j)
    return pairs 

def in2ele(list):
    for i in range(0,len(list)): 
        u = seq[list[i][0]] 
        v = seq[list[i][1]] 
        del list[i]
        list.insert(i,(u,v)) 
    return list 

# print function 
def printSol(pairs): 
    sol = ['.'] * len(seq) 
    for each in pairs: 
        sol[ each[0] ] = '{' 
        sol[ each[1] ] = '}' 
    print('>' + seq + '\n' + ' ' + ''.join(sol) + '\n>' + 'max count of pairs\n' + ' ' + str(len(pairs)) + '\n>' + 'max score\n' + ' ' + str(int(fTb[0][-1])) + '\n' ) 

def main(): 
    global seq 
    global fTb 
    global kTb 

    # read input 
    cwd = os.getcwd() + '/sequence.txt' 
    readFile = open( cwd, 'r' ) 
    for eachLine in readFile: 
        if eachLine[0] == '>': 
            seq = readFile.next().strip() 
    readFile.close() 

    # DP, function-table, k-table  
    n = len(seq) 
    fTb = np.zeros((len(seq), len(seq))) 
    kTb = np.zeros((len(seq), len(seq))) 

    # inside-out 
    for l in range(0,n): 
        for i in range(0,n-l): 
            j = i+l 
            for k in range(i,j): 
                func2 = fTb[i,k] + fTb[k+1,j] 
                if func2 > fTb[i,j]: 
                    fTb[i,j] = func2 
                    kTb[i,j] = k 
            # left-right 
            if Score(seq[i],seq[j]): 
                # if 3 between A-U 
                if 'A' == seq[i] and 'U' == seq[j] : 
                    poPairs = in2ele(TraceBack(i+1,j-1)) 
                    if ('U','A') and ('G','C') and ('C','G') in poPairs : 
                        func1 = fTb[i+1,j-1] + Score(seq[i],seq[j]) 
                        if func1 >= fTb[i,j]: 
                            fTb[i,j] = func1 
                            kTb[i,j] = -1 
                    else: 
                        func1 = fTb[i+1,j-1] 
                        if func1 > fTb[i,j]: 
                            fTb[i,j] = func1 
                            kTb[i,j] = -2 
                else: 
                    func1 = fTb[i+1,j-1] + Score(seq[i],seq[j]) 
                    if func1 >= fTb[i,j]: 
                        fTb[i,j] = func1 
                        kTb[i,j] = -1 

    pairs = TraceBack(0, n-1) 
    printSol(pairs) 
    print fTb
    print kTb

if __name__ == '__main__': 
    main() 
    