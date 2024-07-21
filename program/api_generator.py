import os
import json
from pathlib import Path
import clang.cindex

# Initialize libclang
clang.cindex.Config.set_library_file(r'C:/Users/ernes/scoop/apps/llvm/current/bin/libclang.dll')

def find_files_recursively(dir, glob_pattern):
    return [str(path.relative_to(dir)) for path in Path(dir).rglob(glob_pattern)]

def parse_class(cursor):
    class_info = {
        "name": cursor.spelling,
        "methods": [],
        "base_classes": [],
        "enums": [],
        "structs": [],
        "classes": []
    }

    for c in cursor.get_children():
        if c.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            class_info["base_classes"].append(c.type.spelling)
        elif c.kind == clang.cindex.CursorKind.CXX_METHOD:
            if c.spelling == "GDEXTENSION_CLASS":
                continue
            method_info = {
                "name": c.spelling,
                "return_type": c.result_type.spelling,
                "arguments": [{"name": arg.spelling, "type": arg.type.spelling} for arg in c.get_arguments()],
                "virtual": c.is_virtual_method(),
                "static": c.is_static_method(),
                "constructor": c.kind == clang.cindex.CursorKind.CONSTRUCTOR,
                "destructor": c.kind == clang.cindex.CursorKind.DESTRUCTOR
            }
            class_info["methods"].append(method_info)
        elif c.kind == clang.cindex.CursorKind.ENUM_DECL:
            class_info["enums"].append(parse_enum(c))
        elif c.kind == clang.cindex.CursorKind.STRUCT_DECL:
            class_info["structs"].append(parse_class(c))
        elif c.kind == clang.cindex.CursorKind.CLASS_DECL and not c.is_definition():
            class_info["classes"].append(parse_class(c))

    return class_info

def parse_enum(cursor):
    enum_info = {
        "name": cursor.spelling,
        "values": []
    }
    for c in cursor.get_children():
        if c.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
            enum_info["values"].append({"name": c.spelling, "value": c.enum_value})
    return enum_info

def parse_header_file(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)

    classes = []
    structs = []
    enums = []

    for cursor in translation_unit.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.NAMESPACE and cursor.spelling == "godot":
            for child in cursor.get_children():
                if child.kind == clang.cindex.CursorKind.CLASS_DECL and child.is_definition():
                    classes.append(parse_class(child))
                elif child.kind == clang.cindex.CursorKind.STRUCT_DECL and child.is_definition():
                    structs.append(parse_class(child))
                elif child.kind == clang.cindex.CursorKind.ENUM_DECL:
                    enums.append(parse_enum(child))

    return {"classes": classes, "structs": structs, "enums": enums}

if __name__ == "__main__":
    input_folder = "../.build/godot-cpp/gen/include"
    output_folder = "./generated"

    input_files = find_files_recursively(input_folder, "*.hpp")
    file_classes_dict = {input_file: parse_header_file(os.path.join(input_folder, input_file)) for input_file in input_files if not input_file.startswith(("thirdparty/", "tests/"))}

    with open("wasgo_api.json", "w") as file:
        json.dump(file_classes_dict, file, indent=4)
