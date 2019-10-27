# Python ecosystem.
from __future__ import print_function
from ctypes import CFUNCTYPE, c_double
import llvmlite.binding as llvm
from termcolor import colored

# Local ecosystem.
from codegen import LLVMCodeGenerator
from ast import FunctionAST

def logger(log_function, log_path):
    if log_path:
        with open(log_path, "rw+") as output:
            output.write(log_function())
        output.close()
        return None
    else:
        print(log_function())

class JITCompiler(object):
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.CodeGenerator = LLVMCodeGenerator()
        
        self.target = llvm.Target.from_default_triple()

    def evaluate(self, ast, optimize = True, llvmdump = True):

        # Unfortunately, side effects required...
        self.CodeGenerator.generate_code(ast)
        
        # Verbose.
        if llvmdump:
            print(colored("Unoptimized LLVM IR:", "red"))
            print(str(self.CodeGenerator.module))

        # If we're evaluating a define or extern declaration, stop. Else, if evaluating anonymous wrapper function for expression, proceed to JIT compile and execute.
        if not (isinstance(ast, FunctionAST) and ast.is_anonymous()):
            return None
        
        # Convert LLVM IR into representation in-memory.
        llvm_in_mem = llvm.parse_assembly(str(self.CodeGenerator.module))
        
        # Optimization passes.
        if optimize:
            pass

        # Create a target machine for the JIT compiler.
        target_machine = self.target.create_target_machine()

        with llvm.create_mcjit_compiler(llvm_in_mem, target_machine) as ee:
            ee.finalize_object()

            if llvmdump:
                print(colored("Machine code:", "red"))
                print(target_machine.emit_assembly(llvm_in_mem))

            func_ptr = CFUNCTYPE(c_double)(ee.get_function_address(ast.proto.name))
            result = func_ptr()
            return result
