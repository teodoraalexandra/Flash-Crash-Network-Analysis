import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected int aggressivity;

    protected InformationPair[] prices;
    protected int pricesByDay;

    public InformedAgent(String name, long cash, int aggressivity, InformationPair[] prices, int pricesByDay) {
        super(name, cash);
        this.aggressivity = aggressivity;
        this.prices = prices;
        this.pricesByDay = pricesByDay;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber >= 15 && day.dayNumber <= 16) {
            int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
            long realFundamentalValue = this.prices[priceIndex].fundamentalValue;
            double realValuationUncertainty = this.prices[priceIndex].valuationUncertainty;

            double highestValuationInterval = realFundamentalValue + realValuationUncertainty / 2;

            // Always decide to SELL
            char direction = 'A';

            // SELL all owned assets
            int numberOfAssets = this.getInvest("lvmh");

            // Target price for the order
            long desiredPrice = (long) (highestValuationInterval - ((this.aggressivity * highestValuationInterval) / 100));

            if (numberOfAssets > 0) {
                return new LimitOrder(obName, "" + this.myId, direction, numberOfAssets, desiredPrice);
            }

            return null;
        }
        return null;
    }
}