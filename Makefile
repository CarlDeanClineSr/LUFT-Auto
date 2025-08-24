# Quick tasks for LUFT-Auto

.PHONY: smoke
smoke:
	# Adjust the script path below to your actual entrypoint
	python path/to/your_coherence_script.py \
		--config configs/coherence.yaml \
		--input data/sample_dimuon.csv \
		--out out/quickcheck.json
	@echo "Smoke test complete. Check out/quickcheck.json"
