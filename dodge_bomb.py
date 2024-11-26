import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    Yoko, Tate=True, True
    if rct.left <0 or WIDTH < rct.right: 
        Yoko = False
   
    if rct.top <0 or HEIGHT < rct.bottom: 
        Tate = False
        return Yoko, Tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bb_img = pg.Surface((20, 20), pg.SRCALPHA) #爆弾イメージ
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描画
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # ランダム配置
    # 爆弾の速度
    vx=5
    vy=5
    clock = pg.time.Clock()
    tmr = 0


    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        #if kk_rct.colliderect(bb_rct):
         #   print("ゲームオーバー")
          #  return #げーむオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        
        kk_rct.move_ip(sum_mv)
     
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bb_rct.move_ip(vx, vy)  # 爆弾動く
        Yoko, Tate = check_bound(bb_rct)
        if not Yoko:  # 横にはみ出てる
            vx *= -1
        if not Tate:  # 縦にはみ出てる
            vy *= -1

        bb_rct.move_ip(vx, vy) # 爆弾の移動
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
