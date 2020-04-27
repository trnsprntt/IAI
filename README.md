# Introduction to Artificial Intelligence
# Assigment II Report

Author: Olga Chernukhina
BS18-03


April 2020

Link to the code in github: https://github.com/trnsprntt/IAI

--------------

### Algorithm overview and representation

First let's draw the correspondence between genetic terms and some primitives that was used for image generation:

|Genetics primitive|Image equivalent|
|------------------|----------------|
|Population        |Set of images
|DNA (Chromosome)  |Image
|Gene              |One polygon in the image
|Allele 1          |List of points that define the polygon
|Allele 2          |(R,G,B) tuple to define polygon color
|Allele 3          |Layer number of the polygon$^*$

*$^*$ - the lower layer number, the further (at the very back) the polygon is drawn*

-----------

Here I will give the algorithm's pseudocode. I can call it a regular standart Genetic Algorithm apart from 2 things I used to improve performance:

**1) If best-fit image doesn't change for 50 or more generations:**
*  Worst half of the current population "dies"
*  Absolutely new random population is created and added instead of this "dead" half

**2) At first target picture is resized to 16x16 pixels and algorithm is running on it. When there's no change in the best-fit image during at least 100 generations**:
* It means population changes slowed down considerably *(look at p. 1 described above, even substituting the worst half of population for new species last 50!!! generations didn't help to improve)* and the algorithm reached local maximum on this image
* The best-fit resulted 16x16 image is rescaled to 32x32 pixels and used as background for the future mutations on 32x32 field
* This continues until the image doesn't reach required 512x512 pixels

Reasons are described in *"Image manipulation techniques"* paragraph.

---------
**Algorithm pseudocode**
```python 3.7
set initial dimensions to (16,16)
read Source Image
create initial population

while dimensions!=(512,512):
    apply natural selection to the population based on fit-rate calculation
    choose parents from population
    apply crossingover to parents
    apply mutations to children
    add children to the population
    
    if new_best-fit_rate < best-fit_rate:
        update best-fit picture
        
    if best-fit picture was updated more than 50 generations ago:
        create new population
        substitute worst half of the current population to 
            new population species
            
    if best-fit picture was updated more than 100 generations ago:
        resize best-fit image to (dimensions*2)
        set background to be resized best-fit image
        update dimensions to dimensions*2
        create new population for new dimensioned image
```
    
### Selection mechanism

Since I gave much probability and power to mutations and availability to substitute half of the population in case the algorithm "stucks" in evolution, selection mechanism stayed as simple as possible - **select DNAs with the best fit rate**. Easy and still very effective.

##### Parents selection mechanism
I have a constant called ```parentsRatio``` which for this particular example equals to $80\%\text{~}0.8$. This means that 80% of parents are taken from the first half of the population, which is sorted in decreasing order. The rest 20% are taken randomly from the second half of the population to add variety to the features.   
    
### Fitness function

Error rate is calculated by square deviation betveen each component (R,G,B) for every corresponding pixel in source and samle images.

$Error Rate = \sum_{x,y=0}^{x,y \rightarrow width,heigth} \Big(  sampleImage.pixel[x,y](R,G,B)-sourceImage.pixel[x,y] (R,G,B)\Big)^2$

Hence, the less *Error Rate*, the more successful the DNA.

Adiing squares allows to react even to minor quality changes in a DNA 


### Crossover function

I control Crossover Rate by the variable ```crossoverMutationRate``` *(a float from 0 to 1)*.

This is how it works:
1) Two parent DNAs are taken, say $P1$ and $P2$
2) For every gene in these DNAs the following function is calculated:
    * $random.uniform(0,1)<crossoverMutationRate$
3) If it returns true, the corresponding genes are swapped

*Note: I also tried changing genes from different places. It takes more time and doesn't give more valuable results*


### Mutation criteria

At first it is useful to introduce possible mutations:
* Change polygon's color
* Every point of the polygon could be randomly moved independently of others

These mutations were controlled by ```changeColorMutationRate``` and ```movePointMutationRate``` correspondingly. Both $\subset [0;1]$

The mechanism is pretty same to the one described above:
- If $random.uniform(0,1)<changeColorMutationRate$ returns true, a polygon changes its color to random. 


*Important note: when creating the population, I limited points of the same polygon not to be spreaded on more than ```deviationRate``` fraction of image. Second mutation allowed polygons to overcome this limitation to diversify population.*


### Image manipulation techniques
As it was partially described above, I artificially corrupted the image, spoiled its resolution and then smoothly increased the quality back to the original.

