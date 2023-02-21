package atomSimulation;

import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected long minPrice;
    protected long maxPrice;
    protected int minQuty;
    protected int maxQuty;
    int percentage;

    public InformedAgent(String name, int percentage) {
        super(name, 0L);
        this.minPrice = 14000L;
        this.maxPrice = 15000L;
        this.minQuty = 10;
        this.maxQuty = 100;
        this.percentage = percentage;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber > 30) {
            double n = Math.random();

            char dir = (char) (n > 0.5 ? 66 : 65);
            int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));

            // Price lower than the min market price
            // They believe that the security is overvalued
            // They want to sell it at a lower price than the min market price
            long price = this.minPrice - ((this.percentage * this.minPrice) / 100);
            return new LimitOrder(obName, "" + this.myId, dir, quty, price);

            // NOT YET IMPLEMENTED. Case where the information is undervalued
            // Price higher than the max market price
            // They believe that the security is undervalued
            // They want to buy it at a higher price than the max market price
        }
        return null;
    }
}