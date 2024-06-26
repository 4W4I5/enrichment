import json
import time
import requests
from analyzers.classes import WebAnalyzer


class YARAify(WebAnalyzer):
    def run(self, ioc, type, node_id = None):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "file":
            # Set the endpoint URL
            url = "https://yaraify-api.abuse.ch/api/v1/"

            # Create the headers
            headers = {
                "accept": "application/json"
            }

            # Create the payload
            # These parameters have been defined in the API's documentation
            data = {
                "clamav_scan": 1,
                "unpack": 1,
                "share_file": 1
            }

            # Add the file's contents
            files = {
                "json_data": (None, json.dumps(data), "application/json"),
                "file": ioc}

            # Send the request
            # try:
            #     response = requests.request(
            #         method="POST", url=url, headers=headers, files=files)
            #     response.raise_for_status()

            #     # Extract the task ID from the response
            #     task_id = response.json()["data"]["task_id"]

            # except Exception as e:
            #     print(e)
            #     return None

            # Now, use the task ID to fetch the results of the scan
            task_id = "8f2303f8-d36d-11ed-866d-42010aa4000b"
            data = {"query": "get_results",
                    "task_id": f"{task_id}"}
            data = json.dumps(data)

            # time.sleep(60)

            # Send the request
            try:
                response = requests.request(
                    method="POST", url=url, headers=headers, files=files)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                print(e)
                return None

        elif type == "hash":
            # Set the endpoint URL
            url = "https://yaraify-api.abuse.ch/api/v1/"

            # Create the headers
            headers = {
                "accept": "application/json"
            }

            # Create the payload
            data = {"query": "lookup_hash",
                    "search_term": f"{ioc}"}
            data = json.dumps(data)

            # Send the request
            try:
                response = requests.request(
                    method="POST", url=url, headers=headers, data=data)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                print(e)
                return None

        else:
            return None
