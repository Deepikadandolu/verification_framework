PYTHON=python3

.PHONY: test regression fault clean

test:
	$(PYTHON) -m pytest -q

regression:
	$(PYTHON) -m src.runner --tests 500 --seed 18473 --adaptive

fault:
	$(PYTHON) -m src.runner --tests 500 --seed 18473 --adaptive --fault-campaign

clean:
	rm -rf reports/*.json reports/*.md reports/traces
