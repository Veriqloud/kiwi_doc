targets = encoding.svg pm_qkd.svg system.svg overview.svg optics_alice.svg optics_bob.svg rust_qber_scheme.svg

all: $(targets)

%.svg: %.dvi
	dvisvgm --font-format=WOFF2 --exact --zoom=1.4 --bbox=papersize $<
	rm $<

%.dvi: %.tex
	latex $< 
	rm $(basename $@).log $(basename $@).aux

clean:
	rm -f $(targets)
	rm -f *.dvi


