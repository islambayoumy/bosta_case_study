import json
import os
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from src.utils import parse_args
from src.utils.base_classes import DataExtractor, Logger


class DataFlatten(DataExtractor):
    """A class for building the ETL for DataFlatten"""

    def __init__(self):
        super().__init__()
        self.logger = Logger("Data Flatten API").logger
        self.args = parse_args()
        self.data_url = os.path.join("..", "..", "input_data", "sample_data.json")
        self.data = None
        self.dfs = {}
        self.column_mappings = {
            "orders": {
                "_id": self._safe_get_id,
                "order_id": "order_id",
                "type": "type",
                "createdAt": lambda x: datetime.fromisoformat(x["$date"][:-1]),
                "updatedAt": lambda x: datetime.fromisoformat(x["$date"][:-1]),
                "collectedFromBusiness": lambda x: datetime.fromisoformat(x["$date"][:-1])
            },
            "cod": {
                "_id": self._safe_get_id,
                "amount": "amount",
                "isPaidBack": "isPaidBack",
                "collectedAmount": "collectedAmount"
            },
            "confirmation": {
                "_id": self._safe_get_id,
                "isConfirmed": "isConfirmed",
                "numberOfSmsTrials": "numberOfSmsTrials"
            },
            "address": {
                "_id": self._safe_get_address_id,
                "floor": None,
                "apartment": None,
                "secondLine": "secondLine",
                "district": "district",
                "firstLine": "firstLine",
                "geoLocation_lat": self._safe_get_coordinates(0),
                "geoLocation_long": self._safe_get_coordinates(1),
                "city_id": self._safe_get_nested_value("city", "_id"),
                "zone_id": self._safe_get_nested_value("zone", "_id"),
                "country_id": self._safe_get_nested_value("country", "_id")
            },
            "city": {"name": "name"},
            "zone": {"name": "name"},
            "country": {"name": "name", "code": "code"},
            "receiver": {
                "_id": self._safe_get_id,
                "firstName": "firstName",
                "lastName": "lastName",
                "phone": "phone"
            },
            "star": {"name": "name", "phone": "phone"},
            "tracker": {"trackerId": "trackerId"}
        }

    def _safe_get_id(self, item):
        try:
            if isinstance(item, dict):
                return item.get("_id")
            elif isinstance(item, str):
                return item
            else:
                raise ValueError(f"Unexpected type for _id: {type(item)}")
        except Exception as e:
            self.logger.warning(f"Error getting ID: {str(e)}")
            return None

    def _safe_get_address_id(self, address):
        try:
            if isinstance(address, dict):
                return f'dropoff_{address.get("dropOffAddress", {}).get("_id")}'
            elif isinstance(address, str):
                return address
            else:
                raise ValueError(f"Unexpected type for address: {type(address)}")
        except Exception as e:
            self.logger.warning(f"Error getting address ID: {str(e)}")
            return None

    def _safe_get_nested_value(self, parent_key, child_key):
        def safe_extractor(data):
            try:
                if isinstance(data, dict):
                    parent = data.get(parent_key)
                    if isinstance(parent, dict):
                        return parent.get(child_key)
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                self.logger.warning(f"Error getting nested value: {str(e)}")
                return None

        return safe_extractor

    def _safe_get_coordinates(self, index):
        def safe_extractor(geo_location):
            try:
                if isinstance(geo_location, (list, tuple)) and len(geo_location) > index:
                    return geo_location[index]
                elif isinstance(geo_location, (int, float)):
                    return geo_location
                else:
                    return None
            except Exception as e:
                self.logger.warning(f"Error extracting coordinate: {str(e)}")
                return None

        return safe_extractor

    def _safe_get_city_id(self, city_data):
        try:
            if isinstance(city_data, dict):
                return city_data.get("_id")
            elif isinstance(city_data, str):
                return city_data
            else:
                return None
        except Exception as e:
            self.logger.warning(f"Error getting city ID: {str(e)}")
            return None

    def _safe_get_zone_id(self, zone_data):
        try:
            if isinstance(zone_data, dict):
                return zone_data.get("_id")
            elif isinstance(zone_data, str):
                return zone_data
            else:
                return None
        except Exception as e:
            self.logger.warning(f"Error getting zone ID: {str(e)}")
            return None

    def extract(self) -> None:
        self.logger.info(f"Extracting data from {self.data_url}")
        try:
            with open(self.data_url, 'r') as file:
                self.data = json.load(file)
        except Exception as err:
            self.logger.error(f"Failed to extract data: {str(err)}")
            raise RuntimeError(f"Failed to extract data: {str(err)}")

    def transform(self) -> None:
        self.logger.info("Transforming data")
        self.dfs = {}

        for order in self.data:
            self._process_order(order)

        self.logger.info("Transformation completed")

    def _process_order(self, order: Dict[str, Any]) -> None:
        order_id = order["_id"]

        # Process orders
        self._add_to_dataframe("orders", {
            "_id": order_id,
            "order_id": order["order_id"],
            "type": order["type"],
            "createdAt": order["createdAt"],
            "updatedAt": order["updatedAt"],
            "collectedFromBusiness": order["collectedFromBusiness"],
            "confirmation_id": order_id,
            "dropOffAddress_id": f'dropoff_{order_id}',
            "pickupAddress_id": f'pickup_{order_id}',
            "receiver_id": order["receiver"]["_id"],
            "star_id": order["star"]["_id"],
            "tracker_id": order["tracker"]["trackerId"],
            "cod_id": order_id
        })

        # Process COD
        self._add_to_dataframe("cod", {
            "_id": order_id,
            "amount": order["cod"]["amount"],
            "isPaidBack": order["cod"]["isPaidBack"],
            "collectedAmount": order["cod"]["collectedAmount"]
        })

        # Process Confirmation
        self._add_to_dataframe("confirmation", {
            "_id": order_id,
            "isConfirmed": order["confirmation"]["isConfirmed"],
            "numberOfSmsTrials": order["confirmation"]["numberOfSmsTrials"]
        })

        # Process Addresses
        self._process_addresses(order, order_id)

        # Process other entities
        self._process_other_entities(order, order_id)

    def _process_addresses(self, order: Dict[str, Any], order_id: str) -> None:
        # Process Drop-off Address
        dropoff_address_id = f'dropoff_{order_id}'
        self._add_to_dataframe("address", {
            "_id": dropoff_address_id,
            "floor": None,
            "apartment": None,
            "secondLine": order["dropOffAddress"]["secondLine"],
            "district": order["dropOffAddress"]["district"],
            "firstLine": order["dropOffAddress"]["firstLine"],
            "geoLocation_lat": self._get_geo_location_value(order["dropOffAddress"]["geoLocation"], 0),
            "geoLocation_long": self._get_geo_location_value(order["dropOffAddress"]["geoLocation"], 1),
            "city_id": order["dropOffAddress"]["city"]["_id"],
            "zone_id": order["dropOffAddress"]["zone"]["_id"],
            "country_id": order["dropOffAddress"].get("country", {}).get("_id")
        })

        # Process Pickup Address
        pickup_address_id = f'pickup_{order_id}'
        self._add_to_dataframe("address", {
            "_id": pickup_address_id,
            "floor": order["pickupAddress"]["floor"],
            "apartment": order["pickupAddress"]["apartment"],
            "secondLine": order["pickupAddress"]["secondLine"],
            "district": order["pickupAddress"]["district"],
            "firstLine": order["pickupAddress"]["firstLine"],
            "geoLocation_lat": self._get_geo_location_value(order["pickupAddress"]["geoLocation"], 0),
            "geoLocation_long": self._get_geo_location_value(order["pickupAddress"]["geoLocation"], 1),
            "city_id": order["pickupAddress"]["city"]["_id"],
            "zone_id": order["pickupAddress"]["zone"]["_id"],
            "country_id": order["pickupAddress"].get("country", {}).get("_id")
        })

        # Process City
        self._add_to_dataframe("city", {
            "_id": order["dropOffAddress"]["city"]["_id"],
            "name": order["dropOffAddress"]["city"]["name"]
        })

        # Process Zone
        self._add_to_dataframe("zone", {
            "_id": order["dropOffAddress"]["zone"]["_id"],
            "name": order["dropOffAddress"]["zone"]["name"]
        })

        # Process Country
        if "country" in order["pickupAddress"]:
            self._add_to_dataframe("country", {
                "_id": order["pickupAddress"]["country"]["_id"],
                "name": order["pickupAddress"]["country"]["name"],
                "code": order["pickupAddress"]["country"]["code"]
            })

    def _process_other_entities(self, order: Dict[str, Any], order_id: str) -> None:
        # Process Receiver
        self._add_to_dataframe("receiver", {
            "_id": order["receiver"]["_id"],
            "firstName": order["receiver"]["firstName"],
            "lastName": order["receiver"]["lastName"],
            "phone": order["receiver"]["phone"]
        })

        # Process Star
        self._add_to_dataframe("star", {
            "_id": order["star"]["_id"],
            "name": order["star"]["name"],
            "phone": order["star"]["phone"]
        })

        # Process Tracker
        self._add_to_dataframe("tracker", {
            "_id": order["tracker"]["trackerId"],
            "trackerId": order["tracker"]["trackerId"],
            "order_id": order_id
        })

    def _get_geo_location_value(self, geo_location, index):
        try:
            if isinstance(geo_location, (list, tuple)):
                return geo_location[index] if len(geo_location) > index else None
            elif isinstance(geo_location, (int, float)):
                return geo_location
            else:
                raise ValueError(f"Unexpected type for geoLocation: {type(geo_location)}")
        except Exception as e:
            self.logger.warning(f"Error processing geoLocation: {str(e)}")
            return None

    def _add_to_dataframe(self, table_name: str, data: Dict[str, Any]) -> None:
        if table_name not in self.dfs:
            self.dfs[table_name] = pd.DataFrame(columns=self.column_mappings[table_name].keys())

        new_row = {}
        for key, value in self.column_mappings[table_name].items():
            if callable(value):
                new_row[key] = value(data.get(key))
            else:
                new_row[key] = data.get(value)

        self.dfs[table_name] = pd.concat([self.dfs[table_name], pd.DataFrame([new_row])], ignore_index=True)

    def load(self) -> None:
        self.logger.info("Loading data")
        output_dir = os.path.join("..", "..", "output_data")
        os.makedirs(output_dir, exist_ok=True)

        for name, df in self.dfs.items():
            file_path = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(file_path, index=False)
            self.logger.info(f"Successfully loaded {name} records")


if __name__ == "__main__":
    DataFlatten().run()
