package atomSimulation;

import fr.cristal.smac.atom.*;
import fr.cristal.smac.atom.orders.*;

class MyAgent extends Agent
{
    private final int start;

    public MyAgent(String name, long cash, int start) {
        super(name, cash);
        this.start = start;
    }

    public Order decide(String obName, Day day) {
        if (day.currentPeriod().isContinuous() && day.currentPeriod().currentTick() == start) {
            return new LimitOrder(obName, "" + myId, LimitOrder.ASK, 10, 10000);
        }
        else {
            return null;
        }
    }

    public void touchedOrExecutedOrder(Event e, Order o, PriceRecord p) {
        /*
         * The agent is notified when one of his orders has been touched or executed
         * It's up to him to see what he does with this information.
         * This method is not mandatory.
         */
//        if (e == Event.EXECUTED && o.extId.equals() {
//        }
    }
}