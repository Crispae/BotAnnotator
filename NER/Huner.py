# The Huner class uses the Flair library to extract entities from text using a pre-trained model and
# returns the extracted entities in a uniform format.
from config import config_info
import requests
from urllib.parse import urljoin



class Huner:

    def __init__(self,):
        """
        This function initializes a classifier model named "huner".
        """
        resource_url = config_info.get_resources_url(ner_module="huner")
        self.endpoint_url = urljoin(resource_url,"extract")

        print("Huner loaded")

    def hunerApi(self,text):
      
    
        data = {"text":text}

        ## TO DO: Add a function, which check the response status and raise if error occured
        response = requests.post(url=self.endpoint_url,
                                 json=data)
        return response.json()

    def responseProcessor(self,response):
        """
        This function extracts entities from a response and returns them in a uniform format.
        
        Args:
          response: The response object that contains the annotated text and its corresponding
        annotation layers.
        
        Returns:
          a list of dictionaries containing information about the extracted entities from the response.
        Each dictionary contains the word, start and end positions, and entity tag of a single entity.
        """
       
        return response

    def extractor(self,text):
        """
        The function "extractor" returns the processed response from the "hunerApi" method after passing
        a text parameter.
        
        Args:
          text: The input text that needs to be processed by the `hunerApi` method and then passed to
        the `responseProcessor` method to get the final response.
        
        Returns:
          The method `extractor` returns the output of the `responseProcessor` method, which takes the
        output of the `hunerApi` method as input.
        """
        """
        Method expose to get final response 

        """
        return self.responseProcessor(self.hunerApi(text=text))
    
if __name__ == '__main__':
    text = """Here we show that dysregulated expression of Cyp1a1 in mice
             depletes the reservoir of natural AHR ligands, generating a quasi AHR-deficient state. 
             """
    huner_api = Huner()
    entities = huner_api.extractor(text=text)
    print(entities)
