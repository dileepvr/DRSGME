import sys
import os
import glob
import time
import png as mypng

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Provide folder as argument.")
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("Argument is not a valid directory.")
        sys.exit(1)

    olddir = os.getcwd()
    os.chdir(sys.argv[1])
    timestr = time.strftime("%Y%m%d-%H%M%S")
    outfilename = timestr + '_textures.lmp.new'
    outfile = open(outfilename, 'w')
    for file in glob.glob("*.png"):

        img = mypng.Reader(file)
        try:
            c = img.read(lenient=True)
        except (mypng.ChunkError, mypng.FormatError):
            print("Error while reading file: ", file)
            continue

        xsize = c[0]
        ysize = c[1]

        outfile.write(
            "Sprite " + file[:-4] + ", " + str(xsize) + ", " + str(ysize))
        outfile.write("\n{\n")
        outfile.write("\tPatch \"" + sys.argv[1].strip("/")
                      + "/" + file + "\", 0, 0\n")

        xoff = 0
        yoff = 0
        img = mypng.Reader(file)
        try:
            c = img.chunk(lenient=True)
        except mypng.ChunkError:
            print("ChunkError in file: ", file)
            continue

        while c[0].decode() != "grAb":
            try:
                c = img.chunk(lenient=True)
            except mypng.ChunkError:
                break

        if c[0].decode() == "grAb":
            mydata = c[1]
            xoff = int.from_bytes(mydata[0:4], byteorder='big')
            yoff = int.from_bytes(mydata[4:8], byteorder='big')

        outfile.write("\toffset " + str(xoff) + ", " + str(yoff))
        outfile.write("\n}\n")
        print(file, xsize, ysize, xoff, yoff)

    os.chdir(olddir)
    outfile.close()
