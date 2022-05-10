from typing import Union
import random
import pygame
import math
from typing import List, Tuple
pygame.init()

# ? HYPER PARAM
SCREEN_SIZE = (800, 600)
GAME_SPEED = 10
DEBUG = 1
ANIMATE_SPEED = 5
DELTA_SPAWN_LIMIT = [300, 500] # [Min, Max]
# ? GLOBAL VARIABLE

screen = pygame.display.set_mode(SCREEN_SIZE)

class Object():
    T = 1
    def __init__(self, x, y, img, entry = 0, **kwargs) -> None:
        self.x = x
        self.y = y
        self.entry = entry
        if type(img) is not list:
            self.img:list[pygame.surface.Surface] = [img]
        else:
            self.img:list[pygame.surface.Surface] = img
        self.mask = pygame.mask.from_surface(self.img[0])
        self.__dict__.update(kwargs)
    def move(self):
        self.x -= GAME_SPEED
    def draw(self):
        if DEBUG:
            for point in self.get_points():
                pygame.draw.rect(screen, (255, 0, 0), (point[0], point[1], 5, 5))
        screen.blit(self.img[self.T//ANIMATE_SPEED % len(self.img)], (self.x, self.y))
        self.T += 1
    
    # # ? Helper func
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.img[0].get_width(), self.img[0].get_height())

    def get_top_left(self) -> Tuple[int, int]:
        return (self.x, self.y)
    def get_top_right(self) -> Tuple[int, int]:
        return (self.x + self.img[0].get_width(), self.y)
    def get_bottom_right(self) -> Tuple[int, int]:
        return (self.x + self.img[0].get_width(), self.y + self.img[0].get_height())
    def get_bottom_left(self) -> Tuple[int, int]:
        return (self.x, self.y + self.img[0].get_height())
    def get_points(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        return (self.get_top_left(), self.get_top_right(), self.get_bottom_right(), self.get_bottom_left())

class Ground():
    '''
        Handle All Ground Things Including doubling the ground
    '''
    img = pygame.image.load('../assets/ground.png')
    def __init__(self) -> None:
        self.y = SCREEN_SIZE[1]//2 - self.img.get_height()//2
        self.x1 = 0
        self.x2 = SCREEN_SIZE[0]
        
    def draw(self) -> None:
        screen.blit(self.img, (self.x1, self.y))
        screen.blit(self.img, (self.x2, self.y))
    def move(self) -> None:
        self.x1 -= GAME_SPEED
        self.x2 -= GAME_SPEED
        if self.x1+self.img.get_width() <= 0:
            self.x1 = SCREEN_SIZE[0]
        if self.x2+self.img.get_width() <= 0:
            self.x2 = SCREEN_SIZE[0]

class Dino(Object):
    GRAVITY = 0.9
    JUMP_FORCE = 10
    img = [pygame.image.load('../assets/dino1.png'), pygame.image.load('../assets/dino2.png')]
    img_norm = [pygame.image.load('../assets/dino1.png'), pygame.image.load('../assets/dino2.png')]
    img_down = [pygame.image.load('../assets/dinoDown1.png'), pygame.image.load('../assets/dinoDown2.png')]
    is_crawl = False
    y_norm = 310
    y_down = 330
    dead = pygame.image.load('../assets/dinoDead.png')
    def __init__(self, entry:int=0, **kwargs) -> None:
        self.velocity = 0
        self.x = 20
        self.y = self.y_norm
        super().__init__(self.x, self.y, self.img, entry, **kwargs)
    def move(self) -> None:
        if not self.is_crawl:
            self.y = min(self.y - self.velocity, self.y_norm)
        else:
            self.y = min(self.y - self.velocity, self.y_down)
        self.velocity = self.velocity-self.GRAVITY
    def jump(self) -> None:
        if self.y != self.y_norm:
            return
        self.velocity = self.JUMP_FORCE
    def crawl(self) -> None:
        if self.y != self.y_norm:
            return
        self.is_crawl = 1
        self.img = self.img_down
        self.y = self.y_down
    def normal(self) -> None:
        if self.y != self.y_down:
            return
        self.img = self.img_norm
        self.y = self.y_norm
        self.is_crawl = 0
    
class Cactus(Object):
    imgSmall = pygame.image.load('../assets/cactusSmall.png') # type 0
    imgBig = pygame.image.load('../assets/cactusBig.png') # type 1
    imgMany = pygame.image.load('../assets/cactusMany.png') # type 2
    img = [imgSmall, imgBig, imgMany]
    def __init__(self, type:int, entry:int=0, **kwargs) -> None:
        if type == 0:
            img = self.imgSmall
        elif type == 1:
            img = self.imgBig
        else:
            img = self.imgMany
        super().__init__(SCREEN_SIZE[0], 316, img, entry, **kwargs)

class Bird(Object):
    img = [pygame.image.load('../assets/bird1.png'), pygame.image.load('../assets/bird2.png')]
    def __init__(self, height:int = 0, entry:int=0, **kwargs) -> None:
        '''
            height = 0 dino has to Jump
            height = 1 dino has to crawl
            height = 2 dino cant jump
        '''
        if height == 0:
            y = 320
        if height == 1:
            y = 280
        else:
            y = 260
            
        super().__init__(SCREEN_SIZE[0], y, self.img, entry, **kwargs)
    
def isCollision(dino:Object, obj:Object) -> bool:
    val = dino.mask.overlap(obj.mask, (dino.x-obj.x, dino.y-obj.y))
    return val is not None

# ? HUMAN INTERFACE
def run():
    ground = Ground()
    dino = Dino()
    time = pygame.time.Clock()
    objects:List[Object] = [Cactus(0, entry=0)] # (object, entry time)
    next_spawn = random.randint(DELTA_SPAWN_LIMIT[0], DELTA_SPAWN_LIMIT[1])
    x = 0
    done = 0
    global T
    while True:
        # ? USER INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.normal()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('Jumping')
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    print('Crawling')
                    dino.crawl()
        screen.fill((255, 255, 255))
        ground.draw()
        dino.draw()
        for obj in objects:
            obj.draw()
            done |= isCollision(dino, obj)
        if done:
            break
        
        pygame.display.update()
        
        x += GAME_SPEED
        
        if objects and x-objects[-1].__dict__['entry'] >= next_spawn:
            rand = random.randint(0, 5) # cactus small, cactus big, cactus wide, bird low, bird high
            if rand <= 2:
                objects.append(Cactus(rand, entry=x))
            else:
                objects.append(Bird(rand-3, entry=x))
            next_spawn = random.randint(DELTA_SPAWN_LIMIT[0], DELTA_SPAWN_LIMIT[1])
        
        dino.move()
        for obj in objects:
            obj.move()
            if obj.get_top_right()[0] <= 0:
                objects.remove(obj)
        
        time.tick(30)

# ? MACHINE INTERFACE
class Environment:
    font = pygame.font.Font('freesansbold.ttf', 24)
    def __init__(self, debug_mode=False):
        self.objects:list[Object] = [Cactus(0, entry=0)]
        self.ground = Ground()
        self.x = 0
        # TODO FIX DEBUG MODE
        self.mode = debug_mode
        self.score = 0
        self.next_obj_spawn = 300
        self.time = pygame.time.Clock()

    def get_state(self, dino:Dino, return_int:bool = False) -> Union[list[float], Tuple[int]]:
        ret = [math.dist(dino.get_top_right(), self.objects[0].get_top_left()), math.dist(dino.get_bottom_right(), self.objects[0].get_bottom_left())]
        if return_int:
            return tuple([int(x) for x in ret])
        return ret

    def debug(self):
        if self.mode:
            print(self.score, end='\r')

    def play_step(self, dinos:list[Dino], act:list[int]) -> Tuple[list[Dino], float]:
        '''
            Return 
                Died dino list[Dino] (In order to support population simulation)
                Reward [int]
        '''
        if len(dinos) != len(act): raise IndexError('len(dinos) != len(act)')
        self.debug()
        died_dino = []
        reward = .1
        for inx, dino in enumerate(dinos):
            if act[inx] == 0:
                dino.normal()
            if act[inx] == 1:
                dino.normal()
                dino.jump()
            elif act[inx] == 2:
                dino.crawl()
            if self.isCollision(dino):
                reward = -1000
                died_dino.append(dino)
            dino.move()
        for obj in self.objects:
            # Reward Scheme for Q learning
            if obj.get_bottom_left()[1] < dinos[0].get_top_left()[1] and reward != -1000:
                reward = 100
            if obj.get_top_right()[0] < 0:
                self.objects.remove(obj)
            obj.move()
        if self.objects[-1].x-self.x < self.next_obj_spawn:
            rand = random.randint(0, 5)
            if rand <= 2:
                self.objects.append(Cactus(rand, entry=self.x))
            else:
                self.objects.append(Bird(rand-3, entry=self.x))
            self.next_obj_spawn = random.randint(DELTA_SPAWN_LIMIT[0], DELTA_SPAWN_LIMIT[1])
        self.ground.move()
        self.score += 1
        return died_dino, reward

    def isCollision(self, dino:Dino):
        return isCollision(dino, self.objects[0])

    def render(self, dinos:list[Dino]):
        screen.fill((255, 255, 255))
        self.ground.draw()
        for obj in self.objects:
            obj.draw()
        for dino in dinos:
            dino.draw()
        # TODO REQUIRE DEBUG MODE
        score = self.font.render(f'Score: {self.score}', True, (255, 0, 0))
        num_dino = self.font.render(f'Individuals: {len(dinos)}', True, (0, 0, 255))
        screen.blit(score, (10, 10))
        screen.blit(num_dino, (10, 40))
        pygame.display.update()
        self.time.tick(30)
    

if __name__ == '__main__':
    run()