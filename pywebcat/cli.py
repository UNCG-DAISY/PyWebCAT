import os
import sys
import argparse
import itertools
from pywebcat.utils import WebCAT


def main():
    """Command line function for saving frames of webCAT videos.
    """
    (
        directory,
        station,
        year,
        month,
        day,
        time,
        interval,
        no_meta,
        verbose,
    ) = parse_args()
    wc = WebCAT()
    for item in itertools.product(station, year, month, day, time):
        try:
            sys.stdout = open(os.devnull, "w")  # capture any output from url generation
            wc.generate_url(*item)  # generate url from the input data
            sys.stdout = sys.__stdout__  # reinstate output
            tmp_dir = os.path.join(directory, item[0], wc.name)  # dir to save frames in
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)  # mkdir if not exist
            if verbose:
                print(f"Saving frames of {wc.name}...")
            wc.save_frames(interval, tmp_dir, not no_meta, verbose)  # save frames
        except:
            if verbose:
                url = f"http://webcat-video.axds.co/{item[0]}/raw/{item[1]}/{item[1]}_{item[2]:02}/{item[1]}_{item[2]:02}_{item[3]:02}/{item[0]}.{item[1]}-{item[2]:02}-{item[3]:02}_{item[4]:04}.mp4"
                print(f"Warning: {url} not a valid url... Skipping.")


def parse_args():
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

    return (
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
    main()
