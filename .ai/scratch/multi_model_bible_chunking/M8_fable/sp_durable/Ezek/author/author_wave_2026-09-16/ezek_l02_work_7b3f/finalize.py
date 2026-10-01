# -*- coding: utf-8 -*-
import json, hashlib, os
D = r'C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_l02_work_7b3f'
DEL = os.path.join(D, 'ezek_author_l02_deliverable.json')
FIN = os.path.join(D, 'ezek_author_l02_final_message.json')

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

d = json.load(open(DEL, encoding='utf-8'))
dsha = sha(DEL)
d = dict(d)
d['output_files'] = dict(
  deliverable=dict(path=DEL, sha256=dsha,
                   note='sha256 taken AFTER the final write of the deliverable'),
  final_message=dict(path=FIN, sha256='reported in the returned message; a file cannot carry its own digest'))
json.dump(d, open(FIN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
fsha = sha(FIN)
print('deliverable   sha256 =', dsha)
print('final_message sha256 =', fsha)
print('deliverable   bytes  =', os.path.getsize(DEL))
print('final_message bytes  =', os.path.getsize(FIN))
json.dump(dict(deliverable_sha256=dsha, final_message_sha256=fsha),
          open(os.path.join(D, 'digests.json'), 'w', encoding='utf-8'), indent=1)
