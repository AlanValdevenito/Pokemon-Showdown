import gamelib
import batallas
import random

ANCHO_VENTANA = 1000
ALTO_VENTANA = 750
POKE_WIDTH = 150
VIDA_BASE = 110
ARCHIVO_PARTIDA = "data/partida.csv"
ARCHIVO_POKEMONS = "data/pokemons.csv"
ARCHIVO_DETALLE_MOVIMIENTOS = "data/detalle_movimientos.csv"

def batalla_crear():
    """
    Inicializa el estado de la batalla.
    Devuelve un diccionario de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Devuelve un dicionario de la forma: {pokemon: numero_pokemon}
    Devuelve una lista con tuplas de la forma: [('Bulbasaur', {'numero': '1', 'imagen': 'imgs/1.gif', 'tipo': 'Grass,Poison', 'hp': '45', 'atk': '49', 'defe': '49', 'spa': '65', 'spd': '65', 'spe': '45'})...]
    Devuelve un diccionario de la forma: {'ataque': {'categoria':... , 'objetivo':... , 'pp':... , 'poder':... , 'tipo':..., 'stats':... }}
    """
    
    
    equipos = batallas.cargar_partida(ARCHIVO_PARTIDA)
    pokemons, indices_pokemons = batallas.datos_pokemon(ARCHIVO_POKEMONS)
    informacion_movimientos = batallas.movimientos_informacion(ARCHIVO_DETALLE_MOVIMIENTOS)

    return equipos, pokemons, indices_pokemons, informacion_movimientos

def pedir_equipos(equipos, pokemons):
    """
    Recibe un diccionario con los equipos creados en la pokedex y recibe un diccionario con todos los pokemons.
    Pide los datos al usuario: nombre y numero del equipo.
    Devuelve los equipos para la batalla.
    """
        
    jugador = gamelib.input("Indique el nombre del jugador.")
    nombre_equipo = nombre_equipo_correcto(equipos, jugador)
    indice_equipo = batallas.obtener_indice(equipos, nombre_equipo)
    pokemons_equipo = batallas.pokemons_equipo(equipos, indice_equipo, nombre_equipo)
    equipo = batallas.Equipo(jugador, pokemons_equipo, indice_equipo, nombre_equipo)

    return equipo

def nombre_equipo_correcto(equipos, jugador):
    """
    Se encarga de revisar que el nombre del equipo ingresado por el usuario exista y sea correcto.
    En caso de que lo ingresado sea incorrecto, le sigue pidiendo al usuario un nombre correcto.
    En caso de que sea correcto, devuelve el nombre del equipo ingresado por el usuario.
    """

    nombre_equipo = gamelib.input(f"Indique el nombre del equipo a usar por {jugador}.")

    while not batallas.esta_equipo(equipos, nombre_equipo):
        nombre_equipo = gamelib.input(f"El nombre del equipo ingresado fue incorrecto. Indique el nombre del equipo a usar por {jugador}.")

    return nombre_equipo

def crear_pokemons_utilizados(equipo, equipos, pokemons, indices_pokemon, informacion_movimientos):
    """
    Creamos los Pokemons de cada equipo utilizando la clase Pokemon.
    """
    
    for i in range(0, len(equipo.pokemons)):
        indice_pokemon = indices_pokemon[equipo.pokemons[i]] - 1
        poke, info = pokemons[indice_pokemon]
        indice_equipo = equipo.indice_equipo
        nombre_equipo = equipo.nombre_equipo
        mov = batallas.obtener_movimientos(equipos, indice_equipo, nombre_equipo, poke)
        
        equipo.pokemons[i] = batallas.Pokemon(equipo.pokemons[i], mov, info["imagen"], info["tipo"], info["hp"], info["atk"], info["defe"], info["spa"], info["spd"], info["spe"], VIDA_BASE, batallas.obtener_pp_movimientos(equipo.pokemons[i], mov, informacion_movimientos))

