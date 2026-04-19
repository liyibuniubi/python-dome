import os

os.environ["SDL_IME_SHOW_UI"] = "0"

import pygame
import random
import sys
import math

pygame.init()

# ---------- 屏幕与颜色 ----------
WIDTH, HEIGHT = 480, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打飞机大战")
pygame.key.stop_text_input()
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 80)
YELLOW = (255, 220, 50)
CYAN = (0, 220, 255)
DARK_BLUE = (10, 15, 44)
STAR_COLOR = (180, 200, 255)


# ---------- 绘制函数 ----------
def draw_player(surf, cx, cy):
    """绘制玩家战机"""
    pts = [
        (cx, cy - 22),
        (cx - 6, cy - 10),
        (cx - 18, cy + 8),
        (cx - 22, cy + 14),
        (cx - 8, cy + 10),
        (cx - 6, cy + 18),
        (cx + 6, cy + 18),
        (cx + 8, cy + 10),
        (cx + 22, cy + 14),
        (cx + 18, cy + 8),
        (cx + 6, cy - 10),
    ]
    pygame.draw.polygon(surf, CYAN, pts)
    pygame.draw.polygon(surf, WHITE, pts, 1)
    pygame.draw.circle(surf, WHITE, (cx, cy), 4)


def draw_enemy(surf, cx, cy, size, hp_ratio):
    """绘制敌机"""
    half = size // 2
    pts = [
        (cx, cy + half),
        (cx - half, cy),
        (cx - half + 4, cy - half + 2),
        (cx, cy - half + 6),
        (cx + half - 4, cy - half + 2),
        (cx + half, cy),
    ]
    color = RED if hp_ratio > 0.5 else YELLOW
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, WHITE, pts, 1)
    bar_w = size
    bar_h = 3
    bx = cx - bar_w // 2
    by = cy - half - 8
    pygame.draw.rect(surf, (80, 80, 80), (bx, by, bar_w, bar_h))
    pygame.draw.rect(surf, GREEN, (bx, by, int(bar_w * hp_ratio), bar_h))


def draw_bullet(surf, cx, cy):
    pygame.draw.rect(surf, YELLOW, (cx - 2, cy - 6, 4, 12))


def draw_enemy_bullet(surf, cx, cy):
    pygame.draw.circle(surf, RED, (int(cx), int(cy)), 4)


def draw_explosion(surf, cx, cy, progress):
    """简单粒子爆炸效果"""
    max_r = 30
    r = int(max_r * progress)
    alpha = max(0, 255 - int(255 * progress))
    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 200, 50, alpha), (r, r), r)
    pygame.draw.circle(s, (255, 100, 30, alpha // 2), (r, r), r // 2)
    surf.blit(s, (cx - r, cy - r))


# ---------- 星空背景 ----------
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.5, 2.0)) for _ in range(120)]


def update_and_draw_stars(surf):
    for i, (x, y, speed) in enumerate(stars):
        y += speed
        if y > HEIGHT:
            y = 0
            x = random.randint(0, WIDTH)
        stars[i] = (x, y, speed)
        brightness = int(100 + speed * 70)
        c = min(brightness, 255)
        pygame.draw.circle(surf, (c, c, c), (int(x), int(y)), 1)


