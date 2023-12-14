import csv
import random

def cargar_partida(archivo_equipos):
    """
    Recibe un archivo de la forma equipo;pokemon;movimiento1,movimiento2...
    Devuelve una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    """

    resultado = []
    equipos = {}
    
    try:
        with open(archivo_equipos) as f:
            csv_reader = csv.reader(f, delimiter = ";")

            for linea in csv_reader:
                
                if len(linea) == 3:
                    nombre_equipo, pokemon, movimientos = linea
                    movimientos = movimientos.split(",")
                    equipos[nombre_equipo] = equipos.get(nombre_equipo, {})
                    equipos[nombre_equipo][pokemon] = equipos[nombre_equipo].get(pokemon, []) + movimientos
                    
                if len(linea) == 2:
                    nombre_equipo, pokemon = linea
                    equipos[nombre_equipo] = equipos.get(nombre_equipo, {})
                    
        for equipo, pokemons in equipos.items():
            dic = {}
            dic[equipo] = pokemons
            resultado.append(dic)
        
        return resultado
                
    except FileNotFoundError:
        return resultado

def datos_pokemon(archivo_pokemons):
    """
    Recibe un archivo con todos los pokemons de la forma: numero;imagen;nombre;tipos;hp;atk;def;spa;spd;spe.
    Devuelve un dicionario de la forma: {pokemon: numero_pokemon}
    Devuelve una lista con tuplas de la forma: [('Bulbasaur', {'numero': '1', 'imagen': 'imgs/1.gif', 'tipo': 'Grass,Poison', 'hp': '45', 'atk': '49', 'defe': '49', 'spa': '65', 'spd': '65', 'spe': '45'})...]
    """

    lista = []
    diccionario = {}

    with open(archivo_pokemons) as f:
        csv_reader = csv.reader(f, delimiter = ";")
        encabezado = next(csv_reader)

        for linea in csv_reader:
            numero, imagen, nombre, tipo, hp, atk, defe, spa, spd, spe = linea
            lista.append((nombre, {'numero':int(numero),'imagen':imagen, 'tipo':tipo, 'hp':int(hp), 'atk':int(atk), 'defe': int(defe), 'spa':int(spa), 'spd':int(spd), 'spe':int(spe)}))
            diccionario[nombre] = int(numero)
           
    return lista, diccionario

def informacion_nombre(pokemons, indices_pokemons, pokemon):
    """
    Recibe una lista ordenada de tuplas de la forma: [(pokemon, {info_pokemon})].
    Recibe un diccionario de la forma: {pokemon:numero_pokemon}.
    Recibe el nombre del pokemon particular.
    Devuelve un diccionario que contiene la informacion del pokemon.
    """
    
    pokemon_numero = int(indices_pokemons[pokemon])
    return pokemons[pokemon_numero - 1][1]

def pokemons_equipo(equipos, indice_equipo, nombre_equipo):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Devuelve una lista con cada pokemon que forma el equipo.
    """

    pokemons_equipo = equipos[indice_equipo][nombre_equipo]
    pokemons = []

    for clave in pokemons_equipo.keys():
        pokemons.append(clave)

    return pokemons

def obtener_movimientos(equipos, indice_equipo, nombre_equipo, pokemon):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Recibe el indice del equipo.
    Recibe el nombre del equipo y el pokemon del cual se piden los movimientos.
    Devuelve los movimientos del pokemon ingresado.
    """

    equipo = equipos[indice_equipo]
    return equipo[nombre_equipo][pokemon]

def obtener_indice(equipos, nombre_equipo):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Recibe el nombre del equipo del cual se quiere obtener el indice.
    Devuelve el indice del equipo.
    """

    for indice in range(len(equipos)):
        if nombre_equipo == list(equipos[indice].keys())[0]:
            return indice

def movimientos_informacion(archivo_detalle_movimientos):
    """
    Recibe un archivo de la forma: nombre,categoria,objetivo,pp,poder,tipo,stats
    Devuelve un diccionario de la forma: {'ataque': {'categoria':... , 'objetivo':... , 'pp':... , 'poder':... , 'tipo':..., 'stats':... }}
    """

    resultado = {}

    with open(archivo_detalle_movimientos) as f:
        csv_reader = csv.reader(f, delimiter = ",")
        encabezado = next(csv_reader)
        
        for linea in csv_reader:
            nombre, categoria, objetivo ,pp , poder, tipo, stats = linea
            resultado[nombre] = resultado.get(nombre, {})

            for indice in range(len(encabezado)):
                if encabezado[indice] != "nombre":
                    resultado[nombre][encabezado[indice]] = linea[indice]
                    
    return resultado

def esta_equipo(equipos, nombre_equipo):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Recibe el nombre de un equipo para ver si se encuentra en el diccionario.
    Si el equipo existe, devuelve True.
    Si el equipo no existe, devuelve False.
    """

    for indice in range(len(equipos)):
        if nombre_equipo == list(equipos[indice].keys())[0]:
            return True

    return False
            
