import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

img = Image.new("RGB", (1920, 720))

draw = ImageDraw.Draw(img)

# draw.text((10, 10), "foo")
# draw.ellipse((100, 310, 150, 360))


class Bar:

    def __init__(self, pos, length, height, color):
        self.pos = pos
        self.length = length - height
        self.height = height
        self.color = color

    def draw(self, percentage, draw_object: ImageDraw.Draw):
        draw_object.arc((*self.pos, self.pos[0] + self.height, self.pos[1] + self.height), 90, -90)
        draw_object.arc((self.pos[0] + self.length,
                         self.pos[1], self.pos[0] + self.length + self.height, self.pos[1] + self.height), -90, 90)
        draw_object.line((self.pos[0] + self.height / 2, self.pos[1], self.pos[0] + self.length + self.height / 2, self.pos[1]))
        draw_object.line((self.pos[0] + self.height / 2, self.pos[1] + self.height, self.pos[0] + self.length + self.height / 2, self.pos[1] + self.height))
        draw_object.rectangle((self.pos[0], self.pos[1] + 1, self.pos[0] + ((self.length + self.height) * (percentage / 100)), self.pos[1] + self.height - 1), fill=(255, 0, 0))
        draw_object.arc((*self.pos, self.pos[0] + self.height, self.pos[1] + self.height), 90, -90)
        draw_object.arc((self.pos[0] + self.length,
                         self.pos[1], self.pos[0] + self.length + self.height, self.pos[1] + self.height), -90, 90)
        # draw_object.arc((self.pos[0] - 20, self.pos[1] - 10, self.pos[0] + 20, self.pos[1] + self.height + 10), 90, -90, width=20)

        img2 = Image.new("RGB", (self.height // 2, self.height), color=(255, 255, 255))
        draw2 = ImageDraw.Draw(img2)
        draw2.ellipse((0, 0, self.height, self.height), width=2000, fill=(0, 0, 0))
        img2.show()
        # data = np.array(img2)  # "data" is a height x width x 4 numpy array
        # red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability
        #
        # # Replace white with red... (leaves alpha values alone...)
        # white_areas = (red == 255) & (blue == 255) & (green == 255)
        # data[..., :-1][white_areas.T] = (0, 0, 0, 0)  # Transpose back needed
        #
        # im2 = Image.fromarray(data)
        # im2.show()


Bar((100, 100), 500, 30, (255, 0, 0)).draw(100, draw)

# img.show()
