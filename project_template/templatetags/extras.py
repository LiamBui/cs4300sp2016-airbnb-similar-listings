from django import template
from stop_words import get_stop_words

register = template.Library()
stop_words = get_stop_words('en')


@register.filter(name='highlight')
def highlight(value,similar_words):
	value = '<span class="more">' + value[:210] + '<span class="morecontent"><span>' + value [210:] + '</span><a href="" class="morelink">&nbsp;[Show More]</a></span></span>'
	for word in similar_words:
		value = value.replace(word, '<span class="highlights">' + word + '</span>')
	return value

@register.filter(name='highlight_amenities')
def highlight_amenities(value, similar_words):
	value = '<span class="more">' + value[:210] + '<span class="morecontent"><span>' + value [210:] + '</span></span></span>'
	for word in similar_words:
		value = value.replace(word, '<span class="highlights">' + word + '</span>')
	return value

@register.filter(name='more')
def more(value):
	value = '<span class="more">' + value[:210] + '<span class="morecontent"><span>' + value [210:] + '</span><a href="" class="morelink">&nbsp;[Show More]</a></span></span>'
	return value
