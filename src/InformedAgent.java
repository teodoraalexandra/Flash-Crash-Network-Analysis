import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    public static int InformedTransactions;
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
        if (day.dayNumber >= 15 && day.dayNumber <= 17) {
            int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
            long realFundamentalValue = this.prices[priceIndex].fundamentalValue;
            double realValuationUncertainty = this.prices[priceIndex].valuationUncertainty;

            double lowestValuationInterval = realFundamentalValue - realValuationUncertainty / 2;
            double highestValuationInterval = realFundamentalValue + realValuationUncertainty / 2;

            long realPrice = this.market.orderBooks.get("lvmh").lastFixedPrice != null ?
                    this.market.orderBooks.get("lvmh").lastFixedPrice.price :
                    realFundamentalValue;

            if (realPrice >= highestValuationInterval) {
                // CASE: Outside the upper interval
                // (1) Decide the SELL
                char direction = 'A';

                // (2) SELL all the owned assets
                int numberOfAssets = this.getInvest("lvmh");

                // (3) Desired price
                long desiredPrice = (long) (highestValuationInterval - ((this.aggressivity * highestValuationInterval) / 100));

                if (numberOfAssets > 0) {
                    InformedTransactions += 1;
                    return new LimitOrder(obName, "" + this.myId, direction, numberOfAssets, desiredPrice);
                }
            }

            if (realPrice <= lowestValuationInterval) {
                // CASE: Outside the lower interval
                // (1) Decide the BUY
                char direction = 'B';

                // (2) BUY with available cash
                long wealth = this.getWealth();
                int quantityDesiredToBeInvested = (int) (wealth / realPrice);

                // (3) Desired price
                long desiredPrice = (long) (lowestValuationInterval + ((this.aggressivity * lowestValuationInterval) / 100));

                if (quantityDesiredToBeInvested > 0 && wealth > 0) {
                    InformedTransactions += 1;
                    return new LimitOrder(obName, "" + this.myId, direction, quantityDesiredToBeInvested, desiredPrice);
                }
            }

            return null;
        }
        return null;
    }
}