import json
from datetime import datetime
from typing import Iterable

from app.bookings.dao import BookingDAO
from app.spaces.dao import SpacesDAO
from app.spaces.pools.dao import PoolDAO
from app.logger import logger

TABLE_MODEL_MAP = {
    "spaces": SpacesDAO,
    "pools": PoolDAO,
    "bookings": BookingDAO,
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except ValueError:
        logger.error("Cannot convert CSV into DB format", exc_info=True)
