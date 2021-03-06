### Move Ordering Spy

#### A. Description

It is just a python script or equivalent converted exe file that will attempt to measure the effects of move ordering changes in a computer chess engine. It actually tests the engine with a set of specialized epd suite similar to STS-Strategic Test Suite then record how many points it gets and how long its takes to finish the tests. The engine version which gets a higher point and faster will be considered as the best.

#### B. Usage

<code>move_ordering_spy.py --engine [engine name] --epd [test epd file] --depth [depth] --logging [number 0 or 1]</code>

#### C. Example

1. If your engine is Pluto.exe and your test file is STS.epd and you want Pluto to be tested at depth 12.

<code>move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12</code>

2. If you want to see the engine log you can use the following command line.

<code>move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1</code>

3. If you want the engine to use 128 MB use the option --hash [value in mb]

<code>move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1 --hash 128</code>

4. If you want the engine to use 2 threads use the option --threads [number]

<code>move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1 --hash 128 --threads 2</code>

5. It also supports paths for engine and epd file

<code>move_ordering_spy.py --engine "c:\engines\Pluto\Pluto.exe" --epd "c:\Test Suite\STS\STS.epd" --depth 12</code>

6. If you don't have python installed, and you are using windows you can use the exe file instead.

<code>move_ordering_spy.exe --engine Pluto.exe --epd STS.epd --depth 12 --logging 1</code>

    or for shorter option name with Hash at 128 mb and Thread 1

<code>move_ordering_spy.exe -e Pluto.exe -h 128 -t 1 -f STS.epd -d 12 -l 1</code>


#### D. Output Files

1. mos_summary.txt
2. mos_logs.txt

#### E. Input EPD

1. The recommended input format for epd is STS or Strategic Test Suite which can be found [here](https://sites.google.com/site/strategictestsuite/). However I make some changes on this test suite by adding opcodes for moves in uci format and others just for script convenience, I call it STS1-STS15_LAN_v3.epd and it is included in the package. We are grateful to Swaminathan and Dann for creating such fantastic test suite and its idea of a multi move solution with points.

2. I am generating this kind of epd format from latest strong grandmaster games from tournaments such as London Chess Classic 2016, TataSteel 2017, Sharjah Grand Prix 2017 and World Championships 2016 and others. I will upload these positions once I get some of them.

3. Epd test suites in the pack

    a. STS1-STS15_LAN_v3.epd [1500 positions]  
    b. move_ordering_spy.epd [4554 positions]  
    
   move_ordering_suite.epd are from positions of games from strong tournaments like WCh2016, LondonCC2016, WChCand2016 and others,    positions were analyzed by Stockfish 260317 64 POPCNT at 3 minutes/pos at multipv 5. The points of every epd (1 to 10) which can be found in c8 opcode, were generated based on search score of Stockfish, only the top 4 are saved in the epd and only those positions whose top 1 moves were not easy (according to Stockfish) were saved. Also the top 1 move should have a score of from -0.5 to +1.5 in order for it to be included in the test set. Position selection start at move 12 till move 30 in every game.
    
4. EPD interpretation
   
    <code>r1b2rk1/1pp1qppp/2nb1n2/p3p1N1/2B1N3/2PP4/PP2QPPP/R1B1K2R w KQ - acd 23; bm h4; eco "C65"; Ae "Stockfish 260317 64 POPCNT";
          c6 "64 47 34 22"; c7 "h4 Nxf6+ g4 Bd2"; c8 "10 7 5 3"; c9 "h2h4 e4f6 g2g4 c1d2";</code>
     
    OpCodes:
    
    * acd = analysis depth  
    * bm  = best move  
    * eco = encyclopedia of chess opening  
    * Ae  = analyzing engine  
    * c6  = comment no. 6, these are the values of the analyzing engine (Ae opcode) search score in centipawn, the first (64) is the                 score for top 1 move or bm h4. 47 is for the top 2 move and so on  
    * c7  = comment no. 7, these are the moves in SAN-Standard Algebraic notation format  
    * c8  = comment no. 8, these are the points of this position, for example if the engine under tests would choose g4 as its best move             then it will get 5 points for this test position  
    * c9  = comment no. 9, these are the best moves in uci protocol move format, this is similar to the values in c7 opcode    

#### F. Script idea

This script was created based from the [discussion in CCC](http://talkchess.com/forum/viewtopic.php?topic_view=threads&p=710117&t=63555) on testing move ordering improvement.

#### G. Limitations

Only engines that supports UCI protocol are supported on this script, and that engine should also support the go depth command.

#### H. Example output from summary

<pre>
Test File                 : move_ordering_spy.epd
Total Positions           : 3700
Evaluated Positions       : 3700
Max Evaluated Points      : 37000
Search Depth              : 12
Hash (mb)                 : 128
Threads                   : 1

Engine                              Pts   MaxPts  Pts(%)  Time(ms) Top1(%)
Deuterium v2017.1.35.353          24025    37000   64.93   1268722   42.76
Deuterium v2017.1.35.358          23607    37000   63.80   1227647   41.62
Deuterium v2017.1.35.359          24155    37000   65.28   1231714   42.73
</pre>

    1. Version 353 is the base version
    2. Version 358 is from v353 but without killer move 2 slot
    3. Version 359 is from v353 but has move ordering bonus for captures that attacks the opponent's king
