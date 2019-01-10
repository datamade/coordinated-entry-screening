.PHONY: clean

all: location_codes.csv

clean: 
		rm location_codes.csv

location_codes.csv: raw/CES\ Connect\ Flyer\ Locations_2019.xlsx
		in2csv --no-inference --sheet "Full List" "$<" > $@
