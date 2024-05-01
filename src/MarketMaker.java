import java.util.Random;
import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

class MarketMaker extends Agent {
    protected double spread; // Spread between bid and ask prices
    protected double maxAcceptableLoss; // Maximum acceptable loss threshold
    protected int INITIAL_PRICE;

    public MarketMaker(String name, long cash, double spread, double maxAcceptableLoss, int INITIAL_PRICE) {
        super(name, cash);
        this.spread = spread;
        this.maxAcceptableLoss = maxAcceptableLoss;
        this.INITIAL_PRICE = INITIAL_PRICE;
    }

    private int calculateOrderQuantity(double price) {
        return Math.max(1, (int) (this.cash / price)); // Place orders based on available cash
    }

    private double calculatePotentialLoss(double bidPrice, double askPrice) {
        int inventory = this.getInvest("lvmh");

        // Calculate order quantity based on available inventory and order type (bid or ask)
        int orderQuantity = calculateOrderQuantity(bidPrice); // Use the same quantity for bid and ask for simplicity

        // Calculate potential loss based on the impact of executing orders against current inventory
        double potentialLoss;

        if (inventory >= orderQuantity) {
            // If inventory is sufficient to cover the order quantity, calculate loss based on executed quantity
            potentialLoss = Math.abs((bidPrice - askPrice) * orderQuantity);
        } else {
            // If inventory is insufficient to cover the full order quantity, calculate loss based on remaining inventory
            potentialLoss = Math.abs((bidPrice - askPrice) * inventory);
        }

        return potentialLoss;
    }

    public Order decide(String obName, Day day) {
        // Calculate bid and ask prices based on market conditions
        long lastPrice = this.market.orderBooks.get("lvmh").lastFixedPrice != null ?
                this.market.orderBooks.get("lvmh").lastFixedPrice.price :
                this.INITIAL_PRICE;
        long bidPrice = (long) (lastPrice - (this.spread / 2));
        long askPrice = (long) (lastPrice + (this.spread / 2));

        // Evaluate potential risk before placing orders
        double potentialLoss = calculatePotentialLoss(bidPrice, askPrice);

        // Check if placing orders exceeds the maximum acceptable loss threshold
        if (potentialLoss > maxAcceptableLoss) {
            return null;
        }

        // Randomly choose between placing bid ('A') or ask ('B') order
        char orderType = (new Random().nextBoolean() ? 'A' : 'B');

        if (orderType == 'A') {
            // Place a bid order
            return new LimitOrder(obName, "" + this.myId, 'A', calculateOrderQuantity(bidPrice), bidPrice);
        } else {
            // Place an ask order
            return new LimitOrder(obName, "" + this.myId, 'B', calculateOrderQuantity(askPrice), askPrice);
        }
    }
}
