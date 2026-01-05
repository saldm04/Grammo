import llvmlite.binding as llvm

class GrammoOptimizer:
    """Optimizes LLVM modules using the New Pass Manager.

    Attributes:
        None
    """

    def __init__(self):
        """Initializes the optimizer and native targets."""
        # Initialize LLVM native target if not already done
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    def optimize(self, module, speed_level=3, size_level=0):
        """Optimizes the given LLVM module.

        Args:
            module (llvmlite.ir.Module): The module to optimize.
            speed_level (int): Optimization level for speed (0-3).
            size_level (int): Optimization level for size (0-2).

        Returns:
            llvmlite.binding.ModuleRef: The optimized module reference.
        """
        # Parse the module assembly to get a ModuleRef
        mod_ref = llvm.parse_assembly(str(module))
        mod_ref.verify()

        # Create target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()

        # Create pipeline tuning options
        pto = llvm.create_pipeline_tuning_options(
            speed_level=speed_level,
            size_level=size_level
        )
        
        # Create pass builder
        pass_builder = llvm.create_pass_builder(target_machine, pto)

        # Create module pass manager
        mpm = pass_builder.getModulePassManager()
        
        # Run optimizations
        mpm.run(mod_ref, pass_builder)
        
        return mod_ref
