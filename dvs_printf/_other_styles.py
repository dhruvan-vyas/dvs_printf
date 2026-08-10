from time import sleep
from .console import get_print_function
from ._printf_helper import modifyed


def _silver_fade(values:list[str]):
    from .colors import rgb_to_ansi_func, RESET_FOREGROUND as reset

    silver_color = rgb_to_ansi_func(220, 220, 220)
    step2_color  = rgb_to_ansi_func(170, 170, 170)
    grey_color   = rgb_to_ansi_func(120, 120, 120)
    
    try:    iternum = int(modifyed.style.replace("silverfade", ""))
    except: iternum = 2

    for line in values:
        # line = compile(r'\x1b\[([0-9;]*m)').sub('', line)
        if len(line)>1:
            for _ in range(iternum):

                print(f'{silver_color}{line[0]}{step2_color}{line[1]}{grey_color}{"".join(line[2:])}', end='\r')
                for index in range(len(line)):
                    print(f'{grey_color}{"".join(line[:index])}{step2_color}{line[index]}{silver_color}'
                          f'{"".join(line[index+1:index+2])}{step2_color}{"".join(line[index+2:index+3])}'
                          f'{grey_color}{"".join(line[index+3:])}'
                    , end='\r')
                    sleep(modifyed.speed)
                print(f'{grey_color}{line}{reset}', end='\r')

        else: 
            print(f"{grey_color}{line}", end='\r')

        sleep(modifyed.delay)    
        print(end=modifyed._stay)

def _glitch(values:list[str] | list[list[str]]):
    # "glitch – A random distortion effect, suitable for chaotic animations."
    from random import choice
    
    print  = get_print_function(color=modifyed.color, args=2)
    print1 = get_print_function(color=modifyed.color, args=1)
    def show(len_i, first_char, poschar):
        numbers = list(range(1,len_i))
        if choice((0,1))==1: 
            print(first_char, end="\r")
            sleep(modifyed.speed)
        if poschar==" ":
            while len(numbers) > 0:
                a = choice(numbers)
                numbers.remove(a)
                print(f"\033[{a}C{poschar}", end = "\r")
                sleep(modifyed.speed)
        else:
            while len(numbers) > 0:
                a = choice(numbers)
                print(f"\033[{a}C{poschar[a]}", end = "\r")
                numbers.remove(a)
                sleep(modifyed.speed)
    try:
        petarn = modifyed.style.replace("glitch","").replace(" ","")[0]
    except:
        petarn = "^"
    for i in values:
        len_i = len(i)
        print(petarn*len_i,end="\r")
        show(len_i, i[0], i)
        print1(i)
        sleep(modifyed.delay)
        if modifyed.stay:
            print(modifyed._stay)
        else:
            show(len_i," "," ")

def _mid(values:list[str] | list[list[str]]):
    print  = get_print_function(color=False     , args=1)
    print1 = get_print_function(color=modifyed.color, args=2)
    print2 = get_print_function(color=modifyed.color, args=3)
    for x in values:
        lan = len(x) //2
        for i in range(1,lan):
            print2(" "*(lan-i), x[lan-i:lan+i], end="\r")
            sleep(modifyed.speed+.05)
        print1(x, end="\r")
        sleep(modifyed.delay)
        print(modifyed._stay)

def _newsline(values:list[str] | list[list[str]]): 
    print = get_print_function(color=False, args=1)
    print1 = get_print_function(color=modifyed.color, args=3)

    if type(values) is not list:
        values = list(values) 
    modifyed.maxStrLen  = max( max(len(line) for line in values), 30)

    for value in values:
        len_value = len(value)
        for i in range(modifyed.maxStrLen+1):
            emptyL = modifyed.maxStrLen-i
            start_point = "|"
            if i+1 > len_value:
                start_point = " "*(i-len_value+1)+"|"
            print1('|'+(" "*emptyL), value[:i+1], start_point+"\r")
            sleep(modifyed.speed)
        for i in range(1,len_value+1):
            # end_point = "|"+value[i:len_value]
            end_line = modifyed.maxStrLen-len_value+i+1
            print1("|",value[i:len_value]," "*end_line+"|\r")
            sleep(modifyed.speed)
        sleep(modifyed.delay*.06)
    print("\x1b[2K")
    # modifyed.stay = 0

