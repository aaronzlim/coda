# TODO: Module docstring

import csv
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from enum import IntEnum
from math import modf, floor
from pathlib import Path
import pytz
import xml.etree.ElementTree as ET


# CONSTANTS #
GPX_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
GPX_TIMEZONE = pytz.timezone('GMT')


@dataclass
class GpxTrackPoint:
    """Class to model a GPX track point."""
    lat: float
    lon: float
    speed: float
    time: datetime


class GpxData:
    """Class to model GPX data output by a Cox Orb."""

    def __init__(self, gpx_file: str):
        """Read a GPX file as a set of tracks.

        Args:
            gpx_file (str): Path to the GPX file to read.

        Raises:
            IOError: File does not exist.
            IOError: File does not have a .GPX extension.
        """

        gpx_path = Path(gpx_file)

        if not gpx_path.exists():
            raise IOError(f'No such file {gpx_path}')

        if gpx_path.suffix.upper() != '.GPX':
            raise IOError(f'Expecting file with extension .GPX, given {gpx_path.suffix}')

        tree = ET.parse(gpx_path)
        root = tree.getroot()
        prefix = root.tag.split('}')[0] + '}' # remove anything after the prefix

        trkpts = root.find(prefix+'trk').find(prefix+'trkseg').findall(prefix+'trkpt')

        self.tracks = []
        for trkpt in trkpts:
            lat = float(trkpt.attrib.get('lat', 'nan'))
            lon = float(trkpt.attrib.get('lon', 'nan'))
            speed = float(trkpt.find(prefix+'speed').text)
            time = datetime.strptime(trkpt.find(prefix+'time').text, GPX_TIME_FORMAT)
            # make time timezone aware
            time = datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond, GPX_TIMEZONE)
            self.tracks.append(GpxTrackPoint(lat, lon, speed, time))

    def __iter__(self):
        return iter(self.tracks)


@dataclass
class GraphRecord:
    distance: float
    time: datetime
    stroke_count: int
    stroke_rate: float
    check: float
    split: time
    speed: float
    distance_per_stroke: float


class GraphColumn(IntEnum):
    """Enumeration of column header indices.

    Distance,Elapsed Time,Stroke Count,Rate,Check,Speed (mm:ss/500m),Speed (m/s),Distance/Stroke
    """
    DISTANCE: int = 0
    ELAPSED_TIME: int = 1
    STROKE_COUNT: int = 2
    STROKE_RATE: int = 3
    CHECK: int = 4
    SPLIT: int = 5
    SPEED: int = 6
    DISTANCE_PER_STROKE: int = 7


class GraphData:
    """Class to model graph data output by a Cox Orb."""

    def __init__(self, graph_file: str, tz: str):

        graph_path = Path(graph_file)

        if not graph_path.exists():
            raise IOError(f'No such file {graph_file}')

        if graph_path.suffix.lower() != '.csv':
            raise IOError(f'Expecting file with extension .csv, given {graph_path.suffix}')

        tz = pytz.timezone(tz)
        self.records = []
        with open(graph_path) as csvfile:
            reader = csv.reader(csvfile)
            for idx, row in enumerate(reader):
                if idx == 0:
                    ref = datetime.strptime(row[0], 'COXORB Performance Data   %H:%M  %d/%m/%Y ')
                    ref_datetime = datetime(ref.year, ref.month, ref.day, ref.hour, ref.minute, ref.second, ref.microsecond, tz)

                if idx < 3:
                    continue # empty line, and column names

                # parse the elapsed time into a datetime.time object
                elapsed_hms, elapsed_frac = row[GraphColumn.ELAPSED_TIME].split('.')
                elapsed_millisecond = int(float('0.'+elapsed_frac)*1e3)
                elapsed_hour, elapsed_minute, elapsed_second = (int(t) for t in elapsed_hms.split(':'))
                elapsed_time = timedelta(hours=elapsed_hour, minutes=elapsed_minute, seconds=elapsed_second, milliseconds=elapsed_millisecond)

                # parse the split into a datetime.time object
                split_minute, split_second = (int(x) for x in row[GraphColumn.SPLIT].split(':'))
                if split_minute > 60 or split_second > 59: # sometimes split is 99:59, so correct to 00:00
                    split_minute = 0
                    split_second = 0
                split = time(minute=split_minute, second=split_second)

                self.records.append(
                    GraphRecord(
                        distance=float(row[GraphColumn.DISTANCE]),
                        time=ref_datetime + elapsed_time,
                        stroke_count=int(row[GraphColumn.STROKE_COUNT]),
                        stroke_rate=float(row[GraphColumn.STROKE_RATE]),
                        check=float(row[GraphColumn.CHECK]),
                        split=split,
                        speed=float(row[GraphColumn.SPEED]),
                        distance_per_stroke=float(row[GraphColumn.DISTANCE_PER_STROKE])
                        )
                    )

    def __iter__(self):
        return iter(self.records)
