import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected int minQuty;
    protected int maxQuty;
    int percentage;

    public InformedAgent(String name, int percentage) {
        super(name, 0L);
        this.minQuty = 10;
        this.maxQuty = 100;
        this.percentage = percentage;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber >= 30 && day.dayNumber <= 40) {
            char dir = 65;
            int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));

            long highestPrice = 15000L;
            long closePrice = this.market.orderBooks.get(obName).extradayLog.get(day.dayNumber -2).CLOSE;

            // Price lower than the min market price
            // They believe that the security is overvalued
            // They want to sell it at a lower price than the min market price

//            long min = lowestPrice - ((this.percentage * lowestPrice) / 100);
//            long max = highestPrice - ((this.percentage * highestPrice) / 100);
//            long price = min + (long) ((int) (Math.random() * (double) (max - min)));
//            long price = this.minPrice - ((this.percentage * this.minPrice) / 100);

            return new MarketOrder(obName, "" + this.myId, dir, quty);

            // NOT YET IMPLEMENTED. Case where the information is undervalued
            // Price higher than the max market price
            // They believe that the security is undervalued
            // They want to buy it at a higher price than the max market price
        }
        return null;
    }
}