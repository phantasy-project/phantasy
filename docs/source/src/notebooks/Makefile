.PHONY: convert clean

NB = phantasy_cavity.ipynb phantasy_orbit.ipynb

convert: $(NB)
	jupyter-nbconvert $(NB) --to rst

clean:
	/bin/rm -rf *files *.rst
