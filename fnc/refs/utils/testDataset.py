from csv import DictReader


class TestDataSet():
    def __init__(self, path, a_headline=None, a_body=None):
        if a_headline != None:
            self.stances = [{'Headline' : a_headline, 'Body ID' : 0}]
            self.articles = {0 : a_body}
            print('**** Single Data Test ****')
            print("---------- Stances type: ", str(type(self.stances)))
            print("---------- articles type: ", str(type(self.articles)))
            print("---------- Stances: ", str(self.stances))
            print("---------- articles: ", str(self.articles))
            return
        self.path = path

        print("Reading dataset")
        bodies = "test_bodies.csv"
        stances = "test_stances_unlabeled.csv"

        self.stances = self.read(stances)
        articles = self.read(bodies)
        self.articles = dict()

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Total stances: " + str(len(self.stances)))
        print("Total bodies: " + str(len(self.articles)))
        print("---------- Stances type: ", str(type(self.stances)))
        print("---------- articles type: ", str(type(self.articles)))
        print("---------- Stances: ", str(self.stances))
        print("---------- articles: ", str(self.articles))

    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)

            for line in r:
                rows.append(line)
        return rows

