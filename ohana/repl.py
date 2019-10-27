# Python ecosystem.
import time
import llvmlite.binding as llvm
from pyfiglet import Figlet
from termcolor import colored
from cmd import Cmd
import subprocess

# Local ecosystem.
from parser import Parser
from lexer import Lexer, TokenKind
from jitcompiler import JITCompiler 

def dispatch_to_shell(cmds):
    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0].decode('UTF-8')
    return p

def dispatch(JITCompiler, raw_input):
    '''
    The dispatch function takes in raw input at the REPL and determines what to do with it. 
    
    If the input is preceded by a bang (!), it is interpreted as a bash command.
    Else, it is interpreted as code for the Ohana JIT compiler to deal with.
    '''
    if not raw_input:
        pass
    else:
        if raw_input[0] == "!":
            start = time.time_ns()
            output = dispatch_to_shell(raw_input[1:])
            return(time.time_ns()-start, output)

        else:
            start = time.time_ns()
            ast = Parser().parse_toplevel(raw_input)
            output = JITCompiler.evaluate(ast = ast)
            return(time.time_ns()-start, output)

def REPL(JITCompiler):
    r = Figlet(font = 'contessa')
    banner = colored(r.renderText("Ohana"), 'magenta')
    print("\n" + banner)
    line_count = 0
    while True:
        try:
            line = input(colored("Oh (v0.0.1)", 'magenta') + colored(" [" + str(line_count) + "]", 'cyan')+ colored(" ~> ", 'cyan'))
            execution_time, output = dispatch(JITCompiler, line)
            line_count+=1
            print(colored("Evaluated:", "red"))
            print(output)
            print(u'\u23F1 ' + colored(str(execution_time / (10 ** 9)) + " s\n", 'green'))

        except EOFError:
            break
    

if __name__ == '__main__':
    # Initialize JIT compiler...
    jitcompiler = JITCompiler()

    # Initialize REPL...
    REPL(jitcompiler)
