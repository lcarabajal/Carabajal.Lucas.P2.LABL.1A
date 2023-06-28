import pygame
import sys
import random
import re
import json

#$python -m venv env se crea un entorno
#source env/Scripts/activate    entramos al entorno y ejecuta el script activate
#si usamos el pip list, solo muestra las caracteristicas del entorno env

from animaciones import *
from config import * 
from nave import Nave
from asteroide import Asteroide 
from powerUp import PowerUp
from explosion import Explosion


class Juego:
    def __init__(self):
        pygame.init()
        self.speed_asteroid = 1
        self.speed_powerUp = 1.5
        self.vida = 3
        self.escudo = 0
        self.contador_eliminaciones = 0
        self.tiempo = 0
        self.contador_escudo = 0
        self.contador_explosion = 0
        self.pantalla = pygame.display.set_mode(SIZE)
        self.reloj = pygame.time.Clock()
        self.sonido = pygame.mixer.Sound("./src/sound/laser.mp3")
        self.musica_game_over = pygame.mixer.Sound("./src/sound/menu/Game_Over.mp3")
        self.efecto_sonido_seleccion = pygame.mixer.Sound("./src/sound/menu/seleccion_opcion.mp3")       
        self.efecto_powerUp1 = pygame.mixer.Sound("./src/sound/power_up.mp3")     
        self.efecto_mejora = pygame.mixer.Sound("./src/sound/upgrade.mp3")
        self.efecto_escudo = pygame.mixer.Sound("./src/sound/activacion_escudo.mp3")   
        self.efecto_golpeado = pygame.mixer.Sound("./src./sound/golpeado.mp3")  
        self.efecto_alerta = pygame.mixer.Sound("./src/sound/alerta.mp3")
        self.efecto_explosion = pygame.mixer.Sound("./src/sound/explosion.mp3")
        
        self.lista_score = []
        self.SCORE = 0 
        
        self.inicio = True
        self.finalizado = True
        self.jugando = False
        self.flag_oleada_completada = False
        self.flag_casi_muerto = False
        self.flag_mostrado = False
        
        pygame.display.set_caption("Hateech")
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load(r"./src/animations/jugador/9.png").convert_alpha(),(SIZE_SHIP)))
        
        self.fondo = pygame.image.load("./src/images/fondo.jpg").convert()
        self.fondo = pygame.transform.scale(self.fondo,(WIDTH,HEIGHT))
        self.fuente = pygame.font.Font("./src/font/Type.ttf",30)

        self.sprites = pygame.sprite.Group()
        self.asteroides = pygame.sprite.Group()
        self.powerUps = pygame.sprite.Group()                
        self.lasers = pygame.sprite.Group() 
        self.explosions = pygame.sprite.Group()
        self.nave = Nave(lista_animaciones_jugador,(WIDTH // 2 , HEIGHT - 20))

        self.agregar_sprite(self.nave)
        
        
    def agregar_sprite(self, sprite):
        self.sprites.add(sprite) 

    def agregar_asteroides(self, asteroide):
        self.asteroides.add(asteroide) 
        
    def agregar_laser(self, laser):
        self.lasers.add(laser) 
        
    def agregar_explosion(self,explosion):
        self.explosions.add(explosion)
    
    def agregar_powerUp(self, powerUp):
        self.powerUps.add(powerUp)

        
    #aplicacion
    def comenzar(self):
        self.jugando = True
        musica_fase_comenzando = pygame.mixer.Sound("./src/sound/menu/fase_empezando.mp3")
        musica_fase_comenzando.play()

        while self.jugando:
        
            self.reloj.tick(FPS)
            
            self.manejar_eventos()

            self.rederizar_pantalla()

            self.actualizar_elementos()

    def manejar_eventos(self):
         
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.salir()
            
            elif evento.type == pygame.KEYDOWN:
               
                if evento.key   == pygame.K_LEFT:
                    self.nave.velocidad_x = -SPEED_SHIP
                    

                elif evento.key == pygame.K_RIGHT:
                    self.nave.velocidad_x = SPEED_SHIP
                    
                
                elif evento.key == pygame.K_UP:
                    self.nave.velocidad_y = -SPEED_SHIP
                    

                elif evento.key == pygame.K_DOWN:
                    self.nave.velocidad_y = SPEED_SHIP
                    

                elif evento.key == pygame.K_SPACE:
                    self.nave.disparar(self.sonido,SPEED_LASER,self.sprites,self.lasers)

                elif evento.key == pygame.K_ESCAPE:
                    self.pausa()

            #anti Rebote
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and self.nave.velocidad_x < 0:
                    self.nave.velocidad_x = 0
                    
                elif evento.key == pygame.K_RIGHT and self.nave.velocidad_x > 0:
                    self.nave.velocidad_x = 0
                    
                if evento.key   == pygame.K_UP and self.nave.velocidad_y < 0:
                    self.nave.velocidad_y = 0
                    
                elif evento.key == pygame.K_DOWN and self.nave.velocidad_y > 0:
                    self.nave.velocidad_y = 0
       
    def actualizar_elementos(self):
        self.generar_asteroides(MAX_ASTEROIDES)
        self.sprites.update()
        
        #controlador de animacion de escudo
        if self.escudo > 0:
            self.tiempo += 1
            if self.contador_escudo >= 9:
                self.contador_escudo = 0
            elif self.tiempo == 7:
                self.contador_escudo += 1
                self.tiempo = 0  

        for asteroide in self.asteroides:
            if asteroide.rect.bottom >= HEIGHT:
                self.SCORE -= 20
                asteroide.kill()
            
        choque_asteroide = pygame.sprite.spritecollide(self.nave, self.asteroides, True)
                  
        if len(choque_asteroide) > 0 and self.escudo > 0:
            self.efecto_escudo.play()
            self.escudo -= 1
        elif len(choque_asteroide) > 0:
            self.efecto_golpeado.play()
            self.vida -= 1
            
        if self.vida == 0 and self.escudo == 0:
            pygame.time.wait(800)
            self.game_over()
            
        elif self.vida < 2:
            if  not self.flag_casi_muerto:
                self.efecto_alerta.play()
                self.flag_casi_muerto = True
                        
              
        for laser in self.lasers:
            if laser.rect.top <= 0:
                self.SCORE -= 10
                laser.kill()
                            
            lista_colision = pygame.sprite.spritecollide(laser, self.asteroides, True) #genera una lista de los lasers que se choquen con los asteroides
               
            self.laser_impacta_asteroide(lista_colision)
            if (lista_colision):
                laser.kill()
                self.contador_eliminaciones += 1
        
        powerUp_conseguido = pygame.sprite.spritecollide(self.nave,self.powerUps, True)  
        
        if len(powerUp_conseguido):
            self.efecto_powerUp1.play()
            self.efecto_mejora.play()
            if self.escudo < 3:
                self.escudo = 3
             
        for powerUp in self.powerUps:
            if powerUp.rect.bottom >= HEIGHT:
                powerUp.kill()
                
            elif len(powerUp_conseguido) > 0:
                powerUp.kill() 
                self.powerUps.empty()
      
    def laser_impacta_asteroide(self, lista:list):
        if len(lista): #si la lista tiene algo es porque hubo colision
            explosion = lista[0]
            explosion = explosion.rect.center
            self.generar_explosion(explosion)
            self.efecto_explosion.play()
              
                
            self.SCORE += 10
            if self.escudo < 2:    
                powerUp = lista[0]
                powerUp = powerUp.rect.center
                self.generar_powerUp(MAX_POWER_UPS,powerUp)
            
                
                
        
    def rederizar_pantalla(self):
        self.pantalla.blit(self.fondo, ORIGIN)
        self.pantalla.blit(self.fuente.render("SCORE: " + str(self.SCORE),True,BLANCO),SCORE_POS)
        self.pantalla.blit(lista_animacion_barra_de_vida[self.vida],HEALTH_BAR_POS)
        
        match(self.escudo):
            case 0:
                pass
            case 1:
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS)
            case 2:
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS)
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS_2)
            case 3:
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS)
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS_2)
                self.pantalla.blit(get_animaciones_escudo()[self.contador_escudo],ESCUDO_POS_3)
        
        self.sprites.draw(self.pantalla)
        pygame.display.flip()
           
    def salir(self):
        pygame.quit()
        sys.exit()
    
    def pausa(self):
        self.jugando = False
            
    def generar_asteroides(self, cantidad): 
        if len(self.asteroides) == 0: 
            for i in range(cantidad):
                posicion =(random.randrange(20, WIDTH-20),random.randrange(-500,0))
                
                if self.contador_eliminaciones == 10 and self.speed_asteroid >= 1 and self.flag_oleada_completada:
                    self.speed_asteroid += 0.50
                    self.flag_oleada_completada = False
                elif self.contador_eliminaciones == 10:
                    self.contador_eliminaciones = 0
                    self.flag_oleada_completada = True
                
                
                asteroide = Asteroide(posicion,self.speed_asteroid)
                
                self.agregar_asteroides(asteroide)
                self.agregar_sprite(asteroide)
    
    def generar_powerUp(self, cantidad, posicion): 
        if len(self.powerUps) == 0: 
            for i in range(cantidad):
                if random.randrange(0,10) == random.randrange(0,10):
                    
                    powerUp = PowerUp(posicion,self.speed_powerUp )
                    
                    self.agregar_powerUp(powerUp)
                    self.agregar_sprite(powerUp)
    
    def generar_explosion(self,posicion):
        explosion = Explosion(posicion)
        
        self.agregar_sprite(explosion)
        self.agregar_explosion(explosion)
        

    def game_over(self):
        self.finalizado = True
        self.mostrar_pantalla_fin()
        

    def mostrar_pantalla_fin(self):
        self.musica_game_over.play()
        self.flag = False
        self.guarda_score(self.SCORE)
            
        lista_puntuacion = self.cargar_score()
        
        titilar_texto = True
        while self.finalizado:
            self.pantalla.fill(NEGRO)
            for evento in pygame.event.get():
                
                if evento.type == pygame.QUIT:
                    self.salir()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    self.finalizado = False
                    self.musica_game_over.stop()
                    self.efecto_sonido_seleccion.play()
                    pygame.time.delay(1500)
                    
                    self.reinciar_juego()
            
            sobre_puntuacion = self.fuente.render(f" MEJOR PUNTUACION ",True,VERDE)
            rect_sobre_puntuacion = sobre_puntuacion.get_rect()
            rect_sobre_puntuacion.center = SOBRE_PUN_POS
            self.pantalla.blit(sobre_puntuacion, rect_sobre_puntuacion)
            
            if not self.flag: 
                for i in range(len(lista_puntuacion)):
                    
                    if not self.flag:
                        
                        puntuacion_alta = lista_puntuacion[i]['puntuacion']
                        nombre_alta = lista_puntuacion[i]['nombre']
                        puntuaciones = self.fuente.render(f"{nombre_alta} - {puntuacion_alta}",True,AZUL)
                        self.flag = True
                    
                    elif puntuacion_alta < lista_puntuacion[i]['puntuacion']:
                    
                        puntuacion_alta = lista_puntuacion[i]['puntuacion']
                        nombre_alta = lista_puntuacion[i]['nombre']
                        puntuaciones = self.fuente.render(f"{nombre_alta} - {puntuacion_alta}",True,AZUL)
                
                    elif puntuacion_alta == lista_puntuacion[i]['puntuacion']:
                        
                        numero_1 = random.randrange(0,2)                   
                        numero_2 = random.randrange(0,2)                   
                    
                        if numero_1 >= numero_2:
                            puntuaciones = self.fuente.render(f"{nombre_alta} - {puntuacion_alta}",True,AZUL)
                        
                        else:
                            puntuacion_alta = lista_puntuacion[i]['puntuacion']
                            nombre_alta = lista_puntuacion[i]['nombre']
                            puntuaciones = self.fuente.render(f"{nombre_alta} - {puntuacion_alta}",True,AZUL)
            
            
            
            rect_puntuaciones = puntuaciones.get_rect()
            rect_puntuaciones.center = CENTER
            self.pantalla.blit(puntuaciones, rect_puntuaciones)
                
        
            
            texto = self.fuente.render("GAME OVER", True, VERDE)
            rect_texto = texto.get_rect()
            rect_texto.center = GAME_OVER_POS
            self.pantalla.blit(texto, rect_texto)
            

            texto_reinciar = self.fuente.render("Volver a jugar ? Presione clic", True, BLANCO)
            rect_texto_reinciar = texto_reinciar.get_rect()
            rect_texto_reinciar.midbottom = MID_BOTTOM
            
            if titilar_texto:
                self.pantalla.blit(texto_reinciar, rect_texto_reinciar)
            
            titilar_texto = not titilar_texto
            pygame.time.delay(450)
            pygame.display.flip()
            
    def guarda_score(self,score):
        
        diccionario = {}

        nombre = input("Ingrese su nombre (solo 3 letras o números): ")

        while not re.match(r'^[a-zA-Z0-9]{3}$', nombre):
            print("El nombre debe tener exactamente 3 letras o números.")
            nombre = input("Ingrese su nombre (solo 3 letras o números): ")
        
        diccionario['nombre'] = nombre
        diccionario['puntuacion'] = score
        
        lista_actualizada = self.cargar_score()
        
        
        if lista_actualizada:
            lista_actualizada.append(diccionario)
            with open(r"E:\Hateehc\src\lista_puntuacion.json","w") as archivo:
                json.dump(lista_actualizada,archivo,indent = 2,separators=(", "," : "))
                     
        else:
            self.lista_score.append(diccionario)
            with open(r"E:\Hateehc\src\lista_puntuacion.json","w") as archivo:
                json.dump(self.lista_score,archivo,indent = 2,separators=(", "," : "))
            
        
       
            
    def cargar_score(self):
        try:
            with open(r"E:\Hateehc\src\lista_puntuacion.json","r") as archivo:
                puntuaciones = json.load(archivo)  
                
        except FileNotFoundError:
           return False
        
        return puntuaciones
    
    def reinciar_juego(self):
        self.SCORE = 0
        self.vida = 3
        self.escudo = 0 
        self.speed_asteroid = 1
        self.nave.remove()
        self.sprites.empty()
        self.lasers.empty()
        self.asteroides.empty()
        self.powerUps.empty()
        self.explosions.empty()
        
        self.nave = Nave(lista_animaciones_jugador, (self.pantalla.get_width() // 2 , self.pantalla.get_height() - 20))
        self.agregar_sprite(self.nave)
        self.comenzar()
        
        
              
        
juego = Juego()

while not juego.jugando:
    pygame.init()
    
    screen = pygame.display.set_mode(SIZE)

    color_light = (170,170,170)  #resaltado

    color_dark = (100,100,100) #normal

    fuente_menu = pygame.font.Font('./src/font/Technocra.ttf',25)
    fuente_titulo = pygame.font.Font('./src/font/Technocra.ttf',100)
    
    titulo = fuente_titulo.render("HATEEHC", True, BLANCO)
    texto = fuente_menu.render('Start' , True , VERDE)
    
    musica_menu = pygame.mixer.Sound("./src/sound/menu/menu_Soudtrack.mp3")
    musica_menu.set_volume(0.6)
    efecto_sonido_seleccion = pygame.mixer.Sound("./src/sound/menu/seleccion_opcion.mp3")
    
    
    fondo_menu =  pygame.image.load("./src/images/menu_espacio.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu,(WIDTH,HEIGHT))
    
    while not juego.jugando:
        musica_menu.play()
        
        screen.blit(fondo_menu,(ORIGIN))
        
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                
                if WIDTH/2 <= mouse[0] <= WIDTH/2+110 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40:
                    musica_menu.stop()
                    efecto_sonido_seleccion.play()
                    pygame.time.delay(700)
                    juego.finalizado = True
                    juego.comenzar()
        
        mouse = pygame.mouse.get_pos() #registro del mouse (x,y)
        
        posicion_x = WIDTH/2-55
        posicion_y = HEIGHT/2
        
        if posicion_x <= mouse[0] <= posicion_x+110 and  posicion_y <= mouse[1] <= posicion_y+40: 
            pygame.draw.rect(screen,color_light,[posicion_x,posicion_y,110,40]) 
            
        else: 
            pygame.draw.rect(screen,color_dark,[posicion_x,posicion_y,110,40]) 
        
        screen.blit(titulo ,(WIDTH//2-200,150))            
        screen.blit(texto ,(posicion_x + 22,posicion_y))

        pygame.display.flip()




