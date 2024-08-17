import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageDraw
from scipy import ndimage
import numpy as np

# Inject custom CSS
st.markdown(
    """
    <style>
    /* Change background color */
    .stApp {
        background-color: #2E2E2E;
    }
    /* Change text color */
    .css-10trblm {
        color: #FFFFFF;
    }
    /* Change slider color */
    .stSlider .st-bx {
        background-color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Import enhancement ranges from constants.py
from constant import *

st.header("Super Image Enhancement")

st.markdown("@Liston 2024")

st.caption("Layout + stylesheet: Jayden Jacob")
st.markdown(
    """
    Extra Enhencement Contribution: 
    
    - Maddison Ewart, Jack Coup, Maximo Weber, Adriel Book, 
    - Yohan Vattamkandathil Basil, Danny Jonkers, Matthew Abalajen
    """)

## Preset by Maddison Ewart
if 'color' not in st.session_state:
    st.session_state.color = 1.0  # Default color enhancement value
    st.session_state.sharpness = 1.0  # Default sharpness enhancement value
    st.session_state.contrast = 1.0  # Default contrast enhancement value
    st.session_state.brightness = 1.0  # Default brightness enhancement value
    st.session_state.blur = 0.0  # Default blur value (no blur)
    st.session_state.selected_filter = "None"  # Default filter selection (no filter)

# Tab Layout
upload_tab, edit_tab = st.tabs(["Upload", "Edit"])

# Upload Tab
with upload_tab:
    st.write("Upload an image file to begin:")
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            enhanced_img = img.copy()
            st.image(img, caption='Uploaded Image', use_column_width=True)
            st.write("Once the image has been uploaded, open the edit tab to configure your image.")

            ## Preset by Maddison Ewart
            st.session_state.color = preset_filters["None"]["Color"]
            st.session_state.sharpness = preset_filters["None"]["Sharpness"]
            st.session_state.contrast = preset_filters["None"]["Contrast"]
            st.session_state.brightness = preset_filters["None"]["Brightness"]
            st.session_state.blur = preset_filters["None"]["Blur"]
            st.session_state.selected_filter = "None"

        except Exception as e:
            st.error("This file cannot be read properly. Please upload again or upload a different file.")
            st.error(str(e))

# Edit Tab
with edit_tab:
    if uploaded_file is not None:

        ## Preset by Maddison Ewart

        st.sidebar.write("Preset Filters, by Maddison Ewart")

        selected_filter = st.sidebar.selectbox(
            "Choose a preset filter",
            options=list(preset_filters.keys()),  # Populate the dropdown with the keys from the preset_filters dictionary.
            index=list(preset_filters.keys()).index(st.session_state.selected_filter)  # Set default to the last selected filter.
        )

        st.session_state.selected_filter = selected_filter  # Store the selected filter in session state.

        # Get the enhancement values associated with the selected filter from the preset_filters dictionary.
        filter_values = preset_filters[selected_filter]

        # Apply the additional filter (e.g., sepia, black & white) if selected.
        if filter_values["Filter"]:
            if filter_values["Filter"] == 'sepia':
                sepia_filter = ImageOps.colorize(enhanced_img.convert("L"), '#704214', '#C0C0C0')  # Apply sepia tone.
                enhanced_img = sepia_filter
            elif filter_values["Filter"] == 'bw':
                enhanced_img = enhanced_img.convert("L").convert("RGB")  # Convert to black & white.
            elif filter_values["Filter"] == 'cool_blue':
                enhanced_img = ImageOps.colorize(enhanced_img.convert("L"), '#0000FF', '#FFFFFF')  # Apply cool blue tone.
            elif filter_values["Filter"] == 'warm_sepia':
                enhanced_img = ImageOps.colorize(enhanced_img.convert("L"), '#704214', '#D0B0A1') 


        # Sidebar sliders dynamically created using constants from constant.py
        enhancement_factors = []

        for category in enhancement_range.keys():
            min_val, max_val, step = enhancement_range[category]
            factor = st.sidebar.slider(
                category, 
                min_value=min_val, 
                max_value=max_val, 
                step=step, 
                value=filter_values[category]
            )
            enhancement_factors.append(factor)

        # Apply enhancements
        enhanced_img = img
        for i, category in enumerate(enhancement_range.keys()):
            enhancer = getattr(ImageEnhance, category)(enhanced_img)
            enhanced_img = enhancer.enhance(enhancement_factors[i])

        # Gaussian Blur slider
        sigma = st.sidebar.slider('Gaussian Blur Sigma by Jayden Jacob', min_value=0.0, max_value=10.0, step=0.1, value=0.0)
        if sigma > 0:
            np_img = np.array(enhanced_img)
            enhanced_img = Image.fromarray(ndimage.gaussian_filter(np_img, sigma=sigma))
        
        # Add checkboxes for additional options, By Jack Coup

        st.caption("Color Invertion, by Jack Coup")
        invert_colors = st.checkbox("Invert Colors")  # Checkbox to toggle color inversion
        black_and_white = st.checkbox("Convert to Black and White")  # Checkbox to toggle black and white

        if invert_colors:
            enhanced_img = ImageOps.invert(enhanced_img.convert("RGB"))        
        if black_and_white:
            enhanced_img = enhanced_img.convert("L")  # Change to black and white
        
        # Masking from Maximo
        st.sidebar.write("Apply Shape Mask, by Maximo Weber")
        mask_option = st.sidebar.selectbox("Choose mask type", ["None", "Circular", "Rectangular"])

        if mask_option == "Circular":
            mask = Image.new("L", enhanced_img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, enhanced_img.size[0], enhanced_img.size[1]), fill=255)
            enhanced_img.putalpha(mask)
        elif mask_option == "Rectangular":
            mask = Image.new("L", enhanced_img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rectangle((0, 0, enhanced_img.size[0], enhanced_img.size[1]), fill=255)
            enhanced_img.putalpha(mask)


        #Crop image section by Danny Jonkers

        st.caption("Crop image, by Danny Jonkers & Matthew Abalajen")

        with st.expander("Crop image"):
        
            x = st.slider("X-coordinate", 0, img.width, 0) # Slider to select the X-coordinate of the mask
            y = st.slider("Y-coordinate", 0, img.height, 0) # Slider to select the Y-coordinate of the mask
            width = st.slider("Width", 1, img.width - x, 600) # Slider to select the width of the mask
            height = st.slider("Height", 1, img.height - y, 839) # Slider to select the height of the mask
        
            ### Create a new grayscale mask image with same size as the original image
            mask = Image.new("L", img.size, 0)  # L mode is for grayscale images
            draw = ImageDraw.Draw(mask) # Prepares to draw on the masked image

            # Draw a white rectangle on the mask
            draw.rectangle([x, y, x + width, y + height], fill=255)

            # Control mask opacity
            mask_opacity = st.slider("Opacity", 0, 100, 100) # Slider to adjust the opacity of the mask from 0 to 100 (auto set to 100)
            mask = ImageEnhance.Brightness(mask).enhance(mask_opacity / 100) # Adjusts brightness of the mask to match the selected opacity

            # Apply the mask to the original image by blending it
            enhanced_img = Image.composite(enhanced_img, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask)
            # crop_box = (left, top, right, bottom)
            # if left < right and top < bottom:
            #     enhanced_img = enhanced_img.crop(crop_box)

        # Rescaling, by Adriel Book
        st.sidebar.write("Rescaling/Resize, by Adriel Book")

        scale_factor = st.sidebar.slider(
            "Scale factor",  # Label for the slider
            value=1.0,  # Default value for scaling (no scaling)
            min_value=0.1,  # Minimum value for scaling (10% of the original size)
            max_value=2.0,  # Maximum value for scaling (200% of the original size)
            step=0.1,  # Step size for scaling
            key="scale_factor"  # Unique key for the slider
        )

        # Calculate the new size based on the scaling factor
        if scale_factor:
            new_size = (int(enhanced_img.width * scale_factor), int(enhanced_img.height * scale_factor))
            c = enhanced_img.resize(new_size, Image.LANCZOS)  # Resize the image with the new size

        # Gray-scale Masking by Yohan Vattamkandathil Basil
        st.caption("Gray scale masking, by Yohan Vattamkandathil Basil ")
        with st.expander("Gay Scale Masking"): 
            mask_threshold = st.slider("Mask Intensity", 0, 255, 0, step=1)

            if mask_threshold:
                gray_img = img.convert("L")
                img_for_mask = np.array(gray_img)
                mask = img_for_mask < mask_threshold
                img_for_mask[mask] = 255  
                enhanced_img = Image.fromarray(img_for_mask)#Converting the masked array back to an image
     
        ## 

        st.divider()
        # Display the original and enhanced images side by side
        col1, col2 = st.columns(2)

        with col1:
            st.image(img, caption='Original Image', use_column_width=True)
        with col2:
            st.image(enhanced_img, caption='Enhanced Image', use_column_width=True)

        # Provide a download button for the enhanced image
        st.write("Once you are done editing, press the download button below to download the image.")
        enhanced_img.save("enhanced_image.png")
        with open("enhanced_image.png", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name="enhanced_image.png",
                mime="image/png",
            )
    else:
        st.write("Please upload an image file in the Upload tab to use the edit features.")
