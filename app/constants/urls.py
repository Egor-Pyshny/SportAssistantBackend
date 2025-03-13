from enum import Enum


class Urls(Enum):

    # auth
    login = "/login"
    logout = "/logout"
    registration = "/registration"
    verify_email = "/verify_email"
    resend_verification_code = "/resend_verification_code"
    forgot_password = "/forgot_password"
    reset_password = "/reset_password"

    # user
    get_me = "/get_me"
    check_email = "/check_email"

    # competition
    competition_list = "/"
    competition_detail = "/{competition_id}"
    competition_days = "/{competition_id}/days"
    competition_create = "/create"
    competition_update = "/update/{competition_id}"
    competition_patch = "/{competition_id}"
    competition_delete = "/delete/{competition_id}"
    competition_day = "/{competition_id}/days/{day}"
    competition_results = "/result/{competition_id}"
    competition_update_day = "/update_day/{competition_id}"
    competition_update_result = "/update_result/{competition_id}"

    # camps
    camps_list = "/"
    camps_detail = "/{competition_id}"
    camps_days = "/{competition_id}/days"
    camps_create = "/create"
    camps_update = "/update/{competition_id}"
    camps_patch = "/{competition_id}"
    camps_delete = "/delete/{competition_id}"
    camps_day = "/{competition_id}/days/{day}"
    camps_update_day = "/update_day/{competition_id}"

    # ofp_results
    ofp_all_categories = "/categories"
    ofp_detail = "/{ofp_id}"
    ofp_create = "/create"
    ofp_list = "/"
    ofp_update = "/update/{ofp_id}"
    ofp_delete = "/delete/{ofp_id}"
    ofp_get_graphic_data = "/graphic_data"

    # coach
    coach_list = "/"
    coach_detail = "/{coach_id}"
    coach_create = "/create"
