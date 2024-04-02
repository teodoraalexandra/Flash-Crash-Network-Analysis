import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Noise agents have no private information and simply trade based on random fluctuations in prices
class NoiseAgent extends Agent {
    protected int minQuty;
    protected int maxQuty;
    protected double volatility;
    protected int[] prices;
    protected int pricesByDay;

    public NoiseAgent(String name, int[] prices, double volatility, int minQuty, int maxQuty, int pricesByDay) {
        super(name, 0L);
        this.minQuty = minQuty;
        this.maxQuty = maxQuty;
        this.volatility= volatility; // The standard deviation of returns (sigma)
        this.prices = prices;
        this.pricesByDay = pricesByDay;
    }

    public Order decide(String obName, Day day) {
        double n = Math.random();

        char dir = (n > 0.5 ? 'B' : 'A');
        int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));

        // PRICE_PER_DAY * (dayNumber - 1) + tick - 1
        int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
        long minPrice = (long) (prices[priceIndex] - 2 * this.volatility * prices[priceIndex]);
        long maxPrice = (long) (prices[priceIndex] + 2 * this.volatility * prices[priceIndex]);

        long price = minPrice + (long)((int)(Math.random() * (double)(maxPrice - minPrice)));
        return new LimitOrder(obName, "" + this.myId, dir, quty, price);
    }
}
