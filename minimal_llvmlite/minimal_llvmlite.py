from __future__ import print_function
from llvmlite import ir

"""
Here's a reference implementation of Fibonacci:

    def fibonacci(n):
        if n <= 1:
            return 1
        else:
            return fibonacci(n-1) + fibonacci(n-2)

"""

# This creates a 64 bit Int type.
int_type = ir.IntType(64)

# This creates an Int -> Int function type.
fn_int_to_int_type = ir.FunctionType(int_type, [int_type])

# This creates the module that the code exists in. This is an LLVM-specific concept - see LLVM docs for more details.
module = ir.Module(name = "minimal_fibonacci")

# Here we declare the Fibonacci function and a block to hold its definition.
fn_fib = ir.Function(module, fn_int_to_int_type, name = "minimal_fib")
fn_fib_block = fn_fib.append_basic_block(name = "minimal_fib_entry")

# Now we create a builder for the block.
builder = ir.IRBuilder(fn_fib_block)

# Now we can start writing the implementation of Fibonacci.
fn_fib_n, = fn_fib.args

const_1 = ir.Constant(int_type, 1)
const_2 = ir.Constant(int_type, 2)

fn_fib_n_lt_or_eq_1 = builder.icmp_signed(cmpop = "<=", lhs = fn_fib_n, rhs = const_1)

with builder.if_then(fn_fib_n_lt_or_eq_1):
    builder.ret(const_1)

fn_fib_n_minus_1 = builder.sub(fn_fib_n, const_1)
fn_fib_n_minus_2 = builder.sub(fn_fib_n, const_2)

call_fn_fib_n_minus_1 = builder.call(fn_fib, [fn_fib_n_minus_1])
call_fn_fib_n_minus_2 = builder.call(fn_fib, [fn_fib_n_minus_2])

fn_fib_rec_res = builder.add(call_fn_fib_n_minus_1, call_fn_fib_n_minus_2)

builder.ret(fn_fib_rec_res)

print(module)
