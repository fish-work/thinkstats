import sys
import gzip
import os


class Record(object):
    """ Represents a record. """


class Respondent(Record):
    """ Represents a respondent """


class Pregnancy(Record):
    """ Represents a pregnancy """


class Table(object):
    """ Represents a table as a list of objects """

    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def read_file(self, data_dir, filename, fields, constructor, n=None):
        """ Reads a compressed data file builds one object per record
        :param data_dir:
        :param filename:
        :param fields:8
        :param constructor:
        :param n:
        :return:
        """
        filename = os.path.join(data_dir, filename)

        if filename.endswith('gz'):
            fp = gzip.open(filename)
        else:
            fp = open(filename)

        for i, line in enumerate(fp):
            if i == n:
                break
            record = self.make_record(line, fields, constructor)
            self.add_record(record)
        fp.close()

    @staticmethod
    def make_record(line, fields, constructor):
        """
        Scans a line and return an object with the appropriate fields
        :param line:
        :param fields:
        :param constructor:
        :return:
        """
        obj = constructor()
        for (fields, start, end, cast) in fields:
            try:
                s = line[start-1:end]
                val = cast(s)
            except ValueError:
                val = 'NA'
            setattr(obj, fields, val)
        return obj

    def add_record(self, record):
        """
        Adds a record to this table
        :param record:
        :return:
        """
        self.records.append(record)

    def extend_records(self, records):
        """
        Adds records to this table
        :param records:
        :return:
        """
        self.records.append(records)

    def recode(self):
        """
        Child classes can override this to recode values
        :return:
        """
        pass


class Respondents(Table):
    """
    Represents the respondent table
    被调查者文件
    """
    def read_records(self, data_dir, n=None):
        filename = self.get_file_name()
        self.read_file(data_dir, filename, self.get_fields(), Respondent, n)
        self.recode()

    @staticmethod
    def get_file_name():
        return '2002FemResp.dat.gz'

    @staticmethod
    def get_fields():
        return [
            ('caseid', 1, 12, int),
        ]


class Pregnancies(Table):
    """
    被调查者怀孕情况
    """
    def read_records(self, data_dir, n=None):
        filename = self.get_file_name()
        self.read_file(data_dir, filename, self.get_fields(), Pregnancy, n)

    @staticmethod
    def get_file_name():
        return '2002FemPreg.dat.gz'

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
            ('finalwgt', 423, 440, float),
        ]

    def recode(self):
        for rec in self.records:
            try:
                if rec.agepreg != 'NA':
                    rec.agepreg /= 100.0
            except AttributeError:
                pass

            try:
                if (rec.birthwgt_lb != 'NA' and rec.birthwgt_lb < 20 and
                            rec.birthwgt_oz != 'NA' and rec.birthwgt_oz <= 16):
                    rec.totalwgt_oz = rec.birthwgt_lb * 16 + rec.birthwgt_oz
                else:
                    rec.totalwgt_oz = 'NA'
            except AttributeError:
                pass


def main(name, data_dir='../data/'):
    resp = Respondents()
    resp.read_records(data_dir)
    print('Number of respondents:', len(resp.records))

    preg = Pregnancies()
    preg.read_records(data_dir)
    print('Number of pregnancies:', len(preg.records))


if __name__ == '__main__':
    main(*sys.argv)
