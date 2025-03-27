from filemanipfunc import copy_to_directory, generate_pages_recursive
import sys, os, shutil

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_to_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
 
main()