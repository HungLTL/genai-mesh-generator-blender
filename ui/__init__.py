from . import main_ui, openlrm_sub_ui, craftsman_sub_ui, triposr_sub_ui

def register():
    main_ui.register()
    openlrm_sub_ui.register()
    craftsman_sub_ui.register()
    triposr_sub_ui.register()

def unregister():
    main_ui.unregister()
    openlrm_sub_ui.unregister()
    craftsman_sub_ui.unregister()
    triposr_sub_ui.unregister()
