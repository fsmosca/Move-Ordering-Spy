A. Description

It is a python script that will attempt to measure the effects of move ordering changes in a computer chess engine. It will actually test the engine with a set of specialized epd suite similar to STS test suite then record how many points it gets and how long its takes to finish the tests.

B. Usage

move_ordering_spy.py --engine [engine name] --epd [test epd file] --depth [depth] --logging [number 0 or 1]

C. Example

1. If your engine is Pluto.exe and your test file is STS.epd and you want Pluto to be tested at depth 12.

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12

2. If you want to see the engine log you can use the following command line.

move_ordering_spy.py --engine Pluto.exe --epd STS.epd --depth 12 --logging 1

D. Output Files

1. mos_summary.txt
2. mos_logs.txt


