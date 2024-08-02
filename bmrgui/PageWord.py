_all__ = ['create_word_biblio']

import tkinter as tk 

from bmgui.gui_utils import place_after
from bmgui.gui_utils import place_bellow

def create_word_biblio(self,master, page_name, institute, bibliometer_path, datatype):

    """interactive selection of items among the list list-item
    
    Args:
        list_item (list): list of items used for the selection
        
    Returns:
        list (list): list of selected items without duplicate
        
    """
   
    
    global val
 
    def selected_item():
        global val
        val = [list_items[i] for i in  listbox.curselection()]
        print(val)
    
    list_items = [str(x) for x in range(2012,2100)]
    
    listbox = tk.Listbox(self, width=5, height=10, selectmode=tk.MULTIPLE,)
    listbox.place(x = 40, y = 70,)
                         
    for idx,item in enumerate(list_items):
        listbox.insert(idx, item)
    
   
    listbox.selection_set(0)

    btn = tk.Button(self, text='OK', command=selected_item)
    
    place_bellow(listbox,btn,dy=10,dx=5)

    
    
    