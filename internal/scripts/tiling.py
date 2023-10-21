# READ ME
# Before anything, you need to create some folders inside the TFODCourse>Tensorflow>workspace>images directory. You will probably want to
# perform multiple analyses on your images, changing some parameters and checking things. I name each analysis folder by an Instance number to 
# keep them separated. Inside this images directory, create a folder called Instance 1 (or 2, 3, 4, etc.). Inside the instane 1 folder,
# create four folders: 'photos detected', 'photos raw', 'tiles detected', and 'tiles raw'. Put your cropped but otherwise original images in the
# 'photos raw' folder. This code will divide them into 320 x 320 px tiles and put those tiles in the 'tiles raw' folder. The Detection and Counting
# algorithm will look at the tiles in the 'tiles raw' folder and create boxes around the mussels it detects, saving the tiles with boxes in the 
# 'tiles detected' folder. The tiles will be automatically separated into folders named after the coupon they came from. Each coupon folder will
# contain an automatically created spreadsheet that has the mussel counts for each tile in the coupon. There will also be a total counts spreadsheet
# in the 'tiles detected' folder that contains total mussel counts for each coupon. (the 'photos detected' folder was for stitched together whole
# image of the detected tiles, but we are not using that right now.


# Import dependencies
import cv2
import os

# This defines the pathway for this algorith to look for whatever Instance folder you have defined above. My TFODCourse folder is inside
# a folder called OD13 inside my user folder, but you may have placed yours somewhere else when you downloaded the github files and
# activated the virtual environment.
def tile(input_image_list, output_tiles_dir):
    # Returns the image resolution
    # Defines the starting and ending points of the tiling, and how big you want the tiles to be. You can overlap tiles by tuning the interval 
    # and step values. If you don't want the tiles to overlap but want to change the tile size, then change both the interval and the step.

    for pic in input_image_list: # Loop through the photos
        name = str(pic)
        base_name = os.path.basename(name) # Gets rid of the folder path part of the coupon file name.
        name_only = os.path.splitext(base_name)[0] # Gets rid of the .png part of the coupon file name.
        folder_path = os.path.join(output_tiles_dir, name_only) # Creates the full folder path name for the individual coupon name at this step in the loop.
        
        # Scans the image and returns the height and width
        im = cv2.imread(name) 
        dimensions = im.shape

        Ax = 0    # x axis where you want to start tiling; usually 0 
        Bx = dimensions[1]  # x axis where you want to stop tiling. It will stop tiling one interval before this value
        Ix = int(dimensions[1] / 7)   # x axis interval
        Ixs = int(dimensions[1] / 7) # x axis loop step
        Ay = 0    # y axis where you want to start tiling; usually 0 
        By = dimensions[0] # y axis where you want to stop tiling. It will stop tiling one interval before this value
        Iy = int(dimensions[0] / 7)  # y axis interval
        Iys = int(dimensions[0] / 7) # y axis loop step
        if not os.path.exists(folder_path):
            os.mkdir(folder_path) # Creates the folder
        for x in range(Ax,Bx,Ixs):  # sets range for tiling, as defined above, in the x axis
            for y in range(Ay,By,Iys):  # sets range for tiling, as defined above, in the y axis
                tile_coord = '%04d %04d ' % (x,y) # converts the tile coordinates to a string so it can be used in the file name
                tilename = tile_coord + name_only + '.png' # Adds the tile coordinates to the coupon name to create a unique file name for each tile.
                tile = (im[y:y+Iy,x:x+Ix]) # generates the tile
                cv2.imwrite(os.path.join(folder_path, tilename), tile) #saves the tile as an image in the folder_path folder           
    print('Successfully broke images into tiles.')