import random
import time
import threading

import flet as ft

from .card import Card


class Game(ft.Container):
    def __init__(self, page: ft.Page):
        # Call super constructor
        super().__init__()

        # Save page as class variable
        self.page = page

        # CLASS VARIABLES
        self.n_pairs = 10  # Number of card pairs (int)
        self.card_images_indexes = []  # List of indexes of card images (list)
        self.cards = []  # List of Cards (list)
        
        self.matches = 0  # Number of matches between cards (int)
        self.errors = 0  # Number of errors during the game (int)

        self.selected_card = None  # First card selected from the pair (Card)
        # List of identifiers for those pairs of cards already found (list)
        self.cards_ids_matched = []
        
        # para que todo esté centrado
        self.alignment = ft.alignment.center

        # los genero aqui para poder modificarlos dentro
        self.aciertos = ft.Text(f"Matches: {self.matches}", size=50, color="green")
                       
        self.fallos =  ft.Text(f"Errors: {self.errors}", size=50, color="red")

        self.__initialize_game()

    # DON´T TOUCH THIS FUNCTION
    def did_mount(self):
        self.running = True
        self.th = threading.Thread(
            target=self.__game_logic, args=(), daemon=True)
        self.th.start()

    # DON´T TOUCH THIS FUNCTION
    def will_unmount(self):
        self.running = False

    # DON´T TOUCH THIS FUNCTION
    def __game_logic(self) -> None:
        # Loop inside while the number of found matches is different to the
        # total number of pairs
        while self.matches != self.n_pairs and self.running:
            for card in self.cards:
                if card.animator.content == card.frontside:
                    self.__is_a_match(card)

        # The game is over
        self.running = False
        print('Game Over!')
        time.sleep(1)

        # Go to Congrats view
        self.page.go(f'/congrats/{self.matches}/{self.errors}')

    def __initialize_game(self): 
        # inizializo las variables
        self.matches = 0 
        self.errors = 0 
        # genero una lista de 10 valores entre el 0 y el 19
        image_indices = random.sample(range(20), self.n_pairs)
        # duplico los valores para que tengamos pares y 20 cartas ent otal
        self.card_images_indexes = image_indices * 2
        # utilizando shuffle me aseguro de que los valores estén colocado en la lista de forma aleatoria
        random.shuffle(self.card_images_indexes)
        # hago el bucle que genera las 20 cartas
        self.cards = [Card(self.page, i, img_index) for i, img_index in enumerate(self.card_images_indexes)]

    def build(self):
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment="center",
                    spacing=150,
                    controls=[
                        self.aciertos,
                        self.fallos
                    ],
                ),
                ft.Divider(thickness = 8),
                ft.Container(
                    width=650,
                    content=ft.Row(
                        wrap=True,
                        controls=self.cards,
                    ),
                ),
            ],
        )

    def __update_texts(self) -> None:
        # actualiza los textos de coincidencias y errores
        self.aciertos.value = f"Matches: {self.matches}"
        self.fallos.value = f"Errors: {self.errors}"
        self.page.update()

    def __is_a_match(self, card: Card) -> None:
        # deshabilita las cartas
        self.__disable_all_remaining_cards()

        # para desbloquear si la carta seleccionada es la misma
        if card.id in self.cards_ids_matched or card == self.selected_card:
            self.__enable_all_remaining_cards()
            return

        # guardamos la carta seleccionada en selected_card si no hay ninguna carta seleccionada
        if self.selected_card is None:
            self.selected_card = card
            self.__enable_all_remaining_cards()  # habilito el resto de cartas para que se pueda hacer clic
            return

        # si ya hay una carta seleccionada las comparo
        if self.selected_card.image_path == card.image_path:
            # si son iguales aumentamos el numero de matches
            self.matches += 1
            time.sleep(1)  # espera de 1 segundo para mostrar las cartas antes de voltearlas
            # cambiamos el color de ambas cartas al gris
            self.selected_card.change_fronside_bgcolor()
            card.change_fronside_bgcolor()

            self.cards_ids_matched.extend([self.selected_card.id, card.id]) # no utilizo append ya que lo tendría que poner dos veces 
            # deshabilito las cartas seleccionadas
            self.selected_card.disable_card()  
            card.disable_card() 
        else:
            # si son distintas aumentamos el numero de errores
            self.errors += 1

            time.sleep(1)  # espera de 1 segundo para mostrar las cartas antes de voltearlas

            # animo las cartas para que se den la vuelta a su posicion inicial
            self.selected_card.animate_card(self.selected_card)
            card.animate_card(card)

        # elimino selected_card para la siguiente interaccion y actualizo los textos
        self.selected_card = None
        self.__update_texts()

        # habilito todas las cartas no emparejadas
        self.__enable_all_remaining_cards()

    def __disable_all_remaining_cards(self) -> None:
        for card in self.cards:
            card.disable_card()

    def __enable_all_remaining_cards(self) -> None:
        for card in self.cards:
            if card.id not in self.cards_ids_matched:
                card.enable_card()
        self.update()


    # DON´T TOUCH THIS FUNCTION
    def __game_logic(self) -> None:
        # Loop inside while the number of found matches is different to the
        # total number of pairs
        while self.matches != self.n_pairs and self.running:
            for card in self.cards:
                if card.content == card.frontside:
                    self.__is_a_match(card)

        # The game is over
        self.running = False
        print('Game Over!')
        time.sleep(1)

        # Go to Congrats view
        self.page.go(f'/congrats/{self.matches}/{self.errors}')
