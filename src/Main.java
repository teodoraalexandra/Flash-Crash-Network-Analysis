import fr.cristal.smac.atom.*;
import java.util.Random;

public class Main {

    public static double[] generateBrownianMotion(double initialPrice, int nbSessions, double volatility, int pricesByDay) {
        double[] prices = new double[nbSessions * pricesByDay];
        prices[0] = initialPrice;
        java.util.Random random = new Random(0);
        for (int i = 1; i < nbSessions * pricesByDay; i++) {
            prices[i] = prices[i - 1] + prices[i - 1] * random.nextGaussian() * volatility;
        }
        return prices;
    }

    public static void main(String[] args) {
        // Pre-requisite: Initialize the parameters
        int NUMBER_OF_PERSONS = Integer.parseInt(args[0]);
        double PERCENTAGE_OF_INFORMED = Double.parseDouble(args[1]);
        int AGGRESSIVITY = Integer.parseInt(args[2]);
        int DAYS_OF_SIMULATION = Integer.parseInt(args[3]);
        int SIMULATION_INDEX = Integer.parseInt(args[4]);

        double VOLATILITY =  0.003;
        int PRICES_BY_DAY = 1;
        long INITIAL_PRICE = 14500L;

        int MIN_QTY_UNINFORMED = 1;
        int MAX_QTY_UNINFORMED = 10;
        int MIN_QTY_INFORMED = 20;
        int MAX_QTY_INFORMED = 500;

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

        double[] prices = generateBrownianMotion(INITIAL_PRICE, DAYS_OF_SIMULATION, VOLATILITY, PRICES_BY_DAY);

        for (int index = 1; index <= UNINFORMED_TRADERS; index++) {
            sim.addNewAgent(new NoiseAgent("Noise" + index, prices, VOLATILITY, MIN_QTY_UNINFORMED, MAX_QTY_UNINFORMED));
        }

        for (int index = 1; index <= INFORMED_TRADERS; index++) {
            sim.addNewAgent(new InformedAgent("Overvalued" + index, AGGRESSIVITY, prices, VOLATILITY, MIN_QTY_INFORMED, MAX_QTY_INFORMED));
        }

        // Step 5. Launch the simulation with a specification of the structure of trading day
        // (defaults are provided for EuroNEXT) and the number of days to simulate.
        sim.run(Day.createEuroNEXT(10, 200, 5), DAYS_OF_SIMULATION);
    }
}