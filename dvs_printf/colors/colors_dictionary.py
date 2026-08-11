from   typing                       import Generator      , Tuple      , List
from  .ansi                         import console_EnvType, Font_Styles, RESET
from ..exceptions.colors_exception  import ColorsValueError
from ..exceptions._colored_vars     import * 

Ansi_Int = int
R        = RESET
B        = Font_Styles.BOLD   
I        = Font_Styles.ITALIC 

del Font_Styles


if console_EnvType >= 3: Color_Dict = { # 16 colors ansi or no colors(monocromic) Env_Type: (3, 4)

# NAME              RGB             16Ansi  HEX_INT    INT
'black':         ( (  0,   0,   0), 30 ), # 0x0     ,         0,
'red':           ( (255,   0,   0), 31 ), # 0xff0000,  16711680,
'green':         ( (  0, 128,   0), 32 ), # 0x8000  ,     32768,
'yellow':        ( (255, 255,   0), 33 ), # 0xffff00,  16776960,
'blue':          ( (  0,   0, 255), 34 ), # 0xff    ,       255,
'magenta':       ( (255,   0, 255), 35 ), # 0xff00ff,  16711935,
'cyan':          ( (  0, 255, 255), 36 ), # 0xffff  ,     65535,
'white':         ( (255, 255, 255), 37 ), # 0xffffff,  16777215,
'lightblack':    ( ( 51,   0,   0), 90 ), # 0x330000,   3342336,
'lightred':      ( (204,   0,   0), 91 ), # 0xcc0000,  13369344,
'lightgreen':    ( (  0, 153,   0), 92 ), # 0x9900  ,     39168,
'lightyellow':   ( (255, 255,   0), 93 ), # 0xffff00,  16776960,
'lightblue':     ( (  0,   0, 255), 94 ), # 0xff    ,       255,
'lightmagenta':  ( (255,   0, 204), 95 ), # 0xff00cc,  16711884,
'lightcyan':     ( (224, 255, 255), 96 ), # 0xe0ffff,  14745599,
'lightwhite':    ( (204, 204, 204), 97 ), # 0xcccccc,  13421772,
}

