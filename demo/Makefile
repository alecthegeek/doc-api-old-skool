#TODO  Tesy and fix

PROJECT:=demo6`
CURRENT_BRANCH=master
DOCUMENTCLASS := article

.SUFFIXES:
.PHONY: clean all wc pdf html plain pmd wiki preview publish

PANDOC_FLAGS := --number-sections --standalone -f markdown+startnum+smart+yaml_metadata_block --filter pandoc-fignos
PANDOC_MD_FLAGS := $(PANDOC_FLAGS) -t gfm --template=_template.markdown
PANDOC_PDF_FLAGS := $(PANDOC_FLAGS) -V documentclass=$(DOCUMENTCLASS) --toc --resource-path=$(IMAGE_DIR)

IMAGES := ./demo4.png

pdf: $(PROJECT).pdf $(IMAGES) # Default target
all: pdf html

html: $(PROJECT).html $(IMAGES) $(THISMAKEFILE)
pmd: article/$(PROJECT).pmd $(IMAGES) $(THISMAKEFILE)
plain: $(PROJECT).txt $(IMAGES) $(THISMAKEFILE)
wiki: article/$(PROJECT).md article/_Sidebar.md
publish: wiki


publish:
	git commit -m "About to publish"
	git push

# Create a Pandoc markdown file by running m4
$(PROJECT).pmd: demo4.m4
	m4 -P $< > $@

%.png: %.plantuml
	plantuml -tpng $<
	git add $@
	-git commit -m "Make committed $@"

wc: $(PROJECT).pmd
	@echo Word count: $$(pandoc $(PANDOC_FLAGS) -t plain  $< | wc -w)

$(PROJECT).txt: $(PROJECT).pmd
	pandoc $(PANDOC_FLAGS) -t plain $< -o $@

# Create a PDF from Pandoc Markdown file
$(PROJECT).pdf: $(PROJECT).pmd $(IMAGES)
	pandoc $(PANDOC_PDF_FLAGS) $< -o $@

$(PROJECT).html: article/$(PROJECT).pmd $(IMAGES) $(THISMAKEFILE)
	pandoc $(PANDOC_FLAGS) $< -o $@

# Create a GitHub markdown file by running Pandoc
article/$(PROJECT).md: article/$(PROJECT).pmd  $(IMAGES) _template.markdown $(THISMAKEFILE)
	# Fix the image links
	sed -Ee 's|^(!\[[^]]+\]\()|\1$(WIKI_URL)/$(IMAGE_DIR)/|' $< | \
	pandoc $(PANDOC_MD_FLAGS) -o $@
	git add $@

