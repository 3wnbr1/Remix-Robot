# Vision

### Profiling

`python2 -m cProfile -o human.cprof human_detector.py`

`pyprof2calltree -k -i human.cprof`
