import cv2
import pandas as pd


#uploading image
img_path = r'colorfulstreet.jpg'
img = cv2.imread(img_path)
img= cv2.resize(img,(800,600))

# declaring variables
clicked = False
r =g = b = 0
x_position = y_position = 0


# Reading csv file for colors
index = ["color", "color_name", "hex", "R", "G", "B"]
csv=pd.read_csv('colorsfile.csv',names=index,header=None)


# function to get the most matching color
def get_color_name(R, G, B):
    min=10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= min:
            min= d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
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