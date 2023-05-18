import dearpygui.dearpygui as dpg

# Classes

class labirinthe:
    """
    Classe définissant un labirinthe
    """
    def __init__(self, taille_personnage: int, image, ):
        self.taille_personnage = taille_personnage
        self.image = image

class Niveau:
    """
    Classe définissant un niveau composé de plusieurs Labirinthe
    """
    def __init__(self, nom: str, labirinthes: dict):
        self.nom = nom
        self.labirinthes = labirinthes

# fonctions



def main():

    dpg.create_context()
    dpg.create_viewport(title='Labirynthe', resizable=True, vsync=True, clear_color=(0, 0, 0), min_height=800, min_width=1280)
    dpg.setup_dearpygui()
    dpg.show_viewport(maximized=True)
    
    with dpg.window(tag="Menu Options",label="Menu Options"):
        dpg.add_text("X")

    while dpg.is_dearpygui_running():
        ECRAN = [dpg.get_viewport_client_width(), dpg.get_viewport_client_height()] # Update les dimensions de l'écran à chaque frame

        

        dpg.render_dearpygui_frame()

    dpg.destroy_context()

    
    
    
    
    
main()