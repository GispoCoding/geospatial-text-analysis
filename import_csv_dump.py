import csv
import pytz
from datetime import datetime
from glob import glob
from pyproj import Transformer

DEFAULT_TZ = "Europe/Helsinki"
DEFAULT_CRS = 3879  # By default, the csv is in the Helsinki coordinate system


def format_datetime(datetime_string: str) -> str:
    # Converts weird datetimes to ISO format
    incoming = datetime.strptime(datetime_string, "%Y-%m-%d-%H.%M.%S.%f")
    timezone = pytz.timezone(DEFAULT_TZ)
    incoming = timezone.localize(incoming)
    return incoming.isoformat()


def import_csv_dump(files: str = r"data/*_20[0-9][0-9].csv") -> dict:
    # What we have is yearly csv dumps of the data. Iterate through all of them
    entries = []
    transformer = Transformer.from_crs(DEFAULT_CRS, 4326)
    for file in glob(files):
        with open(file, encoding='latin1') as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            # The file has no header, luckily the field order is the same as in the API.
            #  - Some fields are missing, tho
            #  - Datetimes are in a proprietary format instead of ISO
            #  - Coordinates have to be transformed from Helsinki coords to WGS84
            for row in reader:
                if row[10] and row[11]:
                    lat, lon = transformer.transform(
                        float(row[10]), float(row[11])
                        )
                    # The data may contain erroneous (0, 0) coordinate pairs. They are not
                    # within EPSG:3879 and will transform to infinity.
                    if lat == float('inf') or lat == float('-inf') or lon == float('inf') or lon == float('-inf'):
                        lat, lon = None, None
                else:
                    lat, lon = None, None
                entries.append({
                    "service_request_id": row[0],
                    "service_code": row[1],
                    "description": row[2],
                    "service_notice": None,
                    "requested_datetime": format_datetime(row[3]),
                    "updated_datetime": format_datetime(row[4]),
                    "status": row[5],
                    "status_notes": row[6],
                    "agency_responsible": row[7],
                    "service_name": row[8],
                    "address": row[9],
                    "address_id": None,
                    "zip_code": None,
                    "lat": lat,
                    "media_url": None,
                    "long": lon,
                    "extended_attributes": None
                    })
    return entries
