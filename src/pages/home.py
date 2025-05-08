import flet as ft
def Home(page):

    return ft.SafeArea(
            content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    height=200,bgcolor=ft.colors.with_opacity(0.3,color=ft.colors.BLUE_ACCENT_700),
                                    border_radius=ft.border_radius.all(10),
                                    content=ft.Text("Welcome!",size=25,weight=ft.FontWeight.W_700,text_align=ft.TextAlign.CENTER),
                                    padding=ft.padding.symmetric(horizontal=20),alignment=ft.alignment.center,
                                    on_click= lambda _: page.go("/landing")
                                )
                            ],alignment=ft.MainAxisAlignment.CENTER
                        ),alignment=ft.alignment.center,padding=ft.padding.only(left=30,right=30)
                    ),
            expand= True
        ) 