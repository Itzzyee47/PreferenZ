import flet as ft

def About(page):
    app_info = {
        "name": "PreferenZ",
        "version": "1.0.1",
        "description": "A task management application that helps you organize your work into various categories and according to importance",
        "developer": "Nzenze Lovis",
        "email": "ebongloveis@gmail.com",
        "features": [
            "Create custom task categories",
            "Organize tasks by priority",
            "Reorderable task lists",
            "Category-specific task management",
            "Simple and intuitive interface",
            "Export or import database to(from) local files"
        ],
        "tech_stack": [
            "Built with Flet 0.27.6",
            "SQLite database for data persistence",
            "Python 3.9+"
        ],
        "year": "2025"
    }

    return ft.SafeArea(
        content=ft.Column(
            [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Version {app_info['version']}", 
                        size=16,
                        color=ft.colors.GREY_500
                    ),
                    ft.Divider(),
                    ft.Text(
                        app_info['description'],
                        text_align=ft.TextAlign.CENTER,
                        size=14
                    ),
                    ft.Container(height=20),
                    ft.Text("Features:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Text(f"• {feature}", size=14) 
                        for feature in app_info['features']
                    ]),
                    ft.Container(height=20),
                    ft.Text("Technical Details:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Text(tech, size=14, color=ft.colors.GREY_700) 
                        for tech in app_info['tech_stack']
                    ]),
                    ft.Container(height=20),
                    ft.Text(
                        f"Developed by {app_info['developer']} mail: {app_info['email']}", 
                        size=12,
                        color=ft.colors.GREY_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        f"Copyright © {app_info['year']} All rights reserved.", 
                        size=12,
                        color=ft.colors.GREY_400,
                        text_align=ft.TextAlign.CENTER
                    )
                ],scroll=ft.ScrollMode.AUTO,expand=1,
                ),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
            )
        ], scroll=ft.ScrollMode.AUTO
        ),expand=True
    )