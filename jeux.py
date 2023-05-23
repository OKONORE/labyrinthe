import dearpygui.dearpygui as dpg
import os
import keyboard
from PIL import Image
from pprint import pprint

# Classes

class labirynthe:
    """
    Classe définissant un labirynthe
    """
    def __init__(self, taille_personnage: int, image, pos_depart: tuple):
        self.taille_personnage = taille_personnage
        self.pos_depart = pos_depart
        self.image = image


class Puzzle:
    def __init__(self, image):
        self.image_path = image
        #self.image_list = image_to_list()

    def puzzle_actuel(self):
        pass

# fonctions

def image_to_list(image_path):

    image_filepath = 'pixel_avatar.png'
    myimage = Image.open(image_path)
    width, height = myimage.size
    return [composant for composant in myimage.getpixel((x, y)) for x in range(width) for y in range(height)]

def main():
    x = 10

    dpg.create_context()
    dpg.create_viewport(title='Labirynthe', resizable=True, vsync=True, clear_color=(0, 0, 0))
    dpg.setup_dearpygui()
    dpg.show_viewport(maximized=True)
    ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()]
    Puzzle_actif = Puzzle(os.path.join("data/", "personnage.png"))


    # compteur de pièces obtenues

    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image(os.path.join("data/", "image_test.jpg"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="img_test")
    with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
        dpg.add_image("img_test", tag="image_test", pos=(0, 0), width=500, height=500)

    with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                    no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                    no_background=True, no_title_bar=True, pos=(10, 10)):
        dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(x), width=ECRAN[0]//6)
        dpg.add_checkbox(label="Afficher Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))

    # Fenetre principale

    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image(os.path.join("data/", "personnage.png"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="personnage")

    with dpg.window(tag="fenetre_principale", show=True, pos=(ECRAN[0]//12, ECRAN[1]//12), width=ECRAN[0]-50, height=ECRAN[1]-100,
                    no_move=True, no_title_bar=True):
        dpg.add_image("personnage", tag="personnage1", pos=(0, 0), width=50, height=50)


    with dpg.texture_registry(show=True):
        dpg.add_raw_texture(width=316, height=316, default_value=image_to_list("data/personnage.png"), format=dpg.mvFormat_Float_rgba, tag="texture_tag")


    # BOUCLE PRINCIPALE
    while dpg.is_dearpygui_running():
        ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()] # Update les dimensions de l'écran à chaque frame
        dpg.configure_item("compteur", label="Pièces obtenues: " + str(x),)

        dpg.configure_item("fenetre_principale", width=500, height=500, pos=(50, 100))

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


#main()

print(image_to_list("data/personnage.png"))