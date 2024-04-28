import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;
import java.util.Random;

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

    public boolean willEnterTransaction() {
        Random random = new Random();
        double randomNumber = random.nextDouble(); // Generate a random number between 0.0 (inclusive) and 1.0 (exclusive)
        return (randomNumber <= this.toleranceLevel); // Return true if random number is less than or equal to tolerance level
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

        if (realPrice >= highestValuationInterval || realPrice <= lowestValuationInterval) {
            // CASE: Outside the interval
            // (1) Decide the SELL or BUY by going in the opposite direction towards the last public valuation
            char direction = this.market.orderBooks.get("lvmh").lastFixedPrice.dir;
            char oppositeDirection = direction == 'B' ? 'A' : 'B';

            // (2) If it has enough cash or stock for the selected operation, decides
            // about the traded volume by investing a given percentage of his wealth
            long howMuchMoneyShouldBeInvested = (long) (randomPercentage * wealth);
            int quantityDesiredToBeInvested = (int) (howMuchMoneyShouldBeInvested / realPrice);

            return new MarketOrder(obName, "" + this.myId, oppositeDirection, quantityDesiredToBeInvested);
        }

        // CASE: Inside the interval
        // (1) Given the tolerance level, decide to enter the market by randomly selecting a SELL or BUY operation
        if (willEnterTransaction()) {
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
        return null;
    }
}
