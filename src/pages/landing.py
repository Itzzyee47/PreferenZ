import flet as ft
import sqlite3


def refresh_categories(grid,page):
    """Refresh the categories displayed in the grid."""
    grid.controls.clear()
    with sqlite3.connect("categories.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, icon FROM categories")
        categories = cursor.fetchall()
        
        for cat_id, cat_name, cat_icon in categories:
            grid.controls.append(
                ft.Container(
                    height=30,
                    bgcolor=ft.colors.with_opacity(0.3,color=ft.colors.BLUE_ACCENT_700),
                    border_radius=ft.border_radius.all(10),
                    content=ft.Row(
                        [
                            ft.Icon(name=cat_icon, size=16),
                            ft.Text(cat_name, size=12, weight=ft.FontWeight.W_700),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=3),
                    alignment=ft.alignment.center,
                    on_click=lambda _, id=cat_id: page.go(f"/tasks/{id}")
                )
            )
    page.update()

grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=190,
        child_aspect_ratio=1.7,
        spacing=9,
        run_spacing=9,
        padding=ft.padding.only(bottom=10),auto_scroll=True
    )

def landing(page,grid): 
    page.update()
    
    
    # Load initial categories
    refresh_categories(grid,page)

    return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        height=120,
                        bgcolor=ft.colors.with_opacity(0.3,color=ft.colors.BLUE_ACCENT_700), 
                        border_radius=ft.border_radius.all(10),
                        content=ft.Text(
                            "Welcome to preferenZ, your all in one task manager/organiser",
                            size=19,
                            weight=ft.FontWeight.W_700,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=ft.padding.symmetric(horizontal=20),
                        alignment=ft.alignment.center,
                        on_click=lambda _: page.go("/settings"),
                        margin=ft.margin.symmetric(vertical=10)
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "Categories",
                                size=17,
                                weight=ft.FontWeight.W_700,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.IconButton(
                                icon=ft.icons.REFRESH,
                                icon_color=ft.colors.BLUE_ACCENT_700,
                                tooltip="Refresh",
                                on_click=lambda e: refresh_categories(grid,page),
                            )
                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    grid,
                ],
                
                scroll=ft.ScrollMode.AUTO
            ),padding=ft.padding.symmetric(horizontal=10),expand=True
        )