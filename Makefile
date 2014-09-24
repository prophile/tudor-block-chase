USB_PATH=/Volumes/KINGSTON

all: robot.zip

robot.zip: src/robot.py
	pyenv/make-zip --no-strip src "$@"

copy-macosx: robot.zip
	wait4path $(USB_PATH)
	cp robot.zip $(USB_PATH)/robot.zip
	diskutil unmount $(USB_PATH)

clean:
	rm -f robot.zip

.PHONY: all clean copy-macosx

