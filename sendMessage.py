import smtplib
carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com',
	'verizon_image': '@vzwpix.com'
}

phoneNums = {
	'sam': '5409052428'
}
# TODO: add image sending capabilities
def send(message):
	to_number = '{}{}'.format(phoneNums['sam'],carriers['verizon_image'])
	auth = ('BuyBotHelpsYouBuyThings@gmail.com', 'buybotpassword')

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number, message)
	print("message sent!")

send('earth')