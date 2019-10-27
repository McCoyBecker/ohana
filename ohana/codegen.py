import llvmlite.ir as ir
import llvmlite.binding as llvm
import ast

class CodeGenerationError(Exception):
    pass

class LLVMCodeGenerator(object):
    def __init__(self):
        self.module = ir.Module()
        self.builder = None
        self.func_symtab = {}

    def generate_code(self, node):
        assert isinstance(node, (ast.PrototypeAST, ast.FunctionAST))
        return self._codegen(node)

    def _codegen(self, node):
        method = '_codegen_' + node.__class__.__name__
        return getattr(self, method)(node)

    def _codegen_NumberExprAST(self, node):
        return ir.Constant(ir.DoubleType(), float(node.value))

    def _codegen_VariableExprAST(self, node):
        return self.func_symtab[node.name]

    def _codegen_BinOpExprAST(self, node):
        left = self._codegen(node.left)
        right = self._codegen(node.right)

        if node.op == '+':
            return self.builder.fadd(left, right, 'addtmp')

        elif node.op == '-':
            return self.builder.fsub(left, right, 'subtmp')

        elif node.op == '*':
            return self.builder.fmul(left, right, 'multmp')

        elif node.op == '<':
            cmp = self.builder.fcmp_unordered('<', left, right, 'cmptmp')
            return self.builder.uitofp(cmp, ir.DoubleType(), 'booltmp')

        else:
            raise CodeGenerationError("Unknown binary operator.", node.op)

    def _codegen_CallExprAST(self, node):
        callee_func = self.module.globals.get(node.callee, None)
        if callee_func is None or not isinstance(callee_func, ir.Function):
            raise CodeGenerationError("Call to unknown function.", node.callee)
        if len(callee_func.args) != len(node.args):
            raise CodeGenerationError("Call argument length mismatch.", node.callee)
        call_args = [self._codegen(arg) for arg in node.args]
        return self.builder.call(callee_func, call_args, 'calltmp')

    def _codegen_PrototypeAST(self, node):
        funcname = node.name
        # Create a function type
        func_ty = ir.FunctionType(ir.DoubleType(),
                                  [ir.DoubleType()] * len(node.arg_names))

        # If a function with this name already exists in the module...
        if funcname in self.module.globals:
            # We only allow the case in which a declaration exists and now the
            # function is defined (or redeclared) with the same number of args.
            existing_func = self.module[funcname]
            if not isinstance(existing_func, ir.Function):
                raise CodegenError('Function/Global name collision', funcname)
            if not existing_func.is_declaration():
                raise CodegenError('Redifinition of {0}'.format(funcname))
            if len(existing_func.function_type.args) != len(func_ty.args):
                raise CodegenError(
                    'Redifinition with different number of arguments')
            func = self.module.globals[funcname]
        else:
            # Otherwise create a new function
            func = ir.Function(self.module, func_ty, funcname)
        # Set function argument names from AST
        for i, arg in enumerate(func.args):
            arg.name = node.arg_names[i]
            self.func_symtab[arg.name] = arg
        return func

    def _codegen_FunctionAST(self, node):
        # Reset the symbol table. Prototype generation will pre-populate it with
        # function arguments.
        self.func_symtab = {}
        # Create the function skeleton from the prototype.
        func = self._codegen(node.proto)
        # Create the entry BB in the function and set the builder to it.
        bb_entry = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(bb_entry)
        retval = self._codegen(node.body)
        self.builder.ret(retval)
        return func
