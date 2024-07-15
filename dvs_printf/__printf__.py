from time import sleep
from os import get_terminal_size

def divide_line(string:str, tem_len:int|None=80) -> list[str]:  
    list_=[]
    if len(string) >= tem_len:
        for i in range(1,10):
            if string[:tem_len][-i]==" ":i-=1;break
        else:i=0
        list_.append(string[:tem_len-i])
        list_.extend(divide_line(string[tem_len-i:],tem_len))
    else:list_.append(string)
    return list_

def list_of_str(*values: tuple, getmat: bool | str | None = False) -> list[str]:
    """Takes any values in tuple -> list[str] \n
return list with each elements given. takes any DataType and gives `list[str]`\\
with each elements by index. for `list, tuple, dict, set` breake this kind of \\
DataSet and add Them into a list by index. 
---
## getmat: 
    matrix data modifier for `pytorch, tensorflow, numpy, pandas, list` \\
    it breaks matrices in `rows by index` and convet that in to list of string. `default getmat=False`
### getmat = `True` or `"true"` 
    to modify coyp of data for animation if `getmat=False` \\
    it's just apply animation whitout data modification, `as normal output`
#### getmat = `"show"`
    for values `with information` about matrix `<class, shape, dtype>` 
    """
    values=values[0]  
    newa_a=[]
    for value in values:
        var_type=type(value)
        if getmat:
            try:
                getmat = str(getmat).lower()
                if "numpy" in str(var_type):
                    newa_a.extend(
                [str(sublist.tolist()) for sublist in value.reshape(-1, value.shape[-1])]
                    )
                    if "show" in getmat:newa_a.extend([
    "<class 'numpy.ndarray'","dtype="+str(value.dtype)+" ","shape="+str(value.shape)+">"
                    ])
                    continue
                elif "tensorflow" in str(var_type):    
                    from tensorflow import reshape,shape;newa_a.extend(
                [str(sublist.numpy().tolist()) for sublist in reshape(value, [-1, shape(value)[-1]])]
                    )
                    if "show" in getmat:newa_a.extend([
    "<class 'Tensorflow'",(str(value.dtype).replace("<","")).replace(">","") +" ","shape: "+str(value.shape)+">"
                    ])
                    continue  
                elif "torch" in str(var_type):
                    newa_a.extend(
                [str(sublist.tolist()) for sublist in value.view(-1, value.size(-1))]
                    )
                    if "show" in getmat:newa_a.extend([
    "<class 'torch.Tensor'", " dtype="+str(value.dtype)+" "," shape="+str(value.shape)+">"
                    ])
                    continue
                elif "pandas" in str(var_type):
                    newa_a.extend(value.stack().apply(lambda x: str(x)).tolist())
                    if "show" in getmat:
                        newa_a.extend(["<class 'pandas'"," shape="+str(value.shape)+" "+">"])
                        newa_a.extend(
    (str(value.dtypes).replace("\n","@#$@")).replace("    ",": ").split("@#$@")
                    )
                    continue
                else: 
                    if isinstance(value,list) and isinstance(value[0],list):
                        newa_a.extend(list_of_str(value, getmat=getmat))
                        continue
                    elif isinstance(value,list):
                        newa_a.append(str(value).replace("\n"," "))
                        continue
            except:pass
        try:tem_len=get_terminal_size()[0]-2  
        except:tem_len=80
        if var_type==dict:
            for i in value:
                for var in f"{i}: {value[i]}".split('\n'):
                    newa_a.extend(divide_line(var, tem_len)) if len(var)>=tem_len else newa_a.append(var)
        elif(var_type==list)or(var_type==tuple)or(
var_type==set):newa_a.extend(list_of_str(value,getmat=False))
        else:
            if var_type!=str:value=str(value)
            for vel in value.split("\n"):
                if len(vel)>=tem_len:newa_a.extend(divide_line(vel, tem_len))
                else:newa_a.append(vel)

    return newa_a 


