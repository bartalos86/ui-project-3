from copy import deepcopy
from math import sqrt
import random
import numpy as np
import matplotlib.pyplot as plt


from point import Point

CLUSTERS = 8
STARTING_POINTS = 35
OTHER_POINTS = 8000
OFFSET = 250
MAX_ITERATIONS = 1000


def generate_color():
    r = format(random.randrange(0,255), '02x')
    g = format(random.randrange(0,255), '02x')
    b = format(random.randrange(0,255), '02x')
    color = f"#{r}{g}{b}"
    print(color)
    return color

generate_color()



# colors = ["#ff0000", "#00ff00", "#0000ff", "#ff00ff"]
colors = []
for i in range(CLUSTERS):
    colors.append(generate_color())

print(random.randrange(0,5))

points = []

def point_exists_in_collection(collection, point):
    for cp in collection:
        if(cp.get_code() == point.get_code()):
            return True

    return False

#Starting points
for i in range(STARTING_POINTS):
    point = Point(random.randrange(-5000,5000),random.randrange(-5000,5000))
    while(point_exists_in_collection(points,point)):
        point = Point(random.randrange(-5000,5000),random.randrange(-5000,5000))
    
    points.append(point)

for i in range(OTHER_POINTS):
    base_point = points[random.randrange(len(points))]
    modified = deepcopy(base_point)
    modified.generate_offsets(OFFSET)
    points.append(modified)


def convert_to_points_dict(points_arr):
    points_dict = {"x": [], "y": [], "color": []};

    for point in points_arr:
        points_dict["x"].append(point.get_x())
        points_dict["y"].append(point.get_y())
        points_dict["color"].append(point.get_color())
    return points_dict

def filter_points_by_color(points_arr, color):
    matches = []
    for point in points_arr:
        if point.get_color() == color:
            matches.append(point)

    return matches



# plt.plot(nrows=1, ncols=1, figsize=(8, 4))
# # x, y = points



def create_clusters_centroid(k, points, centroids = None):
    if centroids == None:
        centroids = []
        for i in range(k):
            centroid = Point(random.randrange(-5000,5000),random.randrange(-5000,5000),colors[i])
            centroids.append(centroid)

        # all_distances_fine = False
        # while not all_distances_fine:
        #     for i in range(k):
        #         all_distances_fine = True
        #         for j in range(i+1,k):
        #             distance = sqrt(pow(centroids[j].get_x() - centroids[i].get_x(),2) + pow(centroids[j].get_y() - centroids[i].get_y(),2))
        #             print("Distance: " + str(distance))

        #             if distance < 1500:
        #                 all_distances_fine = False
        #                 centroids[j].set_x(random.randrange(-5000,5000))
        #                 centroids[j].set_y(random.randrange(-5000,5000))
        #                 break
        #         if not all_distances_fine:
        #             break

    # print(convert_to_points_dict(centroids))
    for dp_index in range(len(points)):
        dindex = -1
        min_distance = 9999999
        for cl_index in range(k):
            distance = sqrt(pow(centroids[cl_index].get_x() - points[dp_index].get_x(),2) + pow(centroids[cl_index].get_y() - points[dp_index].get_y(),2))
            if min_distance > distance:
                min_distance = distance
                dindex = cl_index

        points[dp_index].set_color(centroids[dindex].get_color());
    
    return (centroids, points)


def create_centroid(k):
    change_detected = True
    points_local = deepcopy(points)
    centroids, points_local= create_clusters_centroid(k, points_local)
    iteration = 0
    while change_detected:
        change_detected = False
        i = 0
        for i in range(k):
            centroid_color = centroids[i].get_color()
            xsum = 0
            ysum = 0
            count = 0
            for dp_index in range(len(points_local)):
                if points_local[dp_index].get_color() == centroid_color:
                    xsum = xsum + int((points_local[dp_index].get_x()))
                    ysum = ysum + int((points_local[dp_index].get_y()))
                    count = count +1
                    # if points[dp_index].get_y() > 5000 or points[dp_index].get_y() < -5000:
                    #     #  print(xsum / count)
                    #     print(f"t: {points[dp_index].get_y()}" )
            if count == 0:
                 
                new_x =  random.randrange(-5000,5000)
                new_y =  random.randrange(-5000,5000)
                change_detected = True
                #  i = 0
                #  continue
            else:
                new_x = int(xsum / count)
                new_y = int(ysum / count)
                # print(f"newx {new_x} newy {new_y} cp {cluster_points['count']} xs {cluster_points['xsum']} ys {cluster_points['ysum']}")
             

            if centroids[i].get_x() != new_x or centroids[i].get_y() != new_y:
                centroids[i].set_x(new_x)
                centroids[i].set_y(new_y)
                change_detected = True
            # i = i+1

        # if change_detected:
                # print("change detected: iteration " + str(iteration))
                # print(centroids)
        iteration = iteration +1
        centroids, points_local = create_clusters_centroid(k, points_local, centroids)
    return (centroids, points_local)

