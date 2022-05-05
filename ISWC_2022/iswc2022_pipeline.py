# coding=utf-8
# ICSW_20022 - pipeline
import getopt
import os
import logging
import subprocess
import sys
import nltk


from PrototypeM1 import Prototype
from TransformerM1 import Transformer
from UtilityScripts import launchRecommender_sh, launchUpdate

def main():
    nltk.download('punkt')
    args = sys.argv[1:]
    print(f"Arguments count: {len(sys.argv)}")

    fileInputJsonPost = str(sys.argv[1])
    os.system('rm ./ISWC2022_pipeline_log.log')
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('./ISWC2022_pipeline_log.log')
    logger.setLevel(logging.DEBUG)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info('Start ICSW_2022 pipeline')

    # Module 1
    #   - Generation of prototypes prototype.py
    #   - To run the generation of the lemmatized description file: python3 transformer.py

    logger.info('STEP 1: [STARTING] Module 1:  Prototype')

    prototypeM1 = Prototype("Prototype")

    # prototypeM1.__init__()
    prototypeM1.runPrototypes(logger, fileInputJsonPost)    

    # transformer.py
    logger.info('STEP 1: [STARTING] Module 1:  Transformer')
    transformerM1 = Transformer("Transformer")
    transformerM1.runTransformer(logger, fileInputJsonPost)

    retval = os.getcwd()

    logger.info('STEP 2: [CHANGE-DIR] - Sistema di raccomandazione/Classificatore/')
    command = './Launch_Recommender.sh ../prototipi_6'
    # step 4: Launch Launch_Recommender.sh ../prototipi_6 english
    logger.info('STEP 3: [EXECUTE] ./Launch_Recommender.sh ../prototipi_6')
    os.system(command)

    os.chdir('../../')
    retval = os.getcwd()
    print('Directory changed successfully: ' + str(retval))

    # step 5: Launch java -jar update.jar
    # loading RDF triple for reasoning and recommendation
    logger.info('STEP 4: Loading RDF triple for reasoning and recommendation')

    os.chdir('Sistema di raccomandazione/Classificatore/')
    retval = os.getcwd()
    # commandJar = 'java -jar update.jar'

    logger.info('Directory changed successfully: ' + str(retval))
    # commandJar = 'java -jar update.jar'
    logger.info('java -jar update.jar')
    try:
        #  cp = subprocess.call(['java', '-jar', 'update.jar'], universal_newlines=True, stdout=subprocess.PIPE,
                             # stderr=subprocess.PIPE)
        logger.info('STEP 5: [SUCCESSFULLY] java -jar update.jar')
        # cp2 = subprocess.call(['java', '-jar', 'DagaUpdate.jar'], universal_newlines=True, stdout=subprocess.PIPE,
                            # stderr=subprocess.PIPE)
       # logger.info('STEP 6: [SUCCESSFULLY] java -jar DagaUpdate.jar')
    except:
        logger.info('STEP 5: [ERROR] java -jar update.jar')
        # logger.info('STEP 6: [ERROR] java -jar DagaUpdate.jar')

    # subprocess.call(['java', '-jar', 'update.jar'], shell=False)
    # logger.info('STEP 5: [EXECUTE] Launch java -jar update.jar')

if __name__ == "__main__":
    main()
