import flet as ft


class Card(ft.AnimatedSwitcher):
    def __init__(self, page: ft.Page, id: int, image_index: int):
        # Save page as class variable
        self.page = page

        # Class Variables
        self.id = id
        self.image_path = f'images/{image_index}.png'

        # Front part of the card (Emoji)
        self.f_bgcolor = '#5db7fc'  # Blue
        self.frontside = self.__create_card_container(self.f_bgcolor,
                                                      self.image_path)

        # Back part of the card
        self.b_bgcolor = '#ff7200'  # Orange
        self.backside = self.__create_card_container(self.b_bgcolor, None)

        # Call super constructor
        super().__init__(content=self.backside)

        # Animator for back side and front side of the card
        self.transition=ft.AnimatedSwitcherTransition.FADE
        self.duration=500

    def __create_card_container(self, bgcolor: str, image_path: str = None) -> ft.Control:
        if bgcolor == '#ff7200':
            return ft.Container(height = 150, width= 120, border=ft.border.all(5, "black"),border_radius=ft.border_radius.all(5), bgcolor=bgcolor, on_click=self.animate_card)
        else:
            return ft.Container(height = 150, width = 120, padding = 30, border=ft.border.all(5, "black"),border_radius=ft.border_radius.all(5), bgcolor = bgcolor, content = ft.Image(height = 50, width = 50,src=image_path, fit=ft.ImageFit.CONTAIN))

    def animate_card(self, e) -> None:
        self.content = self.frontside if self.content == self.backside else self.backside
        self.update()

    def enable_card(self) -> None:
        self.backside.on_click = self.animate_card

    def disable_card(self) -> None:
        self.backside.on_click = None

    def change_fronside_bgcolor(self, bgcolor: str = '#898989') -> None:
        self.frontside.bgcolor = bgcolor
        self.frontside.update()
        self.update()
