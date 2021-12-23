from tkinter import filedialog, Tk, messagebox, Toplevel, ttk, IntVar
from ttkthemes import ThemedTk
from PIL import Image, ImageFont, ImageDraw
import os
from shutil import rmtree
import sys

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

def createGifButton(box):
    global filepath
    box.destroy()
    imageObject = Image.open(filepath)
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

def resizeButtonPress(variable, widthEntry, widthLabel, heightEntry, heightLabel):
    print(variable.get())
    if variable.get() == 0:
        widthEntry.place_forget()
        widthLabel.place_forget()
        heightEntry.place_forget()
        heightLabel.place_forget()
    elif variable.get() == 1:
        widthEntry.place(relx=0.021, rely=0.656, height=20, relwidth=0.112)
        widthLabel.place(relx=0.021, rely=0.563, height=21, width=48)
        heightEntry.place(relx=0.167, rely=0.656, height=21, relwidth=0.112)
        heightLabel.place(relx=0.186, rely=0.563, height=21, width=38)

def gifConfiguration():
    global resize
    if filepath == "":
        messagebox.showerror("Error!", "No File Selected!")
    else:
        configBox = Toplevel()
        configBox.geometry("484x320")
        configBox.title("Configure Gif")
        configBox.configure(background="#ffffff")
        configBox.resizable(False, False)

        okButton = ttk.Button(configBox)
        okButton.place(relx=0.661, rely=0.906, height=25, width=76)
        okButton.configure(text="Ok", command=lambda: createGifButton(configBox))

        cancelButton = ttk.Button(configBox)
        cancelButton.place(relx=0.826, rely=0.906, height=25, width=76)
        cancelButton.configure(text="Cancel", command=lambda: configBox.destroy())

        bottomSeperator = ttk.Separator(configBox)
        bottomSeperator.place(relx=-0.085, rely=0.875,  relwidth=1.333)
        topSeperator = ttk.Separator(configBox)
        topSeperator.place(relx=0.31, rely=0.0,  relheight=0.875)
        topSeperator.configure(orient="vertical")

        fontSizeSelector = ttk.Spinbox(configBox, from_=1.0, to=1000.0)
        fontSizeSelector.place(relx=0.103, rely=0.188, relheight=0.1, relwidth=0.079)

        fontSizeLabel = ttk.Label(configBox)
        fontSizeLabel.place(relx=0.083, rely=0.094, height=21)
        fontSizeLabel.configure(text="Font Size:")

        widthEntry = ttk.Entry(configBox)
        widthLabel = ttk.Label(configBox)
        widthLabel.configure(text="Width")

        heightEntry = ttk.Entry(configBox)
        heightLabel = ttk.Label(configBox)
        heightLabel.configure(text="Height")

        var = IntVar()
        var.set(0)
        resizeCheck = ttk.Checkbutton(configBox)
        resizeCheck.place(relx=0.066, rely=0.406, relheight=0.0, height=30)
        resizeCheck.configure(text="Resize Gif", variable=var, command=lambda x = var: resizeButtonPress(x, widthEntry, widthLabel, heightEntry, heightLabel))

if __name__ == "__main__":
    width, height = 0, 0
    shadowcolor = (0,0,0)
    filepath = ""
    resize = 0
    print(sys.platform)
    if sys.platform == "win32":
        root = ThemedTk(theme="adapta")
        root.configure(background='#ffffff')
    elif sys.platform == "linux":
        root = ThemedTk(theme="adapta")
        root.configure(background='#ffffff')
    else:
        root = Tk()
    root.resizable(False, False)
    root.title("Gif Text Generator")
    root.geometry("640x480")

    selectFile = ttk.Button(root, command=lambda:chooseImage())
    selectFile.place(relx=0.016, rely=0.792, height=44, width=87)
    selectFile.configure(text="Select Gif")

    outputGif = ttk.Button(root, command=lambda:gifConfiguration())
    outputGif.place(relx=0.016, rely=0.896, height=44, width=87)
    outputGif.configure(text="Create Gif")

    progress = ttk.Progressbar(root)
    progress.place(relx=0.172, rely=0.917, relwidth=0.797, relheight=0.0, height=22)
    progress.configure(length="510")

    fileLabel = ttk.Label(root)
    fileLabel.place(relx=0.172, rely=0.813, height=31)
    fileLabel.configure(text="No File Selected")

    root.mainloop()
