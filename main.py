from tkinter import filedialog, Tk, Button, Label, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageFont, ImageDraw
import os
from shutil import rmtree

def getFilePath():
    files = [("Gif images", "*.gif")]
    return filedialog.askopenfilename(filetypes = files)

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

def saveToFrame(image, font, fontsize):
    global width
    global height
    size = getResizeSize(image)
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
    global filepath
    filepath = getFilePath()
    filename = filepath.split("/")[-1]
    fileLabel.configure(text=filename)

def createGifButton():
    global filepath
    try:
        imageObject = Image.open(filepath)
    except AttributeError:
        messagebox.showerror("Error!", "No File Selected!")
        return False
    try:
        rmtree("frames/")
    except FileNotFoundError:
        pass
    os.mkdir("frames/")
    fontsize = int(input("Enter Font Size: "))
    font = ImageFont.truetype("./impact.ttf", fontsize)
    saveToFrame(imageObject, font, fontsize)
    createGif()
    rmtree("frames/")
    filepath = ""
    fileLabel.configure(text="No File Selected")

if __name__ == "__main__":
    width, height = 0, 0
    shadowcolor = (0,0,0)
    filepath = ""
    root = Tk()
    root.title("Gif Text Generator")
    root.geometry("640x480")

    selectFile = Button(root, command=lambda:chooseImage())
    selectFile.place(relx=0.016, rely=0.792, height=44, width=87)
    selectFile.configure(text="Select Gif")

    outputGif = Button(root, command=lambda:createGifButton())
    outputGif.place(relx=0.016, rely=0.896, height=44, width=87)
    outputGif.configure(text="Create Gif")

    progress = Progressbar(root)
    progress.place(relx=0.172, rely=0.917, relwidth=0.797, relheight=0.0, height=22)
    progress.configure(length="510")

    fileLabel = Label(root)
    fileLabel.place(relx=0.172, rely=0.813, height=31)
    fileLabel.configure(text="No File Selected")

    root.mainloop()
