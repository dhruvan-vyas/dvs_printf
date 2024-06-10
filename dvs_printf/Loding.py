"use `showLoding` function to create loding bar with any back ground function"
import threading
from time import sleep

def loding(t1, Text, lodingchar):
    speed=.16
    if lodingchar in ["","\n","\r", "\b", "\t", "\a", "\f", "\v"]:
        lodingchar =  "-"
    short = str(Text)+"["
    x = f"{lodingchar*30}]"
    for i in range(len(x)-20):
        print(short+" "*(len(x)-i-1)+f"][ {' ' if len(str(int(i*3.33)))==1 else ''}{int(i*3.33)}%]",end="\r", flush=True)
        sleep(speed)
        short=short+x[i]
        if t1.is_alive()==False:speed=.016
    for i in range(len(x)-20, len(x)-5):
        print(short+" "*(len(x)-i-1)+f"][ {int(i*3.33)}%]",end="\r", flush=True)
        sleep(speed)
        short=short+x[i]   
        if t1.is_alive():speed=1
        else:speed=.02
    if t1.is_alive():
        for i in range(60): 
            if t1.is_alive():sleep(1)
            else:break
        if i==59:
            raiseerror=f"it takes more then 2 minits for '{Text}'"
            raise TimeoutError(raiseerror)
    for i in range(len(x)-5, len(x)):
        print(short+" "*(len(x)-i-1)+f"][ {int(i*3.33)}%]",end="\r")
        sleep(speed)
        short=short+x[i]
        if t1.is_alive():speed=1
        else:speed=.02
    print(short+f"[100%]", end="\r")
    sleep(.5)
    print(end="\x1b[2K")
    
def showLoding(target: object, 
    args:tuple|None=(),
    kwargs:dict|None={},
    lodingText:str|None="Loding",
    lodingChar:str|None="#") -> int:
    """
create loding bar in terminal with `threading` for 

* `waiting time for downlod files` 
* `run other function and wait till finish`

#### [readme on github ☻](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#showloding-function)

---
keep in mind that this function already using print function \\
so your target function do not print anything while loding \\
otherwish loding bar will not work proparly. 

`return 0` if work done else `return 1 as ERROR!!!` 

loding funtion works on threading module \\
so, it's `take same input as threading`.

#### target
    the target `object` or `function` to work in background.

#### args
    the positional argument in `tuple` that `target function taks` \\
    But if there is just one positional argument passing add coma \\
    at the end, args=(1`,`) becouse `args should be Tuple`.
    
#### kwargs
    the key words that `target function taks` 

#### lodingText
    text befor loding bar 

#### lodingChar
    Charactor to see progressed loding bar
    """
    try:
        print('\033[?25l', end="")
        lodingChar = str(lodingChar)[0] if (len(str(lodingChar)) != 0) and (lodingChar != " ") and (
        lodingChar[0] not in ["","\n","\r", "\b", "\t", "\a", "\f", "\v"]) else "-"
        if type(args)!=tuple:args = (args,)
        t1 = threading.Thread(target=target,args=args,kwargs=kwargs)
        t2 = threading.Thread(target=loding,args=(t1,lodingText,lodingChar))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print('\033[?25h', end="")
        return 0
    except Exception as EXCPT:
        print('\033[?25h', end="")
        print(EXCPT)
        return 1
