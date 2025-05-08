import flet as ft

def Settings(counter,pop,page):
    lists = ft.ListView([])

    for i in range(0,9):
        lists.controls.append(
            ft.ListTile(
            leading=ft.Icon(name=ft.Icons.SETTINGS_APPLICATIONS),
            title=ft.Text(f"{i + 1} Title"),subtitle=ft.Text(f"Sub title"),min_height=20,
            data=i+1,
            on_click=lambda e:print(f"{e.control.data} list clicked!")
        ))



    return ft.SafeArea( 
            content=ft.Column(
                [
                    ft.Container(
                        height=210,alignment=ft.alignment.center,
                        bgcolor=ft.Colors.BLUE,
                        content=counter, # type: ignore
                        expand=1
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                height=210,width=150,
                                bgcolor=ft.Colors.BLUE,
                                
                            ),ft.Container(
                                height=210,width=150,
                                bgcolor=ft.Colors.BLUE,
                                on_click=lambda _: page.go("/profile")
                            )
                        ],scroll=ft.ScrollMode.AUTO 
                    ),
                    lists
                ],scroll=ft.ScrollMode.ALWAYS
            ), expand= True
        )  
   