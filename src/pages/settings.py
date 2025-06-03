import flet as ft

def Settings(pop,page):
    lists = ft.ListView([])

    lists.controls.append(
        ft.ListTile(
        leading=ft.Icon(name=ft.Icons.MORE),
        title=ft.Text(f"About PreferenZ"),min_height=40, 
        on_click=lambda e: page.go('/about')
    ))
    lists.controls.append(
        ft.ListTile(
        leading=ft.Icon(name=ft.Icons.STORAGE_OUTLINED),
        title=ft.Text(f"Data Management"),min_height=40,
        on_click=lambda e: page.go('/dataManager')
    ))



    return ft.SafeArea( 
            content=ft.Column(
                [
                    lists
                ],scroll=ft.ScrollMode.ALWAYS
            ), expand= True
        )  
   