def create_clusters_medoid(k, points, medoids = None):
    if medoids == None:
        medoids = []
        for i in range(k):
            medoid = random.choice(points)
            medoid.set_color(colors[i])
            medoids.append(medoid)

    # print(convert_to_points_dict(centroids))
    for dp_index in range(len(points)):
        dindex = -1
        min_distance = 9999999
        for md_index in range(k):
            distance = sqrt(pow(medoids[md_index].get_x() - points[dp_index].get_x(),2) + pow(medoids[md_index].get_y() - points[dp_index].get_y(),2))
            if min_distance > distance:
                min_distance = distance
                dindex = md_index

        points[dp_index].set_color(medoids[dindex].get_color());
    
    return (medoids, points)

def create_medoid(k):
    change_detected = True
    points_local = deepcopy(points)
    medoids, points_local = create_clusters_medoid(k,points_local)
    og_medoid = deepcopy(medoids)
    og_points = deepcopy(points_local)
    iteration = 0
    while change_detected:
        change_detected = False
        i = 0
        for md_index in range(k):
            medoid_color = medoids[i].get_color()
            points_in_cluster = filter_points_by_color(points_local, medoid_color)
            total_distance = 0
            
            for point in points_in_cluster:
                if point not in medoids:
                   total_distance += sqrt(pow(medoids[md_index].get_x() - point.get_x(),2) + pow(medoids[md_index].get_y() - point.get_y(),2))

            new_medoid = random.choice(points_in_cluster)
            new_total_distance = 0
            while new_medoid in medoids:
                new_medoid = random.choice(points_in_cluster)

            for point in points_in_cluster:
                if point not in medoids:
                   new_total_distance += sqrt(pow(new_medoid.get_x() - point.get_x(),2) + pow(new_medoid.get_y() - point.get_y(),2))
            
            if new_total_distance-total_distance < 0.01:
                medoids[i] = new_medoid
                change_detected = True
                # print(f"new distance: {new_total_distance} old distance: {total_distance}")
               
        iteration = iteration +1
        # print(convert_to_points_dict([medoids[0]]))
        
        medoids, points_local = create_clusters_medoid(k,points_local, medoids)
        if iteration > MAX_ITERATIONS:
            return (medoids, points_local)
       
    return (medoids, points_local)



def draw_data(title, centers, points):
    for i in range(len(centers)):
           print(f"x: {centers[i].get_x()} y: {centers[i].get_y()}")

    points_dict = convert_to_points_dict(points)
    centers_dict = convert_to_points_dict(centers)
    plt.clf()
    plt.title(title)
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim([-5000,5000])
    plt.ylim([-5000,5000])

    plt.scatter(x=(points_dict["x"]), y=(points_dict["y"]), c=(points_dict["color"]), linewidths=1,s = 15)
    plt.scatter(x=(centers_dict["x"]), y=(centers_dict["y"]), marker ="^", c="yellow",
            edgecolor ="red")
    plt.savefig(f"{title}.png")



def generate_graphs():
    print("Generating K-means centroid graph....")
    centroids, points = create_centroid(CLUSTERS)
    print("Drawing...")
    draw_data("K-means centroid", centers=centroids, points=points)
    print("Graph saved!")
    print("Generating K-means medoid graph....")
    medoids, points = create_medoid(CLUSTERS)
    print("Drawing...")
    draw_data("K-means medoid", centers=medoids, points=points)
    print("Graph saved!")


generate_graphs()



