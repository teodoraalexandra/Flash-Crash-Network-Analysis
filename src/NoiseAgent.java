import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

// Noise agents have no private information and simply trade based on random fluctuations in prices
class NoiseAgent extends Agent {
    protected InformationPair[] prices;
    protected int pricesByDay;

    protected double toleranceLevel; // 1-100 as a percentage of tolerance (probability to enter a risky transaction)

    public NoiseAgent(String name, long cash, InformationPair[] prices, int pricesByDay, double toleranceLevel) {
        super(name, cash);
        this.prices = prices;
        this.pricesByDay = pricesByDay;
        this.toleranceLevel = toleranceLevel;
    }

    public Order decide(String obName, Day day) {
        int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
        long realFundamentalValue = this.prices[priceIndex].fundamentalValue;
        double realValuationUncertainty = this.prices[priceIndex].valuationUncertainty;

        long realPrice = this.market.orderBooks.get("lvmh").lastFixedPrice != null ?
                this.market.orderBooks.get("lvmh").lastFixedPrice.price :
                realFundamentalValue;

        double lowestValuationInterval = realFundamentalValue - realValuationUncertainty / 2;
        double highestValuationInterval = realFundamentalValue + realValuationUncertainty / 2;

        long wealth = this.getWealth();
        double randomPercentage = (50 + (Math.random() * 75)) / 100;

        // (2) Given its actual cash or stock, randomly decide about the volume of the order,
        // by investing a random percentage of the actual wealth
        long howMuchMoneyShouldBeInvested = (long) (randomPercentage * wealth);
        int quantityDesiredToBeInvested = (int) (howMuchMoneyShouldBeInvested / realPrice);

        // (3) Select a random price in the valuation interval
        long price = (long) (lowestValuationInterval + (Math.random() * (highestValuationInterval - lowestValuationInterval)));

        if (quantityDesiredToBeInvested > 0) {
            double n = Math.random();
            char dir = (n > 0.5 ? 'B' : 'A');
            return new LimitOrder(obName, "" + this.myId, dir, quantityDesiredToBeInvested, price);
        }
        return null;
    }
}
