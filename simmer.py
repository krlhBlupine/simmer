#! usr/bin/python3

import time, datetime, sys, re

start_time = time.time()

opts_reg = re.compile(r"(-{,2})(\w+)(?: )?([^-\r\n]*\b[!-/:-@[-`{-~]?)") #TODO if " " raise, if "-" "o"[-1], if "--" dict?
opts_list = re.findall(opts_reg, (" ".join(sys.argv[1:]))) #Group 1 is the selector, g2 is the flag, g3 is any argument

optcheck_dict = {'p': [False,], 'y': [False,], 'x': [False,], 'f': [False,], 'o': [False,], 'c': [False,], 'd': [False,], 'h': [False,]}
longargs_dict = {"periods": "p", "cycles": "y", "execute": "x", "finished": "f", "output": "o", "config": "c", "display": "d", "help": "h"}

def flagtest(i):
    if i == "--":
        return 1
    elif i == "-":
        return 0
    else:
        raise Exception("Options must always be marked with '-', or '--' for their long counterparts.")

def cmdtest_s(i, j): #TODO
    for x in i:
        if str(x) in optcheck_dict:
            optcheck_dict.update({x: [True,]})
            if x == i[-1]:
                optcheck_dict.update({x: [True, j]})    
        else: raise Exception(f"Unknown option {x}.")

def cmdtest_l(i, j): #TODO 
    if i in longargs_dict:
        optcheck_dict.update({longargs_dict[i]: [True, j]})
    else: raise Exception(f"Unknown option {i}.")

def opttest():
    for x in opts_list:
        if flagtest(x[0]):
            cmdtest_l(x[1], x[2])
        else:
            cmdtest_s(x[1], x[2])

opttest()
print(optcheck_dict)
#optargs_true = ("p","y","x","f","o","c") 
