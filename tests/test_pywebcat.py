from pywebcat import __version__
from pywebcat.utils import WebCAT
from pytest import raises


def test_version():
    assert __version__ == "0.1.0"


def test_generate_url():
    wc = WebCAT()
    wc.generate_url("buxtoncoastalcam", 2019, 11, 13, 1000)
    assert (
        wc.url
        == "http://webcat-video.axds.co/buxtoncoastalcam/raw/2019/2019_11/2019_11_13/buxtoncoastalcam.2019-11-13_1000.mp4"
    )
    with raises(ValueError):
        wc.generate_url("fakestation", 2019, 11, 13, 1000)
