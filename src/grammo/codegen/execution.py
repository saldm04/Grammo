import llvmlite.binding as llvm
import ctypes
import ctypes.util

class JITExecutor:
    def __init__(self):
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    def run(self, module_ref):
        """
        Executes the 'main' function in the given LLVM module using MCJIT.
        
        Args:
            module_ref (llvmlite.binding.ModuleRef): The compiled module.
        """
        # Create a target machine
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
             # Fallback or strict error
             libc = None
        
        if libc:
            for name in ["printf", "scanf", "malloc", "strlen", "strcpy", "strcat"]:
                if hasattr(libc, name):
                    func = getattr(libc, name)
                    addr = ctypes.cast(func, ctypes.c_void_p).value
                    llvm.add_symbol(name, addr)

        # Create MCJIT execution engine
        # We need a backing module for the engine.
        # Note: create_mcjit_compiler takes (module, target_machine)
        # It transfers ownership of the module to the engine.
        engine = llvm.create_mcjit_compiler(module_ref, target_machine)
        engine.finalize_object()
        
        # Look up 'main' function
        # Grammo 'main' is void -> main(). 
        # But depending on name munging or if I named it 'main'.
        # I named it 'main' in CodeGenerator.
        
        func_ptr = engine.get_function_address("main")
        if not func_ptr:
            raise RuntimeError("Could not find 'main' function in the module.")
            
        # Cast to C function
        # void main()
        c_func_type = ctypes.CFUNCTYPE(None)
        c_func = c_func_type(func_ptr)
        
        # Execute
        c_func()
