import concurrent.futures
import math
import os
import threading
import tkinter as tk
from idlelib.searchengine import get_selection
from tkinter import ttk
from tkinter.messagebox import showinfo

import Db.database
from Db.database import get_available_software
from GUI.loading_animation import LoadingAnimation
from download.downloader import download_gui, download
from download.verify import verify_downloads
from package.packager import package
from Crawler import crawler
from PIL import Image, ImageTk




class ProgramTable(tk.Frame):
    """Main Frame for the control of AID"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("AID -- automated internet downloader")

        self.loading_animation = LoadingAnimation(self.master)



        self.create_widgets()


    def create_widgets(self):
        """creates the version table view"""
        self.loading_animation.start()
        self.table_frame = ttk.Frame(self.master)
        self.table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Title row
        self.header_frame = ttk.Frame(self.table_frame)
        self.header_frame.pack(fill=tk.X)
        self.header_label = ttk.Label(self.header_frame, text="programs and versions", background="lightgray",
                                      anchor="center")
        self.header_label.pack(fill=tk.X)

        # Treeview
        columns = ("win64", "linux", "android")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="tree headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # column titles
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

        # Package name input frame
        self.pkg_frame = ttk.Frame(self.master)
        self.pkg_frame.pack(fill=tk.X, padx=10, pady=5)

        self.pkg_name_label = ttk.Label(self.pkg_frame, text="package name:", background="lightgray")
        self.pkg_name_label.pack(side=tk.LEFT, padx=(0, 5))

        self.pkg_name = ttk.Entry(self.pkg_frame)
        self.pkg_name.pack(side=tk.LEFT, expand=True, fill=tk.X)


        self.tree.bind("<Button-1>", self.on_click)


        self.download_button = ttk.Button(self.master, text="download and pack selected", command=self.process_clicked)
        self.download_button.pack(pady=10)

        threading.Thread(target=self.load_data).start()

    def load_data(self):
        """loads the application data from the database and inserts it into the table"""

        # crawl new versions
        application_links = crawler.getApplications("Crawler")

        # insert results to db
        Db.database.init_db()
        Db.database.append_software(application_links)

        # load all available apps (paltform and version) from db
        programs = Db.database.get_available_software()

        # diplay them all
        for program, versions in programs.items():
            program_item = self.tree.insert("", "end", text=program, tags=('program',))

            for version in versions:
                values = []
                for platform in ["win64", "linux", "android"]:
                    if version.get(platform):
                        values.append('☑')
                    elif version.get(platform) is False:
                        values.append('☐')
                    else:
                        values.append('')
                self.tree.insert(program_item, "end", text=version['version'], values=values, tags=())

        # tags for row types
        self.tree.tag_configure('program', background='lightblue')
        self.tree.tag_configure('version', background='white')
        self.tree.tag_configure('separator', background='lightgray')

        self.loading_animation.stop()

    def on_click(self, event):
        """Handles checkbox click"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            if column in ("#1", "#2", "#3"):  # Windows, Linux, Android columns
                current_value = self.tree.set(item, column)
                if current_value in ("☑", "☐"):
                    new_value = "☐" if current_value == "☑" else "☑"
                    self.tree.set(item, column, new_value)
                    self.update_checkbox(item, column, new_value == "☑")

    def update_checkbox(self, item, column, is_checked):
        """updates checkbox text in table"""
        program = self.tree.parent(item)
        program_name = self.tree.item(program, "text")
        version = self.tree.item(item, "text")
        platform = self.tree.heading(column)["text"]
        state = "activated" if is_checked else "deactivated"
        print(f"Checkbox for {program_name} version {version} - {platform}: {state}")

    def download(self, app_list, pkg_name):
        """starts the download of selected apps"""
        download_gui(app_list)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(package, app_list, pkg_name)
            path = future.result()

        self.loading_animation.stop()

        os.startfile(path)


    def process_clicked(self):
        """progresses download and pack button click"""
        print("download clicked")
        app_list, pkg_name = self.get_selected()
        self.loading_animation.start("creating package")
        thread = threading.Thread(target=self.download, args=(app_list, pkg_name)).start()


    def get_selected(self):
        """checks checkbox states and generates a dictionary of selected software"""
        selected_versions = []
        for program in self.tree.get_children():
            program_name = self.tree.item(program, 'text')
            for version_item in self.tree.get_children(program):
                version = self.tree.item(version_item, 'text')
                values = self.tree.item(version_item, 'values')
                for i, platform in enumerate(["win64", "linux", "android"]):
                    if values[i] == '☑':
                        selected_versions.append({
                            'program': program_name,
                            'version': version,
                            'platform': platform
                        })

        pkg_name = self.pkg_name.get()
        return selected_versions,pkg_name


if __name__ == "__main__":
    Db.database.get_available_software()
    root = tk.Tk()
    app = ProgramTable(root)
    root.geometry("650x800")
    root.mainloop()
