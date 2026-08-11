from ..colors.ansi import (
        rgb_to_ansi_func, 
        rgb_to_bg_ansi_func, 
        RESET
    )

# Pre-build ANSI style fragments
RED     = rgb_to_ansi_func(230,   0,   0)
ORANGE  = rgb_to_ansi_func(255, 140,   0)
PURPLE  = rgb_to_ansi_func(155,  82, 199)
GREEN   = rgb_to_ansi_func( 28, 131,  99)
PEACH   = rgb_to_ansi_func(206, 145, 120)
GRAY    = rgb_to_ansi_func(110, 118, 129)

# _Warning colors
YELLOW  = rgb_to_ansi_func(255, 255,   0)
SKYBLUE = rgb_to_ansi_func( 51, 204, 255) # OLDER (  0, 204, 255)

# Dark_RED    = "\033[1m"+RED

# __all__ = [
#     'RESET',
#     'RED',
#     'PURPLE',
#     'PEACH',
#     'ORANGE',
#     'GREEN',
#     'Dark_RED',
#     'GRAY',
#     'GRAY2',
#     'PURPLE',
# ]

# PEACH        = rgb_to_ansi_func(206, 145, 120)
# PURPLE         = rgb_to_ansi_func(155, 82, 199)
# PURPLE       = rgb_to_ansi_func(155, 82, 199)

# GREEN    = rgb_to_ansi_func(28, 131, 99)
# GRAY        = rgb_to_ansi_func(110, 118, 129)
# ORANGE      = rgb_to_ansi_func(255, 140, 0)
# RED         = rgb_to_ansi_func(230, 0, 0)
# Dark_RED    = "\033[1m"+RED

# PURPLE       = rgb_to_ansi_func(155, 82, 199)



	# •	(206, 145, 120) → Rosy Brown / Light Brown Peach
	# •	(155, 82, 199) → Amethyst / Medium Purple
	# •	(28, 131, 99) → Sea Green / Jungle Green
	# •	(110, 118, 129) → Slate Gray
	# •	(255, 140, 0) → Dark Orange
	# •	(230, 0, 0) → Red (close to Crimson)

	# •	(155, 82, 199) → same as above → Amethyst / Medium Purple

# GRAY2       = rgb_to_bg_ansi_func(224, 255, 255) + GRAY        



# # Pre-build ANSI style fragments
# LIGHTYELLOW = rgb_to_ansi_func(255, 255,   0)
# SKYBLUE2    = rgb_to_ansi_func(  0, 204, 255)

# # __all__ = [
# #     'RESET',
# #     'RED',
# #     'PURPLE',
# #     'PEACH',
# #     'ORANGE',
# #     'GREEN',
# #     'Dark_RED',
# #     'GRAY',
# #     'GRAY2',
# #     'PURPLE',
# # ]

# PEACH  = rgb_to_ansi_func(206, 145, 120)
# PURPLE   = rgb_to_ansi_func(155,  82, 199)

# GREEN = rgb_to_ansi_func(28,131,99)
# GRAY = rgb_to_ansi_func(110,118,129)

# # ORANGE = "\033[38;5;208m"                                 # name_to_color("darkorange") if console_EnvType > 1 else
# ORANGE = rgb_to_ansi_func(255, 140,   0)

# GRAY2 = rgb_to_bg_ansi_func(224, 255, 255) + GRAY         # name_to_color("grey35") if console_EnvType > 1 else 

# PURPLE = rgb_to_ansi_func(155, 82,199)

# # Dark_RED = "\033[1m\033[31m" #OLD
# # RED = "\033[31m" OLD
 
# RED = rgb_to_ansi_func(230, 0, 0)
# # RED2 = rgb_to_ansi_func(220, 20, 20)
# Dark_RED = "\033[1m"+RED
# # print(RED+"THIS IS OLD RED", RESET, NEW_RED + "THIS IS NEW RED")





