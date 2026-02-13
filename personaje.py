import pygame
import math
from config import *

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 4
        self.ancho = 30
        self.alto = 30 # Usamos un cuadrado para la colisión base
        
        # Rotación
        self.angulo = 0
        self.angulo_objetivo = 0
        self.velocidad_rotacion = 0.15 # Qué tan rápido alcanza el ángulo deseado
        
        # Animación
        self.frame_caminar = 0
        self.velocidad_animacion = 0.2
        self.moviendose = False

    def mover(self, teclas, casillas):
        self.moviendose = False
        dx, dy = 0, 0
        
        # Determinar dirección y ángulo objetivo
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -self.velocidad
            self.angulo_objetivo = 90
            self.moviendose = True
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = self.velocidad
            self.angulo_objetivo = 270
            self.moviendose = True
            
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -self.velocidad
            self.angulo_objetivo = 180
            self.moviendose = True
            if dx > 0: self.angulo_objetivo = 225 # Diagonales
            if dx < 0: self.angulo_objetivo = 135
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = self.velocidad
            self.angulo_objetivo = 0
            self.moviendose = True
            if dx > 0: self.angulo_objetivo = 315
            if dx < 0: self.angulo_objetivo = 45

        # --- Lógica de Rotación Suave ---
        # Esto hace que el ángulo actual "persiga" al objetivo
        diff = (self.angulo_objetivo - self.angulo + 180) % 360 - 180
        self.angulo += diff * self.velocidad_rotacion

        # --- Lógica de Hitbox (Dentro de casillas) ---
        nueva_x = self.x + dx
        nueva_y = self.y + dy
        
        # Definimos el margen de colisión del personaje (su "cuerpo")
        # Para que no se salga de la casilla, evaluamos sus 4 esquinas
        puede_mover = False
        margen = 12 # Radio de colisión
        
        for casilla in casillas:
            # Verificamos si el área ocupada por el personaje está dentro de la casilla
            if (nueva_x - margen >= casilla.x + 5 and 
                nueva_x + margen <= casilla.x + TAMANO_CASILLA - 5 and
                nueva_y - margen >= casilla.y + 5 and 
                nueva_y + margen <= casilla.y + TAMANO_CASILLA - 5):
                puede_mover = True
                break
        
        if puede_mover:
            self.x = nueva_x
            self.y = nueva_y
        
        if self.moviendose:
            self.frame_caminar += self.velocidad_animacion
            if self.frame_caminar >= 4:
                self.frame_caminar = 0

    def dibujar(self, pantalla, offset_x, offset_y):
        sc_x = int(self.x - offset_x)
        sc_y = int(self.y - offset_y)
        
        # Creamos una superficie temporal para dibujar al personaje y luego rotarla
        # o usamos trigonometría para dibujar relativo al centro.
        # Aquí usaremos trigonometría simple para mantener los dibujos vectoriales de pygame.
        
        rad = math.radians(self.angulo)
        
        def rotar_punto(px, py, angulo_rad):
            """Rota un punto respecto al centro (0,0)"""
            nx = px * math.cos(angulo_rad) - py * math.sin(angulo_rad)
            ny = px * math.sin(angulo_rad) + py * math.cos(angulo_rad)
            return (int(nx + sc_x), int(ny + sc_y))

        # 1. Sombra (estática en el suelo)
        pygame.draw.ellipse(pantalla, (0, 0, 0, 60), (sc_x - 15, sc_y - 5, 30, 20))

        # 2. Piernas (se mueven adelante/atrás según el ángulo)
        if self.moviendose:
            oscilacion = math.sin(self.frame_caminar * math.pi / 2) * 8
            p1 = rotar_punto(-6, oscilacion, rad)
            p2 = rotar_punto(6, -oscilacion, rad)
            pygame.draw.circle(pantalla, (40, 40, 40), p1, 5)
            pygame.draw.circle(pantalla, (40, 40, 40), p2, 5)

        # 3. Hombros y Cuerpo (Óvalo que rota)
        # Dibujamos varios círculos/elipses rotados para formar el torso
        for i in range(-12, 13, 4):
            pos_hombro = rotar_punto(i, 0, rad)
            pygame.draw.circle(pantalla, ROJO, pos_hombro, 10)

        # 4. Brazos (Ahora siempre se ven ambos porque rotan con el cuerpo)
        mano_l = rotar_punto(-15, 8 if self.moviendose else 5, rad)
        mano_r = rotar_punto(15, -8 if self.moviendose else 5, rad)
        pygame.draw.circle(pantalla, (255, 200, 150), mano_l, 4)
        pygame.draw.circle(pantalla, (255, 200, 150), mano_r, 4)

        # 5. Cabeza (Encima de todo)
        centro_cabeza = rotar_punto(0, 0, rad)
        pygame.draw.circle(pantalla, (192, 57, 43), centro_cabeza, 11)
        pygame.draw.circle(pantalla, (80, 20, 20), centro_cabeza, 11, 2)
        
        # Referencia de "frente" (pequeña nariz o visera)
        frente = rotar_punto(0, 8, rad)
        pygame.draw.circle(pantalla, (50, 10, 10), frente, 3)