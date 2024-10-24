import geopandas as gpd
import pandas as pd
from rtree import index

def duplicate_remover(intersections, clean_buffer, output_path, projected_crs):
    # Step 1: Reproject to a projected CRS (e.g., UTM zone 15N for Oklahoma)
    intersections = intersections.to_crs(epsg=projected_crs)

    # Step 2: Create a spatial index for efficient querying
    idx = index.Index()

    # Step 3: Add all points to the spatial index
    for i, geometry in enumerate(intersections.geometry):
        idx.insert(i, geometry.bounds)

    # Step 4: Create an empty GeoDataFrame to store filtered points
    filtered_intersections = gpd.GeoDataFrame(columns=intersections.columns, geometry='geometry')

    seen_points = set()  # Keep track of points we've already processed

    # Step 5: Iterate through each point and find nearby points within the buffer distance
    for i, point in intersections.iterrows():
        if i in seen_points:
            continue

        # Query points within the buffer distance
        possible_matches_index = list(idx.intersection(point.geometry.buffer(clean_buffer).bounds))
        nearby_points = intersections.iloc[possible_matches_index]

        # Filter points that are actually within the buffer distance
        nearby_points = nearby_points[nearby_points.geometry.distance(point.geometry) <= clean_buffer]

        # Add the first point from the group to the filtered points
        filtered_intersections = pd.concat([filtered_intersections, point.to_frame().T], ignore_index=True)

        # Mark all points in this buffer as seen
        seen_points.update(nearby_points.index)

    # Step 6: Save the cleaned GeoDataFrame to a shapefile
    filtered_intersections = filtered_intersections.set_geometry('geometry')
    filtered_intersections.to_file(output_path, driver='ESRI Shapefile')

    print(f"Filtered intersections saved: {len(filtered_intersections)}")

