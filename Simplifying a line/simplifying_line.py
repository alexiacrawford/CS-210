"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Alexia Crawford
Credits: Worked with Sam
"""

import csv
import doctest
import geometry
import map_view
import config
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
def read_points(path: str) -> list[tuple[float, float]]:
    points = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                Easting, Northing = map(float, row)
                points.append((Easting, Northing))
            except ValueError:
                log.warning(f'Skip this invalid row: {row}')
    return points
def summarize(points: list[tuple[float, float]], tolerance: float = config.TOLERANCE_METERS) -> list[tuple[float, float]]:
    summary = [points[0]]
    epsilon = tolerance * tolerance
    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary.
        >>> path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
        >>> expect = [(0,0), (2,2), (2,4), (4,4)]
        >>> simple = summarize(path, tolerance=0.5)
        >>> simple == expect
        True
        """
        log.debug(f"Simplifying from {start}: {points[start]} to {end}: {points[end]}, {points[start + 1:end]}")
        log.debug(f"Summary so far: {summary}")
        if end - start > 2:
            map_view.scratch(points[start], points[end])
        max_ds_sq = 0
        farthest_point_idx = start
        for i in range(start, end + 1):
            distance_sqrd = geometry.deviation_sq(points[start], points[end], points[i])
            if distance_sqrd > max_ds_sq:
                max_ds_sq = distance_sqrd
                farthest_point_idx = i
        if max_ds_sq <= epsilon:
            summary.append(points[end])
            map_view.plot_to(points[end])
            return summary
        if max_ds_sq > epsilon:
            simplify(start, farthest_point_idx)
            return simplify(farthest_point_idx, end)

    simplify(0, len(points) - 1)
    map_view.clean_scratches()
    return summary
def main():
    map_view.init()
    points = read_points(config.UTM_CSV)
    for point in points:
        map_view.plot_to(point)
    print(f"{len(points)} raw points")
    summary = summarize(points, config.TOLERANCE_METERS)
    print(f"{len(summary)} points in summary")
    map_view.wait_to_close()
if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()
