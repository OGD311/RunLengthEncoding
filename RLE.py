from PIL import Image, ImageDraw
import random


#create test img
def testImg():
    img = Image.new(mode="RGB", color=(256, 256, 256), size=(8, 8))
    for x in range(img.width):
        for y in range(img.height):
            match random.randint(0,5):
                case 0:
                    img.putpixel((x,y),(0,0,0))
                case 1:
                    img.putpixel((x,y),(255,255,255))
                case 2:
                    img.putpixel((x,y),(128,128,128))
                case 3:
                    img.putpixel((x,y),(255,0,0))
                case 4:
                    img.putpixel((x,y),(0,255,0))
                case 5:
                    img.putpixel((x,y),(0,0,255))
                    
    img.save("Normal.png")
    return img

def openImg():
    img = Image.open("Normal.png")
    return img

#Read the image and create an array
def readImg(img):
    imgArray = []
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x,y))
            imgArray.append(pixel)

    return(imgArray)



#generate the RLE array
def genRLE(imgArray):
    RLEArray = []
    same = 1
    try:
        for i in range(len(imgArray)):
            if imgArray[i] == imgArray[i+1]:
                same += 1
            else:
                combined = (same,imgArray[i])
                RLEArray.append(combined)
                same = 1

    except:
        RLEArray.append((1,imgArray[i]))
        return(RLEArray)


def genRLEText(RLEArray):
    #print(RLEArray)
    with open("RLE.txt", "w") as file:
        for item in RLEArray:
            file.write(str(item)+"\n")
            #print(item)
    file.close()

def readRLEText():
    RLEArray = []
    file = open("RLE.txt")
    content = file.readlines()
    for i in range(0,len(content)):
        q = content[i]
        q = q[1:-2]
        c = q.index(",")
        num = (q[:c])
        colour = (q[c+2:]).strip("() ").split(",")
        colour = (int(colour[0]),int(colour[1]),int(colour[2]))
        combi = (num, colour)
        RLEArray.append(combi)

    return(RLEArray)




#Create image from saved array
def recreateImg(RLEArray,img):
    testImg = Image.new(mode="RGB", color=(256, 256, 256), size=(img.width, img.height))

    x = 0
    y = 0

    for q in range(len(RLEArray)):
        for p in range(int(RLEArray[q][0])):
            if x == testImg.width:
                x = 0
                y += 1
            
            testImg.putpixel((x,y),(RLEArray[q][1]))
            x += 1

    testImg.save("RLE.png")


def menu():
    print("Run Length Encoding Image Compression")
    print("To RLE Compress your own image, please place it in the same folder as this program, with the name 'RLE.png'")
    print("To decompress from a .txt file, please place it in the same folder as this program, with the name 'RLE.txt'")
    choice = int(input("Would you like to compress or decompress? (1/2): "))
    match choice:
        case 1:
            genRLEText(genRLE(readImg(openImg())))
        case 2:
            recreateImg(readRLEText(),openImg())

        
while True:
    menu()