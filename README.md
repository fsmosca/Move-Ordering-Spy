A. Description

It is a python script that will attempt to measure the effects of move ordering changes in a computer chess engine. It will actually test the engine with a set of specialized epd suite similar to STS test suite then record how many points it gets and how long its takes to finish the tests.

B. Usage

move_ordering_spy.py --engine [engine name] --epd [test epd file] --depth [depth] --logging [number 0 or 1]

C. Example

1. If your engine is Pluto.exe and your test file is STS.epd and you want Pluto to be tested at depth 12.

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12

2. If you want to see the engine log you can use the following command line.

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1

3. If you want the engine to use 128 MB use the option --hash [value in mb]

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1 --hash 128

4. If you want the engine to use 2 threads use the option --threads [number]

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1 --hash 128 --threads 2


D. Output Files

1. mos_summary.txt
2. mos_logs.txt

E. Input EPD

1. The recommended input format for epd is STS or Strategic Test Suite which can be found in the following link below. However I make some changes on this test suite by adding opcodes for moves in uci format and others just for script convenience, I call it STS1-STS15_LAN_v3.epd and it is included in the package. We are grateful to Swaminathan and Dann for creating such fantastic test suite and its idea of a multi move solution with points.

https://sites.google.com/site/strategictestsuite/

2. I am generating this kind of epd format from latest strong grandmaster games from tournaments such as London Chess Classic 2016, TataSteel 2017, Sharjah Grand Prix 2017 and World Championships 2016. I will upload these positions once I get some of them.

F. Script idea

This script was created based from the discussion in CCC on testing move ordering improvement.

http://talkchess.com/forum/viewtopic.php?topic_view=threads&p=710117&t=63555

G. Example output from summary
<pre>
Test File           : STS1-STS15_LAN_v3.epd
Total Positions     : 1500
Evaluated Positions : 1500
Search Depth        : 12

Engine                              Pts   MaxPts  Pts(%)  Time(ms)
Stockfish 8 64 POPCNT             11888    15000   79.25    181521
</pre>


