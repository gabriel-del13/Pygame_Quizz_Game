# preguntas.py - Sistema de preguntas actualizado para IDs

def obtener_pregunta(id_casilla):
    """
    Retorna una pregunta basada en el ID de la casilla
    """
    preguntas = {
        "1": {
            "pregunta": "¿Dónde vive Jesús?",
            "opciones": ["En mi corazón", "En la casa de mi tía", "En el mar", "En la tienda"],
            "correcta": 0
        },
        "2": {
            "pregunta": "¿Quien creó a los niños?",
            "opciones": ["El Doctor", "Dios", "Mono", "El Maestro"],
            "correcta": 1
        },
        "3": {
            "pregunta": "¿Quién es el Hijo de Dios?",
            "opciones": ["David", "Daniel", "Jesús", "Pedro"],
            "correcta": 2
        },
        # Preguntas del camino alternativo
        "3.1": {
            "pregunta": "¿Que creó Dios en el Sexto (6) Dia?",
            "opciones": ["Los Humanos", "El Sol", "El Mar", "El Cielo"],
            "correcta": 0
        },
        "3.2": {
            "pregunta": "¿Donde dice: Por tanto, id, y haced discípulos a todas las naciones, bautizándolos en el nombre del Padre, y del Hijo, y del Espíritu Santo...?",
            "opciones": ["Eclesiastés 3:1", "Mateo 28:19", "Apocalipsis 21:4", "Genesis 1:1"],
            "correcta": 1
        },
        "3.3": {
            "pregunta": "¿Cómo se llama el maestro?",
            "opciones": ["Manuel", "Gabriel", "Javier", "Anel"],
            "correcta": 1
        },
        # Preguntas del camino principal
        "4": {
            "pregunta": "¿Que es Orar?",
            "opciones": ["Hablar con Dios", "Hablar con los Niños", "Hablar con los Animales", "Hablar con los Adultos"],
            "correcta": 0
        },
        "5": {
            "pregunta": "¿Cuál es el nombre de la madre de Jesus?",
            "opciones": ["Marta", "Ana", "Rosa", "María"],
            "correcta": 3
        },
        "6": {
            "pregunta": "¿Cual es el Titulo del Libro?",
            "opciones": ["La Gran Aventura", "Un Paseo con Dios", "Jesus y sus Amigos", "La Historia de Sam"],
            "correcta": 0
        },
        "7": {
            "pregunta": "¿Quienes alejaron a los niños de Jesús?",
            "opciones": ["Los otros niños", "Las Viudas", "Los Discípulos", "Los Fariseos"],
            "correcta": 2
        },
        "8": {
            "pregunta": "¿Jesús Murió por...?",
            "opciones": ["Los Perros", "Obligación", "Su madre", "Nuestros pecados"],
            "correcta": 3
        },
        "9": {
            "pregunta": "¿Como se llamaba el gigante que derrotó David?",
            "opciones": ["Samuel", "Saul", "Galileo", "Goliath"],
            "correcta": 3
        },
        "10": {
            "pregunta": "¿Cuál es el nombre de la última clase?",
            "opciones": ["La Historia de Sam", "Hablar a los Demás", "El Amor de Dios", "El Camino de la Vida"],
            "correcta": 1
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