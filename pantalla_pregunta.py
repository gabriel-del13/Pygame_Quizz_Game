# pantalla_pregunta.py - Gestión de la pantalla de preguntas

import pygame
from config import *
from camara_ui import Boton
from efectos_visuales import EfectosVisuales

class PantallaPregunta:
    """Gestiona la pantalla de preguntas y respuestas"""
    
    def __init__(self):
        self.pregunta_actual = None
        self.botones_respuesta = []
        self.respuesta_correcta_mostrada = False
        self.tiempo_mensaje = 0
        self.particulas_confeti = []
        self.confeti_generado = False
        self.ultimo_resultado_fue_correcto = False
    
    def configurar_pregunta(self, pregunta):
        """Configura una nueva pregunta con sus botones de respuesta"""
        self.pregunta_actual = pregunta
        self.respuesta_correcta_mostrada = False
        self.confeti_generado = False
        
        self.botones_respuesta = []
        y_inicial = 320
        for i, opcion in enumerate(pregunta["opciones"]):
            boton = Boton(ANCHO//2 - 250, y_inicial + i * 65, 500, 50, 
                          opcion, AZUL)
            self.botones_respuesta.append(boton)
    
    def verificar_respuesta(self, indice):
        """Verifica si la respuesta seleccionada es correcta"""
        self.respuesta_correcta_mostrada = True
        self.tiempo_mensaje = pygame.time.get_ticks()
        
        if indice == self.pregunta_actual["correcta"]:
            self.ultimo_resultado_fue_correcto = True
            return True  # Respuesta correcta
        else:
            self.ultimo_resultado_fue_correcto = False
            return False  # Respuesta incorrecta
    
    def dibujar(self, pantalla, casilla_id):
        """Dibuja la pantalla de pregunta completa"""
        # Fondo y panel
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(245)
        overlay.fill(GRIS_OSCURO)
        pantalla.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(40, 80, ANCHO - 80, ALTO - 130)
        pygame.draw.rect(pantalla, (44, 62, 80), panel_rect, border_radius=15)
        pygame.draw.rect(pantalla, AMARILLO, panel_rect, 5, border_radius=15)

        # Título
        es_final = casilla_id == "META"
        titulo_texto = "PREGUNTA FINAL" if es_final else f"Pregunta Casilla {casilla_id}"

        fuente_titulo = pygame.font.Font(None, 42)
        titulo = fuente_titulo.render(titulo_texto, True, DORADO if es_final else VERDE)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 110))

        # Pregunta (Renderizado de texto multilinea)
        self._dibujar_pregunta_multilinea(pantalla)

        # Botones de respuesta
        for boton in self.botones_respuesta:
            boton.dibujar(pantalla)

        # Efectos visuales de feedback
        self._dibujar_efectos_feedback(pantalla)
    
    def _dibujar_pregunta_multilinea(self, pantalla):
        """Dibuja la pregunta dividida en múltiples líneas"""
        fuente_pregunta = pygame.font.Font(None, 32)
        pregunta = self.pregunta_actual["pregunta"]
        palabras = pregunta.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = linea_actual + palabra + " "
            if fuente_pregunta.size(prueba)[0] < ANCHO - 180:
                linea_actual = prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra + " "
        if linea_actual:
            lineas.append(linea_actual)

        y_pregunta = 180
        for linea in lineas:
            texto = fuente_pregunta.render(linea, True, BLANCO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, y_pregunta))
            y_pregunta += 38
    
    def _dibujar_efectos_feedback(self, pantalla):
        """Dibuja los efectos visuales después de responder"""
        if not self.respuesta_correcta_mostrada:
            return
        
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_mensaje < 1500:
            if self.ultimo_resultado_fue_correcto:
                # ===== RESPUESTA CORRECTA =====
                # Generar confeti si no se ha generado aún
                if not self.confeti_generado:
                    self.particulas_confeti = EfectosVisuales.generar_confeti(100)
                    self.confeti_generado = True
                
                # Dibujar overlay de victoria con confeti
                EfectosVisuales.dibujar_overlay_victoria(pantalla, self.particulas_confeti)
            else:
                # ===== RESPUESTA INCORRECTA =====
                EfectosVisuales.dibujar_overlay_derrota(pantalla)
    
    def debe_continuar(self):
        """Verifica si ha pasado el tiempo del mensaje de feedback"""
        if not self.respuesta_correcta_mostrada:
            return False
        
        tiempo_actual = pygame.time.get_ticks()
        return tiempo_actual - self.tiempo_mensaje >= 1500
    
    def reset(self):
        """Reinicia el estado de la pantalla de pregunta"""
        self.pregunta_actual = None
        self.botones_respuesta = []
        self.respuesta_correcta_mostrada = False
        self.confeti_generado = False