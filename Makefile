all: robot.zip

robot.zip:
	pyenv/make-zip --no-strip src "$@"

clean:
	rm -f robot.zip

.PHONY: all clean

