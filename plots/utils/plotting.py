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

#--------------------------------------------------------------------------------------------------
def plot_2d_field(data_src,varname,mode='scatter',log=False,output_fpath='2d_field_anim.mp4',save=False):
    fwidth = 1.5 if mode=='img' else 9
    fig,axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 2))
    
    axes.set_xlabel("x")
    axes.set_ylabel("y")

    params =  data_src.get_session().GetParameters()
    x = data_src.get('x')
    y = data_src.get('y')
    f = data_src.get(varname)
    axes.set_title(data_src.label)

    if mode == 'img':
        # Regular spaced coords vary a bit after 12th decimal point; round them to get unique values:
        xb = sorted(set(np.round(x,decimals=12)))
        yb = sorted(set(np.round(y,decimals=12)))
        xindices = np.digitize(x,xb)-1
        yindices = np.digitize(y,yb)-1

        u = np.ones((len(xb),len(yb)))
        for i1D,(ix,iy) in enumerate(zip(xindices,yindices)):
            u[ix,iy] = f[i1D]

        if log:
            #u[u<0]=1e-6
            u = np.log10(u+1)

        plt.imshow(u,interpolation='none', extent=[min(xb),max(xb),min(yb),max(yb)],aspect=0.2,vmax=np.percentile(u,98))
    elif mode=='scatter':
        axes.scatter(x, y, c=f, label=data_src.label, **data_src.get_plot_kws())
    else:
        raise ValueError(f"plot_T_field: {mode} is not a valid mode string")

    if save:
        fig.savefig(output_fpath)
    else:
        plt.show(block=True)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, data_srcs,varname):
        self.data_srcs = data_srcs
        self.params = data_srcs[0].get_session().GetParameters()
        self.varname = varname

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = mpl_animation.FuncAnimation(self.fig, self.update, interval=1, 
                                          init_func=self.setup_plot, frames=len(data_srcs), blit=False)

    def setup_plot(self):
        """First frame."""
        first_src = self.data_srcs[0]
        self.scat = self.ax.scatter(first_src.get('x'), first_src.get('y'), c=first_src.get(self.varname), **first_src.get_plot_kws())
        return self.scat,

    def update(self, i):
        """Frame i."""

        print("Frame {}/{}".format(i+1,len(self.data_srcs)))
        data_src = self.data_srcs[i]
        f = data_src.get(self.varname)

        # Set colors..
        self.scat.set_array(f)
        self.ax.set_title(data_src.label)
        self.fig.canvas.draw()
        
        return self.scat,


def animate_2d_field(data_srcs,varname,mode='scatter',output_fpath='2d_field_anim.mp4',save=False):
    AS = AnimatedScatter(data_srcs,varname)        
    if save:
        FFwriter = mpl_animation.FFMpegWriter()
        AS.ani.save(output_fpath, writer = FFwriter)
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------