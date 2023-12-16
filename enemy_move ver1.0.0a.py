import pygame, sys, random
from pygame import *

"""
敵は基本クラス定義とし、固定変数として敵を設定する。
変数に応じた画像・設定・BGM・画像を適用する。
敵の移動は範囲内ランダムとする。なお、敵の強さに応じて移動範囲は狭まる。
"""

"""
    データ備考：
    １．画像が保存されている場所
    ２．画像切り取り開始地点（x軸、y軸）
    ３．画像サイズ（x軸、y軸）
    ４．画像の数（横列、縦列）
    ５．紺珠伝型フレーム真偽
    ６．ボスHP倍率
    ７．BGM配置path
    ８．移動倍率
"""
enemy_paths = {
    "Dai_1":["chara\\1面大妖精\\DaiyouseiGFWSprite.png", (0, 0), (80, 90), (3, 2), False, 1, "BGM/ルーネイトエルフ.ogg"],
    "Eter_2":["chara\\2面エタニティラルバ\\EternityHSiFS.png", (0, 0), (80, 102), (6, 3), True, 1.2, "BGM/真夏の妖精の夢.ogg"],
    "Lily_3":["chara\\3面リリーホワイト\\LilyWhiteHSiFS.png", (0, 0), (64, 65), (4, 1), False, 1.3, "BGM/桜色の海を泳いで.ogg"],
    "Sunny_4":["chara\\4面三月精\\SunnyStarGFWSprite.png", (0, 0), (96, 96), (4, 2), False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Star_4":["chara\\4面三月精\\SunnyStarGFWSprite.png", (0, 288), (96, 96), (4, 2), False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Luna_4":["chara\\4面三月精\\LunaGFWSprite.png", (0, 0), (96, 96), (4, 2), False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Clown_5":["chara\\5面クラウンピース\\ClownpieceLoLK.png", (0, 0), (64, 97), (8, 1), True, 1.7, "BGM/星条旗のピエロ.ogg"],
    "Marisa_6":["chara\\6面魔理沙\\MarisaGFWSprite.png", (0, 0), (80, 113), (4, 2), False, 1.7, "BGM/恋色マスタースパーク.ogg"]
}
screen_size = (800, 450)

def main():
    global screen, enemy_paths, tmr, screen_size
    pygame.init()
    pygame.display.set_caption("enemy_move.py")
    screen = pygame.display.set_mode(screen_size)
    frame_clock = pygame.time.Clock()
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    tmr = 0
    shown_chara = ""
    #Dai = Enemy("Dai_1")
    Eter = Enemy("Eter_2")
    #Lily = Enemy("Lily_3")
    #Sunny = Enemy("Sunny_4")
    #Star = Enemy("Star_4")
    #Luna = Enemy("Luna_4")
    #Clown = Enemy("Clown_5")
    #Marisa = Enemy("Marisa_6")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if tmr == 100000000:
            tmr = 0
        else:
            tmr += 1
        key_pushed_list = pygame.key.get_pressed()
        screen.fill(WHITE)
        #Dai.built()
        Eter.built()
        #Lily.built()
        #Sunny.built()
        #Star.built()
        #Luna.built()
        #Clown.built()
        #Marisa.built()

        pygame.display.update()
        frame_clock.tick(60)

class Enemy:
    def __init__(self, enemy_index):
        self.x, self.y, self.original_x, self.original_y = 320, 200, 0, 0 #キャラの現在の表示座標＋キャラがランダムに移動する際に移動する直前の座標を保存する変数
        self.target_x, self.target_y, self.target_reached = 0, 0, True #移動先の座標＋到達カウンター
        self.random_range_x, self.random_range_y = [0, 0], [0, 0] #ランダムに移動するための範囲を決める変数（現在不使用）
        self.random_default_range_x = 500 #キャラが移動する際のx,y座標のランダム幅。
        self.random_default_range_y = 10
        self.move_t_set = 60 #横軸ｔの設定。実際のゲームでは各キャラが独自のｔの設定を持っている。その準備としてここに置いておく
        self.start_tmr = 0
        self.enemy_style = 0 #キャラの状態（フレーム処理用変数）に対応する変数
        self.enemy_hp = 1000 * enemy_paths[enemy_index][5]
        self.loaded_enemy = enemy_index
        self.flame_img_list, self.type_flame_img = [], []
        self.flame_limit = enemy_paths[enemy_index][3][0]
        self.whole_img = pygame.image.load(enemy_paths[enemy_index][0])
        for img_y in range(enemy_paths[enemy_index][3][1]):
            for img_x in range(enemy_paths[enemy_index][3][0]):
                #元の画像をカットする左上の座標の位置を設定する変数。
                cut_x = img_x * enemy_paths[enemy_index][2][0] + enemy_paths[enemy_index][1][0]
                cut_y = img_y * enemy_paths[enemy_index][2][1] + enemy_paths[enemy_index][1][1]
                self.surface_img = pygame.Surface(enemy_paths[enemy_index][2], pygame.SRCALPHA) # pygame.SRCALPHAを入れることでpngの透明データを保持可能
                self.surface_img.blit(self.whole_img, (0, 0), (cut_x, cut_y,  enemy_paths[enemy_index][2][0], enemy_paths[enemy_index][2][1]))
                self.surface_img = self.surface_img.convert_alpha()
                self.type_flame_img.append(self.surface_img)
            self.flame_img_list.append(self.type_flame_img)
            self.type_flame_img = []
    
    def built(self):
        """
        ここで、60tickでランダムに移動先を決める。移動先の処理で以下のようにする。
        １．先にランダムで座標を出す。次にその座標が画面外に出ないかを全て検知する方法
        ２．先にはみ出る座標を決め、その範囲内でランダムに数字を抽出する方法
        """
        if self.target_reached and tmr % 120 == 0:
            if self.x > 0 and self.x <= self.random_default_range_x:#画像の左上のx座標が0以上５０以下であるならば、その座標にマイナスをかけて範囲を指定する。
                #上の条件において、self.random_default_range_xがかなり大きいとき、場合によっては外へ飛ばされる可能性がある。
                self.random_range_x = [-self.x, self.random_default_range_x]
            elif screen_size[0] - (self.x + enemy_paths[self.loaded_enemy][2][0]) <= self.random_default_range_x:
                #画像の右上x座標とウィンドウ右端の差が50以下である場合、その差を範囲とする。
                self.random_range_x = [-self.random_default_range_x, screen_size[0] - self.x - enemy_paths[self.loaded_enemy][2][0]]
            else:
                self.random_range_x = [-self.random_default_range_x, self.random_default_range_x]
            
            if self.y > 0 and self.y <= self.random_default_range_y:#画像の左上のy座標が50以下であるならば、その座標にマイナスをかけて範囲を指定する。
                self.random_range_y = [-self.y, self.random_default_range_y]
            elif screen_size[1] - (self.y + enemy_paths[self.loaded_enemy][2][1]) <= self.random_default_range_y:#画像の下y座標とウィンドウ下端の差が50以下である場合、その差を範囲とする。
                #self.random_range_y[1] = screen_size[1] - self.y - enemy_paths[self.loaded_enemy][2][1]
                self.random_range_y = [-self.random_default_range_y, screen_size[1] - self.y - enemy_paths[self.loaded_enemy][2][1]]
            else:
                self.random_range_y = [-self.random_default_range_y, self.random_default_range_y]
            self.target_x, self.target_y = random.randint(self.random_range_x[0], self.random_range_x[1]), random.randint(self.random_range_y[0], self.random_range_y[1])
            self.target_reached = False
            self.start_tmr = tmr
            self.original_x, self.original_y = self.x, self.y
        #if not self.target_reached and (tmr - self.start_tmr) < abs(self.target_x) and (tmr - self.start_tmr) < abs(self.target_y):
        if not self.target_reached and (tmr - self.start_tmr) < self.move_t_set:
            self.x = self.original_x + self.target_x * (1 - (1 - (tmr - self.start_tmr + 1)/self.move_t_set) ** 2)
            #self.x = self.original_x + self.target_x * (1 - (1 - (tmr - self.start_tmr + 1)/(abs(self.target_x))) ** 2)
            self.y = self.original_y + self.target_y * (1 - (1 - (tmr - self.start_tmr + 1)/self.move_t_set) ** 2)
            #self.y = self.original_y + self.target_y * (1 - (1 - (tmr - self.start_tmr + 1)/(abs(self.target_y))) ** 2)
            if enemy_paths[self.loaded_enemy][3][1] > 1:
                self.enemy_style = 1
        elif (tmr - self.start_tmr) >= self.move_t_set:
            self.target_reached = True
            self.enemy_style = 0
        
        #以下はフレーム表示処理
        if not enemy_paths[self.loaded_enemy][4]:
            #ここの処理は非紺珠伝型のフレーム処理
            screen.blit(self.flame_img_list[self.enemy_style][(tmr // 8) % self.flame_limit], [self.x, self.y])
        if enemy_paths[self.loaded_enemy][4]:
            #ここの処理は紺珠伝型のフレーム処理
            loaded_c = enemy_paths[self.loaded_enemy][3][0] - 1
            flame_lolk = abs((((tmr // 9) + loaded_c) % loaded_c * 2) - loaded_c) #ここの式はchatgptより引用（フレーム遅延はここで行うべし）
            screen.blit(self.flame_img_list[self.enemy_style][flame_lolk], [self.x, self.y])
    
    def play(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(enemy_paths[self.loaded_enemy][6])
        pygame.mixer.music.play(-1)

if __name__ == "__main__":
    main()
