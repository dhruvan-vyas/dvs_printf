from re   import sub
from time import sleep
from os   import get_terminal_size

from .console        import get_print_function
from ._printf_helper import modifyed, Modifier


def _typing(values:list, ): # self):
    print2 = get_print_function(color=modifyed.color, args=2)
    for x in values:
        for i in x:
            print2(i, end="|\b")
            sleep(modifyed.speed)
        print2(" \n")
        sleep(modifyed.delay)
    
def _headline(values:list, ): # self):
    print  = get_print_function(color=modifyed.color,args=1)
    print2 = get_print_function(color=modifyed.color,args=2)
    for x in values:
        for i in x:
            print2(i,end="|\b")
            sleep(modifyed.speed)
        sleep(modifyed.delay)
        if modifyed.stay:print(" \n")
        else:
            for i in range(len(x)+1):
                print2(x[:-i],end="|\r")
                sleep(modifyed.speed)
                print("\x1b[2K")

def _async(values:list, ): # self):
    print  =get_print_function(color=modifyed.color,args=1)
    print2 =get_print_function(color=modifyed.color,args=2)
    print3 =get_print_function(color=False     ,args=1)

    tem_size=get_terminal_size()[1]-1
    try:
        # new_size=int(modifyed.style.replace("async", ""))
        new_size =  int(sub(r'\D', '', modifyed.style))
        if 0 < new_size <= tem_size:
            tem_size = new_size
    except:pass

    if type(values) is not list:
        values = list(values) 

    len_val=len(values) 
    for v in range(0,len_val,tem_size):
        lines = (tem_size if len_val>v+tem_size else len_val-v)
        for j in range(max(len(m) for m in values[v:v+tem_size])+1):
            for i in values[v:v+tem_size]:
                print2(i[:j], end="\n")
            print("\033[F"*lines)
            sleep(modifyed.speed)
        sleep(modifyed.delay)
        if modifyed.stay:
                print3("\n"*lines)
        else:   print3('\x1b[2K\n'*lines+f"\033[{lines}A")

def _left(values:list, ): # self):
    print  =get_print_function(color=False,args=1)
    print2 =get_print_function(color=modifyed.color,args=2)
    for i in values:
        i_len=len(i)
        for j in range(1,i_len+1):
            print2(i[-j:],end="\r")
            sleep(modifyed.speed)
        sleep(modifyed.delay)
        if modifyed.stay:print(modifyed._stay)
        else:
            for j in range(1,i_len+1):
                print2(i[j:i_len],end="\r")
                sleep(modifyed.speed)
                print(modifyed._stay)

def _right(values:list, ): # self):
    print    = get_print_function(color=modifyed.color,args=3)
    print1   = get_print_function(color=False,args=1)
    tem_size = get_terminal_size()[0]-1
    tem_size_i_len = 0
    for i in values:
        i_len=len(i)+1
        for j in range(i_len): 
            # print(''.join(i[:j]).rjust(tem_size),end="\r")
            print((" "*(tem_size-j)),i[:j], end="\r")
            sleep(modifyed.speed)
        sleep(modifyed.delay)
        if modifyed.stay:print1(modifyed._stay)
        else:
            tem_size_i_len = tem_size - i_len
            for j in range(1, i_len-1):
                print(" "*(tem_size_i_len+j),i[:i_len-j],end="\r")
                sleep(modifyed.speed)
                print1(modifyed._stay)
            # print1("\x1b[2K")

def _center(values: list, ): # self):
    terminal_size = get_terminal_size()[0]
    print  =get_print_function(color=modifyed.color,args=3)
    print2 =get_print_function(color=False,args=2)
    print1 =get_print_function(color=False,args=1)
    TemSize = terminal_size / 2

    # values = list(values)
    # values = values[:]
    # print(f"\n\n{Modifier().maxStrLen}\n\n")
    values = list(values)
    # values.send("-----")
    # print(f"\n\n{Modifier().maxStrLen}\n\n")
    # if type(Modifier().maxStrLen) == int:
        # pass 
    # elif type(values) is not list:
    modifyed.maxStrLen = max(len(line) for line in values)

    if modifyed.style == "center":
        for i in values:
            # i = list(i)
            i_len=len(i)
            for j in range(i_len+1): 
                print(" "*int(TemSize-j/2),i[:j],end=("|\r"if j<i_len else" \r")) 
                sleep(modifyed.speed)
            sleep(modifyed.delay)
            print1(modifyed._stay)
        modifyed.stay = int(TemSize + i_len/2)
        return
    
    number = sub(r'\D', '', modifyed.style)
    min_pr = modifyed.maxStrLen / 2
    if number:
        TemSize = terminal_size * max(1, min(100, int(number))) / 100
        max_pr  = terminal_size-modifyed.maxStrLen-2

        if   min_pr < TemSize < max_pr: TemSize-= min_pr
        elif min_pr > TemSize         : TemSize = 0
        elif          TemSize > max_pr: TemSize = max_pr
    else:                               TemSize-= min_pr
    
    if (not "al" in modifyed.style) & (not "ar" in modifyed.style):  # center <int>
        for i in values:
            i_len = len(i)
            print1(" "*int(TemSize + (modifyed.maxStrLen - i_len)/2))
            for j in i:
                print2(j, end="|\b")
                sleep(modifyed.speed)
            print1(" ")
            sleep(modifyed.delay)
            # print(end="\n" if modifyed.stay else "\x1b[2K")
            print(modifyed._stay)

    else:
        if "al" in modifyed.style: # Areng-Left <int>
            modifyed.style = 1
        else:modifyed.style = 0  # Areng-Right <int
        for i in values:
            if modifyed.style == 1:
                print1(" "*int(TemSize))
            else:print1(" "*int(TemSize+modifyed.maxStrLen-len(i)))
            for j in i:
                print2(j, end="|\b")
                sleep(modifyed.speed)
            print(" ")
            sleep(modifyed.delay)
            print(modifyed._stay)
