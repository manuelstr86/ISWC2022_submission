import os
import subprocess

'''
Launch_Recommender.sh in prototipi


#Bash script to run DENOTER's Recommender
#on all combined concepts prototypes

#syntax: ./Launch_Recommender [folder]*
#							  *optional


#load prototype files' names from parameter folder
#(default folder is ../prototipi)

folder=${1:-../prototipi}
prototypes=( `ls ${folder}` )

#clears resume files
rm recommendations.tsv
rm resume.tsv

#runs Recommender on each prototype
for (( i = 0 ; i < ${#prototypes[@]} ; i += 1 )) ; do
    python3 Recommender.py ${folder}/${prototypes[$i]}
done

python3 count.py

'''


def launchRecommender_sh(logger):
    # clears resume files
    logger.info('clears resume files')
    logger.info('rm recommendations.tsv')
    logger.info('rm resume.tsv')
    pathDir = 'Sistema di raccomandazione/Classificatore/prototipi_it_6'
    os.chdir(pathDir)
    retval = os.getcwd()
    print('Directory changed successfully 2 ' + str(retval))

    start_path = pathDir  # current directory
    arr = os.listdir()
    print(arr)
    for filename in arr:
        print("filename : " + str(filename))
        cmd = 'python3 ../Recommender.py ' + str(filename)
        os.system(cmd)

    os.chdir('Sistema di raccomandazione/Classificatore/')
    # step 4: Launch Launch_Recommender.sh ../prototipi_it
    # rm recommendations.tsv
    # rm resume.tsv
    os.system('python count.py')
    logger.info('Change directory: Sistema di raccomandazione/Classificatore')

    # script count.py
    lista = []
    logger.info('OPEN - Sistema di raccomandazione/Classificatore/recommendations.tsv')
    with open("recommendations.tsv", "r") as resFile:
        for line in resFile:
            artwork = str(line.split("\t")[0])
            if artwork not in lista:
                lista.append(artwork)

    i = len(lista)
    print("\n\nOVERALL\n" + str(i) + " artworks involved by recommendation\n")
    logger.info('\n\nOVERALL\n' + str(i) + ' artworks involved by recommendation\n')


def launchUpdate(logger):
    # step 5: Launch java -jar update.jar
    logger.info('STEP 5: Launch java -jar update.jar')
    # loading RDF triple for reasoning and recommendation

    os.chdir('Sistema di raccomandazione/Classificatore/')
    logger.info('Change directory: Sistema di raccomandazione/Classificatore/')
    retval = os.getcwd()
    print('Directory changed successfully: ' + str(retval))
    logger.info('Directory changed successfully ' + str(retval))
    # commandJar = 'java -jar update.jar'
    logger.info('java -jar update.jar')
    #p = subprocess.call(['java', '-jar', 'update.jar'], shell=True,stdout=subprocess.PIPE)
    try:
        cp = subprocess.call(['java', '-jar', 'update.jar'], universal_newlines=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        logger.info('STEP 5: [SUCCESSFULLY] java -jar update.jar')
    except FileNotFoundError as e:
        logger.info('STEP 5: [ERROR] java -jar update.jar: ' + str(e))
        # [Errno 2] No such file or directory: 'xxxx'
