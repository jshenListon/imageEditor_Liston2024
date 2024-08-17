enhancement_range = {
  # "enhancement_type": [min, max, step_size]

    "Color": [0.0, 10.0, 0.1], 
    "Sharpness": [0.0, 10.0, 0.1], 
    "Contrast": [0.5, 10.0, 0.05], 
    "Brightness": [0.5, 10.0, 0.05]
}


## Preset filters by Maddison Ewart
preset_filters = {
    "None": {"Color": 1.0, "Sharpness": 1.0, "Contrast": 1.0, "Brightness": 1.0, "Blur": 0.0, "Filter": None},
    "Vintage": {"Color": 0.8, "Sharpness": 1.2, "Contrast": 1.1, "Brightness": 1.0, "Blur": 1.0, "Filter": None},
    "Bright": {"Color": 1.2, "Sharpness": 1.0, "Contrast": 1.2, "Brightness": 1.2, "Blur": 0.0, "Filter": None},
    "Muted": {"Color": 0.6, "Sharpness": 1.0, "Contrast": 0.8, "Brightness": 1.0, "Blur": 0.0, "Filter": None},
    "High Contrast": {"Color": 1.0, "Sharpness": 1.0, "Contrast": 1.5, "Brightness": 1.0, "Blur": 0.0, "Filter": None},
    "Sepia": {"Color": 0.8, "Sharpness": 1.0, "Contrast": 0.9, "Brightness": 1.1, "Blur": 0.0, "Filter": 'sepia'},
    "Black & White": {"Color": 0.0, "Sharpness": 1.0, "Contrast": 1.0, "Brightness": 1.0, "Blur": 0.0, "Filter": 'bw'},
    "Retro": {"Color": 0.5, "Sharpness": 1.2, "Contrast": 1.3, "Brightness": 1.0, "Blur": 0.5, "Filter": None},
    "Cool Blue": {"Color": 1.0, "Sharpness": 1.0, "Contrast": 1.0, "Brightness": 1.0, "Blur": 0.0, "Filter": 'cool_blue'},
    "Warm Sepia": {"Color": 0.7, "Sharpness": 1.0, "Contrast": 1.1, "Brightness": 1.1, "Blur": 0.0, "Filter": 'warm_sepia'},
}
