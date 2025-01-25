import flet as ft


class Congrats(ft.Column):

    def __init__(self, page: ft.Page, matches: int, errors: int):
        # Call super constructor
        super().__init__()

        # Save page as class variable
        self.page = page

        # Class Variables
        self.matches = matches
        self.errors = errors

        self.horizontal_alignment = "center"

    def build(self):
        self.controls = [
            ft.Image(
                src='/images/congrats.png',
                width=500,
                height=500,
                fit=ft.ImageFit.CONTAIN
            ),
            ft.Row(alignment="center",controls=[
                ft.Text(f"Matches: {self.matches} ", size=30, color="green",weight=ft.FontWeight.BOLD),
                ft.Text("|",weight=ft.FontWeight.BOLD, size = 30),
                ft.Text(f"Errors: {self.errors}", size=30, color="red",weight=ft.FontWeight.BOLD),
            ]),
            ft.Divider(thickness = 3),
            ft.Row(
                alignment="center",
                spacing = 50,
                controls=[
                    ft.Container(
                        content = ft.Row(controls = [
                        ft.Icon(name = ft.icons.HOME, color="green", size=50),
                        ft.Text("Go Home", size=30, weight=ft.FontWeight.BOLD)
                        ]),
                        on_click = lambda e: self.page.go("/"),
                    ),
                    ft.Container(
                        content = ft.Row(controls = [
                        ft.Icon(name = ft.icons.RESTART_ALT, color="orange", size=50),
                        ft.Text("Restart Game", size=30,weight=ft.FontWeight.BOLD)
                        ]),
                        on_click = lambda e: self.page.go("/game"),
                    ),
                    ft.Container(
                        content = ft.Row(controls = [
                        ft.Icon(name = ft.icons.POWER_SETTINGS_NEW, color="red", size=50),
                        ft.Text("End Game", size=30, weight=ft.FontWeight.BOLD)
                        ]),
                        on_click = lambda e: self.page.window.close(),
                    )
                ]
            )
        ]
