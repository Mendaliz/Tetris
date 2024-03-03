import random
import pygame

all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
mains = pygame.sprite.Group()
next_blocks = pygame.sprite.Group()
score = pygame.sprite.Group()
web = pygame.sprite.Group()

scorec = 0
colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (200, 0, 200), (0, 200, 200)]

types = {'S': [['ooooo',
                'ooooo',
                'ooxxo',
                'oxxoo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'ooxxo',
                'oooxo',
                'ooooo']],
         'Z': [['ooooo',
                'ooooo',
                'oxxoo',
                'ooxxo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'oxxoo',
                'oxooo',
                'ooooo']],
         'J': [['ooooo',
                'oxooo',
                'oxxxo',
                'ooooo',
                'ooooo'],
               ['ooooo',
                'ooxxo',
                'ooxoo',
                'ooxoo',
                'ooooo'],
               ['ooooo',
                'ooooo',
                'oxxxo',
                'oooxo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'ooxoo',
                'oxxoo',
                'ooooo']],
         'L': [['ooooo',
                'oooxo',
                'oxxxo',
                'ooooo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'ooxoo',
                'ooxxo',
                'ooooo'],
               ['ooooo',
                'ooooo',
                'oxxxo',
                'oxooo',
                'ooooo'],
               ['ooooo',
                'oxxoo',
                'ooxoo',
                'ooxoo',
                'ooooo']],
         'I': [['ooooo',
                'ooooo',
                'oxxxx',
                'ooooo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'ooxoo',
                'ooxoo',
                'ooxoo'],
               ['ooooo',
                'ooooo',
                'xxxxo',
                'ooooo',
                'ooooo'],
               ['ooxoo',
                'ooxoo',
                'ooxoo',
                'ooxoo',
                'ooooo']],
         'O': [['ooooo',
                'ooooo',
                'oxxoo',
                'oxxoo',
                'ooooo']],
         'T': [['ooooo',
                'ooxoo',
                'oxxxo',
                'ooooo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'ooxxo',
                'ooxoo',
                'ooooo'],
               ['ooooo',
                'ooooo',
                'oxxxo',
                'ooxoo',
                'ooooo'],
               ['ooooo',
                'ooxoo',
                'oxxoo',
                'ooxoo',
                'ooooo']]}


class Block(pygame.sprite.Sprite):

    def __init__(self, pos, color, *group):
        super().__init__(*group)
        self.image = pygame.Surface((35, 35))
        self.image.fill(pygame.Color(color), [0, 0, 35, 35])
        self.rect = self.image.get_rect()
        self.rect.x = 20 + pos[0] * 35
        self.rect.y = 30 + pos[1] * 35

        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.active = 1

    def update(self, *args):
        self.rect.x = 20 + self.x * 35
        self.rect.y = 30 + self.y * 35


