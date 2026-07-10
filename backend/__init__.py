from .fetch_openlrm import OpenLRMInferrer
from .fetch_triposr import TSRInferrer
from .fetch_craftsman import CraftsManInferrer

def fetch_and_init_model(model_id, args_dict, modelpath=""):
    match model_id:
        case 'OPTION_LRM':
            return OpenLRMInferrer(args_dict=args_dict, modelpath=modelpath)
        case 'OPTION_CFT3D':
            return CraftsManInferrer(args_dict=args_dict, modelpath=modelpath)
        case 'OPTION_TSR':
            return TSRInferrer(args_dict=args_dict)
        case _:
            raise ValueError('Model type not supported for this operation!')