else: Color_Dict = {     #  console_EnvType is (1 or 2):
    
# NAME                      RGB             256Ansi   HEX_INT    INT
'black':                 ( (  0,   0,   0),   0 ),  # 0x0     ,         0,
'red':                   ( (255,   0,   0),   9 ),  # 0xff0000,  16711680,
'green':                 ( (  0, 128,   0),   2 ),  # 0x8000  ,     32768,
'yellow':                ( (255, 255,   0),  11 ),  # 0xffff00,  16776960,
'blue':                  ( (  0,   0, 255),  12 ),  # 0xff    ,       255,
'magenta':               ( (255,   0, 255),  13 ),  # 0xff00ff,  16711935,
'cyan':                  ( (  0, 255, 255),  14 ),  # 0xffff  ,     65535,
'white':                 ( (255, 255, 255),  15 ),  # 0xffffff,  16777215,
'lightblack':            ( ( 51,   0,   0),  52 ),  # 0x330000,   3342336,
'lightred':              ( (204,   0,   0), 160 ),  # 0xcc0000,  13369344,
'lightgreen':            ( (  0, 153,   0),  34 ),  # 0x9900  ,     39168,
'lightyellow':           ( (255, 255,   0), 226 ),  # 0xffff00,  16776960,
'lightblue':             ( (  0,   0, 255),  21 ),  # 0xff    ,       255,
'lightmagenta':          ( (255,   0, 204), 200 ),  # 0xff00cc,  16711884,
'lightcyan':             ( (224, 255, 255), 195 ),  # 0xe0ffff,  14745599,
'lightwhite':            ( (204, 204, 204), 188 ),  # 0xcccccc,  13421772,
'aliceblue':             ( (240, 248, 255),  15 ),  # 0xf0f8ff,  15792383,
'antiquewhite':          ( (250, 235, 215), 224 ),  # 0xfaebd7,  16444375,
'aqua':                  ( (  0, 255, 255),  14 ),  # 0xffff  ,     65535,
'aqua2':                 ( (  0, 255, 255),  51 ),  # 0xffff  ,     65535,
'aquamarine':            ( (127, 255, 212), 122 ),  # 0x7fffd4,   8388564,
'aquamarine2':           ( (153, 255, 204), 158 ),  # 0x99ffcc,  10092492,
'aquamarine3':           ( (  0, 255, 153),  49 ),  # 0xff99  ,     65433,
'avocado':               ( (102, 153,   0), 106 ),  # 0x669900,   6723840,
'azure':                 ( (240, 255, 255),  15 ),  # 0xf0ffff,  15794175,
'babyblue':              ( ( 51, 204, 255),  81 ),  # 0x33ccff,   3394815,
'babybluelight':         ( (204, 204, 255), 189 ),  # 0xccccff,  13421823,
'babylavender':          ( (153, 153, 204), 146 ),  # 0x9999cc,  10066380,
'beige':                 ( (245, 245, 220), 230 ),  # 0xf5f5dc,  16119260,
'bisque':                ( (255, 228, 196), 224 ),  # 0xffe4c4,  16770244,
'blanchedalmond':        ( (255, 235, 205), 224 ),  # 0xffebcd,  16772045,
'bluebell':              ( (102, 102, 255), 105 ),  # 0x6666ff,   6711039,
'blueviolet':            ( (138,  43, 226),  92 ),  # 0x8a2be2,   9055202,
'blueviolet2':           ( (153,  51, 255), 135 ),  # 0x9933ff,  10040319,
'brick':                 ( (153,  51,  51), 131 ),  # 0x993333,  10040115,
'brown':                 ( (165,  42,  42), 124 ),  # 0xa52a2a,  10824234,
'brown2':                ( (153,  51, 102), 132 ),  # 0x993366,  10040166,
'bubblegum':             ( (204, 102, 255), 177 ),  # 0xcc66ff,  13395711,
'burlywood':             ( (222, 184, 135), 180 ),  # 0xdeb887,  14596231,
'burntorange':           ( (204, 102,   0), 172 ),  # 0xcc6600,  13395456,
'butter':                ( (204, 153,  51), 179 ),  # 0xcc9933,  13408563,
'cadetblue':             ( ( 95, 158, 160),  73 ),  # 0x5f9ea0,   6266528,
'cadetblue2':            ( (102, 153, 153), 109 ),  # 0x669999,   6723993,
'candy':                 ( (204,  51, 153), 169 ),  # 0xcc3399,  13382553,
'carnation':             ( (255, 102, 153), 211 ),  # 0xff6699,  16737945,
'chartreuse':            ( (127, 255,   0), 118 ),  # 0x7fff00,   8388352,
'chartreuse2':           ( (  0, 255,  51),  47 ),  # 0xff33  ,     65331,
'chocolate':             ( (210, 105,  30), 166 ),  # 0xd2691e,  13789470,
'coral':                 ( (255, 127,  80), 209 ),  # 0xff7f50,  16744272,
'cornflowerblue':        ( (100, 149, 237),  69 ),  # 0x6495ed,   6591981,
'cornflowerblue2':       ( ( 51,  51, 255),  63 ),  # 0x3333ff,   3355647,
'cornsilk':              ( (255, 248, 220), 230 ),  # 0xfff8dc,  16775388,
'cottoncandy':           ( (204, 102, 153), 175 ),  # 0xcc6699,  13395609,
'cream':                 ( (255, 255, 153), 229 ),  # 0xffff99,  16777113,
'crimson':               ( (220,  20,  60), 161 ),  # 0xdc143c,  14423100,
'crimson2':              ( (255,  51,  51), 203 ),  # 0xff3333,  16724787,
'crimson3':              ( (153,   0,  51), 125 ),  # 0x990033,  10027059,
'darkblue':              ( (  0,   0, 139),  18 ),  # 0x8b    ,       139,
'darkblue2':             ( (  0,   0, 153),  19 ),  # 0x99    ,       153,
'darkblue3':             ( ( 51,   0, 204),  56 ),  # 0x3300cc,   3342540,
'darkcyan':              ( (  0, 139, 139),  30 ),  # 0x8b8b  ,     35723,
'darkcyan2':             ( (  0,  51, 102),  24 ),  # 0x3366  ,     13158,
'darkgoldenrod':         ( (184, 134,  11), 136 ),  # 0xb8860b,  12092939,
'darkgray':              ( (169, 169, 169), 248 ),  # 0xa9a9a9,  11119017,
'darkgreen':             ( (  0, 100,   0),  22 ),  # 0x6400  ,     25600,
'darkgreen2':            ( ( 51,  51,   0),  58 ),  # 0x333300,   3355392,
'darkgrey':              ( (169, 169, 169), 248 ),  # 0xa9a9a9,  11119017,
'darkgrey2':             ( ( 51,  51,  51),  59 ),  # 0x333333,   3355443,
'darkkhaki':             ( (189, 183, 107), 143 ),  # 0xbdb76b,  12433259,
'darkkhaki2':            ( (204, 204, 102), 186 ),  # 0xcccc66,  13421670,
'darkmagenta':           ( (139,   0, 139),  90 ),  # 0x8b008b,   9109643,
'darkmagenta2':          ( (153,   0, 153), 127 ),  # 0x990099,  10027161,
'darkmagenta3':          ( (102,  51, 102),  96 ),  # 0x663366,   6697830,
'darkolivegreen':        ( ( 85, 107,  47), 239 ),  # 0x556b2f,   5597999,
'darkolivegreen2':       ( ( 51, 102,  51),  65 ),  # 0x336633,   3368499,
'darkorange':            ( (255, 140,   0), 208 ),  # 0xff8c00,  16747520,
'darkorchid':            ( (153,  50, 204),  98 ),  # 0x9932cc,  10040012,
'darkred':               ( (139,   0,   0),  88 ),  # 0x8b0000,   9109504,
'darkred2':              ( (153,   0,   0), 124 ),  # 0x990000,  10027008,
'darkrose':              ( (102,  51,  51),  95 ),  # 0x663333,   6697779,
'darksalmon':            ( (233, 150, 122), 174 ),  # 0xe9967a,  15308410,
'darkseagreen':          ( (143, 188, 143), 108 ),  # 0x8fbc8f,   9419919,
'darkseagreen2':         ( (153, 204, 153), 151 ),  # 0x99cc99,  10079385,
'darkslateblue':         ( ( 72,  61, 139),  60 ),  # 0x483d8b,   4734347,
'darkslateblue2':        ( ( 51,  51, 153),  61 ),  # 0x333399,   3355545,
'darkslategray':         ( ( 47,  79,  79), 238 ),  # 0x2f4f4f,   3100495,
'darkslategrey':         ( ( 47,  79,  79), 238 ),  # 0x2f4f4f,   3100495,
'darkslategray2':        ( (  0,  51,  51),  23 ),  # 0x3333  ,     13107,
'darkturquoise':         ( (  0, 206, 209),  44 ),  # 0xced1  ,     52945,
'darkviolet':            ( (148,   0, 211),  92 ),  # 0x9400d3,   9699539,
'darkviolet2':           ( ( 51,   0, 153),  55 ),  # 0x330099,   3342489,
'deepmagenta':           ( (204,   0, 204), 164 ),  # 0xcc00cc,  13369548,
'deeppink':              ( (255,  20, 147), 198 ),  # 0xff1493,  16716947,
'deeppink2':             ( (255,  51, 153), 205 ),  # 0xff3399,  16724889,
'deepskyblue':           ( (  0, 191, 255),  39 ),  # 0xbfff  ,     49151,
'deepskyblue2':          ( (  0, 204, 255),  45 ),  # 0xccff  ,     52479,
'dimgray':               ( (105, 105, 105), 242 ),  # 0x696969,   6908265,
'dimgrey':               ( (105, 105, 105), 242 ),  # 0x696969,   6908265,
'dodgerblue':            ( ( 30, 144, 255),  33 ),  # 0x1e90ff,   2003199,
'dodgerblue2':           ( ( 51, 153, 255),  75 ),  # 0x3399ff,   3381759,
'dodgerblue3':           ( (  0,  51, 255),  27 ),  # 0x33ff  ,     13311,
'dustrose':              ( (153, 102, 153), 139 ),  # 0x996699,  10053273,
'electricpurple':        ( (153,   0, 255), 129 ),  # 0x9900ff,  10027263,
'firebrick':             ( (178,  34,  34), 124 ),  # 0xb22222,  11674146,
'floralwhite':           ( (255, 250, 240),  15 ),  # 0xfffaf0,  16775920,
'forestgreen':           ( ( 34, 139,  34),  28 ),  # 0x228b22,   2263842,
'forestgreen2':          ( ( 51, 153,   0),  70 ),  # 0x339900,   3381504,
'forestgreen3':          ( (  0, 153,  51),  35 ),  # 0x9933  ,     39219,
'fuchsia':               ( (255,   0, 255),  13 ),  # 0xff00ff,  16711935,
'fuchsia2':              ( (204,   0, 255), 165 ),  # 0xcc00ff,  13369599,
'fuchsia3':              ( (255,   0, 255), 201 ),  # 0xff00ff,  16711935,
'gainsboro':             ( (220, 220, 220), 253 ),  # 0xdcdcdc,  14474460,
'ghostwhite':            ( (248, 248, 255),  15 ),  # 0xf8f8ff,  16316671,
'gold':                  ( (255, 215,   0), 220 ),  # 0xffd700,  16766720,
'gold2':                 ( (255, 204,  51), 221 ),  # 0xffcc33,  16763955,
'goldenrod':             ( (218, 165,  32), 178 ),  # 0xdaa520,  14329120,
'gray':                  ( (128, 128, 128),   8 ),  # 0x808080,   8421504,
'greenleaf':             ( ( 51, 204,   0),  76 ),  # 0x33cc00,   3394560,
'greenyellow':           ( (173, 255,  47), 154 ),  # 0xadff2f,  11403055,
'greenyellow2':          ( (204, 255,  51), 191 ),  # 0xccff33,  13434675,
'greenyellow3':          ( (204, 255,   0), 190 ),  # 0xccff00,  13434624,
'grey':                  ( (128, 128, 128),   8 ),  # 0x808080,   8421504,
'honeydew':              ( (240, 255, 240), 255 ),  # 0xf0fff0,  15794160,
'hotpink':               ( (255, 105, 180), 205 ),  # 0xff69b4,  16738740,
'hotpink2':              ( (255,  51, 204), 206 ),  # 0xff33cc,  16724940,
'ice':                   ( (102, 255, 255), 123 ),  # 0x66ffff,   6750207,
'indianred':             ( (205,  92,  92), 167 ),  # 0xcd5c5c,  13458524,
'indigo':                ( ( 75,   0, 130),  54 ),  # 0x4b0082,   4915330,
'indigo2':               ( (102,   0, 255),  93 ),  # 0x6600ff,   6684927,
'ivory':                 ( (255, 255, 240),  15 ),  # 0xfffff0,  16777200,
'khaki':                 ( (240, 230, 140), 222 ),  # 0xf0e68c,  15787660,
'khaki2':                ( (102, 102,  51), 101 ),  # 0x666633,   6710835,
'lavender':              ( (230, 230, 250), 255 ),  # 0xe6e6fa,  15132410,
'lavender2':             ( (204, 102, 204), 176 ),  # 0xcc66cc,  13395660,
'lavenderblue':          ( (153, 102, 204), 140 ),  # 0x9966cc,  10053324,
'lavenderblush':         ( (255, 240, 245),  15 ),  # 0xfff0f5,  16773365,
'lavenderrose':          ( (255, 102, 204), 212 ),  # 0xff66cc,  16737996,
'lawngreen':             ( (124, 252,   0), 118 ),  # 0x7cfc00,   8190976,
'lawngreen2':            ( (102, 255,  51), 119 ),  # 0x66ff33,   6750003,
'lemon':                 ( (204, 204,  51), 185 ),  # 0xcccc33,  13421619,
'lemonbright':           ( (255, 255,  51), 227 ),  # 0xffff33,  16777011,
'lemonchiffon':          ( (255, 250, 205), 230 ),  # 0xfffacd,  16775885,
'lightblue2':            ( (173, 216, 230), 152 ),  # 0xadd8e6,  11393254,
'lightcoral':            ( (240, 128, 128), 210 ),  # 0xf08080,  15761536,
'lightcyan2':            ( ( 51, 255, 255),  87 ),  # 0x33ffff,   3407871,
'lightgoldenrodyellow':  ( (250, 250, 210), 230 ),  # 0xfafad2,  16448210,
'lightgray':             ( (211, 211, 211), 252 ),  # 0xd3d3d3,  13882323,
'lightgreen2':           ( (144, 238, 144), 120 ),  # 0x90ee90,   9498256,
'lightgreen3':           ( (102, 255, 153), 121 ),  # 0x66ff99,   6750105,
'lightgreen4':           ( (102, 204, 102), 114 ),  # 0x66cc66,   6736998,
'lightgrey':             ( (211, 211, 211), 252 ),  # 0xd3d3d3,  13882323,
'lightlavender':         ( (255, 204, 255), 225 ),  # 0xffccff,  16764159,
'lightolive':            ( (153, 204, 102), 150 ),  # 0x99cc66,  10079334,
'lightpink':             ( (255, 182, 193), 217 ),  # 0xffb6c1,  16758465,
'lightsalmon':           ( (255, 160, 122), 216 ),  # 0xffa07a,  16752762,
'lightseagreen':         ( ( 32, 178, 170),  37 ),  # 0x20b2aa,   2142890,
'lightseagreen2':        ( (  0, 153, 204),  38 ),  # 0x99cc  ,     39372,
'lightskyblue':          ( (135, 206, 250), 117 ),  # 0x87cefa,   8900346,
'lightslate':            ( (102, 102, 153), 103 ),  # 0x666699,   6710937,
'lightslategray':        ( (119, 136, 153), 102 ),  # 0x778899,   7833753,
'lightslategrey':        ( (119, 136, 153), 102 ),  # 0x778899,   7833753,
'lightsteelblue':        ( (176, 196, 222), 152 ),  # 0xb0c4de,  11584734,
'lightyellow2':          ( (255, 255, 224), 230 ),  # 0xffffe0,  16777184,
'lightyellow3':          ( (255, 255, 102), 228 ),  # 0xffff66,  16777062,
'lime':                  ( (  0, 255,   0),  10 ),  # 0xff00  ,     65280,
'lime2':                 ( ( 51, 255,   0),  82 ),  # 0x33ff00,   3407616,
'lime3':                 ( (  0, 255,   0),  46 ),  # 0xff00  ,     65280,
'limegreen':             ( ( 50, 205,  50),  77 ),  # 0x32cd32,   3329330,
'limegreen2':            ( (102, 204,  51), 113 ),  # 0x66cc33,   6736947,
'limegreen3':            ( (  0, 204,   0),  40 ),  # 0xcc00  ,     52224,
'linen':                 ( (250, 240, 230), 255 ),  # 0xfaf0e6,  16445670,
'maroon':                ( (128,   0,   0),   1 ),  # 0x800000,   8388608,
'maroon2':               ( (102,   0,  51),  89 ),  # 0x660033,   6684723,
'mediumaquamarine':      ( (102, 205, 170),  79 ),  # 0x66cdaa,   6737322,
'mediumaquamarine2':     ( (102, 204, 153), 115 ),  # 0x66cc99,   6737049,
'mediumblue':            ( (  0,   0, 205),  20 ),  # 0xcd    ,       205,
'mediumorchid':          ( (186,  85, 211), 134 ),  # 0xba55d3,  12211667,
'mediumorchid2':         ( (204,  51, 255), 171 ),  # 0xcc33ff,  13382655,
'mediumpurple':          ( (147, 112, 219),  98 ),  # 0x9370db,   9662683,
'mediumpurple2':         ( (155,  82, 199), 140 ),  # 0x9370db,   9662683,
'mediumseagreen':        ( ( 60, 179, 113),  71 ),  # 0x3cb371,   3978097,
'mediumseagreen2':       ( (  0, 204, 102),  42 ),  # 0xcc66  ,     52326,
'mediumslateblue':       ( (123, 104, 238),  99 ),  # 0x7b68ee,   8087790,
'mediumspring':          ( ( 51, 204, 102),  78 ),  # 0x33cc66,   3394662,
'mediumspringgreen':     ( (  0, 250, 154),  48 ),  # 0xfa9a  ,     64154,
'mediumturquoise':       ( ( 72, 209, 204),  80 ),  # 0x48d1cc,   4772300,
'mediumturquoise2':      ( (  0, 255, 204),  50 ),  # 0xffcc  ,     65484,
'mediumvioletred':       ( (199,  21, 133), 162 ),  # 0xc71585,  13047173,
'mediumvioletred2':      ( (204,   0, 153), 163 ),  # 0xcc0099,  13369497,
'midnightblue':          ( ( 25,  25, 112),   4 ),  # 0x191970,   1644912,
'midnightblue2':         ( ( 51,   0,  51),  53 ),  # 0x330033,   3342387,
'midnightblue3':         ( (  0,   0,  51),  17 ),  # 0x33    ,        51,
'mint':                  ( ( 51, 255, 153),  85 ),  # 0x33ff99,   3407769,
'mintcream':             ( (245, 255, 250),  15 ),  # 0xf5fffa,  16121850,
'mintcream2':            ( (204, 255, 204), 194 ),  # 0xccffcc,  13434828,
'mintleaf':              ( (153, 255, 102), 156 ),  # 0x99ff66,  10092390,
'mintpastel':            ( (153, 255, 153), 157 ),  # 0x99ff99,  10092441,
'mistyrose':             ( (255, 228, 225), 224 ),  # 0xffe4e1,  16770273,
'moccasin':              ( (255, 228, 181), 223 ),  # 0xffe4b5,  16770229,
'mustard':               ( (204, 204,   0), 184 ),  # 0xcccc00,  13421568,
'navajowhite':           ( (255, 222, 173), 223 ),  # 0xffdead,  16768685,
'navy':                  ( (  0,   0, 128),   4 ),  # 0x80    ,       128,
'neongreen':             ( ( 51, 255,  51),  83 ),  # 0x33ff33,   3407667,
'neonpink':              ( (255,  51, 102), 204 ),  # 0xff3366,  16724838,
'oldlace':               ( (253, 245, 230), 230 ),  # 0xfdf5e6,  16643558,
'olive':                 ( (128, 128,   0),   3 ),  # 0x808000,   8421376,
'olive2':                ( (153, 153,   0), 142 ),  # 0x999900,  10066176,
'olive3':                ( (102, 102,   0), 100 ),  # 0x666600,   6710784,
'olivedrab':             ( (107, 142,  35),  64 ),  # 0x6b8e23,   7048739,
'olivedrab2':            ( (102, 153,  51), 107 ),  # 0x669933,   6723891,
'orange':                ( (255, 165,   0), 214 ),  # 0xffa500,  16753920,
'orangered':             ( (255,  69,   0), 202 ),  # 0xff4500,  16729344,
'orchid':                ( (218, 112, 214), 170 ),  # 0xda70d6,  14315734,
'orchid2':               ( (153,  51, 153), 133 ),  # 0x993399,  10040217,
'orchidbright':          ( (255,  51, 255), 207 ),  # 0xff33ff,  16724991,
'palegoldenrod':         ( (238, 232, 170), 223 ),  # 0xeee8aa,  15657130,
'palegreen':             ( (152, 251, 152), 120 ),  # 0x98fb98,  10025880,
'paleturquoise':         ( (175, 238, 238), 159 ),  # 0xafeeee,  11529966,
'palevioletred':         ( (219, 112, 147), 168 ),  # 0xdb7093,  14381203,
'papayawhip':            ( (255, 239, 213), 230 ),  # 0xffefd5,  16773077,
'pastelpurple':          ( (204, 153, 255), 183 ),  # 0xcc99ff,  13408767,
'peachpink':             ( (255, 153, 255), 219 ),  # 0xff99ff,  16751103,
'peachpuff':             ( (255, 218, 185), 223 ),  # 0xffdab9,  16767673,
'peagreen':              ( (153, 204,  51), 149 ),  # 0x99cc33,  10079283,
'periwinkle':            ( (102, 102, 204), 104 ),  # 0x6666cc,   6710988,
'periwinklelight':       ( (153, 153, 255), 147 ),  # 0x9999ff,  10066431,
'peru':                  ( (205, 133,  63), 173 ),  # 0xcd853f,  13468991,
'pink':                  ( (255, 192, 203), 218 ),  # 0xffc0cb,  16761035,
'pinkpunch':             ( (255,   0, 153), 199 ),  # 0xff0099,  16711833,
'pistachio':             ( (204, 255, 102), 192 ),  # 0xccff66,  13434726,
'plum':                  ( (221, 160, 221), 182 ),  # 0xdda0dd,  14524637,
'plum2':                 ( (153,   0, 102), 126 ),  # 0x990066,  10027110,
'powderblue':            ( (176, 224, 230), 152 ),  # 0xb0e0e6,  11591910,
'powderblue2':           ( (102, 153, 255), 111 ),  # 0x6699ff,   6724095,
'purple':                ( (128,   0, 128),   5 ),  # 0x800080,   8388736,
'purple2':               ( (102,   0, 102),  90 ),  # 0x660066,   6684774,
'purplenight':           ( (102,   0, 153),  91 ),  # 0x660099,   6684825,
'rebeccapurple':         ( (102,  51, 153),  60 ),  # 0x663399,   6697881,
'rebeccapurple2':        ( (102,  51, 153),  97 ),  # 0x663399,   6697881,
'redorange':             ( (255,   0,  51), 197 ),  # 0xff0033,  16711731,
'rose':                  ( (204, 153, 153), 181 ),  # 0xcc9999,  13408665,
'rosybrown':             ( (188, 143, 143), 138 ),  # 0xbc8f8f,  12357519,
'royalblue':             ( ( 65, 105, 225),  62 ),  # 0x4169e1,   4286945,
'royalblue2':            ( (  0,  51, 204),  26 ),  # 0x33cc  ,     13260,
'saddlebrown':           ( (139,  69,  19),  94 ),  # 0x8b4513,   9127187,
'saddlebrown2':          ( (153,  51,   0), 130 ),  # 0x993300,  10040064,
'salmon':                ( (250, 128, 114), 209 ),  # 0xfa8072,  16416882,
'sand':                  ( (153, 153, 102), 144 ),  # 0x999966,  10066278,
'sandstone':             ( (204, 204, 153), 187 ),  # 0xcccc99,  13421721,
'sandybrown':            ( (244, 164,  96), 215 ),  # 0xf4a460,  16032864,
'scarlet':               ( (255,   0,   0), 196 ),  # 0xff0000,  16711680,
'seagreen':              ( ( 46, 139,  87),  29 ),  # 0x2e8b57,   3050327,
'seagreen2':             ( ( 51, 153, 102),  72 ),  # 0x339966,   3381606,
'seagreen3':             ( (  0, 153, 102),  36 ),  # 0x9966  ,     39270,
'seashell':              ( (255, 245, 238), 255 ),  # 0xfff5ee,  16774638,
'sienna':                ( (160,  82,  45), 130 ),  # 0xa0522d,  10506797,
'sienna2':               ( (153, 102,  51), 137 ),  # 0x996633,  10053171,
'silver':                ( (192, 192, 192),   7 ),  # 0xc0c0c0,  12632256,
'silver2':               ( (153, 153, 153), 145 ),  # 0x999999,  10066329,
'skyblue':               ( (135, 206, 235), 116 ),  # 0x87ceeb,   8900331,
'skyblue2':              ( (  0, 102, 204),  32 ),  # 0x66cc  ,     26316,
'skycloud':              ( (102, 153, 204), 110 ),  # 0x6699cc,   6724044,
'skysteel':              ( ( 51, 153, 204),  74 ),  # 0x3399cc,   3381708,
'skywhite':              ( (153, 204, 255), 153 ),  # 0x99ccff,  10079487,
'slateblue':             ( (106,  90, 205),  62 ),  # 0x6a5acd,   6970061,
'slateblue2':            ( ( 51, 102, 204),  68 ),  # 0x3366cc,   3368652,
'slategray':             ( (112, 128, 144),  66 ),  # 0x708090,   7372944,
'slategrey':             ( (112, 128, 144),  66 ),  # 0x708090,   7372944,
'snow':                  ( (255, 250, 250),  15 ),  # 0xfffafa,  16775930,
'softblue':              ( (153, 102, 255), 141 ),  # 0x9966ff,  10053375,
'springgreen':           ( (  0, 255, 127),  48 ),  # 0xff7f  ,     65407,
'springgreen2':          ( ( 51, 255, 102),  84 ),  # 0x33ff66,   3407718,
'springgreen3':          ( (  0, 204,  51),  41 ),  # 0xcc33  ,     52275,
'springmint':            ( (204, 255, 153), 193 ),  # 0xccff99,  13434777,
'steelblue':             ( ( 70, 130, 180),  67 ),  # 0x4682b4,   4620980,
'steelblue2':            ( (  0,  51, 153),  25 ),  # 0x3399  ,     13209,
'tan':                   ( (210, 180, 140), 180 ),  # 0xd2b48c,  13808780,
'teal':                  ( (  0, 128, 128),   6 ),  # 0x8080  ,     32896,
'teal2':                 ( (  0, 102, 153),  31 ),  # 0x6699  ,     26265,
'thistle':               ( (216, 191, 216), 182 ),  # 0xd8bfd8,  14204888,
'tomato':                ( (255,  99,  71), 203 ),  # 0xff6347,  16737095,
'turquoise':             ( ( 64, 224, 208),  80 ),  # 0x40e0d0,   4251856,
'turquoise2':            ( ( 51, 255, 204),  86 ),  # 0x33ffcc,   3407820,
'turquoise3':            ( (  0, 204, 153),  43 ),  # 0xcc99  ,     52377,
'ultramarine':           ( ( 51,   0, 255),  57 ),  # 0x3300ff,   3342591,
'violet':                ( (238, 130, 238), 213 ),  # 0xee82ee,  15631086,
'violet2':               ( (153,   0, 204), 128 ),  # 0x9900cc,  10027212,
'wheat':                 ( (245, 222, 179), 223 ),  # 0xf5deb3,  16113331,
'yellowgreen':           ( (154, 205,  50), 113 ),  # 0x9acd32,  10145074,
'yellowgreen2':          ( (153, 204,   0), 148 ),  # 0x99cc00,  10079232,
'yellowgreen3':          ( (102, 204,   0), 112 ),  # 0x66cc00,   6736896,
'yellowlime':            ( (153, 255,  51), 155 ),  # 0x99ff33,  10092339,

# Grey(Gray) Scale Values.
'gray0':    ( (  0,   0,   0),  16 ),   # 0x0     ,         0,
'grey0':    ( (  0,   0,   0),  16 ),   # 0x0     ,         0,
'gray3':    ( (  8,   8,   8), 232 ),   # 0x80808 ,    526344,
'grey3':    ( (  8,   8,   8), 232 ),   # 0x80808 ,    526344,
'gray7':    ( ( 18,  18,  18), 233 ),   # 0x121212,   1184274,
'grey7':    ( ( 18,  18,  18), 233 ),   # 0x121212,   1184274,
'gray11':   ( ( 28,  28,  28), 234 ),   # 0x1c1c1c,   1842204,
'grey11':   ( ( 28,  28,  28), 234 ),   # 0x1c1c1c,   1842204,
'gray15':   ( ( 38,  38,  38), 235 ),   # 0x262626,   2500134,
'grey15':   ( ( 38,  38,  38), 235 ),   # 0x262626,   2500134,
'gray19':   ( ( 48,  48,  48), 236 ),   # 0x303030,   3158064,
'grey19':   ( ( 48,  48,  48), 236 ),   # 0x303030,   3158064,
'gray23':   ( ( 58,  58,  58), 237 ),   # 0x3a3a3a,   3815994,
'grey23':   ( ( 58,  58,  58), 237 ),   # 0x3a3a3a,   3815994,
'gray27':   ( ( 68,  68,  68), 238 ),   # 0x444444,   4473924,
'grey27':   ( ( 68,  68,  68), 238 ),   # 0x444444,   4473924,
'gray30':   ( ( 78,  78,  78), 239 ),   # 0x4e4e4e,   5131854,
'grey30':   ( ( 78,  78,  78), 239 ),   # 0x4e4e4e,   5131854,
'gray35':   ( ( 88,  88,  88), 240 ),   # 0x585858,   5789784,
'grey35':   ( ( 88,  88,  88), 240 ),   # 0x585858,   5789784,
'gray39':   ( ( 98,  98,  98), 241 ),   # 0x626262,   6447714,
'grey39':   ( ( 98,  98,  98), 241 ),   # 0x626262,   6447714,
'gray42':   ( (108, 108, 108), 242 ),   # 0x6c6c6c,   7105644,
'grey42':   ( (108, 108, 108), 242 ),   # 0x6c6c6c,   7105644,
'gray46':   ( (118, 118, 118), 243 ),   # 0x767676,   7763574,
'grey46':   ( (118, 118, 118), 243 ),   # 0x767676,   7763574,
'gray50':   ( (128, 128, 128), 244 ),   # 0x808080,   8421504,
'grey50':   ( (128, 128, 128), 244 ),   # 0x808080,   8421504,
'gray54':   ( (138, 138, 138), 245 ),   # 0x8a8a8a,   9079434,
'grey54':   ( (138, 138, 138), 245 ),   # 0x8a8a8a,   9079434,
'gray58':   ( (148, 148, 148), 246 ),   # 0x949494,   9737364,
'grey58':   ( (148, 148, 148), 246 ),   # 0x949494,   9737364,
'gray62':   ( (158, 158, 158), 247 ),   # 0x9e9e9e,  10395294,
'grey62':   ( (158, 158, 158), 247 ),   # 0x9e9e9e,  10395294,
'gray66':   ( (168, 168, 168), 248 ),   # 0xa8a8a8,  11053224,
'grey66':   ( (168, 168, 168), 248 ),   # 0xa8a8a8,  11053224,
'gray70':   ( (178, 178, 178), 249 ),   # 0xb2b2b2,  11711154,
'grey70':   ( (178, 178, 178), 249 ),   # 0xb2b2b2,  11711154,
'gray74':   ( (188, 188, 188), 250 ),   # 0xbcbcbc,  12369084,
'grey74':   ( (188, 188, 188), 250 ),   # 0xbcbcbc,  12369084,
'gray78':   ( (198, 198, 198), 251 ),   # 0xc6c6c6,  13027014,
'grey78':   ( (198, 198, 198), 251 ),   # 0xc6c6c6,  13027014,
'gray82':   ( (208, 208, 208), 252 ),   # 0xd0d0d0,  13684944,
'grey82':   ( (208, 208, 208), 252 ),   # 0xd0d0d0,  13684944,
'gray85':   ( (218, 218, 218), 253 ),   # 0xdadada,  14342874,
'grey85':   ( (218, 218, 218), 253 ),   # 0xdadada,  14342874,
'gray89':   ( (228, 228, 228), 254 ),   # 0xe4e4e4,  15000804,
'grey89':   ( (228, 228, 228), 254 ),   # 0xe4e4e4,  15000804,
'gray93':   ( (238, 238, 238), 255 ),   # 0xeeeeee,  15658734,
'grey93':   ( (238, 238, 238), 255 ),   # 0xeeeeee,  15658734,
'gray100':  ( (255, 255, 255), 231 ),   # 0xffffff,  16777215,
'grey100':  ( (255, 255, 255), 231 ),   # 0xffffff,  16777215,
}


