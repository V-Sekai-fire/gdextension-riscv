#pragma once

#include <godot_cpp/classes/resource.hpp>

using namespace godot;

class CPPResource : public Resource {
	GDCLASS(CPPResource, Resource);

protected:
	static void _bind_methods() {}
	String file;

public:
	void set_file(const String &p_file) {
		file = p_file;
		emit_changed();
	}

	String get_file() {
		return file;
	}

	PackedByteArray get_content();
	CPPResource() {}
	~CPPResource() {}
};
