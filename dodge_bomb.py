

import os
import sys
import random
import time
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


def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数。

    引数:
        screen (pg.Surface): 描画対象の画面（Surface）
    """
    # 半透明の黒い画面を作成
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    screen.blit(overlay, (0, 0))

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_kk_rect = cry_kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    cry_kk_rect2 = cry_kk_img2.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    screen.blit(cry_kk_img, cry_kk_rect)
    screen.blit(cry_kk_img2, cry_kk_rect2)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾のサイズ別Surfaceリストと加速度リストを生成する。

    戻り値:
        tuple[list[pg.Surface], list[int]]: 
            - 爆弾のサイズ別Surfaceリスト
            - 加速度リスト
    """
    bb_imgs = []  # 爆弾Surfaceリスト
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # サイズ変更対応
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 赤い円を描画
        bb_imgs.append(bb_img)
        
    return bb_imgs, bb_accs   


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す関数。

    引数:
        sum_mv (tuple[int, int]): こうかとんの移動量（x, y）

    戻り値:
        pg.Surface: 指定された移動量に対応する向きの画像Surface
    """
    # こうかとんの基本画像
    kk_img = pg.image.load("fig/3.png")  # こうかとんの元画像
    kk_img_invarted = pg.transform.flip(kk_img, True, False)
    kk_img_dict = {}

    # 移動方向に応じた画像を準備
    kk_img_dict[(0, 0)] = pg.transform.rotozoom(kk_img, 0, 0.9)  # 停止中
    kk_img_dict[(5, 0)] = pg.transform.rotozoom(kk_img, -90, 0.9)  # 右に移動
    kk_img_dict[(0, 5)] = pg.transform.rotozoom(kk_img, 0, 0.9)  # 下に移動
    kk_img_dict[(-5, 0)] = pg.transform.rotozoom(kk_img, 90, 0.9)  # 左に移動
    kk_img_dict[(0, -5)] = pg.transform.rotozoom(kk_img, 180, 0.9)  # 上に移動

    return kk_img_dict.get(tuple(sum_mv), kk_img_dict[(0, 0)])  # 移動量に応じた画像を返す


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bb_img = pg.Surface((20, 20), pg.SRCALPHA)  # 爆弾イメージ
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描画
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # ランダム配置

    # 爆弾の速度
    vx = 5
    vy = 5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        screen.blit(bg_img, [0, 0])

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_img = get_kk_img(sum_mv)
        kk_rct = kk_img.get_rect(center=kk_rct.center)
        
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

        bb_imgs, bb_accs = init_bb_imgs() 
        avx = vx * bb_accs[min(tmr // 500, 9)] 
        avy = vy * bb_accs[min(tmr // 500, 9)] 
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        Yoko, Tate = check_bound(bb_rct)
        if not Yoko:
            avx *= -1  # 横方向の反転
        if not Tate:
            avy *= -1  # 縦方向の反転

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