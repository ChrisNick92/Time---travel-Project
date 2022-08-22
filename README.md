# *The Time - travel project*

This repository was developed for the purposes of the course in programming tools and technologies for data science and machine learning during my first semester as a graduate student in the Master's programme in Data Science & Machine Learning @ NTUA. 

The storyline is the following:

<em>Imagine that you could travel back in 1970 with a huge list containing the all the information about the stock prices of the companies participated in the American stockmarket from 1970 until 2017. Futhermore, suppose that you are have only 1 dollar in your pocket. The task is find two sequences of buy - sell moves with maximimum lengths 1.000 and 1.000.000, respectively, in order to maximize your profit. At a given point there are six possible moves:

<ol>
  <li><b>Buy - open:</b> buying at the opening price of the day</li>
  <li><b>Sell - open:</b> sell at the opening price of the day</li>
  <li><b>Buy - low:</b> buy at the lowest price of the day</li>
  <li><b>Sell - high:</b> sell at the highest price of the day</li>
  <li><b>Buy - close:</b> buy at the closing price of the day</li>
  <li><b>Sell - close:</b> sell at the closing price of the day</li>
</ol>

The above moves are chronologically ordered in the following manner: {buy-open, sell-open} >> {buy-low, sell-high} >> {buy-close, sell-close}, where the notation "A >> B" indicates that action A must happen before B. Futhermore, each is move is bound to the following restrictions:
  
<ol>
  <li> The total number of stocks "s" that we buy at a given day "d" it should not exceed the 10% of the volume of stocks "s" at day "d"</li>
  <li> Similarly, the total number of stocks "s" that we sell at day "d" it should not exceed the 10% of the volume of stocks "s" at day "d" </li>
  <li> Suppose that at the beginning of day "d" we possess "n" stocks from "s", then during the day "d" we are not allowed to buy more than "n+1" stocks from "s".</li>
</ol>
  
</em>
