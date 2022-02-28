import os
from stl import mesh as ms
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import matplotlib.backends.backend_pdf


def populate_fig(filename, columns=3):
    mesh = ms.Mesh.from_file(filename)
    scale = mesh.points.flatten()

    fig = pyplot.figure(figsize=pyplot.figaspect(0.5))
    fig.suptitle(filename)

    for i in range(columns):
        index = i + 1
        ax = fig.add_subplot(2, columns, index, projection="3d")

        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
        ax.auto_scale_xyz(scale, scale, scale)
        ax.view_init(16, 180 / (columns + 1) * index)

        ax = fig.add_subplot(2, columns, index + columns, projection="3d")

        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
        ax.auto_scale_xyz(scale, scale, scale)
        ax.view_init(32, 180 / (columns + 1) * index)
    return fig


def plot_all(max_count=-1):
    count = 0
    figs = {}
    for root, dirs, filenames in os.walk("."):
        for filename in filenames:
            if filename.lower().endswith(".stl"):
                filepath = os.path.join(root, filename)
                print("Plotting " + len(root.split(os.sep)) * " ", filepath)
                fig = populate_fig(filepath)
                figs[filename] = fig
                if max_count >= 1 and count >= max_count:
                    return figs
                count += 1
    return figs


figs = plot_all()
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
for name, fig in figs.items():
    print("saving " + name)
    # fig.savefig(name+".png")

    pdf.savefig(fig)

pdf.close()
