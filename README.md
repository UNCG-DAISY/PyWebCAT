# WebCAT-Utilities

![](https://img.shields.io/badge/-UNCG-blue)
![](https://img.shields.io/badge/-DAISY-yellow)

Short description.

## Usage

### Module

The webcat_utils module can be imported to access functionality on an as-needed basis. See the [demo Jupyter notebook](notebooks/webcat_utils_demo.ipynb) for a worked example.

```{python}
from webcat_utils import WebCAT
wc = WebCAT()
wc.generate_url("fake", 2019, 11, 13, 1000)  # create the video url

# class attributes
wc.url     # the created url
wc.name    # unique name for the video object
wc.width   # frame width in pixels
wc.height  # frame height in pixels
wc.frames  # total frames in video
wc.fps     # frames per second

# class methods
wc.download_url()        # download the video at the url
wc.save_frames()         # save video frames as .jpg
wc.plot_frames()         # plot select video frames
wc.plot_average_frame()  # plot time-averaged frame
```

### CLI

A key workflow for utilising WebCAT videos is to split videos into select frames for further analysis. While this functionality is supported by the `WebCAT.save_frames()` method, it is further exposed as a CLI.

```{sh}
$ python webcat_utils.py
usage: webcat_utils.py [-h] -dir DIRECTORY -s STATION [STATION ...] -y YEAR
                       [YEAR ...] -m MONTH [MONTH ...] -d DAY [DAY ...] -t
                       TIME [TIME ...] [-i INTERVAL] [-n] [-v]

CLI for saving frames of webCAT video(s).

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        Interval in seconds between video frames to save
                        (default: 10).
  -n, --no_meta         Don't save .csv file of metadata of saved video
                        frames.
  -v, --verbose         Print program status.

required arguments:
  -dir DIRECTORY, --directory DIRECTORY
                        Absolute path of directory to save frames in.
  -s STATION [STATION ...], --station STATION [STATION ...]
                        The station name, e.g., buxtoncoastalcam.
  -y YEAR [YEAR ...], --year YEAR [YEAR ...]
                        The video year(s), e.g., 2019 2020.
  -m MONTH [MONTH ...], --month MONTH [MONTH ...]
                        The video month(s), e.g., 9 10 11.
  -d DAY [DAY ...], --day DAY [DAY ...]
                        The video day(s) e.g., 1 11 21.
  -t TIME [TIME ...], --time TIME [TIME ...]
                        The video time(s), e.g., 1000 1330 1510.
```

The CLI facilitates efficiently looping over input arguments to locate one or more WebCAT videos and split them into the desired number of frames which are saved locally. Here's an example looping over several videos from the Buxton coastal camera on 13th Nov 2019 at different times (a 10 second interval is specified for saving the frames and verbosity is turned on):

```{sh}
$ python webcat_utils.py -dir /Users/tbeuzen/Downloads -s buxtoncoastalcam -y 2019 -m 11 -d 13 -t 1000 1210 1530 -i 10 -v
Saving frames of buxtoncoastalcam_2019_11_13_1000...
100%|███████████████████████████████████████████████████████████████████████████████| 62/62 [00:14<00:00,  4.22it/s]
Saving frames of buxtoncoastalcam_2019_11_13_1210...
100%|███████████████████████████████████████████████████████████████████████████████| 62/62 [00:13<00:00,  4.51it/s]
Saving frames of buxtoncoastalcam_2019_11_13_1530...
100%|███████████████████████████████████████████████████████████████████████████████| 62/62 [00:14<00:00,  4.38it/s]
```

The resultant directory structure looks like:

```{sh}
Users/tbeuzen/Downloads
                └── buxtoncoastalcam
                    ├── buxtoncoastalcam_2019_11_13_1000
                    │   ├── buxtoncoastalcam_2019_11_13_1000.csv
                    │   └── jpg
                    │       ├── frame_0.jpg
                    │       ├── frame_280.jpg
                    │       ├── ...
                    ├── buxtoncoastalcam_2019_11_13_1210
                    │   ├── ...
                    └── buxtoncoastalcam_2019_11_13_1530
                        ├── ...
```

The outputted .csv file contains metadata for the saved frames:

| url        | name           | frame  | path|
| ------------- |-------------| -----|---|
|http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4|buxtoncoastalcam_2019_11_13_1000|0|/Users/tbeuzen/Downloads/buxtoncoastalcam/buxtoncoastalcam_2019_11_13_1000/jpg/frame_0.jpg|
|http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4|buxtoncoastalcam_2019_11_13_1000|280|/Users/tbeuzen/Downloads/buxtoncoastalcam/buxtoncoastalcam_2019_11_13_1000/jpg/frame_280.jpg|
|...|...|...|...|

## Contributing

Contributions are welcome and greatly appreciated! If you're interested in contributing to this project, take a look at the [contributor guide](docs/CONTRIBUTING.md).

## Contributors

All contributions are welcomed and recognized! You can see a list of current contributors in the [contributors tab](https://github.com/UNCG-DAISY/WebCAT-Utilities/graphs/contributors).

## Acknowledgements
