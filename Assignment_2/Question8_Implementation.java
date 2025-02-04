package org.avmframework.localsearch;

import java.util.Random;

import org.avmframework.TerminationException;
import org.avmframework.objective.ObjectiveValue;

public class HillClimbingSearch extends LocalSearch {

  protected ObjectiveValue lastObj;
  protected ObjectiveValue newObj;
  
  protected void performSearch() throws TerminationException {
	  	System.out.print("Hill Search");
	    HillSearch();
  }

	protected void HillSearch() throws TerminationException{
		int hillIterations = 10;
		int bestVal = var.getValue();
		boolean foundBetter = false;
		while(hillIterations > 0) {
			int lastValue = var.getValue();
			lastObj = objFun.evaluate(vector);
			MovingWithGaussianScales();
			newObj = objFun.evaluate(vector);
			hillIterations--;
			if(newObj.betterThan(lastObj)) {
				foundBetter = true;
				bestVal = var.getValue();
			}
			var.setValue(lastValue);
			if(hillIterations == 0 && foundBetter) {
				hillIterations = 10;
				foundBetter = false;
				var.setValue(bestVal);
			}
			else {
				break;
			}
			}
	}
	
	public void MovingWithGaussianScales() {
		double scales[] = new double[3];
		Random random = new Random();
		for(int i=0; i<3; i++) {
			scales[i] = random.nextDouble();
		}
		
		for(double scale: scales) {
			int next = (int)Math.abs(Math.round(var.getValue() * scale * random.nextGaussian()))*40;
			var.setValue(next);
		}	}}
