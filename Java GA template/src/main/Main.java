package main;

import AI.Population;

/**
 * Created by Nicola on 6/16/2017.
 */
public class Main {
    final static String target = "Test sentence";
    final static int populationDimension = 500;
    final static double mutationRate = 0.01;

    public static void main(String[] args) {
        int i = 0;
        double e, s;
        //Population lifecycle
        Population p = new Population(mutationRate, populationDimension, target);
        p.initPopulation();

        s = System.currentTimeMillis();
        while (true) {
            //TODO definitely not the best way!
            try {
                System.out.print("Generation: " + ++i + "\t");
                String result = p.naturalSelection();


                if (result != null) {
                    break;
                }
            } catch (ClassCastException ex) {
                //TODO that catch!
                break;
            }
        }
        e = System.currentTimeMillis();
        System.out.println("Execution time: " + (e - s)/1000 + " seconds" + "\tgenerations: " + i);
    }
}
