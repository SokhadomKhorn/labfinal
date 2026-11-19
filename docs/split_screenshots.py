"""
Splits large screenshots into smaller parts so they stay readable when placed in the report.
Output files are written next to the originals as <name>_partN.png.
Run:  python docs/split_screenshots.py
"""
import os
from PIL import Image

SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screenshots')


def trim_bottom(img, x0=0, x1=None, pad=14, light_bg=True):
    """Remove empty rows at the bottom, looking only at columns x0..x1."""
    x1 = x1 or img.width
    g = img.convert('L')
    px = g.load()
    for y in range(img.height - 1, -1, -1):
        for x in range(x0, x1, 2):
            v = px[x, y]
            if (light_bg and v < 200) or (not light_bg and v > 90):
                return img.crop((0, 0, img.width, min(img.height, y + pad)))
    return img


def save(img, name):
    img.save(os.path.join(SHOTS, name))
    print(f"{name}: {img.size}")


def split(src, parts):
    """parts: list of (out_name, (left, top, right, bottom), trim_kwargs_or_None)."""
    im = Image.open(os.path.join(SHOTS, src))
    for out, box, trim in parts:
        l, t, r, b = box
        piece = im.crop((l, t, r or im.width, b or im.height))
        if trim is not None:
            piece = trim_bottom(piece, **trim)
        save(piece, out)


# ---- Figure 2.1: pods.yaml -> Pod 1 / Pod 2 ----
split('Screenshot 2026-11-12 182811.png', [
    ('pods_yaml_part1.png', (0, 0, 560, 517), None),
    ('pods_yaml_part2.png', (0, 517, 560, 0), None),
])

# ---- Figure 2.2: Dockerfiles -> one part per service ----
split('dockerfiles_all.png', [
    ('dockerfiles_part1.png', (0, 0, 0, 250), None),
    ('dockerfiles_part2.png', (0, 250, 520, 426), None),
    ('dockerfiles_part3.png', (0, 426, 520, 612), None),
])

# ---- Dashboards: browser/header part + table part ----
for name in ('dashboard_pods', 'dashboard_services'):
    split(f'{name}.png', [
        (f'{name}_part1.png', (0, 0, 1000, 208), None),
        (f'{name}_part2.png', (268, 208, 1478, 0), None),
    ])

# ---- Postman: request part (window top, URL, body) + response part ----
POSTMAN = {
    # name: (request_bottom, response_top)
    'postman_1_register': (335, 576),
    'postman_2_get_all': (186, 186),
    'postman_3_get_by_id': (262, 576),
    'postman_4_update_mobile': (285, 576),
    'postman_5_update_password': (285, 576),
    'postman_6_update_both': (300, 576),
    'postman_7_verify': (235, 576),
    'postman_8_error_404': (285, 576),
}
for name, (req_bottom, resp_top) in POSTMAN.items():
    split(f'{name}.png', [
        (f'{name}_part1.png', (0, 0, 1000, req_bottom), None),
        (f'{name}_part2.png', (289, resp_top, 1340, 1002), {'x0': 0, 'x1': 1000}),
    ])

# ---- Figure 7.1: MongoDB query output -> two parts ----
split('mongo_students.png', [
    ('mongo_part1.png', (0, 0, 0, 479), None),
    ('mongo_part2.png', (0, 479, 720, 0), {'light_bg': False, 'x0': 0, 'x1': 300}),
])
