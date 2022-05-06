from markdown import markdown
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd


#Display header on page
st.markdown("<h1 style= 'text-align:center ;color:red;'> Streamlit Drawable Canvas</h1>", unsafe_allow_html=True)

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox("Drawing tool:", 
                ("point", "freedraw", "line", "rect", "circle", "transform")
) 
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", min_value=1, max_value=100, value=3) 

stroke_width = st.sidebar.slider(" Select Stroke width: ", min_value=1, max_value=100, step=1, value=5)
stroke_color = st.sidebar.color_picker("Select stroke color: ")
image = st.sidebar.file_uploader("Upload image:", type=["png", "jpg"])
color = st.sidebar.color_picker("Select background color: ")
realtime_update = st.sidebar.checkbox("Update in realtime", True)


def draw_image(image, stroke_width, stroke_color, drawing_mode):
    """
    Draw image on canvas and other geometrical shapes such as point, line, circle, rectangle.
    Parametrs
    ----------------------------------------
    color: str
     Color in hex format
    image:
     Uploded image file
    stroke_width: int
     Brush stroke width to draw on canvas
    stroke_color: str
     Brush stroke color in hex
    drawing_mode: str
     Various drawing modes

    Returns
    ------------------------
    canvas_result:
     Canvas output in json and image format
    """
    if image is not None:
        img= Image.open(image)

        # Canvas to draw line for pixel length measurement
        width, height= img.size
        canvas_result = st_canvas(fill_color="rgba(0, 0, 0, 0.1)",
                                    background_image= img,
                                        height= height,
                                        width= width,
                                        display_toolbar= True,
                                        stroke_width=stroke_width,
                                        stroke_color=stroke_color,
                                        drawing_mode=drawing_mode,
                                        update_streamlit=realtime_update,
                                        key= "Canvas"
                                        )
        return canvas_result                                    

#####################################################################################################
def draw_canvas(color, stroke_width, stroke_color, drawing_mode):
    """
    Draw on canvas.
    Parametrs
    ----------------------------------------
    color: str
     Color in hex format
    stroke_width: int
     Brush stroke width to draw on canvas
    stroke_color: str
     Brush stroke color in hex
    drawing_mode: str
     Various drawing modes

    Returns
    ------------------------
    canvas_result:
     Canvas output in json and image format
    """

    canvas_result = st_canvas(fill_color="rgba(255, 255, 255, 0.1)",
                                    background_color=color,
                                        stroke_width=stroke_width,
                                        stroke_color=stroke_color,
                                        drawing_mode=drawing_mode,
                                        height=500,
                                        width=500,
                                        display_toolbar= True,
                                        update_streamlit=realtime_update,
                                        key= "Canvas"
                                        )
    return canvas_result 
###################################################################################################
def result(canvas_result):
    """
    Display result of canvas in image and dataframe.
    Parametrs
    ---------------------------
    canvas_result:
     Canvas output in json and image format
    """
    if canvas_result is not None:
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data)
        if canvas_result.json_data is not None:
            objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
            for col in objects.select_dtypes(include=['object']).columns:
                objects[col] = objects[col].astype("str")
            st.dataframe(objects) 

#######################################################################################################        
option= st.selectbox("Choose the drawing option:",
                    ('None','Draw on image','Draw on canvas')
                    )
if option=='None':
    st.text('Choose correct options')
elif option=='Draw on image':
    # Display heading on page
    st.markdown("<h2 style= 'text-align:center ;color:red;'> Draw on Image</h2>", unsafe_allow_html=True)
    canvas_result= draw_image(image, stroke_width, stroke_color, drawing_mode)
    result(canvas_result)
elif option=='Draw on canvas':
    # Display heading on page
    st.markdown("<h2 style= 'text-align:center ;color:red;'> Draw on Canvas</h2>", unsafe_allow_html=True) 
    canvas_result= draw_canvas(color, stroke_width, stroke_color, drawing_mode)
    result(canvas_result)






        
   
    



                                   