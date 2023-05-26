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
    def __init__(self, taille_personnage: float, murs: str, fond: str, pos_depart: tuple[int, int], couleur_fond: tuple[int, int, int], elements_speciaux: list, histoire: str):
        self.fond = fond
        self.murs = murs
        self.murs_data = Image.open("data/"+self.murs+".png")
        self.width, self.height = self.murs_data.size
        self.taille_personnage = taille_personnage
        self.pos_depart = pos_depart
        self.couleur_fond = couleur_fond
        self.histoire = histoire

    def est_mur(self, pos):
        return self.murs_data.getpixel((pos[0]+self.taille_personnage//2, pos[1]+self.taille_personnage//2))[3] > 200

class Special:
    def __init__(self, type, image, pos, callback):
        self.type = type



class Puzzle:
    def __init__(self, path):
        self.path = path
        self.image_actuelle = self.image_to_list()
        self.pieces_totales = 4
        self.pieces_trouvees = 0

    def image_to_list(self):
        """transforme un image, en une liste en 1 dimension"""

        myimage = Image.open("data/"+self.path+".png")
        self.width, self.height = myimage.size
        return [element/255 for y in range(self.width) for x in range(self.height) for element in myimage.getpixel((x, y))]

    def rendre_invisible(self):
        """Rend le puzzle invisble en mettant l'opacité à 0 de chaque pixel de la liste en 1D"""

        for i in range(3, self.width*self.height*4, 4):
            self.image_actuelle[i] = 0.0
        dpg.set_value(self.path, self.image_actuelle)

    def piece_trouve(self):
        """modifie l'image, afin de faire apparaitre un coin du puzzle"""

        cote = round(self.width // sqrt(self.pieces_totales))
        if self.pieces_trouvees == 0:
            for y in [i*4 for i in range(0, cote*cote*2, cote*2)]:
                for x in range(3+y, y+cote*4, 4):
                    self.image_actuelle[x] = 1.0
        elif self.pieces_trouvees == 1:
            for y in [-i*4 for i in range(0, -cote*cote*2, -cote*2)]:
                for x in range(-3+y, y+cote*4, 4):
                    self.image_actuelle[-x] = 1.0
        elif self.pieces_trouvees == 2:
            for y in [i*4 for i in range(cote*cote*2, cote*cote*4, cote*2)]:
                for x in range(3+y, y+cote*4, 4):
                    self.image_actuelle[x] = 1.0
        elif self.pieces_trouvees == 3:
            for y in [-i*4 for i in range(-cote*cote*2, -cote*cote*4, -cote*2)]:
                for x in range(-3+y, y+cote*4, 4):
                    self.image_actuelle[-x] = 1.0
            
        self.pieces_trouvees += 1
        dpg.configure_item("compteur", label="Pièces obtenues: " + str(self.pieces_trouvees)+"/"+str(self.pieces_totales))
        dpg.set_value(self.path, self.image_actuelle)

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

        def set_pos(self, position):
            self.pos = position
            dpg.configure_item("Personnage", pos=self.pos)

        def haut(self, vitesse):
            temp_pos = [self.pos[0], max(0, self.pos[1]-vitesse)]
            if not LABYRINTHES[id_labyrinthe].est_mur(temp_pos):
                self.pos[1] = temp_pos[1]
            return self.pos
        def bas(self, vitesse):
            temp_pos = [self.pos[0], min(700-LABYRINTHES[id_labyrinthe].taille_personnage, self.pos[1]+vitesse)]
            if not LABYRINTHES[id_labyrinthe].est_mur(temp_pos):
                self.pos[1] = temp_pos[1]
            return self.pos
        def gauche(self, vitesse):
            temp_pos = [max(0, self.pos[0]-vitesse), self.pos[1]]
            if not LABYRINTHES[id_labyrinthe].est_mur(temp_pos):
                self.pos[0] = temp_pos[0]
            return self.pos
        def droite(self, vitesse):
            temp_pos = [min(700-LABYRINTHES[id_labyrinthe].taille_personnage, self.pos[0]+vitesse), self.pos[1]]
            if not LABYRINTHES[id_labyrinthe].est_mur(temp_pos):
                self.pos[0] = temp_pos[0]
            return self.pos

    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', width=ECRAN[0], height=ECRAN[1], resizable=False, vsync=True, clear_color=(0, 0, 0))
        dpg.set_viewport_large_icon("data/personnage.png")
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def labirynthe_i(i):
        """change les interfaces pour faire apparraitre le prochain labyrinthe"""

        global id_labyrinthe
        id_labyrinthe += i
        if id_labyrinthe >= len(LABYRINTHES):
            id_labyrinthe = 0
        elif id_labyrinthe < 0:
            id_labyrinthe = len(LABYRINTHES)-1

        Position_perso.pos = LABYRINTHES[id_labyrinthe].pos_depart
        dpg.set_viewport_clear_color(LABYRINTHES[id_labyrinthe].couleur_fond)
        dpg.configure_item("Personnage", pos=LABYRINTHES[id_labyrinthe].pos_depart, width=LABYRINTHES[id_labyrinthe].taille_personnage , height=LABYRINTHES[id_labyrinthe].taille_personnage)
        dpg.configure_item("fond", texture_tag=LABYRINTHES[id_labyrinthe].fond)
        dpg.configure_item("murs", texture_tag=LABYRINTHES[id_labyrinthe].murs)
        dpg.configure_item("histoire_l", default_value=LABYRINTHES[id_labyrinthe].histoire)
    
    def interface():
        """charge toutes les interfaces"""

        # chargement des textures
        with dpg.texture_registry(show=False): # registre des textures chargées
            for image in [ 
                "personnage", "logo", "piece", "portail", "fleches",
                "fonds/nuages", "fonds/lave", "fonds/desert", "fonds/plaine",
                "labirynthes/1", "labirynthes/2", "labirynthes/3", "labirynthes/4",
                        ]:
                width, height, channels, data = [elt for elt in dpg.load_image("data/"+image+".png")]
                dpg.add_static_texture(width=width, height=height, default_value=data, tag=image)
            dpg.add_dynamic_texture(width=PUZZLE.width, height=PUZZLE.height, default_value=PUZZLE.image_actuelle, tag=PUZZLE.path)
            PUZZLE.rendre_invisible()

        # compteur de pièces obtenues

        with dpg.window(label="puzzle", tag="puzzle", autosize=True, no_close=True, no_collapse=True, show=False):
            dpg.add_image(PUZZLE.path, width=ECRAN[0]//3, height=ECRAN[0]//3)

        with dpg.window(tag="compteur_pieces", autosize=True, no_move=True,
                        no_bring_to_front_on_focus=True, no_focus_on_appearing=True,
                        no_background=True, no_title_bar=True, pos=(20, 10)):
            dpg.add_button(tag="compteur", label="Pièces obtenues: " + str(PUZZLE.pieces_trouvees)+"/"+str(PUZZLE.pieces_totales), width= 700)
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))
                
                def debug_mode(sender, app_data):
                    for element in ["DEBUG_PRECEDENT", "DEBUG_SUIVANT", "DEBUG_PUZZLE", "DEBUG_X_perso", "DEBUG_Y_perso"]:
                        dpg.configure_item(element, show=app_data)

                dpg.add_checkbox(label="DEBUG MODE", callback=debug_mode)

                dpg.add_button(show=False, label="DEBUG_PRECEDENT", tag="DEBUG_PRECEDENT", callback= lambda: labirynthe_i(-1))
                dpg.add_button(show=False, label="DEBUG_SUIVANT", tag="DEBUG_SUIVANT", callback= lambda: labirynthe_i(1))
                dpg.add_button(show=False, label="DEBUG_PUZZLE", tag="DEBUG_PUZZLE", callback= PUZZLE.piece_trouve)
                
                dpg.add_input_int(show=False, tag="DEBUG_X_perso", width=30, default_value=0, step=0, on_enter=True, callback=lambda: Position_perso.set_pos([dpg.get_value("DEBUG_X_perso"), dpg.get_value("DEBUG_Y_perso")]))
                dpg.add_input_int(show=False, tag="DEBUG_Y_perso", width=30, default_value=0, step=0, on_enter=True, callback=lambda: Position_perso.set_pos([dpg.get_value("DEBUG_X_perso"), dpg.get_value("DEBUG_Y_perso")]))

            
        # Fenetre principale

        with dpg.window(tag="fenetre_principale", show=True, pos=(25, 75), autosize=True,
                        no_move=True, no_title_bar=True, no_scrollbar=True, no_background=True):
            dpg.add_image(LABYRINTHES[id_labyrinthe].fond, tag="fond", pos=(0, 0), width=700, height=700)
            dpg.add_image(LABYRINTHES[id_labyrinthe].murs, tag="murs", pos=(0, 0), width=700, height=700)
            dpg.add_image("personnage", tag="Personnage", pos=(0,0), width=50, height=50)

        # Fenetre d'histoire

        with dpg.window(label="L'histoire du labirynthe Cosmique", tag="histoire", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True,
                        pos=(ECRAN[0]-530, ECRAN[1] - 790), width=500):
            dpg.add_image("logo", pos=(100, 0), width=320, height=180)
            dpg.add_text(tag="histoire_générale", wrap=500, pos=(5, 175), default_value="Un adorable petit chat nommé Félix se réveille un jour pour découvrir qu'il s'est perdu dans l'immensité de l'univers. Se sentant seul et perdu, Félix décide de partir à l'aventure pour retrouver son chemin vers sa maison. Pour cela Félix doit rassembler les morceaux de la carte stellaire sur 4 mystérieuses planètes-labyrinthe. Mais de nombreux obstacles et pièges l'empécheront de rentrer chez lui. \n\n Êtes-vous suffisament malin pour aider Félix à s'échapper des labyrinthes cosmiques ?")

        with dpg.window(tag="histoire_labi", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=False, no_title_bar=True,
                        pos=(ECRAN[0]-530, ECRAN[1] - 475), width=500, height=130):
            dpg.add_text(tag="histoire_l", wrap=500, pos=(5, 20), default_value="")

        # Fenetre tuto

        with dpg.window(tag="fenetre_tuto", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=True, no_title_bar=True,
                        pos=(ECRAN[0]-530, ECRAN[1]-330), width=500):
            with dpg.group(horizontal=True):
                for image, phrase in [("piece", "C'est une pièce de la carte, trouvez la"), ("portail", "C'est un portail, il vous emmenera a un autre niveau") , ("personnage", "C'est vous, felix"), ("fleches", "Utilisez les flèches pour vous déplacer")]:
                    with dpg.group():
                        dpg.add_image(image, width=95, height=95)
                        dpg.add_text(wrap=80, default_value=phrase)
                    dpg.add_spacer(width=12)
                
        # Fenetre quitter

        with dpg.window(tag="fenetre_quitter", no_title_bar=True, no_move=True, no_background=True,
                        pos=(ECRAN[0]-537, ECRAN[1] - 130), autosize=True):
            dpg.add_button(tag="QUITTER", label="QUITTER LE JEU", width=500, height=90, callback=dpg.stop_dearpygui)

    ECRAN = [1280, 800]   
    PUZZLE = Puzzle("puzzle/puzzle1")
    LABYRINTHES = [ 
        labyrinthe(40, "labirynthes/1",   "fonds/plaine",  [10, 20], (9, 74, 0), [], "La Planète Verdura est un endroit luxuriant et verdoyant, avec de grands arbres qui s'élèvent vers le ciel. Les chemins serpentent entre les racines entrelacées et les plantes exotiques. Le fragment de la carte stellaire se trouve au sommet d'une ancienne tour cachée au cœur de la forêt. "), 
        labyrinthe(50, "labirynthes/2",   "fonds/desert",  [60, 60], (219, 76, 33), [], "La Planète Sableon est un paysage aride et impitoyable, avec des dunes de sable à perte de vue et des tempêtes de sable occasionnelles. Le soleil brille intensément dans un ciel sans nuages. Le fragment de la carte stellaire est enfoui dans une ancienne pyramide perdue sous le sable. "), 
        labyrinthe(20, "labirynthes/3",   "fonds/nuages",  [365, 35], (122, 214, 235), [], "La Planète Nimbroa est un monde céleste rempli de nuages moelleux et de paysages oniriques. Les nuages prennent des formes fantastiques et l' étoile brille aux couleurs charmantes. À première vue, elle peut paraître paisible et paradisiaque mais c'est en réalité une des planètes les plus dangereuses. Le fragment de la carte stellaire se cache, cette fois, au sommet d'une montagne de nuages majestueuse. "), 
        labyrinthe(30, "labirynthes/4",   "fonds/lave",    [290, 70], (117, 1, 1), [], "La Planète Mustafar est un monde tumultueux rempli de volcans en éruption et de rivières de lave brûlante. Des flammes dansent sur la surface, créant une lueur sinistre dans un ciel sombre. Le fragment de la carte stellaire se trouve dans un sanctuaire au cœur d'un volcan actif.  Mais Félix devra d'abord traverser des plateformes instables, éviter toutes éruptions volcaniques et résister à la chaleur étouffante."),
                    ]
    VITESSE = 5
    global id_labyrinthe, DEBUG_MODE
    id_labyrinthe = 0
    viewport_load()
    Position_perso = Position()
    interface()
    labirynthe_i(id_labyrinthe)

    # BOUCLE PRINCIPALE

    while dpg.is_dearpygui_running():

        Vitesse = round(LABYRINTHES[id_labyrinthe].taille_personnage/20*VITESSE)
        if keyboard.is_pressed("down arrow"):
            dpg.configure_item("Personnage", pos=Position_perso.bas(Vitesse))
        if keyboard.is_pressed("up arrow"):
            dpg.configure_item("Personnage", pos=Position_perso.haut(Vitesse))
        if keyboard.is_pressed("left arrow"):
            dpg.configure_item("Personnage", pos=Position_perso.gauche(Vitesse))
        if keyboard.is_pressed("right arrow"):
            dpg.configure_item("Personnage", pos=Position_perso.droite(Vitesse))

        if dpg.get_value("DEBUG"):
            dpg.configure_item("DEBUG_Y_perso", default_value=Position_perso.pos[1])
            dpg.configure_item("DEBUG_X_perso", default_value=Position_perso.pos[0])
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

main()