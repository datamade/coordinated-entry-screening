.PHONY: clean

all: port_location_codes

clean: 
		rm location_codes.csv

location_codes.csv: raw/CES\ Connect\ Flyer\ Locations_2019.xlsx
		in2csv --no-inference --sheet "Full List" "$<" > $@

port_location_codes: location_codes.csv
		cat $< | python port_location_codes.py 
		touch location_codes_ported