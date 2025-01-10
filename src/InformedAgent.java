import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

class InformationDiffusion {
    private final double diffusionCoefficient; // D
    private final double anomalousExponent;    // α

    public InformationDiffusion(double diffusionCoefficient, double anomalousExponent) {
        this.diffusionCoefficient = diffusionCoefficient;
        this.anomalousExponent = anomalousExponent;
    }

    /**
     * Calculates the information level at a given time t.
     * @param time Current time step (or tick).
     * @return Information level.
     */
    public double calculateInformationLevel(double time) {
        return diffusionCoefficient * Math.pow(time, anomalousExponent);
    }
}

// Informed agents have private information about the true value of the security
class InformedAgent extends Agent {
    protected int aggressivity;
    private final InformationDiffusion diffusionModel; // Diffusion model

    protected InformationPair[] prices;
    protected int pricesByDay;

    public InformedAgent(String name, long cash, int aggressivity, InformationDiffusion diffusionModel, InformationPair[] prices, int pricesByDay) {
        super(name, cash);
        this.aggressivity = aggressivity;
        this.diffusionModel = diffusionModel;
        this.prices = prices;
        this.pricesByDay = pricesByDay;
    }

    public Order decide(String obName, Day day) {
        if (day.dayNumber >= 15) {
            int priceIndex = this.pricesByDay * (day.dayNumber - 1) + day.currentPeriod().currentTick() - 1;
            long realFundamentalValue = this.prices[priceIndex].fundamentalValue;
            double realValuationUncertainty = this.prices[priceIndex].valuationUncertainty;

            double highestValuationInterval = realFundamentalValue + realValuationUncertainty / 2;
            // Calculate information level using anomalous diffusion
            double informationLevel = diffusionModel.calculateInformationLevel(day.currentPeriod().currentTick());

            if (informationLevel >= 0.5) {
                // Always decide to SELL
                char direction = 'A';

                // SELL all owned assets
                int numberOfAssets = this.getInvest("lvmh");

                // Target price for the order
                long desiredPrice = (long) (highestValuationInterval - ((this.aggressivity * highestValuationInterval) / 100));

                if (numberOfAssets > 0) {
                    return new LimitOrder(obName, "" + this.myId, direction, numberOfAssets, desiredPrice);
                }
            }

            return null;
        }
        return null;
    }
}