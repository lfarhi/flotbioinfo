all: norm

TOPLEVEL=$(shell pwd)

# work on one week at a time with FOCUS=w1
FOCUS     = $(wildcard w?)
NOTEBOOKS = $(shell git ls-files $(FOCUS) | grep '\.ipynb$$')
NOTEBASES = $(subst .ipynb,,$(NOTEBOOKS))

# for phony targets
force:

####################
# the notebooks saved in python format

# notebase -> full path of py module
define py_path
$(TOPLEVEL)/modules/$(notdir $(subst -,_,$(1))).py
endef

NOTEBOOKS_PY = $(foreach notebase,$(NOTEBASES),$(call py_path,$(notebase)))

py: $(NOTEBOOKS_PY)
python: py

define py_target
$(call py_path,$(1)): $(1).ipynb
	@mkdir -p $(dir $(call py_path,$(1)))
	jupyter nbconvert --to python --output=$(call py_path,$(1)) $(1).ipynb
endef

$(foreach notebase,$(NOTEBASES),$(eval $(call py_target,$(notebase))))

####################
# run nbnorm on all notebooks
norm normalize: normalize-notebook

# nbnorm.py now is python3 script
# it is not in the git repo for bioinfo so locate from PATH
NORM = $(HOME)/git/flotpython-tools/tools/nbnorm.py
NORM_OPTIONS = --author "François Rechenmann" --author "Thierry Parmentelat" --version 1.0 --logo-path media/inria-25-alpha.png --kernel 3

# -type f : we need to skip symlinks
normalize-nb normalize-notebook: force
	 $(NORM) $(NORM_OPTIONS) $(NOTEBOOKS)

.PHONY: norm normalize normalize-nb normalize-notebook

##########
files:
	@git ls-files | egrep -v 'w[0-9]/(media|data)|nbautoeval'

#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
