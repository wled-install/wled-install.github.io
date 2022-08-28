import os, shutil

output_dir="_build"
bin_dir = "bin_dir"
suppl_dir = "suppl_dir"
manifest_dir = "manifest_dir"
output_bin_dir=os.path.join(output_dir,bin_dir)
output_suppl_dir=os.path.join(output_dir,suppl_dir)
output_manifest_dir=os.path.join(output_dir,manifest_dir)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if os.path.exists(output_bin_dir):
    shutil.rmtree(output_bin_dir)
shutil.copytree(bin_dir,output_bin_dir)
if os.path.exists(output_suppl_dir):
    shutil.rmtree(output_suppl_dir)
shutil.copytree(suppl_dir,output_suppl_dir)
if not os.path.exists(output_manifest_dir):
    os.makedirs(output_manifest_dir)

f_index= open(os.path.join(output_dir,"index_new.html"),"w+")
dirs1=os.listdir(output_bin_dir).sort()


for dir1 in dirs1:
     f_index.write(dir1)
f_index.close()

