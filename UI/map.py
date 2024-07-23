import random
import UI.color_printer as colp

# 🏫🏟️🏛️🛕🕌🕍🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒🗼🗽⛺
arbres = ["🌲", "🌳", "🌴"]
cailloux = ["🪨"]
maisons = ["🛖", "🏠", "🏡"]


builds = {
    "Usine": {"money_cost": 0, "wood_cost": 5, "stone_cost": 5, "symbol": "🏭", "gain": 1},
    "Maison t1": {"money_cost": 20, "wood_cost": 5, "stone_cost": 5, "symbol": "🛖", "gain": 1},
    "Maison t2": {"money_cost": 40, "wood_cost": 5, "stone_cost": 5, "symbol": "🏠", "gain": 2},
    "Maison t3": {"money_cost": 60, "wood_cost": 5, "stone_cost": 5, "symbol": "🏡", "gain": 3},
    "Hopital": {"money_cost": 100, "wood_cost": 5, "stone_cost": 5, "symbol": "🏣", "gain": 5}
}

def get_builds():
    return builds


def generate_context(largeur=150, hauteur=24):
    carte = [["" for _ in range(largeur)] for _ in range(hauteur)]
    menu = [["" for _ in range(largeur // 2)] for _ in range(5)]
    __fill_map(carte, hauteur, largeur)
    fill_menu(menu, largeur // 2)

    return carte, menu


def draw_game(carte, menu, game_state):
    draw_map(carte)
    draw_menu(menu, game_state)


def __fill_map(carte, hauteur: int, largeur: int):
    for h in range(hauteur):
        for l in range(largeur):
            if l == 0 and h == 0:
                carte[h][l] = "╔"
            elif l == largeur - 1 and h == 0:
                carte[h][l] = "╗"
            elif l == 0 and h == hauteur - 1:
                carte[h][l] = "╚"
            elif l == largeur - 1 and h == hauteur - 1:
                carte[h][l] = "╝"
            elif h == 0 or h == hauteur - 1:
                carte[h][l] = "═"
            elif l == 0 or l == largeur - 1:
                carte[h][l] = "║"
            elif l <= 65:
                __fill_inside_map(carte, h, l)


def __fill_inside_map(carte, hauteur: int, largeur: int):
    if random.random() < 0.01:
        carte[hauteur][largeur] = random.choice(arbres)
    elif random.random() < 0.005:
        carte[hauteur][largeur] = random.choice(cailloux)
    else:
        carte[hauteur][largeur] = "▪️"


def fill_menu(menu, largeur=150 // 2, bois=0, argent=0, pierre=0):
    hauteur = 5
    for h in range(hauteur):
        for l in range(largeur):
            if l == 0 and h == 0:
                menu[h][l] = "╔"
            elif l == largeur - 1 and h == 0:
                menu[h][l] = "╗"
            elif l == 0 and h == hauteur - 1:
                menu[h][l] = "╚"
            elif l == largeur - 1 and h == hauteur - 1:
                menu[h][l] = "╝"
            elif l <= 65:
                __fill_inside_menu(menu, l, h, bois, argent, pierre)


def __fill_inside_menu(menu, l=150 // 2, h=5, bois=0, argent=0, pierre=0):
    if h == 2:
        match l:
            case 2:
                menu[h][l] = f"💲 = {argent:<3}"
            case 22:
                menu[h][l] = f"🪵 = {bois:<3}"
            case 42:
                menu[h][l] = f"🪨 = {pierre:<3}"
            case _:
                menu[h][l] = " "
    elif h == 1 and l == 25:
        menu[h][l] = '## RESSOURCES ##'
    else:
        menu[h][l] = " "


def draw_map(carte):
    for ligne in carte:
        print(colp.print_color("BLUE") + "".join(ligne), sep="")


def draw_menu(menu, state: int):
    sentences = get_sentences(state)
    sentence_count = len(sentences)
    for i, ligne in enumerate(menu):
        if i <= sentence_count - 1:
            match i:
                case 0 | 2:
                    print(colp.print_color("WARNING") + "".join(ligne), colp.print_color("HEADER") + sentences[i])
                case 1:
                    print(colp.print_color("WARNING") + "".join(ligne), "\t\t", colp.print_color("HEADER") + sentences[i])
                case 3:
                    print(colp.print_color("WARNING") + "".join(ligne), "\t\t\t\t\t\t",
                          colp.print_color("HEADER") + sentences[i])
                case 4:
                    print(colp.print_color("WARNING") + "".join(ligne), "\t\t\t\t\t",
                          colp.print_color("HEADER") + sentences[i])


        else:
            print("".join(ligne))


def respawn_resources(carte):
    for h in range(1, 23):
        for l in range(1, 149):
            if carte[h][l] == "▪️" and random.random() < 0.01:
                carte[h][l] = random.choice(arbres)
            elif carte[h][l] == "▪️" and random.random() < 0.005:
                carte[h][l] = random.choice(cailloux)


def build_building(carte, x, y, resources, batiment, actual_gain):
    if carte[y][x] == "▪️" and batiment in builds:
        building_info = builds[batiment]
        wood_cost = building_info.get("wood_cost", 0)
        stone_cost = building_info.get("stone_cost", 0)
        money_cost = building_info.get("money_cost", 0)
        gain = building_info.get("gain", 0)

        if resources["wood"] >= wood_cost and resources["stone"] >= stone_cost and resources["money"] >= money_cost:
            print("Construction en cours...")
            resources["wood"] -= wood_cost
            resources["stone"] -= stone_cost
            resources["money"] -= money_cost
            actual_gain += gain
            carte[y][x] = building_info["symbol"]

            return resources, actual_gain
        else:
            print("Il vous manque des ressources ! ")
    else:
        print("Le bâtiment n'est pas dans la liste des bâtiments possibles à construire ! ")
    return resources, actual_gain


def get_sentences(state: int):
    match state:
        case 0:
            return (
                "Bonjour chef ! Que souhaitez-vous faire ? (Entrez 0 pour accéder au menu)",
                "1. Se déplacer sur une case (x & y)",
                "2. Récupérer une ressource (Se trouver sur la case de la ressource)",
                "3. Construire un bâtiment",
                "4. Améliorer un bâtiment")
        case 1:
            return colp.print_color("GREEN") + (
                f"""
                ╔                                                                                                    ╗
                                                      ## Bâtiments disponibles ##

                {__format_buildings(builds)}


                ╚                                                                                                    ╝
                """ + colp.print_color("HEADER")
            )
        case 2:
            return (
                "En pleine journée de travail....",
                "",
                "Appuyez sur Q pour quitter le mode automatique",
                "",
                "")


def __format_buildings(builds):
    formatted_buildings = " "
    for i, (name, details) in enumerate(builds.items()):
        color = colp.print_color("GREEN") if i % 2 != 0 else colp.print_color("CYAN")
        if i > 0:
            formatted_buildings += "\t\t\t\t "
        formatted_buildings += color + (
            f"{details['symbol']} {name:<15} "
            f"Coût en argent: {details['money_cost']:<5} "
            f"Coût en bois: {details['wood_cost']:<5} "
            f"Coût en pierre: {details['stone_cost']:<5}"
            f"Argent généré: {details['gain']:<5}\n"
        )
    return formatted_buildings


def find_closest_resource(carte, player_x, player_y):
    closest_resource = None
    min_distance = float("inf")
    resource_positions = []

    for y, row in enumerate(carte):
        for x, cell in enumerate(row):
            if cell in arbres + cailloux:
                resource_positions.append((x, y))

    for resource_x, resource_y in resource_positions:
        distance = abs(player_x - resource_x) + abs(player_y - resource_y)
        if distance < min_distance:
            min_distance = distance
            closest_resource = resource_x, resource_y

    return closest_resource
