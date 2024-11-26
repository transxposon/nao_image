# nao_image
image capturing from nao's top camera

This Python script allows you to capture images from the Nao robot's TOP camera and save them locally with sequential file naming. The images are saved in a folder named `nao_photos` within the current working directory. The script is compatible with Python 2.7.

## Features
- Captures images using the Nao robot's camera.
- Images are saved in the `nao_photos` folder.
- Sequential file naming (e.g., `image00001.png`, `image00002.png`, etc.) to prevent overwriting.
- Supports customizable resolution for captured images.

## Requirements
- **Python 2.7** (required for compatibility with the Naoqi SDK)
- [Naoqi SDK](https://developer.softbankrobotics.com/) (configured and installed)
- Libraries:
  - `numpy`
  - `Pillow` (PIL)
  - `naoqi`
  - `os`
  - `sys`

- NAOqi Python SDK (download and include in your project)
- A NAO robot connected to your network (for the second program)

### **Installing Dependencies**

```bash
pip install os sys numpy pillow
