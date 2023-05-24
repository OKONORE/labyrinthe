import dearpygui.dearpygui as dpg
import os
import keyboard
import array
from math import sqrt

# Classes

class labirynthe:
    """
    Classe définissant un labirynthe
    """
    def __init__(self, taille_personnage: int, image: str, pos_depart: tuple[int, int], precedent):
        self.taille_personnage = taille_personnage
        self.pos_depart = pos_depart
        self.image = image
        self.precedent = precedent



class Puzzle:
    def __init__(self, nom, path):
        self.nom = nom
        self.width, self.height, _, self.data  = dpg.load_image(path)
        self.pieces_totales = 4
        self.pieces_trouvees = 0
        self.pieces = self.diviser_image()

    def piece_trouve(self):
        self.pieces_trouvees += 1

    def diviser_image(self):
        racine = round(sqrt(self.pieces_totales))
        cote = self.width // racine




# fonctions


def main():
    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', resizable=True, vsync=True, clear_color=(0, 0, 0))
        dpg.setup_dearpygui()
        dpg.set_viewport_resize_callback(update_responsive)
        dpg.show_viewport(maximized=True)

    def update_responsive():
        dpg.configure_item("fenetre_principale", width=min(ECRAN)//100*100, height=min(ECRAN)//100*100, pos=(50, 100))

    viewport_load()
    ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]

    puzzle = Puzzle("Premier Puzzle", "data/puzzle/1.png")
    # chargement des textures

    with dpg.texture_registry(show=False): # registre des textures chargées
        for image in ["personnage", "image_test"]:
            width, height, channels, data = [elt for elt in dpg.load_image("data/"+image+".png")]
            dpg.add_raw_texture(width=width, height=height, default_value=data, format=dpg.mvFormat_Float_rgba, tag=image)

    # compteur de pièces obtenues

    with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
        dpg.add_image("image_test", width=500, height=500)
        
    with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                    no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                    no_background=True, no_title_bar=True, pos=(10, 10)):
        dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(1), width=ECRAN[0]//6)
        dpg.add_checkbox(label="Afficher Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))

    # Fenetre principale

    
    with dpg.window(tag="fenetre_principale", show=True, pos=(100, 100), autosize=True,
                    no_move=True, no_title_bar=True):
        dpg.add_image("personnage", tag="personnage1", pos=(0, 0), width=500, height=500)

    # BOUCLE PRINCIPALE
    while dpg.is_dearpygui_running():
        ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()] # Update les dimensions de l'écran à chaque frame
        dpg.configure_item("compteur", label="Pièces obtenues: " + str(puzzle.pieces_trouvees) + "/" + str(puzzle.pieces_totales))
        
        if keyboard.is_pressed("down arrow"):
            pass
        if keyboard.is_pressed("up arrow"):
            pass
        if keyboard.is_pressed("left arrow"):
            pass
        if keyboard.is_pressed("right arrow"):
            pass
            

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


main()