def name_to_rgb(color_name: str) -> Tuple[int, int, int]:
    """
    Get the RGB value for a given color name.
    Args:
        color_name (str): The name of the color to look up.
    Returns:
        RGB_Tuple ((int, int, int)): The RGB (Red, Green, Blue) tuple if the color exists; 
        otherwise, returns (255, 255, 255) (white).
    """
    try:
        return Color_Dict[color_name.lower()][0] # OLDER 
    except:
        if console_EnvType <= 2:
            raise ColorsValueError(
                error_value=color_name, 
                message=f"The Color_name: {PEACH}'{color_name}'{RESET} is not specified in colors dict"
            ).add_note(Note)
        return Color_Dict['white'][0]
        
    
def name_to_256(color_name: str) -> Ansi_Int: 
    """
    Get the ANSI 256-color code for a given color name.
    Args:
        color_name (str): The name of the color to look up.
    Returns:
        Ansi-256-Code (int): The ANSI 256 color code if the color exists; otherwise, returns 15 (white).
    """
    try:
        return Color_Dict[color_name.lower()][1]
    except:
        if console_EnvType <= 2:
            raise ColorsValueError(
                error_value=color_name, 
                message=f"The Color_name: {PEACH}'{color_name}'{RESET} is not specified in colors dict"
            ).add_note(Note)
        return Color_Dict['white'][1]

    
