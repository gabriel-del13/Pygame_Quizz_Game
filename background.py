import pygame
import random
import math
from config import *

class Fondo:
    def __init__(self):
        self.ancho_mundo = ANCHO + 400
        self.alto_mundo = 5000
        self.superficie = pygame.Surface((self.ancho_mundo, self.alto_mundo))
        random.seed(42)
        self.tiempo_rio = 0
        self._generar_puntos_rio() 
        self.generar_mundo()

    def generar_mundo(self):
        # 1. Base de pasto
        self.superficie.fill((34, 139, 34))

        # Textura de pasto (puntitos variados)
        for _ in range(8000):
            x = random.randint(0, self.ancho_mundo)
            y = random.randint(0, self.alto_mundo)
            r = random.randint(32, 48)
            g = random.randint(110, 160)
            b = random.randint(20, 45)
            size = random.randint(1, 4)
            pygame.draw.rect(self.superficie, (r, g, b), (x, y, size, size))

        # Precalcular río
        self._generar_puntos_rio()

        # --- CIELO (Y: 0 a 880) — degradado azul ---
        for y in range(0, 880):
            t = y / 880.0
            cr = int(100 + t * 35)
            cg = int(170 + t * 40)
            cb = int(255 - t * 30)
            pygame.draw.rect(self.superficie, (cr, cg, cb), (0, y, self.ancho_mundo, 1))

        # Nubes
        self.dibujar_nubes()

        # Sol (detrás de las montañas)
        centro_x = self.ancho_mundo // 2
        self.dibujar_sol_epico(centro_x, 560)

        # Montañas: TODAS ANCLADAS AL SUELO (bases llegan a Y~860-900)
        # Capa trasera (oscuras, picos altos, bases al suelo)
        for i in range(10):
            x = (self.ancho_mundo // 10) * i + random.randint(-30, 30)
            alto = random.randint(300, 400)
            pico_y = random.randint(860 - alto, 900 - alto)
            self.dibujar_montana(x, pico_y, random.randint(200, 300), alto, (50, 50, 58), True)

        # Capa frontal (más claras, algo más bajas, también ancladas)
        for i in range(8):
            x = (self.ancho_mundo // 8) * i + random.randint(-25, 25)
            alto = random.randint(200, 300)
            pico_y = random.randint(870 - alto, 920 - alto)
            self.dibujar_montana(x, pico_y, random.randint(230, 350), alto, (95, 95, 110), True)

        # Transición orgánica montaña → pasto (borde ondulado, no lineal)
        for x_pos in range(0, self.ancho_mundo, 3):
            wave = (math.sin(x_pos * 0.007) * 35 +
                    math.sin(x_pos * 0.023 + 1.5) * 18 +
                    math.sin(x_pos * 0.05 + 0.7) * 8)
            y_borde = int(860 + wave)
            alto_col = 960 - y_borde
            if alto_col > 0:
                pygame.draw.rect(self.superficie, (34, 139, 34), (x_pos, y_borde, 3, alto_col))
        # Textura de pasto sobre el borde ondulado
        for _ in range(500):
            x = random.randint(0, self.ancho_mundo)
            wave = (math.sin(x * 0.007) * 35 +
                    math.sin(x * 0.023 + 1.5) * 18 +
                    math.sin(x * 0.05 + 0.7) * 8)
            y_borde = int(860 + wave)
            y = random.randint(y_borde - 8, y_borde + 35)
            cr = random.randint(28, 50)
            cg = random.randint(110, 155)
            cb = random.randint(20, 45)
            pygame.draw.rect(self.superficie, (cr, cg, cb), (x, y, random.randint(2, 5), random.randint(2, 5)))
        # Arbustos pequeños en la transición
        for _ in range(50):
            x = random.randint(0, self.ancho_mundo)
            wave = (math.sin(x * 0.007) * 35 +
                    math.sin(x * 0.023 + 1.5) * 18 +
                    math.sin(x * 0.05 + 0.7) * 8)
            y_borde = int(860 + wave)
            y = random.randint(y_borde - 10, y_borde + 20)
            self.dibujar_arbol(x, y, random.choice([0, 1, 2]), random.uniform(0.35, 0.65))

        # --- RÍO (se dibuja ANTES que los árboles) ---
        self.dibujar_rio_epico()

        # --- ÁRBOLES (se dibujan ENCIMA del río) ---
        # Bosque denso cerca del río (ambas orillas)
        for _ in range(400):
            x = random.randint(0, self.ancho_mundo)
            y_rio = self._y_rio(x)
            lado = random.choice([-1, 1])
            dist = random.randint(60, 220)
            y = int(y_rio) + lado * dist
            if 820 < y < self.alto_mundo:
                tipo = random.choices([0, 1, 2], weights=[0.4, 0.35, 0.25])[0]
                escala = random.uniform(0.7, 1.3)
                self.dibujar_arbol(x, y, tipo, escala)

        # Árboles dispersos zona media
        for _ in range(120):
            x = random.randint(0, self.ancho_mundo)
            y = random.randint(900, 1400)
            y_rio = self._y_rio(x)
            if abs(y - y_rio) > 180:
                tipo = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2])[0]
                escala = random.uniform(0.6, 1.1)
                self.dibujar_arbol(x, y, tipo, escala)

        # Árboles densos zona inferior
        for _ in range(350):
            x = random.randint(0, self.ancho_mundo)
            y = random.randint(1400, self.alto_mundo)
            tipo = random.choices([0, 1, 2], weights=[0.35, 0.4, 0.25])[0]
            escala = random.uniform(0.8, 1.4)
            self.dibujar_arbol(x, y, tipo, escala)

        # Árboles extra en zona de inicio (parte más baja del mapa)
        for _ in range(250):
            x = random.randint(0, self.ancho_mundo)
            y = random.randint(3500, self.alto_mundo)
            tipo = random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
            escala = random.uniform(0.9, 1.5)
            self.dibujar_arbol(x, y, tipo, escala)

    # -------------------------------------------------------
    #  NUBES
    # -------------------------------------------------------
    def dibujar_nubes(self):
        random.seed(77)
        for _ in range(12):
            cx = random.randint(50, self.ancho_mundo - 50)
            cy = random.randint(420, 750)
            n_bolas = random.randint(4, 7)
            for j in range(n_bolas):
                ox = cx + random.randint(-50, 50)
                oy = cy + random.randint(-15, 15)
                r = random.randint(20, 40)
                # Sombra
                pygame.draw.circle(self.superficie, (180, 200, 220), (ox + 3, oy + 4), r)
                # Nube blanca
                pygame.draw.circle(self.superficie, (240, 245, 255), (ox, oy), r)
            # Brillo superior
            pygame.draw.circle(self.superficie, (255, 255, 255), (cx - 10, cy - 10), random.randint(12, 22))

    # -------------------------------------------------------
    #  Puntos del río
    # -------------------------------------------------------
    def _generar_puntos_rio(self):
        self._puntos_rio_cache = []
        y_base = 1200
        frec1 = 0.008
        amp1 = 110
        frec2 = 0.022
        amp2 = 35
        for x in range(0, self.ancho_mundo, 8):
            y = y_base + math.sin(x * frec1) * amp1 + math.sin(x * frec2 + 1.2) * amp2
            self._puntos_rio_cache.append((x, y))

    def _y_rio(self, x):
        y_base = 1200
        frec1 = 0.008
        amp1 = 110
        frec2 = 0.022
        amp2 = 35
        return y_base + math.sin(x * frec1) * amp1 + math.sin(x * frec2 + 1.2) * amp2

    # -------------------------------------------------------
    #  RÍO
    # -------------------------------------------------------
    def dibujar_rio_epico(self):
        puntos = self._puntos_rio_cache
        ancho_rio = 140

        # Lodo / orilla oscura
        for x, y in puntos:
            pygame.draw.circle(self.superficie, (110, 88, 55), (int(x), int(y)), ancho_rio // 2 + 25)

        # Arena / orilla clara
        for x, y in puntos:
            pygame.draw.circle(self.superficie, (180, 160, 100), (int(x), int(y)), ancho_rio // 2 + 15)

        # Piedras en la orilla
        random.seed(7)
        for x, y in puntos[::5]:
            for _ in range(2):
                ox = int(x) + random.randint(-(ancho_rio // 2 + 14), ancho_rio // 2 + 14)
                oy = int(y) + random.randint(-10, 10)
                if random.random() < 0.35:
                    shade = random.randint(130, 180)
                    r = random.randint(3, 7)
                    pygame.draw.circle(self.superficie, (shade, shade - 10, shade - 20), (ox, oy), r)

        # Plantas acuáticas en la orilla
        random.seed(13)
        for x, y in puntos[::12]:
            for _ in range(3):
                ox = int(x) + random.randint(-(ancho_rio // 2 + 12), ancho_rio // 2 + 12)
                oy = int(y) + random.randint(-8, 8)
                if random.random() < 0.5:
                    pygame.draw.circle(self.superficie, (20, 90, 40), (ox, oy), random.randint(3, 6))

        # Agua profunda
        for x, y in puntos:
            pygame.draw.circle(self.superficie, (15, 70, 120), (int(x), int(y)), ancho_rio // 2)

        # Agua (azul medio)
        for x, y in puntos:
            pygame.draw.circle(self.superficie, (30, 110, 170), (int(x), int(y)), ancho_rio // 2 - 12)

        # Corrientes (líneas ondulantes)
        random.seed(99)
        for offset_y in [-30, -10, 10, 30]:
            corriente = []
            for x, y in puntos[::3]:
                # Agregar tiempo_rio para animar
                jitter = math.sin(x * 0.04 + offset_y + self.tiempo_rio * 2) * 8
                corriente.append((int(x), int(y) + offset_y + int(jitter)))
            if len(corriente) > 1:
                pygame.draw.lines(self.superficie, (60, 150, 210), False, corriente, 2)

        # Brillos en el agua
        random.seed(55)
        for x, y in puntos[::4]:
            if random.random() < 0.4:
                bx = int(x) + random.randint(-40, 40)
                by = int(y) + random.randint(-40, 40)
                pygame.draw.circle(self.superficie, (160, 220, 255), (bx, by), random.randint(2, 5))

        # Rocas dentro del río
        random.seed(22)
        for x, y in puntos[::8]:
            if random.random() < 0.25:
                rx = int(x) + random.randint(-35, 35)
                ry = int(y) + random.randint(-35, 35)
                r = random.randint(5, 12)
                pygame.draw.circle(self.superficie, (80, 80, 90), (rx, ry), r)
                pygame.draw.circle(self.superficie, (110, 110, 120), (rx - 2, ry - 2), r // 2)

    def actualizar_rio(self):
        """Redibuja solo el río con la animación actualizada"""
        self._generar_puntos_rio()
        self.dibujar_rio_epico()
    # -------------------------------------------------------
    #  ÁRBOLES (3 tipos: pino, roble, sauce)
    # -------------------------------------------------------
    def dibujar_arbol(self, x, y, tipo=0, escala=1.0):
        s = escala
        if tipo == 0:
            self._arbol_pino(x, y, s)
        elif tipo == 1:
            self._arbol_roble(x, y, s)
        else:
            self._arbol_sauce(x, y, s)

    def _arbol_pino(self, x, y, s):
        """Pino: estrella puntiaguda, verde oscuro."""
        r_sombra = int(20 * s)
        pygame.draw.circle(self.superficie, (15, 45, 15), (x + 4, y + 5), r_sombra)
        color_base = (25, 100, 30)
        color_claro = (40, 130, 45)
        color_oscuro = (15, 70, 20)
        r_ext = int(22 * s)
        r_int = int(10 * s)
        puntos_estrella = []
        for i in range(12):
            angulo = math.radians(i * 30 - 90)
            r = r_ext if i % 2 == 0 else r_int
            puntos_estrella.append((x + int(math.cos(angulo) * r),
                                    y + int(math.sin(angulo) * r)))
        pygame.draw.polygon(self.superficie, color_base, puntos_estrella)
        puntos_sombra = [(x + int(math.cos(math.radians(i * 30 - 90)) * (r_ext if i % 2 == 0 else r_int) * 0.7),
                          y + int(math.sin(math.radians(i * 30 - 90)) * (r_ext if i % 2 == 0 else r_int) * 0.7))
                         for i in range(6, 12)]
        pygame.draw.polygon(self.superficie, color_oscuro, puntos_sombra)
        pygame.draw.circle(self.superficie, color_claro, (x - int(4 * s), y - int(4 * s)), int(5 * s))

    def _arbol_roble(self, x, y, s):
        """Roble: copa redonda y exuberante, verde medio."""
        r_sombra = int(28 * s)
        pygame.draw.circle(self.superficie, (15, 45, 15), (x + 5, y + 6), r_sombra)
        r = int(26 * s)
        pygame.draw.circle(self.superficie, (40, 120, 35), (x, y), r)
        for ang in range(0, 360, 45):
            ox = int(math.cos(math.radians(ang)) * r * 0.55)
            oy = int(math.sin(math.radians(ang)) * r * 0.55)
            pygame.draw.circle(self.superficie, (30, 100, 25), (x + ox, y + oy), int(10 * s))
        pygame.draw.circle(self.superficie, (70, 180, 50), (x - int(7 * s), y - int(7 * s)), int(10 * s))
        pygame.draw.circle(self.superficie, (90, 200, 65), (x - int(9 * s), y - int(9 * s)), int(5 * s))

    def _arbol_sauce(self, x, y, s):
        """Sauce: copa ovalada con ramas, verde amarillento."""
        r_sombra = int(24 * s)
        pygame.draw.circle(self.superficie, (20, 50, 15), (x + 4, y + 5), r_sombra)
        rx = int(22 * s)
        ry = int(18 * s)
        pygame.draw.ellipse(self.superficie, (85, 145, 30), (x - rx, y - ry, rx * 2, ry * 2))
        color_rama = (70, 125, 25)
        for ang in range(0, 360, 40):
            rad = math.radians(ang)
            lx = x + int(math.cos(rad) * rx * 1.1)
            ly = y + int(math.sin(rad) * ry * 1.1)
            pygame.draw.line(self.superficie, color_rama, (x, y), (lx, ly), max(1, int(2 * s)))
            pygame.draw.circle(self.superficie, (100, 160, 40), (lx, ly), int(4 * s))
        pygame.draw.circle(self.superficie, (110, 170, 45), (x - int(4 * s), y - int(4 * s)), int(7 * s))

    # -------------------------------------------------------
    #  MONTAÑAS
    # -------------------------------------------------------
    def dibujar_montana(self, x, y, ancho, alto, color_base, con_nieve=True):
        puntos = self._perfil_montana(x, y, ancho, alto)

        # Cara frontal (en sombra — el sol está DETRÁS)
        pygame.draw.polygon(self.superficie, color_base, puntos)

        r, g, b = color_base
        sol_x = self.ancho_mundo // 2
        pico = min(puntos, key=lambda p: p[1])
        pico_x = pico[0]

        # Rim light solo en el lado que mira al sol
        color_rim = (min(r + 80, 220), min(g + 55, 175), min(b + 10, 110))
        for i in range(len(puntos) - 1):
            p1 = puntos[i]
            p2 = puntos[i + 1]
            if p1[1] > y + alto * 0.7 and p2[1] > y + alto * 0.7:
                continue
            # Cerca del pico: siempre iluminado
            if p1[1] < y + alto * 0.15 or p2[1] < y + alto * 0.15:
                pygame.draw.line(self.superficie, color_rim, p1, p2, 2)
                continue
            # Más abajo: solo en el flanco que mira al sol
            mid_x = (p1[0] + p2[0]) / 2
            if (x < sol_x and mid_x > pico[0]) or (x >= sol_x and mid_x < pico[0]):
                pygame.draw.line(self.superficie, color_rim, p1, p2, 2)

        # Pixel art: textura rocosa con sombreado según posición del sol
        sol_lado = 1 if pico_x < sol_x else -1  # lado iluminado
        # Colores para lado iluminado (rim)
        luz_r = min(r + 35, 240)
        luz_g = min(g + 28, 210)
        luz_b = min(b + 18, 170)
        # Colores para lado en sombra
        som_r = max(r - 30, 0)
        som_g = max(g - 28, 0)
        som_b = max(b - 18, 0)
        for _ in range(55):
            t = random.uniform(0.24, 0.92)
            half_w = int(ancho // 2 * t * 0.70)
            if half_w < 2:
                continue
            offset_x_px = random.randint(-half_w, half_w)
            px = pico_x + offset_x_px
            py = int(y + alto * t) + random.randint(-3, 3)
            pw = random.randint(3, 7)
            ph = random.randint(2, 5)
            # Sombreado según posición relativa al pico y al sol
            lado_rel = (offset_x_px * sol_lado) / max(half_w, 1)
            if lado_rel > 0.2:
                # Lado iluminado
                var = random.randint(-8, 8)
                c = (min(max(luz_r + var, 0), 255), min(max(luz_g + var, 0), 255), min(max(luz_b + var, 0), 255))
            elif lado_rel < -0.2:
                # Lado en sombra profunda
                var = random.randint(-6, 6)
                c = (min(max(som_r + var, 0), 255), min(max(som_g + var, 0), 255), min(max(som_b + var, 0), 255))
            else:
                # Centro — color base con variación
                var = random.randint(-10, 10)
                c = (min(max(r + var, 0), 255), min(max(g + var, 0), 255), min(max(b + var, 0), 255))
            pygame.draw.rect(self.superficie, c, (px, py, pw, ph))
        # Líneas de estrato horizontal (más en lado sombra)
        for _ in range(5):
            t = random.uniform(0.28, 0.85)
            half_w = int(ancho // 2 * t * 0.60)
            if half_w < 6:
                continue
            lado = random.choice([-1, 1])
            if lado == -sol_lado:
                sx = pico_x + lado * random.randint(4, max(5, half_w))
            else:
                sx = pico_x + lado * random.randint(2, max(3, half_w // 2))
            sy = int(y + alto * t)
            lw = random.randint(8, max(9, half_w // 3))
            pygame.draw.line(self.superficie, (som_r, som_g, som_b), (sx, sy), (sx + lw * lado, sy + random.randint(-2, 1)), 1)
        # Puntos de detalle (brillo puntual lado sol, sombra lado opuesto)
        for _ in range(20):
            t = random.uniform(0.22, 0.88)
            half_w = int(ancho // 2 * t * 0.65)
            if half_w < 2:
                continue
            off = random.randint(-half_w, half_w)
            dx = pico_x + off
            dy = int(y + alto * t) + random.randint(-2, 2)
            if (off * sol_lado) > 0:
                pygame.draw.rect(self.superficie, (min(luz_r + 15, 255), min(luz_g + 12, 255), min(luz_b + 8, 255)), (dx, dy, 2, 2))
            else:
                pygame.draw.rect(self.superficie, (max(som_r - 10, 0), max(som_g - 10, 0), max(som_b - 8, 0)), (dx, dy, 2, 2))

        # Grietas / estrías — restringidas dentro del perfil de la montaña
        color_grieta = (max(r - 20, 0), max(g - 20, 0), max(b - 15, 0))
        for _ in range(3):
            t1 = random.uniform(0.18, 0.52)
            gy1 = int(y + alto * t1)
            margen1 = int(ancho // 2 * t1 * 0.62)
            gx = pico_x + random.randint(-margen1, margen1)
            t2 = min(t1 + random.uniform(0.10, 0.22), 0.82)
            gy2 = int(y + alto * t2)
            margen2 = int(ancho // 2 * t2 * 0.62)
            gx2 = pico_x + max(-margen2, min(margen2, (gx - pico_x) + random.randint(-9, 9)))
            pygame.draw.line(self.superficie, color_grieta, (gx, gy1), (gx2, gy2), 2)

        if con_nieve:
            # Nieve con borde inferior ondulado
            nieve_base = pico[1] + alto // 5
            def nieve_y_en(nx):
                return nieve_base + math.sin(nx * 0.08) * 12 + math.sin(nx * 0.22) * 7 + math.sin(nx * 0.45) * 4

            puntos_nieve = []
            cruce_izq = None
            cruce_der = None
            n = len(puntos)
            for i in range(n):
                p = puntos[i]
                p_next = puntos[(i + 1) % n]
                lim = nieve_y_en(p[0])
                lim_next = nieve_y_en(p_next[0])
                p_arriba = p[1] <= lim
                p_next_arriba = p_next[1] <= lim_next

                if p_arriba:
                    puntos_nieve.append(p)

                if p_arriba != p_next_arriba and p_next[1] != p[1]:
                    lim_avg = (lim + lim_next) / 2
                    tc = (lim_avg - p[1]) / (p_next[1] - p[1])
                    tc = max(0.0, min(1.0, tc))
                    ix = int(p[0] + tc * (p_next[0] - p[0]))
                    iy = int(nieve_y_en(ix))

                    if p_arriba and not p_next_arriba:
                        cruce_izq = (ix, iy)
                        puntos_nieve.append(cruce_izq)
                    elif not p_arriba and p_next_arriba:
                        cruce_der = (ix, iy)
                        puntos_nieve.append(cruce_der)

            if cruce_izq and cruce_der and len(puntos_nieve) >= 3:
                idx_izq = puntos_nieve.index(cruce_izq)
                idx_der = puntos_nieve.index(cruce_der)

                # Puntos ondulados entre los dos cruces
                x_from = cruce_izq[0]
                x_to = cruce_der[0]
                wavy = []
                paso = 3 if x_to > x_from else -3
                for wx in range(x_from + paso, x_to, paso):
                    wavy.append((wx, int(nieve_y_en(wx))))

                final_nieve = puntos_nieve[:idx_izq + 1] + wavy + puntos_nieve[idx_der:]

                if len(final_nieve) >= 3:
                    pygame.draw.polygon(self.superficie, (230, 235, 250), final_nieve)
                    # Borde ondulado inferior
                    borde = [cruce_izq] + wavy + [cruce_der]
                    if len(borde) > 1:
                        pygame.draw.lines(self.superficie, (210, 218, 235), False, borde, 2)

    def _perfil_montana(self, x, y, ancho, alto):
        pico_x = x + random.randint(-ancho // 12, ancho // 12)
        pico_y = y
        puntos = [(pico_x, pico_y)]
        pasos = 4
        for i in range(1, pasos + 1):
            t = i / pasos
            bx = pico_x - int(ancho // 2 * t)
            by = y + int(alto * t)
            jitter_x = random.randint(-8, 8)
            jitter_y = random.randint(-5, 5) if i < pasos else 0
            puntos.append((bx + jitter_x, by + jitter_y))
        puntos.append((x + ancho // 2, y + alto))
        for i in range(pasos - 1, 0, -1):
            t = i / pasos
            bx = pico_x + int(ancho // 2 * t)
            by = y + int(alto * t)
            jitter_x = random.randint(-8, 8)
            jitter_y = random.randint(-5, 5)
            puntos.append((bx + jitter_x, by + jitter_y))
        return puntos

    # -------------------------------------------------------
    #  ROCA SUELTA
    # -------------------------------------------------------
    def dibujar_roca(self, x, y, r):
        shade = random.randint(80, 140)
        pygame.draw.circle(self.superficie, (shade, shade, shade - 15), (x, y), r)
        pygame.draw.circle(self.superficie, (shade + 30, shade + 30, shade + 20), (x - r // 3, y - r // 3), r // 2)

    # -------------------------------------------------------
    #  SOL
    # -------------------------------------------------------
    def dibujar_sol_epico(self, x, y):
        # Halo exterior difuminado (más grande)
        for radio in range(350, 110, -10):
            alpha = max(2, int(12 * (1 - (radio - 110) / 240.0)))
            s = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 210, 60, alpha), (radio, radio), radio)
            self.superficie.blit(s, (x - radio, y - radio))

        # Rayos largos (superficie grande para que no se corten)
        tam = 1200
        mitad = tam // 2
        sup_rayos = pygame.Surface((tam, tam), pygame.SRCALPHA)
        for i, angulo in enumerate(range(0, 360, 20)):
            rad = math.radians(angulo)
            grosor = 35 if i % 2 == 0 else 16
            alpha = 70 if i % 2 == 0 else 40
            largo = 580 if i % 2 == 0 else 450
            x2 = mitad + math.cos(rad) * largo
            y2 = mitad + math.sin(rad) * largo
            pygame.draw.line(sup_rayos, (255, 220, 60, alpha), (mitad, mitad), (int(x2), int(y2)), grosor)
        self.superficie.blit(sup_rayos, (x - mitad, y - mitad))

        # Rayos intermedios
        tam2 = 900
        mitad2 = tam2 // 2
        sup_rayos2 = pygame.Surface((tam2, tam2), pygame.SRCALPHA)
        for angulo in range(10, 360, 20):
            rad = math.radians(angulo)
            x2 = mitad2 + math.cos(rad) * 400
            y2 = mitad2 + math.sin(rad) * 400
            pygame.draw.line(sup_rayos2, (255, 240, 100, 30), (mitad2, mitad2), (int(x2), int(y2)), 10)
        self.superficie.blit(sup_rayos2, (x - mitad2, y - mitad2))

        # Corona solar
        pygame.draw.circle(self.superficie, (255, 180, 20), (x, y), 105)
        pygame.draw.circle(self.superficie, (255, 210, 50), (x, y), 95)

        # Núcleo
        pygame.draw.circle(self.superficie, (255, 230, 80), (x, y), 82)
        pygame.draw.circle(self.superficie, (255, 255, 150), (x, y), 68)
        pygame.draw.circle(self.superficie, (255, 255, 220), (x, y), 48)
        pygame.draw.circle(self.superficie, (255, 255, 255), (x, y), 24)

    # -------------------------------------------------------
    #  DIBUJADO EN PANTALLA
    # -------------------------------------------------------
    def dibujar(self, pantalla, offset_x, offset_y):
        pantalla.blit(self.superficie, (-offset_x - 100, -offset_y))
