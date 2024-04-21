import pygame, sys, random
import math as maths
from pygame import *
import numpy as np

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
    "Dai_1":["chara\\1面大妖精\\DaiyouseiGFWSprite.png", [0, 0], [80, 90], [3, 2], False, 1, "BGM/ルーネイトエルフ.ogg"],
    "Eter_2":["chara\\2面エタニティラルバ\\EternityHSiFS.png", [0, 0], [80, 102], [6, 3], False, 1.2, "BGM/真夏の妖精の夢.ogg"],
    "Lily_3":["chara\\3面リリーホワイト\\LilyWhiteHSiFS.png", [0, 0], [64, 65], [4, 1], False, 1.3, "BGM/桜色の海を泳いで.ogg"],
    "Sunny_4":["chara\\4面三月精\\SunnyStarGFWSprite.png", [0, 0], [96, 96], [4, 2], False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Star_4":["chara\\4面三月精\\SunnyStarGFWSprite.png", [0, 288], [96, 96], [4, 2], False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Luna_4":["chara\\4面三月精\\LunaGFWSprite.png", [0, 0], [96, 96], [4, 2], False, 1.4, "BGM/いたずらに命をかけて.ogg"],
    "Clown_5":["chara\\5面クラウンピース\\ClownpieceLoLK.png", [0, 0], [64, 97], [8, 1], True, 1.7, "BGM/星条旗のピエロ.ogg"],
    "Marisa_6":["chara\\6面魔理沙\\MarisaGFWSprite.png", [0, 0], [80, 113], [4, 2], False, 1.7, "BGM/恋色マスタースパーク.ogg"]
}
screen_size = (800, 450)

