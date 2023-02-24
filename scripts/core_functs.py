import json, pygame, math, random

def get_distance(coords, target):
     return math.sqrt((coords[0] - target[0])**2 + (coords[1] - target[1])**2)

#takes into account the inverted y-axis of pygame
def get_angle(coords, target):
    return math.atan2(target[1] - coords[1], target[0] - coords[0])

#vec = [start_point, end_point]
def dot(vec_1, vec_2):
    vec_diff = [[vec_1[1][i] - vec_1[0][i] for i in range(2)], [vec_2[1][i] - vec_2[0][i] for i in range(2)]]
    return (vec_diff[0][0] * vec_diff[1][0]) + (vec_diff[0][1] * vec_diff[1][1])

#default range is 0 to 1
def clamp(value, range=[0, 1]):
    return max(min(value, range[1]), range[0])

#linear interpolation
def lerp(current, target, rate):
    return current + (target - current) * rate

#fractional interpolation
def ferp(current, target, rate):
    return (target - current) * rate

def safe_divide(dividend, divisor):
    try: return dividend/divisor
    except ZeroDivisionError: return 0

def cut(surface, x, y, width, height):
    image = surface.copy()
    rect = pygame.Rect(x, y, width, height)
    image.set_clip(rect)
    croppedImg = surface.subsurface(image.get_clip())
    return croppedImg.copy()

def outline(surf, coords, mask, color=(255, 255, 255)):
    points = mask.outline()
    if len(points) >= 2:
        points = [[coords[j] + i[j] for j in range(2)] for i in points]
        pygame.draw.lines(surf, color, False, points, 3)

#swap color for surfs that only have 1 color
#color info contains (prev_color, next_color)
def swap_color(surf, color_info):
    surf = surf.copy()
    fill_surf = surf.copy()
    fill_surf.fill(color_info[1])
    surf.set_colorkey(color_info[0])
    fill_surf.blit(surf, (0, 0))
    return fill_surf

def randomize_color(color_except=[]):
    rand_color = tuple(map(random.randint, [0] * 3, [255] * 3))
    if rand_color not in color_except:
        return rand_color
    else: randomize_color(color_except=color_except)
    
#circle_info = [point, radius]
def circle_rect_collide(circle_info, rect):
    collide_point = circle_info[0].copy()

    if circle_info[0][0] > rect.right: collide_point[0] = rect.right
    elif circle_info[0][0] < rect.left: collide_point[0] = rect.left

    if circle_info[0][1] > rect.bottom: collide_point[1] = rect.bottom
    elif circle_info[0][1] < rect.top: collide_point[1] = rect.top

    distance = get_distance(collide_point, circle_info[0])
    if distance <= circle_info[1]: 
        return True

#circle = [point, radius]
#line = [start_point, end_point]
def circle_line_collide(circle, line):
    line_diff = [line[1][i] - line[0][i] for i in range(2)]
    line_magnitude = get_distance(line[0], line[1])
    dot_product = dot(line, [line[0], circle[0]])
    normalized_dot = clamp(dot_product/line_magnitude**2)
    collision_point = [line[0][i] + (normalized_dot * line_diff[i]) for i in range(2)]

    if get_distance(collision_point, circle[0]) <= circle[1]: 
        return True

def circle_to_surf(radius, color):
    surf = pygame.Surface([int(radius * 2)] * 2)
    surf.fill((0, 0, 0))
    surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return surf

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_json(file_path, content):
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=6)

#checks if a string represents an int or a float i.e. "12" --> True
#wrapper for string.isdigit() to cover for sign cases
def is_digit(string):
    for char in string:
        if char in ["-", "+", "."]:
            string = string.split(char)
            string = char.join(string)
            
    return string.isdigit()

#used to drill a dictionary and input values
def data_pierce(item, key_list, value={}):
    if len(key_list) > 0:
        if len(key_list) == 1:
            ret_val = value
        else: 
            ret_val = {}

        item[key_list[0]] = item.get(key_list[0], ret_val)
        data_pierce(item[key_list[0]], key_list[1:], value=value)

#tries to retrieve data specified in the dictionary path
#returns None if dictionary path doesn't exist
#kinda sounds like a scout right?
def data_scout(item, key_list):
    if len(key_list) > 0:
        if isinstance(item, dict):
            return data_scout(item.get(key_list[0]), key_list[1:])
    return item

def data_lift(item, target, current=0):
    if current < target:
        if isinstance(item, dict):
            data_carriage = []
            for k in item:
                data_carriage += data_lift(item.get(k), target, current= current + 1)
            return data_carriage

        return []

    elif current > target: return []
    else: return [item]
        
def mince_list(item, target, current=0):
    if current < target:
        if isinstance(item, list):
            data_carriage = []
            for i in item:
                data_carriage += mince_list(i, target, current=current+1)
        return data_carriage


    return [item]


    new_lst = []
def copy_dict(item):
    def replicate_dict(item):
        if isinstance(item, dict):
            copy_dict(item.copy())
        return item

    return {k : replicate_dict(v) for k, v in item.items()}

#this sounds so wrong
def prune_dict(item, blank_val={}):
    if isinstance(item, dict):
        for k in item.copy():
            v = prune_dict(item[k], blank_val=blank_val)
            if v == blank_val:
                item.pop(k)
            if not len(item):
                item = blank_val

    elif item == blank_val:
        return blank_val

    return item



