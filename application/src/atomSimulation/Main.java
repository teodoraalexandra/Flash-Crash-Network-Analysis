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
        // Informed agents -> We will try to simulate a crash by adding them -> Disequilibrium in market

        for (int day = 0; day <= 100; day++) {
            if (day == 0) {
                for (int index = 0; index < 30; index++) {
                    sim.addNewAgent(new ZIT("ZIT1" + index));
                }
            }

            if (day == 10) {
                for (int index = 0; index < 40; index++) {
                    sim.addNewAgent(new InformedAgent("Overvalued_10_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, true, 10));
                }
            }

            if (day == 15) {
                for (int index = 0; index < 25; index++) {
                    sim.addNewAgent(new ZIT("ZIT2" + index));
                }
            }

            if (day == 30) {
                for (int index = 0; index < 20; index++) {
                    sim.addNewAgent(new InformedAgent("Undervalued_15_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, false, 15));
                }
            }

            if (day == 50) {
                for (int index = 0; index < 25; index++) {
                    sim.addNewAgent(new ZIT("ZIT3" + index));
                }
            }

            if (day == 60) {
                for (int index = 0; index < 40; index++) {
                    sim.addNewAgent(new InformedAgent("Overvalued_20_" + index, sim.market.orderBooks.get("lvmh").highestPriceOfDay, true, 20));
                }
            }

            // Step 5. Launch the simulation with a specification of the structure of trading day
            // (defaults are provided for EuroNEXT) and the number of days to simulate.
            // Simulation on min 30 days
            sim.run(Day.createEuroNEXT(1, 1, 1), 1);
        }
        sim.market.printState();
    }
}