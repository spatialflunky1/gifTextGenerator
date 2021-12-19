from tkinter import filedialog, Tk
from PIL import Image, ImageFont, ImageDraw
import os

while True:
    clear_frame_folder = input("Clear frame folder (might break if not cleared) (y/n): ").lower()
    if clear_frame_folder == "y" or clear_frame_folder == "n":
        break
    print("invalid response")

while True:
    resize = input("Resize gif (y/n): ").lower()
    if resize == "y" or resize == "n":
        break
    print("invalid response")

if clear_frame_folder == "y":
    for file in os.listdir("frames/"):
        os.remove("frames/"+file)

root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename()

imageObject = Image.open(filepath)
if resize == "y":
    width = int(input("Width(current: " + str(imageObject.size[0]) + "): "))
    height = int(input("Height(current: " + str(imageObject.size[1]) + "): "))

#savepath = filedialog.SaveFileDialog()
fontsize = int(input("Enter Font Size: "))
font = ImageFont.truetype("./impact.ttf", fontsize)
num_frames = imageObject.n_frames
text_top = input("Enter text to add (top): ").upper()
text_bottom = input("Enter text to add (bottom): ").upper()

def draw_text(x, y, text):
    draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
    draw.text((x-2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x+2, y+2), text, font=font, fill=shadowcolor)
    draw.text((x, y),text,(255,255,255),font=font)


shadowcolor = (0,0,0)
for frame in range(0,imageObject.n_frames):
    y = 0
    imageObject.seek(frame)
    if resize == "y":
        frame_object = imageObject.resize((width, height), Image.ANTIALIAS)
    width, height = frame_object.size
    draw = ImageDraw.Draw(frame_object)
    x = (width-draw.textsize(text_top, font=font)[0])/2
    draw_text(x,y,text_top)
    x = (width-draw.textsize(text_bottom, font=font)[0])/2
    y = height-fontsize-5
    draw_text(x,y,text_bottom)
    frame_object.save("frames/frame" + str(frame) + ".bmp")

files = os.listdir("frames/")
all_frames = []
for frame in range(len(files)):
    if frame != 0:
        file = "frames/"+"frame"+str(frame)+".bmp"
        print(file)
        loadedFrame = Image.open(file)
        loadedFrame.resize((width, height))
        all_frames.append(loadedFrame)

firstFrame = Image.open("frames/frame0.bmp")
firstFrame.save('output.gif', save_all=True, append_images=all_frames[1:], loop=0)
# imageObject.seek(0)
# imageObject.save('output.gif', save_all=True, append_images=all_frames)
