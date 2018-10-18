
# coding: utf-8

# In[90]:


import os

picks = ""
indices = []


def pick_extractor(file_name, folder_name = "picks/"):
    
    f = open(folder_name+file_name).readlines()

    ind = []

    for idx, line in enumerate(f):
        if line.strip().strip("\n") == "<EventParameters>" or \
        line.strip().strip("\n") == "</EventParameters>":
            #print line, idx
            ind.append(idx)

    part = f[ind[0]+1:ind[-1]]
    return part, ind, file_name


def complete_xml_file(file_name, ind, folder_name = "picks/"):
    
    f = open(folder_name+file_name).readlines()
    
    top = "".join(f[:ind[0]+1])
    bottom = "".join(f[ind[1]:])
    
    return top, bottom

for pick_file in os.listdir("picks"):
    print pick_file
    parte, ind, file_name = pick_extractor(pick_file)
    texto = "".join(parte)
    picks += texto 
    
    indices.append([ind, file_name])

ind = indices[0][0]
file_name = indices[0][1]

top, bottom = complete_xml_file(file_name, ind)
picks_file_complete = top+picks+bottom

print len(picks_file_complete.split("\n"))

picks_final = open("picks_final.xml", "w")
picks_final.write(picks_file_complete)
picks_final.close()

