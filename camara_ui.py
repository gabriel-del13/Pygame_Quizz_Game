# camara_ui.py - Sistema de cámara y UI

import pygame
from config import *

class Camara:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        
    def actualizar(self, personaje_x, personaje_y):
        """Actualiza la posición de la cámara siguiendo al personaje"""
        self.offset_x = personaje_x - ANCHO // 2
        self.offset_y = personaje_y - ALTO // 2
        
        # Limitar la cámara
        self.offset_x = max(0, min(self.offset_x, MUNDO_ANCHO - ANCHO))
        self.offset_y = max(0, min(self.offset_y, MUNDO_ALTO - ALTO))


class Boton:
    def __init__(self, x, y, ancho, alto, texto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = tuple(min(c + 30, 255) for c in color)
        self.hover = False
        
    def dibujar(self, pantalla):
        color_actual = self.color_hover if self.hover else self.color
        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, self.rect, 3, border_radius=8)
        
        fuente = pygame.font.Font(None, 28)
        texto = fuente.render(self.texto, True, BLANCO)
        texto_rect = texto.get_rect(center=self.rect.center)
        pantalla.blit(texto, texto_rect)
        
    def click(self, pos):
        return self.rect.collidepoint(pos)
    
    def actualizar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)


class UI:
    @staticmethod
    def dibujar_corazon(pantalla, cx, cy, tam, color):
        """Dibuja un corazón centrado en (cx, cy)"""
        r = tam // 4
        pygame.draw.circle(pantalla, color, (cx - r + 1, cy - r // 2), r)
        pygame.draw.circle(pantalla, color, (cx + r - 1, cy - r // 2), r)
        pygame.draw.polygon(pantalla, color, [
            (cx - tam // 2 + 1, cy),
            (cx + tam // 2 - 1, cy),
            (cx, cy + tam // 2)
        ])

    @staticmethod
    def dibujar_panel_superior(pantalla, vidas, casilla_actual):
        """Dibuja el panel superior con información del juego"""
        panel = pygame.Surface((ANCHO, 60))
        panel.set_alpha(230)
        panel.fill(GRIS_OSCURO)
        pantalla.blit(panel, (0, 0))

        fuente_info = pygame.font.Font(None, 32)

        # Vidas con corazones dibujados
        for i in range(3):
            color = ROJO if i < vidas else GRIS
            UI.dibujar_corazon(pantalla, 25 + i * 28, 30, 22, color)

        vidas_texto = fuente_info.render(f"x{vidas}", True, ROJO)
        pantalla.blit(vidas_texto, (25 + 3 * 28, 18))

        # Progreso
        progreso_texto = fuente_info.render(f"Casilla: {casilla_actual}", True, AMARILLO)
        pantalla.blit(progreso_texto, (ANCHO - 220, 18))
    
    @staticmethod
    def dibujar_panel_inferior(pantalla, mensaje):
        """Dibuja el panel inferior con instrucciones"""
        panel_inferior = pygame.Surface((ANCHO, 50))
        panel_inferior.set_alpha(230)
        panel_inferior.fill(GRIS_OSCURO)
        pantalla.blit(panel_inferior, (0, ALTO - 50))
        
        fuente_hint = pygame.font.Font(None, 26)
        hint = fuente_hint.render(mensaje, True, BLANCO)
        pantalla.blit(hint, (ANCHO//2 - hint.get_width()//2, ALTO - 35))