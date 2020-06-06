import urllib.request
import cv2
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")
plt.rcParams.update(
    {
        "font.size": 14,
        "axes.labelweight": "bold",
        "figure.figsize": (8, 6),
        "axes.grid": False,
    }
)


class VidViewer:
    """Utility class for viewing local or remote webcat videos.

    Parameters
    ----------
    fin : str
        A url or local file path to the .mp4 file to view.

    Attributes
    ----------
    fin
    video : cv2.VideoCapture
        The cv2.VideoCapture object of the video file provided by fin.
    frames: int
        Total number of frames in the video.
    fps : int
        Frames per second in the video.

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

    def __init__(self, fin: str):
        self._fin = fin
        self.video = cv2.VideoCapture(self.fin)

    @property
    def fin(self):
        return self._fin

    @fin.setter
    def fin(self, value: str):
        self._fin = value
        self.video = cv2.VideoCapture(self.fin)

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

    def download_url(self, fout, verbose: bool = True):
        """Download the video from the instance url.

        Parameters
        ----------
        fout : str
            The file path to save the downloaded file to, by default None
        verbose : {True, False}, optional
            Display download progress bar, by default True
        """
        fout = fout + ".mp4" if fout[-4:] != ".mp4" else fout
        try:
            if verbose:
                with TqdmUpTo(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    miniters=1,
                    desc=f"Saving to {fout}",
                ) as t:  # all optional kwargs
                    urllib.request.urlretrieve(self.fin, fout, reporthook=t.update_to)
            else:
                urllib.request.urlretrieve(self.fin, fout)
        except:
            print(f"{self.url} is not a valid url.")

    def save_frames(self, delta_t: int = 10, fout=""):
        """Download the video from the instance url.

        Parameters
        ----------
        delta_t : int, optional
            A frame will be saved every delta_t seconds, by default 10
        fout : str, optional
            Path to save at, e.g., "~/Downloads/"
        """
        assert delta_t < int(
            self.frames / self.fps
        ), f"delta_t should be less than {int(self.frames / self.fps)}"
        step = delta_t * self.fps
        for i in tqdm(range(0, (self.frames + 1), step)):
            self.video.set(1, i)
            _, frame_arr = self.video.read()
            cv2.imwrite(fout + f"frame_{i}.jpg", frame_arr)

    def plot_frames(self, frames: list = [0]):
        """Plot frames from the video, zero-based indexing.

        Parameters
        ----------
        frames : list, optional
            List of the frames to display in a grid plot, by default [0]
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
