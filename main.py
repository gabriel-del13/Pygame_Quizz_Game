# main.py - Archivo principal del juego CON BIFURCACIONES (REFACTORIZADO)

import pygame #type:ignore
import sys
from config import *
from personaje import Personaje
from tablero import Tablero
from preguntas import obtener_pregunta
from camara_ui import Camara, UI
from background import Fondo
from pantalla_pregunta import PantallaPregunta
from pantalla_eleccion import PantallaEleccion
from pantallas_finales import PantallaVictoria, PantallaGameOver


class Juego:
    """Clase principal que gestiona el flujo del juego"""
    
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("La Gran Aventura Carriazo")
        self.reloj = pygame.time.Clock()
        
        # Variables del juego
        self.vidas = 3
        self.estado = "jugando"  # Estados: jugando, pregunta, eligiendo_camino, ganado, perdido
        self.casilla_actual_id = "1"
        
        # Componentes principales del juego
        self.tablero = Tablero()
        self.camara = Camara()
        self.fondo = Fondo()
        
        # Crear personaje en la casilla inicial
        casilla_inicio = self.tablero.obtener_casilla_por_id("1")
        self.personaje = Personaje(
            casilla_inicio.x + TAMANO_CASILLA // 2,
            casilla_inicio.y + TAMANO_CASILLA // 2
        )
        
        # Pantallas del juego
        self.pantalla_pregunta = PantallaPregunta()
        self.pantalla_eleccion = PantallaEleccion()
        self.pantalla_victoria = PantallaVictoria()
        self.pantalla_game_over = PantallaGameOver()
    
    def mostrar_pregunta(self):
        """Cambia el estado a pregunta y configura la pregunta actual"""
        casilla_actual = self.tablero.obtener_casilla_por_id(self.casilla_actual_id)
        # Solo mostrar pregunta si la casilla tiene pregunta
        if casilla_actual.tiene_pregunta:
            self.estado = "pregunta"
            pregunta = obtener_pregunta(self.casilla_actual_id)
            self.pantalla_pregunta.configurar_pregunta(pregunta)
        else:
            # Si llegamos a META (sin pregunta), ya ganamos
            if self.casilla_actual_id == "META":
                self.estado = "ganado"
    
    def verificar_respuesta(self, indice):
        """Verifica si la respuesta es correcta y actualiza el estado del juego"""
        casilla_actual = self.tablero.obtener_casilla_por_id(self.casilla_actual_id)
        casilla_actual.completada = True
        
        # Verificar respuesta
        es_correcta = self.pantalla_pregunta.verificar_respuesta(indice)
        
        if es_correcta:
            # --- RESPUESTA CORRECTA ---
            casilla_actual.resultado = "acierto"  # Marcamos casilla como verde
            
        else:
            # --- RESPUESTA INCORRECTA ---
            casilla_actual.resultado = "fallo"  # Marcamos casilla como roja
            self.vidas -= 1
            
            # SOLO PERDER SI TE QUEDASTE SIN VIDAS
            if self.vidas <= 0:
                self.estado = "perdido"
    
    def avanzar_a_casilla(self, id_destino):
        """Mueve el personaje a la casilla de destino"""
        self.casilla_actual_id = id_destino
        casilla_destino = self.tablero.obtener_casilla_por_id(id_destino)
        
        # Actualizar posición del personaje
        self.personaje.x = casilla_destino.x + TAMANO_CASILLA // 2
        self.personaje.y = casilla_destino.y + TAMANO_CASILLA // 2
    
    def manejar_continuacion_pregunta(self):
        """Maneja la lógica después de que el mensaje de feedback termine"""
        casilla_actual = self.tablero.obtener_casilla_por_id(self.casilla_actual_id)
        
        # Si ya perdimos (sin vidas), no hacer nada más
        if self.estado == "perdido":
            return
        
        # Verificar si hay bifurcación
        if len(casilla_actual.siguientes) > 1:
            self.estado = "eligiendo_camino"
            self.pantalla_eleccion.configurar_opciones(casilla_actual.siguientes)
        elif len(casilla_actual.siguientes) == 1:
            # Avanzar automáticamente a la siguiente casilla
            siguiente_id = casilla_actual.siguientes[0]
            self.avanzar_a_casilla(siguiente_id)
            
            # Si la siguiente casilla es META, ganamos
            if siguiente_id == "META":
                self.estado = "ganado"
            else:
                self.estado = "jugando"
        else:
            # No hay más casillas (fin del camino)
            self.estado = "jugando"
        
        # Limpiar pantalla de pregunta
        self.pantalla_pregunta.reset()
    
    def dibujar_mundo(self):
        """Dibuja el mundo del juego (tablero, personaje, UI)"""
        self.pantalla.fill((34, 139, 34))
        self.camara.actualizar(self.personaje.x, self.personaje.y)
        self.fondo.dibujar(self.pantalla, self.camara.offset_x, self.camara.offset_y)
        self.tablero.dibujar(self.pantalla, self.camara.offset_x, self.camara.offset_y)
        self.personaje.dibujar(self.pantalla, self.camara.offset_x, self.camara.offset_y)
        
        # Panel superior con vidas
        UI.dibujar_panel_superior(self.pantalla, self.vidas, self.casilla_actual_id)
        
        # Mensaje en panel inferior
        casilla_actual = self.tablero.obtener_casilla_por_id(self.casilla_actual_id)
        if casilla_actual.contiene_personaje(self.personaje.x, self.personaje.y):
            if not casilla_actual.completada:
                mensaje = "Presiona ESPACIO para responder la pregunta"
            else:
                mensaje = "Casilla completada - Avanza a la siguiente"
        else:
            mensaje = "Usa WASD o Flechas para moverte"
        
        UI.dibujar_panel_inferior(self.pantalla, mensaje)
    
    def reiniciar(self):
        """Reinicia el juego al estado inicial"""
        self.vidas = 3
        self.estado = "jugando"
        self.casilla_actual_id = "1"
        
        # Resetear todas las casillas
        for casilla in self.tablero.casillas:
            casilla.completada = False
            casilla.resultado = None
        
        # Reiniciar personaje
        casilla_inicio = self.tablero.obtener_casilla_por_id("1")
        self.personaje = Personaje(
            casilla_inicio.x + TAMANO_CASILLA // 2,
            casilla_inicio.y + TAMANO_CASILLA // 2
        )
        
        # Resetear pantallas
        self.pantalla_pregunta.reset()
        self.pantalla_eleccion.reset()
        self.pantalla_victoria.reset()
    
    def manejar_eventos(self, evento, mouse_pos, boton_reinicio):
        """Maneja todos los eventos del juego"""
        if evento.type == pygame.QUIT:
            return False  # Señal para cerrar el juego
        
        if evento.type == pygame.KEYDOWN:
            # Presionar ESPACIO en modo jugando para responder pregunta
            if self.estado == "jugando" and evento.key == pygame.K_SPACE:
                casilla_actual = self.tablero.obtener_casilla_por_id(self.casilla_actual_id)
                if (casilla_actual.contiene_personaje(self.personaje.x, self.personaje.y) 
                    and not casilla_actual.completada):
                    self.mostrar_pregunta()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Click en botones de respuesta
            if self.estado == "pregunta" and not self.pantalla_pregunta.respuesta_correcta_mostrada:
                for i, boton in enumerate(self.pantalla_pregunta.botones_respuesta):
                    if boton.click(mouse_pos):
                        self.verificar_respuesta(i)
            
            # Click en botones de elección de camino
            elif self.estado == "eligiendo_camino":
                id_destino = self.pantalla_eleccion.manejar_click(mouse_pos)
                if id_destino:
                    self.avanzar_a_casilla(id_destino)
                    self.estado = "jugando"
            
            # Click en botón de reinicio (pantallas finales)
            elif self.estado in ["ganado", "perdido"]:
                if boton_reinicio and boton_reinicio.click(mouse_pos):
                    self.reiniciar()
        
        return True  # Continuar ejecutando
    
    def actualizar(self, teclas, mouse_pos):
        self.fondo.tiempo_rio += 0.02  # Incrementar el tiempo para animar el río
        self.fondo.actualizar_rio()  # Actualizar animación del río
        """Actualiza la lógica del juego según el estado actual"""
        if self.estado == "jugando":
            # Mover personaje
            self.personaje.mover(teclas, self.tablero.casillas)
        
        elif self.estado == "pregunta":
            # Actualizar hover de botones
            for boton in self.pantalla_pregunta.botones_respuesta:
                boton.actualizar_hover(mouse_pos)
            
            # Verificar si debe continuar después del mensaje de feedback
            if self.pantalla_pregunta.debe_continuar():
                self.manejar_continuacion_pregunta()
        
        elif self.estado == "eligiendo_camino":
            # Actualizar hover de botones de camino
            self.pantalla_eleccion.actualizar_hover(mouse_pos)
    
    def dibujar(self, mouse_pos):
        """Dibuja todo el juego según el estado actual"""
        # Dibujar mundo base
        self.dibujar_mundo()
        
        # Dibujar overlay según estado
        if self.estado == "pregunta":
            self.pantalla_pregunta.dibujar(self.pantalla, self.casilla_actual_id)
        
        elif self.estado == "eligiendo_camino":
            self.pantalla_eleccion.dibujar(self.pantalla)
        
        elif self.estado == "ganado":
            boton = self.pantalla_victoria.dibujar(self.pantalla, self.vidas)
            if boton:
                boton.actualizar_hover(mouse_pos)
            return boton
        
        elif self.estado == "perdido":
            boton = self.pantalla_game_over.dibujar(self.pantalla, self.vidas)
            if boton:
                boton.actualizar_hover(mouse_pos)
            return boton
        
        return None
    
    def ejecutar(self):
        """Loop principal del juego"""
        ejecutando = True
        boton_reinicio = None
        
        while ejecutando:
            self.reloj.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            teclas = pygame.key.get_pressed()
            
            # Manejar eventos
            for evento in pygame.event.get():
                if not self.manejar_eventos(evento, mouse_pos, boton_reinicio):
                    ejecutando = False
            
            # Actualizar lógica
            self.actualizar(teclas, mouse_pos)
            
            # Dibujar todo
            boton_reinicio = self.dibujar(mouse_pos)
            
            # Actualizar pantalla
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()