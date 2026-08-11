from dvs_printf.colors import Colors
final_total = []

def show_gradient_function(color_obj: Colors, text: str):
    print(f"\n--- Gradient Test: {color_obj!r} ---")

    # Split the text by lines to pass to apply_to_str correctly
    colored_output = color_obj.apply_to_str(text)
    print(colored_output)
    final_total.append(colored_output)
    # print("--- End Gradient Test ---")

 
if __name__ == "__main__":
    print("Testing single foreground color:")
    red_text = Colors("red")
    print([red_text.apply_to_str("Hello Red World!")])

    print("\nTesting single foreground and background color:")
    blue_on_yellow = Colors("blue", background="yellow")
    print([blue_on_yellow.apply_to_str("Blue text on Yellow background.")])

    print("\nTesting foreground gradient (Red to Blue):")
    fg_gradient_obj = Colors("red", "blue", angle=0) # Left-to-right gradient
    show_gradient_function(fg_gradient_obj, "This text should\nshow a gradient\nfrom red to blue.")

    print("\nTesting background gradient (Green to Magenta):")
    bg_gradient_obj = Colors("white", background=["green", "magenta"], angle=90) # Top-to-bottom background gradient
    show_gradient_function(bg_gradient_obj, "This text has a\nwhite foreground\nwith a background gradient.")

    print("\nTesting both foreground and background gradient:")
    both_gradient_obj = Colors(["red", "yellow"], background=["blue", "green"], angle=45)
    show_gradient_function(both_gradient_obj, "Mixed gradients:\nForeground Red->Yellow\nBackground Blue->Green")

    print("\nTesting named colors and hex colors:")
    custom_colors = Colors("#823", "rgb: 255,165,0", background="skyblue") # Hex, RGB string, Named
    print([custom_colors.apply_to_str("Custom colors and backgrounds", reset=True)])

    print("\nTesting HSL and HSV string parsing:")
    hsl_color = Colors("hsl: 240,1,0.5") # Blue
    hsv_color = Colors("hsv: 0,1,1", background="purple") # Red
    print([hsl_color.apply_to_str("This is HSL blue.")])
    print([hsv_color.apply_to_str("This is HSV red with purple background.")])

    print("\nTesting CMYK string parsing:")
    cmyk_color = Colors("cmyk:0,1,1,0") # Red
    print([cmyk_color.apply_to_str("This is CMYK red.")])

    print("\nTesting single gradient color argument:")
    single_list_arg_fg = Colors(["cyan", "yellow"], angle=0)
    show_gradient_function(single_list_arg_fg, "Single list arg\nfor FG gradient.")

    single_list_arg_bg = Colors("black", background=["orange", "purple"], angle=90)
    show_gradient_function(single_list_arg_bg, "Single list arg\nfor BG gradient.")



# co = Colors("red", "green", "orange", "pink") 
# for i in co.apply(["hello world","this is multi colored text test"]):
#     print(i)


# def test_single_foreground_color():
#     red_text = Colors("red")
#     assert red_text.apply_to_str("Hello Red World!") 


# def test_single_foreground_background_color():
#     blue_on_yellow = Colors("blue", background="yellow")
#     assert blue_on_yellow.apply_to_str("Blue text on Yellow background.")

# def test_foreground_gradient():
#     fg_gradient_obj = Colors("red", "blue", angle=0) # Left-to-right gradient
#     show_gradient_function(fg_gradient_obj, "This text should\nshow a gradient\nfrom red to blue.")

# def test_background_gradient():
#     bg_gradient_obj = Colors("white", background=["green", "magenta"], angle=90) # Top-to-bottom background gradient
#     show_gradient_function(bg_gradient_obj, "This text has a\nwhite foreground\nwith a background gradient.")

# def test_both_foreground_and_background_gradient():
#     both_gradient_obj = Colors(["red", "yellow"], background=["blue", "green"], angle=45)
#     show_gradient_function(both_gradient_obj, "Mixed gradients:\nForeground Red->Yellow\nBackground Blue->Green")

# def test_named_colors_and_hex_colors():
#     custom_colors = Colors("#823", "rgb: 255,165,0", background="skyblue") # Hex, RGB string, Named
#     assert custom_colors.apply_to_str("Custom colors and backgrounds", reset=True)

# def test_HSL_and_HSV_string_parsing():
#     hsl_color = Colors("hsl: 240,1,0.5") # Blue
#     hsv_color = Colors("hsv: 0,1,1", background="purple") # Red
#     assert hsl_color.apply_to_str("This is HSL blue.")
#     assert hsv_color.apply_to_str("This is HSV red with purple background.")

