from copy import deepcopy
import random
import numpy as np
import matplotlib.pyplot as plt


from point import Point
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



for p in points:
    plt.plot(p.x,p.y)

plt.show()