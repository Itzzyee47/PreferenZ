import flet as ft
from pages.home import Home
from pages.settings import Settings
from pages.profile import Profile
from pages.landing import landing,grid,refresh_categories
from pages.settingsPages.dataManager import DataManager,startUpDataLoaderPage
from pages.tasks import Tasks
from pages.component1 import create_category_dialog, create_fab, create_fab2, create_task_dialog, dbInitializer, deleteCatById
import sqlite3
from pages.settingsPages.about import About



def main(page: ft.Page):
    page.title = 'PreferenZ'
    page.window.width = 330
    page.window.height = 630
    page.window.resizable = False
    page.window.always_on_top = True
    # page.theme_mode = ft.ThemeMode.DARK
    dbInitializer()


    def view_pop(view):
        try:
            page.views.pop()
            top_view = page.views[-1]
            print(f'{page.views}')
            print(f'the top view {top_view.route}') 
            page.go(top_view.route)
            print(top_view.route)
        except Exception as er:
            print(f"The usual pop error! {er}")
        page.update()
 
    navbar = ft.NavigationBar(destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Explore",
                    
                ),
            ])
    
    appbar = ft.AppBar(leading=ft.Icon(ft.Icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Example",size=15,weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.GREY,
            actions=[
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.Icons.SETTINGS,on_click=lambda _: page.go("/settings")),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],)
    
    bar1 = ft.AppBar(actions=[ft.IconButton(icon=ft.Icons.SETTINGS,on_click=lambda _:page.go('/settings'))],
                     leading=ft.Icon(name=ft.icons.HOME)
                     )

    img = ft.Image(f'/imgs/icon.png') 
    home = Home(page) 
    settings = Settings(view_pop,page)
    profile = Profile(view_pop,page)     
    land = landing(page,grid)
    action = ft.FloatingActionButton(
                icon=ft.icons.ADD
            )
    
    # taskPage = Tasks(page)
    dialog = create_category_dialog(page)
    fab = create_fab(page, dialog)
    grid1 = grid
   
    def delDilog(id):
        def close():
            dialog2.open = False
            page.update()
        dialog2 = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Are you  sure you want to delete category {getCatNameById(id)} ",
                                  size=15,weight=ft.FontWeight.BOLD,
                                  text_align=ft.TextAlign.CENTER
                                  ),
                    content=ft.Text("This action cannot be undone."),
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda e: close()),
                        ft.TextButton("Yes", on_click= lambda _: deleteCatById(id,page)),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
        return dialog2

    pages = {
        '/': ft.View("/",[home],padding=ft.padding.only(left=6,right=6)),
        "/landing": ft.View("/landing",[land],appbar= bar1,floating_action_button=fab,
                           padding=ft.padding.only(left=6,right=6,)
                           ),
        "/settings": ft.View("/settings",[settings],appbar=ft.AppBar(title=ft.Text("Settings",size=15,weight=ft.FontWeight.BOLD),), 
                             scroll=ft.ScrollMode.AUTO, padding=ft.padding.only(left=6,right=6)
                             ),
        "/profile": ft.View("/profile",[profile],appbar=ft.AppBar(title=ft.Text("Profile",size=15,weight=ft.FontWeight.BOLD)),
                            padding=ft.padding.only(left=6,right=6)
                            ),
        "/about": ft.View(
                            "/about",
                            [About(page)],
                            appbar=ft.AppBar(
                                title=ft.Text("About PreferenZ", size=15, weight=ft.FontWeight.BOLD),
                            ),
                            padding=ft.padding.only(left=6, right=6)
                        ),
        "/dataManager": ft.View(
            "/dataManager", [DataManager(page)],
            appbar=ft.AppBar(
                        title=ft.Text("Data Manager", size=15, weight=ft.FontWeight.BOLD),actions=[
                            ft.IconButton( 
                                icon=ft.icons.REFRESH,
                                icon_color=ft.colors.BLUE_ACCENT_700,
                                tooltip="Refresh",
                                on_click=lambda e: startUpDataLoaderPage(e.page),
                            )
                        ],
                    ),padding=ft.padding.only(left=6, right=6)
        )
    }
    
    def route_change(route):
        #print(page.route, route)
        page.views.clear() 
        page.views.append(    
            pages['/']
        )  
        
        if page.route == "/settings": 
            try:
                page.views.append(    
                    pages['/landing']
                )
                page.views.append(
                    pages[page.route]
                ) 
            except Exception as er:
                print("The usual pop error")
        elif page.route == "/about": 
            try:
                page.views.append(    
                    pages['/settings']
                ) 
                page.views.append(
                    pages[page.route]
                ) 
            except Exception as er:
                print("The usual pop error")
        elif page.route == "/dataManager": 
            try:
                page.views.append(    
                    pages['/settings']
                ) 
                page.views.append(
                    pages[page.route]
                ) 
            except Exception as er:
                print("The usual pop error")
        elif page.route == "/landing": 
            try:
                page.views.append(
                    pages[page.route]
                ) 
            except Exception as er:
                print("The usual pop error")
        elif page.route.startswith("/tasks/"):
            category_id = int(page.route.split('/')[-1])
            try:
                page.views.append(    
                    pages['/landing']
                ) 
                lists = Tasks(page,category_id)
                taskDialog = create_task_dialog(page,category_id,lists)
                action2 = create_fab2(page, taskDialog)
                
                page.views.append(
                    ft.View(
                        route=f"/tasks/{category_id}",
                        controls=[ft.SafeArea(
                                    content=ft.Column(
                                        [
                                            lists
                                        ],
                                        scroll=ft.ScrollMode.ALWAYS
                                    ),
                                    expand=True
                                )],
                        appbar=ft.AppBar(title=ft.Text(f"Tasks_{getCatNameById(category_id)}",size=15,weight=ft.FontWeight.BOLD),
                                         actions=[
                                            ft.IconButton(icon=ft.icons.DELETE,on_click= lambda e: page.open((delDilog(category_id))))
                                         ]
                                         ),
                        padding=ft.padding.only(left=6,right=6,),floating_action_button=action2
                    )
                )
            except Exception as er:
                print(f"The usual pop error: {er}")
        page.update()
        

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")

    def getCatNameById(id):
        try:
            conn = sqlite3.connect('preferez.db')  # Replace with your database file
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM categories WHERE id = ?", (id,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown Category"
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return "Unknown Category"
        finally:
            if conn:
                conn.close()


ft.app(main,view=ft.AppView.FLET_APP)

#673508496
