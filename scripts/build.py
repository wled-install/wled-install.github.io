import os, shutil

output_dir="_build"
bin_dir = "bin_dir"
output_bin_dir=os.path.join(output_dir,bin_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if os.path.exists(output_bin_dir):
    shutil.rmtree(output_bin_dir)
shutil.copytree(bin_dir,output_bin_dir)
f= open(os.path.join(output_dir,"index_new.html"),"w+")
for i in range(3):
     f.write("This is line %d\r\n" % (i+1))
f.close()

