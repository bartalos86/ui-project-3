from copy import deepcopy
from math import sqrt
import random
import numpy as np
import matplotlib.pyplot as plt


from point import Point
# random.seed(25)
colors = ["#ff0000", "#00ff00", "#0000ff", "#ff00ff"]

print(random.randrange(0,5))

points = []

def point_exists_in_collection(collection, point):
    for cp in collection:
        if(cp.get_code() == point.get_code()):
            return True

    return False

for i in range(20):
    point = Point(random.randrange(-5000,5000),random.randrange(-5000,5000))
    while(point_exists_in_collection(points,point)):
        point = Point(random.randrange(-5000,5000),random.randrange(-5000,5000))
    
    points.append(point)

for i in range(4000):
    base_point = points[random.randrange(len(points))]
    modified = deepcopy(base_point)
    modified.generate_offsets()
    points.append(modified)

points_dict = {}
points_dict["x"] = []
points_dict["y"] = []
points_dict["color"] = []  

for point in points:
    points_dict["x"].append(point.get_x())
    points_dict["y"].append(point.get_y())
    points_dict["color"].append(point.get_color())


# plt.plot(nrows=1, ncols=1, figsize=(8, 4))
# # x, y = points



def create_clusters_centroid(k = 4, centroids = None):
    if centroids == None:
        centroids = {"x": [], "y": [], "color": []};
        for i in range(k):
            centroids["x"].append(random.randrange(-5000,5000))
            centroids["y"].append(random.randrange(-5000,5000))
            centroids["color"].append(colors[i])
            print("pos: " + str(centroids["x"][i]) + ":" + str(centroids["y"][i]) + " "+ colors[i])
    
    for dp_index in range(len(points)):
        dindex = 0
        min_distance = 9999999
        for cl_index in range(k):
            distance = sqrt(pow(centroids["x"][cl_index] - points_dict["x"][dp_index],2) + pow(centroids["y"][cl_index] - points_dict["y"][dp_index],2))
            if min_distance > distance:
                min_distance = distance
                dindex = cl_index

        points_dict["color"][dp_index] = centroids["color"][dindex]
    
    return centroids


def create_centroid(k = 4):
    change_detected = True
    centroids = create_clusters_centroid(k)
    iteration = 0
    while change_detected:
        change_detected = False
        for i in range(k):
            centroid_color = centroids["color"][i]
            cluster_points = {"xsum": 0, "ysum": 0, "count": 0}
            for dp_index in range(len(points)):
                if points_dict["color"][dp_index] == centroid_color:
                    cluster_points["xsum"] += (points_dict["x"][dp_index])
                    cluster_points["ysum"] += (points_dict["y"][dp_index])
                    cluster_points["count"] = cluster_points["count"] +1
            new_x = int(cluster_points["xsum"] / cluster_points["count"])
            new_y = int(cluster_points["ysum"] / cluster_points["count"])

            if centroids["x"][i] != new_x or centroids["y"][i] != new_y:
                centroids["x"][i] = new_x
                centroids["y"][i] = new_y
                change_detected = True

        if change_detected:
                print("change detected: iteration " + str(iteration))
                print(centroids)
        iteration = iteration +1
        centroids = create_clusters_centroid(k, centroids)






def draw_data():
    plt.scatter(x=(points_dict["x"]), y=(points_dict["y"]), c=(points_dict["color"]))

    plt.title('Scatter: $x$ versus $y$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim([-5000,5000])
    plt.ylim([-5000,5000])

    plt.show()


create_centroid()
draw_data()



