import pygame
from animaciones import get_animaciones_asteroide


class Asteroide(pygame.sprite.Sprite):
    def __init__(self,center: tuple,speed_asteroide:float):
        super().__init__() #llamar al constructor 
        #siempre un sprite tiene que tener una image, y un self.rect
        #y tenemos que redefinir un evento update
        self.animaciones = get_animaciones_asteroide()
        self.indice = 0
        self.timer_animaciones = 0
        self.image = self.animaciones[self.indice]
           
        self.rect = self.image.get_rect() #guarda el rect de la imagen
        self.rect.midbottom = center 
        
        self.velocidad_y = speed_asteroide

    def update(self):
        self.rect.y += self.velocidad_y
        
        self.timer_animaciones += 1 
        if self.indice >= 9:
            self.indice = 0
        elif self.timer_animaciones == 7:
            self.indice += 1
            self.timer_animaciones = 0
        
        self.image = self.animaciones[self.indice]
        
    
        
     
    



