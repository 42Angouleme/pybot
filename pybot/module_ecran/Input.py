import pygame as pg

keys = {
"esc":pg.K_ESCAPE,
"space":pg.K_SPACE,
"!":pg.K_EXCLAIM,
'"':pg.K_QUOTEDBL,
"#":pg.K_HASH,
"$":pg.K_DOLLAR,
"&":pg.K_AMPERSAND,
"(":pg.K_LEFTPAREN,
")":pg.K_RIGHTPAREN,
"*":pg.K_ASTERISK,
"+":pg.K_PLUS,
",":pg.K_COMMA,
"-":pg.K_MINUS,
".":pg.K_PERIOD,
"/":pg.K_SLASH,
"0":pg.K_0,
"1":pg.K_1,
"2":pg.K_2,
"3":pg.K_3,
"4":pg.K_4,
"5":pg.K_5,
"6":pg.K_6,
"7":pg.K_7,
"8":pg.K_8,
"9":pg.K_9,
":":pg.K_COLON,
";":pg.K_SEMICOLON,
"<":pg.K_LESS,
"=":pg.K_EQUALS,
">":pg.K_GREATER,
"?":pg.K_QUESTION,
"@":pg.K_AT,
"[":pg.K_LEFTBRACKET,
"\\":pg.K_BACKSLASH,
"]":pg.K_RIGHTBRACKET,
"^":pg.K_CARET,
"_":pg.K_UNDERSCORE,
"`":pg.K_BACKQUOTE,
"a":pg.K_a,
"b":pg.K_b,
"c":pg.K_c,
"d":pg.K_d,
"e":pg.K_e,
"f":pg.K_f,
"g":pg.K_g,
"h":pg.K_h,
"i":pg.K_i,
"j":pg.K_j,
"k":pg.K_k,
"l":pg.K_l,
"m":pg.K_m,
"n":pg.K_n,
"o":pg.K_o,
"p":pg.K_p,
"q":pg.K_q,
"r":pg.K_r,
"s":pg.K_s,
"t":pg.K_t,
"u":pg.K_u,
"v":pg.K_v,
"w":pg.K_w,
"x":pg.K_x,
"y":pg.K_y,
"z":pg.K_z,
"del":pg.K_DELETE,
"0":pg.K_KP0,
"1":pg.K_KP1,
"2":pg.K_KP2,
"3":pg.K_KP3,
"4":pg.K_KP4,
"5":pg.K_KP5,
"6":pg.K_KP6,
"7":pg.K_KP7,
"8":pg.K_KP8,
"9":pg.K_KP9,
".":pg.K_KP_PERIOD,
"/":pg.K_KP_DIVIDE,
"*":pg.K_KP_MULTIPLY,
"-":pg.K_KP_MINUS,
"+":pg.K_KP_PLUS,
"=":pg.K_KP_EQUALS,
"F1":pg.K_F1,
"F2":pg.K_F2,
"F3":pg.K_F3,
"F4":pg.K_F4,
"F5":pg.K_F5,
"F6":pg.K_F6,
"F7":pg.K_F7,
"F8":pg.K_F8,
"F9":pg.K_F9,
"F10":pg.K_F10,
"F11":pg.K_F11,
"F12":pg.K_F12,
"F13":pg.K_F13,
"F14":pg.K_F14,
"F15":pg.K_F15
}

class Input:
    def __init__(self):
        pass

    @staticmethod
    def check(events, robot):
        result = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                robot.eteindre_ecran()
            if event.type == pg.KEYDOWN:
                for e in events:
                    k = keys[e[0]]
                    if event.key == k:
                        result.append(e[1])
            # self.ui.check_event(event) # boutons
        return result

    #     self.keyboardState = pg.key.get_pressed()
    #     self.mouseState = pg.mouse.get_pressed()
    #     self.mousePos = pg.mouse.get_pos()

    #     if self.keyboardState[pg.K_ESCAPE]:
    #         self.quit()