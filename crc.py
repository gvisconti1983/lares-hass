def u(e):
	t = [];
	for n in range(0, len(e)):
		r = ord(e[n]);
		if (r < 128):
			t.append(r)
		else:
			if (r < 2048):
				t.append(192 | r >> 6, 128 | 63 & r)
			else:
				if (r < 55296 or r >= 57344):
					t.append(224 | r >> 12, 128 | r >> 6 & 63, 128 | 63 & r)
				else:
					n = n + 1; 
					r = 65536 + ((1023 & r) << 10 | 1023 & ord(e[n]));
					t.append(240 | r >> 18, 128 | r >> 12 & 63, 128 | r >> 6 & 63, 128 | 63 & r);
		n = n+1;
	return t

def CRC(e):
	i = u(e);
	l = e.rfind('"CRC_16"') + len('"CRC_16"') + (len(i) - len(e));
	r = 65535;
	s = 0;
	while s < l:
		t = 128;
		o = i[s];
		while t:	
			if(32768& r):
				n = 1;
			else:
				n = 0;
			r <<= 1;
			r &= 65535;
			if(o & t):
				r = r + 1;
			if(n):
				r = r^4129;
			t >>= 1;
		s=s+1;
	return ("0x"+format(r,'04x'));

def addCRC(json_string):
	return json_string[:json_string.rfind('"CRC_16"')+len('"CRC_16":"')] + CRC(json_string) + '"}';
