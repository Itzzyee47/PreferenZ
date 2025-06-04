import flet as ft
import pandas as pd
import os
import sqlite3


def loadDataTable(table, dbname: str, tablename: str):
    # Connect to the SQLite database
    db_path = os.path.join(os.getcwd(), f"{dbname}.db")  # Adjust the path to your database
    conn = sqlite3.connect(db_path)

    try:
        # Read data from the specified table in the database
        query = f"SELECT * FROM {tablename}"
        df = pd.read_sql_query(query, conn)

        # Clear existing rows in the DataTable
        table.rows.clear()
        table.columns = [ft.DataColumn(ft.Text(col,color='#000000')) for col in df.columns]

        # Add rows to the DataTable
        for _, row in df.iterrows():
            table.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell),text_align=ft.TextAlign.CENTER,size=10,scale=1,color='#000000')) for cell in row]))

    except Exception as e:
        print(f"An error occurred while loading data: {e}")

    finally:
        # Close the database connection
        conn.close()

def DataManager(page):
    lists = ft.ListView([])
    table1 = ft.DataTable([],bgcolor=ft.Colors.with_opacity(0.3,'#98ffff'),
                          scale=1,heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                          vertical_lines=ft.BorderSide(width=0.4)
                          )
    table2 = ft.DataTable([],bgcolor=ft.Colors.with_opacity(0.3,'#98ffff'),
                          scale=1,column_spacing=1,heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                          vertical_lines=ft.BorderSide(width=0.4)
                          ) 


    data = ft.Container(
        content=ft.Column([
            ft.Text('Your data', size=24, weight=ft.FontWeight.W_400, color='#000000'),
            ft.Text('Categories', size=14, weight=ft.FontWeight.W_300, color='#000000'),
            table1,
            ft.Divider(),
            ft.Text('Tasks', size=14, weight=ft.FontWeight.W_300, color='#000000'),
            table2
        ], scroll=ft.ScrollMode.ALWAYS, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=1
        ), bgcolor='#fcf5fc', expand=True, border_radius=ft.border_radius.all(5), 
        margin=ft.margin.only(bottom=20)
    )

    def exportDBAsExcel(dbname:str, export_path:str):
        # Connect to the SQLite database
        db_path = os.path.join(os.getcwd(), f"{dbname}.db")  # Adjust the path to your database
        conn = sqlite3.connect(db_path)

        try:  
            # Read data from the database
            query = "SELECT * FROM categories"  # Adjust the query as needed
            df1 = pd.read_sql_query(query, conn)
            df2 = pd.read_sql_query("SELECT * FROM tasks", conn)

            if export_path:
                # Export the DataFrame to an Excel file
                df1.to_excel(os.path.join(export_path, "categories.xlsx"), index=False)
                df2.to_excel(os.path.join(export_path, "tasks.xlsx"), index=False)
                # print(f"Database exported successfully to {export_path}")
            else:
                print("Export canceled.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the database connection
            conn.close()

    def importDBFromExcel(dbname: str, file_path1: str, file_path2: str):
        # Connect to the SQLite database
        db_path = os.path.join(os.getcwd(), f"{dbname}.db")  # Adjust the path to your database
        conn = sqlite3.connect(db_path)

        try:
            # Read the Excel files into DataFrames
            df1 = pd.read_excel(file_path1)
            df2 = pd.read_excel(file_path2)

            # Overwrite the corresponding tables in the database
            df1.to_sql("categories", conn, if_exists="replace", index=False)
            df2.to_sql("tasks", conn, if_exists="replace", index=False)

            print("Database tables updated successfully.")

        except Exception as e:
            print(f"An error occurred while importing data: {e}")

        finally:
            # Close the database connection
            conn.close()

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.path:
            export_path = e.path  # Get the path of the selected file
            exportDBAsExcel(dbname='preferez', export_path=export_path)
            # print(f"The selected export path: {export_path}.....................")
            page.snack_bar = ft.SnackBar(ft.Text(f"Exported to: {export_path}"), open=True)
        elif e.files:
            file_paths = [file.path for file in e.files]
            if len(file_paths) == 2:
                importDBFromExcel(dbname='preferez', file_path1=file_paths[0], file_path2=file_paths[1])
                page.snack_bar = ft.SnackBar(ft.Text("Data imported successfully!"), open=True)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Please select exactly two files for import."), open=True)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Export canceled!"), open=True)
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    page.overlay.append(pick_files_dialog)

    lists.controls.append(
        ft.ListTile(
            leading=ft.Icon(name=ft.Icons.IMPORT_EXPORT, size=28),
            title=ft.Text(f"Export Data", weight=ft.FontWeight.W_500), min_height=30,
            subtitle=ft.Text("Export your data to a file for backup or transfer.", size=10),
            on_click=lambda _: pick_files_dialog.get_directory_path(),
        )
    )
    lists.controls.append(
        ft.ListTile(
        leading=ft.Icon(name=ft.Icons.IMPORT_EXPORT,size=28),
        title=ft.Text(f"Import Data",weight=ft.FontWeight.W_500),min_height=30,
        subtitle= ft.Text("Import data from a file to restore or transfer.",size=10),
        on_click=lambda _:pick_files_dialog.pick_files(allow_multiple=True),
    ))

    loadDataTable(table1, 'preferez','categories',)
    loadDataTable(table2, 'preferez','tasks')
    
    return ft.SafeArea( 
            content=ft.Column(
                [
                    lists,
                    data
                ],scroll=ft.ScrollMode.ALWAYS
            ), expand= True
        )