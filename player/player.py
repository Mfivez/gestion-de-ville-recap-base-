previous_tile = "▪️"
posX = 1
posY = 1


""" MODE MANUEL """


def move(x, y, carte, player="🙎‍♂️"):
    global previous_tile, posX, posY
    current_pos = get_player_pos()
    carte[current_pos["posY"]][current_pos["posX"]] = previous_tile
    set_player_pos(x, y)
    previous_tile = carte[y][x]
    carte[y][x] = player


def get_player_pos():
    return {"posY": posY, "posX": posX}


def set_player_pos(x, y):
    global posX, posY
    posX = x
    posY = y


def break_ressource(bois: int, pierre: int):
    global previous_tile

    if previous_tile in "🌲🌳🌴🪨":
        match previous_tile:
            case "🌲": bois += 3
            case "🌳": bois += 5
            case  "🌴": bois += 7
            case "🪨": pierre += 5
        previous_tile = "▪️"
    return bois, pierre


""" MODE AUTO """


def move_towards(player_x, player_y, target_x, target_y):
    if player_x < target_x:
        player_x += 1
    elif player_x > target_x:
        player_x -= 1

    if player_y < target_y:
        player_y += 1
    elif player_y > target_y:
        player_y -= 1

    return player_x, player_y
