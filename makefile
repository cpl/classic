.PHONY: kernel clean deploy

kernel:
	cd kernel && $(MAKE)

clean:
	cd kernel && $(MAKE) clean

deploy:
	cd kernel && $(MAKE) deploy