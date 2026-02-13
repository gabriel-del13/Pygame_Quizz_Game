# preguntas.py - Sistema de preguntas actualizado para IDs

def obtener_pregunta(id_casilla):
    """
    Retorna una pregunta basada en el ID de la casilla
    """
    preguntas = {
        "1": {
            "pregunta": "¿Cuál es la capital de Francia?",
            "opciones": ["París", "Londres", "Madrid", "Roma"],
            "correcta": 0
        },
        "2": {
            "pregunta": "¿Cuántos planetas tiene el sistema solar?",
            "opciones": ["7", "8", "9", "10"],
            "correcta": 1
        },
        "3": {
            "pregunta": "¿Quién pintó la Mona Lisa?",
            "opciones": ["Van Gogh", "Picasso", "Da Vinci", "Miguel Ángel"],
            "correcta": 2
        },
        # Preguntas del camino alternativo
        "3.1": {
            "pregunta": "¿Cuál es el océano más grande del mundo?",
            "opciones": ["Atlántico", "Índico", "Ártico", "Pacífico"],
            "correcta": 3
        },
        "3.2": {
            "pregunta": "¿En qué año llegó el hombre a la Luna?",
            "opciones": ["1965", "1967", "1969", "1971"],
            "correcta": 2
        },
        "3.3": {
            "pregunta": "¿Cuál es el metal más abundante en la corteza terrestre?",
            "opciones": ["Hierro", "Aluminio", "Cobre", "Oro"],
            "correcta": 1
        },
        # Preguntas del camino principal
        "4": {
            "pregunta": "¿Cuál es el río más largo del mundo?",
            "opciones": ["Nilo", "Amazonas", "Yangtsé", "Misisipi"],
            "correcta": 1
        },
        "5": {
            "pregunta": "¿Quién escribió 'Don Quijote de la Mancha'?",
            "opciones": ["Lope de Vega", "Miguel de Cervantes", "Calderón", "Góngora"],
            "correcta": 1
        },
        "6": {
            "pregunta": "¿Cuántos continentes hay en la Tierra?",
            "opciones": ["5", "6", "7", "8"],
            "correcta": 2
        },
        "7": {
            "pregunta": "¿Cuál es el animal terrestre más rápido?",
            "opciones": ["León", "Guepardo", "Gacela", "Caballo"],
            "correcta": 1
        },
        "8": {
            "pregunta": "¿Qué gas respiramos principalmente?",
            "opciones": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Hidrógeno"],
            "correcta": 1
        },
        "9": {
            "pregunta": "¿Cuántos huesos tiene el cuerpo humano adulto?",
            "opciones": ["186", "206", "226", "246"],
            "correcta": 1
        },
        "10": {
            "pregunta": "¿Quién desarrolló la teoría de la relatividad?",
            "opciones": ["Newton", "Einstein", "Galileo", "Hawking"],
            "correcta": 1
        },
        "META": {
            "pregunta": "¿Cuál es el idioma más hablado en el mundo?",
            "opciones": ["Inglés", "Español", "Mandarín", "Hindi"],
            "correcta": 2
        }
    }
    
    # Si no existe la pregunta, retornar una por defecto
    if id_casilla not in preguntas:
        return {
            "pregunta": f"Pregunta para casilla {id_casilla}",
            "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
            "correcta": 0
        }
    
    return preguntas[id_casilla]