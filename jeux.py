import dearpygui.dearpygui as dpg
import os
import keyboard
import array
from math import sqrt

# Classes

class labyrinthe:
    """
    Classe définissant un labirynthe
    """
    def __init__(self, taille_personnage: int, murs: str, fond: str, pos_depart: tuple[int, int], elements_speciaux: list):
        self.fond = fond
        self.taille_personnage = taille_personnage


class Puzzle:
    def __init__(self, path):
        self.path = path
        self.width, self.height, _, self.data  = dpg.load_image("data/"+path+".png")
        self.pieces_totales = 4
        self.pieces_trouvees = 0
        self.pieces = self.diviser_image()

    def piece_trouve(self):
        self.pieces_trouvees += 1

    def diviser_image(self):
        racine = round(sqrt(self.pieces_totales))
        cote = self.width // racine

def main():
    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', resizable=True, vsync=True, clear_color=(0, 0, 0))
        dpg.setup_dearpygui()
        dpg.set_viewport_resize_callback(update_responsive)
        dpg.show_viewport(maximized=True)

    def update_responsive():
        ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
        dpg.configure_item("fond", width=(min(ECRAN))-100, height=(min(ECRAN))-100)
        dpg.configure_item("compteur", label="Pièces obtenues: " + str(PUZZLE.pieces_trouvees) + "/" + str(PUZZLE.pieces_totales), width=ECRAN[0]-30)

    viewport_load()
    ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
    PUZZLE = Puzzle("puzzle/1")
    LABYRINTHES = [labyrinthe(100, None, "fonds/nuages", (0, 0), [])]
    id_labyrinthe = 0

    # chargement des textures

    with dpg.texture_registry(show=False): # registre des textures chargées
        for image in ["personnage", "puzzle/1", "fonds/nuages", "fonds/lave"]:
            width, height, channels, data = [elt for elt in dpg.load_image("data/"+image+".png")]
            dpg.add_raw_texture(width=width, height=height, default_value=data, format=dpg.mvFormat_Float_rgba, tag=image)

    # compteur de pièces obtenues

    with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
        dpg.add_image(PUZZLE.path, width=500, height=500)
        
    with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                    no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                    no_background=True, no_title_bar=True, pos=(10, 10)):
        dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(1), width=ECRAN[0]//6)
        dpg.add_checkbox(label="Afficher Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))

    # Fenetre principale

    with dpg.window(tag="fenetre_principale", show=True, pos=(50, 75), autosize=True,
                    no_move=True, no_title_bar=True, no_scrollbar=True, no_background=True):
        dpg.add_image(LABYRINTHES[id_labyrinthe].fond, tag="fond", pos=(0, 0), width=500, height=500)
        dpg.add_image("personnage", tag="Personnage", pos=(0, 0), width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)

    # BOUCLE PRINCIPALE

    while dpg.is_dearpygui_running():
  
        if keyboard.is_pressed("down arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=(pos[0], pos[1]+10))
        if keyboard.is_pressed("up arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=(pos[0], pos[1]-10))
        if keyboard.is_pressed("left arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=(pos[0]-10, pos[1]))
        if keyboard.is_pressed("right arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=(pos[0]+10, pos[1]))

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


main()