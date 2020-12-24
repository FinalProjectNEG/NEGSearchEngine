
class Url:

    def __init__(self, url, title, description, num_of_element, dictionary_word):

        self.url = url
        self.title = title
        self.description = description
        self.num_of_element = num_of_element
        self.dictionary_word = dictionary_word
        self.appear_word_title = []
        self.appear_word_description = []
        self.score = 0

