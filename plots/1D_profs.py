import matplotlib.animation as mpl_animation
from matplotlib import pyplot as plt
from utils import get_plot_path, get_plot_style, get_run_root, read_all_nektar_srcs

#--------------------------------------------------------------------------------------------------
def _animate_1D_profiles(run_dir, chk_start=0,chk_end=100, output_fname="profs_evo.mp4", save=False, **animate_kwargs):
    data_srcs =  read_all_nektar_srcs(run_dir,extra_fields=[("u","rhou/rho"),("T","(E-(rhou*rhou/rho)/2)/rho*(gamma-1.0)/GasConstant")],chk_start=chk_start,chk_end=chk_end)

    fig, axarr = plt.subplots(1,3,figsize=(15,5))
    
    # Get x-vals and params from the first source
    first_src = data_srcs[0]
    x = first_src.get('x')
    params = first_src.get_session().GetParameters()

    # rho panel
    rho_ax=axarr[0]
    rho_ax.set_ylim(0.9,2.5)
    rho_ax.set_xlabel("x")
    rho_ax.set_ylabel(r'$\rho$')
    rhoinit = params["RHOINF"]
    rho_ax.axhline(y=rhoinit, **(get_plot_style("line",color='grey',linestyle='--')))

    # u panel
    u_ax=axarr[1]
    u_ax.set_ylim(-1.2,1.2)
    u_ax.set_xlabel("x")
    u_ax.set_ylabel('u')
    uinit = 0
    u_ax.axhline(y = uinit, **(get_plot_style("line",color='grey',linestyle='--')))

    # T panel
    T_ax=axarr[2]
    T_ax.set_ylim(0.5,1.5)
    T_ax.set_xlabel("x")
    T_ax.set_ylabel('T')
    Einit = params["PINF"]/(params["GAMMA"]-1)
    Tinit = (Einit-(rhoinit*uinit**2)/2)/rhoinit*(params["GAMMA"]-1.0)/params["GASCONSTANT"]
    T_ax.axhline(y = Tinit, **(get_plot_style("line",color='grey',linestyle='--')))

    rho_line, = rho_ax.plot(x, x-999, **(get_plot_style("line")))
    u_line, = u_ax.plot(x, x-999, **(get_plot_style("line",color='blue')))
    T_line, = T_ax.plot(x, x-999, **(get_plot_style("line",color='green')))
    def _animate(ii):
        t = params["TIMESTEP"]*params["IO_CHECKSTEPS"]*(ii+1)
        rho_line.set_ydata(data_srcs[ii].get('rho'))
        u_line.set_ydata(data_srcs[ii].get('u'))
        T_line.set_ydata(data_srcs[ii].get('T'))
        # Set title on first plot only
        rho_ax.set_title("t = {:.2f}".format(t))
        return rho_line,

    animate_kwargs = dict(interval=100, blit=False)
    ani = mpl_animation.FuncAnimation(fig, _animate, frames=len(data_srcs), **animate_kwargs )

    if save:
        FFwriter = mpl_animation.FFMpegWriter()
        output_fpath = get_plot_path(output_fname)
        ani.save(output_fpath, writer = FFwriter)
        print(f"Wrote 1D profile animation to {output_fpath}")
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    run_lbl   = '1DSOL'
    save      = True
    chk_start = 0
    chk_end = 100
    _animate_1D_profiles(get_run_root(run_lbl), chk_start=chk_start, chk_end=chk_end, save=save)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()