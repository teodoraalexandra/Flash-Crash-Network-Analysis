package masonSimulation;

import java.util.Objects;

public class Agent {
    public String name;
    public double cash;
    public double shares;

    // Initialize an agent with a given name, cash, and shares
    public Agent(String name, double cash, double shares) {
        this.name = name;
        this.cash = cash;
        this.shares = shares;
    }

    // Define the trade behavior of the agent
    public void trade(Agent other, double price) {
        if (Objects.equals(this.name, "buyer")) {
            // If the agent is a buyer, it will buy one share if it can afford it
            if (this.cash >= price) {
                this.cash -= price;
                this.shares += 1;
                System.out.println("BUY at: " + price);
            }
        } else if (Objects.equals(this.name, "seller")) {
            // If the agent is a seller, it will sell one share if it has any to sell
            if (this.shares > 0) {
                this.cash += price;
                this.shares -= 1;
                System.out.println("SELL at: " + price);
            }
        }
    }
}

