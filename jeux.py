import dearpygui.dearpygui as dpg
import os
import keyboard
import array
from math import sqrt
from PIL import Image

# Classes

class labyrinthe:
    """
    Classe définissant un labirynthe
    """
    def __init__(self, taille_personnage: float, murs: str, fond: str, pos_depart: tuple[int, int], elements_speciaux: list):
        self.fond = fond
        self.taille_personnage = taille_personnage
        self.pos_depart = pos_depart


class Puzzle:
    def __init__(self, path):
        self.path = path
        self.image_actuelle = self.image_to_list()
        self.pieces_totales = 4
        self.pieces_trouvees = 0

    def image_to_list(self):
        myimage = Image.open("data/"+self.path+".png")
        self.width, self.height = myimage.size
        return [element/255 for y in range(self.width) for x in range(self.height) for element in myimage.getpixel((x, y))]

    def rendre_invisible(self):
        for i in range(3, self.width*self.height*4, 4):
            self.image_actuelle[i] = 0.0
        dpg.set_value(self.path, self.image_actuelle)

    def piece_trouve(self):
        racine = sqrt(self.pieces_totales)
        cote = self.width // racine

        ##### ICIC FAIRE LA BOUCLE POUR L'IMAGE EN 1D

        self.pieces_trouvees += 1
        update_responsive()


def main():

    class Position:
        def __init__(self):
            self.pos = [0, 0]
            self.taille_ecran = min(ECRAN)

        def resize(self, ecran):
            delta = self.taille_ecran // min(ecran)
            self.pos = [self.pos[0]-delta, self.pos[1]-delta]
            self.taille_ecran = min(ecran)
            return self.pos

        def haut(self, vitesse):
            self.pos[1] = max(0, self.pos[1]-vitesse)
            return self.pos
        def bas(self, vitesse):
            self.pos[1] = min(min(ECRAN), self.pos[1]+vitesse)
            return self.pos
        def gauche(self, vitesse):
            self.pos[0] = max(0, self.pos[0]-vitesse)
            return self.pos
        def droite(self, vitesse):
            self.pos[0] = min(min(ECRAN), pos[0]+vitesse)
            return self.pos

    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', resizable=True, vsync=True, clear_color=(0, 0, 0))
        dpg.setup_dearpygui()
        dpg.set_viewport_resize_callback(update_responsive)
        dpg.show_viewport(maximized=True)


    def update_responsive():
        ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
        dpg.configure_item("fond", width=min(ECRAN)-100, height=min(ECRAN)-100)
        dpg.configure_item("compteur", label="Pièces obtenues: " + str(PUZZLE.pieces_trouvees) + "/" + str(PUZZLE.pieces_totales), width=ECRAN[0]-30)
        dpg.configure_item("Personnage", pos=Position_perso.resize(ECRAN), width=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage, height=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage)


    viewport_load()
    ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
    PUZZLE = Puzzle("puzzle/1")
    LABYRINTHES = [ labyrinthe(1.0 , None, "fonds/plaine",  (0, 0), []), 
                    labyrinthe(1.0 , None, "fonds/nuages",  (0, 0), []), 
                    labyrinthe(1.0 , None, "fonds/desert",  (0, 0), []), 
                    labyrinthe(1.0 , None, "fonds/lave",    (0, 0), [])
                    ]
    VITESSE = 10
    Position_perso = Position()

    id_labyrinthe = 0

    # chargement des textures

    with dpg.texture_registry(show=False): # registre des textures chargées
        for image in [  "personnage", 
                        "fonds/nuages", "fonds/lave", "fonds/desert", "fonds/plaine",
                        
                        ]:
            width, height, channels, data = [elt for elt in dpg.load_image("data/"+image+".png")]
            dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag=image)
        dpg.add_dynamic_texture(width=375, height=375, default_value=PUZZLE.image_actuelle, tag=PUZZLE.path)
        PUZZLE.rendre_invisible()

    # compteur de pièces obtenues

    with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
        dpg.add_image(PUZZLE.path, width=ECRAN[0]//3, height=ECRAN[0]//3)

    with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                    no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                    no_background=True, no_title_bar=True, pos=(10, 10)):
        dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(1), width=ECRAN[0]//6)
        dpg.add_checkbox(label="Afficher Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))

    # Fenetre principale

    with dpg.window(tag="fenetre_principale", show=True, pos=(50, 75), autosize=True,
                    no_move=True, no_title_bar=True, no_scrollbar=True, no_background=True):
        dpg.add_image(LABYRINTHES[id_labyrinthe].fond, tag="fond", pos=(0, 0), width=min(ECRAN)-100, height=min(ECRAN)-100)
        dpg.add_image(  "personnage", tag="Personnage", pos=LABYRINTHES[id_labyrinthe].pos_depart, 
                        width=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage, height=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage)

    # BOUCLE PRINCIPALE

    while dpg.is_dearpygui_running():

        Vitesse = round(LABYRINTHES[id_labyrinthe].taille_personnage*VITESSE)
        if keyboard.is_pressed("down arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=Position_perso.bas(Vitesse))
        if keyboard.is_pressed("up arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=Position_perso.haut(Vitesse))
        if keyboard.is_pressed("left arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=Position_perso.gauche(Vitesse))
        if keyboard.is_pressed("right arrow"):
            pos = dpg.get_item_pos("Personnage")
            dpg.configure_item("Personnage", pos=Position_perso.droite(Vitesse))
        
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

main()