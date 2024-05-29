import fr.cristal.smac.atom.*;
import java.util.Random;

public class Main {

    public static InformationPair[] generateBrownianMotion(long initialPrice, double initialUncertainty, int daysOfSimulation, double volatility, int pricesByDay) {
        InformationPair[] informationPairs = new InformationPair[daysOfSimulation * pricesByDay];
        informationPairs[0] = new InformationPair(initialPrice, initialUncertainty);
        java.util.Random random = new Random(0);
        for (int i = 1; i < daysOfSimulation * pricesByDay; i++) {
            int computedFundamentalValue = (int) Math.ceil(informationPairs[i - 1].fundamentalValue + informationPairs[i - 1].fundamentalValue * random.nextGaussian() * volatility);
            int computedValuationUncertainty = (int) Math.ceil(informationPairs[i - 1].valuationUncertainty + informationPairs[i - 1].valuationUncertainty * random.nextGaussian() * volatility);
            informationPairs[i] = new InformationPair(computedFundamentalValue, computedValuationUncertainty);
        }
        return informationPairs;
    }

    // Function to generate endowment following power law distribution
    private static double generateEndowment(double alpha) {
        Random random = new Random();
        double u = random.nextDouble(); // Generate a random number between 0 and 1
        return 1.0 / Math.pow(u, 1.0 / (alpha - 1.0));
    }

    // Function to generate a random number from a uniform distribution within [min, max]
    private static double generateUniform(double min, double max) {
        Random random = new Random();
        return min + (max - min) * random.nextDouble();
    }

    public static void main(String[] args) {
        // Pre-requisite: Initialize the parameters
        int NUMBER_OF_PERSONS = Integer.parseInt(args[0]);
        double PERCENTAGE_OF_INFORMED = Double.parseDouble(args[1]);
        int AGGRESSIVITY = Integer.parseInt(args[2]);
        int DAYS_OF_SIMULATION = Integer.parseInt(args[3]);
        int SIMULATION_INDEX = Integer.parseInt(args[4]);

        double VOLATILITY =  0.003;

        // Value of alpha for power law distribution - the wealth disparity within the society.
        // The lower the alpha, the bigger the discrepancy between the cash
        double alpha = 3;

        // Crash length (24 = 8h ; 6-9: 2-3h crash)
        int PRICES_BY_DAY = 2;
        int INITIAL_PRICE = 15000;
        double INITIAL_UNCERTAINTY_UNINFORMED = 0.1 * INITIAL_PRICE;
        double INITIAL_UNCERTAINTY_INFORMED = 0.01 * INITIAL_PRICE;

        int INFORMED_TRADERS = (int) Math.round((PERCENTAGE_OF_INFORMED / 100) * NUMBER_OF_PERSONS);
        int MARKET_MAKERS = (int) Math.round((PERCENTAGE_OF_INFORMED * 2 / 100) * NUMBER_OF_PERSONS);
        int UNINFORMED_TRADERS = NUMBER_OF_PERSONS - INFORMED_TRADERS - MARKET_MAKERS;

        Simulation sim = new MonothreadedSimulation();
        sim.setLogger(new Logger("csvs/data" + SIMULATION_INDEX + ".csv"));
        String obName = "lvmh";
        sim.addNewOrderBook(obName);

        InformationPair[] pricesUninformed = generateBrownianMotion(INITIAL_PRICE, INITIAL_UNCERTAINTY_UNINFORMED, DAYS_OF_SIMULATION, VOLATILITY, PRICES_BY_DAY);
        InformationPair[] pricesInformed = generateBrownianMotion(INITIAL_PRICE, INITIAL_UNCERTAINTY_INFORMED, DAYS_OF_SIMULATION, VOLATILITY, PRICES_BY_DAY);

        int totalTraders = UNINFORMED_TRADERS + INFORMED_TRADERS + MARKET_MAKERS;
        long[] cashEndowments = new long[totalTraders];
        int[] assetEndowments = new int[totalTraders];

        // Generate cash and asset endowments for uninformed traders
        for (int index = 0; index < UNINFORMED_TRADERS; index++) {
            long cash = (long) generateEndowment(alpha);
            cashEndowments[index] = cash * INITIAL_PRICE;

            int asset = (int) generateEndowment(alpha);
            assetEndowments[index] = asset;
        }

        // Generate cash and asset endowments for informed traders
        for (int index = UNINFORMED_TRADERS; index < UNINFORMED_TRADERS + INFORMED_TRADERS; index++) {
            long cash = (long) generateUniform(50, 200);
            cashEndowments[index] = cash * INITIAL_PRICE ;

            int asset = (int) generateUniform(50, 200);
            assetEndowments[index] = asset;
        }

        // Generate cash and asset endowments for market makers
        for (int index = UNINFORMED_TRADERS + INFORMED_TRADERS; index < totalTraders; index++) {
            long cash = (long) generateUniform(1, 25);
            cashEndowments[index] = cash * INITIAL_PRICE ;

            int asset = (int) generateUniform(1, 25);
            assetEndowments[index] = asset;
        }

        for (int index = 0; index < UNINFORMED_TRADERS; index++) {
            Random random = new Random();
            double toleranceLevel = random.nextDouble();
            NoiseAgent noiseAgent = new NoiseAgent("Noise" + index, cashEndowments[index], pricesUninformed, PRICES_BY_DAY, toleranceLevel);
            noiseAgent.setInvest(obName, assetEndowments[index]);
            sim.addNewAgent(noiseAgent);
        }

        for (int index = UNINFORMED_TRADERS; index < UNINFORMED_TRADERS + INFORMED_TRADERS; index++) {
            InformedAgent informedAgent = new InformedAgent("Overvalued" + index, cashEndowments[index], AGGRESSIVITY, pricesInformed, PRICES_BY_DAY);
            informedAgent.setInvest(obName, assetEndowments[index]);
            sim.addNewAgent(informedAgent);
        }

        for (int index = UNINFORMED_TRADERS + INFORMED_TRADERS; index < totalTraders; index++) {
            MarketMaker marketMaker = new MarketMaker("MM" + index, cashEndowments[index], INITIAL_PRICE);
            marketMaker.setInvest(obName, assetEndowments[index]);
            sim.addNewAgent(marketMaker);
        }

        sim.run(Day.createSinglePeriod(MarketPlace.CONTINUOUS, PRICES_BY_DAY), DAYS_OF_SIMULATION);
    }
}