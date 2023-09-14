import dearpygui.dearpygui as dpg
import keyboard
from math import sqrt
from PIL import Image
import os
import json

def main():

    class labyrinthe:
        """
        Classe définissant un labirynthe
        """
        def __init__(   self, nom, taille_personnage: float, couleur_fond: tuple[int, int, int], 
                        elements: dict[tuple, tuple, tuple], histoire: str):
            self.nom = nom
            self.fond = "labirynthes/fonds/" + nom + ".png"
            self.murs = "labirynthes/murs/" + nom + ".png"
            self.murs_data = Image.open(os.path.join("data", self.murs))
            self.width, self.height = self.murs_data.size
            self.taille_personnage = taille_personnage
            self.vitesse = round(self.taille_personnage/15)
            self.couleur_fond = couleur_fond
            self.histoire = histoire
            self.elements = elements

        def est_mur(self, pos):
            "vérifie si l'opacité du pixel demandé est > à 200"
            x, y = pos
            return self.murs_data.getpixel((
                x + self.taille_personnage // 2, 
                y + self.taille_personnage // 2))[3] > 200
                    
    class Puzzle:
        def __init__(self, path: str):
            self.path = path
            self.image_actuelle = self.image_to_list()
            self.pieces_totales = sum([
                element == "piece" 
                for laby in LABIRYNTHES[1] 
                for element in laby.elements])
            self.pieces_trouvees = 0
            self.cote_piece = self.width // self.pieces_totales

        def image_to_list(self):
            """transforme un image, en une liste en 1 dimension"""
            myimage = Image.open(os.path.join("data", self.path+".png"))
            self.width, self.height = myimage.size
            return [element/255 
                    for y in range(self.width) 
                    for x in range(self.height) 
                    for element in myimage.getpixel((x, y))]

        def rendre_invisible(self):
            """Rend le puzzle invisble en mettant l'opacité à 0 de chaque 
            pixel de la liste en 1D"""

            for i in range(self.width*self.height):
                self.image_actuelle[3+i*4] = 0.0
            dpg.set_value(self.path, self.image_actuelle)

        def piece_trouvee(self):
            """modifie l'image, afin de faire apparaitre une piece du puzzle"""

            for i in range(
                self.width*self.height//self.pieces_totales*self.pieces_trouvees, 
                self.width*self.height//self.pieces_totales*(self.pieces_trouvees+1)):
                self.image_actuelle[3+i*4] = 1.0

            self.pieces_trouvees += 1
            dpg.configure_item("compteur", label="Pièces obtenues: " + str(self.pieces_trouvees) + "/" + str(self.pieces_totales))
            dpg.set_value(self.path, self.image_actuelle)

            if self.pieces_trouvees == self.pieces_totales:
                with dpg.window(label="victoire", width=ECRAN[0], height=ECRAN[1], no_move=True, no_close=True, no_collapse=True, no_title_bar=True):
                    dpg.add_image("texture_"+COMPOSANTS["planete"].image, tag="planete")
                    dpg.add_button(label="QUITTER LE JEU", width=500, height=90, callback=dpg.stop_dearpygui)

    class Composante:
        def __init__(self, image: str, tutoriel: bool, desciption: str):
            self.image = image
            self.pos = [0, 0]
            self.tutoriel = tutoriel
            self.desciption = desciption

        def set_pos(self, position):
            """Définie la position du Composant"""
            self.pos = position
            dpg.set_item_pos(self.image, self.pos)

        def deplacer(self, mouvement):
            x, y = self.pos
            x_1, y_2 = mouvement
            temp_pos = [max(min(x+x_1, 700-LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage), 0), 
                        max(min(y+y_2, 700-LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage), 0)]
            if not LABIRYNTHES[1][LABIRYNTHES[0]].est_mur(temp_pos) or dpg.get_value("DEBUG_FANTÔME"):
                self.set_pos(temp_pos)

        def lancer(self, element):
            """Lance l'action de l'element"""
            if element == "piece":
                PUZZLE.piece_trouvee()
                LABIRYNTHES[1][LABIRYNTHES[0]].elements.pop(element)
                dpg.configure_item("piece.png", show=False)

            elif element == "portail_avant":
                labirynthe_i(1)

            elif element == "portail_arriere":
                labirynthe_i(-1)

    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', width=ECRAN[0], height=ECRAN[1], resizable=False, vsync=True, clear_color=(0, 0, 0))
        dpg.set_viewport_large_icon(os.path.join("data", "felix.png"))
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def distance(pos_1, pos_2):
        x, y = pos_1
        x_1, y_2 = pos_2
        return sqrt((x-x_1)**2 + (y-y_2)**2)

    def est_proche(pos_1, pos_2):
        return distance(pos_1, pos_2) <= LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage//2

    def labirynthe_i(i):
        """change les interfaces pour faire apparraitre le labyrinthe i"""
        
        LABIRYNTHES[0] += i
        if LABIRYNTHES[0] < 0:
            LABIRYNTHES[0] = len(LABIRYNTHES[1])-1
        elif LABIRYNTHES[0] > len(LABIRYNTHES[1])-1:
            LABIRYNTHES[0] = 0
        
        for composant in COMPOSANTS:
            if composant in LABIRYNTHES[1][LABIRYNTHES[0]].elements:
                COMPOSANTS[composant].set_pos(LABIRYNTHES[1][LABIRYNTHES[0]].elements[composant])
                dpg.configure_item(COMPOSANTS[composant].image, show=True, width=LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage, height=LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage)
            else:
                dpg.configure_item(COMPOSANTS[composant].image, show=False)

        dpg.set_viewport_clear_color(LABIRYNTHES[1][LABIRYNTHES[0]].couleur_fond)
        dpg.configure_item("fond", texture_tag="texture_"+LABIRYNTHES[1][LABIRYNTHES[0]].fond)
        dpg.configure_item("murs", texture_tag="texture_"+LABIRYNTHES[1][LABIRYNTHES[0]].murs)
        dpg.configure_item("histoire_l", default_value="texture_"+LABIRYNTHES[1][LABIRYNTHES[0]].histoire)

    def interface():
        """charge toutes les interfaces"""

        def textures(): # Charges les textures nécéssaires
            with dpg.texture_registry(show=False):
                for image in [COMPOSANTS[key].image for key in COMPOSANTS] + [labi.fond for labi in LABIRYNTHES[1]] + [labi.murs for labi in LABIRYNTHES[1]]:
                    width, height, channels, data = [elt for elt in dpg.load_image(os.path.join("data", image))]
                    dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_"+image)
                
                dpg.add_dynamic_texture(width=PUZZLE.width, height=PUZZLE.height, default_value=PUZZLE.image_actuelle, tag=PUZZLE.path)
                PUZZLE.rendre_invisible()

        def compteur_puzzle(): # compteur de pièces obtenues
            with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
                dpg.add_image(PUZZLE.path, width=ECRAN[0]//3, height=ECRAN[0]//3)

            with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                            no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                            no_background=True, no_title_bar=True, pos=(20, 10)):
                dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(PUZZLE.pieces_trouvees)+"/"+str(PUZZLE.pieces_totales), width= 700)
                with dpg.group(horizontal=True):
                    dpg.add_button(show=True, label="Crédits", tag="Crédits", callback=lambda: dpg.configure_item("fenetre_credits", show=True))
                    dpg.add_checkbox(label="Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))
                    
                    def debug_mode(sender, app_data):
                        for element in ["DEBUG_PRECEDENT", "DEBUG_SUIVANT", "DEBUG_PUZZLE", "DEBUG_X_perso", "DEBUG_Y_perso", "DEBUG_FANTÔME"]:
                            dpg.configure_item(element, show=app_data)

                    dpg.add_checkbox(label="DEBUG", callback=debug_mode)

                    dpg.add_button(show=False, label="PRECEDENT", tag="DEBUG_PRECEDENT", callback= lambda: labirynthe_i(-1))
                    dpg.add_button(show=False, label="SUIVANT", tag="DEBUG_SUIVANT", callback= lambda: labirynthe_i(1))
                    dpg.add_button(show=False, label="PUZZLE + 1", tag="DEBUG_PUZZLE", callback= PUZZLE.piece_trouvee)
                    dpg.add_checkbox(show=False, label="Fantôme", tag="DEBUG_FANTÔME", default_value= False)
                    dpg.add_input_int(show=False, tag="DEBUG_X_perso", width=30, default_value=0, step=0, on_enter=True, callback=lambda: personnage.set_pos([dpg.get_value("DEBUG_X_perso"), dpg.get_value("DEBUG_Y_perso")]))
                    dpg.add_input_int(show=False, tag="DEBUG_Y_perso", width=30, default_value=0, step=0, on_enter=True, callback=lambda: personnage.set_pos([dpg.get_value("DEBUG_X_perso"), dpg.get_value("DEBUG_Y_perso")]))           

        def histoire(): # Fenetre d'histoire
            with dpg.window(label="L'histoire du labirynthe Cosmique", tag="histoire", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True,
                            pos=(ECRAN[0]-530, ECRAN[1] - 790), width=500):
                dpg.add_image("texture_"+COMPOSANTS["logo"].image, pos=(100, 0), width=320, height=180)
                dpg.add_text(tag="histoire_générale", wrap=500, pos=(5, 175), default_value="Un adorable petit chat nommé Personnage se réveille un jour pour découvrir qu'il s'est perdu dans l'immensité de l'univers. Se sentant seul et perdu, Personnage décide de partir à l'aventure pour retrouver son chemin vers sa maison. Pour cela Personnage doit rassembler les morceaux de la carte stellaire sur 4 mystérieuses planètes-labyrinthe. Mais de nombreux obstacles et pièges l'empécheront de rentrer chez lui. \n\n Êtes-vous suffisament malin pour aider Personnage à s'échapper des labyrinthes cosmiques ?")

            with dpg.window(tag="histoire_labi", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=False, no_title_bar=True,
                            pos=(ECRAN[0]-530, ECRAN[1] - 475), width=500, height=130):
                dpg.add_text(tag="histoire_l", wrap=500, pos=(5, 20), default_value="")

        def tuto():# Fenetre tuto
            with dpg.window(tag="fenetre_tuto", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=True, no_title_bar=True,
                            pos=(ECRAN[0]-530, ECRAN[1]-330), width=500):
                with dpg.group(horizontal=True):
                    for image, phrase in [(COMPOSANTS[key].image, COMPOSANTS[key].desciption) for key in COMPOSANTS if COMPOSANTS[key].tutoriel]:
                        with dpg.group():
                            dpg.add_image("texture_"+image, tag=image+"_tuto", width=95, height=95)
                            dpg.add_text(wrap=80, default_value=phrase)
                        dpg.add_spacer(width=12)
                
        def quitter(): # Fenetre quitter
            with dpg.window(tag="fenetre_quitter", no_title_bar=True, no_move=True, no_background=True,
                            pos=(ECRAN[0]-537, ECRAN[1] - 130), autosize=True):
                dpg.add_button(tag="QUITTER", label="QUITTER LE JEU", width=500, height=90, callback=dpg.stop_dearpygui)
        
        def credits():# Fenetre Crédits
            with dpg.window(tag="fenetre_credits", pos=(ECRAN[0]//2, ECRAN[1]//2), autosize=True, show=False, no_scrollbar=True, no_collapse=True):
                dpg.add_button(label="github.com/OKONORE/labyrinthe", tag="github", callback=lambda:webbrowser.open("https://github.com/OKONORE/labyrinthe"))
                dpg.bind_item_theme("github", "__demo_hyperlinkTheme")
                dpg.add_text(tag="text_credits", default_value="""Mathieu THOS\nClémentine GHOSN\nElias PUJOL-HERING\nAntonin SIDHOUM""", wrap = 300)

        def principale(): # Fenetre principale
            with dpg.window(tag="fenetre_principale", show=True, pos=(25, 75), autosize=True,
                            no_move=True, no_title_bar=True, no_scrollbar=True, no_background=True):
                dpg.add_image("texture_"+LABIRYNTHES[1][LABIRYNTHES[0]].fond, tag="fond", pos=(0, 0), width=700, height=700)
                dpg.add_image("texture_"+LABIRYNTHES[1][LABIRYNTHES[0]].murs, tag="murs", pos=(0, 0), width=700, height=700)
                
                for cle in COMPOSANTS:
                    dpg.add_image("texture_"+COMPOSANTS[cle].image, tag=COMPOSANTS[cle].image, pos=[-500,-500], width=LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage, height=LABIRYNTHES[1][LABIRYNTHES[0]].taille_personnage, show=False)

        # Lance toutes les fonctions du GUI
        for fonction in [textures, compteur_puzzle, histoire, tuto, quitter, credits, principale]:
            fonction()

    ECRAN = [1280, 800]

    # Charge les composants entrés dans le composants.json
    
    data = json.load(open('data/composants.json'))
    COMPOSANTS = dict()
    for nom_composant in data:
        COMPOSANTS[nom_composant] = Composante(data[nom_composant]["image"], data[nom_composant]["tutoriel"], data[nom_composant]["description"])
    open('data/composants.json').close()

    # Charge les zones entrées dans le labirynthes.json
    
    data = json.load(open('data/labirynthes/labirynthes.json'))
    LABIRYNTHES = [0, []]
    for i in data:
        LABIRYNTHES[1].append(labyrinthe(i, data[i]["taille_personnage"], data[i]["couleur_fond"], data[i]["elements"], data[i]["histoire"]))

    PUZZLE = Puzzle("puzzle/puzzle1")

    viewport_load()
    
    PIECE = {}
    interface()
    labirynthe_i(LABIRYNTHES[0])

    # BOUCLE PRINCIPALE

    while dpg.is_dearpygui_running():

        if keyboard.is_pressed("down arrow"):
            COMPOSANTS["personnage"].deplacer([0, LABIRYNTHES[1][LABIRYNTHES[0]].vitesse])
        if keyboard.is_pressed("up arrow"):
            COMPOSANTS["personnage"].deplacer([0, -LABIRYNTHES[1][LABIRYNTHES[0]].vitesse])
        if keyboard.is_pressed("left arrow"):
            COMPOSANTS["personnage"].deplacer([-LABIRYNTHES[1][LABIRYNTHES[0]].vitesse, 0])
        if keyboard.is_pressed("right arrow"):
            COMPOSANTS["personnage"].deplacer([LABIRYNTHES[1][LABIRYNTHES[0]].vitesse, 0])

        dpg.configure_item("DEBUG_Y_perso", default_value=COMPOSANTS["personnage"].pos[1])
        dpg.configure_item("DEBUG_X_perso", default_value=COMPOSANTS["personnage"].pos[0])
        
        for composant in COMPOSANTS:
            
            if composant != "personnage" and composant in LABIRYNTHES[1][LABIRYNTHES[0]].elements and est_proche(COMPOSANTS["personnage"].pos, COMPOSANTS[composant].pos):
                COMPOSANTS[composant].lancer(composant)

        dpg.render_dearpygui_frame()

    dpg.destroy_context()

main()