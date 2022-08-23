# *The Time - travel project*

This repository was developed for the purposes of the course in programming tools and technologies for data science and machine learning during my first semester as a graduate student in the Master's programme in Data Science & Machine Learning @ NTUA. 

The storyline is the following:

<em>Imagine that you could travel back in 1970 with a huge list containing all the information about the stock prices of the companies participated in the American stockmarket from 1970 until 2017. Futhermore, suppose that you have only 1 dollar in your pocket. The task is find two sequences of buy - sell moves with maximum lengths 1.000 and 1.000.000, respectively, in order to maximize your profit. At a given point there are six possible moves:

<ol>
  <li><b>Buy - open:</b> buy at the opening price of the day</li>
  <li><b>Sell - open:</b> sell at the opening price of the day</li>
  <li><b>Buy - low:</b> buy at the lowest price of the day</li>
  <li><b>Sell - high:</b> sell at the highest price of the day</li>
  <li><b>Buy - close:</b> buy at the closing price of the day</li>
  <li><b>Sell - close:</b> sell at the closing price of the day</li>
</ol>

The above moves are chronologically ordered in the following manner: 
  
  {buy-open, sell-open} >> {buy-low, sell-high} >> {buy-close, sell-close},
  
where the notation "A >> B" indicates that action A must happen before B. Futhermore, each move is bound to the following restrictions:
  
<ol>
  <li> The total number of stocks "s" that we buy at a given day "d" it should not exceed the 10% of the volume of stocks "s" at day "d"</li>
  <li> Similarly, the total number of stocks "s" that we sell at day "d" it should not exceed the 10% of the volume of stocks "s" at day "d" </li>
  <li> Suppose that at the beginning of day "d" we possess "n" stocks from "s", then during the day "d" we are not allowed to buy more than "n+1" stocks from "s".</li>
</ol>

Under these restrictions the goal is to find two sequences of moves with at most 1.000 and 1.000.000 moves, respectively, that maximize the profit. By the term profit we mean the total money after the execution of all moves. Futhermore, for a given sequence of moves we define the evaluation at a given day to be the sum of the money on the bank account and the value of all of our stocks in the closing price.
</em>

More details about the algorithm that was developed in order to provide a solution to this problem can be found on the report-pdf. The dataset can be found on Kaggle in the following [link](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs). Since it is infisible to examine every combination of companies the algorithm takes as input a list of companies and tries to find the best transactions between these companies. Below you can see the results obtained for the sequence with at most 1.000 and 1.000.000 moves respectively.

### 1.000 Moves

<div id="container">
  <div id="content">
    <p>- Default Companies:  {'AMZN', 'GE', 'AAPL'}</p>
    <p>- Total transactions:  936</p>
    <p>- Money earned:  4670718.89886</p>
  </div>
</div>

Below you can see the graph of the profit (balance) and evaluation (portfolio) obtained for the above transactions.


<img src="https://github.com/ChrisNick92/Time-travel-Project/blob/main/images/1000.png?raw=true" width="800" height="600">


### 1.000.000 Moves

<div id="container">
  <div id="content">
    <p>- Default Companies:  {'MSFT', 'BAC', 'SIRI', 'FB', 'ORCL', 'EBAY', 'CSCO', 'AAPL', 'MO', 'GE', 'INTC', 'HD'}</p>
    <p>- Total transactions:  52481</p>
    <p>- Money earned:  22912967542.46073</p>
  </div>
</div>

<img src="https://github.com/ChrisNick92/Time-travel-Project/blob/main/images/1000000.png?raw=true" width="800" height="600">

### Try your own combination of companies!

You can download the .py scripts and execute the mainscript.py with your own list of companies and become billionaire! Suppose you want to set a maximum number of 1500 moves and choose Amazon, Apple, Facebook and General Electric as companies, then you type the following command in the command line.

`>python ./mainscript.py 1500 COMPANIES 4 AMZN FB AAPL GE`

The identified word COMPANIES tells the program that the user will choose his/her own combination of companies, the number following the identifier word corresponds to the number of companies that the user will provide. If you want to print the results on screen you can type the following command.

`>python ./mainscript.py 1500 COMPANIES 4 AMZN FB AAPL GE PRINT TRUE`

and if you want to save the transactions into a txt file you can type

`>python ./mainscript.py 1500 COMPANIES 4 AMZN FB AAPL GE SAVEFILE TRUE`

Have fun!
