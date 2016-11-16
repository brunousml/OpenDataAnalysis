class StringCharset(object):
    @staticmethod
    def latin_to_utf(string):
        return string.decode('latin-1').encode('utf-8')
