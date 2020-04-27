import random
import cv2
import numpy as np
import copy

######          constants        ######

pointsNumber = 5
mutationRate = 0.5


changeColorMutationRate = 0.6
movePointMutationRate = 0.7
changeLayerMutationRate = 0.5
moveOnePointMutationRate = 0.4
crossingoverMutationRate = 0.6
parentsRatio = 0.8
populationSize = 40
parentsNumber = 20
genesNumber = 10
layersNumber = genesNumber

######      end of constants     ######


######      constants that change during execution     ######
deviationPercentage = 0.45
h=16
w=16
background_image = np.zeros((h, w, 3), np.uint8)
background_image.fill(128)

# background_image = cv2.resize(cv2.imread("Hand1423.png"),(w,h))

######                        end                      ######





######                 reading source image            ######

srcFileName = "grade.png"
initialSrcIm = cv2.imread(srcFileName)
if initialSrcIm is None:
    exit("Could not read the image.")
dimensions = (h, w)
srcIm = cv2.resize(initialSrcIm, dimensions)


# to save the resulted image
bestIm = np.zeros((h, w, 3), np.uint8)

# def readSourceImage():
#     srcIm = cv2.cvtColor(cv2.imread(srcFileName), cv2.COLOR_RGB2BGR)
#     if srcIm is None:
#         exit("Could not read the image.")
#     dimensions = (h, w)
#     srcIm = cv2.resize(srcIm, dimensions)
#     return srcIm

def main():
    global srcIm
    global h
    global w
    global populationSize
    global initialSrcIm
    global genesNumber
    population = createPopulation()
    lastBestFitChange = 0
    fitRate = population[0][1]
    generation =0
    while(w!=1024 and h!=1024):
        cv2.imshow('source', srcIm)
        cv2.waitKey(1000)
        while (generation-lastBestFitChange<100):
            print("generation {} fitrate {}".format(generation,fitRate))
            population = evolve(population)
            if (fitRate>population[0][1]):
                fitRate = population[0][1]
                lastBestFitChange = generation
                bestIm = getImage(population[0].copy())
                currentIm = getImage(population[0].copy())
                #cv2.imwrite('current.png', currentIm)
                cv2.imshow('current',currentIm)
                cv2.waitKey(1000)
            if (generation-lastBestFitChange>40):
                new_population = createPopulation()
                population[int(populationSize/2):] = copy.deepcopy(new_population[int(populationSize/2):])
            generation+=1
        cv2.imwrite("grade"+str(generation)+".png",currentIm)
        global background_image
        background_image = cv2.resize(getImage(population[0].copy()),(w*2,h*2))
        global deviationPercentage
        deviationPercentage = deviationPercentage*0.85
        h = h*2
        w = w*2
        srcIm = cv2.resize(initialSrcIm, (w,h))
        genesNumber = int(genesNumber*1.2)
        population = copy.deepcopy(createPopulation())
        lastBestFitChange = generation
        fitRate = population[0][1]

    bestIm = cv2.resize(bestIm, (1024,1024))
    bestIm = cv2.resize(bestIm,(512, 512))
    cv2.imwrite("grade"+str(generation)+".png",bestIm)


def createPopulation():
    population = [[[[createPoints(),
                     tuple([random.randint(0, 255) for k in range(3)]), random.randint(0, layersNumber)] for j in
                    range(genesNumber)], 0.0] for i in
                  range(populationSize)]
    #draw every species in population
    for osob in range(populationSize):
        genes = population[osob][0]
        dna_pic = copy.deepcopy(background_image)

        genes.sort(key=lambda x: x[2])

        for gene in genes:
            pts = np.array(gene[0], np.int32).copy()
            pts = pts.reshape((-1, 1, 2))

            cv2.fillConvexPoly(dna_pic, pts, gene[1])

        # calculate fit rate
        fitRate = calculateFitRate(dna_pic)
        population[osob][1] = fitRate

    return population


#create points for polygon in some range (so that a polygon will not be too big and take the whole image)
def createPoints():
    points = []
    points+=[(random.randint(0,w),random.randint(0,h))]
    xmin = max(0,points[0][0]-w*deviationPercentage)
    xmax = min(w,points[0][0]+w*deviationPercentage)
    ymin = max(0,points[0][1]-h*deviationPercentage)
    ymax = min(h,points[0][1]+h*deviationPercentage)
    for i in range(pointsNumber-1):
        points+=[(random.uniform(xmin,xmax),random.uniform(ymin,ymax))]
    return (points)


#get image from a DNA
def getImage(dna):
    dna_pic = copy.deepcopy(background_image)

    # draw polys

    dna[0].sort(key=lambda x: x[2])

    for dna_gene in dna[0]:
        pts = np.array(dna_gene[0], np.int32).copy()
        pts = pts.reshape((-1, 1, 2))

        cv2.fillConvexPoly(dna_pic, pts, dna_gene[1])

    return dna_pic

def chooseParents(population):
    parents = []
    parents += population[:int(parentsNumber * parentsRatio)].copy()
    parents += population[populationSize - (parentsNumber - int(parentsNumber * parentsRatio)):].copy()
    return parents

def crossingover(parents):
    children_genes = []

    for p1_i in range(parentsNumber):
        for p2_i in range(p1_i + 1, parentsNumber):

            child_1_genes = copy.deepcopy(parents[p1_i][0])
            child_2_genes = copy.deepcopy(parents[p2_i][0])

            for gene in range(genesNumber):
                if(random.random()<crossingoverMutationRate):

                    child_1_genes[gene], child_2_genes[gene] = child_2_genes[gene], child_1_genes[gene]

            children_genes += [child_1_genes, child_2_genes]

    return copy.deepcopy(children_genes)

def mutate(children_genes):

    for child_genes in children_genes:
        for gene in child_genes:
            if random.random() < mutationRate:

                if random.random() < changeColorMutationRate:
                    gene[1] = tuple([random.randint(0, 255) for component in range(3)])

                for dot in gene[0]:
                    if random.random() < movePointMutationRate:
                        dot = (random.randint(0, w), random.randint(0, h))

                if random.random() < changeLayerMutationRate:
                    gene[2] = random.randint(0, layersNumber)

    return children_genes


def constructDnaFromGenes(children_genes):
    children = []
    for child_genes in children_genes:
        # calculate fit rates
        dna_pic = copy.deepcopy(background_image)

        # draw polys

        child_genes.sort(key=lambda x: x[2])

        for gene in child_genes:
            pts = np.array(gene[0], np.int32).copy()
            pts = pts.reshape((-1, 1, 2))

            cv2.fillConvexPoly(dna_pic, pts, gene[1])

        # calculate fit rate
        current_fit_rate = calculateFitRate(dna_pic)
        children.append([child_genes, current_fit_rate])
    return children

def calculateFitRate(img):
    fit_rate = np.sum((cv2.resize(img, (h,w)).astype("float") - srcIm.astype("float")) ** 2)
    return fit_rate

def evolve(population):

    population.sort(key=lambda x: x[1])
    population = population[:populationSize]

    parents = chooseParents(copy.deepcopy(population))

    # crossingover
    children_genes = crossingover(copy.deepcopy(parents))

    # mutation (only children)
    children_genes = mutate(copy.deepcopy(children_genes))

    # create children dna from genes
    children = constructDnaFromGenes(copy.deepcopy(children_genes))

    # update population (add children to population)
    population += children

    return population


main()