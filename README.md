Number guessing game with expensive answers
===========================================

At [CampZer0](https://camp.hsbp.org/2013/zer0/) we tried to figure out how one could optimize the process of a time-based blind SQL injection if "succeeding" queries take a long time to execute. We wrote a small simulation script to measure the efficiency of different strategies, but couldn't figure out a convincing solution. 

So we [turned to the smart people of Mathematics Stack Exchange](https://math.stackexchange.com/questions/488869/number-guessing-game-with-expensive-answers/) with a slightly rephrased problem, and after 3 years we got an [answer](http://math.stackexchange.com/a/1918211/93994). Although we can't verify the correctnes of the calculation, the simulated results look convincing :)

Results
-------

The following table shows simulation results of the standard binary search and Erick Wong's algorithm (average game costs after 1000 runs):

|SIZE   |Penalty (1+x)  |Binary Search  |EW's algorithm |Perf. Gain (%) |
|------:|--------------:|--------------:|--------------:|--------------:|
|5000   |0.1            |14.0697        |13.8091        |1.8522072255   |
|1000   |0.1            |11.5647        |11.3283        |2.0441515993   |
|500    |0.1            |10.5325        |10.2723        |2.4704486114   |
|100    |0.1            |8.169          |7.9221         |3.0224017628   |
|50     |0.1            |7.1053         |6.7982         |4.3221257371   |
|50     |1              |10.329         |9.801          |5.1118210863   |
|50     |2              |13.898         |12.165         |12.4694200604  |
|50     |5              |24.602         |19.444         |20.9657751402  |
|50     |9              |39.03          |26.364         |32.4519600307  |

As we can see, the optimized algorithm can yield significant performance gain in case the penalty is big (e.g. querying a large dataset).
