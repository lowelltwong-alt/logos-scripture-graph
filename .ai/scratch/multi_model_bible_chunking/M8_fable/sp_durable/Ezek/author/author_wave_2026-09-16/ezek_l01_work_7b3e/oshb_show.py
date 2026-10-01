import sys
P=r'C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\Ezek_oshb.txt'
V={}
for ln in open(P,encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln.strip(): continue
    r,_,t=ln.partition('\t'); V[r]=t
for ref in sys.argv[1:]:
    print(f'{ref}\t{V.get(ref,"<<MISSING>>")}')
