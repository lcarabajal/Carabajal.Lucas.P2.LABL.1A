import pygame
from config import *


pygame.init()
pantalla = pygame.display.set_mode(SIZE)

lista_animaciones_jugador = [
    # Personaje yendo a la izquierda 7 - 8
    pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/7.png").convert_alpha(),(SIZE_SHIP)),
    pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/8.png").convert_alpha(),(SIZE_SHIP)),
    # Personaje stand by 9 r
    pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/9.png").convert_alpha(),(SIZE_SHIP)),
    # Personaje yendo a la derecha 10 - 11r
    pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/10.png").convert_alpha(),(SIZE_SHIP)),
    pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/11.png").convert_alpha(),(SIZE_SHIP))]


lista_animacion_barra_de_vida = [
    pygame.transform.scale(pygame.image.load(r"./src/animations/health Bar/0.png").convert_alpha(),(SIZE_HEALTH_BAR)),
    pygame.transform.scale(pygame.image.load(r"./src/animations/health Bar/1.png").convert_alpha(),(SIZE_HEALTH_BAR)),
    pygame.transform.scale(pygame.image.load(r"./src/animations/health Bar/2.png").convert_alpha(),(SIZE_HEALTH_BAR)),
    pygame.transform.scale(pygame.image.load(r"./src/animations/health Bar/3.png").convert_alpha(),(SIZE_HEALTH_BAR)) ]

def get_animaciones_asteroide():
    lista_animacion_asteroide = [
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-00.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-01.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-02.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-03.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-04.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-05.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-06.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-07.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-08.png").convert_alpha(),(SIZE_ASTEROID)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/asteroide/spin-09.png").convert_alpha(),(SIZE_ASTEROID))]
    
    return lista_animacion_asteroide                            

def get_animaciones_escudo():                             
    lista_animacion_powerUp_escudo = [
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/0.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/1.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/2.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/3.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/4.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/5.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/6.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/7.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/8.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/9.png").convert_alpha(),(SIZE_POWER_UP)),
        pygame.transform.scale(pygame.image.load(r"./src/animations/powerUP/10.png").convert_alpha(),(SIZE_POWER_UP))]
                            
    return lista_animacion_powerUp_escudo

def get_animaciones_explosion():
    lista_animaciones_explosion = [
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/17.png").convert_alpha()),(SIZE_EXPLOSION)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/16.png").convert_alpha()),(SIZE_EXPLOSION)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/12.png").convert_alpha()),(SIZE_EXPLOSION)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/13.png").convert_alpha()),(SIZE_EXPLOSION)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/14.png").convert_alpha()),(SIZE_EXPLOSION)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/explosion/15.png").convert_alpha()),(SIZE_EXPLOSION))]
    

    return lista_animaciones_explosion

def get_animaciones_disparo():
    lista_animaciones_disparo = [
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/0.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/1.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/2.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/3.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/4.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/5.png").convert_alpha()),(SIZE_LASER)),
        pygame.transform.scale((pygame.image.load(r"./src/animations/disparo/6.png").convert_alpha()),(SIZE_LASER))]
    
    return lista_animaciones_disparo