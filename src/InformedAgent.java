import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected int minQuty;
    protected int maxQuty;
    protected int aggressivity;

    protected double volatility;
    protected double[] prices;

    public InformedAgent(String name, int aggressivity, double[] prices, double volatility, int minQuty, int maxQuty) {
        super(name, 0L);
        this.minQuty = minQuty;
        this.maxQuty = maxQuty;
        this.aggressivity = aggressivity;
        this.volatility = volatility; // The standard deviation of returns (sigma)
        this.prices = prices;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber >= 30 && day.dayNumber <= 31) {
            int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));
            char dir = 'A';

            // Price lower than the min market price
            // They believe that the security is overvalued
            // They want to sell it at a lower price than the min market price

            long minPrice = (long) (prices[day.dayNumber - 1] - 2 * this.volatility * prices[day.dayNumber - 1]);
            long maxPrice = (long) (prices[day.dayNumber - 1] + 2 * this.volatility * prices[day.dayNumber - 1]);

            minPrice = minPrice - ((this.aggressivity * minPrice) / 100);
            maxPrice = maxPrice - ((this.aggressivity * maxPrice) / 100);

            long price = minPrice + (long) ((int) (Math.random() * (double) (maxPrice - minPrice)));

            return new LimitOrder(obName, "" + this.myId, dir, quty, price);
        }
        return null;
    }
}