# def test_CMYK_string_parsing():
#     cmyk_color = Colors("cmyk:0,1,1,0") # Red
#     assert cmyk_color.apply_to_str("This is CMYK red.")

# def test_single_gradient_color_argument():
#     single_list_arg_fg = Colors(["cyan", "yellow"], angle=0)
#     show_gradient_function(single_list_arg_fg, "Single list arg\nfor FG gradient.")

#     single_list_arg_bg = Colors("black", background=["orange", "purple"], angle=90)
#     show_gradient_function(single_list_arg_bg, "Single list arg\nfor BG gradient.")


# # Testing single foreground color:
# # ['\x1b[38;2;255;0;0mHello Red World!\x1b[39m']

# # Testing single foreground and background color:
# # ['\x1b[38;2;0;0;255m\x1b[48;2;255;255;0mBlue text on Yellow background.\x1b[39m\x1b[49m']

# # Testing foreground gradient (Red to Blue):

# # --- Gradient Test: Colors(foreground=[(255, 0, 0), (0, 0, 255)], background=None, angle=0) ---
# # ['\x1b[38;2;235;0;20mT\x1b[39m\x1b[38;2;225;0;30mh\x1b[39m\x1b[38;2;215;0;40mi\x1b[39m\x1b[38;2;205;0;50ms\x1b[39m\x1b[38;2;195;0;60m \x1b[39m\x1b[38;2;180;0;75mt\x1b[39m\x1b[38;2;170;0;85me\x1b[39m\x1b[38;2;160;0;95mx\x1b[39m\x1b[38;2;150;0;105mt\x1b[39m\x1b[38;2;140;0;115m \x1b[39m\x1b[38;2;130;0;125ms\x1b[39m\x1b[38;2;120;0;135mh\x1b[39m\x1b[38;2;110;0;145mo\x1b[39m\x1b[38;2;100;0;155mu\x1b[39m\x1b[38;2;90;0;165ml\x1b[39m\x1b[38;2;80;0;175md\x1b[39m\n\x1b[38;2;225;0;30ms\x1b[39m\x1b[38;2;215;0;40mh\x1b[39m\x1b[38;2;205;0;50mo\x1b[39m\x1b[38;2;195;0;60mw\x1b[39m\x1b[38;2;180;0;75m \x1b[39m\x1b[38;2;170;0;85ma\x1b[39m\x1b[38;2;160;0;95m \x1b[39m\x1b[38;2;150;0;105mg\x1b[39m\x1b[38;2;140;0;115mr\x1b[39m\x1b[38;2;130;0;125ma\x1b[39m\x1b[38;2;120;0;135md\x1b[39m\x1b[38;2;110;0;145mi\x1b[39m\x1b[38;2;100;0;155me\x1b[39m\x1b[38;2;90;0;165mn\x1b[39m\x1b[38;2;80;0;175mt\x1b[39m\n\x1b[38;2;215;0;40mf\x1b[39m\x1b[38;2;205;0;50mr\x1b[39m\x1b[38;2;195;0;60mo\x1b[39m\x1b[38;2;180;0;75mm\x1b[39m\x1b[38;2;170;0;85m \x1b[39m\x1b[38;2;160;0;95mr\x1b[39m\x1b[38;2;150;0;105me\x1b[39m\x1b[38;2;140;0;115md\x1b[39m\x1b[38;2;130;0;125m \x1b[39m\x1b[38;2;120;0;135mt\x1b[39m\x1b[38;2;110;0;145mo\x1b[39m\x1b[38;2;100;0;155m \x1b[39m\x1b[38;2;90;0;165mb\x1b[39m\x1b[38;2;80;0;175ml\x1b[39m\x1b[38;2;65;0;190mu\x1b[39m\x1b[38;2;55;0;200me\x1b[39m\x1b[38;2;45;0;210m.\x1b[39m\n']

# # Testing background gradient (Green to Magenta):