def main():
    global screen, enemy_paths, tmr, screen_size, keys, key_space
    global bullet_positions, bullet_speed, ram_bullets, bullet
    global BLACK, WHITE, GREEN, RED
    pygame.init()
    pygame.display.set_caption("enemy_move.py")
    screen = pygame.display.set_mode(screen_size)
    frame_clock = pygame.time.Clock()
    BLACK, WHITE, GREEN, RED = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0)
    move_lock = False
    key_space = False
    player_bullet_limit = 100
    tmr = 0
    shown_chara = ""
    Dai = Enemy("Dai_1")
    Eter = Enemy("Eter_2")
    Lily = Enemy("Lily_3")
    Sunny = Enemy("Sunny_4")
    Star = Enemy("Star_4")
    Luna = Enemy("Luna_4")
    Clown = Enemy("Clown_5")
    Marisa = Enemy("Marisa_6")
    enemies_list = [Dai, Eter, Lily, Sunny, Star, Luna, Clown, Marisa]
    Tirno = Player("chara\\自機チルノ\\Cirno.png")
    bullet_positions = np.zeros((2, 100)) #　ここは自機玉の座標保存用リスト 0はx軸、1はy軸
    bullet_speed = np.zeros((2, 100)) # ここは自機玉の速度ベクトルを表したところ。なお、次元（単位）は[pixel/tick]。
    ram_bullets = np.full(100, False) #ここは自機玉の稼働フラグ
    bullet_class_list = np.full(100, None).tolist()
    bullet_speed[1] -= 20
    split_bullet()
    #print(Lily.current_hp)
    #Lily.play()
    #damage_sound = pygame.mixer.Sound("C:\\Users\\blueg\\Desktop\\ideal_game\\se\\se_damage00.wav")
    #damage_sound.set_volume(0.3)
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if tmr == 100000000:
            tmr = 0
        else:
            tmr += 1
        Tirno.chara_turn = 0 #０は無移動　１は右移動　２は左移動
        if keys[K_SPACE] and (len(np.where(ram_bullets==True)[0]) != player_bullet_limit):
            """
            この条件分岐について説明：
            スペースキーを押されたときに自機玉が稼働している数を計算し、それらが上限値もしくは下限値に達しているかを比較し、
            それらに達しているならばTrueを出力するのでnotで結果を反転している。
            また、上限値は設定により変更可能。（player_bullet_limitから変更可）
            """
            register_index = np.where(ram_bullets==False)[0].min()
            bullet_class_list[register_index] = Bullet(register_index, Tirno.x, Tirno.y)
        screen.fill(GREEN)
        #Dai.built()
        #Eter.built()
        if Lily.current_hp > 0:
            Lily.built()
        else:
            Lily.rect = Rect(0, 0, 0, 0)
        #Sunny.built()
        #Star.built()
        #Luna.built()
        #Clown.built()
        #Marisa.built()
        ###ここで自機玉の移動処理を行う。

        bullet_positions = bullet_positions + bullet_speed
        for ram_index in np.where(ram_bullets)[0]:
            bullet_class_list[ram_index].update()
        frame_count = int(tmr // 5) % 8
        if Tirno.chara_turn != 0 and (move_lock or frame_count == 7):
            frame_count = 7
            move_lock = True
        elif Tirno.chara_turn == 0:
            move_lock = False
        Tirno.key_movement()
        Tirno.built(frame_count)
        for enemy_check in enemies_list:
            if np.any(ram_bullets):#1つでも稼働している自機玉が存在した場合、当たり判定処理を実行する。
                for bullet_index in np.where(ram_bullets)[0]:
                    if pygame.sprite.collide_rect(enemy_check, bullet_class_list[bullet_index]) and enemy_check.current_hp > 0:
                        enemy_check.current_hp -= 1
                        #damage_sound.play()
                    elif enemy_check.current_hp <= 0:
                        print("done, hp: {}".format(enemy_check.current_hp))
        pygame.display.update()
        frame_clock.tick(60)

def split_bullet():
    global bullet_image_list
    split_point_x = [60, 35, 15, 0]
    split_point = [(176, (20, 59)), (113, (20, 59)), (52, (17, 59)), (0, (17, 53))]#1stは画像切り取りy軸位置、2ndは切り取り横幅、3rdは切り取り縦幅
    image = pygame.image.load("chara\\自機チルノ\\CirnoBullet.png")
    bullet_image_list, image_type = [], []
    for row in split_point_x:
        for size in split_point:
            surface = pygame.Surface(size[1], pygame.SRCALPHA)#pygame.SRCALPHA
            surface.blit(image, (0, 0), (row, size[0], size[1][0], size[1][1]))
            surface = surface.convert_alpha()
            image_type.append(surface)
        bullet_image_list.append(image_type)
        image_type = []
    bullet_image_list[2].append(bullet_image_list[3][0])
    

class Enemy(pygame.sprite.Sprite):
    """
    ここは敵本体のクラス定義である。
    初期化処理として各座標、カウンター、HP、移動距離設定、画像等を登録する。
    その際に設定リストからデータを読みだして各ステータスを設定する。詳細はこのコード上部に記載。
    画像分割はクラス定義の頻度が低いことから内部処理で問題ないが、メンテナンス性を重視するならば自機玉処理と同じ場所に置くと良い。
    敵移動については設定した範囲でランダムに移動するようにしてあるが、境界に近い場合はその境界までを事前に移動範囲としている。
    また、移動の際に敵の移動画像を同時に表示している。2024年1月29日現在、再現には成功しているが、完璧ではないため、改善が必要。
    更に紺珠伝以降のフレーム処理が複雑化している。クラウンピースの部分が最適化できていない。
    """
    def __init__(self, enemy_index):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.original_x, self.original_y = 320, 200, 0, 0 #キャラの現在の表示座標＋キャラがランダムに移動する際に移動する直前の座標を保存する変数
        self.rect = Rect(self.x, self.y, enemy_paths[enemy_index][2][0], enemy_paths[enemy_index][2][1])
        self.target_x, self.target_y, self.target_reached = 0, 0, True #移動先の座標＋到達カウンター
        self.random_range_x, self.random_range_y = [0, 0], [0, 0] #ランダムに移動するための範囲を決める変数（現在不使用）
        self.random_default_range_x = 100 #キャラが移動する際のx,y座標のランダム幅。
        self.random_default_range_y = 10
        self.move_t_set = 60 #横軸ｔの設定。実際のゲームでは各キャラが独自のｔの設定を持っている。その準備としてここに置いておく
        self.start_tmr = 0
        self.move_T = 1*60 #tick
        self.enemy_style = 0 #キャラの状態（フレーム処理用変数）に対応する変数
        self.flame_lock = False
        self.enemy_hp = 1000 * enemy_paths[enemy_index][5]
        self.current_hp = self.enemy_hp
        self.hp_bar_setting = 30
        self.loaded_enemy = enemy_index
        self.flame_img_list, self.type_flame_img = [], []
        self.flame_limit = enemy_paths[enemy_index][3][0]
        self.whole_img = pygame.image.load(enemy_paths[enemy_index][0])
        #self.radius = max(enemy_paths[self.loaded_enemy][2])
        for img_y in range(enemy_paths[enemy_index][3][1] + 1):
                for img_x in range(enemy_paths[enemy_index][3][0]):
                    #元の画像をカットする左上の座標の位置を設定する変数。
                    if img_y != 2:
                        cut_x = img_x * enemy_paths[enemy_index][2][0] + enemy_paths[enemy_index][1][0]
                        cut_y = img_y * enemy_paths[enemy_index][2][1] + enemy_paths[enemy_index][1][1]
                        self.surface_img = pygame.Surface(enemy_paths[enemy_index][2], pygame.SRCALPHA) # pygame.SRCALPHAを入れることでpngの透明データを保持可能
                        self.surface_img.blit(self.whole_img, (0, 0), (cut_x, cut_y,  enemy_paths[enemy_index][2][0], enemy_paths[enemy_index][2][1]))
                        self.surface_img = self.surface_img.convert_alpha()
                        self.type_flame_img.append(self.surface_img)
                    else:
                        self.type_flame_img.append(pygame.transform.flip(self.flame_img_list[1][img_x], True, False))
                self.flame_img_list.append(self.type_flame_img)
                self.type_flame_img = []
    
    def built(self):
        """
        ここで、60tickでランダムに移動先を決める。移動先の処理で以下のようにする。
        １．先にランダムで座標を出す。次にその座標が画面外に出ないかを全て検知する方法
        ２．先にはみ出る座標を決め、その範囲内でランダムに数字を抽出する方法
        """
        if self.target_reached and tmr % self.move_T == 0:
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
            self.flame_either_side = 1 if self.target_x > 0 else 2
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
            self.flame_lock = False
            self.enemy_style = 0

        #以下はフレーム表示処理
        if not enemy_paths[self.loaded_enemy][4]:#ここの処理は非紺珠伝型のフレーム処理
            if self.target_reached or enemy_paths[self.loaded_enemy][3][1] == 1:
                screen.blit(self.flame_img_list[0][(tmr // 8) % self.flame_limit], [self.x, self.y])
            elif not self.target_reached and enemy_paths[self.loaded_enemy][3][1] > 1:
                if ((tmr // 8) % self.flame_limit) != self.flame_limit - 1 and not self.flame_lock:# and not self.flame_lock:
                    screen.blit(self.flame_img_list[self.flame_either_side][(tmr // 8) % self.flame_limit], [self.x, self.y])
                elif (tmr // 8) % self.flame_limit == self.flame_limit - 1 or self.flame_lock:
                    screen.blit(self.flame_img_list[self.flame_either_side][self.flame_limit - 1], [self.x, self.y])
                    self.flame_lock = True
        if enemy_paths[self.loaded_enemy][4]:#ここの処理は紺珠伝型のフレーム処理
            loaded_c = enemy_paths[self.loaded_enemy][3][0] - 1
            flame_lolk = abs((((tmr // 9) + loaded_c) % loaded_c * 2) - loaded_c) #ここの式はchatgptより引用（フレーム遅延はここで行うべし）
            screen.blit(self.flame_img_list[self.enemy_style][flame_lolk], [self.x, self.y])
        
        self.rect = Rect(self.x, self.y, enemy_paths[self.loaded_enemy][2][0], enemy_paths[self.loaded_enemy][2][1])

        #以下は敵のHP表示
        self.radius = max(enemy_paths[self.loaded_enemy][2])
        self.center_point = [self.x + enemy_paths[self.loaded_enemy][2][0]/2, self.y + enemy_paths[self.loaded_enemy][2][1]/2]
        self.radius_back = self.radius + 2
        pygame.draw.arc(screen, RED, [self.center_point[0] - self.radius_back, self.center_point[1] - self.radius_back, 2*self.radius_back, 2*self.radius_back], maths.radians(90), maths.radians(90+360*1), 7)
        pygame.draw.arc(screen, WHITE, [self.center_point[0] - self.radius, self.center_point[1] - self.radius, 2*self.radius, 2*self.radius], maths.radians(90), maths.radians(90+360*(self.current_hp/self.enemy_hp)), 3)
        
    def play(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(enemy_paths[self.loaded_enemy][6])
        pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.chara_turn, self.count_point = 0, 0, 0, 0
        self.speed = 3
        self.sp_size = (32, 39)
        self.rect = Rect(self.x, self.y, self.sp_size[0], self.sp_size[1])
        self.start_points = [6, 53, 101]
        self.movement_img_list, self.type_move_img = [], []
        for img_y in self.start_points:
            for img_x in range(0, self.sp_size[0] * 9, self.sp_size[0]):
                self.surface_img = pygame.Surface(self.sp_size, pygame.SRCALPHA)
                self.surface_img.blit(pygame.image.load(image_path), (0, 0), (img_x, img_y, self.sp_size[0], self.sp_size[1]))
                self.surface_img = self.surface_img.convert_alpha()
                self.type_move_img.append(self.surface_img)
            self.movement_img_list.append(self.type_move_img)
            self.type_move_img = []
            self.count_point += 1
    
    def built(self, frame_count):
        self.rect = Rect(self.x, self.y, self.sp_size[0], self.sp_size[1])
        screen.blit(self.movement_img_list[self.chara_turn][frame_count], [self.x, self.y])
    
    def key_movement(self):
        if keys[K_a] and self.x >= 0: #左移動
            self.chara_turn = 1
            self.x -= self.speed
        elif keys[K_d] and self.x <= 800 - 32:
            self.chara_turn = 2
            self.x += self.speed
        if keys[K_w] and self.y >= 0:
            self.y -= self.speed
        elif keys[K_s] and self.y <= 450 - 38:
            self.y += self.speed
        
        

class Bullet(pygame.sprite.Sprite):
    """
    画像分割について：

    チルノの弾は縦59pixel,横20pixel（一部サイズ違いのため、多少調整が必要）
    画像分割の処理は画像の右下から上方向に切り取り、だんだんと左に移動するように設計。
    

    動作について：

    numpy.ndarrayで定義した座標リスト、速度ベクトルをもとに1tick当たりの処理を行う。（加速度ベクトルの変数は未実装、設定する速度の次元は[pixel/tick]ピクセル毎tickとする。）
    class定義の際に使用されていない部分、メモリ番号の最小値を選択し、番号をクラス内に登録する
    spaceキーを押されたときに空いているメモリ最小値を選択し、その場所にndarray型として保存し、クラスの座標データは別の場所に保存する。
    このクラスは主に画像データや当たり判定を定義するために使用されている。
    定義毎に画像を分割する際にリソースを食って動作を重くさせる可能性があるので、プログラム起動時に別途画像を分割・保存し、クラス定義の際に読み込みする。
    """
    def __init__(self, index, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.moving = False
        self.index = index
        self.rect = Rect(x, y, 20, 59)
        self.image_list = bullet_image_list
        bullet_positions[0][self.index] = x
        bullet_positions[1][self.index] = y
        ram_bullets[self.index] = True
        self.moving = True
    def update(self):
        self.x = bullet_positions[0][self.index]
        self.y = bullet_positions[1][self.index]
        if self.y < 0 - 59:
            ram_bullets[self.index] = False
            self.kill()
            #スプライト削除した後はクラスをリストから削除する方法もあるが、今のうちはしないでおく
        self.rect = Rect(self.x, self.y, 20, 59)
        screen.blit(self.image_list[0][0], [self.x, self.y])

if __name__ == "__main__":
    main()
