# WebCAT utilities

This repository provides a Pythonic way to interface with the NOAA National Ocean Service Web Camera Applications 
Testbed (WebCAT). The real-time data is hosted on the [SECOORA site](https://secoora.org) 
(The Southeast Coastal Ocean Observing Regional Association), on the dedicated [WebCAT page](https://secoora.org/webcat/).
Historic data can also be accessed by retrieving files using specific HTTP requests (using a pattern described on the 
[WebCAT page](https://secoora.org/webcat/). 

Details about WebCAT can also be seen in this Open Access paper:

>Dusek, G., Hernandez, D., Willis, M., Brown, J. A., Long, J. W., Porter, D. E., & Vance, T. C. (2019). WebCAT: Piloting the development of a web camera coastal observing network for diverse applications. Frontiers in Marine Science, 6, 353, 25 June 2019 | https://doi.org/10.3389/fmars.2019.00353

`webcat_utils.py` allows users to:
- generate urls for video segments by specifying the camera station, year, month, day, time. 
- requests retrieve historic data
- extract specific video frames as jpegs. 
- plot individual video frames
- plot averages of frames

Examples can be seen in `webcat_utils_demo.ipynb`

