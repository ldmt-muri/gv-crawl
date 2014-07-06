all: train.sw-en

FRE=swa
FR=sw
ENG=eng
EN=en
SPLIT=../../teny/split.py
TOTEXT=../../teny/totext.py
PASTEIT=~/cdec/corpus/paste-files.pl
GARGANTUA=../../Gargantua1.0c/src/sentence-aligner
TEMPDIR := $(shell mktemp -u -p $(PWD) -t gargXXXX)

articles.db:
	python ../gv-crawl/warc2db.py ./crawl-$(FR)/*.warc.gz $@

all.$(ENG)-$(FRE).xml: articles.db
	mkdir -p $(TEMPDIR)
	python ../gv-crawl/db2bidoc.py $(EN) $(FR) $< $(TEMPDIR)
	cd $(TEMPDIR) && mkdir -p corpus_data && cd corpus_data && ../../$(GARGANTUA)
	python ../gv-crawl/align2xml.py eng swa $(TEMPDIR)/corpus_to_align/align_info.txt $(TEMPDIR)/corpus_data/output_data_aligned > $@
	# $(RM) -rf $(TEMPDIR)

train.$(ENG)-$(FRE).xml: all.$(ENG)-$(FRE).xml
	cat $< | python $(SPLIT) 08 31 > $@

# could do dev and test here

train.$(EN): train.$(ENG)-$(FRE).xml
	cat $< | python $(TOTEXT) $(ENG) > $@

train.$(FR): train.$(ENG)-$(FRE).xml
	cat $< | python $(TOTEXT) $(FRE) > $@

train.$(FR)-$(EN): train.$(FR) train.$(EN)
	$(PASTEIT) train.$(FR) train.$(EN) > $@

