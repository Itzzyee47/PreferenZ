import flet as ft

def Settings(pop,page):
    lists = ft.ListView([])

    lists.controls.append(
        ft.ListTile(
        leading=ft.Icon(name=ft.Icons.DETAILS_OUTLINED),
        title=ft.Text(f"About PreferenZ"),min_height=20,
        on_click=lambda e: page.go('/about')
    ))



    return ft.SafeArea( 
            content=ft.Column(
                [
                    lists
                ],scroll=ft.ScrollMode.ALWAYS
            ), expand= True
        )  
   