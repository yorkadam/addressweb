class Result(object):
    def __init__(self):
        self.message = None
        self.objects = []
        self.error_status = False
        self.value = None
        self.success = False
    pass


def build_result_error(method, error_type):
    result = Result()
    if error_type == "DataError":
        result.error_status = True
        result.message = "SQLite Data Error"
        result.value = False
    elif error_type == "ProgrammingError":
        result.error_status = True
        result.message = "SQLite Programming Error"
        result.value = False
    elif error_type == "IntegrityError":
        result.error_status = True
        result.message = "SQLite Data Integrity Error"
        result.value = False
    elif error_type == "Error":
        result.error_status = True
        result.message = "SQLite Base Error"
        result.value = False
    elif error_type == "SystemError":
        result.error_status = True
        # result.message = Ex.__cause__
        result.value = False
    return result
    pass
