#! usr/bin/python3
# --- root ---
import time, datetime, sys, re

opts_reg = re.compile(r"(-{,2})(\w+)(?: )?([^-\r\n]*\b[!-/:-@[-`{-~]?)") #TODO if " " raise, if "-" "o"[-1], if "--" dict?
opts_list = re.findall(opts_reg, (" ".join(sys.argv[1:]))) #Group 1 is the selector, g2 is the flag, g3 is any argument

optcheck_dict = {'p': [False,], 'y': [False,], 'x': [False,], 'f': [False,], 'o': [False,], 'c': [False, 0], 'd': [False,], 'h': [False,]}
longargs_dict = {"periods": "p", "cycles": "y", "execute": "x", "finished": "f", "output": "o", "config": "c", "display": "d", "help": "h"}
# --- option testing ---
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
#optargs_true = ("p","y","x","f","o","c") 

# --- argument eval ---
period_reg = re.compile("(\d*)([d|h|m|s])")
period_tup = re.findall(period_reg, optcheck_dict["p"][1])
span_dict = {'d': 'days', 'h': 'hours','m': 'minutes','s': 'seconds'}
period_list = [list(ele) for ele in period_tup]

for x in period_list:
    if x[1] in span_dict:
     x[1] = span_dict[x[1]]   
print(period_list)

# ---timer function---
def timer(dur, disp, num, cyc=1, out=''):
    start_time = (datetime.datetime.now())
    end_time = start_time + dur
    while (datetime.datetime.now() < end_time):
        remaining = (end_time - (datetime.datetime.now()))
        if disp == True:
            print(f"{(remaining.days*86400)+remaining.seconds}       ", end='\r')
        if out != '':
            print(out)
        if disp == True or out != '': time.sleep(1)
        else: time.sleep(remaining.seconds)
    if disp == True:
        print(f"Done with period {num}, {cyc}, {dur}.")

c_len=0
while c_len != optcheck_dict["c"][1]:
    p_len=0
    for x in period_list:
        timer(eval(f"datetime.timedelta({x[1]}={x[0]})"), optcheck_dict["d"][0], p_len)
        p_len += 1
    c_len += 1