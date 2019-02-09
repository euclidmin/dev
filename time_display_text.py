
# 00:01
# 01:32 --> It's one thirty two am

# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
num_0_19 = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
num_20_50 = ['', '', 'twenty', 'thirty', 'forty', 'fifty']
ampm = ['am', 'pm']

def input_digital_time(hhmm):
	hh, mm = map(int, hhmm.split(':'))
	print('hh={0}, mm={1}'.format(hh, mm))
	return (hh, mm)

def make_mm_text(mm):
	if mm < 20:
		return num_0_19[mm]

	mm_10, mm_1 = divmod(mm, 10)
	mm_10_text = num_20_50[mm_10]

	if mm_1 == 0:
		mm_1_text = ''
	else:
		mm_1_text = num_0_19[mm_1]
	return mm_10_text + ' ' + mm_1_text


def make_hh_text(hh):
	if hh == 0 or hh == 12 :
		return 'twelve'
	hh_idx = hh % 12
	return num_0_19[hh_idx]



def make_text_time(hh_mm):
	(hh, mm) = hh_mm
	ampm_idx =  1 if hh > 12 else 0

	text_clock = 'It\'s ' + make_hh_text(hh) + ' '+ make_mm_text(mm) + ' ' + ampm[ampm_idx]
	# print(text_clock)
	return text_clock


def time_display(hhmm):
	hh_mm = input_digital_time(hhmm)
	text_clock = make_text_time(hh_mm)
	# print(text_clock)
	return text_clock


with open('text_time_test.txt', 'r') as file:
	for line in file:
		print(line.strip() + ' ' + time_display(line))

