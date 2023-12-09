"""A Test dvs_printf Package."""

from time import sleep
renint = ["a","b","c","d","e","f","g","h","i","c","d","-","l","a","w","t","r","s","v","x","a","z","n","o","p","q","r","s","t"]


def listfunction(*values: any, getMet: bool | None=False) -> list:
    """
return list with each element given.
takes any DataType and gives `str(list)`

`set, dict, list, tuple` breake this kind 
of DataSet and add Them into a list by index.

getMet: `detult getMet = False` \n
  if metrix is given, set `getMet=True`
  it breaks metix in `rows by index` \n 
  and convet that in to string and add that in to list
    """
    if len(values)==1:values=values[0]
    newa_a=[]
    for x in values: 
        try:
            res=list(filter(lambda x:isinstance(x,list),x))
            if(len(res)==len(x)):getMet=True
        except:pass
        if getMet:
            for i in x:newa_a.append(str(i).replace("\n",""))
        elif type(x) == dict:
            for i in x:newa_a.append(f"{i}: {x[i]}".replace("\n",""))
        elif (type(x) == list)or(type(x)==tuple)or(type(x) == set):
            newa_a.extend(listfunction(x))
        else:newa_a.append(str(x))
    return newa_a

def printf(*values, styl: str | None='typing', speed: int | None = 3, intervel: int | None = 2,  stay=True):
    ''' 
prints values to a stream.

styl
   different type if printing styles, `default a "typing"`.
speed
   speed of print letter by letter, from 1 to 6 `default a 3`
intervel
   waiting time between two lines, `default a 2`.
stay
   after animetion whether you want the stream OR NOT, 
   `default a True`.

`styl="help" for more info`.'''
    if intervel < 0 : intervel==3
    if styl=="gunshort":speed = (.064/speed) if (speed >= 1 and speed <= 6) else .016
    elif styl=="snip":speed = (.016/speed) if (speed >= 1 and speed <= 6) else .008
    elif styl=="mid":speed = (.16/speed) if (speed >= 1 and speed <= 4) else .08
    else:speed = (.16/speed) if (speed >= 1 and speed <=6) else .08

    if styl == "typing":
        for x in values:
            emty = ""
            x = str(x)
            for y in range(0, len(x)):
                emty = emty + x[y] if x!=set or tuple else x
                print(emty+"⎮", end="\r", flush = True)
                sleep(speed)
                print(end="\r")
                print(emty[:len(emty)], end="\r", flush = True)
            print(end="\x1b[2K")
            print(emty,end="\n")
            sleep(intervel)

    elif styl == "headline":
        for x in values:
            emty = ""
            x = str(x)
            for y in range(0, len(x)):
                emty = emty + x[y].replace("\n","")
                print(emty+"⎮", end="\r", flush = True)
                sleep(speed)
                print(emty[:len(emty)], end="\r", flush = True)
                print(end="\x1b[2K")
            sleep(intervel)
            for i in range(0, len(x)):
                delete_last = x[:len(x)-i-1].replace("\n","")
                print(delete_last+"|", end="\r", flush = True)
                sleep(speed)
                print(end="\x1b[2K")
    
    elif styl == "mid":
        for x in values:
            x = str(x) if len(x)%2==0 else str(x)+" "
            lan = len(x)//2
            front,back="",""
            for i in range(lan):
                front = x[lan-i-1]+front
                back = back +x[lan+i]
                print(" "*(lan-i-1)+front+back,end="\r",flush=True)
                sleep(speed)
            print(end="\x1b[2K")
            if stay==True:print(x)
            sleep(intervel)

    elif styl=="gunshort":
        for x in values:
            short=""
            len_x = len(x)
            for i in range(len_x):
                try:
                    next_let = x[i+1] if " " != x[i+1] else "_"
                    index = x[i] if " " != x[i] else "_"
                except:next_let=" "; index = x[len_x-1]
                for j in range(len_x-i):
                    print(short+" "*(len_x-j-1-len(short))+index+(" "*j)+f"  <==[{next_let}]=|",end="\r")
                    sleep(speed)
                sleep(speed)
                short = short + x[i]
            print(end="\x1b[2K", flush=True)
            if stay:
                print(short)
                sleep(intervel)
            else:
                print(short,end="\r")
                sleep(intervel)
                print(end="\x1b[2K", flush=True)

    elif styl == "snip":
        import os
        for x in values:
            short=""
            one = 0
            for i in range(len(x)):
                try:
                    next_let = x[i+1] if " " != x[i+1] else "_"
                    index = x[i] if " " != x[i] else "_"
                except: 
                    next_let=" "; index = x[len(x)-1]
                temlen = os.get_terminal_size()[0]
                for j in range(0,temlen-i-len(short)+one-10):
                    print(short+" "*(temlen-j-len(short)-11)+index+" "*(j)+f" <===[{next_let}]=|",end="\r")
                    sleep(speed)
                sleep(speed)
                print(end="\x1b[2K")
                one+=1
                short=short+x[i]
            if stay==True:
                print(x)
            else:
                print(x,end="\r")
                print(end="\x1b[2K")
            sleep(intervel)

    elif styl == "f2b":
        for x in values:
            x = str(x)
            for y in range(0, len(x)):
                print(x[y].replace("\n",""), end="", flush = True)
                sleep(speed)
            sleep(intervel)
            for y in range(0, len(x)+1):
                print(" "*y, end="\r", flush = True)
                sleep(speed)
            print(end="\x1b[2K")
            print(end="\r")

    elif styl=="b2f":
        bigestlen = 0
        for x in values:
            if bigestlen < len(x):
                bigestlen = len(x)
            else: x = x + " "*(bigestlen-len(x))
            for y in range(0, len(x)):
                print(x[y], end="", flush = True)
                sleep(speed)
            sleep(intervel)
            print(end="\r")
            for i in range(0, len(x)):
                delete_last = x[:len(x)-i-1]
                print(delete_last, end="  \r", flush = True)
                sleep(speed)
                print(end="\x1b[2K")
            print(end="\r")

    elif styl=="metrix":
        from random import randint
        for ab in values:
            entry = ""
            ab = ""+ab
            astimet = ""
            ab = str(ab)
            for i in range(len(ab)-1): 
                entry = (entry + ab[i]).replace("\n","")
                for rex in range(0,7):
                    addentru = "" 
                    for j in range(len(ab)-i-2):
                        _ = randint(5,20)
                        addentru = addentru+renint[_]
                    ren = randint(0,len(renint))-1
                    print(entry+renint[ren]+addentru, end="\r", flush = True)
                    astimet = astimet + entry+renint[ren]+addentru
                    sleep(speed)
                print(end="\x1b[2K")
            if stay:
                print(end="\x1b[2K")
                print(ab, flush = True)
            else:
                print(ab,end="\r", flush = True)
                print(end="\x1b[2K")
            sleep(intervel)

    elif styl == "metrix2":
        from random import randint
        for ab in values:
            entry = ""
            ab = ""+ab
            ab = str(ab)
            for i in range(len(ab)-1):
                entry = entry+ ab[i]
                for _ in range(randint(5,20)):
                    ren = randint(0,len(renint))-1
                    print(entry+renint[ren], end="\n", flush = True)
                    sleep(speed)
            print(end="\x1b[2K")
            print(ab)
    
    elif styl == "firing":
        if values==[]:values=["__-¯¯----¯¯___¯¯----¯--¯-----¯- -¯---",]
        import os
        for z in values:
            len_x = len(z)
            for i in range(len_x):
                try:next_let=z[i];index=z[i] 
                except: next_let=" ";index=z[i]
                for j in range(len_x):
                    os.system("clear")
                    print("\n\n|\n|")
                    print("|"+" "*(len_x-j-2)+index+(" "*j)+f" <==[{next_let}]=|",end="\r")#*(len(x)-j)
                    print("\n|\n|") 
                    sleep(0.001)
                sleep(.008)
                os.system("clear")
        
    elif styl == "help":
        print("""\n
        >>>>>>>>  DVS_PRINTF Function  <<<<<<<<\n

keywords --> printf(values, styl='typing', speed=3, intervel=2, stay=True)
                
                
values --> main stream input value      
        Ex. printf(str, list, [tuple, set], dict, int,...)
                

styl -->  style is different type if printing animetion 
        styles, from this list each style type works 
        differently according to description below

        [typing, headline, mid, f2b, b2f, gunshort, 
        snip, metrix, metrix2, firing, help ]

        typing   =>  print like typing
        headline =>  print head lines in news
        mid      =>  print line from mid
        f2b      =>  remove word from (back to front)
        b2f      =>  remove word from (front to back)
        gunshort =>  firing the words from short gun
        snip     =>  sniping the words from end of the terminal
        metrix   =>  print random words to real line 
        metrix2  =>  print 1st word and 2nd random word
        firing   =>  just look like firing (Just For Fun)
                
speed -->  speed of printf's animetion 
           defult speed is 3, from (1 to 6)
                
           1 = Very Slow  
           2 = Slow  
           3 = Mediam
           4 = Fast
           5 = Fast+
           6 = Very Fast

                    
intervel --> intervel is waiting time between printing 
             of each value, (intervel in second) 
             defult intervel is 2, you can set from 0 to grater
            
                
stay --> after styl animetion whether you want the stream OR Not
         `defult stay is True`, can be `True or False` 
                
         but some styles take `No action on stay`
         whether it is True OR False 
         Ex. ( typing, headline, f2b,  b2f, metrix2, firing )\n\n""")
        for i in values:
            print(i)

    else:
        print("\n\n  >>>>>>>>>>  please enter name in ,styl=  from the list    <<<<<<<<<<<<<   ")
        print("[typing, headline, mid, f2b, b2f, gunshort, snip, metrix, metrix2, firing, help]\n\n")
        for i in values:
            print(i)

    del values
