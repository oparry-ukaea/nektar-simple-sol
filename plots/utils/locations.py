import os.path

# Store some useful locations in a dict
LOCATIONS = {}
LOCATIONS["plots_dir"] = os.path.abspath(os.path.dirname(__file__)+"/..")
LOCATIONS["repo_root"] = os.path.normpath(os.path.join(LOCATIONS["plots_dir"],".."))
LOCATIONS["runs_dir"]  = os.path.join(LOCATIONS["repo_root"],"runs")

def get_run_root(subdir):
    return os.path.join(LOCATIONS["runs_dir"],subdir)

def get_plot_path(fname):
    return os.path.join(LOCATIONS["plots_dir"],fname)

def get_template_root(template):
    return os.path.join(LOCATIONS["runs_dir"],"templates",template)