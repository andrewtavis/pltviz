# =============================================================================
# Utility functions for viewing objects
#
# Contents
# --------
#   0. No Class
#       in_ipynb
#       disp
#       add_num_commas 
# =============================================================================

import pandas as pd

def in_ipynb():
    """Checks to see if code is being run in an iPython notebook"""
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False
    except NameError:
        return False  


def disp(obj, l=5, w=None):
    """
    Display with a version that allows for dimension inputs
    
    Parameters
    ----------
        obj : object
            Something to be displayed

        l : int : optional (default=5)
            The length to be displayed

        w : int : optional (default=None)
            The width to be displayed
            Note: default is show full

    Returns
    -------
        The item displayed at the given dimensions
    """
    import pandas as pd
    from IPython.display import display
    if type(obj) == pd.core.frame.DataFrame:
        if w == None:
            w = len(obj.columns)
            
        disp_df = obj[[c for c in list(obj.columns)[:w]]]
        from IPython.display import display
        if in_ipynb():
            display(disp_df.head(l))
            display(disp_df.shape)
        else:
            print(disp_df.head(l))
            print(disp_df.shape)

    elif type(obj) == dict:
        disp_dict = {k: obj[k] for k in obj.keys() if list(obj.keys()).index(k) in range(l)}
        print(disp_dict)

    elif type(obj) == list or type(obj) == str:
        print(obj[:l])

    else:
        if in_ipynb():
            display(obj)
        else:
            print(obj)


def add_num_commas(num):
    """Adds commas to a numeric string for readability"""
    num_str = str(num)
    num_str_no_decimal = num_str.split('.')[0]
    if '.' in num_str:
        decimal = num_str.split('.')[1]
    else:
        decimal = None

    str_list = [i for i in num_str_no_decimal]
    str_list = str_list[::-1]
    
    str_list_with_commas = [str_list[i] + ',' if i % 3 == 0 and i != 0 else str_list[i] for i in range(len(str_list))]
    str_list_with_commas = str_list_with_commas[::-1]
    
    str_with_commas = ''
    for i in str_list_with_commas:
        str_with_commas += i

    if decimal != None:
        return str_with_commas + '.' + decimal
    else:
        return str_with_commas