def esta_pokemon(equipos, equipo, nombre_pokemon):
    """
    Recibe una lista de la forma: [{equipo: {pokemon: [movimientos]}}, {equipo: {pokemon: []}, ...}]
    Recibe el equipo.
    Recibe el nombre de un pokemon para ver si se encuentra en el diccionario.
    Si el pokemon se encuentra en el equipo, devuelve True.
    Si el pokemon no se encuentra en el equipo, devuelve False.
    """

    return nombre_pokemon in equipos[equipo.indice_equipo][equipo.nombre_equipo]
    
def obtener_tabla_tipos(archivo_tabla_tipos):
    """
    Recibe un archivo en forma de tabla con los tipos de pokemons.
    Devuelve un diccionario de la forma {tipo1:{tipo1 : 1, tipo2 : 1, tipo3 : 0.5, ...}, tipo2 : {tipo1 : 2, tipo2 : 1, ...}},
    en el cual cada numero representa el modificador de daño, que depende de el tipo del pokemon que ataca y el tipo de pokemon
    que defiende.
    """

    tabla = {}
    tipos = []
    
    with open(archivo_tabla_tipos) as f:
    
        for linea in csv.reader(f, delimiter = ";"):
            for tipo in linea:
                if tipo == 'Types':
                    pass
                else:
                    tabla[tipo] = {}
                    tipos.append(tipo)
            break
    
        for linea in csv.reader(f, delimiter = ";"):
            clave = linea[0]
            for i in range(len(linea)):
            
                if linea[i].isalpha():
                    pass
                    
                else:
                    tipo = tipos[i - 1]
                    tabla[clave][tipo] = linea[i]
                    
    return tabla

def calcular_danio_base(movimiento, informacion_movimientos, pokemon_atacante, pokemon_defensor):
    """
    Recibe el pokemon atacante y el pokemon defensor, movimiento que realiza el pokemon atacante y la informacion de los movimientos.
    Devuelve el daño base que realiza el pokemon atacante.
    """

    if informacion_movimientos[movimiento]["categoria"] == "Physical":
        ataque = pokemon_atacante.atk
        defensa = pokemon_defensor.defe
    
    elif informacion_movimientos[movimiento]["categoria"] == "Special":
        ataque = pokemon_atacante.spa
        defensa = pokemon_defensor.spd
    
    poder = int(informacion_movimientos[movimiento]["poder"])
    
    danio_base = 15 * poder * ataque / defensa / 50
    return danio_base

def movimiento_es_stab(movimiento, informacion_movimientos, pokemon):
    """
    Recibe el movimiento elegido por el usuario, el diccionario con la informacion de los movimientos y el pokemon.
    Devuelve True si el movimiento es STAB (Same Type Attack Bonus) y False en caso contrario.
    """
    return informacion_movimientos[movimiento]["tipo"] in pokemon.tipos

def calcular_modificador_danio(movimiento, informacion_movimientos, pokemon_defensor, tabla_tipos):
    """
    Recibe el pokemon atacante, el pokemon defensor y la tabla de tipos.
    Devuelve el valor del modificador de tipo defensor.
    """
    
    tipo_movimiento = informacion_movimientos[movimiento]["tipo"]
    tipos_defensor = (pokemon_defensor.tipos).split(",")
    modificador = 1
    
    if len(tipos_defensor) > 1:
        for tipo in tipos_defensor:

            modificador *= float(tabla_tipos[tipo][tipo_movimiento])

    else:
        modificador = float(tabla_tipos[tipos_defensor[0]][tipo_movimiento])

    return modificador
    
def obtener_danio_aleatorio(danio_base):
    """
    Recibe el daño base con los modificadores aplicados y devuelve un entero entre
    el 80% y el 100% del danio base
    """
    
    danio_menor = int(0.8 * danio_base)
    
    try:
        danio_final = random.randrange(danio_menor, int(danio_base))
    
    except ValueError:
        return 0
    
    return danio_final

def calcular_danio(movimiento, informacion_movimientos, pokemon_atacante, pokemon_defensor, tabla_tipos):
    """
    Recibe el movimiento que realiza el pokemon atacante, el diccionario con los movimientos, el pokemon
    atacante y el pokemon defensor.
    Devuelve el danio final que se le aplica al pokemon defensor.
    """
    
    danio_base = int(calcular_danio_base(movimiento, informacion_movimientos, pokemon_atacante, pokemon_defensor))
    
    if movimiento_es_stab(movimiento, informacion_movimientos, pokemon_atacante):
        danio_base *= 1.5
        
    modificador_danio = calcular_modificador_danio(movimiento, informacion_movimientos, pokemon_defensor, tabla_tipos)
    
    danio_base = danio_base * modificador_danio

    danio_final = obtener_danio_aleatorio(danio_base)
    return danio_final

