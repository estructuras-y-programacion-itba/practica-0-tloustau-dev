# ## Trabajo Práctico: Simulación del Juego de la Generala
import random
import csv

# 1) LANZAR DADOS
def lanzar_dados(cantidad):
    dados = []
    for i in range(cantidad):
        dado = random.randint(1, 6)
        dados.append(dado)
    return dados

# 2) TURNO
def turno():
    dados = lanzar_dados(5)
    print("Tirada 1:", dados)
    primera_tirada = True

    for tirada in range(2, 4):
        mantener = input("¿Qué posiciones mantenés? (ENTER para quedarte con todos): ")
        if mantener == "":
            print("Mantuviste todos. Fin del turno.")
            break
        primera_tirada = False
        posiciones = [int(x) for x in mantener.split(",")]
        dados_mantenidos = [dados[p - 1] for p in posiciones]
        dados_nuevos = lanzar_dados(5 - len(dados_mantenidos))
        dados = dados_mantenidos + dados_nuevos
        dados.sort()
        print(f"Tirada {tirada}:", dados)

    return dados, primera_tirada

# 3) VERIFICAR JUGADA
def verificar_jugada(dados):
    conteos = {}
    for d in dados:
        if d not in conteos:
            conteos[d] = 0
        conteos[d] += 1

    valores = sorted(conteos.values(), reverse=True)
    jugadas = []

    if valores[0] == 5:
        jugadas.append("G")
    if valores[0] >= 4:
        jugadas.append("P")
    if valores[0] >= 3 and len(valores) >= 2 and valores[1] >= 2:
        jugadas.append("F")

    dados_unicos = sorted(set(dados))
    if len(dados_unicos) == 5 and dados_unicos[4] - dados_unicos[0] == 4:
        jugadas.append("E")

    return jugadas

# 4) CALCULAR PUNTAJE
def calcular_puntaje(categoria, dados, primera_tirada):
    jugadas = verificar_jugada(dados)
    bonus = 5 if primera_tirada else 0

    if categoria == "G":
        return 50 if "G" in jugadas else 0
    if categoria == "P":
        return (40 + bonus) if "P" in jugadas else 0
    if categoria == "F":
        return (30 + bonus) if "F" in jugadas else 0
    if categoria == "E":
        return (20 + bonus) if "E" in jugadas else 0

    numero = int(categoria)
    return sum(d for d in dados if d == numero)

# 4) ELEGIR CATEGORÍA
def elegir_categoria(dados, planilla, primera_tirada):
    disponibles = [c for c in planilla if planilla[c] is None]
    print("Categorías disponibles:", disponibles)

    while True:
        eleccion = input("Elegí una categoría: ").upper()
        if eleccion in disponibles:
            puntaje = calcular_puntaje(eleccion, dados, primera_tirada)
            planilla[eleccion] = puntaje
            print(f"Anotaste {puntaje} puntos en '{eleccion}'.")
            return
        else:
            print("Categoría inválida o ya usada. Intentá de nuevo.")

# 6) GUARDAR CSV
def guardar_csv(planillas, nombres):
    with open("jugadas.csv", "w", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["jugada", "j1", "j2"])
        for cat in ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"]:
            v1 = planillas[0][cat] if planillas[0][cat] is not None else ""
            v2 = planillas[1][cat] if planillas[1][cat] is not None else ""
            writer.writerow([cat, v1, v2])

# 5) JUEGO PRINCIPAL
def jugar():
    nombre_j1 = input("Nombre Jugador 1: ")
    nombre_j2 = input("Nombre Jugador 2: ")
    nombres = [nombre_j1, nombre_j2]

    planillas = [
        {"E": None, "F": None, "P": None, "G": None,
         "1": None, "2": None, "3": None, "4": None, "5": None, "6": None},
        {"E": None, "F": None, "P": None, "G": None,
         "1": None, "2": None, "3": None, "4": None, "5": None, "6": None}
    ]

    juego_terminado = False

    while not juego_terminado:
        for i in range(2):
            print(f"\n--- Turno de {nombres[i]} ---")
            dados, primera_tirada = turno()
            elegir_categoria(dados, planillas[i], primera_tirada)
            guardar_csv(planillas, nombres)  # guarda después de cada turno

            j1_completo = all(v is not None for v in planillas[0].values())
            j2_completo = all(v is not None for v in planillas[1].values())
            if j1_completo and j2_completo:
                juego_terminado = True
                break

    total_j1 = sum(v for v in planillas[0].values())
    total_j2 = sum(v for v in planillas[1].values())

    print(f"\n{nombres[0]}: {total_j1} puntos")
    print(f"{nombres[1]}: {total_j2} puntos")

    if total_j1 > total_j2:
        print(f"¡Ganó {nombres[0]}!")
    elif total_j2 > total_j1:
        print(f"¡Ganó {nombres[1]}!")
    else:
        print("¡Empate!")

# ARRANCAR EL JUEGO
jugar()