# The Abner class provides methods to extract entities from text using the ABNER NER module and
# process the response in a uniform format.

from config import config_info
from urllib.parse import urljoin
import requests
class Abner:

    def __init__(self,):
        """
        This function initializes an endpoint URL for extracting entities using the ABNER named entity
        recognition module.
        """
        
        resource_url = config_info.get_resources_url(ner_module="abner")
        self.endpoint_url = urljoin(resource_url,"extract_entities")

        print("Abner loaded")

    def abnerApi(self,text):
        """
        This function sends a POST request to an API endpoint with a given text and returns the JSON
        response.
        
        Args:
          text: The text that needs to be sent to the API for processing.
        
        Returns:
          the JSON response obtained from a POST request to a specified endpoint URL with the input text
        as a parameter.
        """
        
        data = {"text":text}

        ## TO DO: Add a function, which check the response status and raise if error occured
        response = requests.post(url=self.endpoint_url,
                                 json=data)
        return response.json()

    
    def responseProcessor(self,response):
        """
        This function processes a response and converts it into a uniform format for named entity
        recognition.
        
        Args:
          response: a dictionary containing the result of a named entity recognition (NER) process, with
        keys "Result" and "Status"
        
        Returns:
          a list of dictionaries containing information about entities extracted from the input text. If
        the input response contains a "Result" key with a list value, the function extracts the "word",
        "start", "end", and "entity_type" values for each entity in the list and adds them to a
        dictionary. This dictionary is then appended to the "processed" list. If the input
        """
    
        processed = []
        if isinstance(response["Result"],list):
            entities = response["Result"]

            for entity in entities:
                entityData = {"word": entity["word"],
                            "start":entity["start"],
                            "end":entity["end"],
                            "entity":entity["entity_type"].lower()}
                processed.append(entityData)
        else:
            print("Error occured in ABNER ner")

        return processed

    def extractor(self,text):
        """
        The function "extractor" returns the final response by processing the output of the "abnerApi"
        function.
        
        Args:
          text: The input text that needs to be processed by the Abner API.
        
        Returns:
          The method `extractor` returns the output of the method `responseProcessor` which takes the
        output of the method `abnerApi` as input.
        """
        
        return self.responseProcessor(self.abnerApi(text=text))
    
if __name__ == '__main__':
    text = """Constitutive expression of Cyp1a1 throughout the body or restricted specifically to intestinal epithelial cells resulted in loss of AHR-dependent type 3 innate lymphoid cells and T helper 17 cells and increased susceptibility to enteric infection. The deleterious effects of excessive AHR ligand degradation on intestinal immune functions could be counter-balanced by increasing the intake of AHR ligands in the diet. Thus, our data indicate that intestinal epithelial cells serve as gatekeepers for the supply of AHR ligands to the host and emphasize the importance of feedback control in modulating AHR pathway activation"""
    abner_api = Abner()
    entities = abner_api.extractor(text=text)
    print(entities)