The image manipulation algorithm in a few words:
- The image is resized initially to $16 \times 16$ pixels, for simplic say $N \times N$
- Repeat until $N \times N$ is not equal to $ 512 \times 512$ 
    - The algorithm approximates $N \times N$ image
    - When there's no progress in last 100 generations
        * This $N\times N$ image is resized to $2N\times2N$
        * It is set to be background for the future approximations
        * The source picture is also resized to $2N\times2N$
    - The algorithm approximates $2N\times2N$ in the same manner


    

This is extremely useful from the performance point of view since 
1) At first iterations the algorithm determines basic image colors, which is simple and fast
2) Using these colors in the background decrease overall 
$Error Rate$ 
3) Having base structure of the picture set, the algorithm is allowed to care about smaller shades and shapes
4) Every next resized generation results in more and more detailed output ~~(Agile in practice)~~


### Some thoughts about the philosophy of art

For all kinds of design tasks (logos,presentations, etc) I usually use the same app called "Canva.com". Every time you save something there appears a window with an art-related quote of some extremely famous guy. Here is an example (I apologise for Russian)

![](https://i.imgur.com/pbPSzTo.png)
Over the years I unintentionally processed hundreds of thoughts most of which were capable of commemorating a whole art streaming or at least some crucial decade. The problem is, often these widely-recognised artists support completely conflicting thesises. Samuel Butler believes that the sinews of art and literature, like those of war, are money, when at the same time Seneca says "All art is but imitation of nature". However, reading between the lines reveals that all of these are just different paths to one destination - "Art is anything that causes anyone feel something". Even if only a single person in the world would ever take a peek at your work and even if the only though that would appear in his/her mind is "oh what a disaster", you will know you have done something valuable. 

So, even if my algorithm produces pictures that are far far away from being "an excellent example of genetic algorithm's work", they already "caused" sincere people's emotions. I have sent a generated picture to my close friend to her birthday. She was more than happy (and no matter she didn't even understand at first it was a photo of hers :) I believe that her smile converted a suspicious-too-much-abstract-looking-image into a piece of art.  

### Images examples

The bithday girl :)

![](https://i.imgur.com/DaUnGhB.png) ![](https://i.imgur.com/FMZZ0Ku.png) ![](https://i.imgur.com/jRaHIY5.png) ![](https://i.imgur.com/pmMyirx.png) ![](https://i.imgur.com/Br8zWre.png) ![](https://i.imgur.com/VLURSEs.jpg)

-------------
Just flying Mario

![](https://i.imgur.com/aT4wyZY.png) ![](https://i.imgur.com/AEjNE2k.png) ![](https://i.imgur.com/5M5n1R8.png) ![](https://i.imgur.com/ibOKv3m.png) ![](https://i.imgur.com/qKg41tp.png) ![](https://i.imgur.com/een0CWl.png)

--------------
My grade for this assignment (just a joke:)

![](https://i.imgur.com/myMVnLI.png) ![](https://i.imgur.com/6Q7suy9.png) ![](https://i.imgur.com/Q8Lj0ZM.png) ![](https://i.imgur.com/31HpvU5.jpg) ![](https://i.imgur.com/1AGtc6j.jpg) ![](https://i.imgur.com/0O8V3pa.png)

--------------
Ex boyfriend (sorry for another bad joke)
Here i tried to use transparency instead of layers

![](https://i.imgur.com/sVN4hzH.png) ![](https://i.imgur.com/UxRl5oJ.png) ![](https://i.imgur.com/QKeDPXN.jpg) ![](https://i.imgur.com/VCzl2GG.jpg) ![](https://i.imgur.com/ZQ9F51O.jpg) ![](https://i.imgur.com/CPlafkM.png)




--------------
Violet hand


![](https://i.imgur.com/11CFeRA.png) ![](https://i.imgur.com/sPIHxln.png) ![](https://i.imgur.com/Uzab2qx.png) ![](https://i.imgur.com/odxXyJK.jpg) ![](https://i.imgur.com/38zFgfj.jpg) ![](https://i.imgur.com/FwylP6w.jpg)




### Analysis
I understood that increasing the size of image twice takes much more than twice a time to reach the same error rate. Increasing the number of genes results in similar complications. This is because the algorithm should process much much more genes combinations.

To achieve the best possible precision at the given time I should have splitted the picture into several smaller pieces and run the algorithm separately on every part.

But for me the main purpose was not reproducing the exact image, but to design something new, that would not be the same at the first glance, therefore I decided to use polygons and not split the image.

### Final words

For me it was the hardest and still the most interesting assignment among all 4 semesters. 

At first I wrote the whole algorithm and classes implementation on C++, but got into huge troubles with graphical library 'glut'. Then I decided to move to python, but it worked extremely slowly with classes.  Finally, for the third time I implemented the algorithm on python without classes using only primitive structures. 

Seeing the algorithm step by step producing something that is similar to the original picture in terms of colors literally from absolutely random figures and colors is extremely astonishing. 






