print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from utils import *
import sudokuSolver
import cv2
import numpy as np


########################################################################
#pathImage = "Resources/1.jpg"
heightImg = 450
widthImg = 450
model = intializePredectionModel()  # LOAD THE CNN MODEL
########################################################################


def fullsudoku(image):
    #### 1. PREPARE THE IMAGE
    img = cv2.imread(image)
    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgThreshold = preProcess(img)

    # #### 2. FIND ALL CONTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    #imgBigContour1 = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    #imgBigContour2 = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS


    #### 3. FIND THE BIGGEST CONTOUR AND USE IT AS SUDOKU
    biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
    print(biggest)
    if biggest.size != 0:
        biggest = reorder(biggest)
        print(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits = imgBlank.copy()
        imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

        #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
        imgSolvedDigits = imgBlank.copy()
        boxes = splitBoxes(imgWarpColored)
        print(len(boxes))
        # cv2.imshow("Sample",boxes[65])
        numbers = getPredection(boxes, model)
        print(numbers)
        imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
        numbers = np.asarray(numbers)
        posArray = np.where(numbers > 0, 0, 1)
        print(posArray)


        #### 5. FIND SOLUTION OF THE BOARD
        board = np.array_split(numbers,9)
        print(board)
        try:
            sudokuSolver.solve(board)
        except:
            pass
        print(board)
        flatList = []
        for sublist in board:
            for item in sublist:
                flatList.append(item)
        solvedNumbers =flatList*posArray
        imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)

        # #### 6. OVERLAY SOLUTION
        pts2 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts1 =  np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
        imgInvWarpColored = img.copy()
        imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
        inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
        imgDetectedDigits = drawGrid(imgDetectedDigits)
        imgSolvedDigits = drawGrid(imgSolvedDigits)

        imageArray = ([img,imgThreshold,imgContours, imgBigContour],
                      [imgDetectedDigits, imgSolvedDigits,imgInvWarpColored,inv_perspective])
        stackedImage = stackImages(imageArray, 1)
        #cv2.imshow('Stacked Images', stackedImage)
    else:
        print("No Sudoku Found")
    return stackedImage


def horizontal_sudoku(image):
    img = cv2.imread(image)
    img = cv2.resize(img, (widthImg, heightImg))
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    imgThreshold = preProcess(img)

    imgContours = img.copy()
    imgBigContour1 = img.copy()

    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

    biggest1, maxArea1 = VerticalContour(contours)
    print(biggest1)

    if biggest1.size != 0:
        biggest1 = reorder(biggest1)
        cv2.drawContours(imgBigContour1, biggest1, -1, (0, 0, 255), 25)
        pts1 = np.float32(biggest1)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored1 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits1 = imgBlank.copy()

        imgSolvedDigits1 = imgBlank.copy()
        boxes1 = splitBoxes1(imgWarpColored1)
        print(len(boxes1))

        numbers1 = getPredection(boxes1, model)
        print(numbers1)
        imgDetectedDigits1 = displayNumbers1(imgDetectedDigits1, numbers1, color=(255, 0, 255))
        numbers1 = np.asarray(numbers1)
        posArray1 = np.where(numbers1 > 0, 0, 1)
        print(posArray1)

        board1 = np.array_split(numbers1, 9)
        print(board1)
        try:
            sudokuSolver.solve(board1)
        except:
            pass
        print(board1)
        flatList1 = []
        for sublist in board1:
            for item in sublist:
                flatList1.append(item)
        solvedNumbers1 = flatList1 * posArray1
        imgSolvedDigits1 = displayNumbers1(imgSolvedDigits1, solvedNumbers1)

        pts2 = np.float32(biggest1)
        pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgInvWarpColored1 = img.copy()
        imgInvWarpColored1 = cv2.warpPerspective(imgSolvedDigits1, matrix, (widthImg, heightImg))
        inv_perspective1 = cv2.addWeighted(imgInvWarpColored1, 1, img, 0.5, 1)
        imgDetectedDigits1 = drawGrid1(imgDetectedDigits1)
        imgSolvedDigits1 = drawGrid1(imgSolvedDigits1)

        imageArray = ([img, imgThreshold, imgContours, imgBigContour1],
                      [imgDetectedDigits1, imgSolvedDigits1, imgInvWarpColored1, inv_perspective1])
        stackedImage = stackImages(imageArray, 1)

    else:
        print("No Sudoku Found")
    return stackedImage








def vertical_sudoku(image):
    img = cv2.imread(image)
    img = cv2.resize(img, (widthImg, heightImg))
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    imgThreshold = preProcess(img)

    imgContours = img.copy()
    imgBigContour2 = img.copy()

    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3)

    biggest2, maxArea2 = HorizontalContour(contours)
    print(biggest2)

    if biggest2.size != 0:
        biggest2 = reorder(biggest2)
        cv2.drawContours(imgBigContour2, biggest2, -1, (0, 0, 255), 25)
        pts1 = np.float32(biggest2)
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored2 = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgDetectedDigits2 = imgBlank.copy()

        imgSolvedDigits2 = imgBlank.copy()
        boxes2 = splitBoxes2(imgWarpColored2)
        print(len(boxes2))

        numbers2 = getPredection(boxes2, model)
        print(numbers2)
        imgDetectedDigits2 = displayNumbers2(imgDetectedDigits2, numbers2, color=(255, 0, 255))
        numbers2 = np.asarray(numbers2)
        posArray2 = np.where(numbers2 > 0, 0, 1)
        print(posArray2)

        board2 = np.array_split(numbers2, 9)
        print(board2)
        try:
            sudokuSolver.solve(board2)
        except:
            pass
        print(board2)
        flatList2 = []
        for sublist in board2:
            for item in sublist:
                flatList2.append(item)
        solvedNumbers2 = flatList2 * posArray2
        imgSolvedDigits2 = displayNumbers2(imgSolvedDigits2, solvedNumbers2)

        pts2 = np.float32(biggest2)
        pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgInvWarpColored2 = img.copy()
        imgInvWarpColored2 = cv2.warpPerspective(imgSolvedDigits2, matrix, (widthImg, heightImg))
        inv_perspective2 = cv2.addWeighted(imgInvWarpColored2, 1, img, 0.5, 1)
        imgDetectedDigits2 = drawGrid2(imgDetectedDigits2)
        imgSolvedDigits2 = drawGrid2(imgSolvedDigits2)

        imageArray = ([img, imgThreshold, imgContours, imgBigContour2],
                      [imgDetectedDigits2, imgSolvedDigits2, imgInvWarpColored2, inv_perspective2])
        stackedImage = stackImages(imageArray, 1)
    else:
        print("No Sudoku Found")
    return stackedImage
"""
cv2.waitKey(0)
"""
