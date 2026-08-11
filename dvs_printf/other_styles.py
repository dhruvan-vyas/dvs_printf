from time import sleep
from os import get_terminal_size

def help():
    tem_len_line = get_terminal_size()[0]
    mid_len_line = max(0, int(tem_len_line/2 - 12))
    from .__printf__ import printf
    print("\n"+"="*tem_len_line+"\n"+(" "*mid_len_line)+">>> DVS_PRINTF HELP SYSTEM <<<"+"\n"+"="*tem_len_line)
    printf("""
printf(values, style='typing', speed=3, delay=0, stay=True, color=None, background_color=None, attrs=[], getmat=False)

PARAMETERS:
  values           : Input data stream to animate (string, list, tuple, set, dict, matrix, custom objects).
  style            : Animation style key (typing, glitch, matrix, matrix2, headline, async, wave, fire, newsline, gunshort, snip, silverfade, scatter, blink, f2b, b2f, help).
  speed            : Animation speed multiplier (1 to 6, or 7 for instantaneous). Default: 3.
  delay            : Pause duration in seconds after rendering or between line steps. Default: 0.
  stay             : If True, output remains visible. If False, clears line after animation completes.
  color            : Foreground color/gradient (HEX, RGB tuple, named color, or Colors object).
  background_color : Background color/gradient.
  attrs            : Text formatting attributes (e.g. ['bold', 'italic', 'underline']).
  getmat           : scientific matrix formatting (True, False, or 'show').

AVAILABLE ANIMATION STYLES:
  ["typing", "async", "headline", "newsline", "mid", "gunshort", "snip",
   "left", "right", "center", "centerAC", "centerAL", "centerAR", "wave",
   "matrix", "matrix2", "scatter", "fire", "blink", "f2b", "b2f", "help"]

  |   Style    | Description                                                 |
  |------------|-------------------------------------------------------------|
  | typing     | Sequential character typewriter animation (default)         |
  | async      | High-speed multi-line parallel streaming                    |
  | headline   | Centered section heading banner style                       |
  | newsline   | Scrolling news ticker-tape animation                        |
  | mid        | Expands outwards from line center                           |
  | left/right | Text slides in from left or right terminal edge             |
  | center     | Aligned center text animation                               |
  | gunshort   | Rapid letter firing particle effect                         |
  | snip       | Horizontal scissors trimming movement                       |
  | matrix/2   | Digital rain / code stream falling animation                |
  | scatter    | Fragmented letters coalescing into target text              |
  | fire       | Flickering intense flame color glow                         |
  | wave       | Case-swapping oscillating ripple effect                     |
  | blink      | Flash visibility pulse animation                            |
  | f2b / b2f  | Front-to-back or back-to-front line trimming                |
  | help       | Launches this interactive module help guide                 |

MODULE SPECIFIC GUIDES & GITHUB DOCUMENTATION LINKS:
  • Core printf Guide    : https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/printf_README.md
  • colors Engine        : https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/colors_README.md
  • loaders (Bars/Spin)  : https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/loaders_README.md
  • Init Global Config   : https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/init_README.md
  • exceptions Visualizer: https://github.com/dhruvan-vyas/dvs_printf/blob/main/READMES/exceptions_README.md
""", style="async", speed=6)
    print("="*tem_len_line+"\n")

def fuzzy_check(str1):
    for str2 in [ "typing", "async", "headline", "newsline", 
"mid", "gunshort", "snip", "left", "right", "center","Fire", 
"wave", "Blink", "Scatter", "matrix", "f2b", "b2f", "help"]: 
        if 1 - (sum(1 for a,b in zip(str1,str2) if a!=b) 
        / min(len(str1),len(str2))) >= 0.6: return str2
    else:return False
    
def otherStyles(values, style, speed, delay, stay):
    try:
        print('\033[?25l', end="")
        if style=="newsline":
            max_line_len = max(max([len(line) for line in values]), 30)
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
                sleep(delay*.06)
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
                sleep(delay)
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
                sleep(delay)
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
                sleep(delay)
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
                    sleep(delay)
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
                    print(ab);sleep(delay)
            elif style=="scatter":
                for line in values:
                    for _ in range(13):
                        print(''.join(sample(line+ranchoice_, len(line))), end="\r")
                        sleep(speed)
                    print(line, end="\r")
                    sleep(delay)
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
                sleep(delay)
                print(end=("\n" if stay else "\x1b[2K"))
        elif style in ["f2b","b2f"]:
            for x in values:
                for y in range(0, len(x)+1):
                    print(x[:y], end="\r")
                    sleep(speed)
                sleep(delay)
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
            help()
            for i in values:print(i)
        else:
            fuzy_style=fuzzy_check(style)
            for j in (f'''\n
\tprintf does not accepts style='{style}' as parameter
\t{"-"*31}{"^"*len(style)}{"-"*14}\n\t>>> please enter name of style from the list <<<\n\n
\tstyle_list: [\n\tTyping, async, headline, newsline, mid, gunshort, snip, 
\tleft, right, center, centerAC, centerAL, centerAR, wave,
\tmatrix, matrix2, scatter, blink, fire, b2f, f2b, help ]\n\n
StyleNameError: The Style '{style}' Is Not Recognized. {f'Did you mean: "{fuzy_style}"?' if fuzy_style else "!!!"}\n\n'''):
                print(j,end="",flush=True)
                sleep(.003)
            sleep(1)
            for i in values:print(i);sleep(.03)
    
    except Exception as EXP:
        print("\n",EXP,"\n\n")
    
    finally:
        print(end="\033[?25h")
        del values

