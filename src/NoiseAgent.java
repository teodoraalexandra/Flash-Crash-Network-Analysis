import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Useful for last price: this.market.orderBooks.get(obName).extradayLog.get(day.dayNumber - 1).LOW

// Noise agents have no private information and simply trade based on random fluctuations in prices
class NoiseAgent extends Agent {
    protected int minQuty;
    protected int maxQuty;
    protected double volatility;
    protected double[] prices;

    public NoiseAgent(String name, double[] prices, double volatility, int minQuty, int maxQuty) {
        super(name, 0L);
        this.minQuty = minQuty;
        this.maxQuty = maxQuty;
        this.volatility= volatility; // The standard deviation of returns (sigma)
        this.prices = prices;
    }

    public Order decide(String obName, Day day) {
        double n = Math.random();

        char dir = (n > 0.5 ? 'B' : 'A');
        int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));

        long minPrice = (long) (prices[day.dayNumber - 1] - 2 * this.volatility * prices[day.dayNumber - 1]);
        long maxPrice = (long) (prices[day.dayNumber - 1] + 2 * this.volatility * prices[day.dayNumber - 1]);

        long price = minPrice + (long)((int)(Math.random() * (double)(maxPrice - minPrice)));
        return new LimitOrder(obName, "" + this.myId, dir, quty, price);
    }
}
