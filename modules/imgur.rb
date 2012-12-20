# Dependencies:
# Install required rubygems

require 'json'
require 'open-uri'

gallery = JSON.parse(open('http://imgur.com/gallery.json').read)['gallery']

gallery.each {|i| i['url'] = "http://imgur.com/#{i['hash']}#{i['ext']}" }

puts gallery.sample['url']
