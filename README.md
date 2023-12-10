# dvs_printf 

simple pritning animetion styles for python Project

https://github.com/dhruvan-vyas/dvs_printf/assets/98950841/efd02b0f-6c83-4d5b-b759-75ea036c5467

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

[Style Video](https://github/dhruvan-vyas/ds_printf#dvs_printf)

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



https://github.com/dhruvan-vyas/dvs_printf/assets/98950841/5055e3cf-409a-4995-b4ea-37ad3f3e28cc



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

https://github.com/dhruvan-vyas/dvs_printf/assets/98950841/4222cfac-a1fa-48d1-8d9d-6f7b26789c3b

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
