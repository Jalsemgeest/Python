# %%
# pip install pillow

from PIL import Image
test_image = Image.frombytes("RGB", (2, 2), bytes([255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255]))
test_image.save('test_image.png')


# %%
SECRET = "jake is cool"

def create_ascii_from_string(string):
	return list(map(lambda char: ord(char), list(string)))

print(list(SECRET))
print(create_ascii_from_string(SECRET))
ascii_secret = create_ascii_from_string(SECRET)

# %%
import random

image_width = 1920
image_height = 1080
rgb = [255 for val in range((image_width * image_height * 3))]

# %%
SALT = 15

def salt_ascii_value(value):
	return value + SALT

def unsalt_ascii_value(value):
	return value - SALT

salted_list = list(map(salt_ascii_value, ascii_secret))

# %%
range_offset = 30

# for i in range(len(salted_list)):
# 	rgb[i + range_offset] = salted_list[i]

# img = Image.frombytes("RGB", (image_width, image_height), bytes(rgb))
# img.save('decode-2-base3.png')

# %%
sami_image = Image.open('sami.png')
width = sami_image.size[0]
height = sami_image.size[1]
sami = sami_image.load()

new_sami_list = []
for h in range(height):
    for w in range(width):
        new_sami_list.append(sami[w, h][0])
        new_sami_list.append(sami[w, h][1])
        new_sami_list.append(sami[w, h][2])

for i in range(len(salted_list)):
	new_sami_list[i + range_offset] = salted_list[i]

new_sami_img = Image.frombytes("RGB", (width, height), bytes(new_sami_list))
new_sami_img.save('secret3.png')



# %%
decode_image = Image.open('secret3.png')
im = decode_image.load()

letters = []
for i in range(100):
	rgb = list(im[(range_offset / 3) + i, 0])
	letters.append(rgb[0])
	letters.append(rgb[1])
	letters.append(rgb[2])
	
print(letters)

# %%
unsalted_letters = list(map(unsalt_ascii_value, letters))
non_zero_list = list(filter(lambda x: x >= 0, unsalted_letters))

# %%
message = list(map(lambda x: chr(x), non_zero_list))

print(message)