def mostrar_campo_batalla(equipo1, equipo2, movimiento1, movimiento2, informacion_movimientos):
    """
    Recibe los equipos que van a batallar.
    
    Dibuja en pantalla el campo de batalla, los gifs de los entrenadores, el nombre de los jugadores, las
    pokeballs y el pokemon activo de cada equipo junto a su correspondiente barra de salud.
    """
    
    gamelib.draw_rectangle(0,0, ANCHO_VENTANA, ALTO_VENTANA, fill='red')
    gamelib.draw_image("imgs/background1.gif", 25, 25)

    gamelib.draw_rectangle(850, 685, 950, 715, fill='white', outline = 'gray')
    gamelib.draw_text("Escape", 900, 700, size = 18, bold = True, fill = "gray")
    gamelib.draw_text("(Salir)", 900, 730, size = 10, bold = True, fill = "white")
    
    gamelib.draw_rectangle(50, 685, 150, 715, fill='white', outline = 'gray')
    gamelib.draw_text("Enter", 100, 700, size = 18, bold = True, fill = "gray")
    gamelib.draw_text("(Elegir el Pokemon activo)", 100, 730, size = 10, bold = True, fill = "white")

    gamelib.draw_text(equipo1.jugador, 110, 480, size=18, bold=True, fill='white')
    gamelib.draw_image("imgs/trainer1.gif", 50, 530)

    gamelib.draw_text(equipo2.jugador, 880, 60, size=18, bold=True, fill='white')
    gamelib.draw_image("imgs/trainer2.gif", 830, 100)

    mostrar_pokeballs(equipo1, 50, 505)
    mostrar_pokeballs(equipo2, 820, 85)

    if equipo1.poke_activo != None and equipo2.poke_activo != None:
        mostrar_hp(equipo1.poke_activo, 250, 380, POKE_WIDTH)
        gamelib.draw_image(equipo1.poke_activo.imagen, 200, 400)
        mostrar_hp(equipo2.poke_activo, 650, 180, POKE_WIDTH)
        gamelib.draw_image(equipo2.poke_activo.imagen, 650, 200)

        gamelib.draw_rectangle(250, 685, 350, 715, fill='white', outline = 'gray')
        gamelib.draw_text("Espacio", 300, 700, size = 18, bold = True, fill = "gray")
        gamelib.draw_text("(Elegir movimientos)", 300, 730, size = 10, bold = True, fill = "white")

        gamelib.draw_rectangle(450, 685, 550, 715, fill='white', outline = 'gray')
        gamelib.draw_text("1", 500, 700, size = 18, bold = True, fill = "gray")
        gamelib.draw_text(f"(Stats de {equipo1.poke_activo})", 500, 730, size = 10, bold = True, fill = "white")

        gamelib.draw_rectangle(650, 685, 750, 715, fill='white', outline = 'gray')
        gamelib.draw_text("2", 700, 700, size = 18, bold = True, fill = "gray")
        gamelib.draw_text(f"(Stats de {equipo2.poke_activo})", 700, 730, size = 10, bold = True, fill = "white")

        if movimiento1 != "" and movimiento2 != "":
            mostrar_movimientos(movimiento1, equipo1.poke_activo, equipo2.poke_activo, informacion_movimientos, 40)
            mostrar_movimientos(movimiento2, equipo2.poke_activo, equipo1.poke_activo, informacion_movimientos, 60)

def mostrar_hp(poke, x, y, width):
    """
    Recibe un pokemon y unas coordenadas.
    Dibuja en pantalla el hp del pokemon que se introdujo como parametro.
    """
    
    porcentaje_restante = poke.hp / poke.hp_total
    if porcentaje_restante > 0.7:
        color = "green"
    elif 0.2 < porcentaje_restante <= 0.7:
        color = "yellow"
    else:
        color = "red"
    gamelib.draw_text(f"HP: {poke.hp}", x, y-15, size=15, bold=True, fill='black')
    gamelib.draw_rectangle(x, y, x + width, y + 10, fill='gray')
    gamelib.draw_rectangle(x, y, x + (width * porcentaje_restante), y + 10, fill=color)

