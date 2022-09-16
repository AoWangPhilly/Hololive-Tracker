twitter := src.twitter_pipeline

run_stream:
	python3 -m $(twitter).database
	python3 -m $(twitter).main