import flet as ft
def Home(page):
    print(f"Page width: {page.width}.................................")

    return ft.SafeArea(
            content=ft.Container(
                        content=ft.Stack(
                            [
                                ft.Image(
                                    src="https://images.unsplash.com/photo-1692158962133-6c97ee651ab9?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                                    fit=ft.ImageFit.COVER,
                                    width=page.width,height=page.height,
                                    expand=1 
                                ),
                                ft.Container(
                                    height=200, 
                                    bgcolor=ft.colors.with_opacity(0.3, color=ft.colors.BLUE_ACCENT_700), 
                                    border_radius=ft.border_radius.all(10),
                                    content=ft.Text( 
                                        "Welcome!", 
                                        size=25, 
                                        weight=ft.FontWeight.W_700, 
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    padding=ft.padding.symmetric(horizontal=20),
                                    margin=ft.margin.symmetric(horizontal=25),
                                    alignment=ft.alignment.center, 
                                    on_click=lambda _: page.go("/landing") 
                                )
                            ],expand=True,alignment=ft.alignment.center
                        ),
                        
                    ),
            expand=True
        ) 