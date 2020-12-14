from pygame.locals import *
import pygame
import time
import duckylights
import random
from duckylights import device_path

import logging.config
import os.path

# define top level module logger
# https://docs.python.org/3/howto/logging.html#configuring-logging
logger = logging.getLogger(__name__)



def random_color():
    return hex(random.randint(0, 256**3 - 1))[2:].rjust(6, '0')

  
 
class Player:
    # define top level module logger
    logger = logging.getLogger(__name__)
    x = 1
    y = 1
    speed = 1

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def moveRight(self):
        if(self.x==11):
            self.x=0
        else:
            self.x = self.x + self.speed
        self.logger.info(str(self.x)+" "+str(self.y))

    def moveLeft(self):
        if(self.x==0):
            self.x=11
        else:
            self.x = self.x - self.speed
        self.logger.info(str(self.x)+" "+str(self.y))

    def moveUp(self):
        if(self.y==0):
            self.y=4
        else:
            self.y = self.y - self.speed
        self.logger.info(str(self.x)+" "+str(self.y))

    def moveDown(self):
        if(self.y==4):
            self.y=0
        else:
            self.y = self.y + self.speed
        self.logger.info(str(self.x)+" "+str(self.y))

class App:

    windowWidth = 800
    windowHeight = 600
    player = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player() 

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        #self._image_surf = pygame.image.load("pygame.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass
    
    def on_render(self):
        #self._display_surf.fill((0,0,0))
        #self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        #with duckylights.keyboard() as dev, dev.programming() as ducky:
        #  colors = [random_color() for i in range(6 * 22)]
        count = min(10, 8)
        colors = ['000000'] * (6 * 22)
        #colors[count*6+1] = 'ff0000'
        #colors[14*6+3]='00ff00'
        #colors[8*6+4]='0000ff' 
        colors[self.player.x*6+self.player.y]='ffffff'
        ducky.custom_mode(colors)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            
            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
            time.sleep (50.0 / 1000.0);
        self.on_cleanup()
 
if __name__ == "__main__" :
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'default_handler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': os.path.join('logs', 'application.log'),
                'encoding': 'utf8'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default_handler','console'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_config)
    with duckylights.keyboard(path=device_path(vendor=0x04d9, product=0x0356)) as dev, dev.programming() as ducky:
        theApp = App()
        theApp.on_execute()
    