import java.util.Random;
import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

class MarketMaker extends Agent {
    protected int INITIAL_PRICE;

    public MarketMaker(String name, long cash, int INITIAL_PRICE) {
        super(name, cash);
        this.INITIAL_PRICE = INITIAL_PRICE;
    }

    private int calculateOrderQuantity(double price) {
        return Math.max(1, (int) (this.cash / price)); // Place orders based on available cash
    }

    private double calculatePotentialLoss(double bidPrice, double askPrice) {
        int inventory = this.getInvest("lvmh");
        // Calculate order quantity based on available inventory and order type (bid or ask)
        int orderQuantity = calculateOrderQuantity(bidPrice);

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

        double spread = 0.005 * lastPrice;
        long bidPrice = (long) (lastPrice - (spread / 2));
        long askPrice = (long) (lastPrice + (spread / 2));

        // Check the inventory levels
        int currentInventory = this.getInvest("lvmh");
        int maxInventory = (int) (0.5 * this.cash / lastPrice); // max x% of cash in inventory

        // Adjust prices if inventory exceeds max level
        if (currentInventory > maxInventory) {
            // Increase the spread and adjust bid price to be lower
            spread *= 2; // Increase spread
            bidPrice = (long) (lastPrice - (spread / 2));
            askPrice = (long) (lastPrice + (spread / 2));
        } else if (currentInventory < -maxInventory) {
            // Decrease the spread to encourage inventory buildup
            spread /= 2; // Decrease spread
            bidPrice = (long) (lastPrice - (spread / 2));
            askPrice = (long) (lastPrice + (spread / 2));
        }

        // Evaluate potential risk before placing orders
        double potentialLoss = calculatePotentialLoss(bidPrice, askPrice);
        double maxAcceptableLoss = 0.02 * this.getWealth();

        // Check if placing orders exceeds the maximum acceptable loss threshold
        if (potentialLoss > maxAcceptableLoss) {
            return null;
        }

        // Randomly choose between placing bid ('A') or ask ('B') order
        char orderType;
        if (currentInventory > maxInventory / 2) {
            orderType = 'B'; // More inclined to place ask orders to reduce inventory
        } else if (currentInventory < -maxInventory / 2) {
            orderType = 'A'; // More inclined to place bid orders to increase inventory
        } else {
            orderType = (new Random().nextBoolean() ? 'A' : 'B');
        }

        if (orderType == 'A') {
            // Place a bid order
            return new LimitOrder(obName, "" + this.myId, 'A', calculateOrderQuantity(bidPrice), bidPrice);
        } else {
            // Place an ask order
            return new LimitOrder(obName, "" + this.myId, 'B', calculateOrderQuantity(askPrice), askPrice);
        }
    }
}
