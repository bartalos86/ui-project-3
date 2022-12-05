from copy import deepcopy
from math import sqrt
import random
import numpy as np
import matplotlib.pyplot as plt


from point import Point

CLUSTERS = 5
def generate_color():
    r = hex(random.randrange(0,255))
    g = hex(random.randrange(0,255))
    b = hex(random.randrange(0,255))
    print(f"#{r}{g}{b}")

generate_color()

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

points_dict = {"x": [], "y": [], "color": []};

for point in points:
    points_dict["x"].append(point.get_x())
    points_dict["y"].append(point.get_y())
    points_dict["color"].append(point.get_color())


# plt.plot(nrows=1, ncols=1, figsize=(8, 4))
# # x, y = points



def create_clusters_centroid(k = 4, centroids = None):
    global points_dict
    if centroids == None:
        centroids = {"x": [], "y": [], "color": []};
        for i in range(k):
            centroids["x"].append(random.randrange(-5000,5000))
            centroids["y"].append(random.randrange(-5000,5000))
            centroids["color"].append(colors[i])
            # print("pos: " + str(centroids["x"][i]) + ":" + str(centroids["y"][i]) + " "+ colors[i])

        all_distances_fine = False
        while not all_distances_fine:
            for i in range(k):
                all_distances_fine = True
                for j in range(i+1,k):
                    distance = sqrt(pow(centroids["x"][j] - centroids["x"][i],2) + pow(centroids["y"][j] - centroids["y"][i],2))
                    print("Distance: " + str(distance))

                    if distance < 1500:
                        all_distances_fine = False
                        centroids["x"][j] = random.randrange(-5000,5000)
                        centroids["y"][j] = random.randrange(-5000,5000)
                        break
                if not all_distances_fine:
                    break



    
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
    global points_dict

    change_detected = True
    centroids = create_clusters_centroid(k)
    iteration = 0
    while change_detected:
        change_detected = False
        i = 0
        for i in range(k):
            centroid_color = centroids["color"][i]
            cluster_points = {"xsum": 0, "ysum": 0, "count": 0}
            xsum = 0
            ysum = 0
            for dp_index in range(len(points)):
                if points_dict["color"][dp_index] == centroid_color:
                    xsum = xsum + int((points_dict["x"][dp_index]))
                    ysum = ysum + int((points_dict["y"][dp_index]))
                    # print(xsum)
                    cluster_points["count"] += 1
                
            # print(cluster_points["count"])
            cluster_points["xsum"] = xsum
            cluster_points["ysum"] = ysum
            if cluster_points["count"] == 0:
                 
                print("regenerated")
                new_x =  random.randrange(-5000,5000)
                new_y =  random.randrange(-5000,5000)
                change_detected = True
                #  i = 0
                #  continue
            else:
                new_x = int(cluster_points["xsum"] / cluster_points["count"])
                new_y = int(cluster_points["ysum"] / cluster_points["count"])
                print(f"newx {new_x} newy {new_y} cp {cluster_points['count']} xs {cluster_points['xsum']} ys {cluster_points['ysum']}")
             

            if centroids["x"][i] != new_x or centroids["y"][i] != new_y:
                centroids["x"][i] = new_x
                centroids["y"][i] = new_y
                change_detected = True
            # i = i+1

        if change_detected:
                print("change detected: iteration " + str(iteration))
                # print(centroids)
        iteration = iteration +1
        centroids = create_clusters_centroid(k, centroids)
    return centroids






def draw_data():
    centroids = create_centroid()

    for i in range(len(centroids)):
           print(f"x: {centroids['x'][i]} y: {centroids['y'][i]}")

    plt.scatter(x=(points_dict["x"]), y=(points_dict["y"]), c=(points_dict["color"]))
    plt.scatter(x=(centroids["x"]), y=(centroids["y"]))
    
    plt.title('Scatter: $x$ versus $y$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim([-5000,5000])
    plt.ylim([-5000,5000])

    plt.show()


draw_data()



