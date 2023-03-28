import json
from analyzers.classes import WebAnalyzer
import pypdns


class CirclDNS(WebAnalyzer):

    def run(self, ioc, type):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "domain" or type == "ip":

            # Load the authentication credentials
            with open("../src/configurations/analyzers.json") as jsonFile:
                configurations = json.load(jsonFile)
                jsonFile.close()
                username = configurations["circlDNS"]["username"]
                password = configurations["circlDNS"]["password"]

            # Authenticate the client
            client = pypdns.PyPDNS(basic_auth=(username, password))

            # Make the query
            try:
                data = client.query(ioc)
                return data

            except Exception as e:
                print(f"Error: {e}")
                return None

        else:
            return None
