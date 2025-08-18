from tkinter import ttk
import tkinter as tk

import src.Services.settings as settings
import constants as cta



def setMainViewStyle(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure("MainLogin.TFrame", background="#D3EEFF")

    style.configure("MainTitle.TLabel", font=("Arial", 16, "bold"), background="#D3EEFF")
    style.configure("MainLabel.TLabel", font=("Arial", 12), background="#D3EEFF")
    style.configure("MainConectionLabel.TLabel", background="#D3EEFF")
    style.configure("MainConectionLabelSuccess.TLabel", font=("Arial", 10), background="#D3EEFF", foreground="green")
    style.configure("MainConectionLabelFail.TLabel", font=("Arial", 10), background="#D3EEFF", foreground="red")
    style.configure("MainVersionLabel.TLabel", background="#D3EEFF")

    style.configure("TEntry", padding=(6, 4))

    style.configure("MainConnect.TButton", font=("Segoe UI", 11, "bold"))
    style.map("MainConnect.TButton",
            background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
            foreground=[("!disabled", "white")])

    style.configure("TCheckbutton", background="#f7f7f7", font=("Arial", 12))

    return style


def setQueryViewStyle(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    style.theme_use("clam")   
    style.configure("QVMainFrame.TFrame", background="#78B0D3", relief="flat")
    style.configure("QVHeader.TFrame", background="#78B0D3", relief="flat")
    style.configure("QVLeftCard.TFrame", background="#D3EEFF", relief="flat")
    style.configure("QVRightCard.TFrame", background="#D3EEFF", relief="flat")
    style.configure("QVActionFrame.TFrame", background="#D3EEFF", relief="flat")
    style.configure("QVFooter.TFrame", background="#D3EEFF", relief="flat")

    style.configure("QVMainPanel.TPanedwindow", background="#D3EEFF", relief="flat")
    style.configure("QVRightPanel.TPanedwindow", background="#D3EEFF", relief="flat")
    style.configure("QVOutputFrame.TFrame", background="#D3EEFF", relief="flat")
    style.configure("QVLogsFrame.TFrame", background="#D3EEFF", relief="flat")
    style.configure("QVToggleLogsFrame.TFrame", background="#D3EEFF", relief="flat")

    style.configure("QVLeftCardHeader.TLabel", font=("Segoe UI", 14, "bold"), background="#D3EEFF", foreground="#222")
    style.configure("QVRightCardHeader.TLabel", font=("Segoe UI", 14, "bold"), background="#D3EEFF", foreground="#222")
    style.configure("QVLabel.TLabel", font=("Segoe UI", 11), background="#D3EEFF", foreground="#444")
    style.configure("QVStatus.TLabel", font=("Segoe UI", 10), background="#D3EEFF", foreground="red")
    style.configure("QVExecLabel.TLabel", font=("Segoe UI", 14), background="#D3EEFF", foreground="#666")
    
    style.configure("QVClear.TButton", font=("Segoe UI", 11, "bold"))
    style.map("QVClear.TButton",
            background=[("active", "#E00000"), ("!disabled", "#E43232")],
            foreground=[("!disabled", "white")])
    style.configure("QVAction.TButton", font=("Segoe UI", 11, "bold"))
    style.map("QVAction.TButton",
            background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
            foreground=[("!disabled", "white")])
    style.configure("QVOptions.TButton", font=("Segoe UI", 11, "bold"))
    style.map("QVOptions.TButton",
            background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
            foreground=[("!disabled", "white")])
    
    return style


def setAnalyticsViewStyle(root: tk.Tk) -> ttk.Style:
     style = ttk.Style(root)
     style.configure("AVMainFrame.TFrame", background="#78B0D3", relief="flat")
     style.configure("AVSummaryFrame.TFrame", background="#78B0D3", relief="relief", borderwidth=2)
     style.configure("AVChartsFrame.TLabelFrame", font= ("Arial", 11, "bold"), padding=(10, 10), background="#78B0D3", relief="relief")
     style.configure("AVLeftChartFrame.TLabelFrame", font= ("Arial", 11, "bold"), padding=(10, 10), background="#78B0D3", relief="relief")
     style.configure("AVRightChartFrame.TLabelFrame", font= ("Arial", 11, "bold"), padding=(10, 10), background="#78B0D3", relief="relief")
     
     style.configure("AVTitle.TLabel", font=("Arial", 20, "bold"), background="#78B0D3")
     style.configure("AVTotLabel.TLabel", font = ("Arial", 11))
     style.configure("AVExecLabel.TLabel", font = ("Arial", 11))
     style.configure("AVSlowestLabel.TLabel", font = ("Arial", 11), background="#fff56e")
     style.configure("AVErrLabel.TLabel", font = ("Arial", 11), background="#ffa962")
     
     style.configure("AVTreeview.TTreeview", background="#eaeaea")
     
     style.configure("AVAction.TButton", font=("Segoe UI", 11, "bold"))
     style.map("AVAction.TButton",
        background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
        foreground=[("!disabled", "white")]
     )

     style.configure("AVClear.TButton", font=("Segoe UI", 11, "bold"))
     style.map("AVClear.TButton",
            background=[("active", "#E00000"), ("!disabled", "#E43232")],
            foreground=[("active", "white")])

     return style