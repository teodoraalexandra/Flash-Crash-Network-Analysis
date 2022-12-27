package masonSimulation;

import sim.engine.SimState;
import sim.engine.Steppable;
import sim.field.continuous.Continuous2D;
import sim.util.Double2D;

public class Market extends SimState {
    // Define the dimensions of the market environment
    public static final double WIDTH = 100;
    public static final double HEIGHT = 100;

    // Define the starting stock price
    public static final double INITIAL_PRICE = 100;

    // Define the number of agents in the market
    public static final int NUM_AGENTS = 100;

    // Define the agents in the market
    public Agent[] agents;

    // Define the market environment
    public Continuous2D environment;

    // Define the stock price
    public double stockPrice;

    // Initialize the market
    public Market(long seed) {
        super(seed);
    }

    // Initialize the agents and environment
    public void start() {
        super.start();

        // Create the agents
        agents = new Agent[NUM_AGENTS];
        for (int i = 1; i <= NUM_AGENTS; i++) {
            agents[i] = new Agent("Name" + i, i * 100, i * 20);
        }

        // Create the market environment
        environment = new Continuous2D(WIDTH, HEIGHT, WIDTH);

        // Set the initial stock price
        stockPrice = INITIAL_PRICE;

        // Add the agents to the environment
//        for (Agent agent : agents) {
//            environment.setObjectLocation(agent, new Double2D(random.nextDouble() * WIDTH, random.nextDouble() * HEIGHT),
//
//                    // Schedule the agents to trade with each other
//                    schedule.scheduleRepeating(new Steppable() {
//                        public void step(SimState state) {
//                            // Select two agents at random
//                            Agent a = agents[random.nextInt(NUM_AGENTS)];
//                            Agent b = agents[random.nextInt(NUM_AGENTS)];
//
//                            // Allow the agents to trade with each other
//                            a.trade(b, stockPrice);
//                        }
//                    });
//
//            // Schedule the market environment to update the stock price
//            schedule.scheduleRepeating(new Steppable() {
//                public void step(SimState state) {
//                    // Update the stock price based on the agents' trading behavior
//                    // For example, the price could increase if more agents are buying than selling,
//                    // or decrease if more agents are selling than buying
//                    stockPrice = stockPrice * 1.2;
//                }
//            });
//        }
    }
}