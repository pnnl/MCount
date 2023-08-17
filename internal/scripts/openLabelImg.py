

def labelImageOpen():
        #!/usr/bin/env python
    # coding: utf-8

    # In[8]:


    # Algorithm 2: Image Labeling and Algorigthm 3: Training and Detection are closely adapted from a tutorial and accompanying code, found here:
    # Tutorial: https://www.youtube.com/watch?v=yqkISICHH-U
    # Code: https://github.com/nicknochnack/TFODCourse

    # The purpose of this code is to perform some setup and installation and then start up the LabelImg user interface. 
    # LabelImg allows the user to mark the locations of objects of interest for training purposes. It will generate an xml file ...
    # ... that contains the coordinates of every box that you mark in LabelImg. Just run each cell, and at the end, ...
    # ... labelImg will start up after you run the last cell. The last cell will continue to appear running as long as LabelImg is running.
    # Steps 2 and 3 are not strictly necessary for the protocol we are using, but they are necessary for this code to work, so you need to ...
    # ... run those cells. You shouldn't need to add or remove or change anything (including the label names... this was for generating ...
    # ... an auto-collecting interface for each label type. We're not doing that, so you don't need to update the label name. Just label everything...
    # ... consistently and correctly in labelImg.


    # # 1. Import Dependencies

    # In[6]:


    # Import opencv
    import cv2 

    # Import uuid
    import uuid

    # Import Operating System
    import os

    # Import time
    import time

    from IPython import get_ipython     
    
    LABELIMG_PATH = os.path.join('tensorflow', 'labelimg')


    # In[13]:


    LABELIMG_PATH


    # In[14]:


    if not os.path.exists(LABELIMG_PATH):
        get_ipython().system('mkdir {LABELIMG_PATH}')
        get_ipython().system('git clone https://github.com/tzutalin/labelImg {LABELIMG_PATH}')


    # In[ ]:


    if os.name == 'posix':
        get_ipython().system('make qt5py3')
    if os.name =='nt':
        get_ipython().system('cd {LABELIMG_PATH} && pyrcc5 -o libs/resources.py resources.qrc')


    # In[15]:


    get_ipython().system('cd {LABELIMG_PATH} && python labelImg.py')



