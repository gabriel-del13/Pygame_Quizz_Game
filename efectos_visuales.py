# efectos_visuales.py - Efectos visuales del juego (confeti, partículas, etc.)

import pygame
import random
from config import *

class EfectosVisuales:
    """Gestiona todos los efectos visuales del juego"""
    
    @staticmethod
    def generar_confeti(cantidad=100):
        """Genera partículas de confeti que caen desde arriba"""
        particulas = []
        for _ in range(cantidad):
            particulas.append({
                'x': random.randint(0, ANCHO),
                'y': -random.randint(0, 100),  # Empiezan arriba
                'velocidad': random.randint(3, 8),
                'tam': random.randint(5, 15),
                'color': random.choice([
                    (255, 215, 0),   # Dorado
                    (255, 105, 180), # Rosa
                    (0, 191, 255),   # Azul cielo
                    (50, 205, 50),   # Verde lima
                    (255, 165, 0),   # Naranja
                    (138, 43, 226)   # Violeta
                ])
            })
        return particulas
    
    @staticmethod
    def actualizar_confeti(particulas, pantalla):
        """Actualiza y dibuja las partículas de confeti"""
        for p in particulas:
            p['y'] += p['velocidad']  # Caen
            if p['y'] < ALTO:
                pygame.draw.circle(pantalla, p['color'], (int(p['x']), int(p['y'])), p['tam'])
    
    @staticmethod
    def dibujar_estrella(pantalla, cx, cy, radio, color):
        """Dibuja una estrella de 5 puntas"""
        puntos = []
        for i in range(10):
            angulo = i * 3.14159 * 2 / 10 - 3.14159 / 2
            r = radio if i % 2 == 0 else radio / 2
            x = cx + r * pygame.math.Vector2(1, 0).rotate_rad(angulo).x
            y = cy + r * pygame.math.Vector2(0, 1).rotate_rad(angulo).y
            puntos.append((x, y))
        pygame.draw.polygon(pantalla, color, puntos)
    
    @staticmethod
    def dibujar_cara_triste(pantalla, centro_x, centro_y, radio=60):
        """Dibuja una cara triste (para respuestas incorrectas)"""
        # Círculo amarillo de la cara
        pygame.draw.circle(pantalla, (255, 193, 7), (centro_x, centro_y), radio)
        pygame.draw.circle(pantalla, NEGRO, (centro_x, centro_y), radio, 3)

        # Ojos tristes (círculos negros)
        pygame.draw.circle(pantalla, NEGRO, (centro_x - 20, centro_y - 15), 8)
        pygame.draw.circle(pantalla, NEGRO, (centro_x + 20, centro_y - 15), 8)

        # Boca triste (arco invertido)
        pygame.draw.arc(pantalla, NEGRO, 
                    (centro_x - 25, centro_y + 15, 50, 30), 
                    0, 3.14, 4)
    
    @staticmethod
    def dibujar_overlay_victoria(pantalla, particulas_confeti):
        """Dibuja el overlay verde con confeti para respuesta correcta"""
        # PANTALLA VERDE CON TRANSPARENCIA
        overlay_resultado = pygame.Surface((ANCHO, ALTO))
        overlay_resultado.set_alpha(180)
        overlay_resultado.fill((46, 204, 113))  # Verde brillante
        pantalla.blit(overlay_resultado, (0, 0))

        # MENSAJE CORRECTO CON SOMBRA
        fuente_grande = pygame.font.Font(None, 100)
        texto = fuente_grande.render("¡CORRECTO!", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO//2, ALTO//2))

        # Sombra oscura
        texto_sombra = fuente_grande.render("¡CORRECTO!", True, (0, 100, 0))
        pantalla.blit(texto_sombra, (texto_rect.x + 4, texto_rect.y + 4))
        pantalla.blit(texto, texto_rect)

        # CONFETI
        EfectosVisuales.actualizar_confeti(particulas_confeti, pantalla)
    
    @staticmethod
    def dibujar_overlay_derrota(pantalla):
        """Dibuja el overlay rojo con cara triste para respuesta incorrecta"""
        # PANTALLA ROJA CON TRANSPARENCIA
        overlay_resultado = pygame.Surface((ANCHO, ALTO))
        overlay_resultado.set_alpha(180)
        overlay_resultado.fill((231, 76, 60))  # Rojo brillante
        pantalla.blit(overlay_resultado, (0, 0))

        # MENSAJE INCORRECTO CON SOMBRA
        fuente_grande = pygame.font.Font(None, 100)
        texto = fuente_grande.render("INCORRECTO", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO//2, ALTO//2))

        # Sombra oscura
        texto_sombra = fuente_grande.render("INCORRECTO", True, (100, 0, 0))
        pantalla.blit(texto_sombra, (texto_rect.x + 4, texto_rect.y + 4))
        pantalla.blit(texto, texto_rect)

        # CARA TRISTE DIBUJADA
        centro_x, centro_y = ANCHO//2, ALTO//2 + 120
        EfectosVisuales.dibujar_cara_triste(pantalla, centro_x, centro_y)