class Main(pygame.sprite.Sprite):

    def __init__(self, field, typik, color, *group):
        super().__init__(*group)
        self.field = field
        self.x = 5
        self.y = 1
        self.color = color
        self.going = 1
        self.flipping = 0
        self.is_touched = 0
        self.game_over = 0
        self.mode = 0

        self.type = typik
        self.shape = types[self.type][self.mode]
        self.add_in_field()

    def update(self, *args):
        if args[0].key == pygame.K_UP:
            self.flip()
        if args[0].key == pygame.K_LEFT:
            self.move_left()
        if args[0].key == pygame.K_RIGHT:
            self.move_right()

    def del_in_field(self):
        for y in range(5):
            for x in range(5):
                if self.shape[y][x] == "x":
                    self.field[self.y + (y - 2)][self.x + (x - 2)].kill()
                    self.field[self.y + (y - 2)][self.x + (x - 2)] = 0

    def add_in_field(self):
        for y in range(5):
            for x in range(5):
                if self.shape[y][x] == "x":
                    self.field[self.y + (y - 2)][self.x + (x - 2)] = Block([self.x + (x - 2), self.y + (y - 2)],
                                                                           self.color, all_sprites, blocks)

    def touched(self):
        for y in range(5):
            for x in range(5):
                if self.shape[y][x] == "x":
                    self.field[self.y + (y - 2)][self.x + (x - 2)].active = 0
        self.is_touched = 1
        self.check_completed()
        if self.field[1][5] != 0:
            self.game_over = 1

    def check_completed(self):
        global scorec
        y = self.y + (self.y < 19) + (self.y < 18)
        while y != 1:
            if 0 not in self.field[y]:
                self.delete_st(y)
                scorec += 1
                y += 1
            y -= 1

    def delete_st(self, start_y):
        for block in self.field[start_y]:
            block.kill()
        self.field[start_y] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(start_y, 0, -1):
            self.field[y], self.field[y - 1] = self.field[y - 1], self.field[y]
            for block in self.field[y]:
                if block != 0:
                    block.y += 1

    def flip(self):
        if self.check_flip():
            self.del_in_field()
            self.mode = (self.mode + 1) % len(types[self.type])
            self.shape = types[self.type][self.mode]
            self.add_in_field()

    def check_flip(self):
        shape = types[self.type][(self.mode + 1) % len(types[self.type])]
        for y in range(5):
            for x in range(5):
                if shape[y][x] == "x":
                    if self.y + (y - 2) > 19 or self.y + (y - 2) < 0 or self.x + (x - 2) > 9 or self.x + (x - 2) < 0:
                        return False
                    if self.field[self.y + (y - 2)][self.x + (x - 2)] != 0:
                        if self.field[self.y + (y - 2)][self.x + (x - 2)].active == 0:
                            return False
        return True

    def down(self):
        if self.check_down():
            self.del_in_field()
            self.y += 1
            self.add_in_field()
        else:
            self.touched()

    def check_down(self):
        try:
            for y in range(5):
                for x in range(5):
                    if self.shape[y][x] == "x":
                        if self.field[self.y + y - 1][self.x + x - 2] != 0:
                            if self.field[self.y + y - 1][self.x + x - 2].active == 0:
                                return False
            return True
        except Exception:
            return False

    def move_right(self):
        if self.check_right():
            self.del_in_field()
            self.x += 1
            self.add_in_field()

    def check_right(self):
        for y in range(5):
            if "x" in self.shape[y]:
                x = 4 - self.shape[y][::-1].index("x")
                if self.x + x - 1 > 9:
                    return False
                if self.field[self.y + (y - 2)][self.x + x - 1] != 0:
                    if self.field[self.y + (y - 2)][self.x + x - 1].active == 0:
                        return False
        return True

    def move_left(self):
        if self.check_left():
            self.del_in_field()
            self.x -= 1
            self.add_in_field()

    def check_left(self):
        for y in range(5):
            if "x" in self.shape[y]:
                x = self.shape[y].index("x")
                if self.x + x - 3 < 0:
                    return False
                if self.field[self.y + (y - 2)][self.x + x - 3] != 0:
                    if self.field[self.y + (y - 2)][self.x + x - 3].active == 0:
                        return False
        return True


class NextBlock(pygame.sprite.Sprite):

    def __init__(self, next, color, *group):
        super().__init__(*group)
        self.image = pygame.Surface((175, 175))
        self.image.fill(pygame.Color("black"), [0, 0, 175, 175])
        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 170

        self.next = next
        self.color = color
        self.blocks = []
        for y in range(5):
            for x in range(5):
                if types[next][0][y][x] == "x":
                    self.blocks += [Block([x, y], color, next_blocks)]
                    self.blocks[-1].rect.x = 420 + x * 35
                    self.blocks[-1].rect.y = 170 + y * 35

    def update(self):
        pass