# # --- Gradient Test: Colors(foreground=(255, 255, 255), background=[(0, 128, 0), (255, 0, 255)], angle=90) ---
# # ['\x1b[38;2;255;255;255m\x1b[48;2;0;128;0mT\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;9;123;9mh\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;18;118;18mi\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;28;113;28ms\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;37;109;37m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;47;104;47mt\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;56;99;56me\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;66;94;66mx\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;75;90;75mt\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;85;85;85m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;94;80;94mh\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;103;75;103ma\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;113;71;113ms\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;122;66;122m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;129;63;129ma\x1b[39m\x1b[49m\n\x1b[38;2;255;255;255m\x1b[48;2;0;128;0mw\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;9;123;9mh\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;18;118;18mi\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;28;113;28mt\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;37;109;37me\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;47;104;47m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;56;99;56mf\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;66;94;66mo\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;75;90;75mr\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;85;85;85me\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;94;80;94mg\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;103;75;103mr\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;113;71;113mo\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;122;66;122mu\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;129;63;129mn\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;138;58;138md\x1b[39m\x1b[49m\n\x1b[38;2;255;255;255m\x1b[48;2;0;128;0mw\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;9;123;9mi\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;18;118;18mt\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;28;113;28mh\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;37;109;37m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;47;104;47ma\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;56;99;56m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;66;94;66mb\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;75;90;75ma\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;85;85;85mc\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;94;80;94mk\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;103;75;103mg\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;113;71;113mr\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;122;66;122mo\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;129;63;129mu\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;138;58;138mn\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;147;53;147md\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;157;48;157m \x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;166;44;166mg\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;176;39;176mr\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;185;34;185ma\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;195;30;195md\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;204;25;204mi\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;214;20;214me\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;223;15;223mn\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;232;11;232mt\x1b[39m\x1b[49m\x1b[38;2;255;255;255m\x1b[48;2;242;6;242m.\x1b[39m\x1b[49m\n']

# # Testing both foreground and background gradient:

