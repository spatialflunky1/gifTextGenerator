from tkinter import filedialog, Tk, Button
from PIL import Image, ImageFont, ImageDraw
import os
from shutil import rmtree

def getFilePath():
    return filedialog.askopenfilename()

width, height = 0, 0
def getResizeSize(imageToResize):
    global width
    global height
    while True:
        resize = input("Resize gif (y/n): ").lower()
        if resize == "y" or resize == "n":
            break
        print("invalid response")
    if resize == "y":
        width = int(input("Width(current: " + str(imageToResize.size[0]) + "): "))
        height = int(input("Height(current: " + str(imageToResize.size[1]) + "): "))
        return [width, height]
    return False

def saveToFrame(image):
    global width
    global height
    size = getResizeSize(imageObject)
    text_top = input("Enter text to add (top): ").upper()
    text_bottom = input("Enter text to add (bottom): ").upper()
    for frame in range(0,image.n_frames):
        y = 0
        image.seek(frame)
        frame_object = image.quantize(colors=253)
        if size:
            width, height = size
            frame_object = frame_object.resize((size[0], size[1]), Image.ANTIALIAS)
        width, height = frame_object.size
        draw = ImageDraw.Draw(frame_object)
        x = (width-draw.textsize(text_top, font=font)[0])/2
        draw.text((x-2, y-2), text_top, font=font, fill=shadowcolor)
        draw.text((x+2, y-2), text_top, font=font, fill=shadowcolor)
        draw.text((x-2, y+2), text_top, font=font, fill=shadowcolor)
        draw.text((x+2, y+2), text_top, font=font, fill=shadowcolor)
        draw.text((x, y),text_top,(255,255,255),font=font)
        x = (width-draw.textsize(text_bottom, font=font)[0])/2
        y = height-fontsize-5
        draw.text((x-2, y-2), text_bottom, font=font, fill=shadowcolor)
        draw.text((x+2, y-2), text_bottom, font=font, fill=shadowcolor)
        draw.text((x-2, y+2), text_bottom, font=font, fill=shadowcolor)
        draw.text((x+2, y+2), text_bottom, font=font, fill=shadowcolor)
        draw.text((x, y),text_bottom,(255,255,255),font=font)
        frame_object.save("frames/frame" + str(frame) + ".bmp")

def createGif():
    files = os.listdir("frames/")
    all_frames = []
    for frame in range(len(files)):
        if frame != 0:
            file = "frames/"+"frame"+str(frame)+".bmp"
            loadedFrame = Image.open(file)
            loadedFrame.resize((width, height))
            all_frames.append(loadedFrame)
    firstFrame = Image.open("frames/frame0.bmp")
    firstFrame.save('output.gif', save_all=True, append_images=all_frames[1:], loop=0)
    firstFrame.close()
    for file in all_frames:
        file.close()

def chooseImage():
    filepath = getFilePath()
    return filepath

def createGifButton():
    try:
        rmtree("frames/")
    except FileNotFoundError:
        pass
    os.mkdir("frames/")
    imageObject = Image.open(filepath)
    shadowcolor = (0,0,0)
    fontsize = int(input("Enter Font Size: "))
    font = ImageFont.truetype("./impact.ttf", fontsize)
    saveToFrame(imageObject)
    createGif()
    rmtree("frames/")

if __name__ == "__main__":
    root = Tk()
    root.title("Gif Text Generator")
    root.geometry("800x600")
    selectFile = Button(root, text="Select File", command=lambda:chooseImage())
    selectFile.pack()
    root.mainloop()
