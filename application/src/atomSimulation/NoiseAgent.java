package atomSimulation;

import java.util.Random;

import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Noise agents have no private information and simply trade based on random fluctuations in prices
class NoiseAgent extends Agent {
    public NoiseAgent(String name) {
        super(name);
    }

    //  a. Decide randomly whether to submit a buy or sell order
    //  b. Submit the order with a random size
    public Order decide(String obName, Day day) {
        // Noise traders usually submit orders at the current market price
        // They don't have any information about the true value of the security
        Random random = new Random();
        int randomQuantity = random.nextInt(1000 + 1 - 10) + 10;
        if (random.nextBoolean()) {
            market.log.info("Sending an ASK order [tick="+day.currentTick()+"]");
            return new MarketOrder(obName, this.name, LimitOrder.BID, randomQuantity);
        }
        market.log.info("Sending a BID order [tick="+day.currentTick()+"]");
        return new MarketOrder(obName, this.name, LimitOrder.BID, randomQuantity);
    }
}