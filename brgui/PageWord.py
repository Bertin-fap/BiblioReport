_all__ = ['create_word_biblio']

import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from pathlib import Path

from bmgui.gui_utils import place_after
from bmgui.gui_utils import place_bellow
from bmgui.gui_utils import font_size
from bmgui.gui_utils import mm_to_px
from brfuncts.makeword import master_make_document

from bmgui.gui_utils import last_available_years
import bmgui.gui_globals as gg
import brgui.gui_globals as ggr

def create_word_biblio(self,master, page_name, institute, bm_path, datatype):

    """interactive selection of items among the list list-item
    
    Args:
        list_item (list): list of items used for the selection
        
    Returns:
        list (list): list of selected items without duplicate
        
    """
   
    
    global year_list
    year_list = []
 
    def selected_item():
        global year_list
        year_list = [list_items[i] for i in  listbox.curselection()]
   
    def _create_word():
        global year_list
        if not year_list:
            messagebox.showinfo("MakeWord", "Please select years")
            return
        for year in year_list:
            datatype_without_blank = datatype.replace(' ','')
            master_make_document(Path(bm_path), year, institute, datatype_without_blank, "departement")
        
    from brgui.main_page import AppMain

    # Setting effective font sizes and positions (numbers are reference values)
    eff_etape_font_size      = font_size(gg.REF_ETAPE_FONT_SIZE,   AppMain.width_sf_min)
    eff_launch_font_size     = font_size(gg.REF_ETAPE_FONT_SIZE-1, AppMain.width_sf_min)
    eff_help_font_size       = font_size(gg.REF_ETAPE_FONT_SIZE-2, AppMain.width_sf_min)
    eff_select_font_size     = font_size(gg.REF_ETAPE_FONT_SIZE, AppMain.width_sf_min)
    eff_buttons_font_size    = font_size(gg.REF_ETAPE_FONT_SIZE-3, AppMain.width_sf_min)

    if_analysis_x_pos_px     = mm_to_px(10 * AppMain.width_sf_mm,  gg.PPI)
    if_analysis_y_pos_px     = mm_to_px(40 * AppMain.height_sf_mm, gg.PPI)
    year_analysis_label_dx_px  = mm_to_px( 0 * AppMain.width_sf_mm,  gg.PPI)
    year_analysis_label_dy_px  = mm_to_px(15 * AppMain.height_sf_mm, gg.PPI)
    launch_dx_px             = mm_to_px( 0 * AppMain.width_sf_mm,  gg.PPI)
    launch_dy_px             = mm_to_px( 5 * AppMain.height_sf_mm, gg.PPI)

    year_button_x_pos        = mm_to_px(gg.REF_YEAR_BUT_POS_X_MM * AppMain.width_sf_mm,  gg.PPI)
    year_button_y_pos        = mm_to_px(gg.REF_YEAR_BUT_POS_Y_MM * AppMain.height_sf_mm, gg.PPI)

        # Création du label
    self.font_Label_years = tkFont.Font(family = gg.FONT_NAME,
                                        size = eff_select_font_size,
                                        weight = 'bold')
    self.Label_years = tk.Label(self,
                                text = ggr.TEXT_YEAR_PI,
                                font = self.font_Label_years)
    self.Label_years.place(x = year_button_x_pos, y = year_button_y_pos)
    
    list_items = last_available_years(bm_path, gg.CORPUSES_NUMBER)
    
    listbox = tk.Listbox(self, width=5, height=10, selectmode=tk.MULTIPLE,)
    place_bellow(self.Label_years, listbox, dy = 10, dx=70)
                         
    for idx,item in enumerate(list_items):
        listbox.insert(idx, item)
    
    listbox.selection_set(0)
    
        # Création du boutton
    btn = tk.Button(self, text='OK', command=selected_item)
    
    place_bellow(listbox,btn,dy=10,dx=5)
    
    btn_create_word = tk.Button(self, text='Lancer la création des fichiers', command=_create_word)
    
    place_bellow(btn,btn_create_word,dy=10,dx=0)
    


    
    
    