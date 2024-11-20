"""The `analysis_corpus_page` module allows to perform 
impact factors, keywords and coupling analysis.
"""

__all__ = ['create_graph_dep']

# Standard library imports
import os
import tkinter as tk
from pathlib import Path
from tkinter import font as tkFont
from tkinter import messagebox
import webbrowser 

# Third party imports
import matplotlib.pyplot as plt
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

# Local imports
import brgui.gui_globals as gg
import brfuncts.functs_globals as rg
import bmfuncts.pub_globals as pg
from bmgui.gui_utils import font_size
from bmgui.gui_utils import mm_to_px
from bmgui.gui_utils import place_after
from bmgui.gui_utils import place_bellow
from bmfuncts.consolidate_pub_list import get_if_db
from bmfuncts.pub_analysis import if_analysis
from bmfuncts.pub_analysis import coupling_analysis
from bmfuncts.pub_analysis import keywords_analysis
from bmfuncts.config_utils import set_org_params
from brfuncts.br_analyze import parse_kw_filename
from brfuncts.br_analyze import create_kw_cloud
from brfuncts.br_analyze import plot_countries_analysis
from brfuncts.br_analyze import plot_if_analysis
from brfuncts.graph_lib import plot_graph_departement


# Standard library imports
import pathlib
from pathlib import Path

# 3rd party imports
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

    
def _launch_graph_analysis(year,bibliometer_path, datatype,institute):
    G = plot_graph_departement(Path(bibliometer_path),institute,year,datatype.replace(' ',''))

def create_graph_dep(self, master, page_name, institute, bibliometer_path, datatype):
    """
    Description : function working as a bridge between the BiblioMeter
    App and the functionalities needed for the use of the app.

    Args: takes only self and bibliometer_path as arguments.
    self is the instense in which PageThree will be created.
    bibliometer_path is a type Path, and is the path to where the folders
    organised in a very specific way are stored.

    Returns:
        None.
    """

    # Internal functions
        
    def _launch_graph_analysis_try():
        year_select = variable_years.get()
        _launch_graph_analysis(int(year_select),bibliometer_path, datatype,institute)
        

    # Setting effective font sizes and positions (numbers are reference values)
    eff_etape_font_size = font_size(gg.REF_ETAPE_FONT_SIZE, master.width_sf_min)           # 14
    eff_launch_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-1, master.width_sf_min)
    eff_help_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-2, master.width_sf_min)
    eff_select_font_size = font_size(gg.REF_ETAPE_FONT_SIZE, master.width_sf_min)
    eff_buttons_font_size = font_size(gg.REF_ETAPE_FONT_SIZE-3, master.width_sf_min)
    if_analysis_x_pos_px = mm_to_px(10 * master.width_sf_mm, gg.PPI)
    if_analysis_y_pos_px = mm_to_px(40 * master.height_sf_mm, gg.PPI)
    co_analysis_label_dx_px = mm_to_px(0 * master.width_sf_mm, gg.PPI)
    co_analysis_label_dy_px = mm_to_px(10 * master.height_sf_mm, gg.PPI)
    kw_analysis_label_dx_px = mm_to_px(0 * master.width_sf_mm, gg.PPI)
    kw_analysis_label_dy_px = mm_to_px(10 * master.height_sf_mm, gg.PPI)
    launch_dx_px = mm_to_px(0 * master.width_sf_mm, gg.PPI)
    launch_dy_px = mm_to_px(3 * master.height_sf_mm, gg.PPI)
    year_button_x_pos = mm_to_px(gg.REF_YEAR_BUT_POS_X_MM * master.width_sf_mm, gg.PPI)     # 10
    year_button_y_pos = mm_to_px(gg.REF_YEAR_BUT_POS_Y_MM * master.height_sf_mm, gg.PPI)    # 26
    dy_year = -6
    bar_height_px = mm_to_px(rg.BAR_HEIGHT * master.height_sf_mm, gg.PPI)
    

    # Setting common attributes
    etape_label_format = 'left'
    etape_underline = -1


    # Getting institute parameters
    org_tup = set_org_params(institute, bibliometer_path)

    # Creating and setting year selection widgets
    default_year = master.years_list[-1]
    variable_years = tk.StringVar(self)
    variable_years.set(default_year)

    # - Creating years button option
    self.font_OptionButton_years = tkFont.Font(family=gg.FONT_NAME,
                                               size=eff_buttons_font_size)
    self.OptionButton_years = tk.OptionMenu(self,
                                            variable_years,
                                            *master.years_list)
    self.OptionButton_years.config(font=self.font_OptionButton_years)

    # - Creating year selection label
    self.font_Label_years = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_select_font_size,
                                        weight='bold')
    self.Label_years = tk.Label(self,
                                text=gg.TEXT_YEAR_KPI,
                                font=self.font_Label_years)
    self.Label_years.place(x=year_button_x_pos, y=year_button_y_pos)

    place_after(self.Label_years, self.OptionButton_years, dy=dy_year)

    # Creating and setting impact-factors analysis widgets
    
    # - Setting title
    if_analysis_font = tkFont.Font(family=gg.FONT_NAME,
                                size=eff_etape_font_size,
                                weight='bold')
    if_analysis_label = tk.Label(self,
                              text=gg.TEXT_GRAPH_DEP,
                              justify=etape_label_format,
                              font=if_analysis_font,
                              underline=etape_underline)

    if_analysis_label.place(x=if_analysis_x_pos_px,
                            y=if_analysis_y_pos_px)

    # - Setting help text
    help_label_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_help_font_size)
    help_label_if = tk.Label(self,
                             text=gg.HELP_GRAPH_DEP,
                             justify="left",
                             font=help_label_font)
    place_bellow(if_analysis_label,
                 help_label_if)
                 
    
    ## - Creating departement button option
    dep_analysis_launch_font = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_launch_font_size)
    dep_analysis_launch_button = tk.Button(self,
                                        text=gg.TEXT_IF_ANALYSIS,
                                        font=dep_analysis_launch_font,
                                        command= _launch_graph_analysis_try)
    place_bellow(help_label_if,
               dep_analysis_launch_button,
               dx=0,
               dy=10)
    