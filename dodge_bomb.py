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
    """
    画面内または画面外の判定を行う
    引数:
        rct (pg.Rect): 判定対象の矩形
    戻り値:
        (横方向, 縦方向)の真理値タプル
        (True: 画面内, False: 画面外)
    """
    Yoko, Tate = True, True
    if rct.left < 0 or rct.right > WIDTH:
        Yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
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
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return  # ゲームオーバー

        screen.blit(bg_img, [0, 0])

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外なら元に戻す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 爆弾の移動処理
        bb_rct.move_ip(vx, vy)
        Yoko, Tate = check_bound(bb_rct)
        if not Yoko:
            vx *= -1  # 横方向の反転
        if not Tate:
            vy *= -1  # 縦方向の反転

        # 描画
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