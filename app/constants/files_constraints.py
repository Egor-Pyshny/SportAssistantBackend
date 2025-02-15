from enum import Enum


class FileConstraints(Enum):

    excel_accepted_file_extensions = {"csv"}
    excel_accepted_content_types = {
        "text/csv",
    }
    excel_file_size_limit = 10485760  # 10 MB
