import flet as ft

def Profile(pop,page):
    return ft.SafeArea(
        content=ft.Column(
            [
                ft.Container(
                    height=110,alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLUE,
                    content=ft.CircleAvatar(radius=50,content=ft.Container(image=ft.DecorationImage(src=f"/imgs/icon.png"))),
                    
                ), 
                ft.Row(
                    [
                        ft.Container(
                            height=110,width=130,
                            bgcolor=ft.Colors.BLUE,
                            on_click=lambda _: pop, 
                        ),ft.Container(
                            height=110,width=130,
                            bgcolor=ft.Colors.BLUE,
                            image=ft.DecorationImage(src=f"/imgs/icon.png")
                        )
                    ],alignment=ft.MainAxisAlignment.SPACE_AROUND
                )
            ],
        )
    )