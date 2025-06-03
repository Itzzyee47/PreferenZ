import flet as ft
import sqlite3

from pages.landing import refresh_categories,grid


db_file = "./preferez.db"

def dbInitializer():
    # Ensure the tasks table exists
    with sqlite3.connect("preferez.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subtitle TEXT,
                position INTEGER NOT NULL,
                category_id INTEGER NOT NULL
            )
        """)
        conn.commit()

    # Ensure the categories table exists
    with sqlite3.connect("preferez.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT NOT NULL
            )
        """)
        conn.commit()

def create_category_dialog(page):
    icon_options = {
        "Work": "work", 
        "Person": "person",
        "Shopping Cart": "shopping_cart",
        "Fitness": "fitness_center",
        "School": "school",
        "Home": "home",
        "Star": "star",
        "Favorite": "favorite",
        "Settings": "settings",
        "List": "list"
    }

    name_field = ft.TextField(
        label="Category Name",
        border=ft.InputBorder.UNDERLINE,
        hint_text="Enter category name" 
    )

    icon_dropdown = ft.Dropdown(
        label="Select Icon",
        options=[
            ft.dropdown.Option(key=icon_name, text=display_name)
            for display_name, icon_name in icon_options.items()
        ],
        width=200
    )

    def close_dialog(e):
        dialog.open = False
        page.update()

    def add_category(e):
        name = name_field.value
        icon = icon_dropdown.value

        if name and icon:
            with sqlite3.connect("preferez.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categories (name, icon) VALUES (?, ?)",
                    (name, icon)
                )
                conn.commit()
            
            # Clear the form
            name_field.value = ""
            icon_dropdown.value = None
            
            # Close dialog
            close_dialog(e)
            refresh_categories(grid, page)
            

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add New Category",size=15,weight=ft.FontWeight.BOLD,
                      text_align=ft.TextAlign.CENTER
                      ),
        content=ft.Column(
            [name_field, icon_dropdown],
            tight=True,
            spacing=10
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.TextButton("Add", on_click=add_category),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return dialog

def create_task_dialog(page, category_id, lists):
    title_field = ft.TextField(
        label="Task Title",
        border=ft.InputBorder.UNDERLINE,
        hint_text="Enter task title"
    )

    description_field = ft.TextField(
        label="Task Description",
        border=ft.InputBorder.UNDERLINE,
        hint_text="Enter task description",
        multiline=True
    )

    def close_dialog(e):
        dialog.open = False
        page.update()

    def load_tasks():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, subtitle, position 
                FROM tasks 
                WHERE category_id = ? 
                ORDER BY position
            """, (category_id,))
            rows = cursor.fetchall()
            print(f"Loaded tasks for: {rows}..............")
            if not rows:
                return [{"id": "1", "title": "No Task added", "subtitle": "Add a new task", "position": "0"} ]
            else:
                return [{"id": row[0], "title": row[1], "subtitle": row[2], "position": row[3]} for row in rows]
            
    def getColorBasedOnPosition(total_tasks, index):
        # Determine the color based on the position
            if index < total_tasks * 0.33:
                color = ft.colors.RED
                return color
            elif index < total_tasks * 0.66:
                color = ft.colors.ORANGE 
                return color 
            else:
                color = ft.colors.GREEN
                return color

    def loadData(lists):
       
        tasks = load_tasks()
        print(f"Loading data for items for list: {lists} {tasks}")
        lists.controls.clear()
        total_tasks = len(tasks)
        for index, task in enumerate(tasks):
            color = getColorBasedOnPosition(total_tasks, index)
            lists.controls.append(
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.TASK, color=color),
                    title=ft.Text(task["title"], color=color),
                    subtitle=ft.Text(task["subtitle"], color=color),
                    min_height=20,
                    key=str(task["id"]),
                    data=[task["subtitle"], task["title"]],
                    on_click=lambda e: print(f"{e.control.data} list clicked!")
                )
            )

    def add_task(e):
        title = title_field.value
        description = description_field.value

        if title:
            with sqlite3.connect("preferez.db") as conn:
                cursor = conn.cursor()
                # Get the current position value
                cursor.execute(
                    "SELECT COUNT(*) FROM tasks WHERE category_id = ?", (category_id,)
                )
                position = cursor.fetchone()[0] + 1

                # Insert the new task
                cursor.execute(
                    "INSERT INTO tasks (title, subtitle, position, category_id) VALUES (?, ?, ?, ?)",
                    (title, description, position, category_id)
                )
                conn.commit()

            # Clear the form
            title_field.value = ""
            description_field.value = ""

            # Close dialog
            close_dialog(e)
            
            loadData(lists)
            page.update()
           

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add New Task", size=15, weight=ft.FontWeight.BOLD,
                      text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [title_field, description_field],
            tight=True,
            spacing=10
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.TextButton("Add", on_click=lambda e: add_task(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END, 
    )

    return dialog

def deleteCatById(id,page):
    try:
        deleteTaskForCategory(id)
        conn = sqlite3.connect("preferez.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (id,))
        conn.commit()
        print(f"Deleted sucessfully!")
        refresh_categories(grid, page)
        page.go("/landing")
        page.update()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def deleteTaskForCategory(id):
    try:
        conn = sqlite3.connect("preferez.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE category_id = ?", (id,))
        conn.commit()
        print(f"Deleted all category tasks!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def create_fab(page, dialog):

    return ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click= lambda e: page.open(dialog)
    )

def create_fab2(page, dialog):

    return ft.FloatingActionButton(
        icon=ft.icons.ADD,
        on_click= lambda e: page.open(dialog)
    )