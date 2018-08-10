import math
from copy import deepcopy

header = '''ply
format ascii 1.0
comment made by Matt Zahara
element vertex 200
property float x
property float y
property float z
end_header
'''

#rotate the fake coordinates by 18 deg. giving you 20 rotated coordinates
#each set of rotated coordinates will contain 10 points
#this is a total of 200 points in this example

abs_min = 100
sets = []
base_points = []
for i in range(1, 11):
    _ = [i, i, 0]
    base_points.append(_)

print "base_points: ", base_points
    
for i in range(20):
    curr_set = []
    degrees_rotated = 18 * i
    rads = math.radians(degrees_rotated)
    curr = deepcopy(base_points)
    print "curr: ", curr
    for j in curr:
        x = float(j[0])
        y = float(j[1])
        z = float(j[2])
        new_x = round((z * math.sin(rads)) + (x * math.cos(rads)), 2)
        new_y = round(y, 2)
        new_z = round((z * math.cos(rads)) - (x * math.sin(rads)), 2)
#        abs_min = min(new_x, new_y, new_z, abs_min)
        curr_set.append([new_x, new_y, new_z])
    sets.append(curr_set)

print "------------"

angle = 0
for i in sets:
    for j in i:
        print "curr set @ ", angle, ": ", j
    print "---"
    angle += 18

#adjust all points so that they are all non-negative
#for i in sets:
#    for j in i:
#        j[0] += abs_min
#        j[1] += abs_min
#        j[2] += abs_min

    
file_contents = ""

for i in sets:
    for j in i:
        line = ""
        line += str(j[0]) + " "
        line += str(j[1]) + " "
        line += str(j[2]) + " "
        line += "\n"
        file_contents += line

print "file contents"
print file_contents

f = open("my_first_ply.ply", 'w')
f.write(header)
f.write(file_contents)
