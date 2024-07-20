FROM ubuntu:latest

RUN apt update && apt install -y \
	cmake git \
	clang-18 \
	tcc libtcc-dev \
    ninja-build \
    dos2unix \
	g++-riscv64-linux-gnu

ENV CXX=clang++-18

# Fast emulation (with TCC JIT compilation)
WORKDIR /app/
RUN bash
