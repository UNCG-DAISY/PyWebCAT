import os
import cv2
import argparse
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from tqdm import tqdm

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelweight": "bold",
        "figure.figsize": (8, 6),
        "axes.grid": False,
    }
)


class WebCAT:
    """Utility class for viewing local or remote webcat videos.

    Attributes
    ----------
    url : 
        url to the .mp4 file.
    name : 
        Unique name based on url.
    video : cv2.VideoCapture
        The cv2.VideoCapture object of the video file at url.
    frames: int
        Total number of frames in the video.
    fps : int
        Frames per second in the video.
    width : int
        Width of video frames in pixels.
    height : int
        Height of video frames in pixels.

    Methods
    -------
    download_url(self, fout=None, verbose=1)
        Download the video from the url.

    Examples
    --------
    >>> from webcat_utils import VidRetriever
    >>> url = "http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4"
    >>> vr = VidRetriever(url)
    >>> vr.download_url()
    ...
    Saving to buxtoncoastalcam.2019-11-13_1000.mp4:  0%|      | 44.1M/125M [00:08<00:16, 5.18MB/s]
    """

    def __init__(self):
        self.url = None
        self.name = None
        self.video = None

    @property
    def width(self):
        return int(self.video.get(3))

    @property
    def height(self):
        return int(self.video.get(4))

    @property
    def frames(self):
        return int(self.video.get(7))

    @property
    def fps(self):
        return int(self.video.get(cv2.CAP_PROP_FPS))

    def generate_url(self, station: str, year: int, month: int, day: int, time: int):
        """Generate WebCAT URLs and expressive name for files from user inputs.

        Parameters
        ----------
        station : str
            Station name, e.g., "buxtoncoastalcam".
        year : int
            Year of video, e.g., 2020.
        month: int
            Month (numerical) of video, e.g., 11.
        day: int
            Day of video, e.g., 17.
        time: int
            Time (24 hr) of video rounded to nearest 10 minutes, e.g., 0500 (5:00 am), 1300 (1:00 pm), 1330 (1:30pm).

        """
        url = f"http://webcat-video.axds.co/{station}/raw/{year}/{year}_{month}/{year}_{month}_{day}/{station}.{year}-{month}-{day}_{time}.mp4"
        vid = cv2.VideoCapture(url)
        if int(vid.get(7)) == 0:  # check if there are any frames
            raise ValueError(f"{url} is not a valid url.")
        else:
            self.url = url
            self.video = vid
            self.name = f"{station}_{year}_{month}_{day}_{time}"

    def download_url(self, fout: str = None, verbose: bool = True):
        """Download the video from the instance url.

        Parameters
        ----------
        fout : str
            The file path to save the downloaded file to, e.g., ~/Downloads/download.mp4, by default None
        verbose : {True, False}, optional
            Display download progress bar, by default True
        """
        fout = self.name + ".mp4" if fout == None else fout
        if verbose:
            with TqdmUpTo(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                miniters=1,
                desc=f"Saving to {fout}",
            ) as t:  # all optional kwargs
                urllib.request.urlretrieve(self.url, fout, reporthook=t.update_to)
        else:
            urllib.request.urlretrieve(self.url, fout)

    def save_frames(
        self, delta_t: int = 10, fout_path: str = "", save_csv=True, verbose=False
    ):
        """Download the video from the instance url.

        Parameters
        ----------
        delta_t : int, optional
            A frame will be saved every delta_t seconds, by default 10.
        fout : str, optional
            Path to save frames and csv to, e.g., "~/Downloads/".
        """
        assert delta_t < int(
            self.frames / self.fps
        ), f"delta_t should be less than {int(self.frames / self.fps)}"
        step = delta_t * self.fps
        step_range = range(0, (self.frames + 1), step)
        loop = tqdm(step_range) if verbose else step_range
        tmp_dir = os.path.join(fout_path, "jpg")  # save images in a "jpg" folder
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)  # mkdir if not exist
        for i in loop:
            self.video.set(1, i)
            _, frame_arr = self.video.read()
            cv2.imwrite(os.path.join(tmp_dir, f"frame_{i}.jpg"), frame_arr)
        if save_csv:
            (
                pd.DataFrame(
                    {
                        "url": self.url,
                        "name": self.name,
                        "frame": list(step_range),
                        "path": [
                            os.path.join(tmp_dir, f"frame_{_}.jpg") for _ in step_range
                        ],
                    }
                ).to_csv(os.path.join(fout_path, f"{self.name}.csv"))
            )

    def plot_frames(self, frames: list = [0]):
        """Plot frames from the video, zero-based indexing.

        Parameters
        ----------
        frames : list, optional
            List of the frames to display in a grid plot, by default [0].
        
        Examples
        --------
        >>> from webcat_utils import WebCAT
        >>> wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
        >>> wc.plot_frames()
        ...
        <matplotlib.subplots>
        """
        assert all(
            (_ >= 0) & (_ < self.frames) for _ in frames
        ), f"frames should be between 0 and {self.frames-1}."
        rows = 1 + (len(frames) - 1) // 3
        cols = len(frames) if len(frames) < 3 else 3
        fig, ax = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3), squeeze=False)
        for i, frame in enumerate(frames):
            plt.sca(ax[0, i]) if rows == 1 else plt.sca(ax[i // 3, i % 3])
            self.video.set(1, frame)
            _, frame_arr = self.video.read()
            plt.imshow(
                cv2.cvtColor(frame_arr, cv2.COLOR_BGR2RGB)
            )  # plot the image on current axis
            plt.title(f"Frame {frame + 1} of {self.frames}")
        if len(frames) < rows * cols:  # clear any unsued axes (this is dirty)
            for j in np.arange(len(frames), rows * cols):
                ax[j // 3, j % 3].set_visible(False)
        plt.tight_layout()

    def plot_average_frame(self, step: int = 500):
        """Plot the average of every "step" frames in the video.

        Parameters
        ----------
        step : int, optional
            The step between frames to average by, lower values result in a smoother average, by default 10.
        
        Examples
        --------
        >>> from webcat_utils import WebCAT
        >>> wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
        >>> wc.plot_average_frame()
        ...
        <matplotlib.subplot>
        """
        N = self.frames // step  # how many frames to average based on step
        timex = np.zeros((self.height, self.width, 3, N), np.float)  # init array
        for i in range(N):  # I dislike loops, could probably make this much faster
            self.video.set(1, i * step)
            _, frame_arr = self.video.read()
            timex[:, :, :, i] = cv2.cvtColor(frame_arr, cv2.COLOR_BGR2RGB)
        timex = np.mean(timex, axis=-1).astype(int)
        plt.subplots(1, 1, figsize=(10, 7))
        plt.imshow(timex)
        plt.title(f"Average of every {step} frames, {N} frames in total")


class TqdmUpTo(tqdm):
    """Utility class for displaying a progress bar.

    Methods
    -------
    download_url(self, fout=None, verbose=1)
        Download the video from the url.

    Examples
    --------
    >>> url = "http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4"
    >>> with TqdmUpTo(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=f"Saving to {fout}") as t:
    >>>     urllib.request.urlretrieve(self.fin, fout, reporthook=t.update_to)
    ...
    Saving to buxtoncoastalcam.2019-11-13_1000.mp4:  0%|      | 44.1M/125M [00:08<00:16, 5.18MB/s]
    """

    def update_to(self, b: int = 1, bsize: int = 1, tsize: int = None):
        """Progress bar udpate function.

        Parameters
        ----------
        b : int, optional
            Number of blocks transferred so far, by default 1
        bsize : int, optional
             Size of each block (in tqdm units), by default 1
        tsize : int, optional
            Total size (in tqdm units), by default None
        """

        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


def cli(
    directory: str,
    station: list,
    year: list,
    month: list,
    day: list,
    time: list,
    interval: int,
    no_meta: bool,
    verbose: bool,
):
    """Command line function for saving frames of webCAT videos.

    Parameters
    ----------
    directory : str
        Absolute path of directory to save frames and metadata in.
    station : list
        List of stations to iterate over.
    year : list
        List of years to iterate over.
    month : list
        List of months to iterate over.
    day : list
        List of days to iterate over.
    time : list
        List of times to iterate over.
    interval : int
        Interval in seconds between video frames to save.
    no_meta : bool
        Don't save .csv file of metadata of saved video frames.
    verbose : bool
        Print program status during execution.
    """
    wc = WebCAT()
    for item in itertools.product(station, year, month, day, time):
        try:
            wc.generate_url(*item)  # generate url from the input data
            tmp_dir = os.path.join(directory, item[0], wc.name)  # dir to save frames in
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)  # mkdir if not exist
            if verbose:
                print(f"Saving frames of {wc.name}...")
            wc.save_frames(interval, tmp_dir, not no_meta, verbose)  # save frames
        except:
            url = f"http://webcat-video.axds.co/{item[0]}/raw/{item[1]}/{item[1]}_{item[2]}/{item[1]}_{item[2]}_{item[3]}/{item[0]}.{item[1]}-{item[2]}-{item}_{item[4]}.mp4"
            print(f"Warning: {url} not a valid url... Skipping.")


def dir_path(path: str):
    """Utility function for argparse to check existence of a passed directory.

    Parameters
    ----------
    path : str
        Absolute path to local directory.

    """

    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid directory path."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI for saving frames of webCAT video(s)."
    )
    required = parser.add_argument_group("required arguments")
    # below I'm using --arg with "required" to allow for multiple "nargs"
    required.add_argument(
        "-dir",
        "--directory",
        type=dir_path,
        help="Absolute path of directory to save frames in.",
        required=True,
    )
    required.add_argument(
        "-s",
        "--station",
        nargs="+",
        type=str,
        help="The station name, e.g., buxtoncoastalcam.",
        required=True,
    )
    required.add_argument(
        "-y",
        "--year",
        nargs="+",
        type=int,
        help="The video year(s), e.g., 2019 2020.",
        required=True,
    )
    required.add_argument(
        "-m",
        "--month",
        nargs="+",
        type=int,
        help="The video month(s), e.g., 9 10 11.",
        required=True,
    )
    required.add_argument(
        "-d",
        "--day",
        nargs="+",
        type=int,
        help="The video day(s) e.g., 1 11 21.",
        required=True,
    )
    required.add_argument(
        "-t",
        "--time",
        nargs="+",
        type=int,
        help="The video time(s), e.g., 1000 1330 1510.",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--interval",
        default=10,
        type=int,
        help="Interval in seconds between video frames to save (default: 10).",
    )
    parser.add_argument(
        "-n",
        "--no_meta",
        action="store_true",
        help="Don't save .csv file of metadata of saved video frames.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print program status."
    )
    args = parser.parse_args()
    cli(
        args.directory,
        args.station,
        args.year,
        args.month,
        args.day,
        args.time,
        args.interval,
        args.no_meta,
        args.verbose,
    )
