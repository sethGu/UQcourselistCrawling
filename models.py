import pickle

file_name = "courseCode.pickle"

class Solutions:
    def __init__(self):
        self.all_course = []

    def getCourseCode(self, li: list):
        if not li: return
        res = []
        for i in li:
            tmp = i[12:20]
            res.append(tmp)
        self.all_course = res
        return res

    def save(self):
        with open(file_name, "wb") as f:
            pickle.dump(self.all_course, f)