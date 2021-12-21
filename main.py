from tkinter import filedialog, Tk
from PIL import Image, ImageFont, ImageDraw
import os
from shutil import rmtree

# Cleaning of the frames folder
try:
    rmtree("frames/")
except FileNotFoundError:
    pass
os.mkdir("frames/")

# Creates dialog for choosing base gif
root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename()

# Checks if needed to resize gif
while True:
    resize = input("Resize gif (y/n): ").lower()
    if resize == "y" or resize == "n":
        break
    print("invalid response")

# Opens image and gets size if resizing
imageObject = Image.open(filepath)
if resize == "y":
    width = int(input("Width(current: " + str(imageObject.size[0]) + "): "))
    height = int(input("Height(current: " + str(imageObject.size[1]) + "): "))

# Configuration for options like the font
fontsize = int(input("Enter Font Size: "))
font = ImageFont.truetype("./impact.ttf", fontsize)
num_frames = imageObject.n_frames
text_top = input("Enter text to add (top): ").upper()
text_bottom = input("Enter text to add (bottom): ").upper()
shadowcolor = (0,0,0)

# Self explanitory function
def draw_text(x, y, text):
    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x, y),text,(255,255,255),font=font)

# Calls the draw text function on each frame and saves each as a bitmap image
for frame in range(0,imageObject.n_frames):
    y = 0
    imageObject.seek(frame)
    frame_object = imageObject.quantize(colors=254)
    if resize == "y":
        frame_object = frame_object.resize((width, height), Image.ANTIALIAS)
    width, height = frame_object.size
    draw = ImageDraw.Draw(frame_object)
    x = (width-draw.textsize(text_top, font=font)[0])/2
    draw_text(x,y,text_top)
    x = (width-draw.textsize(text_bottom, font=font)[0])/2
    y = height-fontsize-5
    draw_text(x,y,text_bottom)
    frame_object.save("frames/frame" + str(frame) + ".bmp")

# Appends all bitmap images in the frame folder to the all_frames list
files = os.listdir("frames/")
all_frames = []
for frame in range(len(files)):
    if frame != 0:
        file = "frames/"+"frame"+str(frame)+".bmp"
        loadedFrame = Image.open(file)
        loadedFrame.resize((width, height))
        all_frames.append(loadedFrame)

# Saves the frames to a singular gif file
firstFrame = Image.open("frames/frame0.bmp")
firstFrame.save('output.gif', save_all=True, append_images=all_frames[1:], loop=0)

# Cleanup used frames and removes the frames folder
firstFrame.close()
for file in all_frames:
    file.close()
rmtree("frames/")
