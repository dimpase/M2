To install the Macaulay2 Jupyter kernel and start Jupyter, run the following.  Note that Macaulay2 should already be installed on your system.

```sh
mkdir m2-jupyter
python3 -m venv m2-jupyter
source m2-jupyter/bin/activate
pip install git+https://github.com/Macaulay2/Macaulay2-Jupyter-Kernel
python3 -m m2_kernel install --user
pip install jupyterlab # or 'pip install notebook' for Jupyter Notebook
jupyter lab # or 'jupyter notebook'
```

At this point, your web browser should open with an instance of JupyterLab.  Click on the "M2" icon to open up to a new Macaulay2 notebook.

After it's installed, then further sessions only need the following:

```sh
source m2-jupyter/bin/activate
jupyter lab
```

See also:

* [this demo notebook](https://nbviewer.org/github/Macaulay2/Macaulay2-Jupyter-Kernel/blob/master/demo/demo.ipynb)
* the [kernel git repository](https://github.com/Macaulay2/Macaulay2-Jupyter-Kernel)
* [Macaulay2 + JupyterLab in GitHub Codespaces](https://github.com/d-torrance/codespaces-jupyter-macaulay2)