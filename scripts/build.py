import os

output_dir="_build"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
f= open(os.path.join(output_dir,"index_new.html"),"w+")
for i in range(3):
     f.write("This is line %d\r\n" % (i+1))
f.close()
