from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as mpl_animation

PLOT_STYLES = {}
PLOT_STYLES["line"] = dict(linestyle="-", color='r')
PLOT_STYLES["points"]   = dict(color='b', linestyle="", linewidth=0.2, marker='x', markersize=5, markeredgewidth=0.5, mec='b', mfc='b', markevery=8 )
PLOT_STYLES["scatter"]  = dict()

valid_names_str = ",".join(list(PLOT_STYLES.keys()))

def get_plot_style(name, **kwargs):
    try:
        ps = dict(PLOT_STYLES[name])
        ps.update(kwargs)
        return ps
    except KeyError as ex:
        print(f"{name} is not a valid plot style; choose from [{valid_names_str}]")
        raise(ex)
