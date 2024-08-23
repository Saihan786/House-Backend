Welcome!

This software aims to assist in plotting houses in a user-provided region of space. This works with .geojson files and has its own method of generating them, but users are welcome to submit their own. It is available in a website, but the website must be run locally as it is not hosted anywhere.

The house plotter currently generates rows of houses parallel to the longest edge of the given region, optimised with iterative padding. I plan to add a road generator which will first divide the RLP into chunks, and then have a road touch each chunk and houses will be plotted in the resulting regions.

The Prototype branches each serve their own purpose regarding this project, with more details in PLAN.txt. P1 is for creating user-defined houses, P2 is for generating house polygons and plotting them within the region, P3 is for optimisation of house placement (hopefully with regard to roads), and P4 is for providing a map (for user shapefile generation) and for building the website. Chronologically, the order was actually P4->P1->P2->P4(for the website)->P3.

Feel free to browse the python files! For a better understanding of the plotting process (separate to the website), check out the file 'README_software' in the folder 'HOUSE/website/rlpsite/plot/software'.




TO RUN:
*The website can be run by cd'ing into 'HOUSE/website/rlpsite' and executing 'python manage.py runserver' into your terminal. The available pages are '/plot' and '/plot/generate'.
*If you don't want to use the website, run the file 'HOUSE/website/rlpsite/plot/software/Main.py' after making your desired setup (a default one exists too, but isn't good for large RLPs).



![Map Page](images_for_README/map_page.png)