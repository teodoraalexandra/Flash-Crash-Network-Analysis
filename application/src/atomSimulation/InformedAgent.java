package atomSimulation;

import java.util.Random;

import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    long lastPriceOfDay;
    boolean isOvervalued;
    int percentage;
    public InformedAgent(String name, long lastPriceOfDay, boolean isOvervalued, int percentage) {
        super(name);
        this.lastPriceOfDay = lastPriceOfDay;
        this.isOvervalued = isOvervalued;
        this.percentage = percentage;
    }

    // a. Generate private information about the true value of the security
    // b. Based on the private information and the current market price, decide whether to submit a buy or sell order
    // c. Submit the order with a random size
    public Order decide(String obName, Day day) {
        Random random = new Random();
        int randomQuantity = random.nextInt(1000 + 1 - 10) + 10;
        if (this.isOvervalued) {
            market.log.info("Sending an ASK order [tick="+day.currentTick()+"]");
            // Price lower than the current market price
            // They believe that the security is overvalued
            // They want to sell it at a lower price than the current market price
            long informedPrice = this.lastPriceOfDay - ((this.percentage * this.lastPriceOfDay) / 100);
            if (informedPrice <= 0 || this.lastPriceOfDay == -1) {
                return new MarketOrder(obName, this.name, LimitOrder.ASK, randomQuantity);
            } else {
                return new LimitOrder(obName, this.name, LimitOrder.ASK, randomQuantity, informedPrice);
            }
        }
        market.log.info("Sending a BID order [tick="+day.currentTick()+"]");
        // Price higher than the current market price
        // They believe that the security is undervalued
        // They want to buy it at a higher price than the current market price
        long informedPrice = this.lastPriceOfDay + ((this.percentage * this.lastPriceOfDay) / 100);
        if (informedPrice <= 0 || this.lastPriceOfDay == -1) {
            return new MarketOrder(obName, this.name, LimitOrder.BID, randomQuantity);
        } else {
            return new LimitOrder(obName, this.name, LimitOrder.BID, randomQuantity, informedPrice);
        }
    }
}