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

    def ReadFile(self, data_dir, filename, fields, constructor, n=None):
        """ Reads a compressed data file builds one object per record
        :param data_dir:
        :param filename:
        :param fields:
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
            record = self.MakeRecord(line, fields, constructor)
            self.AddRecord(record)
        fp.close()

    def MakeRecord(self, line, fields, constructor):
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

    def AddRecord(self, record):
        """
        Adds a record to this table
        :param record:
        :return:
        """
        self.records.append(record)

    def ExtendRecords(self, records):
        """
        Adds records to this table
        :param records:
        :return:
        """
        self.records.append(records)

    def Recode(self):
        """
        Child classes can override this to recode values
        :return:
        """
        pass


class