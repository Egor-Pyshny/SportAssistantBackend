from enum import Enum


class Exceptions(Enum):

    lead_not_found = "Lead not found"
    lead_data_invalid = "Invalid file"

    file_has_non_excel_extension = "The file must be in .csv format"
    file_is_not_in_excel_format = "The file must be in .csv format"
    unprocessed_file_exception = "Invalid file"

    transaction_failed = "Transaction failed"
