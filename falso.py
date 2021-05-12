from io import BytesIO
from tkinter import TOP, Button, Tk, E, W, N, S, messagebox, Menu, Scrollbar, Text, RIGHT, Y, LEFT, END, DISABLED, \
    NORMAL, Entry, Checkbutton, IntVar, PhotoImage, Label, VERTICAL, HORIZONTAL, Listbox
from tkinter.ttk import Notebook, Frame, Combobox, Progressbar
from PIL import ImageTk, Image
from tkinter import messagebox


class GeneralVentana:
    __name: str
    __object_list: list
    __ventana: Tk
    __menubar = None
    __dict_keys: list = ("type", "item")


# region Rama Tabs
class GeneralNotebook:
    __parent = None
    __name: str
    __tab_list: list
    __notebook: Notebook


class GeneralTab:
    __parent: GeneralNotebook
    __name: str
    __div_list: list
    __tab: Frame
    __dict_keys: list = ("type", "item")


class GeneralDivTab:
    __parent = None
    __name: str
    __row: int
    __col: int
    __object_list: list
    __div: Frame
    __dict_keys: list = ("type", "item")


class GeneralTextAreaScrollTab:
    __parent: GeneralDivTab
    __name: str
    __text: Text = None
    __scroll: Scrollbar = None


class GeneralEntradaTexto:
    __parent: GeneralDivTab
    __name: str
    __text: Entry


class GeneralButton:
    __parent: GeneralDivTab
    __name: str
    __button: Button


class GeneralCombox:
    __parent: GeneralDivTab
    __name: str
    __box: Combobox


class GeneralCheckBox:
    __parent: GeneralDivTab
    __name: str
    __box: Checkbutton
    __variable: IntVar


class GeneralLabel:
    __parent: GeneralDivTab
    __name: str
    __label: Label


class GeneralPhoto:
    __parent: GeneralDivTab
    __name: str
    __image = None
    __label: Label


class GeneralProgressBar:
    __parent: GeneralDivTab
    __name: str
    __bar: Progressbar


class GeneralListBox:
    __parent: GeneralDivTab
    __name: str
    __list: Listbox


# endregion
# region Menu
class GeneralMenuBar:
    __parent: GeneralVentana
    __name: str
    __menu_list: list
    __menubar: Menu


class GeneralMenu:
    __parent: GeneralMenuBar
    __name: str
    __menu: Menu

# endregion

