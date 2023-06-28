import pygame
from laser import Laser
from config import WIDTH,HEIGHT
from animaciones import get_animaciones_disparo

class Nave(pygame.sprite.Sprite):
    def __init__(self, animaciones:str,midBottom: tuple):
        super().__init__() #llamar al constructor 
        #siempre un sprite tiene que tener una image, y un self.fact
        #y tenemos que redefinir un evento update
        self.animacion = animaciones
        self.indice = 2
        self.image = self.animacion[self.indice]
        # self.image = pygame.transform.scale(self.image,(size))

        self.rect = self.image.get_rect() #guarda el rect de la imagen
        self.rect.midbottom = midBottom 

        self.velocidad_x = 0
        self.velocidad_y = 0
        
        self.tiempo_antirrebote = 0
        self.tiempo_maximo = 100

    def update(self):
       
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        #para cuando va a la izquierda
        if self.velocidad_x == -5.5: 
            if self.indice <= 2 and self.indice > 0:
                self.indice = 1
                self.indice -= 1 
                
                    
        #para cuando esta quieto
        if self.velocidad_x == 0:  
            self.indice = 2 
          
        #para cuando va a la derecha
        if self.velocidad_x > 0:
            if self.indice >= 2 and self.indice < 4:
                self.indice = 3
                self.indice += 1
                   
        
        #izquieda y derecha            
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        
        #izquierda inferior e izquierda superior / Derecha inferior y Derecha superior
        if self.rect.left <= 0 and self.rect.bottom >= HEIGHT:
            self.rect.left = 0
            self.rect.bottom = HEIGHT
        elif self.rect.right >= WIDTH and self.rect.bottom >= HEIGHT :
            self.rect.right = WIDTH
            self.rect.bottom = HEIGHT
        if self.rect.left <= 0 and self.rect.bottom <= 0:
            self.rect.left = 0
            self.rect.bottom = 0
        elif self.rect.right >= WIDTH and self.rect.bottom <= 0 :
            self.rect.right = WIDTH
            self.rect.bottom = 0
        
        elif self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom =  HEIGHT
            
        
        self.image = self.animacion[self.indice]

        
    def disparar(self,sonido,speed,sprites,lasers):
        laser = Laser(get_animaciones_disparo(),self.rect.midtop,speed)
        sonido.play() 
        sprites.add(laser)
        lasers.add(laser)
    
    


