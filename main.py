from tkinter import filedialog, messagebox, Toplevel, ttk, IntVar, Text, Label
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
from shutil import rmtree
import sys

def getFilePath():
    files = [("Gif images", "*.gif")]
    filepath = filedialog.askopenfilename(filetypes = files)
    return filepath

def saveToFrame(image, font, fontsize, resize, text):
    global width
    global height
    global progressValue
    text_top = text[0]
    text_bottom = text[1]
    for frame in range(0,image.n_frames):
        y = 0
        image.seek(frame)
        frame_object = image.convert('P', palette=Image.ADAPTIVE, colors=253)
        if resize:
            width, height = resize
            frame_object = frame_object.resize((resize[0], resize[1]), Image.ANTIALIAS)
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
        # Saved for later as if the gif is too large it goes over the window elements
        #
        # render = ImageTk.PhotoImage(frame_object)
        # img = Label(root, image=render)
        # img.image = render
        # img.place(x=150, y=100)
        frame_object.save("frames/frame" + str(frame) + ".bmp")
        progressValue += 1
        progress['value'] = int((progressValue/image.n_frames)*100)
        root.update_idletasks()


def createGif():
    files = os.listdir("frames/")
    progressValue = 0
    all_frames = []
    num_frames = range(len(files))
    for frame in num_frames:
        if frame != 0:
            file = "frames/"+"frame"+str(frame)+".bmp"
            loadedFrame = Image.open(file)
            loadedFrame.resize((width, height))
            all_frames.append(loadedFrame)
            # Saved for later as if the gif is too large it goes over the window elements
            #
            # render = ImageTk.PhotoImage(loadedFrame)
            # img = Label(root, image=render)
            # img.image = render
            # img.place(x=150, y=100)
            progressValue += 1
            progress['value'] = int((progressValue/num_frames[-1])*100)
            root.update_idletasks()
    firstFrame = Image.open("frames/frame0.bmp")
    firstFrame.save('output.gif', save_all=True, append_images=all_frames[1:], loop=0)
    firstFrame.close()
    for file in all_frames:
        file.close()
    messagebox.showinfo(title="Done", message="Gif successfully created!")

def chooseImage():
    global filepath
    filepath = getFilePath()
    filename = filepath.split("/")[-1]
    fileLabel.configure(text=filename)

def changeStatus(message, location):
    global statusLabel
    statusLabel.destroy()
    statusLabel = ttk.Label(root)
    statusLabel.configure(font="-family {Segoe UI} -size 20")
    statusLabel.configure(text=message)
    statusLabel.place(relx=location[0], rely=location[1], width=300)

def createGifButton(box, text, width, height):
    global statusLabel
    global filepath
    box.destroy()
    imageObject = Image.open(filepath)
    if var.get() == 1:
        resize = [int(width), int(height)]
    else:
        resize = False
    try:
        rmtree("frames/")
    except FileNotFoundError:
        pass
    os.mkdir("frames/")
    fontsize = text[2]
    font = ImageFont.truetype("./impact.ttf", fontsize)
    changeStatus("Status: Writing to frames", [0.281, 0.021])
    saveToFrame(imageObject, font, fontsize, resize, text)
    changeStatus("Status: Saving to gif file", [0.281, 0.021])
    createGif()
    rmtree("frames/")
    filepath = ""
    fileLabel.configure(text="No File Selected")
    changeStatus("Status: Ready", [0.375, 0.021])

def resizeButtonPress(widthEntry, widthLabel, heightEntry, heightLabel):
    if var.get() == 0:
        widthEntry.place_forget()
        widthLabel.place_forget()
        heightEntry.place_forget()
        heightLabel.place_forget()
    elif var.get() == 1:
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
        configBox.configure(background="#f7f7f7")
        configBox.resizable(False, False)
        configBox.focus()

        bottomSeperator = ttk.Separator(configBox)
        bottomSeperator.place(relx=-0.085, rely=0.875,  relwidth=1.333)
        topSeperator = ttk.Separator(configBox)
        topSeperator.place(relx=0.31, rely=0.0,  relheight=0.875)
        topSeperator.configure(orient="vertical")

        fontSizeSelector = ttk.Spinbox(configBox, from_=1.0, to=1000.0)
        fontSizeSelector.insert(1, "1")
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

        var.set(0)
        resizeCheck = ttk.Checkbutton(configBox)
        resizeCheck.place(relx=0.066, rely=0.406, relheight=0.0, height=30)
        resizeCheck.configure(text="Resize Gif", variable=var, command=lambda: resizeButtonPress(widthEntry, widthLabel, heightEntry, heightLabel))

        topEntry = Text(configBox)
        topEntry.place(relx=0.393, rely=0.156, height=50, relwidth=0.525)
        topLabel = ttk.Label(configBox)
        topLabel.place(relx=0.579, rely=0.063, height=21, width=52)
        topLabel.configure(text="Top Text")

        bottomEntry = Text(configBox)
        bottomEntry.place(relx=0.393, rely=0.594, height=50, relwidth=0.525)
        bottomLabel = ttk.Label(configBox)
        bottomLabel.place(relx=0.579, rely=0.5, height=21, width=75)
        bottomLabel.configure(text="Bottom Text")

        okButton = ttk.Button(configBox)
        okButton.place(relx=0.661, rely=0.906, height=25, width=76)
        okButton.configure(text="Ok", command=lambda: createGifButton(configBox, [topEntry.get('1.0', 'end-1c'), bottomEntry.get('1.0', 'end-1c'), int(fontSizeSelector.get())], widthEntry.get(), heightEntry.get()))

        cancelButton = ttk.Button(configBox)
        cancelButton.place(relx=0.826, rely=0.906, height=25, width=76)
        cancelButton.configure(text="Cancel", command=lambda: configBox.destroy())

if __name__ == "__main__":
    progressValue = 0
    width, height = 0, 0
    shadowcolor = (0,0,0)
    filepath = ""
    resize = 0
    if sys.platform == "win32" or sys.platform == "linux":
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="adapta")
        root.configure(background='#ffffff')
    else:
        from tkinter import Tk
        root = Tk()
    root.resizable(False, False)
    root.title("Gif Text Generator")
    root.geometry("640x480")
    var = IntVar()

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

    statusLabel = ttk.Label(root)
    statusLabel.place(relx=0.375, rely=0.021, height=39)
    statusLabel.configure(font="-family {Segoe UI} -size 20")
    statusLabel.configure(text="Status: Ready")

    root.mainloop()
