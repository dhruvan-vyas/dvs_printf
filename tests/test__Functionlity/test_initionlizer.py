from dvs_printf import (printf, init, list_of_str) # ShowLoading)
import dvs_printf
# from dvs_printf.colors.colors import Colors
pf = dvs_printf.Init()
printf = pf.printf

# pf.style = "red"
# pf.colors = "red" #Colors(("lightred",))
# printf("hello world", 
#        colors = ((10,2),),
#         style="typing", 
#         speed=1, 
#         # delay="b", 
#         stay=True, 
#         getmat="show",
#     )




def test_import_all(): 
    # Import All
    assert printf
    assert init
    assert list_of_str
    # assert ShowLoading


def test_init():
    # -------------------------------------(create init)
    pf = dvs_printf.init()
    printf = pf.printf

    # -------------------------------------(assert init)
    assert pf.style == "typing" 
    assert pf.speed == 3
    assert pf.delay == 0
    assert pf.stay == True
    assert pf.getmat == False

    # -------------------------------------(Update in init)
    pf = dvs_printf.init(
        style="left", 
        speed=2, 
        delay=2, 
        stay=False, 
        getmat=True
    )

    # -------------------------------------(assert init)
    assert pf.style == "left" 
    assert pf.speed == 2
    assert pf.delay == 2
    assert pf.stay == False
    assert pf.getmat == True

    # -------------------------------------(Update with setter)
    pf.style = "gunshort"
    pf.speed = 6
    pf.delay = 3
    pf.stay = True
    pf.getmat = "true"

    # -------------------------------------(Update in pf.printf)
    printf("hello world", 
        style="mid", 
        speed=4, 
        delay=.5, 
        stay=False, 
        getmat="show"
    )

    # -------------------------------------(Check for Changes)
    assert pf.style == "gunshort"
    assert pf.speed == 6
    assert pf.delay == 3
    assert pf.stay == True
    assert pf.getmat == "true"