def _gunshort(values:list[str] | list[list[str]]):
    print   = get_print_function(color=False , args=1)
    for x in values:
        short=""
        len_x = len(x)
        for i, v in enumerate(x):
            try:
                next_let = x[i+1] if " " != x[i+1] else "_"
                index = v if " " != v else "_"
            except:
                next_let=" "
                index = x[len_x-1]

            short_len = i #len(short)
            for j in range(len_x-i):
                S  = (len_x-j-2-short_len)
                print(short+(" "*S)+index+(" "*j)+f"  <==[{next_let}]=|\r")
                sleep(modifyed.speed)
            sleep(modifyed.speed)
            short += x[i]

        print("\x1b[2K"+short+"\r")
        sleep(modifyed.delay)
        print(modifyed._stay)

def _snip(values:list[str] | list[list[str]]):
    from os import get_terminal_size
    print1   = get_print_function(color=False , args=1)

    for x in values:
        short = ''
        addone = 0
        for i in range(len(x)):
            try:
                next_let = x[i+1] if " " != x[i+1] else "_"
                index = x[i] if " " != x[i] else "_"
            except:
                next_let=" "
                index = x[len(x)-1]

            temlen = get_terminal_size()[0]
            len_short = i 
            print1(f"{short}{' '*(temlen-len_short-11)} <===[{index}]=|\r")
            sleep(.05)
            print1(f"{short}{' '*(temlen-len_short-12)}{index} <==[{next_let}]=|\r")
            sleep(.05)

            for j in range(2,temlen-i-len(short)+addone-10):
                print1(f"{short}{' '*(temlen-j-len_short-11)}{index}{' '*(j)} <===[{next_let}]=|\r")
                sleep(modifyed.speed)
            addone+=1
            short+=x[i]

        print1("\x1b[2K" + short)
        sleep(modifyed.delay)
        print1(modifyed._stay)

# def style in ["matrix","matrix2","scatter"]:
def _matter(values:list[str] | list[list[str]]):
    from random import choice,randint,sample
    ranchoice="abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-1234567890" 
    if modifyed.color: ranchoice= list(ranchoice)
    print  = get_print_function(color=modifyed.color         , args=2)
    print1a2 = get_print_function(color=True, args=2)
    print2b3 = get_print_function(color=modifyed.color, args=3)
    print2a3 = get_print_function(color=True, args=3)
    
    for value in values:
        val = ""
        len_val = len(value)-1
        if modifyed.style=="matrix":
            for i, j in enumerate(value):
                val += j
                for _ in range(5):
                    print2a3(val, sample(value+ranchoice, len_val-i), end="\r")
                    sleep(modifyed.speed)

        elif modifyed.style=="matrix2":
            for i in range(len_val):
                val+=value[i]
                for _ in range(randint(5,15)):
                    print2b3(val,f"{choice(ranchoice)}\n")
                    sleep(modifyed.speed)
        else:
            for _ in range(10):
                print1a2(sample(value+ranchoice, len_val), end="\r")
                sleep(modifyed.speed)
        print(value, "\r")
        sleep(modifyed.delay)
        print(modifyed._stay)

# def modifyed.style in ["blink","wave","fire"]:
def _blwafi(values:list[str] | list[list[str]]):
    print  = get_print_function(color=False, args=1)
    print2 = get_print_function(color=modifyed.color, args=2)

    for line in values:
        if modifyed.style=="wave":
            for i in range(len(line)):
                print2(line[:i], f"{line[i][-1].swapcase()}{''.join(line[i+1:])}\r")
                sleep(modifyed.speed)
        elif modifyed.style=="blink":
            for i in range(len(line)):
                print2(line[:i],f"{line[i].swapcase()}\r")
                sleep(modifyed.speed)
        else:
            for i in range(len(line)):
                print2(line[:i],f" {line[i]}\r")
                sleep(modifyed.speed)

        print2(line,end=" \r")
        sleep(modifyed.delay)
        print(modifyed._stay)

def _f2b2f(values:list[str] | list[list[str]]):
    print  = get_print_function(color=False, args=1)
    print1 = get_print_function(color=modifyed.color, args=1)
    print2 = get_print_function(color=modifyed.color, args=2)

    for x in values:
        len_x = len(x)
        for y in range(0, len_x+1):
            print2(x[:y], end="\r")
            sleep(modifyed.speed)
        sleep(modifyed.delay)
        if modifyed.style=="f2b":
            for y in range(0, len_x+1):
                print((" "*y)+"\r")
                sleep(modifyed.speed)
            print("\x1b[2K")
        else:
            for i in range(len_x):
                print1(f"\r\033[{len_x-i}C ")
                sleep(modifyed.speed)
            print(" \r\x1b[2K")
