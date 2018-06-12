# MatrixMultiplication
## Requirement
```shell
$ pip3 install -r requirements.txt
```

## Usage
### Main
```shell
$ python3 main.py -h
usage: main.py [-h] [--mode MODE] [--test]

optional arguments:
  -h, --help            show this help message and exit
  --mode MODE, -m MODE  -1 for control, 0 for tradition, 1 for strassen, 2 for
                        anotherway
  --test

$ python3 main.py < /path/to/test/file
```

### Generator
```shell
$ python3 generator.py -h
usage: generator.py [-h] [--exp EXP]

optional arguments:
  -h, --help         show this help message and exit
  --exp EXP, -e EXP  max 2's exponential

$ python3 generator.py < /path/to/test/file
```

### Intel AVX2
```shell
$ make
$ ./mul_avx2.c < /path/to/test/file
```
