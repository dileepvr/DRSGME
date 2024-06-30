BUILDDIR=build
ZIP=zip
ZIPFLAGS=-r -FS
ZIPEXCLUDES=-x '**~' 'build/*' '.*' 'makefile'
ZIPTARGET=$(BUILDDIR)/$(notdir $(CURDIR)).pk3

TARGETS=$(BUILDDIR) $(ZIPTARGET)

.phony: all debug clean
all: $(TARGETS)

debug:
	@echo $(BUILDDIR)
	@echo $(ZIPTARGET)
	@echo $(ZIPEXCLUDES)

$(BUILDDIR):
	mkdir $(BUILDDIR)

$(ZIPTARGET) : *.* */*.png *.zc */*.zc | $(BUILDDIR)
	$(ZIP) $(ZIPFLAGS) $(ZIPTARGET) * $(ZIPEXCLUDES)
