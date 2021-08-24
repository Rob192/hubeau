from show_results import *
import pandas as pd
from termcolor import colored
from pprintpp import pprint
from flair.models import SequenceTagger
import stanza
# stanza.download('fr') # run once
def main():
    MODEL_PATH = "NER_tool/stacked-standard-flair-150-wikiner.pt"
    nb_mesures = None

    flair_model = SequenceTagger.load(MODEL_PATH)
    nlp = stanza.Pipeline(lang='fr', processors='tokenize,mwt,pos,lemma,depparse', logging_level="FATAL")
    heideltime_parser = Heideltime()
    ##################################################################################

    # Reading dataset of all location names
    communes_ = pd.read_csv("demonyms/Data/locations/commune2021.csv", encoding='utf-8')["LIBELLE"].tolist()
    departements_ = pd.read_csv("demonyms/Data/locations/departement2021.csv", encoding='utf-8')["LIBELLE"].tolist()
    regions_ = pd.read_csv("demonyms/Data/locations/region2021.csv", encoding='utf-8')["LIBELLE"].tolist()
    all_locations = list(map(replace, np.unique(np.concatenate((communes_, departements_, regions_)))))

    # Reading the dictionnary of demonyms
    demonym_dict = {"communes": json.load(open("demonyms/Data/final/gentiles_merged_reversed_stemmed.json")),
                    "departements": json.load(open("demonyms/Data/deps_stemmed_reversed.json"))}

    # Getting user's IP adress
    with requests.get("https://geolocation-db.com/json") as url:
        data = json.loads(url.text)
        ip_address = data["IPv4"]

    ## User Query
    query = "Y'a-t-il de l'eau dans le sous-sol à 03635X0545/PZ1 ?"
    # a_file.write(query)
    # a_file.write("\n")
    ####################################################################################################################
    final_result = show_results(query, flair_model, nlp, heideltime_parser, nb_mesures, all_locations, demonym_dict,
                                ip_address)
    for text, elem in final_result.items():

        if text == "tables":
            for tb in elem:
                print(tb["table"])
        else:
            print(colored(text, "red"))
            print()
            print(elem)

if __name__ == "__main__":
    main()
