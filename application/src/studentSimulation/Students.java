package studentSimulation;

import sim.engine.*;
import sim.util.*;
import sim.field.continuous.*;
import sim.field.network.*;

public class Students extends SimState {
    public Continuous2D yard = new Continuous2D(1.0,100,100);

    public double TEMPERING_CUT_DOWN = 0.99;
    public double TEMPERING_INITIAL_RANDOM_MULTIPLIER = 10.0;
    public boolean tempering = true;

    public int numStudents = 50;
    double forceToSchoolMultiplier = 0.01;
    double randomMultiplier = 0.1;

    public Network buddies = new Network(false);

    public Students(long seed) {
        super(seed);
    }

    public void start() {
        super.start();

        // add the tempering agent
        if (tempering)
        {
            randomMultiplier = TEMPERING_INITIAL_RANDOM_MULTIPLIER;
            schedule.scheduleRepeating(Schedule.EPOCH, 1, (Steppable) state -> { if (tempering) randomMultiplier *= TEMPERING_CUT_DOWN; });
        }

        // clear the yard
        yard.clear();

        // clear the buddies
        // buddies.clear();

        // add some students to the yard
        for(int i = 0; i < numStudents; i++) {
            Student student = new Student();
            yard.setObjectLocation(student,
                    new Double2D(yard.getWidth() * 0.5 + random.nextDouble() - 0.5,
                            yard.getHeight() * 0.5 + random.nextDouble() - 0.5));
            buddies.addNode(student);
            schedule.scheduleRepeating(student);
        }

        // define like/dislike relationships
        Bag students = buddies.getAllNodes();
        for(int i = 0; i < students.size(); i++) {
            Object student = students.get(i);
            // who does he like?
            Object studentB;
            do
                studentB = students.get(random.nextInt(students.numObjs));
            while (student == studentB);
            double buddiness = random.nextDouble();
            buddies.addEdge(student, studentB, buddiness);

            // who does he dislike?
            do
                studentB = students.get(random.nextInt(students.numObjs));
            while (student == studentB);
            buddiness = random.nextDouble();
            buddies.addEdge(student, studentB, -buddiness);
        }
    }

    public static void main(String[] args) {
        doLoop(Students.class, args);
        System.exit(0);
    }
}

