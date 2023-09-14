import dearpygui.dearpygui as dpg
import keyboard
from math import sqrt
from PIL import Image
import os
import webbrowser

id_labyrinthe = 0

def main():

    class labyrinthe:
        """
        Classe définissant un labirynthe
        """
        def __init__(   self, nom, taille_personnage: float, pos_depart, couleur_fond: tuple[int, int, int], 
                        elements: dict[tuple, tuple, tuple], histoire: str):
            self.nom = nom
            self.fond = "labirynthes/" + nom + ".png"
            self.murs = "fonds/" + nom + ".png"
            self.murs_data = Image.open(os.path.join("data", self.murs))
            self.width, self.height = self.murs_data.size
            self.taille_personnage = taille_personnage
            self.vitesse = round(self.taille_personnage/15)
            self.pos_depart = pos_depart
            self.couleur_fond = couleur_fond
            self.histoire = histoire
            self.elements = elements

        def est_mur(self, pos):
            "vérifie si l'opacité du pixel demandé est > à 200"
            x, y = pos
            return self.murs_data.getpixel((
                x + self.taille_personnage // 2, 
                y + self.taille_personnage // 2))[3] > 200

        def lancer(self, element):
            """Lance l'action de l'element"""
            if element == "PIECE":
                PUZZLE.piece_trouvee()
                LABYRINTHES[id_labyrinthe].elements[element] = None
                dpg.configure_item("PIECE", show=False)

            elif element == "PORTAIL_AVANT":
                labirynthe_i(1)
            elif element == "PORTAIL_ARRIERE":
                labirynthe_i(-1)
                    
    class Puzzle:
        def __init__(self, path: str):
            self.path = path
            self.image_actuelle = self.image_to_list()
            self.pieces_totales = sum([
                element == "piece" 
                for laby in LABYRINTHES 
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
                    dpg.add_image("planete")
                dpg.configure_item("puzzle", show=True)

    class Composante:
        def __init__(self, image):
            self.image = image
            self.pos = [0, 0]

        def set_pos(self, position):
            """Définie la position de Composant"""
            self.pos = position
            dpg.configure_item("texture_"+image, pos=self.pos)

        def deplacer(self, mouvement):
            x, y = self.pos
            x_1, y_2 = mouvement
            temp_pos = [max(min(x+x_1, 700-LABYRINTHES[id_labyrinthe].taille_personnage), 0), 
                        max(min(y+y_2, 700-LABYRINTHES[id_labyrinthe].taille_personnage), 0)]
            if not LABYRINTHES[id_labyrinthe].est_mur(temp_pos) or dpg.get_value("DEBUG_FANTÔME"):
                self.set_pos(temp_pos)

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
        return distance(pos_1, pos_2) <= LABYRINTHES[id_labyrinthe].taille_personnage//2

    def labirynthe_i(i):
        """change les interfaces pour faire apparraitre le labyrinthe i"""
        
        global id_labyrinthe
        
        for element in LABYRINTHES[id_labyrinthe].elements:
            dpg.configure_item(element, show=False)


        for element in LABYRINTHES[id_labyrinthe].elements:
            if not LABYRINTHES[id_labyrinthe].elements[element] is None:
                dpg.configure_item(element, show=True, pos=LABYRINTHES[id_labyrinthe].elements[element], width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)

        PERSONNAGE.set_pos(LABYRINTHES[id_labyrinthe].pos_depart)
        dpg.set_viewport_clear_color(LABYRINTHES[id_labyrinthe].couleur_fond)
        dpg.configure_item("Personnage", width=LABYRINTHES[id_labyrinthe].taille_personnage , height=LABYRINTHES[id_labyrinthe].taille_personnage)
        dpg.configure_item("fond", texture_tag=LABYRINTHES[id_labyrinthe].fond)
        dpg.configure_item("murs", texture_tag=LABYRINTHES[id_labyrinthe].murs)
        dpg.configure_item("histoire_l", default_value=LABYRINTHES[id_labyrinthe].histoire)

    def interface():
        """charge toutes les interfaces"""

        def textures(): # Charges les textures nécéssaires
            with dpg.texture_registry(show=False):
                for image in [COMPOSANTES[key].image for key in COMPOSANTES] + [labi.fond for labi in LABYRINTHES] + [labi.murs for labi in LABYRINTHES]:
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
                dpg.add_image("logo.png", pos=(100, 0), width=320, height=180)
                dpg.add_text(tag="histoire_générale", wrap=500, pos=(5, 175), default_value="Un adorable petit chat nommé Personnage se réveille un jour pour découvrir qu'il s'est perdu dans l'immensité de l'univers. Se sentant seul et perdu, Personnage décide de partir à l'aventure pour retrouver son chemin vers sa maison. Pour cela Personnage doit rassembler les morceaux de la carte stellaire sur 4 mystérieuses planètes-labyrinthe. Mais de nombreux obstacles et pièges l'empécheront de rentrer chez lui. \n\n Êtes-vous suffisament malin pour aider Personnage à s'échapper des labyrinthes cosmiques ?")

            with dpg.window(tag="histoire_labi", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=False, no_title_bar=True,
                            pos=(ECRAN[0]-530, ECRAN[1] - 475), width=500, height=130):
                dpg.add_text(tag="histoire_l", wrap=500, pos=(5, 20), default_value="")

        def tuto():# Fenetre tuto
            with dpg.window(tag="fenetre_tuto", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=True, no_title_bar=True,
                            pos=(ECRAN[0]-530, ECRAN[1]-330), width=500):
                with dpg.group(horizontal=True):
                    for image, phrase in [("piece.png", "C'est une pièce de la carte, trouvez la"), ("portail_avant.png", "C'est un portail, il vous emmenera a un autre niveau") , ("felix.png", "C'est vous, felix"), ("fleches.png", "Utilisez les flèches pour vous déplacer")]:
                        with dpg.group():
                            dpg.add_image(image, tag=image+"_tuto", width=95, height=95)
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
                dpg.add_image(LABYRINTHES[id_labyrinthe].fond, tag="fond", pos=(0, 0), width=700, height=700)
                dpg.add_image(LABYRINTHES[id_labyrinthe].murs, tag="murs", pos=(0, 0), width=700, height=700)
                dpg.add_image("texture_"+COMPOSANTES["personnage"].image, tag="Personnage", pos=(0,0), width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)
                dpg.add_image("texture_"+COMPOSANTES["piece"].image, tag="PIECE", pos=[580, 520], width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)
                dpg.add_image("texture_"+COMPOSANTES["portail_avant"].image, tag="PORTAIL_AVANT", pos=[580, 520], width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)
                dpg.add_image("texture_"+COMPOSANTES["portail_arriere"].image, tag="PORTAIL_ARRIERE", show=False, pos=[110, 120], width=LABYRINTHES[id_labyrinthe].taille_personnage, height=LABYRINTHES[id_labyrinthe].taille_personnage)

        # Lance toutes les fonctions du GUI
        for fonction in [textures, compteur_puzzle, histoire, tuto, quitter, credits, principale]:
            fonction()

    ECRAN = [1280, 800]
    
    COMPOSANTES = {
        "personnage":       Composante("felix.png"),
        "logo":             Composante("logo.png"),
        "piece":            Composante("piece.png"),
        "portail_avant":    Composante("portail_avant.png"),
        "portail_arriere":  Composante("portail_arriere.png"),
        "fleches":          Composante("fleches.png"),
        "planete":          Composante("planete.png"),
    }

    LABYRINTHES = [
        labyrinthe("plaine", 40, [10, 20],   (9, 74, 0),      {"piece":[580, 520], "portail_avant":[210, 580], "portail_arriere":[70, 205]}, "La Planète Verdura est un endroit luxuriant et verdoyant, avec de grands arbres qui s'élèvent vers le ciel. Les chemins serpentent entre les racines entrelacées et les plantes exotiques. Le fragment de la carte stellaire se trouve au sommet d'une ancienne tour cachée au cœur de la forêt."),
        labyrinthe("desert", 50, [60, 60],   (219, 76, 33),   {"piece":[320, 330], "portail_avant":[190, 600], "portail_arriere":[460, 600]}, "La Planète Sableon est un paysage aride et impitoyable, avec des dunes de sable à perte de vue et des tempêtes de sable occasionnelles. Le soleil brille intensément dans un ciel sans nuages. Le fragment de la carte stellaire est enfoui dans une ancienne pyramide perdue sous le sable. "), 
        labyrinthe("nuages", 40, [365, 20],  (122, 214, 235), {"piece":[330, 330], "portail_avant":[20, 360], "portail_arriere":[570, 520]}, "La Planète Nimbroa est un monde céleste rempli de nuages moelleux et de paysages oniriques. Les nuages prennent des formes fantastiques et l' étoile brille aux couleurs charmantes. À première vue, elle peut paraître paisible et paradisiaque mais c'est en réalité une des planètes les plus dangereuses. Le fragment de la carte stellaire se cache, cette fois, au sommet d'une montagne de nuages majestueuse. "), 
        labyrinthe("lave",   30,   [290, 70],  (117, 1, 1),   {"piece":[480, 70],  "portail_avant":[90, 240], "portail_arriere":[380, 570]}, "La Planète Mustafar est un monde tumultueux rempli de volcans en éruption et de rivières de lave brûlante. Des flammes dansent sur la surface, créant une lueur sinistre dans un ciel sombre. Le fragment de la carte stellaire se trouve dans un sanctuaire au cœur d'un volcan actif.  Mais Personnage devra d'abord traverser des plateformes instables, éviter toutes éruptions volcaniques et résister à la chaleur étouffante."),
                ]


    
    PUZZLE = [Puzzle("puzzle/puzzle1")][0]
    


    viewport_load()
    
    PIECE = {}
    interface()
    labirynthe_i(id_labyrinthe)

    # BOUCLE PRINCIPALE

    while dpg.is_dearpygui_running():

        if keyboard.is_pressed("down arrow"):
            PERSONNAGE.deplacer([0, LABYRINTHES[id_labyrinthe].vitesse])
        if keyboard.is_pressed("up arrow"):
            PERSONNAGE.deplacer([0, -LABYRINTHES[id_labyrinthe].vitesse])
        if keyboard.is_pressed("left arrow"):
            PERSONNAGE.deplacer([-LABYRINTHES[id_labyrinthe].vitesse, 0])
        if keyboard.is_pressed("right arrow"):
            PERSONNAGE.deplacer([LABYRINTHES[id_labyrinthe].vitesse, 0])

        dpg.configure_item("DEBUG_Y_perso", default_value=PERSONNAGE.pos[1])
        dpg.configure_item("DEBUG_X_perso", default_value=PERSONNAGE.pos[0])
        
        for element in LABYRINTHES[id_labyrinthe].elements:
            if not LABYRINTHES[id_labyrinthe].elements[element] is None:
                if est_proche(PERSONNAGE.pos, LABYRINTHES[id_labyrinthe].elements[element]):
                    LABYRINTHES[id_labyrinthe].lancer(element)

        dpg.render_dearpygui_frame()

    dpg.destroy_context()

main()