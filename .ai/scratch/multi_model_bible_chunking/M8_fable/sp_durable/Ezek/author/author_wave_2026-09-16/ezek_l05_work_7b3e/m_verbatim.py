P=r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek\Ezek_oshb.txt"
d={}
for l in open(P,encoding='utf-8'):
    l=l.rstrip('\n')
    if not l.strip(): continue
    k,_,t=l.partition('\t'); d[k]=t
o=open('verbatim_measured.txt','w',encoding='utf-8')
a=d['Ezek.33.17'].split(); b=d['Ezek.33.20'].split()
o.write("33.17 words: "+str(len(a))+"\n")
for i,w in enumerate(a): o.write(f"  a[{i}]={w}\n")
o.write("33.20 words: "+str(len(b))+"\n")
for i,w in enumerate(b): o.write(f"  b[{i}]={w}\n")
# longest common contiguous run
best=(0,-1,-1)
for i in range(len(a)):
    for k in range(len(b)):
        n=0
        while i+n<len(a) and k+n<len(b) and a[i+n]==b[k+n]: n+=1
        if n>best[0]: best=(n,i,k)
n,i,k=best
o.write(f"\nLONGEST IDENTICAL CONTIGUOUS RUN (pointed, whitespace-tokenised): {n} words\n")
o.write("  33.17["+str(i)+":"+str(i+n)+"] = "+" ".join(a[i:i+n])+"\n")
o.write("  33.20["+str(k)+":"+str(k+n)+"] = "+" ".join(b[k:k+n])+"\n")
o.write("  byte-identical: "+str(a[i:i+n]==b[k:k+n])+"\n")
vq=['אִ֧ישׁ','כִּדְרָכָ֛יו','אֶשְׁפּ֥וֹט','אֶתְכֶ֖ם']
o.write("\nverdict clause tokens "+" ".join(vq)+"\n")
o.write("  present in 33.20: "+str(all(t in b for t in vq))+"\n")
o.write("  present in 33.17: "+str([t for t in vq if t in a])+"  (empty list = none present)\n")
o.write("  33.17 second half after etnachta: "+" ".join(a[4:])+"\n")
o.close(); print('ok')
