#! usr/bin/python3
# --- root ---
import time, datetime, sys, re, subprocess

# opts_reg = re.compile(r"(-{,2})(\w+)(?: )?([^-\r\n]*\b[!-/:-@[-`{-~]?)") #TODO if " " raise, if "-" "o"[-1], if "--" dict?
# opts_list = re.findall(opts_reg, (" ".join(sys.argv[1:]))) #Group 1 is the selector, g2 is the flag, g3 is any argument

optcheck_dict = {'p': [False,], 'y': [False,], 'x': [False,], 'f': [False,], 's': [False,], 'o': [False,], 'c': [False, 1], 'd': [False,], 'h': [False,], 'b':[False,], 't':[False,]}
longargs_dict = {"periods": "p", "cycles": "y", "execute": "x", "finishcyc": "f", "finishsim": "s", "output": "o", "config": "c", "display": "d", "help": "h", "execboth": "b", "cmdout": "t"}
# --- option testing ---
reg = ''
def arghandle():
    global reg
    for i in sys.argv[1:]:
        m = re.search(r"^(-|--)(\w+)$", i)
        if m and m.groups()[0] == "-":
                arg_s(m.groups()[1])
        elif m and m.groups()[0] == "--":
                arg_l(m.groups()[1])
        elif not reg == '':
                arg_ap(i)
        else: print(f"Unknown option {i}. Did you forget a flag?")

def arg_s(options):
    global reg
    for x in options:
        if str(x) in optcheck_dict:
            optcheck_dict.update({x: [True,]})
            if x == options[-1]: reg = x
        else: print(f"Unknown option -{x}") 

def arg_l(option):
    global reg
    if option in longargs_dict:
        optcheck_dict.update({longargs_dict[option]: [True,]})
        reg = longargs_dict[option]
    else: print(f"Unknown option --{option}") 

def arg_ap(argument):
    global reg
    if reg in optcheck_dict:
        optcheck_dict[reg].append(argument)

arghandle()
# --- argument eval ---
period_reg = "(\d*)([d|h|m|s])"
period_tup = re.findall(period_reg, optcheck_dict["p"][1])

span_dict = {'d': 'days', 'h': 'hours','m': 'minutes','s': 'seconds'}
period_list = [list(ele) for ele in period_tup]

for x in period_list:
    if x[1] in span_dict:
     x[1] = span_dict[x[1]]   

# ---exec---
def exec(which):
    if optcheck_dict[which][0] == True:
        if optcheck_dict['t'][0] == True:
            p = subprocess.Popen(optcheck_dict[which][1].split(" "))
        else: p = subprocess.Popen(optcheck_dict[which][1].split(" "), stdout=subprocess.DEVNULL)

# ---timer function---
def timer(dur, disp, num, cyc=0, out=''):
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
        print(f"Done with period {num}, cycle {cyc}, {dur}.")

c_len=0
while c_len < int(optcheck_dict["c"][1]):
    p_len=0
    for i in period_list:
        timer(eval(f"datetime.timedelta({i[1]}={i[0]})"), optcheck_dict["d"][0], p_len, c_len)
        p_len += 1
        if optcheck_dict['b'][0] == False:
            if p_len < len(period_list) or len(period_list) == 1: exec("x")
        else: exec("x")
    c_len += 1
    exec("f")
exec('s')
# ---