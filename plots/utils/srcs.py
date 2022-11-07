from NekPlot.data import get_source
from .locations import get_data_path
from .plotting import get_plot_style

#--------------------------------------------------------------------------------------------------
def read_an_src(fname,plot_style="line"):    
    src = get_source("dsv", get_data_path(fname))
    src.set_plot_kws(get_plot_style(plot_style))
    return src
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def read_nektar_src(run_dir,chk_num,plot_style="points"):
    nek_src = get_source("nektar", run_dir, chk_num=chk_num, label=f"Checkpoint {chk_num}")
    nek_src.set_plot_kws(get_plot_style(plot_style))
    return nek_src
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def read_all_nektar_srcs(run_dir, chk_start=0,chk_end=100,chk_stride=1,compute_gradients=False,plot_style="points",extra_fields=[]):
    data_srcs = []
    for chk_num in range(chk_start,chk_end+chk_stride,chk_stride):
        nek_src = get_source("nektar", run_dir, chk_num=chk_num, label=f"Checkpoint {chk_num}")
        params =  nek_src.get_session().GetParameters()
        nek_src.label = "t = {:.2f}".format(params["TIMESTEP"]*params["IO_CHECKSTEPS"]*(chk_num+1))
        if compute_gradients:
            nek_src.add_gradients()
        nek_src.set_plot_kws(get_plot_style(plot_style))
        # Add any extra fields
        for name_def in extra_fields:
            nek_src.add_field(name_def[0],name_def[1])
        data_srcs.append(nek_src)
    return data_srcs
#--------------------------------------------------------------------------------------------------