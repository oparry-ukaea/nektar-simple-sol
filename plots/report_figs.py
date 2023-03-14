
from utils import get_plot_path, get_plot_style, read_nektar_src, read_an_src

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, gridspec

rho_color='blue'
u_color='red'
T_color='green'

#--------------------------------------------------------------------------------------------------
def process_nektar_src(nek_src):
    params = nek_src.get_session().GetParameters()
    th = params['THETA']
    smax = params.get('srcs_smax',110.0)
    xmax = smax*np.cos(th)
    ymax = smax*np.sin(th)
    interp_str=f"line=1101,0,0,{xmax},{ymax}"

    x = nek_src.get('x',mode='interppoints',interp_str=interp_str)
    y = nek_src.get('y',mode='interppoints',interp_str=interp_str)
    s = x*np.cos(th) + y*np.sin(th)
    rho = nek_src.get('rho',mode='interppoints',interp_str=interp_str)
    rhou = nek_src.get('rhou',mode='interppoints',interp_str=interp_str)
    rhov = nek_src.get('rhov',mode='interppoints',interp_str=interp_str)
    vel = np.cos(th)*rhou + np.sin(th)*rhov
    E    = nek_src.get('E',mode='interppoints',interp_str=interp_str)
    T    = (E-(rhou*rhou/rho + rhov*rhov/rho)/2)/rho*(params["GAMMA"]-1.0)/params["GASCONSTANT"]

    # Store ICs
    rho_ICs = [float(params["RHOINF"]) for ix in x]
    u_ICs   = [0.0 for ix in x]
    # Temp overwrite of pinf - should this be set in the config anyway?
    params["PINF"] = "0.66666666666666666666666666"
    T_ICs   = [float(params["PINF"])/(float(params["GAMMA"])-1) for ix in x]

    return dict(s=s,rho=rho,u=vel,T=T,rho_ICs=rho_ICs,u_ICs=u_ICs,T_ICs=T_ICs)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def plot_prof(ax,nek_src,an_src, fldname, sty_kws, mode='prof'):
    an_sty_kws = sty_kws["an"][fldname]
    nek_sty_kws = sty_kws["nek"][fldname]

    if mode =='prof':
        ax.plot(an_src.get('s'), an_src.get(fldname), label='analytic', **an_sty_kws)
        ax.plot(nek_src.get('s'), nek_src.get(fldname), label='Simple SOL', **nek_sty_kws)
        ax.plot(nek_src.get('s'),nek_src.get(fldname+'_ICs'),linestyle=':',color='grey',label='ICs')
    elif mode =='res':
        res = (an_src.get(fldname)-nek_src.get(fldname))/an_src.get(fldname)
        ax.plot(an_src.get('s'), res, label='residual', **nek_sty_kws)
        ax.hlines(0, *ax.get_xlim(), linestyle=':',color='grey')
    return ax
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def comp_analytic_steady_state(run_dir,output_fpath = get_plot_path("simple-SOL-rot45_comp_profs_analytic.png"),save=True):
    # Data sources
    an_src = read_an_src('analytic_sigma2.csv')
    nek_src = read_nektar_src(run_dir,chk_num=None,plot_style="points")
    # Workaround for the fact add_field doesn't work with interpolation
    nek_src = process_nektar_src(nek_src)

    # plot_styles
    an_sty_kws = {}
    an_sty_kws["rho"] = get_plot_style("line",linestyle='--',color=rho_color)
    an_sty_kws["u"] = get_plot_style("line",linestyle='--',color=u_color)
    an_sty_kws["T"] = get_plot_style("line",linestyle='--',color=T_color)
    nek_sty_kws = {}
    nek_sty_kws["rho"] = get_plot_style("points",mec=rho_color,mfc=rho_color,markevery=10)
    nek_sty_kws["u"] = get_plot_style("points",mec=u_color,mfc=u_color,markevery=10)
    nek_sty_kws["T"] = get_plot_style("points",mec=T_color,mfc=T_color,markevery=10)
    sty_kws = dict(an=an_sty_kws,nek=nek_sty_kws)

    # Gen fig, axes
    fig = plt.figure(figsize=(16,8))
    gs = gridspec.GridSpec(2, 3, height_ratios=[9, 2],wspace=0.3)
    
    rho_ax = plot_prof(fig.add_subplot(gs[0,0]),nek_src,an_src,"rho",sty_kws)
    u_ax   = plot_prof(fig.add_subplot(gs[0,1]),nek_src,an_src,"u",sty_kws)
    T_ax   = plot_prof(fig.add_subplot(gs[0,2]),nek_src,an_src,"T",sty_kws)
    
    rho_res_ax = plot_prof(fig.add_subplot(gs[1,0]),nek_src,an_src,"rho",sty_kws,mode='res') 
    u_res_ax   = plot_prof(fig.add_subplot(gs[1,1]),nek_src,an_src,"u",sty_kws,mode='res') 
    T_res_ax   = plot_prof(fig.add_subplot(gs[1,2]),nek_src,an_src,"T",sty_kws,mode='res')

    # Tweak properties of some plot
    rho_ax.set_ylabel("n (dimensionless)")
    rho_ax.legend()
    u_ax.set_ylabel("u (dimensionless)")
    T_ax.set_ylabel("T (dimensionless)")
    rho_res_ax.legend()
    for ax in [rho_res_ax,u_res_ax,T_res_ax]:
        ax.set_ylim(-3e-3,3e-3)
        ax.set_xlabel("s / m")

    if save:
        fig.savefig(output_fpath)
        print(f"Steady-state comparison to analytic solution: {output_fpath}")
    else:
        plt.show()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def report_figs(run_dir,chk_num=None,save=True):
    comp_analytic_steady_state(run_dir,save=save)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    run_dir    = r"/tmp/neso-tests/solvers/SimpleSOL/2Drot45/"
    opts = dict(chk_num = None, save = True)

    report_figs(run_dir,**opts)
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()