class Web(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((352, 702))
        for y in range(0, 701, 35):
            pygame.draw.line(self.image, (50, 50, 50), (0, y), (350, y), width=3)
        for x in range(0, 351, 35):
            pygame.draw.line(self.image, (50, 50, 50), (x, 0), (x, 700), width=3)

        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 30

    def update(self):
        pass


class Score(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.update()

        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 580
        self.score = scorec

    def update(self):
        self.image = pygame.Surface((200, 70))
        pygame.draw.rect(self.image, (50, 50, 50), pygame.Rect(2, 2, 196, 66), width=2)

        font = pygame.font.Font(pygame.font.match_font('arial'), 60)
        text_surface = font.render("0" * (7 - len(str(scorec))) + str(scorec), True, (70, 70, 70))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (100, 0)
        self.image.blit(text_surface, text_rect)


class Tetris:

    def __init__(self):
        self.web = Web(all_sprites, web)
        self.score = Score(all_sprites, score)
        self.field = self.new_field()
        self.type = list(types.keys())[random.randint(0, 5)]
        self.color = colors[random.randint(0, 5)]
        self.figure = Main(self.field, "L", self.color, mains)
        self.next_type = NextBlock(self.type, self.color, all_sprites)

    def new_figure(self):
        self.figure.kill()
        for block in next_blocks:
            block.kill()
        self.figure = Main(self.field, self.next_type.next, self.color, mains)
        self.type = list(types.keys())[random.randint(0, 5)]
        self.color = colors[random.randint(0, 5)]
        self.next_type = NextBlock(self.type, self.color)

    def new_field(self):
        return [[0 for _ in range(10)] for __ in range(20)]


class GameOver:

    def __init__(self, screen):
        self.screen = screen
        screen.fill(pygame.Color("black"))

        font = pygame.font.Font(pygame.font.match_font('arial'), 100)
        text_surface = font.render('Game Over', True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 300)
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(pygame.font.match_font('arial'), 50)
        text_surface = font.render('Your score:', True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 420)
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(pygame.font.match_font('arial'), 50)
        text_surface = font.render(str(scorec), True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 480)
        screen.blit(text_surface, text_rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

    def update(self, *args):
        pass


class StartGame:

    def __init__(self, screen):
        self.screen = screen
        start_buttons = pygame.sprite.Group()
        screen.fill(pygame.Color("black"))

        font = pygame.font.Font(pygame.font.match_font('arial'), 50)
        text_surface = font.render('Press any button to start.', True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 400)
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(pygame.font.match_font('arial'), 50)
        text_surface = font.render('To Pause press esc.', True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 470)
        screen.blit(text_surface, text_rect)

        self.startb = StartButton(start_buttons)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False
            start_buttons.update()
            start_buttons.draw(screen)
            pygame.display.flip()

    def update(self, *args):
        pass


class StartButton(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((540, 200))
        pygame.draw.rect(self.image, (100, 100, 0), pygame.Rect(6, 6, 534, 194), width=6)

        font = pygame.font.Font(pygame.font.match_font('arial'), 130)
        text_surface = font.render("Start", True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (270, 20)
        self.image.blit(text_surface, text_rect)

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 150
        self.score = scorec

    def update(self):
        pass


class PauseGame:

    def __init__(self, screen):
        self.screen = screen
        screen.fill(pygame.Color("black"))

        font = pygame.font.Font(pygame.font.match_font('arial'), 50)
        text_surface = font.render('Press any button to continue.', True, (100, 100, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 400)
        screen.blit(text_surface, text_rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False
            pygame.display.flip()

    def update(self, *args):
        pass


def main():
    pygame.init()
    size = width, height = (640, 800)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")

    StartGame(screen)

    game = Tetris()

    screen.fill(pygame.Color("black"))

    clock = pygame.time.Clock()
    fps = 60
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                    mains.update(event)
                if event.key == pygame.K_ESCAPE:
                    PauseGame(screen)
        screen.fill(pygame.Color("black"))

        all_sprites.update()
        all_sprites.draw(screen)
        next_blocks.draw(screen)
        pygame.display.flip()
        game.figure.down()
        if game.figure.is_touched:
            if game.figure.game_over:
                GameOver(screen)
                running = False
            else:
                game.new_figure()
        clock.tick(fps / 10)


if __name__ == "__main__":
    main()
