from analyzers.classes import WebAnalyzer
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import json
import analyzers.contextualize.contextualize
from utils import encode

class AlienVault(WebAnalyzer):

    def make_relationship(self, data, source_id):
        sdo = json.loads(data)
        target_id = sdo["id"]
        relationship_data = {
            "source": source_id,
            "target": target_id,
            "rel_type": "indicates"
        }
        print(relationship_data)
        relationship = encode("sro", relationship_data)
        return relationship
    

    def convert(self, data, node_id):
        pulse_info = data["pulse_info"]
        pulses = pulse_info["pulses"]
        encoded_data = []
        countries = []
        sighted_by = []
        ttps = []
        if len(pulses) > 0:
            for pulse in pulses:
                # getting the location
                for country in pulse["targeted_countries"]:
                    if country not in countries:
                        countries.append(country)
        
                        

                # storing the ttps!
                for attack_id in pulse["attack_ids"]:
                    if attack_id["id"] not in ttps:
                        ttps.append(attack_id["id"])
                    
        for country in countries:
            data = {
                "name": country,
                "country": country,
                "latitude": 0,
                "longitude": 0,
            }
            data_to_send = {
                "type": "location",
                "data": data
            }
            result = encode("sdo", data_to_send)
            if result is not None:
                encoded_data.append(result)
                sro = self.make_relationship(result, node_id)
                if sro is not None:
                    encoded_data.append(sro)
        
        for attack_id in ttps:
            attack_pattern = analyzers.contextualize.contextualize.get_mitre_data(attack_id, "attack-pattern")
            if attack_pattern is not None:
                encoded_data.append(attack_pattern)
                sro = self.make_relationship(attack_pattern, node_id)
                if sro is not None:
                    encoded_data.append(sro)


        return encoded_data


    def run(self, ioc, type, node_id = None):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        # Load the API key
        with open("../src/configurations/analyzers.json") as jsonFile:
            configurations = json.load(jsonFile)
            jsonFile.close()
        self._key = configurations["alienVault"]["key"]
        otx = OTXv2(self._key)

        # Determine which indicator type to use
        if type == "file":
            pass

        # File hashes
        elif type == "sha1":
            indicatorType = IndicatorTypes.FILE_HASH_SHA1

        elif type == "sha256":
            indicatorType = IndicatorTypes.FILE_HASH_SHA256

        elif type == "md5":
            indicatorType = IndicatorTypes.FILE_HASH_MD5

        elif type == "url":
            indicatorType = IndicatorTypes.URL

        elif type == "domain":
            indicatorType = IndicatorTypes.DOMAIN

        elif type == "ip":
            indicatorType = IndicatorTypes.IPv4

        else:
            pass

        # response = otx.get_indicator_details_full(
        #    indicator_type=indicatorType, indicator=ioc)

        response = otx.get_indicator_details_by_section(
            indicator_type=indicatorType, indicator=ioc, section="general")
        if node_id is not None:
            data = self.convert(response, node_id)
            return data
        else:
            return response
