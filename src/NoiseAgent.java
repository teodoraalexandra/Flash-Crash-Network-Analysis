import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Noise agents have no private information and simply trade based on random fluctuations in prices
class NoiseAgent extends Agent {
    protected long minPrice;
    protected long maxPrice;
    protected int minQuty;
    protected int maxQuty;

    public NoiseAgent(String name) {
        super(name, 0L);
        this.minPrice = 14500L;
        this.maxPrice = 15000L;
        this.minQuty = 10;
        this.maxQuty = 100;
    }

    public Order decide(String obName, Day day) {
        double n = Math.random();

        char dir = (char) (n > 0.5 ? 66 : 65);
        int quty = this.minQuty + (int) (Math.random() * (double) (this.maxQuty - this.minQuty));

        long lowestPrice = 14000L;
        long highestPrice = 15000L;

        if (day.dayNumber > 30) {
            long extraDayClosePrice = this.market.orderBooks.get(obName).extradayLog.get(day.dayNumber - 2).CLOSE;
            long extraDayLowestPrice = this.market.orderBooks.get(obName).extradayLog.get(day.dayNumber - 2).LOW;
            long extraDayHighestPrice = this.market.orderBooks.get(obName).extradayLog.get(day.dayNumber - 2).HIGH;
        }

        long price = lowestPrice + (long) ((int) (Math.random() * (double) (highestPrice - lowestPrice)));

        return new LimitOrder(obName, "" + this.myId, dir, quty, price);
    }
}
