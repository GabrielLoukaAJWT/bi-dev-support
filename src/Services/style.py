from tkinter import ttk
import tkinter as tk

import src.Services.settings as settings
import constants as cta



def setMainViewStyle(root: tk.Tk):
    style = ttk.Style(root)
    style.configure("Main.TFrame", background="#FFFFFF")
    style.configure("Title.TLabel", font=("Arial", 16, "bold"))
    style.configure("Body.TLabel", font=("Arial", 12))
    style.configure("Status.TLabel", font=("Arial", 10))

    style.configure("TEntry", padding=(6, 4))
    style.configure("Primary.TButton", padding=(10, 6), font=("Arial", 12, "bold"))

    style.map(
        "Primary.TButton",
        foreground=[("!disabled", "white")],
        background=[("!disabled", "#4CAF50"), ("active", "#45A049")],
    )

    style.configure("TCheckbutton", background="#f7f7f7", font=("Arial", 12))

    return style


def setQueryViewStyle(root: tk.Tk):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("MainFrame.TFrame")
    style.configure("MainPanel.TPanedwindow")
    style.configure("Footer.TFrame")
    style.configure("ActionFrame.TFrame")
    style.configure("LeftCard.TFrame", relief="flat")
    style.configure("RightCard.TFrame", relief="flat")
    style.configure("Header.TFrame")
    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#222")
    style.configure("Label.TLabel", font=("Segoe UI", 11), foreground="#444")
    style.configure("Status.TLabel", font=("Segoe UI", 10), foreground="red")
    style.configure("Clear.TButton", font=("Segoe UI", 11, "bold"))
    style.map("Clear.TButton",
            background=[("active", "#FF1414"), ("!disabled", "#FF3B3B")],
            foreground=[("active", "white")])
    style.configure("Action.TButton", font=("Segoe UI", 11, "bold"))
    style.map("Action.TButton",
            background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
            foreground=[("!disabled", "white")])
    style.configure("Options.TButton", font=("Segoe UI", 11, "bold"))
    style.map("Options.TButton",
            background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
            foreground=[("!disabled", "white")])
    
    return style