# Off-Grid Rugged Camp Wiki V1.0
# Local text file wiki program for offline or off-grid camping and survival.
# Copyright (C) 2024, Sourceduty - All Rights Reserved.

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import os

class DarkTheme:
    BACKGROUND_DARK = "#121212"
    BACKGROUND_MEDIUM = "#1E1E1E"
    BACKGROUND_LIGHT = "#2C2C2C"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B0B0B0"
    ACCENT = "#BB86FC"
    BUTTON_BG = "#3F3F3F"
    BUTTON_FG = "#FFFFFF"

class WikiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Off-Grid Rugged Camp Wiki")
        self.geometry("1000x700")

        self.wiki_dir = "wiki_pages"
        if not os.path.exists(self.wiki_dir):
            os.makedirs(self.wiki_dir)

        self.current_page = None
        self.is_creating_page = False
        self.create_style()
        self.create_widgets()
        self.show_default_help()

    def create_style(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TFrame", background=DarkTheme.BACKGROUND_DARK)
        style.configure("TButton", 
                        background=DarkTheme.BUTTON_BG, 
                        foreground=DarkTheme.BUTTON_FG,
                        font=('Helvetica', 10),
                        padding=5)
        style.map("TButton", background=[('active', DarkTheme.ACCENT)])
        style.configure("TLabel", 
                        background=DarkTheme.BACKGROUND_DARK, 
                        foreground=DarkTheme.TEXT_PRIMARY)

    def create_widgets(self):
        self.configure(bg=DarkTheme.BACKGROUND_DARK)

        # Top frame for buttons
        top_frame = ttk.Frame(self, style="TFrame")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Button configurations
        buttons = [
            ("List Pages", self.list_pages),
            ("View Page", self.view_page),
            ("Create Page", self.create_page),
            ("Edit Page", self.edit_page),
            ("Search Pages", self.search_pages),
            ("Delete Page", self.delete_page),
            ("Rename Page", self.rename_page),
            ("Help", self.show_default_help)
        ]

        for text, command in buttons:
            btn = ttk.Button(top_frame, text=text, command=command, style="TButton")
            btn.pack(side=tk.LEFT, padx=5)

        # Save button
        self.save_button = ttk.Button(top_frame, text="Save", command=self.save_page, style="TButton", state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Content area
        self.content_area = scrolledtext.ScrolledText(
            self, 
            wrap=tk.WORD, 
            bg=DarkTheme.BACKGROUND_MEDIUM, 
            fg=DarkTheme.TEXT_PRIMARY,
            insertbackground=DarkTheme.TEXT_PRIMARY,
            selectbackground=DarkTheme.ACCENT
        )
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            self, 
            textvariable=self.status_var, 
            style="TLabel"
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

    def set_status(self, message):
        self.status_var.set(message)
        self.after(3000, lambda: self.status_var.set(""))

    def show_default_help(self):
        help_text = """
Off-Grid Rugged Camp Wiki V1.0

====================================

Local text file wiki program for offline or off-grid camping and survival.
Copyright (C) 2024, Sourceduty - All Rights Reserved.
 
==================  Menu ==================

1. List Pages: View all available wiki pages.
2. View Page: Read the content of a specific page.
3. Create Page: Make a new wiki page.
4. Edit Page: Modify an existing page.
5. Search Pages: Find pages containing specific text.
6. Delete Page: Remove a page from the wiki.
7. Rename Page: Change the name of an existing page.
8. Save: Save changes when creating or editing a page.

To get started, try creating a new page or viewing an existing one.
If you need more help, click the 'Help' button at any time.
        """
        self.content_area.delete('1.0', tk.END)
        self.content_area.insert(tk.END, help_text)
        self.set_status("Showing help menu")

    def list_pages(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        pages = [f[:-4] for f in os.listdir(self.wiki_dir) if f.endswith('.txt')]
        self.content_area.delete('1.0', tk.END)
        if pages:
            self.content_area.insert(tk.END, "Available Pages:\n\n")
            for page in sorted(pages):
                self.content_area.insert(tk.END, f"• {page}\n")
            self.set_status(f"Found {len(pages)} pages")
        else:
            self.content_area.insert(tk.END, "No pages found.")
            self.set_status("No pages exist")

    def view_page(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        page_name = self.get_input("View Page", "Enter page name:")
        if page_name:
            file_path = os.path.join(self.wiki_dir, f"{page_name}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                self.content_area.delete('1.0', tk.END)
                self.content_area.insert(tk.END, f"Page: {page_name}\n\n")
                self.content_area.insert(tk.END, content)
                self.current_page = page_name
                self.set_status(f"Viewing page: {page_name}")
            else:
                messagebox.showerror("Error", f"Page '{page_name}' not found")

    def create_page(self):
        page_name = self.get_input("Create Page", "Enter new page name:")
        if page_name:
            file_path = os.path.join(self.wiki_dir, f"{page_name}.txt")
            if not os.path.exists(file_path):
                self.content_area.delete('1.0', tk.END)
                self.content_area.insert(tk.END, f"Creating new page: {page_name}\n\n")
                self.current_page = page_name
                self.is_creating_page = True
                self.save_button.config(state=tk.NORMAL)
                self.set_status(f"Creating new page: {page_name}")
            else:
                messagebox.showerror("Error", f"Page '{page_name}' already exists")

    def edit_page(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        page_name = self.get_input("Edit Page", "Enter page name to edit:")
        if page_name:
            file_path = os.path.join(self.wiki_dir, f"{page_name}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                self.content_area.delete('1.0', tk.END)
                self.content_area.insert(tk.END, f"Editing: {page_name}\n\n")
                self.content_area.insert(tk.END, content)
                self.current_page = page_name
                self.set_status(f"Editing page: {page_name}")
            else:
                messagebox.showerror("Error", f"Page '{page_name}' not found")

    def save_page(self):
        if self.current_page and self.is_creating_page:
            content = self.content_area.get('1.0', tk.END).strip()
            file_path = os.path.join(self.wiki_dir, f"{self.current_page}.txt")
            with open(file_path, 'w') as file:
                file.write(content)
            self.set_status(f"Page '{self.current_page}' saved")
            self.is_creating_page = False
            self.save_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "No page selected for saving or not in creation mode")

    def search_pages(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        query = self.get_input("Search Pages", "Enter search term:")
        if query:
            results = []
            for filename in os.listdir(self.wiki_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(self.wiki_dir, filename), 'r') as file:
                        content = file.read().lower()
                        if query.lower() in content:
                            results.append(filename[:-4])
            
            self.content_area.delete('1.0', tk.END)
            if results:
                self.content_area.insert(tk.END, "Search Results:\n\n")
                for page in results:
                    self.content_area.insert(tk.END, f"• {page}\n")
                self.set_status(f"Found {len(results)} matching pages")
            else:
                self.content_area.insert(tk.END, "No results found.")
                self.set_status("No pages matched the search")

    def delete_page(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        page_name = self.get_input("Delete Page", "Enter page name to delete:")
        if page_name:
            file_path = os.path.join(self.wiki_dir, f"{page_name}.txt")
            if os.path.exists(file_path):
                if messagebox.askyesno("Confirm", f"Delete page '{page_name}'?"):
                    os.remove(file_path)
                    self.set_status(f"Deleted page: {page_name}")
            else:
                messagebox.showerror("Error", f"Page '{page_name}' not found")

    def rename_page(self):
        self.is_creating_page = False
        self.save_button.config(state=tk.DISABLED)
        old_name = self.get_input("Rename Page", "Current page name:")
        if old_name:
            new_name = self.get_input("Rename Page", "New page name:")
            if new_name:
                old_path = os.path.join(self.wiki_dir, f"{old_name}.txt")
                new_path = os.path.join(self.wiki_dir, f"{new_name}.txt")
                if os.path.exists(old_path):
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        self.set_status(f"Renamed {old_name} to {new_name}")
                    else:
                        messagebox.showerror("Error", f"Page '{new_name}' already exists")
                else:
                    messagebox.showerror("Error", f"Page '{old_name}' not found")

    def get_input(self, title, prompt):
        return simpledialog.askstring(title, prompt)

if __name__ == "__main__":
    app = WikiApp()
    app.mainloop()
