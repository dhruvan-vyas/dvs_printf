import threading
from time import sleep

def Loading(t1, Text, progressChar):
    speed=.16
    if progressChar in ["","\n","\r", "\b", "\t", "\a", "\f", "\v"]:
        progressChar =  "-"
    short = str(Text)+"["
    x = f"{progressChar*30}]"
    len_x = len(x)
    for i in range(len_x-20):
        print(short+" "*(len_x-i-1)+f"][ {' ' if len(str(int(i*3.33)))==1 else ''}{int(i*3.33)}%]",end="\r", flush=True)
        sleep(speed)
        short=short+x[i]
        if t1.is_alive()==False:speed=.016
    for i in range(len_x-20, len_x-5):
        print(short+" "*(len_x-i-1)+f"][ {int(i*3.33)}%]",end="\r", flush=True)
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
    for i in range(len_x-5, len_x):
        print(short+" "*(len_x-i-1)+f"][ {int(i*3.33)}%]",end="\r")
        sleep(speed)
        short=short+x[i]
        if t1.is_alive():speed=1
        else:speed=.02
    print(short+f"[100%]", end="\r")
    sleep(.5)
    print(end="\x1b[2K")

def showLoading(target: object, 
    args:tuple|None=(),
    kwargs:dict|None={},
    LoadingText:str|None="Loading",
    progressChar:str|None="#" ) -> int:
    """
create Loading bar in terminal with `threading` for 

* `waiting time for downlod files`.
* `run other function and wait till finish`.
* `Suitable for tasks completing within 4 to 120 seconds`.

#### [readme on github ☻](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#showLoading-function)

---
keep in mind that this function already using print function \\
so your target function do not print anything while Loading \\
otherwish Loading bar will not work proparly. 

`return 0` if work done else `return 1 as ERROR!!!` 

Loading funtion works on threading module \\
so, it's `take same input as threading`.

---
## keywords 

### target
the target `object` or `function` to work in background.

### args
the positional argument in `tuple` that `target function taks` \\
But if there is just one positional argument passing add coma \\
at the end, args=(1`,`) becouse `args should be Tuple`.

### kwargs
`dictionary` of the `keyword arguments` that `target function taks.` \\
`keywords in string` and `arguments in asked data-type.` 
```py
kwargs={
    "number": 20, 
    "name": "coder"
}
```

### LoadingText
    ```test
    text befor Loading bar, default LoadingText = "Loading"
    Loading[----------------------------- ] %99  
    ```

### progressChar
    ```test
    Charactor to see progressed Loading bar, default progressChar = "#" 
    downloading files[##########                    ] %35
    ```
    """
    try:
        print(end='\033[?25l')
        progressChar = str(progressChar)[0] if (len(str(progressChar)) != 0) and (progressChar != " "
        ) and (progressChar[0] not in ["","\n","\r", "\b", "\t", "\a", "\f", "\v"]) else "-"

        if args is not tuple: 
            args = (args,)

        t1 = threading.Thread(target=target, args=args, kwargs=kwargs)
        t2 = threading.Thread(target=Loading, args=(t1,LoadingText,progressChar))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        print(end='\033[?25h')
        return 0
    
    except Exception as EXCPT:
        print(end='\033[?25h')
        print(EXCPT)
        return 1