# # --- Gradient Test: Colors(foreground=[(255, 0, 0), (255, 255, 0)], background=[(0, 0, 255), (0, 128, 0)], angle=45) ---
# # ['\x1b[38;2;255;23;0m\x1b[48;2;0;11;231mM\x1b[39m\x1b[49m\x1b[38;2;255;30;0m\x1b[48;2;0;15;224mi\x1b[39m\x1b[49m\x1b[38;2;255;38;0m\x1b[48;2;0;19;216mx\x1b[39m\x1b[49m\x1b[38;2;255;50;0m\x1b[48;2;0;25;204me\x1b[39m\x1b[49m\x1b[38;2;255;57;0m\x1b[48;2;0;29;197md\x1b[39m\x1b[49m\x1b[38;2;255;65;0m\x1b[48;2;0;32;189m \x1b[39m\x1b[49m\x1b[38;2;255;73;0m\x1b[48;2;0;36;181mg\x1b[39m\x1b[49m\x1b[38;2;255;81;0m\x1b[48;2;0;40;173mr\x1b[39m\x1b[49m\x1b[38;2;255;88;0m\x1b[48;2;0;44;166ma\x1b[39m\x1b[49m\x1b[38;2;255;96;0m\x1b[48;2;0;48;158md\x1b[39m\x1b[49m\x1b[38;2;255;104;0m\x1b[48;2;0;52;150mi\x1b[39m\x1b[49m\x1b[38;2;255;112;0m\x1b[48;2;0;56;142me\x1b[39m\x1b[49m\x1b[38;2;255;119;0m\x1b[48;2;0;60;135mn\x1b[39m\x1b[49m\x1b[38;2;255;131;0m\x1b[48;2;0;65;123mt\x1b[39m\x1b[49m\x1b[38;2;255;139;0m\x1b[48;2;0;69;115ms\x1b[39m\x1b[49m\x1b[38;2;255;146;0m\x1b[48;2;0;73;108m:\x1b[39m\x1b[49m\n\x1b[38;2;255;30;0m\x1b[48;2;0;15;224mF\x1b[39m\x1b[49m\x1b[38;2;255;38;0m\x1b[48;2;0;19;216mo\x1b[39m\x1b[49m\x1b[38;2;255;50;0m\x1b[48;2;0;25;204mr\x1b[39m\x1b[49m\x1b[38;2;255;57;0m\x1b[48;2;0;29;197me\x1b[39m\x1b[49m\x1b[38;2;255;65;0m\x1b[48;2;0;32;189mg\x1b[39m\x1b[49m\x1b[38;2;255;73;0m\x1b[48;2;0;36;181mr\x1b[39m\x1b[49m\x1b[38;2;255;81;0m\x1b[48;2;0;40;173mo\x1b[39m\x1b[49m\x1b[38;2;255;88;0m\x1b[48;2;0;44;166mu\x1b[39m\x1b[49m\x1b[38;2;255;96;0m\x1b[48;2;0;48;158mn\x1b[39m\x1b[49m\x1b[38;2;255;104;0m\x1b[48;2;0;52;150md\x1b[39m\x1b[49m\x1b[38;2;255;112;0m\x1b[48;2;0;56;142m \x1b[39m\x1b[49m\x1b[38;2;255;119;0m\x1b[48;2;0;60;135mR\x1b[39m\x1b[49m\x1b[38;2;255;131;0m\x1b[48;2;0;65;123me\x1b[39m\x1b[49m\x1b[38;2;255;139;0m\x1b[48;2;0;69;115md\x1b[39m\x1b[49m\x1b[38;2;255;146;0m\x1b[48;2;0;73;108m-\x1b[39m\x1b[49m\x1b[38;2;255;154;0m\x1b[48;2;0;77;100m>\x1b[39m\x1b[49m\x1b[38;2;255;162;0m\x1b[48;2;0;81;92mY\x1b[39m\x1b[49m\x1b[38;2;255;170;0m\x1b[48;2;0;85;85me\x1b[39m\x1b[49m\x1b[38;2;255;177;0m\x1b[48;2;0;89;77ml\x1b[39m\x1b[49m\x1b[38;2;255;185;0m\x1b[48;2;0;93;69ml\x1b[39m\x1b[49m\x1b[38;2;255;193;0m\x1b[48;2;0;96;61mo\x1b[39m\x1b[49m\x1b[38;2;255;200;0m\x1b[48;2;0;100;54mw\x1b[39m\x1b[49m\n\x1b[38;2;255;38;0m\x1b[48;2;0;19;216mB\x1b[39m\x1b[49m\x1b[38;2;255;50;0m\x1b[48;2;0;25;204ma\x1b[39m\x1b[49m\x1b[38;2;255;57;0m\x1b[48;2;0;29;197mc\x1b[39m\x1b[49m\x1b[38;2;255;65;0m\x1b[48;2;0;32;189mk\x1b[39m\x1b[49m\x1b[38;2;255;73;0m\x1b[48;2;0;36;181mg\x1b[39m\x1b[49m\x1b[38;2;255;81;0m\x1b[48;2;0;40;173mr\x1b[39m\x1b[49m\x1b[38;2;255;88;0m\x1b[48;2;0;44;166mo\x1b[39m\x1b[49m\x1b[38;2;255;96;0m\x1b[48;2;0;48;158mu\x1b[39m\x1b[49m\x1b[38;2;255;104;0m\x1b[48;2;0;52;150mn\x1b[39m\x1b[49m\x1b[38;2;255;112;0m\x1b[48;2;0;56;142md\x1b[39m\x1b[49m\x1b[38;2;255;119;0m\x1b[48;2;0;60;135m \x1b[39m\x1b[49m\x1b[38;2;255;131;0m\x1b[48;2;0;65;123mB\x1b[39m\x1b[49m\x1b[38;2;255;139;0m\x1b[48;2;0;69;115ml\x1b[39m\x1b[49m\x1b[38;2;255;146;0m\x1b[48;2;0;73;108mu\x1b[39m\x1b[49m\x1b[38;2;255;154;0m\x1b[48;2;0;77;100me\x1b[39m\x1b[49m\x1b[38;2;255;162;0m\x1b[48;2;0;81;92m-\x1b[39m\x1b[49m\x1b[38;2;255;170;0m\x1b[48;2;0;85;85m>\x1b[39m\x1b[49m\x1b[38;2;255;177;0m\x1b[48;2;0;89;77mG\x1b[39m\x1b[49m\x1b[38;2;255;185;0m\x1b[48;2;0;93;69mr\x1b[39m\x1b[49m\x1b[38;2;255;193;0m\x1b[48;2;0;96;61me\x1b[39m\x1b[49m\x1b[38;2;255;200;0m\x1b[48;2;0;100;54me\x1b[39m\x1b[49m\x1b[38;2;255;212;0m\x1b[48;2;0;106;42mn\x1b[39m\x1b[49m\n']

