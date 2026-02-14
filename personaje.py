import pygame
import math
from config import *

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 2
        self.ancho = 30
        self.alto = 30

        # Dirección: 0=abajo, 1=izquierda, 2=arriba, 3=derecha
        self.direccion = 0
        
        # Animación
        self.frame_caminar = 0
        self.velocidad_animacion = 0.15
        self.moviendose = False
        self.tick_animacion = 0

    def mover(self, teclas, casillas):
        self.moviendose = False
        dx, dy = 0, 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -self.velocidad
            self.direccion = 1
            self.moviendose = True
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = self.velocidad
            self.direccion = 3
            self.moviendose = True

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -self.velocidad
            if not (dx != 0):
                self.direccion = 2
            self.moviendose = True
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = self.velocidad
            if not (dx != 0):
                self.direccion = 0
            self.moviendose = True

        # Movimiento diagonal más lento
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        nueva_x = self.x + dx
        nueva_y = self.y + dy

        puede_mover = False
        margen = 12

        for casilla in casillas:
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
            self.tick_animacion += self.velocidad_animacion
            self.frame_caminar = int(self.tick_animacion) % 4
        else:
            self.frame_caminar = 0
            self.tick_animacion = 0

    def dibujar(self, pantalla, offset_x, offset_y):
        cx = int(self.x - offset_x)
        cy = int(self.y - offset_y)

        # =============================================
        #  PALETA DE COLORES
        # =============================================
        COLOR_PIEL       = (225, 159, 86)
        COLOR_PIEL_OSCURO= (210, 165, 120)
        COLOR_CAMISA     = (0, 134, 70)    # Rojo (cambia si quieres)
        COLOR_CAMISA_OSC = (2, 102, 56)
        COLOR_PANTALON   = (70, 55, 40)
        COLOR_PANTALON_OSC = (50, 38, 28)
        COLOR_PELO       = (60, 40, 25)
        COLOR_PELO_OSC   = (40, 25, 15)
        COLOR_ZAPATO     = (50, 35, 25)
        COLOR_OJO        = (30, 30, 30)
        COLOR_BOCA       = (180, 100, 80)
        COLOR_SOMBRA     = (0, 0, 0)

        # Oscilación de piernas al caminar
        # frame_caminar va de 0 a 3:  0=parado, 1=pie adelante, 2=centro, 3=pie atrás
        osc = 0
        if self.moviendose:
            osc = math.sin(self.tick_animacion * math.pi) * 5  # oscila entre -5 y 5

        # =============================================
        #  SOMBRA EN EL SUELO
        # =============================================
        sombra_surf = pygame.Surface((28, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 50), (0, 0, 28, 12))
        pantalla.blit(sombra_surf, (cx - 14, cy + 8))

        # =============================================
        #  DIBUJO SEGÚN DIRECCIÓN
        # =============================================
        if self.direccion == 0:
            self._dibujar_frente(pantalla, cx, cy, osc,
                                 COLOR_PIEL, COLOR_PIEL_OSCURO,
                                 COLOR_CAMISA, COLOR_CAMISA_OSC,
                                 COLOR_PANTALON, COLOR_PANTALON_OSC,
                                 COLOR_PELO, COLOR_PELO_OSC,
                                 COLOR_ZAPATO, COLOR_OJO, COLOR_BOCA, COLOR_SOMBRA)
        elif self.direccion == 2:
            self._dibujar_espalda(pantalla, cx, cy, osc,
                                  COLOR_PIEL, COLOR_PIEL_OSCURO,
                                  COLOR_CAMISA, COLOR_CAMISA_OSC,
                                  COLOR_PANTALON, COLOR_PANTALON_OSC,
                                  COLOR_PELO, COLOR_PELO_OSC,
                                  COLOR_ZAPATO, COLOR_SOMBRA)
        elif self.direccion == 1:
            self._dibujar_lado(pantalla, cx, cy, osc, False,
                               COLOR_PIEL, COLOR_PIEL_OSCURO,
                               COLOR_CAMISA, COLOR_CAMISA_OSC,
                               COLOR_PANTALON, COLOR_PANTALON_OSC,
                               COLOR_PELO, COLOR_PELO_OSC,
                               COLOR_ZAPATO, COLOR_OJO, COLOR_SOMBRA)
        elif self.direccion == 3:
            self._dibujar_lado(pantalla, cx, cy, osc, True,
                               COLOR_PIEL, COLOR_PIEL_OSCURO,
                               COLOR_CAMISA, COLOR_CAMISA_OSC,
                               COLOR_PANTALON, COLOR_PANTALON_OSC,
                               COLOR_PELO, COLOR_PELO_OSC,
                               COLOR_ZAPATO, COLOR_OJO, COLOR_SOMBRA)

    # =================================================================
    #  VISTA FRONTAL (mirando hacia abajo / hacia la cámara)
    # =================================================================
    def _dibujar_frente(self, s, cx, cy, osc,
                        PIEL, PIEL_O, CAM, CAM_O, PAN, PAN_O,
                        PELO, PELO_O, ZAP, OJO, BOCA, SOMBRA):
        # -- Piernas / Zapatos --
        pie_izq_y = cy + 10 + int(osc)
        pie_der_y = cy + 10 - int(osc)
        pygame.draw.ellipse(s, PAN, (cx - 7, pie_izq_y - 2, 6, 8))
        pygame.draw.ellipse(s, PAN, (cx + 1, pie_der_y - 2, 6, 8))
        pygame.draw.ellipse(s, ZAP, (cx - 8, pie_izq_y + 3, 7, 5))
        pygame.draw.ellipse(s, ZAP, (cx + 1, pie_der_y + 3, 7, 5))

        # -- Cuerpo / Torso --
        pygame.draw.ellipse(s, CAM, (cx - 10, cy - 4, 20, 16))
        # Sombra inferior del torso
        pygame.draw.ellipse(s, CAM_O, (cx - 8, cy + 6, 16, 6))

        # -- Brazos --
        brazo_osc = int(osc * 0.6)
        # Brazo izquierdo
        pygame.draw.ellipse(s, CAM, (cx - 14, cy - 2 + brazo_osc, 7, 12))
        pygame.draw.circle(s, PIEL, (cx - 11, cy + 9 + brazo_osc), 3)
        # Brazo derecho
        pygame.draw.ellipse(s, CAM, (cx + 7, cy - 2 - brazo_osc, 7, 12))
        pygame.draw.circle(s, PIEL, (cx + 11, cy + 9 - brazo_osc), 3)

        # -- Cabeza --
        # Pelo trasero (se ve un poquito arriba)
        pygame.draw.ellipse(s, PELO, (cx - 11, cy - 20, 22, 18))
        # Cara
        pygame.draw.ellipse(s, PIEL, (cx - 9, cy - 17, 18, 16))
        # Pelo flequillo
        pygame.draw.ellipse(s, PELO, (cx - 10, cy - 20, 20, 8))
        # Mechones laterales
        pygame.draw.ellipse(s, PELO_O, (cx - 11, cy - 16, 6, 6))
        pygame.draw.ellipse(s, PELO_O, (cx + 5, cy - 16, 6, 6))

        # Ojos
        pygame.draw.circle(s, OJO, (cx - 4, cy - 10), 2)
        pygame.draw.circle(s, OJO, (cx + 4, cy - 10), 2)
        # Brillito en los ojos
        pygame.draw.circle(s, (255, 255, 255), (cx - 3, cy - 11), 1)
        pygame.draw.circle(s, (255, 255, 255), (cx + 5, cy - 11), 1)
        # Boca
        pygame.draw.line(s, BOCA, (cx - 2, cy - 6), (cx + 2, cy - 6), 1)

    # =================================================================
    #  VISTA TRASERA (mirando hacia arriba)
    # =================================================================
    def _dibujar_espalda(self, s, cx, cy, osc,
                         PIEL, PIEL_O, CAM, CAM_O, PAN, PAN_O,
                         PELO, PELO_O, ZAP, SOMBRA):
        # -- Piernas / Zapatos --
        pie_izq_y = cy + 10 + int(osc)
        pie_der_y = cy + 10 - int(osc)
        pygame.draw.ellipse(s, PAN, (cx - 7, pie_izq_y - 2, 6, 8))
        pygame.draw.ellipse(s, PAN, (cx + 1, pie_der_y - 2, 6, 8))
        pygame.draw.ellipse(s, ZAP, (cx - 8, pie_izq_y + 3, 7, 5))
        pygame.draw.ellipse(s, ZAP, (cx + 1, pie_der_y + 3, 7, 5))

        # -- Cuerpo / Torso --
        pygame.draw.ellipse(s, CAM, (cx - 10, cy - 4, 20, 16))
        pygame.draw.ellipse(s, CAM_O, (cx - 8, cy + 6, 16, 6))

        # -- Brazos --
        brazo_osc = int(osc * 0.6)
        pygame.draw.ellipse(s, CAM, (cx - 14, cy - 2 - brazo_osc, 7, 12))
        pygame.draw.circle(s, PIEL, (cx - 11, cy + 9 - brazo_osc), 3)
        pygame.draw.ellipse(s, CAM, (cx + 7, cy - 2 + brazo_osc, 7, 12))
        pygame.draw.circle(s, PIEL, (cx + 11, cy + 9 + brazo_osc), 3)

        # -- Cabeza (vista trasera = más pelo, sin cara) --
        # Pelo cubre toda la cabeza desde atrás
        pygame.draw.ellipse(s, PELO, (cx - 11, cy - 20, 22, 20))
        # Detalle de pelo
        pygame.draw.ellipse(s, PELO_O, (cx - 9, cy - 14, 18, 10))
        # Cuello apenas visible
        pygame.draw.ellipse(s, PIEL, (cx - 4, cy - 4, 8, 5))

    # =================================================================
    #  VISTA LATERAL (izquierda o derecha)
    # =================================================================
    def _dibujar_lado(self, s, cx, cy, osc, mirando_derecha,
                    PIEL, PIEL_O, CAM, CAM_O, PAN, PAN_O,
                    PELO, PELO_O, ZAP, OJO, SOMBRA):
        
        flip = 1 if mirando_derecha else -1

        # -- Piernas (una delante, otra detrás) --
        pie_del_y = cy + 10 + int(osc)
        pie_tra_y = cy + 10 - int(osc)
        
        # Pierna trasera (más al centro, se ve "detrás")
        pygame.draw.ellipse(s, PAN_O, (cx - 3, pie_tra_y - 2, 6, 8))
        pygame.draw.ellipse(s, ZAP, (cx - 4 + flip * 1, pie_tra_y + 3, 7, 5))

        # Pierna delantera
        pygame.draw.ellipse(s, PAN, (cx - 3, pie_del_y - 2, 6, 8))
        pygame.draw.ellipse(s, ZAP, (cx - 4 + flip * 1, pie_del_y + 3, 7, 5))

        # -- Cuerpo (más estrecho de lado) --
        pygame.draw.ellipse(s, CAM, (cx - 7, cy - 4, 14, 16))
        pygame.draw.ellipse(s, CAM_O, (cx - 5, cy + 6, 10, 6))

        # -- Brazo visible (solo uno en vista de perfil) --
        brazo_osc = int(osc * 0.7)
        pygame.draw.ellipse(s, CAM, (cx - 2 + flip * 2, cy - 1 + brazo_osc, 6, 11))
        pygame.draw.circle(s, PIEL, (cx + 1 + flip * 2, cy + 9 + brazo_osc), 3)

        # -- Cabeza --
        # Pelo trasero
        pygame.draw.ellipse(s, PELO, (cx - 9 - flip * 2, cy - 20, 20, 18))
        # Cara de perfil
        pygame.draw.ellipse(s, PIEL, (cx - 6 + flip * 2, cy - 18, 14, 16))
        # Pelo encima
        pygame.draw.ellipse(s, PELO, (cx - 8, cy - 20, 18, 8))
        # Mechón que cae
        pygame.draw.ellipse(s, PELO_O, (cx - 8 - flip * 2, cy - 16, 7, 8))

        # Ojo (uno solo, de perfil)
        ojo_x = cx + flip * 3
        pygame.draw.circle(s, OJO, (ojo_x, cy - 10), 2)
        pygame.draw.circle(s, (255, 255, 255), (ojo_x + flip, cy - 11), 1)

        # Nariz pequeña
        pygame.draw.circle(s, PIEL_O, (cx + flip * 8, cy - 9), 2)