# ---------- 游戏对象类 ----------
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = 6
        self.shoot_delay = 8
        self.shoot_timer = 0
        self.lives = 3
        self.invincible = 0

    def update(self, pressed):
        if pressed.get(pygame.K_LEFT) or pressed.get(pygame.K_a):
            self.x = max(22, self.x - self.speed)
        if pressed.get(pygame.K_RIGHT) or pressed.get(pygame.K_d):
            self.x = min(WIDTH - 22, self.x + self.speed)
        if pressed.get(pygame.K_UP) or pressed.get(pygame.K_w):
            self.y = max(22, self.y - self.speed)
        if pressed.get(pygame.K_DOWN) or pressed.get(pygame.K_s):
            self.y = min(HEIGHT - 22, self.y + self.speed)
        if self.invincible > 0:
            self.invincible -= 1
        self.shoot_timer = max(0, self.shoot_timer - 1)

    def shoot(self):
        if self.shoot_timer == 0:
            self.shoot_timer = self.shoot_delay
            return [Bullet(self.x, self.y - 22)]
        return []

    def draw(self, surf):
        if self.invincible > 0 and (self.invincible // 4) % 2 == 0:
            return
        draw_player(surf, self.x, self.y)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.alive = True

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.alive = False

    def draw(self, surf):
        draw_bullet(surf, self.x, self.y)


class EnemyBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.alive = True

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.y > HEIGHT + 10 or self.x < -10 or self.x > WIDTH + 10:
            self.alive = False

    def draw(self, surf):
        draw_enemy_bullet(surf, self.x, self.y)


class Enemy:
    def __init__(self, x, y, kind="small"):
        self.x = x
        self.y = y
        self.kind = kind
        if kind == "small":
            self.size = 28
            self.max_hp = 1
            self.speed = 2.5
            self.score = 100
        elif kind == "medium":
            self.size = 40
            self.max_hp = 4
            self.speed = 1.5
            self.score = 300
            self.shoot_timer = random.randint(30, 90)
        else:
            self.size = 56
            self.max_hp = 12
            self.speed = 1.0
            self.score = 800
            self.shoot_timer = random.randint(20, 60)
        self.hp = self.max_hp
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT + 40:
            self.alive = False
        if hasattr(self, "shoot_timer"):
            self.shoot_timer -= 1

    def can_shoot(self):
        if not hasattr(self, "shoot_timer"):
            return False
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 150)
            return True
        return False

    def get_bullets(self, px, py):
        """朝玩家方向发射子弹"""
        dx = px - self.x
        dy = py - self.y
        dist = math.hypot(dx, dy) or 1
        spd = 3.5
        return [EnemyBullet(self.x, self.y, dx / dist * spd, dy / dist * spd)]

    def draw(self, surf):
        draw_enemy(surf, int(self.x), int(self.y), self.size, self.hp / self.max_hp)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.duration = 25

    @property
    def done(self):
        return self.timer >= self.duration

    def update(self):
        self.timer += 1

    def draw(self, surf):
        draw_explosion(surf, self.x, self.y, self.timer / self.duration)


