import llvmlite.binding as llvm
import ctypes
import ctypes.util

class JITExecutor:
    """Executes compiled LLVM modules using MCJIT.

    Handles initialization of LLVM native targets and finding standard library symbols.
    """

    def __init__(self):
        """Initializes the JIT executor."""
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    def run(self, module_ref):
        """Executes the 'main' function in the given LLVM module.

        Args:
            module_ref (llvmlite.binding.ModuleRef): The compiled LLVM module.

        Raises:
            RuntimeError: If the 'main' function cannot be found in the module.
        """
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        
        # Register standard library symbols explicitly
        # This fixes resolution issues on Windows/some platforms
        try:
            if hasattr(ctypes, 'cdll') and hasattr(ctypes.cdll, 'msvcrt'):
                libc = ctypes.cdll.msvcrt
            else:
                # Robust fallback for MacOS/Linux
                libc_path = ctypes.util.find_library('c')
                if libc_path:
                    libc = ctypes.CDLL(libc_path)
                else:
                    libc = ctypes.CDLL(None)
        except OSError:
             libc = None
        
        if libc:
            for name in ["printf", "scanf", "malloc", "strlen", "strcpy", "strcat"]:
                if hasattr(libc, name):
                    func = getattr(libc, name)
                    addr = ctypes.cast(func, ctypes.c_void_p).value
                    llvm.add_symbol(name, addr)

        engine = llvm.create_mcjit_compiler(module_ref, target_machine)
        engine.finalize_object()
        
        func_ptr = engine.get_function_address("main")
        if not func_ptr:
            raise RuntimeError("Could not find 'main' function in the module.")
            
        c_func_type = ctypes.CFUNCTYPE(None)
        c_func = c_func_type(func_ptr)
        c_func()