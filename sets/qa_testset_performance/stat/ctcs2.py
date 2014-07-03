import re
import os

class LogDB:
    def __init__(self, dirname):
        assert isinstance(dirname, str)
        assert dirname != ''

        #strip the tailing '/'
        if dirname[-1] == '/':
            self.log_dir = dirname[0:-1]
        else:
            self.log_dir = dirname
        self.name = os.path.basename(self.log_dir)

    def samples(self, db_path, db_name, sample_class):
        db = list()
        path_pt = re.compile('%s-(\d{4}-\d{2}-\d{2})-(\d{2})-(\d{2})-(\d{2})' % db_path)
        for name in os.listdir(self.log_dir):
            r = path_pt.match(name)
            if r:
                sample_name = db_name + '_' + "%sT%s:%s:%s" % (r.group(1), r.group(2),
                                               r.group(3), r.group(4))
                filename = self.log_dir + '/' + name + '/' + db_name
                db.append(sample_class(filename, sample_name))
        return db
