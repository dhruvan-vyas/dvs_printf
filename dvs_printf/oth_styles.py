from time import sleep
from os import get_terminal_size

def _help_():
    tem_len_line = get_terminal_size()[0]
    mid_len_line = int(tem_len_line/2 - 9)
    print("\n"+"="*tem_len_line+"\n"+(" "*mid_len_line)+">>> DVS_PRINTF <<<"+"\n"+"="*tem_len_line)
    print("""
keywords --> printf(values, style='typing', speed=3, interval=2, stay=True)\n\n
values --> main stream input values  
           value can be any-data-Type 
           Ex. printf(str, list, [tuple, set], dict, int,...)\n\n
style --> style is different type if printing animation 
          styles, from this list each style type works 
          differently according to description below\n
        ["typing", "async", "headline", "newsline", "mid", "gunshort", "snip",
        "left", "right", "center", "centerAC", "centerAL", "centerAR", "wave",
        "matrix", "matrix2", "scatter", "fire", "blink", "f2b", "b2f", "help"]\n
        |¯¯¯|¯¯¯¯¯¯¯¯¯¯|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
        |   |  option  |                 description                  |
        |___|__________|______________________________________________|
        | * | typing   | print like typing animation                  |
        | * | async    | print multiple lines simultaneously          |
        |   | headline | print like head lines in news                |
        |   | newsline | print running newslines animation            |
        |   | mid      | print line from mid                          |
        | * | left     | value coming from left side of the terminal  |
        | * | right    | value coming from right side of the terminal |
        | * | center   | animation appear at center of the terminal   |
        | * | centerAC | values arrang at center of the terminal      |
        | * | centerAL | arrang each-item at center-Left on terminal  |
        | * | centerAR | arrang each-item at center-Right on terminal |
        |   | gunshort | firing the letters from short gun            |
        |   | snip     | sniping the letters from end of the terminal |
        |   | matrix   | print random letters to real line            |
        |   | matrix2  | print 1st letter and 2nd random letters      |
        |   | Scatter  | Scattered latters effect for each line       |
        |   | Fire     | appear latters with gap creates flame effect | 
        |   | wave     | creates wave effect with each line.          | 
        |   | Blink    | appear Blink effect from start to end.       |
        |   | f2b      | typing and remove letter from back to front  |
        |   | b2f      | typing and remove letter from front to back  |
        ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ \n\n
speed --> speed of printf's animation 
          defult speed is 3, from (1 to 6)\n
          1 = Very Slow  
          2 = Slow  
          3 = Mediam
          4 = Fast
          5 = Fast+
          6 = Very Fast\n\n
interval --> interval is waiting time between printing 
             of each values, (interval in second) 
             defult interval is 2, you can set from 0 to grater\n\n    
stay --> after style animation whether you want the values OR Not
         defult stay is True, can be `True or False`\n
         but some styles take No action on stay
         whether it is True OR False 
         Ex. ( typing, async, headline, newsline, f2b,  b2f, matrix2 )\n\n""")
    print("="*tem_len_line+"\n")

def fuzzy_check(str1):
    for str2 in ["typing", "async", "headline", "newsline", "mid", 
"gunshort", "snip", "left", "right", "center","Fire", "wave", "Blink", 
"Scatter", "matrix", "f2b", "b2f", "help"]: 
        if 1 - (sum(1 for a,b in zip(str1,str2) if a!=b)/min(len(str1),len(str2)))>=0.6:
            return str2
    else:return False

    
