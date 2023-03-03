package atomSimulation;

import fr.cristal.smac.atom.*;

public class Main {
    public static void main(String[] args)
    {
        // Pre-requisite: Initialize the parameters
        int NUMBER_OF_PERSONS = Integer.parseInt(args[0]);
        double PERCENTAGE_OF_INFORMED = Double.parseDouble(args[1]);
        int AGGRESSIVITY = Integer.parseInt(args[2]);
        int DAYS_OF_SIMULATION = Integer.parseInt(args[3]);
        int SIMULATION_INDEX = Integer.parseInt(args[4]);

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

        for (int index = 1; index <= UNINFORMED_TRADERS; index++) {
            sim.addNewAgent(new NoiseAgent("Noise" + index));
        }

        for (int index = 1; index <= INFORMED_TRADERS; index++) {
            sim.addNewAgent(new InformedAgent("Overvalued" + index, AGGRESSIVITY));
        }

        // Step 5. Launch the simulation with a specification of the structure of trading day
        // (defaults are provided for EuroNEXT) and the number of days to simulate.
        // System.out.println("Simulation running...");
        long start = System.currentTimeMillis();
        sim.run(Day.createEuroNEXT(10, 200, 5), DAYS_OF_SIMULATION);
        long end = System.currentTimeMillis();
        float sec = (end - start) / 1000F;
        // sim.market.printState();
        // System.out.println("Finished in " + sec + " seconds.\n");
    }
}