def printf(*values:object, 
    style:str|      None='typing', 
    speed:int|float|None=3, 
    delay:int|float|None=0,  
    stay:bool|      None=True,
    getmat:bool|str|None=False) -> None:
    ''' 
#### [printf](https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#printf-function): \
prints values to a stream with animation. 
---
#### style: 
    style is defins different types of print animation. `default a "typing"`. 
[typing, async, headline, newsline, mid, gunshort, snip,scatter, fire, wave, blink, \\
left, right, center, centerAC, centerAL, centerAR, matrix, matrix2, f2b,b2f, help] \\
"async <int>" To introduce a delay before printing a set of lines from given values
#### speed:
    speed is defins printf's animation speed `from 1 to 6` `default a 3`
#### delay:
    waiting time between printing animation of two lines `default a 0`.
`(delay in second >= 0)` int | float  
#### stay:
    decide after style animation whether you want the values 
on stream OR NOT `default a True`. don't work for some styles
#### getmat: 
    matrix data modifier for `pytorch, tensorflow, numpy, pandas, list` 
for animation, `default getmat=False`, set as `True, "true", "show"`
    '''
    if values==(): return None
    values=list_of_str(values, getmat=getmat) 
    style=style.lower()

    try:delay=abs(delay)
    except:delay=0

    try:
        if speed==7:speed=.003
        elif style in["typing","headline"]or("center" in style
        ):speed=(.08/speed)if(speed>=1 and speed<=6)else 0.028
        elif style in["right","left"]:speed=(.032/speed)if(speed>=1 and speed<=6)else .016
        elif "async" in style:speed=(.045/speed)if(speed>=1 and speed<=6)else .015
        elif style=="gunshort":speed=(.064/speed)if(speed>=1 and speed<=6)else .016
        elif style=="snip":speed=(.016/speed)if(speed>=1 and speed<=6)else .008
        elif style=="scatter":speed=(.3/speed)if(speed>=1 and speed<=6)else .1
        elif style=="newsline":speed=(.18/speed)if(speed>=1 and speed<=6)else .06 
        else:speed=(.16/speed)if(speed>=1 and speed<=6)else .08 
    except:speed=.05

    if ("center" in style) or ("async" in style):
        max_line_len=max(len(line) for line in values)

    try:
        print(end='\033[?25l')
        if style=="typing":
            for x in values:
                for i in x:
                    print(i+"|\b", end="",flush=True)
                    sleep(speed)
                print(" ")
                sleep(delay)
        elif style=="headline":
            for x in values:
                for i in x:
                    print(i+"|\b", end="",flush=True)
                    sleep(speed)
                sleep(delay)
                for i in range(len(x)+1):
                    print(x[:-i]+"|",end="\r")
                    sleep(speed)
                    print(end="\x1b[2K")
        elif "async" in style: 
            tem_size=get_terminal_size()[1]-1
            try:
                new_size=int(style.replace("async", ""))
                if 0 < new_size <= tem_size:
                    tem_size = new_size
            except:pass
            max_line_len+=1
            len_val=len(values)
            for v in range(0,len_val,tem_size):
                for j in range(max(len(m) for m in values[v:v+tem_size])+1):
                    for i in values[v:v+tem_size]:
                        print(i[:j])
                    print(end="\033[F"*(tem_size if len_val>v+tem_size else len_val-v))
                    sleep(speed)
                print("\n"*(tem_size-1 if len_val>v+tem_size else len_val-v-1))
                sleep(delay)
        elif style=="left":
            for i in values:
                i_len=len(i)
                for j in range(1,i_len+1):
                    print(i[-j:],end="\r")
                    sleep(speed)
                sleep(delay)
                if stay:print(end="\n")
                else:
                    for j in range(1,i_len+1):
                        print(i[j:i_len],end="\r")
                        print(end="\x1b[2K")
                        sleep(speed)
        elif style=="right":
            for i in values:
                i_len=len(i)
                for j in range(i_len+1): 
                    print(i[:j].rjust(get_terminal_size()[0]),end="\r")
                    sleep(speed)
                sleep(delay)
                if stay:print(end="\n")
                else:
                    for j in range(i_len+1):
                        print(i[:i_len-j].rjust(get_terminal_size()[0]),end="\r")
                        print(end="\x1b[2K")
                        sleep(speed)
        elif style=="center":
            for i in values:
                i_len=len(i)
                for j in range(i_len+1):
                    print(" "*int(get_terminal_size()[0]/2-len(i[:j])/2)
                    +i[:j]+("|"if j<i_len else" "),end="\r") 
                    sleep(speed)
                sleep(delay)
                print(end=("\n"if stay else"\x1b[2K"))
        elif "center" in style:
            for i in values:
                i_len=len(i)
                if style=="centerac":
                    for j in range(i_len+1):
                        print(" "*int(get_terminal_size()[0]/2-i_len/2)+i[0:j]
                        +("|"if j<i_len else" ")+" "*(i_len-j-1),end="\r")
                        sleep(speed)
                elif style=="centeral":
                    for j in range(i_len+1):
                        print(" "*int(get_terminal_size()[0]/2-(max_line_len/2))
                        +i[0:j]+("|"if j<i_len else" "),end="\r")
                        sleep(speed)
                elif style=="centerar":
                    for j in range(i_len+1):
                        print(" "*int(get_terminal_size()[0]/2+(max_line_len/2-i_len))
                        +i[:j]+("|"if j<i_len else" "),end="\r")
                        sleep(speed)
                sleep(delay)
                print(end=("\n"if stay else"\x1b[2K"))
        else: 
            from .other_styles import otherStyles
            otherStyles(values, style, speed, delay, stay)    
    
    except Exception as EXP:
        print("\n",EXP,"\n\n")
    
    finally:
        print(end="\033[?25h")
        del values
