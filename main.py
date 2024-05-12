import cv2
import sys
from sudokuMain import fullsudoku as full_sudoku
from sudokuMain import horizontal_sudoku as horizontal_sudoku
from sudokuMain import vertical_sudoku as vertical_sudoku
#pathImage = "Resources/1.jpg"
# Input handling
if len(sys.argv) != 2:
	print("Please provide the path to the image")
	exit()
image_path = sys.argv[1]

# Read Image using OpenCV and initialize variables
image = cv2.imread(image_path)
image = cv2.resize(image,(450,450))
new_image = image.copy()
window_title = "Image"

# Get User Input for editing image
user_choice = input("What would you like the sudoku solver to solve? \n1. Total \n2. Vertical \n3.Horizontal  \nEnter the number from choices: ")

if user_choice == '1':
    image_path = input("Enter the path to the image: ")  # Ask for the image path
    new_image = full_sudoku(image_path)  # Pass the image path to full_sudoku function
    cv2.imshow("Sudoku Solver - Total", new_image)  # Show the result with a window title
    cv2.waitKey(0)  # Wait for user input to close the window
    cv2.destroyAllWindows()  # Close all OpenCV windows

elif user_choice == '2':
    image_path = input("Enter the path to the image: ")  # Ask for the image path
    new_image = horizontal_sudoku(image_path)  # Pass the image path to full_sudoku function
    cv2.imshow("Sudoku Solver - Total", new_image)  # Show the result with a window title
    cv2.waitKey(0)  # Wait for user input to close the window
    cv2.destroyAllWindows()  # Close all OpenCV windows

elif user_choice == '3':
    image_path = input("Enter the path to the image: ")  # Ask for the image path
    new_image = vertical_sudoku(image_path)  # Pass the image path to full_sudoku function
    cv2.imshow("Sudoku Solver - Total", new_image)  # Show the result with a window title
    cv2.waitKey(0)  # Wait for user input to close the window
    cv2.destroyAllWindows()  # Close all OpenCV windows
else:
    print("Invalid option selected. Aborting...")
    exit()
