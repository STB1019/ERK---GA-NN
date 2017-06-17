package util;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by Nicola on 6/16/2017.
 */
public class RandomUtil {
    public static int min_maxBoundedInt(int min, int max) {
        return ThreadLocalRandom.current().nextInt(min, max + 1);
    }

    public static char randomChar() {
        return (char) min_maxBoundedInt(32, 122);
    }

    public static String randomString(int length) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append(randomChar());
        }
        return sb.toString();
    }

    //TODO consider improving this algorithm
    public static boolean extractWithRate(double rate){
        rate *= 100;
        ArrayList<Integer> l = new ArrayList();

        //Fill arrays
        for(int i = 0; i<100 - rate; i++) l.add(0);
        for(int i = 0; i<rate; i++) l.add(1);
        return (l.get(min_maxBoundedInt(0, l.size()-1)) == 1) ? true : false;
    }
}
