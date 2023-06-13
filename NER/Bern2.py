# The Bern2 class is a Python implementation of the BERN2 model for named entity recognition, which
# can be used to extract entities from text and normalize them.
from  NER.Bern import BERN2
import os
from config import config_info


class Bern2:

    def __init__(self,):
        """
        This function initializes and sets up the BERN2 model for named entity recognition and
        normalization.
        """
    
        ## TO DO: Run the Multi_ner server from here

        resources_path = config_info.get_resources_path(ner_module="bern2") ## It hold the resources such as tmVarJava, GnormPlus etc.
        ## TO DO: Perform a check to see is this directory available

        self.gnormplus = os.path.join(resources_path,"GNormPlusJava")
        self.tmvar = os.path.join(resources_path,"tmVarJava")
        self.normalization = os.path.join(resources_path,"normalization")

        ### Instansiating the model
        self.model = BERN2(
            normalizer_dir=self.normalization,
            mtner_home="Bern\multi_ner", ## mtner_home will run from here
            mtner_port= 18894,
            gnormplus_home=self.gnormplus,
            gnormplus_port=18895,
            tmvar2_home=self.tmvar,
            tmvar2_port=18896,
            gene_norm_port=18888,
            disease_norm_port=18892,
            cache_host="localhost",
            use_neural_normalizer=False,
            no_cuda=False,
            cache_port=27017,
        )

        print("BERN2 loaded")

    def bern2Api(self,text):
        """
        The function takes in text and returns an API through either URL access or a class, with error
        handling.
        
        Args:
          text: The input text that needs to be annotated using the BERN model.
        
        Returns:
          If there is an error in annotating the text using the BERN model, the function will return
        `None`. Otherwise, it will return a dictionary containing the annotated text.
        """
      
        result_dict = self.model.annotate_text(text)
        if "error_code" in result_dict.keys():
            if int(result_dict["error_code"]) != 0:
                return None
            else:
                return result_dict
        else:
            print("error ocurred in annotating through BERN model, check log files")


    def responseProcessor(self,response):
        """
        This function processes a response by extracting relevant information from it and returning it
        in a uniform format.
        
        Args:
          response: a dictionary containing the response data from an API call
        
        Returns:
          a list of dictionaries, where each dictionary contains information about an entity mentioned
        in the response. The information includes the word, start and end positions of the entity in the
        response, the entity type, and the normalized ID of the entity.
        """
        """
        Process the repsone and harmonize it in a uniform format

        """
        annotation = response["annotations"]
        processed = []
        for entity in annotation:
            ## Need to append the normalization infor as well
            entityData = {"word": entity["mention"],
                        "start":entity["span"]["begin"],
                        "end":entity["span"]["end"],
                        "entity":entity["obj"].lower(),
                        "normalized_id": entity["id"],
                        }
            processed.append(entityData)


        return processed
        

    def extractor(self,text):
        """
        The function "extractor" returns the processed response from the "bern2Api" method.
        
        Args:
          text: The input text that needs to be processed by the API.
        
        Returns:
          The method `extractor` is returning the output of the method `responseProcessor` which takes
        the input `text` and passes it to the method `bern2Api`. The output of `bern2Api` is then
        returned by `responseProcessor` and ultimately returned by `extractor`. Therefore, `extractor` is
        returning the final response generated by the `bern2Api` method after
        """
        """
        Method expose to get final response 

        """
        return self.responseProcessor(self.bern2Api(text))
    
    
if __name__ == '__main__':
    text = """Here we show that dysregulated expression of Cyp1a1 in mice depletes the reservoir of natural AHR ligands, generating a quasi AHR-deficient state. 
             """
    abner_api = Bern2()
    entities = abner_api.extractor(text=text)
    print(entities)