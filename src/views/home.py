import flet as ft


class Home(ft.Column):

    def __init__(self, page: ft.Page):
        # Call super constructor
        super().__init__()

        # Save page as class variable
        self.page = page
        self.horizontal_alignment = "center"

    def build(self):
        self.controls = [
            ft.Image(
                src="/images/cover.png",
                width=400,
                height=400,
                fit=ft.ImageFit.CONTAIN,
            ), 
            ft.Container(
                height=100,
                width=180,
                content=ft.Text("Jugar", weight=ft.FontWeight.BOLD, color = "black", size = 50),
                bgcolor = ft.colors.DEEP_ORANGE,
                alignment = ft.alignment.center,
                border = ft.border.all(3, "black"),
                border_radius = ft.border_radius.all(5),
                on_click= lambda e: self.page.go("/game")
            )
        ]
