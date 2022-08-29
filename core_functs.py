import json, pygame, math

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
    fill_surf = surf.copy()
    fill_surf.fill(color_info[1])
    surf.set_colorkey(color_info[0])
    fill_surf.blit(surf, (0, 0))
    return fill_surf

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

#used to load dict data but it returns 
#a value if there is no such key in the dict
def load_data(dict, key, ret_val=[]):
    try: data = dict[key]
    except KeyError: data = ret_val

    return data
#I know it's supposed to have none as an error return value
#but most of the data I wanna load are of type list
