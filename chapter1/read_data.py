import gzip
import pandas as pd


class ReadFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.DataFrame()

    def read_file(self, fields):
        if self.filename.endswith('gz'):
            fp = gzip.open(self.filename)
        else:
            fp = open(self.filename)

        for line in fp:
            df_line_recode = self.parse_record(fields, line)
            if not df_line_recode.empty:
                self.df = pd.concat([self.df, df_line_recode])

        fp.close()

    @staticmethod
    def parse_record(fields, line):
        field_arr = []
        name_arr = []
        for (name, begin, end, cast) in fields:

            s = line[begin - 1:end].strip()
            if s:
                val = cast(s)
            else:
                val = 'na'
            field_arr.append(val)
            name_arr.append(name)

        df_signal_record = pd.DataFrame(field_arr).T
        df_signal_record.columns = name_arr

        return df_signal_record


class Respondents(ReadFile):
    def read_respondents_file(self):
        self.read_file(fields=self.get_fields())

    @staticmethod
    def get_fields():
        return [('caseid', 1, 12, int)]


class Pregnancies(ReadFile):
    def read_pregnancies_file(self):
        self.read_file(fields=self.get_fields())

    @staticmethod
    def get_fields():
        return [
            ('caseid', 1, 12, int),
            ('nbrnaliv', 22, 22, int),
            ('babysex', 56, 56, int),
            ('birthwgt_lb', 57, 58, int),
            ('birthwgt_oz', 59, 60, int),
            ('prglength', 275, 276, int),
            ('outcome', 277, 277, int),
            ('birthord', 278, 279, int),
            ('agepreg', 284, 287, int),
            ('finalwgt', 423, 440, float)
        ]


def parse_respondents():
    resp_file = '../data/2002FemResp.dat.gz'
    res = Respondents(resp_file)
    res.read_respondents_file()
    return res.df


def parse_pregnancies():
    resp_file = '../data/2002FemPreg.dat.gz'
    res = Pregnancies(resp_file)
    res.read_pregnancies_file()
    return res.df


if __name__ == '__main__':
    print(parse_respondents())
    # print(parse_pregnancies())
