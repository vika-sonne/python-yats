# Python Yet Another Test Suite

### :muscle: Python speed tests. Used for coding style & interpreter guides.

Here is several kind of tests: get/set data to containers & class attributes, strings manipulation.

One test runs for thousands times to gather it time metric, then averages calculated for this test.

So, several implementation are under test: **cpython**, **pypy**, **numba**.

Numba tests includes mathematical calculation only, since numba project in the grow stage and has shallow documentation. But this system has impressive test results and looks like exciting future, see [Numba documentation](https://numba.readthedocs.io/en/stable/).

### Test suite results

Below is set of graphs of tests time metrics. So, for best performance - less execution time and lowest bars on the graphs. Graph bars are grouped for a better look. Each group has it own name according to test feature.

#### Containers:
![](/images/speed_tests_1.png)

#### Assingment variables:
![](/images/speed_tests_2.png)

#### String manipulations:
![](/images/speed_tests_3.png)

#### Numba & other:
![](/images/numba_tests.png)
