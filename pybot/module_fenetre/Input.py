import pygame as pg

keys = {
"echap":pg.K_ESCAPE,
"espace":pg.K_SPACE,
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
        if (robot.isWriting == False):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    robot.fermer_fenetre()
                if event.type == pg.KEYDOWN:
                    for e in events:
                        k = keys[e[0]]
                        if event.key == k:
                            result.append(e[1])
        return result

    @staticmethod
    def get_user_entry(robot, text_area) :
        user_texte = ""
        if (robot.isWriting) :
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    robot.fermer_fenetre()
                    return "stop"
                if event.type == pg.KEYDOWN:
                    user_texte += event.unicode
                if event.type == pg.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        text_area.check_is_outside(event.pos) 
        if (user_texte == "") :
            return None
        else :
            return user_texte
