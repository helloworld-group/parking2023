import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.ops import unary_union, polygonize

def rectilinear_decomposition(polygon):
    # Convert the Shapely Polygon to a list of exterior coordinates
    coords = list(polygon.exterior.coords)

    # Perform rectilinear decomposition
    rectilinear_polygons = list(polygonize(coords))

    return rectilinear_polygons

# Define the coordinates of the original rectilinear polygon
original_polygon_coords = [(0, 0), (6, 0), (6, 4), (3, 4), (3, 6), (0, 6)]

# Create a Shapely Polygon from the coordinates
original_polygon = Polygon(original_polygon_coords)

# Perform rectilinear decomposition
rectilinear_polygons = rectilinear_decomposition(original_polygon)

# Create the figure and axis
fig, ax = plt.subplots()

# Plot the original rectilinear polygon
ax.plot(*original_polygon.exterior.xy, label='Original Polygon', color='blue')

# Plot the decomposed rectilinear polygons
for i, polygon in enumerate(rectilinear_polygons):
    ax.plot(*polygon.exterior.xy, label=f'Rectilinear Polygon {i+1}', linestyle='dashed', color='red')

# Set the axis limits
ax.set_xlim(0, 7)
ax.set_ylim(0, 7)

# Add legend
ax.legend()

# Show the plot
plt.show()
