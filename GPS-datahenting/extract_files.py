import os
import glob

if __name__ == "__main__":
    source_files = glob.glob("source/*")

    for file_name in source_files:
        # Retrieve date from filename
        date = "-".join(os.path.basename(file_name).split(".")[0].split("-")[1:])
        print(date)

        # Create new files for  GPGGA_og GEINS tekstfiler
        f_source = open(file_name, 'r')
        f_geins = open(os.path.join("target", "GEINS", f"GEINS_{date}.txt"), 'a')
        f_gpgga = open(os.path.join("target", "GPGGA", f"GPGGA_{date}.txt"), 'a')

        # Delete previous file content
        f_geins.truncate(0)
        f_gpgga.truncate(0)

        # For each line in the source, extract GEINS and GPGGA info and write to correct file
        for line in f_source.readlines():
            if line[:6] == "@GEINS":
                f_geins.write(line)
            elif line[:6] == "$GPGGA":
                f_gpgga.write(line)