# # Testing named colors and hex colors:
# # ['\x1b[38;2;148;47;45m\x1b[48;2;135;206;235mC\x1b[39m\x1b[49m\x1b[38;2;152;52;43m\x1b[48;2;135;206;235mu\x1b[39m\x1b[49m\x1b[38;2;156;56;42m\x1b[48;2;135;206;235ms\x1b[39m\x1b[49m\x1b[38;2;160;61;40m\x1b[48;2;135;206;235mt\x1b[39m\x1b[49m\x1b[38;2;160;61;40m\x1b[48;2;135;206;235mo\x1b[39m\x1b[49m\x1b[38;2;164;65;38m\x1b[48;2;135;206;235mm\x1b[39m\x1b[49m\x1b[38;2;168;70;36m\x1b[48;2;135;206;235m \x1b[39m\x1b[49m\x1b[38;2;168;70;36m\x1b[48;2;135;206;235mc\x1b[39m\x1b[49m\x1b[38;2;172;74;35m\x1b[48;2;135;206;235mo\x1b[39m\x1b[49m\x1b[38;2;177;79;33m\x1b[48;2;135;206;235ml\x1b[39m\x1b[49m\x1b[38;2;177;79;33m\x1b[48;2;135;206;235mo\x1b[39m\x1b[49m\x1b[38;2;181;83;31m\x1b[48;2;135;206;235mr\x1b[39m\x1b[49m\x1b[38;2;185;88;29m\x1b[48;2;135;206;235ms\x1b[39m\x1b[49m\x1b[38;2;189;92;28m\x1b[48;2;135;206;235m \x1b[39m\x1b[49m\x1b[38;2;189;92;28m\x1b[48;2;135;206;235ma\x1b[39m\x1b[49m\x1b[38;2;193;97;26m\x1b[48;2;135;206;235mn\x1b[39m\x1b[49m\x1b[38;2;197;101;24m\x1b[48;2;135;206;235md\x1b[39m\x1b[49m\x1b[38;2;197;101;24m\x1b[48;2;135;206;235m \x1b[39m\x1b[49m\x1b[38;2;201;106;22m\x1b[48;2;135;206;235mb\x1b[39m\x1b[49m\x1b[38;2;205;110;21m\x1b[48;2;135;206;235ma\x1b[39m\x1b[49m\x1b[38;2;209;115;19m\x1b[48;2;135;206;235mc\x1b[39m\x1b[49m\x1b[38;2;209;115;19m\x1b[48;2;135;206;235mk\x1b[39m\x1b[49m\x1b[38;2;213;119;17m\x1b[48;2;135;206;235mg\x1b[39m\x1b[49m\x1b[38;2;218;124;15m\x1b[48;2;135;206;235mr\x1b[39m\x1b[49m\x1b[38;2;218;124;15m\x1b[48;2;135;206;235mo\x1b[39m\x1b[49m\x1b[38;2;222;128;14m\x1b[48;2;135;206;235mu\x1b[39m\x1b[49m\x1b[38;2;226;133;12m\x1b[48;2;135;206;235mn\x1b[39m\x1b[49m\x1b[38;2;226;133;12m\x1b[48;2;135;206;235md\x1b[39m\x1b[49m\x1b[38;2;230;137;10m\x1b[48;2;135;206;235ms\x1b[39m\x1b[49m']

# # Testing HSL and HSV string parsing:
# # ['\x1b[38;2;0;0;255mThis is HSL blue.\x1b[39m']
# # ['\x1b[38;2;255;0;0m\x1b[48;2;128;0;128mThis is HSV red with purple background.\x1b[39m\x1b[49m']

# # Testing CMYK string parsing:
# # ['\x1b[38;2;255;0;0mThis is CMYK red.\x1b[39m']

# # Testing single gradient color argument:

# # --- Gradient Test: Colors(foreground=[(0, 255, 255), (255, 255, 0)], background=None, angle=0) ---
# # ['\x1b[38;2;23;255;231mS\x1b[39m\x1b[38;2;31;255;223mi\x1b[39m\x1b[38;2;47;255;207mn\x1b[39m\x1b[38;2;55;255;199mg\x1b[39m\x1b[38;2;63;255;191ml\x1b[39m\x1b[38;2;79;255;175me\x1b[39m\x1b[38;2;87;255;167m \x1b[39m\x1b[38;2;103;255;151ml\x1b[39m\x1b[38;2;111;255;143mi\x1b[39m\x1b[38;2;127;255;127ms\x1b[39m\x1b[38;2;135;255;119mt\x1b[39m\x1b[38;2;143;255;111m \x1b[39m\x1b[38;2;159;255;95ma\x1b[39m\x1b[38;2;167;255;87mr\x1b[39m\x1b[38;2;183;255;71mg\x1b[39m\n\x1b[38;2;31;255;223mf\x1b[39m\x1b[38;2;47;255;207mo\x1b[39m\x1b[38;2;55;255;199mr\x1b[39m\x1b[38;2;63;255;191m \x1b[39m\x1b[38;2;79;255;175mF\x1b[39m\x1b[38;2;87;255;167mG\x1b[39m\x1b[38;2;103;255;151m \x1b[39m\x1b[38;2;111;255;143mg\x1b[39m\x1b[38;2;127;255;127mr\x1b[39m\x1b[38;2;135;255;119ma\x1b[39m\x1b[38;2;143;255;111md\x1b[39m\x1b[38;2;159;255;95mi\x1b[39m\x1b[38;2;167;255;87me\x1b[39m\x1b[38;2;183;255;71mn\x1b[39m\x1b[38;2;191;255;63mt\x1b[39m\x1b[38;2;199;255;55m.\x1b[39m\n']

