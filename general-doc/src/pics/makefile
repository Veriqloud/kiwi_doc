targets = encoding.svg pm_qkd.svg system.svg overview.svg

all: $(targets)

%.svg: %.dvi
	dvisvgm --no-font --exact --zoom=1.4 $<
	rm $<

%.dvi: %.tex
	latex $< 
	rm $(basename $@).log $(basename $@).aux

clean:
	rm -f $(targets)
	rm -f *.dvi


