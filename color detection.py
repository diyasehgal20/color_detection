import cv2
import pandas as pd


#uploading image
img_path = r'colorfulstreet.jpg'
img = cv2.imread(img_path) #reads the image file
img= cv2.resize(img,(800,600)) #resizes image to the given format

# declaring variables
clicked = False #whether the user has clicked on a particular color
r =g = b = 0 #initialising rgb values as 0
x_position = y_position = 0 #mouse coordinate used to determine where on the screen the event of click took place.


# Reading csv file for colors (more than 800)
index = ["color", "color_name", "hex", "R", "G", "B"]
csv=pd.read_csv('colorsfile.csv',names=index,header=None) #reading csv files of color-names


# We use the function get_color_name(R, G, B) that takes three arguments
#representing the red(R), green(G), and blue(B) color components of a pixel. 
#The function is designed to determine the closest color name from a predefined 
#list of colors  from csv file based on the RGB values of the input pixel.
def get_color_name(R, G, B):
     #This value is used to keep track 
    #of the minimum difference between the input RGB values and the RGB values of the predefined colors.
    min=10000
    #This line starts a for loop that iterates through the rows of a predefined csv. 
    #i will take on values from 0 to one less than the number of rows in the dataset.
    for i in range(len(csv)):
        #d is the color distance between RGB values
        #csv.loc[i, "R"], csv.loc[i, "G"], and csv.loc[i, "B"] access the red, green, and blue components of the color
        #abs() is used to calculate the absolute difference (positive)
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= min: #This line checks if d is less than or equal to min(defined above).
            #If it is, it means that the current color is a closer match to the input RGB values.
            min= d #if above statement is true min is updated to d 
            cname = csv.loc[i, "color_name"] 
            #his line stores the name of the color from the dataset (found at row i) as cname.
            #This color name corresponds to the color that is currently the closest match to the input RGB values.
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param): #callback functions for mouse events,different flags may be set to provide additional context about the event.
    #EVENT_LBUTTONDOWN is for left button single click on image
    if event == cv2.EVENT_LBUTTONDOWN:
        global b, g, r, x_position, y_position, clicked
        clicked = True
        x_position = x
        y_position = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


while True:
    cv2.imshow("image", img)
    if clicked:


        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r),-1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start point,font(0to7),fontScale,color,thickness,linetype )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours text displayed in black color
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False


    # Break the loop with 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break


cv2.destroyAllWindows()