# --- Gradient Test: Colors(foreground=(0, 0, 0), background=[(255, 165, 0), (128, 0, 128)], angle=90) ---
# ['\x1b[38;2;0;0;0m\x1b[48;2;255;165;0mS\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;247;154;8mi\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;239;144;16mn\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;231;134;24mg\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;223;123;32ml\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;215;113;40me\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;207;103;48m \x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;199;92;56ml\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;191;82;64mi\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;187;77;68ms\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;179;67;76mt\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;171;56;84m \x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;163;46;92ma\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;155;36;100mr\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;147;25;108mg\x1b[39m\x1b[49m\n\x1b[38;2;0;0;0m\x1b[48;2;255;165;0mf\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;247;154;8mo\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;239;144;16mr\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;231;134;24m \x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;223;123;32mB\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;215;113;40mG\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;207;103;48m \x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;199;92;56mg\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;191;82;64mr\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;187;77;68ma\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;179;67;76md\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;171;56;84mi\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;163;46;92me\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;155;36;100mn\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;147;25;108mt\x1b[39m\x1b[49m\x1b[38;2;0;0;0m\x1b[48;2;139;15;116m.\x1b[39m\x1b[49m\n']
# ['\x1b[38;2;165;44;0mh\x1b[39m', '\x1b[38;2;153;51;0me\x1b[39m', '\x1b[38;2;127;64;0ml\x1b[39m', '\x1b[38;2;114;70;0ml\x1b[39m', '\x1b[38;2;102;76;0mo\x1b[39m', '\x1b[38;2;76;89;0m \x1b[39m', '\x1b[38;2;63;96;0mw\x1b[39m', '\x1b[38;2;38;108;0mo\x1b[39m', '\x1b[38;2;25;115;0mr\x1b[39m', '\x1b[38;2;12;121;0ml\x1b[39m', '\x1b[38;2;12;129;0md\x1b[39m']
# ['\x1b[38;2;153;51;0mt\x1b[39m', '\x1b[38;2;127;64;0mh\x1b[39m', '\x1b[38;2;114;70;0mi\x1b[39m', '\x1b[38;2;102;76;0ms\x1b[39m', '\x1b[38;2;76;89;0m \x1b[39m', '\x1b[38;2;63;96;0mi\x1b[39m', '\x1b[38;2;38;108;0ms\x1b[39m', '\x1b[38;2;25;115;0m \x1b[39m', '\x1b[38;2;12;121;0mm\x1b[39m', '\x1b[38;2;12;129;0mu\x1b[39m', '\x1b[38;2;25;131;0ml\x1b[39m', '\x1b[38;2;38;133;0mt\x1b[39m', '\x1b[38;2;63;137;0mi\x1b[39m', '\x1b[38;2;76;139;0m \x1b[39m', '\x1b[38;2;89;140;0mc\x1b[39m', '\x1b[38;2;114;144;0mo\x1b[39m', '\x1b[38;2;127;146;0ml\x1b[39m', '\x1b[38;2;153;150;0mo\x1b[39m', '\x1b[38;2;165;152;0mr\x1b[39m', '\x1b[38;2;178;153;0me\x1b[39m', '\x1b[38;2;204;157;0md\x1b[39m', '\x1b[38;2;216;159;0m \x1b[39m', '\x1b[38;2;229;161;0mt\x1b[39m', '\x1b[38;2;255;165;0me\x1b[39m', '\x1b[38;2;255;166;10mx\x1b[39m', '\x1b[38;2;255;167;20mt\x1b[39m', '\x1b[38;2;255;170;40m \x1b[39m', '\x1b[38;2;255;171;50mt\x1b[39m', '\x1b[38;2;255;174;71me\x1b[39m', '\x1b[38;2;255;175;81ms\x1b[39m', '\x1b[38;2;255;177;91mt\x1b[39m']
