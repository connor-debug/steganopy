# stenopy

Based on Stepic (Lenny Domnitser)

encode_imdata(imdata, data)
	recieves arbitrary pixels and encodes data
	
	
decode_imdata(imdata)
	Given a sequence of pixels, returns an iterator of characters
    encoded in the image
    
    
encode_inplace(image, data)
	hides data in image
	
	
encode(image, data)
	generates a new image with hidden data
	
	
decode(image)
	extracts data from an image
