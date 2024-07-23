import random
import UI.map as context_ui
import player.player as pl
import time
import keyboard

run = True
village, menu = context_ui.generate_context(150, 24)
game_state = 0
pl.move(1, 1, village)
resources = {"money": 0, "wood": 5, "stone": 5}
game_mode = "manuel"
gain_per_print = 0

if __name__ == "__main__":
    while run:
        resources["money"] += gain_per_print
        context_ui.fill_menu(
            menu, bois =resources.get("wood"), argent=resources.get("money"), pierre=resources.get("stone")
        )

        context_ui.draw_game(village, menu, game_state)
        if game_mode == "manuel":
            try:
                match int(input("On vous écoute : ")):
                    case 0 :
                        match int(input(""" Options :
                            1. Passer en mode automatique.
                            2. Quitter la partie. """)
                                  ):
                            case 1:
                                game_mode = "automatique"
                                game_state = 2
                            case 2: run = False

                    case 1 :
                        pl.move(int(input("Position en x :")), int(input("Position en y :")), village)
                    case 2 :
                        resources["wood"], resources["stone"] = pl.break_ressource(resources.get("wood"), resources.get("stone"))
                        # context_ui.fill_menu(menu, bois=resources.get("wood"), pierre=resources.get("stone"))
                    case 3 :
                        x = int(input("Position en x :"))
                        y = int(input("Position en y :"))
                        print(context_ui.get_sentences(1))
                        batiment = input("Quel bâtiment souhaitez-vous construire (maison, bureau, etc.) ? ")

                        resources, gain_per_print = context_ui.build_building(
                            village, x, y, resources, batiment, gain_per_print
                        )

                        time.sleep(2)
                    case 4 :
                        print("Amélioration")
            except:
                print("Rentre un nombre présent dans les options !")
                time.sleep(2)
        else:
            closest_resource = context_ui.find_closest_resource(
                village,
                pl.get_player_pos().get("posX"),
                pl.get_player_pos().get("posY")
            )

            if closest_resource:
                player_x, player_y = pl.move_towards(
                    pl.get_player_pos().get("posX"),
                    pl.get_player_pos().get("posY"),
                    closest_resource[0],
                    closest_resource[1]
                )

                if village[player_y][player_x] in "🌲🌳🌴🪨":
                    pl.move(player_x, player_y, village)
                    resources["wood"], resources["stone"] = pl.break_ressource(resources.get("wood"),
                                                                               resources.get("stone"))
                    context_ui.fill_menu(menu, bois=resources.get("wood"), pierre=resources.get("stone"))
                else :
                    pl.move(player_x, player_y, village)

            if keyboard.is_pressed("q"):
                game_mode = "manuel"
                game_state = 0
                print("Passage en mode manuel")

            time.sleep(1)

        if random.random() < 0.05:
            context_ui.respawn_resources(village)
