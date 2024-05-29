import java.util.Random;
import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

class MarketMaker extends Agent {
    protected int INITIAL_PRICE;

    public MarketMaker(String name, long cash, int INITIAL_PRICE) {
        super(name, cash);
        this.INITIAL_PRICE = INITIAL_PRICE;
    }

    private int calculateOrderQuantity(double price, int currentInventory, int maxInventory) {
        int baseQuantity = (int) (0.5 * this.cash / price); // Base quantity as x% of cash divided by price

        // Adjust base quantity based on inventory levels
        if (currentInventory > maxInventory) {
            baseQuantity /= 1.1; // Reduce order size if inventory is high
        } else if (currentInventory < -maxInventory) {
            baseQuantity *= 1.1; // Increase order size if inventory is low
        }

        // Ensure order quantity is at least 1
        return Math.max(1, baseQuantity);
    }

    private double calculatePotentialLoss(double bidPrice, double askPrice) {
        double expectedValue = (bidPrice + askPrice) / 2.0;
        return Math.abs(expectedValue - bidPrice) + Math.abs(expectedValue - askPrice);
    }

    public Order decide(String obName, Day day) {
        // Calculate bid and ask prices based on market conditions
        long lastPrice = this.market.orderBooks.get("lvmh").lastFixedPrice != null ?
                this.market.orderBooks.get("lvmh").lastFixedPrice.price :
                this.INITIAL_PRICE;
        // Determine the sensitivity parameter lambda
//        double lambda = 0.5;
//
//        long totalOrderFlow = this.market.orderBooks.get(obName).numberOfOrdersReceived;
//        long newPrice = (long) (lastPrice + lambda * totalOrderFlow);
//
        double spread = 0.05 * lastPrice;
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
        double maxAcceptableLoss = 0.1 * this.cash;

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
            return new LimitOrder(obName, "" + this.myId, 'A', calculateOrderQuantity(bidPrice, currentInventory, maxInventory), bidPrice);
        } else {
            // Place an ask order
            return new LimitOrder(obName, "" + this.myId, 'B', calculateOrderQuantity(askPrice, currentInventory, maxInventory), askPrice);
        }
    }
}
