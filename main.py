import pygame
import os
from random import randint

MAIN_WIDTH = 10  # кол-во клеток по горизонтали
MAIN_HEIGHT = 10  # кол-во клеток по вертикали

d = {}  # словарь, в котором хранатся все данные по клеткам(открыта или нет, мина или нет, кол-во мин вокруг)
b_width = 35 # ширина клетки
b_height = 35  # высота клетки
mines_kol = int(MAIN_WIDTH*MAIN_HEIGHT*0.15)  # общее количество мин

pygame.init()
size = width, height = MAIN_WIDTH*b_width, MAIN_HEIGHT*b_height  # вычисление размеров окна
screen = pygame.display.set_mode(size)


def load_image(name, colorkey = None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        #image = image.convert_alpha()
        #if colorkey is not None:
        #    if colorkey is -1:
        #        colorkey = image.get_at((0, 0))
        #    image.set_colorkey(colorkey)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


bomb_image = load_image("bomb.png")
flag_image = load_image("flag.png")

all_sprites = pygame.sprite.Group()
flag_sprites = pygame.sprite.Group()


class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        flags_k = 0
    for i in range(MAIN_WIDTH):
        for j in range(MAIN_HEIGHT):
            if d[(i * b_width, j * b_height)][0] == 2 and d[(i * b_width, j * b_height)][1] == 1:
                flags_k += 1
            if flags_k == mines_kol:
                all_sprites.draw(screen)
                return True
    return False


# проверка на взрыв
def check_bomb():
    for i in range(MAIN_WIDTH):
        for j in range(MAIN_HEIGHT):
            if d[(i * b_width, j * b_height)][0] == 1 and d[(i * b_width, j * b_height)][1] == 1:
                all_sprites.draw(screen)
                return True
    return False


# основная программа
def main():
    # двойной цикл для создания всех клеток и добавление их в GUI
    for i in range(MAIN_WIDTH):
        for j in range(MAIN_HEIGHT):
            gui.add_element(Button((i*b_width, j*b_height, b_width, b_height), ""))
            d[(i*b_width, j*b_height)] = [0, 0]

    # генерация мин и расстановка их на поле
    for _ in range(mines_kol):
        i = randint(0, MAIN_WIDTH - 1)
        j = randint(0, MAIN_HEIGHT - 1)
        while d[(i*b_width, j*b_height)][1] == 1:
            i = randint(0, MAIN_WIDTH - 1)
            j = randint(0, MAIN_HEIGHT - 1)
        d[(i * b_width, j * b_height)][1] = 1

    for i in range(MAIN_WIDTH):
        for j in range(MAIN_HEIGHT):
            if d[(i*b_width, j*b_height)][1] == 1:
                bomb = pygame.sprite.Sprite(all_sprites)
                bomb.image = bomb_image
                bomb.rect = (i * b_width + 3, j * b_height + 3, b_width, b_height)

    # вычисление для каждой клетки (кроме клеткок с минами) количества мин по соседству
    for i in range(MAIN_WIDTH):
        for j in range(MAIN_HEIGHT):
            mines_k = 0
            x = i*b_width
            y = j*b_height
            if d[(x, y)][1] == 0:
                if ((i-1)*b_width, (j-1)*b_height) in d:
                    mines_k += d[((i-1)*b_width, (j-1)*b_height)][1]
                if ((i)*b_width, (j-1)*b_height) in d:
                    mines_k += d[((i)*b_width, (j-1)*b_height)][1]
                if ((i+1)*b_width, (j-1)*b_height) in d:
                    mines_k += d[((i+1)*b_width, (j-1)*b_height)][1]
                if ((i-1)*b_width, (j)*b_height) in d:
                    mines_k += d[((i-1)*b_width, (j)*b_height)][1]
                if ((i+1)*b_width, (j)*b_height) in d:
                    mines_k += d[((i+1)*b_width, (j)*b_height)][1]
                if ((i-1)*b_width, (j+1)*b_height) in d:
                    mines_k += d[((i-1)*b_width, (j+1)*b_height)][1]
                if ((i)*b_width, (j+1)*b_height) in d:
                    mines_k += d[((i)*b_width, (j+1)*b_height)][1]
                if ((i+1)*b_width, (j+1)*b_height) in d:
                    mines_k += d[((i+1)*b_width, (j+1)*b_height)][1]
                if mines_k == 0:
                    d[(x, y)].append('')
                else:
                    d[(x, y)].append(mines_k)
            else:
                d[(x, y)].append('*')

    # основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            gui.get_event(event)

        gui.render(screen)
        gui.update()
        if check_win():
            print('~~~ WIN ~~~')
            pygame.display.set_caption("~~~ WIN ~~~")
            #running = False
        if check_bomb():
            print('~~~ GAME OVER ~~~')
            pygame.display.set_caption("~~~ GAME OVER ~~~")
            #running = False
        flag_sprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    gui = GUI()
    main()