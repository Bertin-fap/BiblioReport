"""The `analysis_corpus_page` module allows to perform 
impact factors, keywords and coupling analysis.
"""

__all__ = ['create_analysis']

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
import brgui.gui_rglobals as gg
import brfuncts.functs_globals as gr
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
from brfuncts.bmr_utils import parse_kw_filename
from brfuncts.bmr_utils import create_kw_cloud
from brfuncts.bmr_utils import plot_countries_analysis
from brfuncts.bmr_utils import plot_if_analysis


# Standard library imports
import pathlib
from pathlib import Path

# 3rd party imports
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def _plot_countries_analysis(year,biblio_path,datatype,institute):
    plot_countries_analysis(year,biblio_path,datatype,institute)

def create_analysis(self, master, page_name, institute, bibliometer_path, datatype):
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
    def _launch_if_analysis_try():
        # Getting year selection
        year_select = variable_years.get()
        dep_select = variable_dep_if.get()
        plot_if_analysis(institute,
                         year_select,
                         dep_select,
                         bibliometer_path,
                         datatype,
                         bar_height_px,
                         verbose = True)
        
    def _launch_kw_plot():
        # Getting year selection, keyword selection and departement selection
        year_select = variable_years.get()
        kw_select = variable_kw.get()
        kw_inv_dict = dict(zip(gg.KW_DICT.values(),gg.KW_DICT.keys()))
        kw_select = kw_inv_dict[kw_select]
        dep_select = variable_dep.get()
        
        
        create_kw_cloud(institute, year_select, kw_select, dep_select, bibliometer_path,datatype,
                        verbose = False)


    def _launch_coupling_analysis_try():
        # Getting year selection
        year_select = variable_years.get()
        
        _plot_countries_analysis(int(year_select),bibliometer_path, datatype,institute)
        

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
    bar_height_px = mm_to_px(gr.BAR_HEIGHT * master.height_sf_mm, gg.PPI)
    

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
                                 text=gg.TEXT_IFPLOT,
                                 justify=etape_label_format,
                                 font=if_analysis_font,
                                 underline=etape_underline)

    if_analysis_label.place(x=if_analysis_x_pos_px,
                            y=if_analysis_y_pos_px)

    # - Setting help text
    help_label_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_help_font_size)
    help_label_if = tk.Label(self,
                             text=gg.HELP_IF_PLOT,
                             justify="left",
                             font=help_label_font)
    place_bellow(if_analysis_label,
                 help_label_if)
                 
    # Creating and setting department selection widgets
    if_path = bibliometer_path / Path(variable_years.get()) / Path('5 - Analyses\IFs')
    if_tup = parse_kw_filename(bibliometer_path,
                               variable_years.get().strip(),
                               'IF',
                               '.xlsx',
                               datatype,) # kw list of nametuples kw.dep, kw.year, kw.kw
    default_dep_if = if_tup.dep[-1]
    variable_dep_if = tk.StringVar(self)
    variable_dep_if.set(default_dep_if)
    mode_list =['png','HTML']
    default_mode = mode_list[-1]
    
    # - Creating departement selection label
    Label_if = tk.Label(self,
                        text=gg.TEXT_DEPT,
                        font=help_label_font)
                          
    # - Creating departement button option
    OptionButton_dep_if = tk.OptionMenu(self,
                                        variable_dep_if,
                                        *if_tup.dep)
    OptionButton_dep_if.config(font=self.font_OptionButton_years)
    
    place_bellow(help_label_if, Label_if, dy=30)
    place_after(Label_if, OptionButton_dep_if, dy=-5)
    

    if_analysis_launch_font = tkFont.Font(family=gg.FONT_NAME,
                                          size=eff_launch_font_size)
    if_analysis_launch_button = tk.Button(self,
                                          text=gg.TEXT_IF_ANALYSIS,
                                          font=if_analysis_launch_font,
                                          command= _launch_if_analysis_try)
    place_after(OptionButton_dep_if,
                if_analysis_launch_button,
                dx=50,
                dy=0)

    ###################################################
    # Creating and setting geographics analysis widgets
    ###################################################

    # - Setting title
    co_analysis_label_font = tkFont.Font(family=gg.FONT_NAME,
                                         size=eff_etape_font_size,
                                         weight='bold')
    co_analysis_label = tk.Label(self,
                                 text=gg.TEXT_GEOPLOT,
                                 justify="left",
                                 font=co_analysis_label_font)
    place_bellow(Label_if,
                 co_analysis_label,
                 dx=co_analysis_label_dx_px,
                 dy=co_analysis_label_dy_px)

    # - Setting help text
    help_label_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_help_font_size)
    help_label_if = tk.Label(self,
                          text=gg.HELP_GEO_PLOT,
                          justify="left",
                          font=help_label_font)
    place_bellow(co_analysis_label,
                 help_label_if)

    # - Setting launch button
    co_analysis_launch_font = tkFont.Font(family=gg.FONT_NAME,
                                          size=eff_launch_font_size)
    co_analysis_launch_button = tk.Button(self,
                                          text = gg.BUTT_GEOPLOT,
                                          font = co_analysis_launch_font,
                                          command = _launch_coupling_analysis_try)
    place_bellow(help_label_if,
                co_analysis_launch_button,
                dx = launch_dx_px,
                dy = launch_dy_px)

    ################################################
    # Creating and setting keywords analysis widgets
    ################################################

    # - Setting title
    kw_analysis_label_font = tkFont.Font(family = gg.FONT_NAME,
                                         size = eff_etape_font_size,
                                         weight = 'bold')
    kw_analysis_label = tk.Label(self,
                                 text=gg.TEXT_WORDCLOUD,
                                 justify="left",
                                 font=kw_analysis_label_font)
    place_bellow(co_analysis_launch_button,
                 kw_analysis_label,
                 dx=kw_analysis_label_dx_px,
                 dy=kw_analysis_label_dy_px)

    # - Setting help text
    help_label_font = tkFont.Font(family=gg.FONT_NAME,
                                  size=eff_help_font_size)
    help_label_kw = tk.Label(self,
                          text=gg.HELP_KW_PLOT,
                          justify="left",
                          font=help_label_font)
    place_bellow(kw_analysis_label,
                 help_label_kw)
                 
    # Creating and setting department selection widgets
    kw = parse_kw_filename(bibliometer_path,
                           variable_years.get().strip(),
                           'KW',
                           '.xlsx',
                           datatype) # kw list of nametuples kw.dep, kw.year, kw.kw
                           
    default_dep = kw.dep[-1]
    variable_dep = tk.StringVar(self)
    variable_dep.set(default_dep)
    
    # - Creating departement selection label
    Label_dep = tk.Label(self,
                         text=gg.TEXT_DEPT,
                         font=help_label_font)
                          
    # - Creating departement button option
    font_OptionButton_dep = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_buttons_font_size)
    OptionButton_dep = tk.OptionMenu(self,
                                      variable_dep,
                                      *kw.dep)
    OptionButton_dep.config(font=self.font_OptionButton_years)
    
    place_bellow(help_label_kw, Label_dep, dy=30)
    place_after(Label_dep, OptionButton_dep, dy=dy_year)
    
    # - Creating keyword selection label
    Label_kw = tk.Label(self,
                        text=gg.TEXT_KW,
                        font=help_label_font)
                         
    # Creating and setting keywords selection widgets
    kw_longtext = [gg.KW_DICT[x] for x in kw.kw]
    default_kw = kw_longtext[-1]
    variable_kw = tk.StringVar(self)
    variable_kw.set(default_kw)
                  
    # - Creating keyword button option
    font_OptionButton_kw = tkFont.Font(family=gg.FONT_NAME,
                                        size=eff_buttons_font_size)
    OptionButton_kw = tk.OptionMenu(self,
                                    variable_kw,
                                    *kw_longtext)
    OptionButton_kw.config(font=self.font_OptionButton_years)
    
    place_after(OptionButton_dep, Label_kw, dx=70, dy=10)
    place_after(Label_kw, OptionButton_kw, dy=dy_year)
    
    # - Setting launch button
    kw_analysis_launch_font = tkFont.Font(family=gg.FONT_NAME,
                                          size=eff_launch_font_size)
    kw_analysis_launch_button = tk.Button(self,
                                          text=gg.TEXT_KW_ANALYSIS,
                                          font=kw_analysis_launch_font,
                                          command= _launch_kw_plot)
    place_after(OptionButton_kw,
                kw_analysis_launch_button,
                dx=70,)
    