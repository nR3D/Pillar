from models import Obj
import numpy as np
from pathlib import Path

def import_obj(file_path : str, **kwargs) -> Obj:
    res_obj = Obj([], kwargs=kwargs)
    for line in open(Path(file_path)):
        line = line.rstrip('\n').split(' ')
        if line[0] == 'v':
            res_obj.vertices.append(np.array([float(l) for l in line[1:]]))
            while len(res_obj.vertices[-1]) < 4:
                res_obj.vertices[-1] = np.append(res_obj.vertices[-1],1)
        elif line[0] == 'f':
            # this implementation ignores vt and vn
            res_obj.faces.append([])
            for f in line[1:]:
                res_obj.faces[-1].append(int(f.split('/')[0]))
    return res_obj