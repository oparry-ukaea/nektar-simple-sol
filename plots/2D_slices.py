
from utils import get_plot_path, get_plot_style, get_run_root, read_all_nektar_srcs, read_an_src

import math
from matplotlib import pyplot as plt
import matplotlib.animation as mpl_animation
import numpy as np

#--------------------------------------------------------------------------------------------------
def animate_rho_vel_T_slices(run_dir,chk_start=0,chk_end=100,chk_stride=1,output_fpath=None,save=False):

    data_srcs=read_all_nektar_srcs(run_dir, chk_start=chk_start,chk_end=chk_end,chk_stride=chk_stride)

    # Get s vals and params from the first source
    first_src = data_srcs[0]
    params = first_src.get_session().GetParameters()
    th = params['THETA']
    xmax = 110.0*np.cos(th)
    ymax = 110.0*np.sin(th)
    interp_str=f"line=114,0,0,{xmax},{ymax}"
    x = first_src.get('x',mode='interppoints',interp_str=interp_str)
    y = first_src.get('y',mode='interppoints',interp_str=interp_str)
    s = x*np.cos(th) + y*np.sin(th)

    fig, axarr = plt.subplots(1,3,figsize=(16,5))

    # rho panel
    rho_ax=axarr[0]
    rho_ax.set_ylim(0.9,2.3)
    rho_ax.set_xlabel("s")
    rho_ax.set_ylabel('n')
    rhoinit = params["RHOINF"]
    rho_ax.axhline(y=rhoinit, color='grey',linestyle='--',label='ICs')
    rho_ax.legend()

    # u panel
    vel_ax=axarr[1]
    vel_ax.set_ylim(-1.2,1.2)
    vel_ax.set_xlabel("s")
    vel_ax.set_ylabel('$v_s$')
    uinit = 0
    vel_ax.axhline(y = uinit, color='grey',linestyle='--',label='ICs')

    # T panel
    T_ax=axarr[2]
    T_ax.set_ylim(0.7,1.4)
    T_ax.set_xlabel("s")
    T_ax.set_ylabel('T')
    Einit = params["PINF"]/(params["GAMMA"]-1)
    Tinit = (Einit-(rhoinit*uinit**2)/2)/rhoinit*(params["GAMMA"]-1.0)/params["GASCONSTANT"]
    T_ax.axhline(y = Tinit, color='grey',linestyle='--',label='ICs')

   # Plot analytic data
    an_fname    = 'analytic_sigma{:d}.csv'.format(int(params.get("SIGMA",2.0)))
    an_data_src = read_an_src(an_fname)
    an_s        = an_data_src.get('x')
    rho_ax.plot(an_s, an_data_src.get('rho'), **(get_plot_style("line",linestyle='--',color='blue')))
    vel_ax.plot(an_s, an_data_src.get('u'), **(get_plot_style("line",linestyle='--',color='red')))
    T_ax.plot(an_s, an_data_src.get('T'), **(get_plot_style("line",linestyle='--',color='green')))

    # Plot initial (dummy) Nektar data
    rho_line, = rho_ax.plot(s, s-999, color='blue',linestyle='-')
    vel_line, = vel_ax.plot(s, s-999, color='red',linestyle='-')
    T_line, = T_ax.plot(s, s-999, color='green',linestyle='-')

    def _animate(ii):
        rho  = data_srcs[ii].get('rho',mode='interppoints',interp_str=interp_str)
        rhou = data_srcs[ii].get('rhou',mode='interppoints',interp_str=interp_str)
        rhov = data_srcs[ii].get('rhov',mode='interppoints',interp_str=interp_str)
        vel = math.cos(th)*rhou + math.sin(th)*rhov
        E    = data_srcs[ii].get('E',mode='interppoints',interp_str=interp_str)
        T    = (E-(rhou*rhou/rho + rhov*rhov/rho)/2)/rho*(params["GAMMA"]-1.0)/params["GASCONSTANT"]
        rho_line.set_ydata(rho)
        vel_line.set_ydata(vel)
        T_line.set_ydata(T)
        # Set title on centre plot only
        vel_ax.set_title(data_srcs[ii].label)
        return rho_line,


    animate_kwargs = dict(interval=100, blit=False)
    ani = mpl_animation.FuncAnimation(fig, _animate, frames=len(data_srcs), **animate_kwargs )

    if save:
        FFwriter = mpl_animation.FFMpegWriter()
        ani.save(output_fpath, writer = FFwriter)
        print(f"Wrote 2D slice profiles animation to {output_fpath}")
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    # Choose run subdirectory, range of checkpoint files.
    run_subdir = '2Drot45'
    chk_start  = 0
    chk_end    = 105
    save       = True

    animate_rho_vel_T_slices(get_run_root(run_subdir),chk_start=chk_start,chk_end=chk_end,output_fpath=get_plot_path('rho_vel_T_2D_slice_anim.mp4'),save=save)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()