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
        self.id = id
        self.fond = fond
        self.taille_personnage = taille_personnage
        self.pos_depart = pos_depart
        self.couleur_fond = couleur_fond
        self.histoire = histoire

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
        dpg.configure_item("compteur", label="Pièces obtenues: " +str(self.pieces_trouvees)+"/"+str(self.pieces_totales))
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

        def haut(self, vitesse):
            self.pos[1] = max(-50, self.pos[1]-vitesse)
            return self.pos
        def bas(self, vitesse):
            self.pos[1] = min(min(ECRAN)-200, self.pos[1]+vitesse)
            return self.pos
        def gauche(self, vitesse):
            self.pos[0] = max(-50, self.pos[0]-vitesse)
            return self.pos
        def droite(self, vitesse):
            self.pos[0] = min(min(ECRAN)-200, pos[0]+vitesse)
            return self.pos

    def viewport_load():
        dpg.create_context()
        dpg.create_viewport(title='Labirynthe', width=ECRAN[0], height=ECRAN[1], resizable=False, vsync=True, clear_color=(0, 0, 0))
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def labirynthe_suivant():
        """change les interfaces pour faire apparraitre le prochain labyrinthe"""

        global id_labyrinthe
        id_labyrinthe += 1
        dpg.set_viewport_clear_color(LABYRINTHES[id_labyrinthe].couleur_fond)
        dpg.configure_item("Personnage", pos=LABYRINTHES[id_labyrinthe].pos_depart)
        dpg.configure_item("fond", texture_tag=LABYRINTHES[id_labyrinthe].fond)
        dpg.configure_item("histoire_l", default_value=LABYRINTHES[id_labyrinthe].histoire)   
    
    def interface():
        """charge toutes les interfaces"""

        DEBUG_MODE = True # Permet l'affichage du mode débug

        # chargement des textures
        with dpg.texture_registry(show=False): # registre des textures chargées
            for image in [ 
                "personnage", "logo",
                "fonds/nuages", "fonds/lave", "fonds/desert", "fonds/plaine",
                        ]:
                width, height, channels, data = [elt for elt in dpg.load_image("data/"+image+".png")]
                dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag=image)
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
                dpg.add_checkbox(label="Afficher Puzzle", tag="Afficher_puzzle", callback= lambda: dpg.configure_item("puzzle", show=dpg.get_value("Afficher_puzzle")))
                if DEBUG_MODE:
                    dpg.add_button(tag="DEBUG_suivant", label="DEBUG_SUIVANT", callback=lambda: labirynthe_suivant())
                    dpg.add_button(tag="DEBUG_puzzle", label="DEBUG_PUZZLE", callback=lambda: PUZZLE.piece_trouve())

            
        # Fenetre principale

        with dpg.window(tag="fenetre_principale", show=True, pos=(25, 75), autosize=True,
                        no_move=True, no_title_bar=True, no_scrollbar=True, no_background=True):
            dpg.add_image(LABYRINTHES[id_labyrinthe].fond, tag="fond", pos=(0, 0), width=min(ECRAN)-100, height=min(ECRAN)-100)
            dpg.add_image(  "personnage", tag="Personnage", pos=(0,0),
                            width=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage, height=min(ECRAN)/5*LABYRINTHES[id_labyrinthe].taille_personnage)

        # Fenetre d'histoire

        with dpg.window(label="L'histoire du labirynthe Cosmique", tag="histoire", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True,
                        pos=(ECRAN[0]-530, ECRAN[1] - 790), width=500):
            dpg.add_image("logo", pos=(100, 0), width=320, height=180)
            dpg.add_text(tag="histoire_générale", wrap=500, pos=(5, 175), default_value="Un adorable petit chat nommé Félix se réveille un jour pour découvrir qu'il s'est perdu dans l'immensité de l'univers. Se sentant seul et perdu, Félix décide de partir à l'aventure pour retrouver son chemin vers sa maison. Pour cela Félix doit rassembler les morceaux de la carte stellaire sur 4 mystérieuses planètes-labyrinthe. Mais de nombreux obstacles et pièges l'empécheront de rentrer chez lui. \n\n Êtes-vous suffisament malin pour aider Félix à s'échapper des labyrinthes cosmiques ?")

        with dpg.window(tag="histoire_labi", no_close=True, no_collapse=True, show=True, no_move=True, no_resize=True, autosize=True, no_title_bar=True,
                        pos=(ECRAN[0]-530, ECRAN[1] - 475), width=500):
            dpg.add_text(tag="histoire_l", wrap=500, pos=(5, 20), default_value="")

        # Fenetre quitter

        with dpg.window(tag="fenetre_quitter", no_title_bar=True, no_move=True, no_background=True,
                        pos=(ECRAN[0]-530, ECRAN[1] - 200), autosize=True):
            dpg.add_button(tag="QUITTER", label="QUITTER LE JEU", width=500, height=150, callback=dpg.stop_dearpygui)

    ECRAN = [1280, 800]   
    PUZZLE = Puzzle("puzzle/1")
    LABYRINTHES = [ 
        labyrinthe(1.0, None, "fonds/plaine",  (0, 0), (9, 74, 0), [], "La Planète Verdura est un endroit luxuriant et verdoyant, avec de grands arbres qui s'élèvent vers le ciel. Les chemins serpentent entre les racines entrelacées et les plantes exotiques. Le fragment de la carte stellaire se trouve au sommet d'une ancienne tour cachée au cœur de la forêt. "), 
        labyrinthe(1.0, None, "fonds/desert",  (0, 0), (219, 76, 33), [], "La Planète Sableon est un paysage aride et impitoyable, avec des dunes de sable à perte de vue et des tempêtes de sable occasionnelles. Le soleil brille intensément dans un ciel sans nuages. Le fragment de la carte stellaire est enfoui dans une ancienne pyramide perdue sous le sable. "), 
        labyrinthe(1.0, None, "fonds/nuages",  (0, 0), (122, 214, 235), [], "La Planète Nimbroa est un monde céleste rempli de nuages moelleux et de paysages oniriques. Les nuages prennent des formes fantastiques et l' étoile brille aux couleurs charmantes. À première vue, elle peut paraître paisible et paradisiaque mais c'est en réalité une des planètes les plus dangereuses. Le fragment de la carte stellaire se cache, cette fois, au sommet d'une montagne de nuages majestueuse. "), 
        labyrinthe(1.0, None, "fonds/lave",    (0, 0), (117, 1, 1), [], "La Planète Mustafar est un monde tumultueux rempli de volcans en éruption et de rivières de lave brûlante. Des flammes dansent sur la surface, créant une lueur sinistre dans un ciel sombre. Le fragment de la carte stellaire se trouve dans un sanctuaire au cœur d'un volcan actif.  Mais Félix devra d'abord traverser des plateformes instables, éviter toutes éruptions volcaniques et résister à la chaleur étouffante."),
                    ]
    VITESSE = 10
    global id_labyrinthe
    id_labyrinthe = -1
    viewport_load()
    Position_perso = Position()
    interface()
    labirynthe_suivant()

    

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