def modificar_stats(movimiento, informacion_movimientos, pokemon_atacante, pokemon_defensor):
    """
    Recibe el movimiento del pokemon atacante, el diccionario con la informacion de los movimientos, el pokemon
    atacante y el pokemon defensor.
    Modifica los stats dependiendo del objetivo y del stat del movimiento.
    """
    objetivo = informacion_movimientos[movimiento]["objetivo"]
    stats = informacion_movimientos[movimiento]["stats"].split(",")
    
    for i in range(len(stats)):        
        if stats[i] == "def":           
            stats[i] = "defe"    
    
    if objetivo == "self":       
        for stat in stats:
            if stat == "":
                restauracion = pokemon_atacante.hp_total // 2
                pokemon_atacante.aumentar_hp(restauracion)
            else:               
                pokemon_atacante.aumentar_stats(stat)
        
    else:
        for stat in stats:               
            pokemon_defensor.reducir_stats(stat)

def especificar_stat(stat):
    """
    Recibe un stat y devuelve la palabra que representa a ese stat.
    Por ejemplo: recibe 'hp' y devuelve 'vida'.
    """
    
    if stat == "":
        return "vida"
    if stat == "atk":
        return "ataque"
    if stat == "def":
        return "defensa"
    if stat == "spe":
        return "velocidad"

def obtener_pp_movimientos(pokemon, movimientos, informacion_movimientos):
    """
    Recibe el pokemon, el diccionario de movimientos y la informacion de los movimientos.
    Devuelve un diccionario cuyas claves son los movimientos del pokemon y los valores son la cantidad de veces
    que puede usar dicho movimiento en una partida.
    """
    
    pp_movimientos = {}
    for movimiento in movimientos:
        if movimiento in informacion_movimientos:
            pp_movimientos[movimiento] = int(informacion_movimientos[movimiento]["pp"])

    return pp_movimientos

class Equipo:

    def __init__(self, jugador, pokemons, indice_equipo, nombre_equipo):
        self.jugador = jugador
        self.poke_activo = None
        self.pokemons = pokemons
        self.indice_equipo = int(indice_equipo)
        self.nombre_equipo = nombre_equipo
        self.cantidad_vivos = len(pokemons)

    def __str__(self):
        return f"{self.nombre_equipo}"

class Pokemon:

    def __init__(self, nombre, movimientos, imagen, tipos, hp, atk, defe, spa, spd, spe, vida_base, pp_movimientos):
        self.nombre = nombre
        self.movimientos = movimientos
        self.imagen = imagen
        self.tipos = tipos
        self.hp = int(hp) + int(vida_base)
        self.atk = int(atk)
        self.defe = int(defe)
        self.spa = int(spa)
        self.spd = int(spd)
        self.spe = int(spe)
        self.hp_total = int(hp) + int(vida_base)
        self.vivo = True
        self.pp_movimientos = pp_movimientos

    def __str__(self):
        return f"{self.nombre}"

    def recibir_daño(self, daño):
        self.hp -= daño

        if self.hp <= 0:
            self.vivo = False

    def aumentar_hp(self, vida):
        if self.hp < self.hp_total:

            if (self.hp + vida) > self.hp_total:
                self.hp += vida
                hp_perdido = self.hp - self.hp_total
                self.hp -= hp_perdido

            else:
               self.hp += vida

    def aumentar_stats(self, stat):
        if stat == "hp":
            self.hp = 2 * self.hp
        
        if stat == "atk":
            self.atk = 2 * self.atk
        
        if stat == "defe":
            self.defe =  2 * self.defe
        
        if stat == "spa":
            self.spa = 2 * self.spa
        
        if stat == "spe":
            self.spe = 2 * self.spe
        
        if stat == "spd":
            self.spd = 2 * self.spd        

    def reducir_stats(self, stat):
        if stat == "hp":
            self.hp = self.hp // 2
        
        if stat == "atk":
            self.atk = self.atk // 2
        
        if stat == "defe":
            self.defe =  self.defe // 2
        
        if stat == "spa":
            self.spa = self.spa // 2
        
        if stat == "spe":
            self.spe = self.spe // 2
        
        if stat == "spd":
            self.spd = self.spd // 2

    def descontar_pp(self, movimiento):
        self.pp_movimientos[movimiento] = self.pp_movimientos[movimiento] - 1
        pp = self.pp_movimientos[movimiento]
        
        if pp == 0:
           self.pp_movimientos.pop(movimiento)
           self.movimientos.remove(movimiento)
        
        if self.pp_movimientos == {}:
           self.vivo = False

    def resetear_stats(self, atk, defe, spa, spd, spe):
        self.atk = atk
        self.defe = defe
        self.spa = spa
        self.spd = spd
        self.spe = spe
