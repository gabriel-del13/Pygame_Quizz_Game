# tablero.py - Gestión del tablero y casillas CON BIFURCACIONES

import pygame
from config import *

class Casilla:
    def __init__(self, x, y, id_casilla, numero_display, color, siguientes=None, tiene_pregunta=True):
        self.x = x
        self.y = y
        self.id = id_casilla
        self.numero = numero_display
        self.color = color
        self.completada = False
        self.resultado = None  # Puede ser "acierto" o "fallo"
        self.es_final = (id_casilla == "META")
        self.tiene_pregunta = tiene_pregunta  
        self.siguientes = siguientes if siguientes else []
        
    def contiene_personaje(self, px, py):
        return (px >= self.x and px <= self.x + TAMANO_CASILLA and
                py >= self.y and py <= self.y + TAMANO_CASILLA)
        
    def dibujar(self, pantalla, offset_x, offset_y):
        screen_x = int(self.x - offset_x)
        screen_y = int(self.y - offset_y)
        
        # --- LÓGICA DE COLORES CORREGIDA ---
        if self.completada:
            if self.resultado == "acierto":
                color_fondo = VERDE  # ¡Se pone VERDE si acertaste!
            elif self.resultado == "fallo":
                color_fondo = ROJO   # ¡Se pone ROJO si fallaste!
            else:
                color_fondo = GRIS   # Por seguridad
        elif self.es_final:
            color_fondo = DORADO
        else:
            color_fondo = self.color
        
        # Dibujar casilla
        rect = pygame.Rect(screen_x, screen_y, TAMANO_CASILLA, TAMANO_CASILLA)
        pygame.draw.rect(pantalla, color_fondo, rect)
        pygame.draw.rect(pantalla, NEGRO, rect, 3)
        
        # Número
        fuente = pygame.font.Font(None, 50)
        color_texto = BLANCO if self.color == MARRON_OSCURO else NEGRO
        
        # Si está completada (Verde/Rojo) o es Meta, texto negro se lee mejor
        if self.completada or self.es_final:
            color_texto = NEGRO
            
        texto = fuente.render(str(self.numero), True, color_texto)
        texto_rect = texto.get_rect(center=(screen_x + TAMANO_CASILLA//2, 
                                            screen_y + TAMANO_CASILLA//2))
        pantalla.blit(texto, texto_rect)
        
        # Marca visual de estado
        if self.completada:
            fuente_check = pygame.font.Font(None, 60)
            if self.resultado == "acierto":
                # Check para acierto
                check = fuente_check.render("OK", True, NEGRO) 
            else:
                # X para fallo
                check = fuente_check.render("X", True, NEGRO)
            
            check_rect = check.get_rect(center=(screen_x + TAMANO_CASILLA//2, 
                                                screen_y + 25))
            pantalla.blit(check, check_rect)
        
        # Etiqueta META
        if self.es_final:
            fuente_meta = pygame.font.Font(None, 28)
            meta = fuente_meta.render("META", True, NEGRO)
            meta_rect = meta.get_rect(center=(screen_x + TAMANO_CASILLA//2, 
                                             screen_y + 95))
            pantalla.blit(meta, meta_rect)

class Tablero:
    def __init__(self):
        self.casillas = self.crear_tablero_con_bifurcaciones()
        self.casillas_dict = {c.id: c for c in self.casillas}
    
    def crear_tablero_con_bifurcaciones(self):
        # (Tu código de creación de tablero estaba perfecto, no cambia nada aquí)
        # ... Mantén el código original de esta función ...
        # Solo copio el inicio para contexto, usa tu función original
        casillas = []
        x_base = 330
        y_base = 1400
        
        # Definir columnas
        x_izq = x_base
        x_centro = x_base + TAMANO_CASILLA
        x_der = x_base + TAMANO_CASILLA * 2
        x_extra_izq = x_base - TAMANO_CASILLA 
        
        filas = {}
        for i in range(15):
            filas[i] = y_base - (TAMANO_CASILLA * i)
        
        # ============ CAMINO PRINCIPAL ============
        
        # Casilla 1 (inicio)
        casillas.append(Casilla(x_izq, filas[0], "1", "1", MARRON_CLARO, siguientes=["2"], tiene_pregunta=True))
        print(f"Casilla 1: x={x_izq}, y={filas[0]} -> siguiente: 2")
        
        # Casilla 2
        casillas.append(Casilla(x_izq, filas[1], "2", "2", MARRON_OSCURO, siguientes=["3"], tiene_pregunta=True))
        print(f"Casilla 2: x={x_izq}, y={filas[1]} -> siguiente: 3")
        
        # Casilla 3 (BIFURCACIÓN: puede ir a 4 o a 3.1)
        casillas.append(Casilla(x_izq, filas[2], "3", "3", MARRON_CLARO, siguientes=["4", "3.1"], tiene_pregunta=True))
        print(f"Casilla 3: x={x_izq}, y={filas[2]} -> siguientes: 4 (derecha) o 3.1 (izquierda alternativo)")
        
        # ============ CAMINO ALTERNATIVO (desde 3) ============
        
        # Casilla 3.1 (camino alternativo - izquierda de la 3)
        casillas.append(Casilla(x_extra_izq, filas[2], "3.1", "3.1", AZUL, siguientes=["3.2"], tiene_pregunta=True))
        print(f"Casilla 3.1 (ALT): x={x_extra_izq}, y={filas[2]} -> siguiente: 3.2")
        
        # Casilla 3.2 (sube)
        casillas.append(Casilla(x_extra_izq, filas[3], "3.2", "3.2", AZUL, siguientes=["3.3"], tiene_pregunta=True))
        print(f"Casilla 3.2 (ALT): x={x_extra_izq}, y={filas[3]} -> siguiente: 3.3")
        
        # Casilla 3.3 (sube más y se une al 9)
        casillas.append(Casilla(x_extra_izq, filas[4], "3.3", "3.3", AZUL, siguientes=["9"], tiene_pregunta=True))
        print(f"Casilla 3.3 (ALT): x={x_extra_izq}, y={filas[4]} -> siguiente: 9")
        
        # ============ CONTINUACIÓN CAMINO PRINCIPAL ============
        
        # Casilla 4 (desde 3, camino principal)
        casillas.append(Casilla(x_centro, filas[2], "4", "4", MARRON_OSCURO, siguientes=["5"], tiene_pregunta=True))
        print(f"Casilla 4: x={x_centro}, y={filas[2]} -> siguiente: 5")
        
        # Casilla 5
        casillas.append(Casilla(x_der, filas[2], "5", "5", MARRON_CLARO, siguientes=["6"], tiene_pregunta=True))
        print(f"Casilla 5: x={x_der}, y={filas[2]} -> siguiente: 6")
        
        # Casilla 6
        casillas.append(Casilla(x_der, filas[3], "6", "6", MARRON_OSCURO, siguientes=["7"], tiene_pregunta=True))
        print(f"Casilla 6: x={x_der}, y={filas[3]} -> siguiente: 7")
        
        # Casilla 7
        casillas.append(Casilla(x_der, filas[4], "7", "7", MARRON_CLARO, siguientes=["8"], tiene_pregunta=True))
        print(f"Casilla 7: x={x_der}, y={filas[4]} -> siguiente: 8")
        
        # Casilla 8
        casillas.append(Casilla(x_centro, filas[4], "8", "8", MARRON_OSCURO, siguientes=["9"], tiene_pregunta=True))
        print(f"Casilla 8: x={x_centro}, y={filas[4]} -> siguiente: 9")
        
        # Casilla 9 (UNIÓN: aquí llegan tanto el camino principal como el alternativo)
        casillas.append(Casilla(x_izq, filas[4], "9", "9", MARRON_CLARO, siguientes=["10"], tiene_pregunta=True))
        print(f"Casilla 9 (UNIÓN): x={x_izq}, y={filas[4]} -> siguiente: 10")
        
        # Casilla 10
        casillas.append(Casilla(x_izq, filas[5], "10", "10", MARRON_OSCURO, siguientes=["META"], tiene_pregunta=True))
        print(f"Casilla 10: x={x_izq}, y={filas[5]} -> siguiente: META")
        
        # Casilla META
        casillas.append(Casilla(x_izq, filas[6], "META", "META", DORADO, siguientes=[], tiene_pregunta=False))
        print(f"Casilla META (SOLO DECORATIVA): x={x_izq}, y={filas[6]} -> FIN")
        
        print("==========================================\n")
        
        return casillas
    
    def obtener_casilla_por_id(self, id_casilla):
        """Obtiene una casilla por su ID"""
        return self.casillas_dict.get(id_casilla)
    
    def dibujar(self, pantalla, offset_x, offset_y):
        """Dibuja todas las casillas"""
        for casilla in self.casillas:
            casilla.dibujar(pantalla, offset_x, offset_y)