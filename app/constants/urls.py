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
    ofp_detail = "/get/{ofp_id}"
    ofp_create = "/create"
    ofp_list = "/"
    ofp_update = "/update/{ofp_id}"
    ofp_delete = "/delete/{ofp_id}"
    ofp_get_graphic_data = "/graphic_data/"

    # sfp_results
    sfp_all_categories = "/categories"
    sfp_detail = "/get/{sfp_id}"
    sfp_create = "/create"
    sfp_list = "/"
    sfp_update = "/update/{sfp_id}"
    sfp_delete = "/delete/{sfp_id}"
    sfp_get_graphic_data = "/graphic_data/"

    # ant_params
    ant_params_detail = "/get/{params_id}"
    ant_params_create = "/create"
    ant_params_list = "/"
    ant_params_update = "/update/{params_id}"
    ant_params_delete = "/delete/{params_id}"
    ant_params_get_graphic_data = "/graphic_data/"

    # notes
    note_detail = "/get/{note_id}"
    note_create = "/create"
    note_list = "/"
    note_update = "/update/{note_id}"
    note_delete = "/delete/{note_id}"

    # comprehensive_examination
    comprehensive_examination_detail = "/get/{exam_id}"
    comprehensive_examination_create = "/create"
    comprehensive_examination_list = "/"
    comprehensive_examination_update = "/update/{exam_id}"
    comprehensive_examination_delete = "/delete/{exam_id}"

    # med_examination
    med_examination_detail = "/get/{exam_id}"
    med_examination_create = "/create"
    med_examination_list = "/"
    med_examination_update = "/update/{exam_id}"
    med_examination_delete = "/delete/{exam_id}"

    # coach
    coach_list = "/"
    coach_detail = "/{coach_id}"
    coach_create = "/create"