def othStyles(values,style,speed,interval,stay):  
    try:
        print('\033[?25l', end="")
        if style=="newsline":
            max_line_len = 30
            for L in values:
                if len(L)>max_line_len:max_line_len=len(L)
            for value in values:
                for i in range(max_line_len+1):
                    emptyL = max_line_len-i
                    start_point = "|"
                    if i+1 > len(value):
                        start_point = " "*(i-len(value)+1) +"|"
                    print('|'+" "*(emptyL)+value[0:i+1]+start_point, end="\r")
                    sleep(speed)
                for i in range(1,len(value)+1):
                    end_point = "|"+value[i:len(value)]
                    end_line = max_line_len-len(value)+i+1
                    print(end_point+" "*end_line+"|", end="\r")
                    sleep(speed)
                    print(end="\x1b[2K")
                sleep(interval*.06)
        elif style=="mid":
            for x in values:
                x = x if len(x)%2==0 else x+" "
                lan = len(x)//2
                front,back="",""
                for i in range(lan):
                    front = x[lan-i-1]+front
                    back += x[lan+i]
                    print(" "*(lan-i-1)+front+back,end="\r")
                    sleep(speed)
                sleep(interval)
                print(end=("\n" if stay else "\x1b[2K"))
        elif style=="gunshort":
            for x in values:
                short=""
                len_x = len(x)
                for i in range(len_x):
                    try:
                        next_let = x[i+1] if " " != x[i+1] else "_"
                        index = x[i] if " " != x[i] else "_"
                    except:next_let=" "; index = x[len_x-1]
                    for j in range(len_x-i):
                        print(short+" "*(len_x-j-2-len(short))+index
                            +(" "*j)+f"  <==[{next_let}]=|",end="\r")
                        sleep(speed)
                    sleep(speed)
                    short += x[i]
                print(end="\x1b[2K")
                print(short,end="\r",flush=True)
                sleep(interval)
                print(end=("\n"if stay else "\x1b[2K"))
        elif style=="snip":
            for x in values:
                short,addone="",0
                for i in range(len(x)):
                    try:next_let = x[i+1] if " " != x[i+1] else "_";index = x[i] if " " != x[i] else "_"
                    except:next_let=" ";index = x[len(x)-1]
                    temlen = get_terminal_size()[0]
                    for j in range(0,temlen-i-len(short)+addone-10):
                        print(short+" "*(temlen-j-len(short)-11)+index+" "*(j)+f" <===[{next_let}]=|",end="\r")
                        sleep(speed)
                    sleep(speed)
                    addone+=1
                    short+=x[i]
                print(end="\x1b[2K")
                print(x,end="\r",flush=True)
                sleep(interval)
                print(end=("\n"if stay else "\x1b[2K"))
        elif style in ["matrix","matrix2","scatter"]:
            from random import choice,randint,sample
            ranchoice_="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890" 
            if style=="matrix":
                for value in values:
                    entry=""
                    len_value = len(value)
                    for i in range(len_value): 
                        entry+=value[i] 
                        for _ in range(5):
                            nxt=""
                            for _ in range(len_value-i-1):
                                nxt+=choice(ranchoice_) 
                            print(entry+nxt, end="\r")
                            sleep(speed)
                    sleep(interval)
                    print(value,end="\r")
                    print(end=("\n" if stay else "\x1b[2K"))
            elif style=="matrix2":
                for ab in values:
                    entry=""
                    for i in range(len(ab)-1):
                        entry+=ab[i]
                        for _ in range(randint(5,20)):
                            print(entry+choice(ranchoice_))
                            sleep(speed)
                    print(ab);sleep(interval)
            elif style=="scatter":
                for line in values:
                    for _ in range(13):
                        print(''.join(sample(line+ranchoice_, len(line))), end="\r")
                        sleep(speed)
                    print(line, end="\r")
                    sleep(interval)
                    print(end=("\n" if stay else "\x1b[2K"))
        elif style in ["blink","wave","fire"]:
            for line in values:
                if style=="wave":
                    for i in range(len(line)):
                        print(line[:i]+line[i].swapcase()+line[i+1:],end="\r")
                        sleep(speed)
                elif style=="blink":
                    for i in range(len(line)):
                        print(line[:i]+line[i].swapcase(),end="\r")
                        sleep(speed)
                else:
                    for i in range(len(line)):
                        print(line[:i]+" "+line[i],end="\r")
                        sleep(speed)
                print(line+" ",end="\r")
                sleep(interval)
                print(end=("\n" if stay else "\x1b[2K"))
        elif style in ["f2b","b2f"]:
            for x in values:
                for y in range(0, len(x)+1):
                    print(x[:y], end="\r")
                    sleep(speed)
                sleep(interval)
                if style=="f2b":
                    for y in range(0, len(x)+1):
                        print(" "*y, end="\r")
                        sleep(speed)
                    print(end="\x1b[2K")
                else:
                    for i in range(0, len(x)+1):
                        print(x[:len(x)-i], end="\r")
                        sleep(speed)
                        print(end="\x1b[2K")
        elif style=="help":
            _help_()
            for i in values:print(i)
        else:
            fuzy_style=fuzzy_check(style)
            for j in (f'''\n
\tprintf does not accepts style='{style}' as parameter
\t{"-"*31}{"^"*len(style)}{"-"*14}\n\t>>> please enter name of style from the list <<<\n\n
\tstyle_list: [\n\tTyping, async, headline, newsline, mid, gunshort, snip, 
\tleft, right, center, centerAC, centerAL, centerAR, wave,
\tmatrix, matrix2, scatter, blink, fire, b2f, f2b, help ]\n\n
StyleNameError: styleName '{style}' is not defined. {f"Did you mean: '{fuzy_style}'?" if fuzy_style else "!!!"}
\n'''):print(j,end="",flush=True);sleep(.003)
            sleep(1);print(i)
    except Exception as EXP:print("\n",EXP,"\n\n")
    finally:
        print(end="\033[?25h")
        del values

