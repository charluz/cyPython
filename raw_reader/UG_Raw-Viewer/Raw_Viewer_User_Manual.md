# User's Manual of RAW Viewer #

![Application Main Window](./R001.jpg)

## Operation ##

1. Confiure format of target RAW image
    ![Step1](./O001.jpg)

2. Select and Open the target RAW image
    * Click **OpenRAW** button to select target RAW image.
    * ![Step2-1](./O002.jpg)
    * ![Step2-2](./O003.jpg)
    * ![Step2-3](./O004.jpg)

3. Click **RESET** button to dismiss current image, or **Exit** to exit RAW Viewer.
    * After **RESET**, user can select and open next RAW image as Step 1 ~ 3.
    * ![](./O005.jpg)

## Saving converted images ##
No matter what display options are selected, RAW Viewer will convert RAW image and save the converted images automatically. The saved images include: RawGray, RawRGB, and four bayer colors (R/Gr/Gb/B) and will be collected in a sub-folder (_imageRepo) under the work directory of the RAW image.

![SavedImage](./Saved-Images.jpg)

## Quick Config Buttons ##
There are four buttons at the top right corner which are provided to configure known project RAW format including width, height, bits per pixel, and starting bayer color.

![Select a pre-configured RAW format](./R002.jpg)

The user can customize the preset format of each button via a JSON-formatted configuration file. While Raw View starts, it will look at the configuration file, **raw_format.json**, in the working directory.

![Config JSON](./R003.jpg)

## Customizing your Quick Config buttons ##

![Modify RAW format](./R004.jpg)

![New Format](./R005.jpg)
