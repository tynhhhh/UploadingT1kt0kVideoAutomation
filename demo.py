from pytube import YouTube

a = YouTube('https://www.youtube.com/shorts/FCqEFvKpT9s')
a.streams.first().download()