# ---------- HUD ----------
def _get_cn_font(size):
    """尝试加载中文字体，失败则回退默认字体"""
    import os
    candidates = [
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Fonts", "msyh.ttc"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Fonts", "simhei.ttf"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Fonts", "simsun.ttc"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return pygame.font.Font(path, size)
    return pygame.font.SysFont("arial", size)


font = _get_cn_font(22)
font_big = _get_cn_font(48)
font_mid = _get_cn_font(30)


def draw_hud(surf, score, lives, high_score):
    txt = font.render(f"分数: {score}", True, WHITE)
    surf.blit(txt, (10, 10))
    htxt = font.render(f"最高: {high_score}", True, YELLOW)
    surf.blit(htxt, (WIDTH - htxt.get_width() - 10, 10))
    for i in range(lives):
        draw_player(surf, 30 + i * 36, HEIGHT - 30)


# ---------- 生成敌机波次 ----------
def spawn_enemy(frame, score):
    enemies = []
    if frame % 30 == 0:
        enemies.append(Enemy(random.randint(30, WIDTH - 30), -30, "small"))
    if frame % 90 == 0 and score >= 500:
        enemies.append(Enemy(random.randint(40, WIDTH - 40), -40, "medium"))
    if frame % 200 == 0 and score >= 2000:
        enemies.append(Enemy(random.randint(50, WIDTH - 50), -50, "big"))
    return enemies


# ---------- 碰撞检测 ----------
def collide(ax, ay, ar, bx, by, br):
    return math.hypot(ax - bx, ay - by) < ar + br


# ---------- 主游戏 ----------
def main():
    high_score = 0

    while True:
        player = Player()
        bullets = []
        enemy_bullets = []
        enemies = []
        explosions = []
        score = 0
        frame = 0
        game_over = False
        paused = False
        pressed = {}

        while True:
            clock.tick(FPS)

            restart = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pressed[event.key] = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        paused = not paused
                    if game_over and event.key == pygame.K_r:
                        restart = True
                if event.type == pygame.KEYUP:
                    pressed[event.key] = False

            if restart:
                break

            if game_over:
                screen.fill(DARK_BLUE)
                update_and_draw_stars(screen)
                over_txt = font_big.render("游戏结束", True, RED)
                screen.blit(over_txt, (WIDTH // 2 - over_txt.get_width() // 2, HEIGHT // 2 - 60))
                sc_txt = font_mid.render(f"得分: {score}", True, WHITE)
                screen.blit(sc_txt, (WIDTH // 2 - sc_txt.get_width() // 2, HEIGHT // 2 + 10))
                hint = font.render("按 R 重新开始", True, YELLOW)
                screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))
                draw_hud(screen, score, 0, high_score)
                pygame.display.flip()
                continue

            if paused:
                ptxt = font_big.render("暂停", True, WHITE)
                screen.blit(ptxt, (WIDTH // 2 - ptxt.get_width() // 2, HEIGHT // 2 - 24))
                pygame.display.flip()
                continue

            frame += 1
            player.update(pressed)

            if pressed.get(pygame.K_SPACE) or pressed.get(pygame.K_j):
                bullets.extend(player.shoot())

            for b in bullets:
                b.update()
            bullets = [b for b in bullets if b.alive]

            for eb in enemy_bullets:
                eb.update()
            enemy_bullets = [eb for eb in enemy_bullets if eb.alive]

            enemies.extend(spawn_enemy(frame, score))
            for e in enemies:
                e.update()
                if e.can_shoot():
                    enemy_bullets.extend(e.get_bullets(player.x, player.y))

            for b in bullets:
                for e in enemies:
                    if e.alive and b.alive and collide(b.x, b.y, 4, e.x, e.y, e.size // 2):
                        b.alive = False
                        e.hp -= 1
                        if e.hp <= 0:
                            e.alive = False
                            score += e.score
                            explosions.append(Explosion(e.x, e.y))

            if player.invincible == 0:
                for e in enemies:
                    if e.alive and collide(player.x, player.y, 16, e.x, e.y, e.size // 2):
                        e.alive = False
                        explosions.append(Explosion(e.x, e.y))
                        player.lives -= 1
                        player.invincible = 90
                        if player.lives <= 0:
                            explosions.append(Explosion(player.x, player.y))
                            high_score = max(high_score, score)
                            game_over = True

                for eb in enemy_bullets:
                    if eb.alive and collide(player.x, player.y, 14, eb.x, eb.y, 4):
                        eb.alive = False
                        player.lives -= 1
                        player.invincible = 90
                        if player.lives <= 0:
                            explosions.append(Explosion(player.x, player.y))
                            high_score = max(high_score, score)
                            game_over = True

            enemies = [e for e in enemies if e.alive]
            bullets = [b for b in bullets if b.alive]
            enemy_bullets = [eb for eb in enemy_bullets if eb.alive]

            for ex in explosions:
                ex.update()
            explosions = [ex for ex in explosions if not ex.done]

            # -- 绘制 --
            screen.fill(DARK_BLUE)
            update_and_draw_stars(screen)

            for b in bullets:
                b.draw(screen)
            for eb in enemy_bullets:
                eb.draw(screen)
            for e in enemies:
                e.draw(screen)
            for ex in explosions:
                ex.draw(screen)


            if not game_over:
                player.draw(screen)

            draw_hud(screen, score, player.lives, high_score)
            pygame.display.flip()


if __name__ == "__main__":
    main()