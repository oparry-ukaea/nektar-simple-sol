from NekPlot.data import get_source
from NekPy.FieldUtils import Field, InputModule, OutputModule
import pyvista as pv

from utils import get_plot_path, get_run_root
import os.path
import time

#--------------------------------------------------------------------------------------------------
def animate_vtus(run_dir,chk_start,chk_end,chk_stride=1,output_fpath=get_plot_path('rho_u_T_anim.mp4'),**kwargs):
    meshes = read_vtus(run_dir,chk_start,chk_end,chk_stride,**kwargs)

    pl = gen_plotter(off_screen=True)

    # Get params from first checkpoint
    params = get_session_params(run_dir,chk_start)

    # Populate plotter with first mesh
    populate_plotter(pl,meshes[0],params)

    # Define update function
    def update(mesh):
        time.sleep(0.01)
        pl.clear()
        populate_plotter(pl,mesh,params)
        pl.update()
        pl.write_frame()

    # Write other frames
    pl.show(auto_close=False)
    pl.open_movie(output_fpath,framerate=10)
    for mesh in meshes[1:]:
        update(mesh)

    # Close plotter
    pl.close()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def convert_chk_to_vtu(session_fpaths,chk_fpath,vtu_fpath):
    print(f"Converting {chk_fpath} to {vtu_fpath}")
    if not os.path.exists(chk_fpath):
        raise RuntimeError(f"convert_chk_to_vtu: No chk file at {chk_fpath}")
    try:
        field = Field([], forceoutput=True)
        InputModule.Create("xml", field, *session_fpaths).Run()
        InputModule.Create("fld", field, chk_fpath).Run()
        OutputModule.Create("vtu", field, outfile=vtu_fpath).Run()
    except Exception as ex:
        print(f"Failed to convert chk file at {chk_fpath} to VTU using Nekpy.") 
        print(ex)
        return None
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def gen_plotter(**kwargs):
    kwargs['window_size'] = kwargs.pop('window_size',[int(0.8*d) for d in [1920,1080]])
    kwargs['border'] = kwargs.pop('border',True)
    return pv.Plotter(shape=(3, 1), **kwargs)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def get_session_params(run_dir,chk_num):
    nek_src = get_source("nektar", run_dir, chk_num=chk_num)
    return nek_src.get_session().GetParameters()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def populate_plotter(pl,mesh,params):
    # Color bar properties that are common to all three subplots
    sb_args_common = dict(
        height=0.8, width=0.05, vertical=True, position_x=0.05, position_y=0.05,
        title_font_size=18, label_font_size=14, shadow=False,
        )

    # Calculate derived fields
    E    = mesh.point_data['E']
    rho  = mesh.point_data['rho']
    rhou = mesh.point_data['rhou']
    mesh.point_data['u'] = rhou/rho
    mesh.point_data['T'] = (E-(rhou*rhou/rho)/2)/rho*(params["GAMMA"]-1.0)/params["GASCONSTANT"]

    pl.subplot(0, 0)
    sb_args = dict(sb_args_common)
    sb_args.update(title="rho")
    pl.add_mesh(mesh,scalars='rho', clim=[0.5,2.5], show_edges=False, scalar_bar_args=sb_args)
    pl.view_xy()

    pl.subplot(1, 0)
    sb_args = dict(sb_args_common)
    sb_args.update(title='u')
    pl.add_mesh(mesh.copy(),scalars='u', clim=[-1,1],show_edges=False, scalar_bar_args=sb_args)
    pl.view_xy()

    pl.subplot(2, 0)
    sb_args = dict(sb_args_common)
    sb_args.update(title='T')
    pl.add_mesh(mesh.copy(),scalars='T',clim=[0.7,1.4],show_edges=False, scalar_bar_args=sb_args)
    pl.view_xy()
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def read_vtu(run_dir,chk_num, **kwargs):
    file_base = kwargs.get('file_base')
    if not file_base:
        exit("read_vtu: Need to specify file prefix as a kwarg for now")

    fpath_base    = os.path.join(run_dir,f"{file_base}_{chk_num}")
    vtu_fpath     = fpath_base+".vtu"

    # Convert chk to vtu if necessary
    if not os.path.exists(vtu_fpath):
        session_fpaths = [os.path.join(run_dir,f"{file_base}.xml")]
        chk_fpath      = fpath_base+".chk"
        convert_chk_to_vtu(session_fpaths,chk_fpath,vtu_fpath)

    mesh = pv.read(vtu_fpath)
    
    # Stretch mesh in the y direction to make it easier to see
    scale_factors = kwargs.get('scale_factors',[1.0, 8.0, 1.0])
    mesh.scale(scale_factors, inplace=True)

    # Read vtu
    return mesh
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def read_vtus(run_dir,chk_start,chk_end,chk_stride,**kwargs):
    """Read vtus for checkpoints <chk_start>:<chk_end> inclusive, with a stride of <chk_stride>"""
    return [read_vtu(run_dir,chk_num, **kwargs) for chk_num in range(chk_start,chk_end+chk_stride,chk_stride)]
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def plot_single_vtu(run_dir, chk_num, output_fbase='rho_u_T', save=False, **kwargs):
    output_fpath = get_plot_path(f"{output_fbase}_{chk_num}.png")

    mesh = read_vtu(run_dir, chk_num, **kwargs)

    # Enable png output, if requested
    plotter_args={}
    show_args = {}
    if save:
        plotter_args['off_screen'] = True
        show_args['screenshot']    = output_fpath

    pl = gen_plotter(**plotter_args)
    params = get_session_params(run_dir,chk_num)
    populate_plotter(pl,mesh,params)
    pl.show(**show_args)
    if save:
        print(f"Wrote 2D animation to {output_fpath}")
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def main():
    mode     = 'animate'
    #mode     = 'single'
    run_lbl  = '2DSOL'

    run_dir = get_run_root(run_lbl)
    
    if mode=='animate':
        chk_start = 0
        chk_end = 100
        chk_stride = 1
        animate_vtus(run_dir, chk_start, chk_end, chk_stride=chk_stride, file_base=run_lbl)
    elif mode=='single':
        chk_num = 75
        save    = True
        plot_single_vtu(run_dir, chk_num, save=save, file_base=run_lbl)
    else:
        exit(f"Mode {mode} not recognised")
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':
    main()