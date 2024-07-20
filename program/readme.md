# Readme

```
docker build . -t riscv-compiler
docker run -v ${PWD}/../:/app/ --rm -i -t riscv-compiler ./build.sh
```
