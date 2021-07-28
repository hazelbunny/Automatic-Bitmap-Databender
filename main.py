from random import randint
from math import sqrt
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from os import remove as delete_file
from os import path
import sys


def shift_chunk(file_input):
    scnew_file = file_input
    length = len(scnew_file)-1
    take_point = randint(1,length)
    removed_section = scnew_file[take_point]
    insertion_point = randint(1,length)
    scnew_file.remove(removed_section)
    scnew_file.insert(insertion_point,removed_section)
    return scnew_file
def scramble(file_input):
    snew_file = file_input
    output = shift_chunk(snew_file)
    for i in range(randint(0,10)):
        output = shift_chunk(output)
    return output

def get_right_click_path():
    global right_click_path
    global right_click_index
    right_click_path=write_path.replace(".", "-"+str(right_click_index)+".")
    right_click_index += 1
    return right_click_path
    

def on_press(event):
    global picked
    global picked_image
    global write_path
    sys.stdout.flush()
    if picked == True:
        if str(event.button) == "MouseButton.RIGHT":
            print("right click")
            #save_feature(picked_image)
            picked=False
            write_image(get_right_click_path(),picked_image)
        elif str(event.button) == "MouseButton.LEFT":
            write_image(write_path,picked_image)
            plt.clf()
            new_images()
            picked=False
        else:
            print(str(event.button))

def on_key(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'f5':
        print("refresh")
        plt.draw()


        
def onclick(event):
    global picked
    global picked_image
    picked = True
    line = event.artist
    data = line.get_url()    
    picked_image=imagelist[int(data)-1]



def write_image(path,array):
    im = Image.fromarray(array)
    im.save(path)
    pass

def datastream_to_numpy(datastream):
    if path.exists("temp.jpg"):
        delete_file("temp.jpg")
    with open("temp.jpg","bx") as new_img:
        for datum in datastream:
            new_img.write(datum)
        new_img.close()
        numpy_image_out = np.array(Image.open('temp.jpg'))
        return numpy_image_out
    

def new_images():
    
    #clear filestream
    array_of_numpys.clear()
    filestream = []
    
    with open(write_path,"br") as img:
        for line in img:
            filestream.append(line)
        img.close()
    
    #generate new images
    i=0
    while i<9:
        if i==0:
            #first image displays the previous picked image
            array_of_numpys.append(picked_image)
            fig.add_subplot(rows, columns, 1)
            # showing image
            plt.imshow(picked_image, picker=True, url=str(1))
            plt.axis('off')
            i+=1
        elif i>0:
            temp_filestream = []
            for datum in filestream:
                temp_filestream.append(datum)
            #other eight images are scrambled
            new_img_data=scramble(temp_filestream)
            try:
                numpy_image = datastream_to_numpy(new_img_data)
                array_of_numpys.append(numpy_image)
                # Adds a subplot at the 1st position
                fig.add_subplot(rows, columns, i+1)
                # showing image
                plt.imshow(numpy_image, picker=True, url=str(i+1))
                plt.axis('off')
                i+=1
            except:
                print("image failed to load")
    plt.draw()
    return array_of_numpys

#create matplotlib figure
fig = plt.figure(figsize=(10, 7))

# setting values to rows and column variables
rows = 3
columns = 3

#initialize index variable, which determines which image is being worked on
index = ""
img_path = "mustard_oil2\mustard_oil.jpg"

array_of_numpys=[]

#account for previous runs of program
version = 1
finished = False
write_path = img_path.replace(".","-v1.")
while finished == False:
    #fails if the file already exists
    try:
        with open(write_path,"x") as index_init:
            index_init.close()
        finished = True
    except:
        version += 1
        write_path = img_path.replace(".","-v"+str(version)+".")
delete_file(write_path)

picked_image = np.array(Image.open(img_path))
write_image(write_path,picked_image)
print("writing image "+str(picked_image)+" to "+write_path)

right_click_path=write_path
right_click_index = 0
get_right_click_path()

picked = False

#start program
kp = fig.canvas.mpl_connect('button_press_event', on_press)
cid = fig.canvas.mpl_connect('pick_event', onclick)
refresh = fig.canvas.mpl_connect('key_press_event', on_key)
imagelist = new_images()
plt.show()