def name_to_16(name:str) -> Ansi_Int:
    """
    Get the ANSI 16-color code for a given color name.
    Args:
        color_name (str): The name of the color to look up.
    Returns:
        Ansi-16-Code (int): The ANSI 16 color code if the color exists; otherwise, returns 37 (white).
    """
    return Color_Dict.get(name.lower(), Color_Dict['white'])[1] 

Note = f''' Please check the available COLORS:
>>> from dvs_printf import get_colors_names
>>> get_colors_names(show_color_table = True)'''


# ===============================================================================================================
# |                                                (New Version)                                                |
# ===============================================================================================================


def get_colors_names(
    return_dict:      bool = True,
    show_color_table: bool = True,
    colorize_names:   bool = True ) -> List[str]:
    """
    Retrieves color data and optionally prints a dynamically formatted color reference 
    table to the console using styled, animated output.

    The structure and ANSI formatting of the printed table automatically adapt based 
    on the internal global `console_EnvType` to ensure compatibility 
    (e.g., full RGB, 256-color, or 16-color modes).

    Args:
        return_dict (bool, optional): If True, returns the internal color data 
            dictionary (color_name: ((R, G, B), ANSI_code)). If False, returns 
            a simple list of all color names (strings). Defaults to True.
        show_color_table (bool, optional): If True, the formatted color table is 
            printed to the console using the custom `__typing__` effect. 
            Defaults to True.
        colorize_names (bool, optional): If True and a table is shown, attempts to 
            colorize the color names within the table using their respective 
            ANSI codes, provided the current console environment supports 
            the complexity (`console_EnvType <= 3`). Defaults to True.

    Returns:
        Union[Dict[str, Tuple[Tuple[int, int, int], int]], List[str]]: 
            The color data, either as the dictionary of color objects or a list 
            of names, depending on the `return_dict` argument.

    Notes:
        This function has strict dependencies on constants and module for 
        its display functionality:
        - `console_EnvType`: Determines the table layout and ANSI code depth.
        - `Color_Dict`: The source dictionary containing all color data.
        - `B`, `I`, `R`: Required formatting constants (Bold, Italics, Reset).
        - `__printf__.modifyed` and `__printf__.__typing__`: Used for animated/styled 
          console output.
    """


    if show_color_table:

        if console_EnvType in (1,2):
            table_top = (  f'\n\n{B}{I}Color_Table{R}\n'
                            '╭──────────────────────┬─────────────────┬──────────╮\n'
                            '│                      │                 │          │\n'
                           f'│ {B}Name{R}                 │ {B}RGB-Value{R}       │ {B}ANSI-256{R} │\n'
                            '├──────────────────────┼─────────────────┼──────────┤')
            table_bottum =  '╰──────────────────────┴─────────────────┴──────────╯\n'

        else:
            table_top = (  f'\n\n{B}{I}16_Color_Table{R}\n'
                             '╭────────────────┬───────────────────────────────────────╮\n'
                            f'│                │                 {B}Anis{R}                  │\n'
                            f'│      {B}Name{R}      ├─────────────────┬──────────┬──────────┤\n'
                            f'│                │ {B}RGB-Value{R}       │{B}fourground{R}│{B}background{R}│\n'
                             '├────────────────┼─────────────────┼──────────┼──────────┤')
            table_bottum =   '╰────────────────┴─────────────────┴──────────┴──────────╯\n'

        if colorize_names and console_EnvType <= 3:

            if  console_EnvType == 1: 
                color_lines = (
                    (
                        f'\033[0m│ \033[38;2;{r};{g};{b}m{key:<21}  '
                        f'({r:3},{g:4},{b:4})   '
                        f'\033[38;5;{ansi}m{ansi:3}      \033[0m│\r\033[23C│\r\033[41C│\n'
                    ) for key, ((r, g, b), ansi) in Color_Dict.items()
                )

            elif console_EnvType == 2: 
                
                color_lines = (
                    (
                        f'\033[0m│ \033[38;5;{ansi}m{key:<21}  '
                        f'({r:3},{g:4},{b:4})   '
                        f'{ansi:3}      \033[0m│\r\033[23C│\r\033[41C│\n'
                    ) for key, ((r, g, b), ansi) in Color_Dict.items()
                )

            else: color_lines = ( # console_EnvType == 3: 
                    (
                        f'\033[0m│ \033[{ansi}m{key:<15}  '
                        f'({r:3},{g:4},{b:4})   '
                        f'{ansi}         \033[0m\033[{ansi+10}m{(ansi+9):<9}\033[0m'
                        '\r\033[17C│\r\033[35C│\r\033[46C│\r\033[57C|\n'
                    ) for key, ((r, g, b), ansi) in Color_Dict.items()
            )

        elif console_EnvType in (1,2):
            color_lines = (
                f'│ {key:<20} │ ({r:3},{g:4},{b:4}) │ {ansi:3}      │\n' 
                for key, ((r, g, b), ansi) in Color_Dict.items()
            )

        else: 
             color_lines = (
                f'│ {key:<14} │ ({r:3},{g:4},{b:4}) │ {ansi:3}      │ {(ansi+10):3}      │\n' 
                for key, ((r, g, b), ansi) in Color_Dict.items()
            )
        try:
            # from ..__printf__ import modifyed #, _typing, _async
            from .._printf_helper import modifyed
            from ..console import _write, _flush
            from time import sleep
            modifyed.parameters("center", .001, 0, True, False)

            print(table_top)
            # modifyed.speed = .02
            # modifyed.color = True
            # _async(color_lines)
            # _typing(color_lines)
            for line in color_lines:
                _write(line)
                _flush()
                sleep(.003)
            print(table_bottum)
        except Exception as E:
            raise E
            # print("Somthing Went Wrong!", E)

    return Color_Dict if return_dict else list(Color_Dict)



