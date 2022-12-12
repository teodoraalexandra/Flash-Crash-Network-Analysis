package atomSimulation;

import atomSimulation.MyAgent;
import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.agents.*;

public class Main {
    public static void main(String[] args)
    {
        Simulation sim = new MonothreadedSimulation();
        //sim.market.logType = MarketPlace.LONG; // or SHORT

        sim.setLogger(new Logger(System.out));

        String obName = "lvmh";
        sim.addNewOrderBook(obName);
        // sim.addNewMicrostructure(new OrderBook(obName)); // same as previous

        sim.addNewAgent(new ZIT("paul")); // cash, default terminals

        // sim.addNewAgent(new ZIT("paul",10000)); // default terminal
        sim.addNewAgent(new MyAgent("pierre", 0, 1000));
        // sim.addNewAgent(new ZIT("paul",0,10000,20000,10,50, new double[]{0.25 , 0.25}, 1.0));

        sim.run(Day.createEuroNEXT(0, 1000, 0), 1);
        // sim.run(Day.createSinglePeriod(MarketPlace.FIX, 1000));

        sim.market.printState();
    }
}