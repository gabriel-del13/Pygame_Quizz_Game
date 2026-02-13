# pantallas_finales.py - Pantallas de victoria y game over

import pygame
from PIL import Image, ImageSequence
from config import *
from camara_ui import Boton
from efectos_visuales import EfectosVisuales

class PantallaVictoria:
    """Gestiona la pantalla de victoria con GIF animado"""
    
    def __init__(self, ruta_gif="sticker.gif"):
        # Cargar y procesar GIF
        try:
            self.gif_victoria = Image.open(ruta_gif)
            self.gif_frames = []
            for frame in ImageSequence.Iterator(self.gif_victoria):
                # Convertir cada frame a formato Pygame
                frame_rgba = frame.convert("RGBA")
                frame_pygame = pygame.image.fromstring(
                    frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                )
                # Redimensionar el sticker (ajusta el tamaño aquí)
                frame_pygame = pygame.transform.scale(frame_pygame, (200, 200))
                self.gif_frames.append(frame_pygame)
        except:
            # Si no se encuentra el GIF, usar frames vacíos
            self.gif_frames = []
        
        self.gif_frame_actual = 0
        self.gif_tiempo = 0
        self.particulas_confeti = []
        self.confeti_generado = False
    
    def actualizar_gif(self):
        """Actualiza el frame actual del GIF"""
        if not self.gif_frames:
            return
        
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.gif_tiempo > 70:  # Velocidad del GIF
            self.gif_frame_actual = (self.gif_frame_actual + 1) % len(self.gif_frames)
            self.gif_tiempo = tiempo_actual
    
    def dibujar(self, pantalla, vidas):
        """Dibuja la pantalla de victoria"""
        # Overlay verde
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(250)
        overlay.fill((39, 174, 96))  # Verde victoria
        pantalla.blit(overlay, (0, 0))
        
        # Título
        fuente_titulo = pygame.font.Font(None, 80)
        titulo = fuente_titulo.render("¡GANASTE!", True, DORADO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
        
        # Subtítulo
        fuente_sub = pygame.font.Font(None, 38)
        subtitulo = fuente_sub.render("¡Llegaste a la meta!", True, BLANCO)
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 280))
        
        # Estadísticas
        fuente_stats = pygame.font.Font(None, 32)
        stats = fuente_stats.render(f"Vidas restantes: {vidas}", True, BLANCO)
        pantalla.blit(stats, (ANCHO//2 - stats.get_width()//2, 340))
        
        # Animar y dibujar GIF
        if self.gif_frames:
            self.actualizar_gif()
            sticker_x = ANCHO//2 - 100  # Centrado horizontalmente
            sticker_y = 500              # Ajusta altura
            pantalla.blit(self.gif_frames[self.gif_frame_actual], (sticker_x, sticker_y))
        
        # Generar confeti si no se ha generado
        if not self.confeti_generado:
            self.particulas_confeti = EfectosVisuales.generar_confeti(200)
            self.confeti_generado = True
        
        # Dibujar confeti
        EfectosVisuales.actualizar_confeti(self.particulas_confeti, pantalla)
        
        # Botón de reinicio
        boton_reinicio = Boton(ANCHO//2 - 140, 420, 280, 55, "Jugar de Nuevo", AZUL)
        boton_reinicio.dibujar(pantalla)
        
        return boton_reinicio
    
    def reset(self):
        """Reinicia el estado de la pantalla de victoria"""
        self.confeti_generado = False
        self.gif_frame_actual = 0


class PantallaGameOver:
    """Gestiona la pantalla de game over"""
    
    def dibujar(self, pantalla):
        """Dibuja la pantalla de game over"""
        # Overlay rojo
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(250)
        overlay.fill((192, 57, 43))  # Rojo game over
        pantalla.blit(overlay, (0, 0))
        
        # Título
        fuente_titulo = pygame.font.Font(None, 80)
        titulo = fuente_titulo.render("GAME OVER", True, BLANCO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 180))
        
        # Subtítulo
        fuente_sub = pygame.font.Font(None, 38)
        subtitulo = fuente_sub.render("Se acabaron las vidas", True, BLANCO)
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 280))
        
        # Botón de reinicio
        boton_reinicio = Boton(ANCHO//2 - 140, 420, 280, 55, "Jugar de Nuevo", AZUL)
        boton_reinicio.dibujar(pantalla)
        
        return boton_reinicio