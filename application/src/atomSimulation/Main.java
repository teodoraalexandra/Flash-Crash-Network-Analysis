package atomSimulation;

import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.agents.*;

public class Main {
    public static void main(String[] args)
    {
        // Step 1. Create a simulation object by choosing a mono or multithreaded implementation.
        Simulation sim = new MonothreadedSimulation();

        // Step 2. Define what kind of logging you need.
        sim.setLogger(new Logger("data.csv"));

        // Step 3. Create orderbooks.
        String obName = "lvmh";
        sim.addNewOrderBook(obName);

        // Step 4. Create agents that will be used and add them to the simulation.
        // Default for ZIT: cash=0, minPrice=14k, maxPrice=15k, minQty=10, maxQty=100

        for (int day = 0; day <= 30; day++) {
            // ZIT agents: 10 - initialized in day 0
            if (day == 0) {
                for (int index = 0; index < 10; index++) {
                    sim.addNewAgent(new ZIT("ZIT" + index));
                }
            }

            // Noise agents: 7 - initialized in day 0
            if (day == 0) {
                for (int index = 0; index < 7; index++) {
                    sim.addNewAgent(new NoiseAgent("Noise" + index));
                }
            }

            // Informed agents: 10 -> We will try to simulate a crash by adding them -> Disequilibrium in market
            if (day == 1) {
                for (int index = 0; index < 10; index++) {
                    sim.addNewAgent(new InformedAgent("Overvalued_10_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, true, 10));
                }
            }

            if (day == 10) {
                for (int index = 0; index < 10; index++) {
                    sim.addNewAgent(new InformedAgent("Undervalued_15_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, false, 15));
                }
            }

            if (day == 15) {
                for (int index = 0; index < 3; index++) {
                    sim.addNewAgent(new ZIT("New_ZIT" + index));
                    sim.addNewAgent(new NoiseAgent("New_Noise" + index));
                }
            }

            if (day == 25) {
                for (int index = 0; index < 10; index++) {
                    sim.addNewAgent(new InformedAgent("Overvalued_20_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, true, 20));
                }
            }

            // Step 5. Launch the simulation with a specification of the structure of trading day
            // (defaults are provided for EuroNEXT) and the number of days to simulate.
            // Simulation on min 30 days
            sim.run(Day.createEuroNEXT(1, 1, 1), 1);
        }
        sim.market.printState();

        // For project:
        // Bipartivity,
        // Assortativity,
        // Spectral bipartivity,
        // Clustering,
        // Community detection
    }
}