#|===========================================================|
#| IF We use HEX_RGB_INT inplace of RGB Tuple.               |
#| In Future, IF this module needs less memory footprint     |
#|___________________________________________________________|
#|                                                           |
#| def rgb_to_int(r, g, b):                                  |
#|     return (r << 16) + (g << 8) + b                       |
#|                                                           |
#| def int_to_rgb(i):                                        |
#|     return ((i >> 16) & 0xFF, (i >> 8) & 0xFF, i & 0xFF)  |
#|                                                           |
#|===========================================================|


# ===========================================================================
# |                        (WE MIGHT USE IN FUTURE)                         |
# ===========================================================================
#
# modifyed.speed = .05
# modifyed.color = True
# for key, ((r, g, b), ansi) in Color_Dict.items():
#     _typing(
#         f'\033[0m│ \033[38;2;{r};{g};{b}m{key:<21}  ',
#         f'({r:3},{g:4},{b:4})   ',
#         f'\033[38;5;{ansi}m{ansi:3}      \033[0m│\r\033[23C│\r\033[41C│'
#     ) 
#     sleep(.002)

# for key, ((r, g, b), ansi) in Color_Dict.items():
#     print(
#         f'\033[0m│ \033[38;5;{ansi}m{key:<21}  ' 
#         f'({r:3},{g:4},{b:4})   ' 
#         f'{ansi:3}{" "*6}\033[0m│\r\033[23C│\r\033[41C│'
#     ) 
# color_lines = (
#     f'│ {key:<14} | {ansi}{" "*8} | {(ansi+10):<10} │\n'
#     for key, ansi in Color_Dict.items()
# )

# return HEX_TO_RGB(Color_Dict[color_name.lower()][0]) # NEWER
# return HEX_TO_RGB(Color_Dict['white'][0]) # NEWER
# ===========================================================================
    
