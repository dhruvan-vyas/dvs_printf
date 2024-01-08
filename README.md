# dvs_printf 


<section class="hidden"><div><h3>simple pritning animetion styles for python Project</h3></div> </section> 
<section class="hidden">
<div class="main" align="center">
<div class="glow"></div>
<div class="behind" align="absmiddle">
<div class="shadowimg1"></div><div class="shadowimg2"></div><div class="shadowtext1"></div><div class="shadowtext2"></div>
<div class="github-repo" align="absmiddle"><a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf"><img class="git_img" src="https://desktop.github.com/images/desktop-icon.svg" align="absmiddle"/><mark class="git_text">dvs_printf GitHub</mark></a></div>
<div class="github-repo" align="absmiddle"><a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf"><mark class="git_text_in">dvs_printf GitHub</mark><img class="git_img_in" src="https://desktop.github.com/images/desktop-icon.svg" align="absmiddle"/></a></div>
</div>
<style>
.shadowimg1{height:120px;width:120px;background-color:rgba(8,1,11,0.5);position:absolute;z-index:-1;margin-top:4px;margin-left:6px;border-radius:100px;filter:blur(10px);} 
.shadowimg2{left:320px;top:130px;height:120px;width:120px;background-color:rgba(8,1,11,0.5);position:absolute;z-index:-1;margin-top:4px;margin-left:6px;border-radius:100px;filter:blur(10px);}
.shadowtext1{height:85px;width:240px;background-color:rgba(8,1,11,0.5);position:absolute;z-index:-1;margin-top:25px;margin-left:179px;border-radius:20px;filter:blur(10px);} 
.shadowtext2{height:85px;width:240px;background-color:rgba(8,1,11,0.5);position:absolute;z-index:-1;margin-top:153px;margin-left:8px;border-radius:20px;filter:blur(10px);}
.main{padding-top:40px;padding-bottom:40px;padding-right:39px;background-repeat:repeat;position:relative;}
mark{padding-right:40px;padding-left:40px;text-align:right;padding-top:32px;padding-bottom:30px;background-color:#CEDEF4;font-weight:600;font-size: 20px;color:#224499;border-radius:20px;}
.glow {border-color: white;background-image:radial-gradient(#ffffff 1%, transparent 20%),radial-gradient(#ffffff 1%, transparent 20%);background-size:6px 6px;background-position: 0 0, 3px 3px;background-color:rgba(77,10,106,.6);border-radius:8px;height:256px;width:480px;display:inline-block;position:absolute;display:relative;z-index:-5;}
.behind{display:inline-block;padding-left:35px;position:relative;display:relative;} 
.git_img{margin-right:20px;}        
.git_text{margin-left:20px;} 
.git_img_in{margin-left:20px;} 
.git_text_in{margin-right:20px;} 
</style>
</div> 
</section> 
<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@200;400;700&display=swap");
section{display: grid;place-items: center;align-content: center;min-height: 40vh;}
.hidden{opacity: 0;transition: all 2s;}
.show{opacity: 1;}

</style> 
<script>
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry)=>{console.log(entry)
        if (entry.isIntersecting){entry.target.classList.add('show')
        } else {entry.target.classList.remove('show')}
    });
});
const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));
</script>


***


## Installation with python (pip)

just copy and past oneliner command on Terminal


### Linux / macOS 
```bash
pip3 install dvs_printf
```
```bash
python3 -m pip install dvs_printf
```

### On Windows
```bash
pip install dvs_printf
```
```bash
python -m pip install dvs_printf
```

# Documentation

## dvs_printf function
This function makes your python project looks good,
by using printf's styl animetion function you can print you stream in uniq styles 


## printf function keywords

``` python
from dvs_printf import printf

printf(*values, styl='typing', speed=3, intervel=2, stay=True)
```




### values
values stream can be anythin like
`(string, int, float, list, set, tuple, dict)`
and you can give multiple input as any-data-type

```  python              
printf(str, list, [tuple, set], dict, int,...) 
```     

### styl

[Style Video](#dvs_printf)

styl is different types of print animetion
each style type works differently according to description below

``` python
 ["typing", "headline", "mid", "f2b", "b2f", "gunshort", 
  "sniper", "metrix", "metrix2", "firing", "help"]
``` 

|  option  |                 description                |
| -------- | -------------------------------------------|
| typing   | print like typing                          |
| headline | print head lines in news                   |
| mid      | print line from mid                        |
| f2b      | remove word from (back to front)           |
| b2f      | remove word from (front to back)           |
| gunshort | firing the words from short gun            |
| sniper   | sniping the words from end of the terminal |
| metrix   | print random words to real line            |
| metrix2  | print 1st word and 2nd random word         |
| firing   | just look like firing the gun              |


### speed

 Speed is printf's animetion speed, `defult speed is 3` <br> 
 you can set `speed from ( 1 to 6 )`

*1 = Very Slow* 

*2 = Slow*

*3 = Mediam*

*4 = Mediam Fast*

*5 = Fast*

*6 = Very Fast*


``` python
printf("hello world", speed=2)
```


### intervel


intervel is waiting time between printing 
of two lines (intervel in second)
`defult intervel is 2`, 

you can set intervel from `0 to 10 or greater` 
``` python
printf("hello world", "hii I am coder", intervel=4)
   
>>> hello world
(Then wating time of intervel time in second)
>>> hii I am coder
```






### stay
stay decides after styl animetion whether you want the `stream OR Not`. <br>
stay can be True or False, `(defult stay = True)`. <br>
if you want to remove printed line. you can set `stay=False`. <br>
So, After styl amimetion and intervel time printed Line can be removes.<br><br>
but some styles `takes No action on stay`,
whether it is `True OR False`. it works as it should be.

`Ex. (typing, f2b, b2f, metrix, metrix2)`


```python
printf("hello world", styl="headline", stay=True)
```









# listfunction

***
``` python
listfunction(*values: any, getMet: bool | None=False) -> list
```

An additionl function which is used by printf function 

listfunction( ) takes `Any DataType` in input and return a new list.
created by input values & it break deta sets by index and add them into 
new list then return that list.



### getMet
`detult getMet = False` <br>
if metrix is given, set `getMet=True`, 
it breaks metix in `rows by index` and convet that in to string. 
