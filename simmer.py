#! usr/bin/python3
# --- root ---
import time, datetime, sys, re, subprocess, shlex

optcheck_dict = {
 'p': [False,''], 'y': [False,1 ], 'N': [False,  ],
 'x': [False,''], 'f': [False,''],
 'F': [False,''], 's': [False,  ],
 'o': [False,''], 'c': [False,''],
 'd': [False,  ], 'h': [False,  ],
 'b': [False,  ], 't': [False,  ]}

longargs_dict = {
 "periods":   "p", "cycles":    "y", "nowait":   "N",
 "execute":   "x", "finishcyc": "f",
 "finally":   "F", "stats":     "s", 
 "output":    "o", "config":    "c", 
 "display":   "d", "help":      "h", 
 "execboth":  "b", "cmdout":    "t"}

flag_list = []
for i in optcheck_dict:
    if len(optcheck_dict[i]) == 1:
        flag_list.append(i)

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
        else: raise Exception('NoFlag')

def arg_s(options):
    global reg
    for x in options:
        if str(x) in optcheck_dict:
            optcheck_dict.update({x: [True,]})
            if x == options[-1]: reg = x
        else: raise Exception(f"Unknown option -{x}") 

def arg_l(option):
    global reg
    if option in longargs_dict:
        optcheck_dict.update({longargs_dict[option]: [True,]})
        reg = longargs_dict[option]
    else: raise Exception(f"Unknown option --{option}") 

def arg_ap(argument):
    global reg
    if reg in optcheck_dict:
        optcheck_dict[reg].append(argument)

try:
    arghandle()
    period_reg = "(\d*)(\w)"
    period_tup = re.findall(period_reg, optcheck_dict["p"][1])
    span_dict = {'d': 'days', '': 'hours','m': 'minutes','s': 'seconds'}
    period_list = [list(ele) for ele in period_tup]
except:
    print("Unknown option.")
    print("Usage: simmer [-p <PERIODS>] [-y|--cycles <int>] [-x <command>]")
    print("See --help for more options.")
    exit()

a = False
try:
    for i in optcheck_dict:
        if optcheck_dict[i][0] == True:
            a = True
    if a == False: raise Exception
except: print("No options specified! See --help for usage.") ; exit()

try:
    for i in flag_list:
        if len(optcheck_dict[i]) == 1:
            pass
        else: raise Exception(f"Flag -{i} supplied with unnecessary data.")
except: print(f"Flag -{i} supplied with unnecessary data.") ; exit()
# --- argument eval ---

for x in period_list:
    try:
        if x[1] in span_dict:
            x[1] = span_dict[x[1]]
        else: raise Exception 
    except: 
        print("Unknown period length. Options are: d (days), h (hours), m (minutes), s (seconds).")
        exit()
    try: 
        if x[0] == '': raise Exception   
    except:
        print("Missing period duration.") 
        exit()

try:
    optcheck_dict['y'][1] = int(optcheck_dict['y'][1])
    if optcheck_dict['y'][1] > 0:
        pass
    else: raise Execption("Cycle number must be an integer greater than 0.")
except: print("Cycle number must be an integer.") ; exit()

# ---exec---
def exec(which):
    try:
        if optcheck_dict[which][0] == True:
            x = shlex.split(optcheck_dict[which][1])
            if optcheck_dict['t'][0] == True:
                p = subprocess.Popen(x, stderr=subprocess.PIPE)
            else: p = subprocess.Popen(x, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if optcheck_dict['N'][0] == False: p.wait()
    except FileNotFoundError:
        print(f'{which}: No command ({" ".join(x)}), found.')
        exit() 

# ---timer function---
def timer(dur, disp, stats, num, cyc=0, out=''):
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
    if stats == True:
        print(f"Done with period {num}, cycle {cyc}, {dur}.")

c_len=0
try:
    while c_len < int(optcheck_dict["y"][1]):
        p_len=0
        for i in period_list:
            timer(eval(f"datetime.timedelta({i[1]}={i[0]})"), 
            optcheck_dict["d"][0], 
            optcheck_dict["s"][0], 
            p_len, c_len)
            p_len += 1
            if optcheck_dict['b'][0] == False:
                if p_len < len(period_list) or optcheck_dict['c'][0] == False or len(period_list) == 1: exec("x")
            else: exec('x')
        c_len += 1
        exec('f')
except KeyboardInterrupt: print("\nCaught term signal, exiting.") ; exit()
except: print('Timer failed.') ; exit()
exec('F')
# ---