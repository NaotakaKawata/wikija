python3 flair_test.py
ruby src/supervised_linker.rb -T 0.3 -m data/parameter.txt -f extracted -t linked < predict.json > output.json
python3 display.py

