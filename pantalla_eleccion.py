# pantalla_eleccion.py - Gestión de la pantalla de elección de camino

import pygame
from config import *
from camara_ui import Boton

class PantallaEleccion:
    """Gestiona la pantalla de elección de camino en bifurcaciones"""
    
    def __init__(self):
        self.botones_camino = []
    
    def configurar_opciones(self, siguientes_casillas):
        """Configura los botones para elegir entre caminos"""
        self.botones_camino = []
        
        if len(siguientes_casillas) == 2:
            boton1 = Boton(ANCHO//2 - 330, ALTO//2 - 40, 300, 60,
                          f" Ir a Casilla {siguientes_casillas[1]}", VERDE)
            boton2 = Boton(ANCHO//2 + 30, ALTO//2 - 40, 300, 60,
                          f" Ir a Casilla {siguientes_casillas[0]}", AZUL)
            self.botones_camino = [(boton1, siguientes_casillas[1]), (boton2, siguientes_casillas[0])]
    
    def dibujar(self, pantalla):
        """Dibuja la pantalla de elección de camino"""
        # Overlay oscuro semi-transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(230)
        overlay.fill((44, 62, 80))
        pantalla.blit(overlay, (0, 0))
        
        # Título principal
        fuente_titulo = pygame.font.Font(None, 55)
        titulo = fuente_titulo.render("Elige tu camino", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
        
        # Descripción
        fuente_desc = pygame.font.Font(None, 32)
        desc = fuente_desc.render("Selecciona la casilla a la que quieres ir", True, BLANCO)
        pantalla.blit(desc, (ANCHO//2 - desc.get_width()//2, 250))
        
        # Botones de opciones
        for boton, _ in self.botones_camino:
            boton.dibujar(pantalla)
    
    def manejar_click(self, mouse_pos):
        """Maneja el click en alguno de los botones de camino"""
        for boton, id_destino in self.botones_camino:
            if boton.click(mouse_pos):
                return id_destino
        return None
    
    def actualizar_hover(self, mouse_pos):
        """Actualiza el estado hover de los botones"""
        for boton, _ in self.botones_camino:
            boton.actualizar_hover(mouse_pos)
    
    def reset(self):
        """Limpia los botones de camino"""
        self.botones_camino = []