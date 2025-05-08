from time import sleep
import flet as ft
import sqlite3
import os



def Tasks(page, category_id):
    # Path to SQLite database file
    db_file = "tasks.db"
    category_id = int(page.route.split('/')[-1])
    print(f'THis the page route: {page.route}')

    # Initialize the database with category support
    def init_db():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            # Drop existing table if it exists
            # cursor.execute('DROP TABLE IF EXISTS tasks')
            
            # Create new table with all required columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    subtitle TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    position INTEGER NOT NULL
                )
            ''')
            conn.commit()

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
            if not rows:
                return [{"id": "1", "title": "No Task added", "subtitle": "Add a new task", "position": "0"} ]
            else:
                return [{"id": row[0], "title": row[1], "subtitle": row[2], "position": row[3]} 
                   for row in rows]


    def save_tasks(old_index, new_index):
        try:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                tasks = load_tasks()

                # Swap the tasks positions
                old_task = tasks.pop(old_index)
                tasks.insert(new_index, old_task)

                # Update positions for all affected tasks
                for pos, task in enumerate(tasks):
                    cursor.execute("""
                        UPDATE tasks 
                        SET position = ? 
                        WHERE id = ? AND category_id = ?
                    """, (pos, task["id"], category_id))
                conn.commit()
        except Exception as er:
            print(f'There was an error saving the new reordered list: {er}')


    # ...  ...
    def on_reorder(e):
        print(f"Item reordered from {e.old_index} to {e.new_index}")
        save_tasks(e.old_index, e.new_index)
        loadData()
        page.update()

    lists = ft.ReorderableListView(
        on_reorder=on_reorder,
        controls=[]
    )

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
            
    def show_edit_delete_dialog(e):

        def save_changes():
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE tasks 
                        SET title = ?, subtitle = ? 
                        WHERE id = ? AND category_id = ?
                    """, (e.control.title.value, e.control.subtitle.value, e.control.key, category_id))
                    conn.commit()
                dialog.open = False
                loadData()
                page.update()
            except Exception as er:
                print(f"Error updating task: {er}")

        def delete_task():
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        DELETE FROM tasks 
                        WHERE id = ? AND category_id = ?
                    """, (e.control.key, category_id))
                    conn.commit()
                dialog.open = False
                loadData()
                page.update()
            except Exception as er:
                print(f"Error deleting task: {er}")

        def close(e):
            title_field.value = ""
            subtitle_field.value = ""

            page.close(dialog)

        title_field = ft.TextField(label="Title", value=e.control.title.value, 
                                   border=ft.InputBorder.UNDERLINE,
                                    hint_text="title")
        subtitle_field = ft.TextField(label="Subtitle", value=e.control.subtitle.value, 
                                   border=ft.InputBorder.UNDERLINE,
                                    hint_text="subtitle")
        
        # print(e.control.key)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit or Delete Task",size=19,weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER),
            content=ft.Column([title_field, subtitle_field],tight=True,spacing=10), 
            actions=[
                ft.Row(
                    [
                        ft.TextButton("Save", style=ft.ButtonStyle(color=ft.colors.GREEN), on_click= lambda _: save_changes()),
                        ft.TextButton("Delete", style=ft.ButtonStyle(color=ft.colors.RED_ACCENT), on_click= lambda _: delete_task()),
                        ft.TextButton("Cancel", style=ft.ButtonStyle(color=ft.colors.BLUE_ACCENT), on_click=lambda e: close(e)),
                    ]
                )  
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            alignment=ft.alignment.center,
            open=True,
            
        )
        page.open(dialog)
        page.update()


    def loadData():
        tasks = load_tasks()
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
                    on_long_press=lambda e: show_edit_delete_dialog(e),
                )
            )

    # Initialize the database and load tasks
    init_db()
    loadData()

    return lists