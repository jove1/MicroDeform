

main_window.py: main_window.ui
	patch $^ patch_palette.diff -o - | pyside6-uic -g python > $@