def mostrar_pokeballs(equipo, x_inicial, y):
    """
    Dados un equipo y unas coordenadas, dibuja en pantalla los gifs de las pokeballs segun la cantidad de
    pokemones que tenga el equipo.
    """
    
    for i, poke in enumerate(equipo.pokemons):
        if equipo.pokemons[i].vivo:
            gamelib.draw_image("imgs/pokeball.gif", x_inicial + i * 20, y)
        if not equipo.pokemons[i].vivo:
            gamelib.draw_image("imgs/pokeball_gray.gif", x_inicial + i * 20, y)

def elegir_pokemon_activo(equipos, equipo, pokemons, indices_pokemons):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Recibe el equipo al cual se le pregunta que pokemon quiere como activo.
    Si el pokemon existe, entonces se lo define como el pokemon activo del equipo.
    """

    while True:

        poke = nombre_pokemon_correcto(equipos, equipo)

        for i in range(len(equipo.pokemons)):
            if poke == equipo.pokemons[i].nombre:

                if equipo.pokemons[i].vivo:
                    equipo.poke_activo = equipo.pokemons[i]
                    resetear_stats(equipo.poke_activo, pokemons, indices_pokemons)
                    return
                
                else:
                    gamelib.say(f"{poke} no se encuentra con vida. Por favor introduzca un pokemon que se encuentre con vida.")

def nombre_pokemon_correcto(equipos, equipo):
    """
    Se encarga de revisar que el nombre del pokemon ingresado por el usuario exista y sea correcto.
    En caso de que lo ingresado sea incorrecto, le sigue pidiendo al usuario un nombre correcto.
    En caso de que sea correcto, devuelve el nombre del equipo ingresado por el usuario.
    """

    nombre_pokemon = gamelib.input(f"Ingrese el nombre del pokemon que desea activo para el equipo {equipo.nombre_equipo}.")

    while not batallas.esta_pokemon(equipos, equipo, nombre_pokemon):
        nombre_pokemon = gamelib.input(f"El nombre del pokemon ingresado fue incorrecto. Ingrese el nombre del pokemon que desea activo para el equipo {equipo.nombre_equipo}.")

    return nombre_pokemon

def elegir_movimiento(equipo, informacion_movimientos):
    """
    Recibe al equipo que elige el movimiento.
    Recibe un diccionario de la forma: {'ataque': {'categoria':... , 'objetivo':... , 'pp':... , 'poder':... , 'tipo':..., 'stats':... }}
    Devuelve el movimiento elegido por el equipo.
    Devuelve True si el usuario hizo clic en Cancelar (vuelve atras).
    """

    while True:
    
        for movimiento in equipo.poke_activo.movimientos:
            if movimiento in informacion_movimientos:
                mov = gamelib.input(f"Equipo {equipo.nombre_equipo}: Usar el movimiento {movimiento} de categoria {informacion_movimientos[movimiento]['categoria']} para {equipo.poke_activo} │ [S/N].")

            if mov in ("S", "s"):
                return movimiento

            if mov == None:
                return None

def pokemon_mas_rapido(equipos, equipo1, equipo2, movimiento1, movimiento2, informacion_movimientos, pokemons, indices_pokemons):
    """
    Recibe ambos equipos que participan de la batalla.
    Segun el pokemon que tenga activo cada equipo el que sea mas rapido hara el movimiento primero.
    """

    if equipo1.poke_activo.spe == equipo2.poke_activo.spe:
        poke1_mas_rapido = random.choice([True, False])

    if equipo1.poke_activo.spe > equipo2.poke_activo.spe:
        poke1_mas_rapido = True

    else:
        poke1_mas_rapido = False

    if poke1_mas_rapido:
        partida_finalizada = realizar_movimiento(movimiento1, movimiento2, equipo1, equipo2, equipos, informacion_movimientos, pokemons, indices_pokemons)

    else:
        partida_finalizada = realizar_movimiento(movimiento2, movimiento1, equipo2, equipo1, equipos, informacion_movimientos, pokemons, indices_pokemons)

    return partida_finalizada
      
def realizar_movimiento(movimiento_ataca, movimiento_defiende, equipo_ataca, equipo_defiende, equipos, informacion_movimientos, pokemons, indices_pokemons):
    """
    Recibe el movimiento realizado por el atacante (el que comienza el turno por ser mas rapido).
    Recibe el movimiento realizado por el defensor.
    Recibe el equipo que ataca.
    Recibe el equipo que defiende.
    Recibe la lista de equipos.
    Recibe el diccionario con la informacion de los movimientos.
    Recibe la lista de pokemons.
    Recibe los indices de los pokemons.
    
    Esta funcion se encarga de invocar a la funcion que modifica los stats segun el movimiento y se encarga
    tambien de chequear si los pokemons mueren.

    Devuelve True si la partida termino. Devuelve False si la partida continua (siguen pokemons vivos).
    """

    modificar_stats(movimiento_ataca, equipo_ataca, equipo_defiende, informacion_movimientos)

    if not equipo_defiende.poke_activo.vivo:
        equipo_defiende.cantidad_vivos -= 1
        gamelib.say(f"El Pokemon {equipo_defiende.poke_activo} perteneciente al equipo {equipo_defiende.nombre_equipo} ha muerto. Deberas elegir otro pokemon.")

        if equipo_defiende.cantidad_vivos == 0:
            return True
            
        else:   
            elegir_pokemon_activo(equipos, equipo_defiende, pokemons, indices_pokemons)

    else:
        modificar_stats(movimiento_defiende, equipo_defiende, equipo_ataca, informacion_movimientos)

    if not equipo_ataca.poke_activo.vivo:
        equipo_ataca.cantidad_vivos -= 1
        gamelib.say(f"El Pokemon {equipo_ataca.poke_activo} perteneciente al equipo {equipo_ataca.nombre_equipo} ha muerto. Deberas elegir otro pokemon.")

        if equipo_ataca.cantidad_vivos == 0:
            return True
            
        else:   
            elegir_pokemon_activo(equipos, equipo_ataca, pokemons, indices_pokemons)

    return False

def modificar_stats(movimiento, equipo_ataca, equipo_defiende, informacion_movimientos):
    """
    Recibe el movimiento que realizo el pokemon.
    Recibe el equipo que ataca.
    Recibe el equipo que defiende.
    Recibe el diccionario con la informacion de los movimientos.
    De acuerdo a la categoria del movimiento, la funcion se encarga de modificar los stats.
    """

    if informacion_movimientos[movimiento]["categoria"] in ["Physical", "Special"]:
        daño = batallas.calcular_danio(movimiento, informacion_movimientos, equipo_ataca.poke_activo, equipo_defiende.poke_activo, batallas.obtener_tabla_tipos("data/tabla_tipos.csv"))
        equipo_defiende.poke_activo.recibir_daño(int(daño))

    if informacion_movimientos[movimiento]["categoria"] in ["Status"]:
        batallas.modificar_stats(movimiento, informacion_movimientos, equipo_ataca.poke_activo, equipo_defiende.poke_activo)

    equipo_ataca.poke_activo.descontar_pp(movimiento)

def resetear_stats(pokemon, pokemons, indices_pokemons):
    """
    Recibe el pokemon activo, la lista pokemons y el diccionario con los indices de los pokemons.
    Resetea los stats (atk, defe, spa, spd, spe).
    """
    indice_pokemon = indices_pokemons[pokemon.nombre]
    info_pokemon = pokemons[indice_pokemon - 1][1]
    
    pokemon.resetear_stats(info_pokemon["atk"], info_pokemon["defe"], info_pokemon["spa"], info_pokemon["spd"], info_pokemon["spe"])

def mostrar_movimientos(movimiento, pokemon_ataca, pokemon_defiende, informacion_movimientos, altura):
    """
    Recibe los movimientos de los pokemons, los pokemons y la informacion de los movimientos.
    Dibuja en la pantalla los movimientos que realizan los pokemons.
    """

    if informacion_movimientos[movimiento]["categoria"] in ["Status"]:
        stat = batallas.especificar_stat(informacion_movimientos[movimiento]["stats"])
        
        if informacion_movimientos[movimiento]["objetivo"] in ["self"]:  
            if stat == "vida":
                gamelib.draw_text(f"{pokemon_ataca} lanzó {movimiento} y restauró la mitad de su vida máxima. ", 40, altura, fill = 'white', size = 15, bold = True, anchor = 'w')         
            
            else:
                gamelib.draw_text(f"{pokemon_ataca} lanzó {movimiento} y duplicó su {stat}", 40, altura, fill = 'white', size = 15, bold = True, anchor = 'w')
        
        else:
            gamelib.draw_text(f"{pokemon_ataca} lanzó {movimiento} contra {pokemon_defiende} y redujo a la mitad su {stat}", 40, altura, fill = 'white', size = 15, bold = True, anchor = 'w')
    
    else:
        gamelib.draw_text(f"{pokemon_ataca} lanzó {movimiento} y le infligió daño a {pokemon_defiende}", 40, altura, fill = 'white', size = 15, bold = True, anchor = 'w')

def main():

    gamelib.title("Pokemon Showdown")
    equipos, pokemons, indices_pokemons, informacion_movimientos = batalla_crear()

    if equipos == {}:
        gamelib.say("No hay ningun equipo creado en la pokedex. Para comenzar una batalla primero cree equipos.")
        return

    equipo1, equipo2 = pedir_equipos(equipos, pokemons), pedir_equipos(equipos, pokemons)

    movimiento1 = ""
    movimiento2 = ""

    crear_pokemons_utilizados(equipo1, equipos, pokemons, indices_pokemons, informacion_movimientos)
    crear_pokemons_utilizados(equipo2, equipos, pokemons, indices_pokemons, informacion_movimientos)
    
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    while gamelib.is_alive():
        gamelib.draw_begin()
        mostrar_campo_batalla(equipo1, equipo2, movimiento1, movimiento2, informacion_movimientos)
        gamelib.draw_end()
        
        ev = gamelib.wait()

        if not ev:
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            break

        if ev.type == gamelib.EventType.KeyPress:
            
            if ev.key == "Return":
                elegir_pokemon_activo(equipos, equipo1, pokemons, indices_pokemons)
                elegir_pokemon_activo(equipos, equipo2, pokemons, indices_pokemons)

            if equipo1.poke_activo and equipo2.poke_activo and ev.key == "space":
                movimiento1 = elegir_movimiento(equipo1, informacion_movimientos)
                movimiento2 = elegir_movimiento(equipo2, informacion_movimientos)

                if movimiento1 != None and movimiento2 != None:
                    partida_finalizada = pokemon_mas_rapido(equipos, equipo1, equipo2, movimiento1, movimiento2, informacion_movimientos, pokemons, indices_pokemons)
                    
                    if partida_finalizada:
                        gamelib.say(f"Juego terminado.\n\n¡Felicitaciones!")
                        break
                        
            if equipo1.poke_activo and equipo2.poke_activo and ev.key in ["1", "2"]:

                if ev.key == "1":
                    gamelib.say(f"Nombre: {equipo1.poke_activo.nombre}\nTipos: {equipo1.poke_activo.tipos}\nAtaque: {equipo1.poke_activo.atk}\nDefensa: {equipo1.poke_activo.defe}\nAtaque Especial: {equipo1.poke_activo.spa}\nDefensa Especial: {equipo1.poke_activo.spd}\nVelocidad: {equipo1.poke_activo.spe}")

                if ev.key == "2":
                    gamelib.say(f"Nombre: {equipo2.poke_activo.nombre}\nTipos: {equipo2.poke_activo.tipos}\nAtaque: {equipo2.poke_activo.atk}\nDefensa: {equipo2.poke_activo.defe}\nAtaque Especial: {equipo2.poke_activo.spa}\nDefensa Especial: {equipo2.poke_activo.spd}\nVelocidad: {equipo2.poke_activo.spe}")

gamelib.init(main)
