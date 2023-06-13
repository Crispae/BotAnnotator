# The Bioner class loads and manages models for named entity recognition of chemical, disease, and
# gene entities, and provides an API for extracting entities from text using a specified model type.
from transformers import AutoTokenizer,AutoModelForTokenClassification, pipeline
from collections import Counter
from config import config_info
import os

# The Bioner class loads and manages models for named entity recognition of chemical, disease, and
# gene entities.
class Bioner:
    
    def __init__(self,):
        ## loading base_path of model
        self.model_resources = config_info.get_resources_path(ner_module="bioner")
        
        self.models = {
                        "chemical": {
                                        "model_path": os.path.join(self.model_resources,"ner-chemical-bionlp-bc5cdr-pubmed"),
                                        "model": None,
                                        "tokenizer": None
                                    },

                        "disease": {
                                        "model_path": os.path.join(self.model_resources,"ner-disease-ncbi-bionlp-bc5cdr-pubmed"),
                                        "model": None,
                                        "tokenizer": None
                                    },

                            "gene": {
                                        "model_path": os.path.join(self.model_resources,"ner-gene-dna-rna-jnlpba-pubmed"),
                                        "model": None,
                                        "tokenizer": None
                                    }
                    }
        ### Models are loaded correctly
        self.load_models()

        self._current_model = None
        self._current_tokenizer = None

        print("BIONER loaded")


    def load_models(self,):
        """
        This function loads all models when the class is instantiated.
        """

        for model_type, model_info in self.models.items():
            model_path = model_info["model_path"]
            model_info["model"] = AutoModelForTokenClassification.from_pretrained(model_path, local_files_only=True)
            model_info["tokenizer"] = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

    def bionerApi(self,text,model_type):
        """
        The function takes in text and a model type, selects the corresponding model and tokenizer,
        generates a pipeline for named entity recognition, and returns the outputs and tokenizer.
        
        Args:
          text: The input text that needs to be analyzed for named entities.
          model_type: The type of NER model to use, such as "bert-base-cased" or
        "distilbert-base-cased".
        
        Returns:
          a tuple containing the outputs and tokenizer.
        """
        """
        This will provide the API either through url access or
        through class

        """
        model = self.models[model_type]["model"] ## choosing the model to use and tokenizer
        tokenizer = self.models[model_type]["tokenizer"]
        self._current_tokenizer = tokenizer

        ### Pipeline generated on choosen model
        ner = pipeline(task="ner",
                       model=model,
                       tokenizer=tokenizer)
        
        outputs = ner(text)

        return outputs,tokenizer

    
    def responseProcessor(self,response):
        """
        This function processes a response by grouping outputs by position and converting tokens to
        strings.
        
        Args:
          response: The response parameter is a tuple containing two elements:
        
        Returns:
          The function `responseProcessor` returns a list of dictionaries, where each dictionary
        represents an entity found in the input text. Each dictionary contains the following keys:
        `word` (the entity text), `start` (the starting position of the entity in the input text), `end`
        (the ending position of the entity in the input text), and `entity` (the type of entity).
        """
        outputs,tokenizer = response

        results = []
        current = []
        last_idx = 0
        # make to sub group by position
        for output in outputs:
            if output["index"]-1==last_idx:
                current.append(output)
            else:
                results.append(current)
                current = [output, ]
            last_idx = output["index"]

        if len(current)>0:
            results.append(current)
        
        # from tokens to string
        strings = []
        for c in results:
            tokens = []
            starts = []
            ends = []
            for o in c:
                tokens.append(o['word'])
                starts.append(o['start'])
                ends.append(o['end'])

            new_str = tokenizer.convert_tokens_to_string(tokens)
            if new_str!='':
                strings.append(dict(
                    word=new_str,
                    start = min(starts),
                    end = max(ends),
                    entity = c[0]['entity']
                ))
        return strings
        

    def extractor(self,text,model_type):
        """
        This Python function extracts named entities from text using a specified model type and returns
        the entities as a response.
        
        :param text: The input text for which entities need to be extracted
        :param model_type: The type of NER model being used for extracting entities from the text. It
        could be a pre-trained model or a custom model trained on specific data
        :return: The method `extractor` returns the `entities` extracted from the input `text` using the
        `bionerApi` and `responseProcessor` methods.
        """
        """
        Method expose to get final response 

        """
        ner_output = self.bionerApi(text,model_type)
        entities = self.responseProcessor(ner_output)
        return entities
    

if __name__ == '__main__':
    text = """This study aimed to investigate the detoxification metabolism responses in scallop Chlamys farreri exposed to phenanthrene (PHE), chrysene (CHR), benzo[a]pyrene (B[a]P) and PHE + CHR + B[a]P for 15 days under laboratory conditions. The mRNA expression levels of AhR signaling pathway (AhR, HSP90, XAP2 and ARNT), detoxification system (phase I: CYP1A1 and CYP1B1; phase II: SULTs, UGT and GSTs) and ATP-binding cassette transporters (phase 0: ABCB1 and phase III: ABCC1, ABCG2) in digestive glands of scallops exposed to PHE (0.7, 2.1 μg/L), CHR (0.7, 2.1 μg/L), B[a]P (0.7, 2.1 μg/L), and PHE + CHR + B[a]P (0.7 + 0.7 +0.7, 2.1 + 2.1 + 2.1 μg/L) were detected. In present study, key genes (AhR, HSP90, XAP2 and ARNT) of the AhR signaling pathway can be significantly induced by pollutants, suggesting that the AhR/ARNT signaling pathway plays a role directly or indirectly. AhR, HSP90 and ARNT reached the maximum value on day 6, which can be preliminarily understood as the synchronization of their functions. Besides, the results also indicated that different genes had specific response to different pollution exposure. CYP1B1, GST-2, GST-omega and GST-microsomal could be potional indexes to PHE, ARNT, GST-sigma 2 and GST-3 were sensitive to CHR exposure, HSP90, GST-theta and ABCG2 were considered as potional indexes to BaP while CYP1A1 and UGT were possible to be indexes for monitoring the mix exposure of these three PAHs. These findings in C. farreri suggested that phase II detoxification metabolic enzymes isoforms played an essential role in detoxification mechanisms and mRNA expression levels of specific SULTs, UGTs and GSTs were potentially to be ideal indexes in PAHs pollution research. In summary, this study provides more valuable information for the risk assessments of different rings of PAHs.
            """
    bioner_api = Bioner()
    entities = bioner_api.extractor(text=text,model_type="chemicals")
    print(entities)