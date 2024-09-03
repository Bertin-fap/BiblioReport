__all__ = ['set_page_title']

import tkinter as tk
from tkinter import font as tkFont

import bmrgui.gui_rglobals as gg
from bmgui.gui_utils import font_size
from bmgui.gui_utils import mm_to_px

def set_page_title(self, master, page_name, institute, datatype = None):
    """
    """

    # Setting page title
    label_text = gg.PAGES_LABELS[page_name]
    page_title = label_text + " du " + institute

    # Setting font size for page label and button
    eff_label_font_size = font_size(gg.REF_LABEL_FONT_SIZE, master.width_sf_min)
    eff_label_pos_y_px  = mm_to_px(gg.REF_LABEL_POS_Y_MM * master.height_sf_mm, gg.PPI)
    eff_dy_px           = mm_to_px(gg.REF_LABEL_DX_Y_MM * master.height_sf_mm, gg.PPI)
    mid_page_pos_x_px   = master.win_width_px * 0.5

    # Creating title widget
    label_font = tkFont.Font(family = gg.FONT_NAME,
                             size   = eff_label_font_size)
    self.label = tk.Label(self,
                          text = page_title,
                          font = label_font)
    self.label.place(x = mid_page_pos_x_px,
                     y = eff_label_pos_y_px,
                     anchor = "center")

    if datatype:
        page_sub_title = f"Données {datatype}"

        # Creating title widget
        label_font = tkFont.Font(family = gg.FONT_NAME,
                                 size   = int(eff_label_font_size * 0.7))
        self.label = tk.Label(self,
                              text = page_sub_title,
                              font = label_font)
        self.label.place(x = mid_page_pos_x_px,
                         y = eff_label_pos_y_px + eff_dy_px,
                         anchor = "center")