from . import general_operators, openlrm_operators, triposr_operators, craftsman_operators, eval_operators

def register():
    general_operators.register()
    openlrm_operators.register()
    craftsman_operators.register()
    triposr_operators.register()
    eval_operators.register()

def unregister():
    general_operators.unregister()
    openlrm_operators.unregister()
    craftsman_operators.unregister()
    triposr_operators.unregister()
    eval_operators.unregister()