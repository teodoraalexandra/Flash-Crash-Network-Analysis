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

    public static void main(String[] args) {
        // Pre-requisite: Initialize the parameters
        int NUMBER_OF_PERSONS = Integer.parseInt(args[0]);
        double PERCENTAGE_OF_INFORMED = Double.parseDouble(args[1]);
        int AGGRESSIVITY = Integer.parseInt(args[2]);
        int DAYS_OF_SIMULATION = Integer.parseInt(args[3]);
        int SIMULATION_INDEX = Integer.parseInt(args[4]);

        double VOLATILITY =  0.003;
        double alpha = 3.5;   // Value of alpha for power law distribution - the wealth disparity within the society.
        // The lower the alpha, the bigger the discrepancy between the cash

        // Crash length (24 = 8h ; 6-9: 2-3h crash)
        int PRICES_BY_DAY = 2;
        int INITIAL_PRICE = 14500;
        double INITIAL_UNCERTAINTY_UNINFORMED = 50;
        double INITIAL_UNCERTAINTY_INFORMED = 0;

        int MULTIPLY_INFORMED = 200; // Has enough cash for at least 200 stocks

        int INFORMED_TRADERS = (int) Math.round((PERCENTAGE_OF_INFORMED / 100) * NUMBER_OF_PERSONS);
        int UNINFORMED_TRADERS = NUMBER_OF_PERSONS - INFORMED_TRADERS;

        // Step 1. Create a simulation object by choosing a mono or multithreaded implementation.
        Simulation sim = new MonothreadedSimulation();

        // Step 2. Define what kind of logging you need.
        sim.setLogger(new Logger("csvs/data" + SIMULATION_INDEX + ".csv"));
        // Step 3. Create orderbooks.
        String obName = "lvmh";
        sim.addNewOrderBook(obName);

        // Step 4. Create agents that will be used and add them to the simulation.
        // Default for ZIT: cash=0, minPrice=14k, maxPrice=15k, minQty=10, maxQty=100
        // Informed agents -> We will try to simulate a crash by adding them -> Disequilibrium in market

        InformationPair[] pricesUninformed = generateBrownianMotion(INITIAL_PRICE, INITIAL_UNCERTAINTY_UNINFORMED, DAYS_OF_SIMULATION, VOLATILITY, PRICES_BY_DAY);
        InformationPair[] pricesInformed = generateBrownianMotion(INITIAL_PRICE, INITIAL_UNCERTAINTY_INFORMED, DAYS_OF_SIMULATION, 0, PRICES_BY_DAY);

        int totalTraders = UNINFORMED_TRADERS + INFORMED_TRADERS;
        long[] cashEndowments = new long[totalTraders];
        int[] assetEndowments = new int[totalTraders];

        // Generate cash and asset endowments for uninformed traders
        for (int index = 0; index < UNINFORMED_TRADERS; index++) {
            long cash = (long) generateEndowment(alpha);
            cashEndowments[index] = cash * INITIAL_PRICE;

            // Generate asset endowment for uninformed traders
            int asset = (int) generateEndowment(alpha);
            assetEndowments[index] = asset;
        }

        // Generate cash and asset endowments for informed traders
        for (int index = UNINFORMED_TRADERS; index < UNINFORMED_TRADERS + INFORMED_TRADERS; index++) {
            long cash = (long) generateEndowment(alpha);
            cashEndowments[index] = cash * INITIAL_PRICE * MULTIPLY_INFORMED;

            // Informed traders do not receive asset endowments
            int asset = (int) generateEndowment(alpha);
            assetEndowments[index] = asset * MULTIPLY_INFORMED; // Set asset endowment to 0 for informed traders
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

        // Step 5. Launch the simulation with a specification of the structure of trading day
        // (defaults are provided for EuroNEXT) and the number of days to simulate.
        sim.run(Day.createSinglePeriod(MarketPlace.CONTINUOUS, PRICES_BY_DAY), DAYS_OF_SIMULATION);
    }
}