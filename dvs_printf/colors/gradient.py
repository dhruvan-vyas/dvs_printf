
from typing import Tuple, List, Generator
from math   import sqrt, radians, sin, cos
from dvs_printf._printf_helper import modifyed, Modifier
from .ansi  import (
    RESET_FOREGROUND as RESET_FG,
    RESET_BACKGROUND as RESET_BG,
    rgb_to_ansi_func,
    rgb_to_bg_ansi_func,
    values_to_ansi_fg,
    values_to_ansi_bg
)

StrArray = list[str]




def apply_gradient(
    text_list: List[str],
    colors: List[Tuple[int, int, int]],
    background: Tuple[int, int, int] | List[Tuple[int, int, int], ] | bool = False,
    angle: int | None = None,
    reset: bool | None = True,
    is_gradient_pre_config: bool | None = None,
) -> Generator[list[str], None, None]:
    """
    Applies a gradient to a list of strings `text_list` with foreground and
    optional background color gradients.

    Args:
        text_list (List[str]): The text to which the gradient will be applied.
        colors (List[Tuple[int, int, int]]): A list of foreground color tuples (RGB).
                                          If one color is provided, it's a static color.
                                          If more than one, it's a gradient.
        background (Tuple | List | bool): Optional background color(s).
                                          - Tuple: A static background color (RGB).
                                          - List: A list of background color tuples (RGB) for a gradient.
                                          - True: Applies a static black background.
                                          - False: No background color.
        angle (int | None): The angle of the gradient in degrees.
        reset (bool | None): Whether to apply an ANSI reset code at the end of each line.

    Yields:
        Generator[list[str], None, None]: A generator that yields a list of
                                          colored strings for each line of the input text.
    """

    # --- Initial Validation & Setup ---
    
    if is_gradient_pre_config: 
        (
            is_static_fg_color,
            is_static_bg_color,
            is_fg_gradient,
            is_bg_gradient,

        ) = is_gradient_pre_config

    else:
        # Check if a foreground gradient is requested.
        is_fg_gradient = len(colors) > 1

        # Check if a static fourbackground color is requested.
        is_static_fg_color = not is_fg_gradient
        
        # Check if a background gradient is requested.
        is_bg_gradient = isinstance(background, list) 
        
        # Check if a static background color is requested.
        is_static_bg_color = isinstance(background, tuple) or background is True

    # Validate that at least one gradient is requested.
    if not is_fg_gradient and not is_bg_gradient:
        raise ValueError("From Grid: At least two foreground or two background colors are required for a gradient.")

    
    # Main gredinat Logic
    text_list = tuple(text_list)
    num_rows = len(text_list)
    num_cols = max(len(line) for line in text_list) if num_rows > 0 else 0
    Modifier().maxStrLen = num_cols
    total_chars = num_rows * num_cols

    if total_chars == 0:
        yield []
        return

    # --- Setup gradient space ---
    center_x, center_y = num_rows / 2, num_cols / 2
    max_distance = sqrt(center_x**2 + center_y**2)
    angle_rad = radians(angle or 45)
    cos_angle_rad, sin_angle_rad = cos(angle_rad), sin(angle_rad)
    max_distance_2 = 2 * max_distance

    def make_gradient(steps: int, palette: List[Tuple[int, int, int]], color_func) -> List[str]:
        """Creates a list of ANSI color strings for a gradient."""
        grad = []
        num_palette_colors = len(palette)
        steps_per_segment = steps // (num_palette_colors - 1) if num_palette_colors > 1 else steps

        for i in range(num_palette_colors - 1):
            start, end = palette[i], palette[i + 1]
            for j in range(steps_per_segment):
                t = j / steps_per_segment
                grad.append(
                    color_func(
                        int(start[0] + (end[0] - start[0]) * t),
                        int(start[1] + (end[1] - start[1]) * t),
                        int(start[2] + (end[2] - start[2]) * t),
                ))
        grad.append(color_func(*palette[-1]))
        return grad


    # Determine the appropriate reset code based on the colors in use.
    reset_code = ""
    if reset: # HEW VERSION
        if is_fg_gradient or is_static_fg_color:
            reset_code += RESET_FG
        if is_bg_gradient or is_static_bg_color:
            reset_code += RESET_BG

    # Log("[THIS IS RESET - T]:", f'{[reset, reset_code], [RESET_FG, RESET_BG]}\n\n\n')
    
    # --- Main Logic: Define color components and coloring function ---
    fg_colors = colors
    bg_colors = background if is_bg_gradient else []
    static_color_ansi = ''

    # Initialize a static background color if one is provided.
    if is_static_bg_color:
        if isinstance(background, (list, tuple)):
            static_color_ansi = rgb_to_bg_ansi_func(*background) 

        else:
            static_color_ansi = values_to_ansi_bg(background) if background and background != True else None

    # Initialize a static foreground color if one is provided.
    if is_static_fg_color:
        if isinstance(background, (list, tuple)):
            static_color_ansi = values_to_ansi_fg(fg_colors[0]) 
        else:
            static_color_ansi = rgb_to_ansi_func(*fg_colors) 


    # Generate gradients based on the input
    fg_gradient_ansi = None
    if is_fg_gradient:
        fg_gradient_ansi = make_gradient(total_chars, fg_colors, rgb_to_ansi_func)

    bg_gradient_ansi = None
    if is_bg_gradient:
        bg_gradient_ansi = make_gradient(total_chars, bg_colors, rgb_to_bg_ansi_func)

    
    # apply gredint to str function 
    # if is_fg_gradient and is_bg_gradient:   
    #     color_func =        (lambda idx, ch: f"{fg_gradient_ansi[idx]}{bg_gradient_ansi[idx]}{ch}{reset_code}" 
    #         ) if reset else (lambda idx, ch: f"{fg_gradient_ansi[idx]}{bg_gradient_ansi[idx]}{ch}")
        
    # elif is_fg_gradient and static_color_ansi:       
    #     color_func =        (lambda idx, ch: f"{fg_gradient_ansi[idx]}{static_color_ansi}{ch}{reset_code}" 
    #         ) if reset else (lambda idx, ch: f"{fg_gradient_ansi[idx]}{static_color_ansi}{ch}")
        
    # elif is_bg_gradient and static_color_ansi: 
    #     color_func =        (lambda idx, ch: f"{static_color_ansi}{bg_gradient_ansi[idx]}{ch}{reset_code}" 
    #         ) if reset else (lambda idx, ch: f"{static_color_ansi}{bg_gradient_ansi[idx]}{ch}")
        
    # elif is_fg_gradient:                         
    #     color_func =        (lambda idx, ch: f"{fg_gradient_ansi[idx]}{ch}{reset_code}" 
    #         ) if reset else (lambda idx, ch: f"{fg_gradient_ansi[idx]}{ch}")
        
    # else: 
    #     color_func =        (lambda idx, ch: f"{bg_gradient_ansi[idx]}{ch}{reset_code}" 
    #         ) if reset else (lambda idx, ch: f"{bg_gradient_ansi[idx]}{ch}")

    
    if is_fg_gradient and is_bg_gradient:   
        color_func =        (lambda idx, ch: fg_gradient_ansi[idx] + bg_gradient_ansi[idx] + ch + reset_code
            ) if reset else (lambda idx, ch: fg_gradient_ansi[idx] + bg_gradient_ansi[idx] + ch )
        
    elif is_fg_gradient and static_color_ansi:   
        color_func =        (lambda idx, ch: fg_gradient_ansi[idx] + static_color_ansi + ch + reset_code 
            ) if reset else (lambda idx, ch: fg_gradient_ansi[idx] + static_color_ansi + ch )
        
    elif is_bg_gradient and static_color_ansi:
        color_func =        (lambda idx, ch: static_color_ansi + bg_gradient_ansi[idx] + ch + reset_code
            ) if reset else (lambda idx, ch: static_color_ansi + bg_gradient_ansi[idx] + ch )
        
    elif is_fg_gradient:
        color_func =        (lambda idx, ch: fg_gradient_ansi[idx] + ch + reset_code
            ) if reset else (lambda idx, ch: fg_gradient_ansi[idx] + ch )
        
    else: 
        color_func =        (lambda idx, ch: bg_gradient_ansi[idx] + ch + reset_code 
            ) if reset else (lambda idx, ch: bg_gradient_ansi[idx] + ch )

    # --- Gradient application loop ---
    gradient_len = len(fg_gradient_ansi or bg_gradient_ansi) - 1
    
    # for row_idx, line in enumerate(text_list):
    #     colored_line = [None] * len(line)
    #     print("start Gen Apply")
    #     for col_idx, char in enumerate(line):
    #         i = int(( (row_idx - center_x) * cos_angle_rad
    #                 + (col_idx - center_y) * sin_angle_rad
    #                 + max_distance
    #               ) / max_distance_2
    #                 * gradient_len
    #         )
    #         colored_line[col_idx] = color_func(i, char)
    #     yield colored_line

        #     colored_line[col_idx] = color_func(int(
        #                                 (   (row_idx - center_x) * cos_angle_rad
        #                                   + (col_idx - center_y) * sin_angle_rad
        #                                   + max_distance
        #                                 ) / max_distance_2
        #                                   * gradient_len
        #                             ), char)


    # for row_idx, line in enumerate(text_list):
    yield from (
        [
            color_func(
                int((   (row_idx - center_x) * cos_angle_rad
                      + (col_idx - center_y) * sin_angle_rad
                      + max_distance
                    ) / max_distance_2
                      * gradient_len
                ), char
            ) for col_idx, char in enumerate(line) 
        ] for row_idx, line in enumerate(text_list)
    )
        # yield colored_line

