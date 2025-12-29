from . import general_operators, openlrm_operators

def register():
    general_operators.register()
    openlrm_operators.register()

def unregister():
    general_operators.unregister()
    openlrm_operators.unregister()