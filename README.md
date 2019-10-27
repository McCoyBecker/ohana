<p align="center">
<img src=ohana.png style="max-width: 30%">
</p>

## Introduction

To explore IR, we'll use a language with I think everyone knows (Python) to write a compiler for a language which we'll create (Ohana) using a Python library (llvmlite) with bindings to LLVM C. llvmlite is supposed to be used with Numba (which is a JIT compiler for Python which does cool stuff to code that uses NumPy a lot). Not so secretly, llvmlite is really supposed to be used to construct JIT compilers so we're going to use it to study IR and also construct a JIT compiler. 

## Intermediate representations

As this is part description of the code and part tutorial, let's talk about intermediate representations. Most of what I will discuss comes from the book [Engineering A Compiler](http://www.r-5.org/files/books/computers/compilers/writing/Keith_Cooper_Linda_Torczon-Engineering_a_Compiler-EN.pdf) which one should keep on the desk as they think about compilers. In this section, I'll discuss SSA-form IR, as well as CPS-form IR. SSA-form is typically used in imperative language design and has C-like syntax whereas CPS-form is used in functional languages and is incredibly hard for me to understand. I'll sprinkle references throughout.

### SSA-form IR

### CPS-form IR

### Introduction to LLVM IR

Most of this section is taken from a tutorial on constructing a JIT compiler in Haskell by Stephen Diehl [here](http://www.stephendiehl.com/llvm/). In fact, I was seriously considering following that tutorial but I decided against it in case anyone tries to take Haskell into a real project :)

I'll copy some of the information from that tutorial here, and I'll also specialize some of it to our case. First, let's look at the typical compiler pipeline again

<center><img src=http://www.stephendiehl.com/llvm/img/compiler.png></center>

Last time, we saw lexing and parsing with the BF language. Remember that the short answer for all these steps is: we don't want to program in assembly, I want to program in some fancy high-level language with nice abstractions. Instead of dealing with the pain of assembly, we forced some programmers to deal with the pain of building a system to convert from the high-level language to the low-level stuff (that's compilation). In this tutorial, we'll actually build a little lexer/parser, but we'll also build something which will **lower** the AST representation to LLVM IR representation. From there, the LLVM toolchain can take over and do the rest for us. Okay, so to build that **lower** part, we need to look at some LLVM IR.

Here's an example:

```
declare i32 @putchar(i32)

define i32 @add(i32 %a, i32 %b) {
%1 = add i32 %a, %b
ret i32 %1
}

define void @main() {
%1 = call i32 @add(i32 0, i32 97)
call i32 @putchar(i32 %1)
ret void
}
```

So we can immediately talk about a few things. First, declare is sort of like C headers. Second, the @ syntax means that the symbol defined by a *declare* or *define* statement is a global statement.

Here are examples of the first class types in LLVM IR:

<table>
<thead>
<tr class="header">
<th align="left"></th>
<th align="left">Type</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><code>i1</code></td>
<td align="left">A unsigned 1 bit integer</td>
</tr>
<tr class="even">
<td align="left"><code>i32</code></td>
<td align="left">A unsigned 32 bit integer</td>
</tr>
<tr class="odd">
<td align="left"><code>i32*</code></td>
<td align="left">A pointer to a 32 bit integer</td>
</tr>
<tr class="even">
<td align="left"><code>i32**</code></td>
<td align="left">A pointer to a pointer to a 32 bit integer</td>
</tr>
<tr class="odd">
<td align="left"><code>double</code></td>
<td align="left">A 64-bit floating point value</td>
</tr>
<tr class="even">
<td align="left"><code>float (i32)</code></td>
<td align="left">A function taking a <code>i32</code> and returning a 32-bit floating point <code>float</code></td>
</tr>
<tr class="odd">
<td align="left"><code>&lt;4 x i32&gt;</code></td>
<td align="left">A width 4 vector of 32-bit integer values.</td>
</tr>
<tr class="even">
<td align="left"><code>{i32, double}</code></td>
<td align="left">A struct of a 32-bit integer and a double.</td>
</tr>
<tr class="odd">
<td align="left"><code>&lt;{i8*, i32}&gt;</code></td>
<td align="left">A packed structure of an integer pointer and 32-bit integer.</td>
</tr>
<tr class="even">
<td align="left"><code>[4 x i32]</code></td>
<td align="left">An array of four i32 values.</td>
</tr>
</tbody>
</table>
