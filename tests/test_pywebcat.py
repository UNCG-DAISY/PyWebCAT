from pywebcat import __version__
from pywebcat.utils import WebCAT
from pytest import raises
import numpy as np
import os


def test_version():
    assert __version__ == "0.1.2"


def test_generate_url():
    wc = WebCAT()
    wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
    assert (
        wc.url
        == "http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4"
    )
    assert [wc.name, wc.width, wc.height, wc.frames, wc.fps] == [
        "buxtoncoastalcam_2019_11_13_1000",
        1280,
        720,
        17097,
        28,
    ]
    with raises(ValueError):
        wc.generate_url("fakestation", 2019, 11, 13, 1000)


def test_save_frames(tmpdir):
    wc = WebCAT()
    wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
    wc.save_frames(
        delta_t=int(wc.frames / wc.fps // 2), fout_path=tmpdir, save_csv=True
    )
    with raises(ValueError):
        wc.save_frames(delta_t=wc.frames)


# commenting out for now because this test takes some time
# def test_download(tmpdir):
#     wc = WebCAT()
#     wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
#     wc.download_url(fout=os.path.join(tmpdir, "download.mp4"), verbose=False)
#     wc.download_url(fout=os.path.join(tmpdir, "download.mp4"), verbose=True)


def test_plotting():
    wc = WebCAT()
    wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
    wc.plot_frames(frames=[0, 1])
    with raises(ValueError):
        wc.plot_frames(frames=[wc.frames])
    wc.plot_average_frame(step=wc.frames // 2)
