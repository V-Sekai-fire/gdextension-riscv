<p align="center">
<img src="https://github.com/libriscv/godot-sandbox/blob/main/banner.png?raw=true" width="312px"/>
</p>
<p align="center">

<p align="center">
        <img src="https://github.com/libriscv/godot-sandbox/actions/workflows/runner.yml/badge.svg?branch=main"
            alt="Godot Sandbox Build"></a>
        <img src="https://img.shields.io/badge/Godot-4.2-%23478cbf?logo=godot-engine&logoColor=white" />
</p>

<p align = "center">
    <strong>
        <a href="https://libriscv.no">Website</a> | <a href="https://github.com/libriscv/godot-sandbox/blob/main/CHANGELOG.md">Changelog</a> | <a href="https://discord.gg/n4GcXr66X5">Discord</a>
    </strong>
</p>


-----

<p align = "center">
<b>Safe, low-latency and fast sandbox</b>
<i>for the Godot game engine.</i>
</p>

-----

This extension exists to allow Godot creators to implement safe modding support, such that they can pass around programs built by other players, knowing that these programs cannot harm other players.


## Installation

- Automatic (Recommended): Download the plugin from the official [Godot Asset Store](.) using the **AssetLib** tab in Godot by searching for **Godot Sandbox**. TODO

- Manual: Download the [latest github release](https://github.com/libriscv/godot-sandbox/releases/latest) and move only the **addons** folder into your project **addons** folder.

## Usage

Create a new `Sandbox` and assign a RISC-V ELF program resource to it.

```gdscript
extends Sandbox

func _ready():
	# Make a function call into the sandbox
	vmcall("my_function", Vector4(1, 2, 3, 4));

	# Measure the time it takes to cold-call one function
	print("\nMeasuring call overhead...");
	var emptyfunc = vmcallable("empty_function");

	var t0 = Time.get_ticks_usec()
	emptyfunc.call();
	var t1 = Time.get_ticks_usec()
	print("Execution time: ", (t1 - t0), "us")

	# Pass a complex Variant to the sandbox
	var d = Dictionary();
	d["test"] = 123;
	vmcall("my_function", d);

	# Create a callable Variant, and then call it later
	var callable = vmcallable("function3");
	callable.call(123, 456.0, "Test");

	# Pass a function to the sandbox as a callable Variant, and let it call it
	var ff : Callable = vmcallable("final_function");
	vmcall("trampoline_function", ff);

	# Pass a packed byte array
	var testbuf = PackedByteArray();
	testbuf.resize(32);
	testbuf.fill(0xFF);
	vmcall("test_buffer", testbuf);

	#vmcall("failing_function");

	pass # Replace with function body.
```

The API towards the sandbox uses Variants, and the API inside the sandbox uses (translated) Variants.

```C++
extern "C"
void function3(Variant x, Variant y, Variant text) {
	UtilityFunctions::print("x = ", x, " y = ", y, " text = ", text);
}
```

Above: An example of a sandboxed C++ function.

### What can I do?

- You can implement a modding API for your game, to be used inside the sandbox. This API can then be used by other players to extend your game, in a safe manner. That is, they can send their mod to other people, including you, and they (and you) can assume that it is safe to try out the mod. The mod is *not supposed* to be able to do any harm. That is the whole point of this extension.
- You can implement support for your favorite language inside the sandbox. The sandbox receives Variants from Godot or GDScript, and can respond back with Variants. This means the communication is fully dynamic, and supports normal Godot usage. 

Languages that are known to work inside _libriscv_:
1. QuickJS
2. C
3. C++
4. Rust
5. Zig
6. Nim
7. Nelua
8. v8 JavaScript w/JIT
9. Go (not recommended)
10. Lua, Luau
11. Any other language that can produce RISC-V programs

## Performance

The sandbox is implemented using _libriscv_ which primarily focuses on being low-latency. This means that calling small functions in the sandbox is extremely fast, unlike all other sandboxing solutions.

There are high-performance modes for _libriscv_ available for both development and final builds. When developing on Linux, libtcc-jit is available (which is in theory portable to both Windows and MacOS). And for final builds one can produce a high-performance binary translation, with up to 92% native performance, that can be embedded in the project (either Godot itself, or the GDExtension). This high-performance binary translation works on all platforms, such as Nintendo Switch, Mobile Phones, and other locked-down systems. It is especially made for such systems, but is inconvenient to produce.

Please see the [documentation for libriscv](https://github.com/libriscv/libriscv) for more information.

As a final note, the default interpreter mode in _libriscv_ is no slouch, being among the fastest interpreters. And will for most games, and in most scenarios be both the slimmest in terms of memory and the fastest in terms of iteration. Certain variant operations will call out to Godot in order to get native performance.

## Contributing

Requirements:
- [SCons](https://www.scons.org)
- [python3](https://www.python.org)

If you want to contribute to this repo, here are steps on how to build locally:

```sh
scons
```

Linting:

```sh
./scripts/clang-tidy.sh
```

### How to compile cpp code locally

This project provides a dockerfile for compiling cpp code locally. For usage example, go to:

```
cd program
docker run -v .:/usr/src -d ghcr.io/fwsgonzo/compiler build.sh
```
