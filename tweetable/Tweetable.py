import ui


class TweetTextView:
	"""Delegate for ui.TextView implementing one method."""
	
	def textview_did_change(self, textview):
		"""Change label to length of text"""
		
		length = len(textview.text)
		
		v = textview.superview
		label = v['length']
		label.text = 'Length: {}'.format(str(length))
		
		if length > 140:
			color = 'lightyellow'
			if length > 280:
				color = 'red'
		else:
			color = 'white'
		v.background_color = color


v = ui.load_view()

tweet = v['tweet']
tweet.delegate = TweetTextView()
# properly initialize everything
tweet.delegate.textview_did_change(tweet)

v.present('sheet')

