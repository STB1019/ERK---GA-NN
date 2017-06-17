package AI;

import util.RandomUtil;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Nicola on 6/16/2017.
 */
public class Population {
    private ArrayList<DNA> population = new ArrayList();
    private double mutationRate;
    private int maxPopulation;
    private String target;

    // Population class constructor
    public Population(double mutationRate, int maxPopulation, String target) {
        this.mutationRate = mutationRate;
        this.maxPopulation = maxPopulation;
        this.target = target;
    }

    //Initialize random population
    public void initPopulation() {
        for (int i = 0; i < maxPopulation; i++)
            this.getPopulation().add(new DNA(RandomUtil.randomString(target.length())));
    }

    //Perform natural selection on the population: members
    //with higher fitness score have higher probability of
    //being select for reproduction
    public String naturalSelection() {
        HashMap<DNA, Integer> fitnessScores = calcPopulationFitness(this.target);
        if (fitnessScores.size() == 1) return (String) fitnessScores.keySet().toArray()[0];
        ArrayList<DNA> matingPool = matingPool(fitnessScores);
        ArrayList<DNA> newGeneration = new ArrayList<>();

        //Selection and reproduction
        for (int i = 0; i < maxPopulation; i++) {
            newGeneration.add(reproduce(
                    matingPool.get(RandomUtil.min_maxBoundedInt(0, matingPool.size() - 1)),
                    matingPool.get(RandomUtil.min_maxBoundedInt(0, matingPool.size() - 1))));
        }

        //Replace population
        this.population.clear();
        this.setPopulation(newGeneration);
        return null;
    }

    // Calculate fitness for each member in the given population
    public HashMap<DNA, Integer> calcPopulationFitness(String target) {
        HashMap<DNA, Integer> fitnessValues = new HashMap<>();
        int maxFitnessScore = 0;
        DNA maxDNAfitnessScore = null;

        for (int i = 0; i < maxPopulation; i++) {
            DNA indexDNA = this.getPopulation().get(i);
            int indexFitness = calcIndividualFitness(indexDNA, target);

            if (indexFitness > maxFitnessScore) {
                maxFitnessScore = indexFitness;
                maxDNAfitnessScore = indexDNA;
            }

            //If optimal solution is found then return a single element -> this situation will be treated
            //in the calling method
            if (maxFitnessScore == target.length()) {
                fitnessValues.clear();
                fitnessValues.put(indexDNA, indexFitness);
                break;
            }
            fitnessValues.put(indexDNA, indexFitness);
        }

        //DEBUG
        System.out.println("max fitness: " + maxDNAfitnessScore.getGenes() + " score: " + maxFitnessScore);
        return fitnessValues;
    }

    // Evaluate every single fitness score for each member in the population
    // In this case fitness score is incremented if the n-th gene (in this case the n-th letter)
    // corresponds to the n-th character of the target string
    public int calcIndividualFitness(DNA dna, String target) {
        int fitnessScore = 0;
        String genes = dna.getGenes();

        for (int i = 0; i < target.length(); i++)
            if (genes.charAt(i) == target.charAt(i))
                fitnessScore++;

        return fitnessScore;
    }

    //Create a mating pool selecting a couple of DNAs from the population,
    // evaluating each of them with their fitness score
    public ArrayList<DNA> matingPool(HashMap<DNA, Integer> fitnessScores) {
        ArrayList<DNA> poll = new ArrayList<>();

        for (DNA indexDNA : fitnessScores.keySet())
            for (int i = 0; i < fitnessScores.get(indexDNA); i++)
                poll.add(indexDNA);

        return poll;
    }

    //Create a new DNA given the 2 parents' DNAs
    //taking 50% genetic information from each one + consider
    //mutation rate
    public DNA reproduce(DNA p1, DNA p2) {
        StringBuilder sb = new StringBuilder();
        sb.append(p1.getGenes().substring(0, p1.getGenes().length() / 2));
        sb.append(p2.getGenes().substring(p2.getGenes().length() / 2, p2.getGenes().length()));

        //perform mutation
        char[] child = new char[sb.length()];
        sb.getChars(0, sb.length(), child, 0);

        for (int i = 0; i < sb.length(); i++)
            if (RandomUtil.extractWithRate(this.getMutationRate()))
                child[i] = RandomUtil.randomChar();

        return new DNA(new String(child));
    }

    //Getters and setters
    public double getMutationRate() {
        return mutationRate;
    }

    public void setMutationRate(double mutationRate) {
        this.mutationRate = mutationRate;
    }

    public int getMaxPopulation() {
        return maxPopulation;
    }

    public void setMaxPopulation(int maxPopulation) {
        this.maxPopulation = maxPopulation;
    }

    public ArrayList<DNA> getPopulation() {
        return this.population;
    }

    public void setPopulation(ArrayList<DNA> population) {
        this.population = population;
    }
}
