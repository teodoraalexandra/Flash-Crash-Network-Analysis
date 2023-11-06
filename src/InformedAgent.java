import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected int minQuty;
    protected int maxQuty;
    protected int aggressivity;

    protected double volatility;
    protected int[] prices;
    protected int pricesByDay;

    public InformedAgent(String name, int aggressivity, int[] prices, double volatility, int minQuty, int maxQuty, int pricesByDay) {
        super(name, 0L);
        this.minQuty = minQuty;
        this.maxQuty = maxQuty;
        this.aggressivity = aggressivity;
        this.volatility = volatility; // The standard deviation of returns (sigma)
        this.prices = prices;
        this.pricesByDay = pricesByDay;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber >= 30 && day.dayNumber <= 31) {
            int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));
            char dir = 'A';

            // Price lower than the min market price
            // They believe that the security is overvalued
            // They want to sell it at a lower price than the min market price

            // PRICE_PER_DAY * (dayNumber - 1) + tick - 1
            int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
            long minPrice = (long) (prices[priceIndex] - 2 * this.volatility * prices[priceIndex]);
            long maxPrice = (long) (prices[priceIndex] + 2 * this.volatility * prices[priceIndex]);

            minPrice = minPrice - ((this.aggressivity * minPrice) / 100);
            maxPrice = maxPrice - ((this.aggressivity * maxPrice) / 100);

            long price = minPrice + (long) ((int) (Math.random() * (double) (maxPrice - minPrice)));

            return new LimitOrder(obName, "" + this.myId, dir, quty, price);
        }
        return null;
    }
}