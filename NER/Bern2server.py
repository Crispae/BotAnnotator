# The Reach class provides a method to extract entities from text using the Reach API and processes
# the response to harmonize it in a uniform format.
from config import config_info
from urllib.parse import urljoin
import requests

class Bern2server:

    def __init__(self,):
        """
        This function initializes an endpoint URL for a text body API resource.
        """

        resource_url = config_info.get_resources_url(ner_module="bern2server")
        self.endpoint_url = urljoin(resource_url,"plain")

        print("Reach loaded")

    def bern2serverApi(self,text):
        """
        The function sends a POST request to an API endpoint with a given text and returns the response
        in JSON format.
        
        Args:
          text: The text that needs to be sent to the API for processing.
        
        Returns:
          the JSON response obtained from the API after sending a POST request with the provided text
        data to the endpoint URL.
        """
       
        data = {"text":text}

        ## TO DO: Add a function, which check the response status and raise if error occured
        response = requests.post(url=self.endpoint_url,
                                 json=data)
        return response.json()

    
    def responseProcessor(self,response):
        """
        The function processes a response by extracting entities and harmonizing them into a uniform
        format.
        
        Args:
          response: a dictionary containing the response from a natural language processing tool, which
        includes information about entities and their positions in the input text.
        
        Returns:
          a list of dictionaries, where each dictionary contains information about an entity detected in
        the response. The information includes the word, start and end positions, and the type of entity.
        """
       
        entities = response["annotations"]
        processed = []
        for entity in entities:
            ## Need to append the normalization infor as well
            entityData = {"word": entity["mention"],
                        "start":entity["span"]["begin"],
                        "end":entity["span"]["end"],
                        "entity":entity["obj"].lower(),
                        "id":entity["id"],
                        "prob":entity["prob"]
                        }
            processed.append(entityData)
    
        return processed

    def extractor(self,text):
        """
        This function returns the final response by processing the output of the reachApi method with
        the help of the responseProcessor method.
        
        Args:
          text: The input text that needs to be processed by the code. It is passed as an argument to
        the method `extractor()`.
        
        Returns:
          The method `extractor` is returning the output of the method `responseProcessor` which takes
        the output of the method `reachApi` as input. The exact value being returned depends on the
        implementation of `responseProcessor` and `reachApi`.
        """
        
        return self.responseProcessor(self.bern2serverApi(text=text))    
    
if __name__ == '__main__':
    text = """Here we show that dysregulated expression of Cyp1a1 in mice
             depletes the reservoir of natural AHR ligands, generating a quasi AHR-deficient state. 
             """
    bern2_server = Bern2server()
    entities = bern2_server.extractor(text=text)
    print(entities)
