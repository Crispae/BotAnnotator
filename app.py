from flask import Flask,json,jsonify,render_template,request


### Importing NERs classes
from NER.Abner import Abner
from NER.Bern2 import Bern2
from NER.Bioner import Bioner
from NER.Huner import Huner
from NER.Reach import Reach
from NER.Bern2server import Bern2server

app = Flask(__name__)

### Instansiating classes
abner = Abner()
### this can be processed either through direct source or by API
bern2 = Bern2() ## Need to put huner in docker as well
bioner = Bioner()
bern2server = Bern2server()
reach = Reach()
huner = Huner() ## HunerWeird loading, it loads the model multiple times and brea
## in middle and researt the server, better to use docker image of Huner server

@app.route("/annotate",methods=["POST","GET"])
def annotate():
    if request.method == "POST":

        ## getting request in json format
        json_data = request.get_json()
        input_text = str(json_data["text"])
        model_type = int(json_data["type"]) ## Extracting model type
        print(model_type)

        if model_type == 2: ## FOR Rule NER

            print("processing through reach")

            ##### Rule Based NER ######
            Rule_extracted_entites = reach(input_text)
            return [Rule_extracted_entites,input_text]

        elif model_type == 3: ### For LSTM
            print("Processing through LSTM-CRF model")

            lstm_extracted_entites = huner(input_text)

            lstm_processed = lstm_extracted_entites[0]
            returned_text = lstm_extracted_entites[1]

            return [lstm_processed,returned_text]

        elif model_type == 4: ### For BERN
            print("Processing through BERN2 model")

            ##### BIO-LM Based NER ######
            Bern_extracted_entites = bern2(input_text)
            return [Bern_extracted_entites,input_text]
        
        elif model_type == 5: ### for ABNER
            print("Processing through ABNER model")

            ##### ABNER NER ######
            Abner_extracted_entites = abner(input_text)
            return [Abner_extracted_entites,input_text]
        
        elif model_type == 6: ### bern2 server
            print("Processing through BERN2 server")

            bern2_extracted_entites = bern2server(input_text)
            return [bern2_extracted_entites,input_text]


        elif model_type == 1:

            print("processing through BERT")
            #### Transformer Based NER #####
            # 
            #### for chemicals
            extracted_chemicals = bioner(text=input_text,model_type="chemical")

            #### for disease
            extracted_disease = bioner(text=input_text,model_type="disease")

            #### for gene
            extracted_genes = bioner(text=input_text,model_type="gene")


            return [extracted_chemicals,extracted_disease,extracted_genes,input_text,]
    
    if request.method == "GET":
          return "<p> GET recieved </p>"



if __name__ == '__main__':
    app.run(debug=True)