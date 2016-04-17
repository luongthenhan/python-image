import sys
import urllib2


class Crawler:
    def __init__(self, request_url):
        self.url = request_url
        request = urllib2.Request(request_url)
        try:
            response = urllib2.urlopen(request)
        except:
            print "URL does not exists"
            raise sys.exit()
        self.read = response.read()

    def writeToFile(self, filepath):
        f = open(filepath, "wb")
        try:
            f.write(self.read)
        except:
            print "Failed to write file " + filepath
            raise sys.exit()
        finally:
            print "Successfully write file " + filepath
        f.close()