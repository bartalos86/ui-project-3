from copy import deepcopy
from math import sqrt
import os
import random
import time
import numpy as np
import matplotlib.pyplot as plt


from point import Point

CLUSTERS = 20
STARTING_POINTS = 20
OTHER_POINTS = 4000
OFFSET = 150
MAX_ITERATIONS = 15000


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

#Other points
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

def control_correctness(centers, points):
    correct = True
    for center in centers:
        total_distance = 0
        points_in_cluster = filter_points_by_color(points, center.get_color())
        for point in points_in_cluster:
            total_distance += sqrt(pow(center.get_x() - point.get_x(),2) + pow(center.get_y() - point.get_y(),2))

        avg_distance = total_distance / len(points_in_cluster)
        if avg_distance > 500:
            print(f"Too big distance in cluster: {center.get_color()} - {avg_distance}")
            correct = False

    if(correct):
        print("All clusters are correct!")
    return correct
        


def create_clusters_centroid(k, points, centroids = None):
    if centroids == None:
        centroids = []
        for i in range(k):
            centroid = Point(random.randrange(-5000,5000),random.randrange(-5000,5000),colors[i])
            centroids.append(centroid)

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
            if count == 0:
                 
                new_x =  random.randrange(-5000,5000)
                new_y =  random.randrange(-5000,5000)
                change_detected = True
            else:
                new_x = int(xsum / count)
                new_y = int(ysum / count)

            if centroids[i].get_x() != new_x or centroids[i].get_y() != new_y:
                centroids[i].set_x(new_x)
                centroids[i].set_y(new_y)
                change_detected = True
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

        iteration = iteration +1
        
        medoids, points_local = create_clusters_medoid(k,points_local, medoids)
        if iteration > MAX_ITERATIONS:
            return (medoids, points_local)
       
    return (medoids, points_local)


def color_clusters_divisive(points,centroids):
    for dp_index in range(len(points)):
        dindex = -1
        min_distance = 9999999
        for cl_index in range(len(centroids)):
            distance = sqrt(pow(centroids[cl_index].get_x() - points[dp_index].get_x(),2) + pow(centroids[cl_index].get_y() - points[dp_index].get_y(),2))
            if min_distance > distance:
                min_distance = distance
                dindex = cl_index

        points[dp_index].set_color(centroids[dindex].get_color());
    
    return (centroids, points)

def divisive_centroid(k):
    points_local = deepcopy(points)
    centroids = []

    for point in points_local:
        point.set_color(colors[0])
    xsum = 0
    ysum = 0
    count = 0
    for dp_index in range(len(points_local)):
                xsum = xsum + int((points_local[dp_index].get_x()))
                ysum = ysum + int((points_local[dp_index].get_y()))
                count = count +1
    center_x = int(xsum / count)
    center_y = int(ysum / count)

    centroids.append(Point(center_x, center_y, color=colors[0]))
    color_counter = 1

    while len(centroids) < k:
       
        for centroid in centroids:
            xpsum = 0
            ypsum = 0
            countp = 0
            xmsum = 0
            ymsum = 0
            countm = 0

            for point in points_local:
                if centroid.get_color() == point.get_color():
                    if point.get_x() > centroid.get_x():
                        xpsum = xpsum + int((point.get_x()))
                        ypsum = ypsum + int((point.get_y()))
                        countp = countp +1
                    else:
                        xmsum = xmsum + int((point.get_x()))
                        ymsum = ymsum + int((point.get_y()))
                        countm = countm +1

            added_both = 0
            if countp > 0:
                center_xp = int(xpsum / countp)
                center_yp = int(ypsum / countp)
                if len(centroids) == k:
                    break
                else:
                    centroid.set_x(center_xp)
                    centroid.set_y(center_yp)
                    added_both += 1


            if countm > 0:
                center_xm = int(xmsum / countm)
                center_ym= int(ymsum / countm)
                if len(centroids) == k:
                    break
                else:
                    centroids.append(Point(center_xm, center_ym, colors[color_counter]))
                    color_counter += 1
                    added_both += 1

        centroids, points_local = color_clusters_divisive(points_local, centroids)
    
    return (centroids, points_local)

    



def draw_data(title, centers, points):
    for i in range(len(centers)):
           print(f"x: {centers[i].get_x()} y: {centers[i].get_y()}")

    points_dict = convert_to_points_dict(points)
    centers_dict = convert_to_points_dict(centers)
    plt.clf()
    plt.title(f"{title} - {STARTING_POINTS + OTHER_POINTS} points")
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.xlim([-5000,5000])
    plt.ylim([-5000,5000])

    plt.scatter(x=(points_dict["x"]), y=(points_dict["y"]), c=(points_dict["color"]), linewidths=1,s = 15)
    plt.scatter(x=(centers_dict["x"]), y=(centers_dict["y"]), marker ="^", c="yellow",
            edgecolor ="red")
    if not os.path.exists("images/"):
        os.mkdir("images")

    plt.savefig(f"images/{title} - {STARTING_POINTS + OTHER_POINTS}.png")



def generate_graphs():
    print("Generating K-means centroid graph....")
    start = time.time()
    centroids, points = create_centroid(CLUSTERS)
    end = time.time()
    control_correctness(centroids, points)
    print(f"Elapsed time: {end - start}s")
 
    print("Drawing...")
    draw_data("K-means centroid", centers=centroids, points=points)
    print("Graph saved!")
    print("Generating K-means medoid graph....")
    start = time.time()
    medoids, points = create_medoid(CLUSTERS)
    end = time.time()
    control_correctness(medoids, points)

    print(f"Elapsed time: {end - start}s")
    print("Drawing...")
    draw_data("K-means medoid", centers=medoids, points=points)
    print("Graph saved!")
    print("Generating Divisive centroid graph....")
    start = time.time()
    centroids, points = divisive_centroid(CLUSTERS)
    end = time.time()
    control_correctness(centroids, points)
    print(f"Elapsed time: {end - start}s")
    print("Drawing...")
    draw_data("Divisive centroid", centers=centroids, points=points)
    print("Graph saved!")


generate_graphs()



